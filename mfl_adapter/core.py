"""Immutable EPUB inspection and integrity checks. No network access."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import zipfile
from collections import Counter
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit, unquote
from tempfile import TemporaryDirectory
import posixpath

from lxml import etree as E

X = "http://www.w3.org/1999/xhtml"
EPUB = "http://www.idpf.org/2007/ops"
OPF = "http://www.idpf.org/2007/opf"
DC = "http://purl.org/dc/elements/1.1/"
NS = {"x": X, "opf": OPF, "dc": DC}
LOCK_CLASSES = ("canonical-copy", "activation-copy", "instruction-copy")

class AdapterError(RuntimeError):
    """A failed custody, scope, or package invariant."""

def require(condition, message):
    if not condition:
        raise AdapterError(message)

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def xml(data: bytes):
    # Input publication must not depend on external entities or script execution.
    safe = re.sub(br"<!DOCTYPE\s+html\s*>", b"", data, flags=re.I)
    require(b"<!DOCTYPE" not in safe.upper() and b"<!ENTITY" not in safe.upper(),
            "DTD/entity-bearing XML is outside the v0.1 safe profile.")
    parser = E.XMLParser(recover=False, remove_blank_text=False,
                         resolve_entities=False, no_network=True, huge_tree=False)
    try:
        return E.fromstring(data, parser)
    except E.XMLSyntaxError as exc:
        raise AdapterError(f"Strict XML parse failed: {exc}") from exc

def canonical(el) -> bytes:
    return E.tostring(el, method="c14n", exclusive=True, with_comments=True)

def detached(el):
    result = copy.deepcopy(el)
    result.tail = None
    return result

def text(el) -> str:
    """Logical text with <br> and element boundaries separated; no OCR."""
    return " ".join(" ".join(el.itertext()).split())

def exact(el) -> str:
    """Exact XML serialization for diagnostic records, not a source file."""
    return E.tostring(el, encoding="unicode", with_tail=False)

def has_class(el, name):
    return name in el.get("class", "").split()

def only(doc, xpath, label="target"):
    nodes = doc.xpath(xpath, namespaces=NS)
    require(len(nodes) == 1, f"{label}: expected exactly one node, found {len(nodes)}.")
    return nodes[0]

def record_node(doc, el):
    return {
        "xpath": doc.getroottree().getpath(el),
        "line": el.sourceline,
        "tag": E.QName(el).localname,
        "attributes": dict(el.attrib),
        "logical_text": text(el),
        "canonical_sha256": digest(canonical(el)),
    }

def locked_regions(doc):
    nodes = [el for el in doc.iter()
             if isinstance(el.tag, str) and any(has_class(el,c) for c in LOCK_CLASSES)]
    # Exclude any nested match: the outer source-copy root already covers it.
    nodes = [el for el in nodes if not any(a in nodes for a in el.iterancestors())]
    return [record_node(doc, el) for el in nodes]

def safe_member(name):
    require("\\" not in name and not name.startswith("/"),
            f"Unsafe ZIP member path: {name}")
    p = PurePosixPath(name)
    require(name and ".." not in p.parts and ":" not in name,
            f"Unsafe ZIP member path: {name}")
    return name

def resolve_member(current, href):
    p = urlsplit(href)
    if p.scheme or p.netloc:
        return None, p.fragment
    path = unquote(p.path)
    target = posixpath.normpath(posixpath.join(posixpath.dirname(current), path)) if path else current
    safe_member(target)
    return target, unquote(p.fragment)

def read_zip(path: Path):
    with zipfile.ZipFile(path) as z:
        names = [i.filename for i in z.infolist() if not i.is_dir()]
        require(len(names)==len(set(names)), "Duplicate ZIP member names.")
        require(sum(i.file_size for i in z.infolist()) <= 512*1024*1024,
                "Archive exceeds v0.1 uncompressed size limit.")
        for i in z.infolist():
            safe_member(i.filename)
            require(not i.flag_bits & 1, "Encrypted ZIP member is unsupported.")
            require((i.external_attr >> 16) & 0o170000 != 0o120000, "ZIP symlink refused.")
            require(i.file_size <= 128*1024*1024, "ZIP member exceeds v0.1 size limit.")
        require(z.testzip() is None, "ZIP CRC/integrity failure.")
        require(z.infolist()[0].filename=="mimetype" and
                z.infolist()[0].compress_type==zipfile.ZIP_STORED,
                "EPUB mimetype must be first and uncompressed.")
        require(z.read("mimetype")==b"application/epub+zip", "Invalid EPUB mimetype.")
        return {n:z.read(n) for n in names}

class Publication:
    def __init__(self, path, expected_sha):
        self.path=Path(path).resolve()
        require(self.path.is_file(), f"Input file unavailable: {self.path}")
        require(re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha or "") is not None,
                "An explicit 64-digit expected EPUB SHA-256 is required.")
        self.sha256=digest(self.path.read_bytes())
        require(self.sha256==expected_sha.lower(), "EPUB SHA-256 mismatch; no work performed.")
        self.members=read_zip(self.path)
        container=xml(self.members["META-INF/container.xml"])
        paths=container.xpath('//*[local-name()="rootfile"]/@full-path')
        require(len(paths)==1, "v0.1 requires one OPF rootfile.")
        self.opf_name=safe_member(paths[0])
        self.opf=xml(self.members[self.opf_name])
        self.manifest={}
        for item in self.opf.xpath("./opf:manifest/opf:item", namespaces=NS):
            name,_=resolve_member(self.opf_name,item.get("href",""))
            require(name in self.members, f"OPF resource missing: {name}")
            self.manifest[item.get("id")]=(name,item)
        self.spine=[self.manifest[e.get("idref")][0]
                    for e in self.opf.xpath("./opf:spine/opf:itemref", namespaces=NS)]
        self.docs={name:xml(self.members[name]) for name,item in self.manifest.values()
                   if item.get("media-type")=="application/xhtml+xml"}
        require(not any(d.xpath('//*[local-name()="script"]') for d in self.docs.values()),
                "Script-bearing EPUB requires manual inspection; renderer will not execute it.")
        self.nav_names=[name for name,item in self.manifest.values()
                        if "nav" in item.get("properties","").split()]
        self.original_ids={n:d.xpath('//*[@id]/@id') for n,d in self.docs.items()}
        for n,ids in self.original_ids.items():
            require(len(ids)==len(set(ids)),f"Duplicate XML IDs in {n}")
    def unchanged(self):
        require(digest(self.path.read_bytes())==self.sha256,
                "Source EPUB changed during execution.")
    def inventory(self):
        return {
            "epub_sha256":self.sha256,
            "opf":self.opf_name,
            "spine":self.spine,
            "members":[{"path":n,"bytes":len(b),"sha256":digest(b)} for n,b in self.members.items()],
            "documents":[{
                "path":n,"sha256":digest(self.members[n]),
                "figures":[record_node(d,f) for f in d.xpath("//x:figure",namespaces=NS)],
                "source_locks":locked_regions(d),
                "heading_count":len(d.xpath("//x:h1|//x:h2|//x:h3",namespaces=NS)),
                "id_count":len(self.original_ids[n]),
            } for n,d in self.docs.items()],
        }

def load_profile(path):
    path=Path(path).resolve()
    p=json.loads(path.read_text(encoding="utf-8"))
    p["_profile_sha256"]=digest(path.read_bytes())
    require(p.get("profile_version") in (1,2), "Unsupported profile version.")
    require(p.get("mode") in ("four-case-extract-probe","component-extract-probe"),
            "Only isolated component probes are implemented.")
    components=p.get("components",[])
    require(1 <= len(components) <= 12, "Probe profile requires between 1 and 12 routed cases.")
    require(len({c["key"] for c in components})==len(components), "Duplicate component keys.")
    supported=("SMALL PLATE","MEDIUM PLATE","FIELD PLATE","OPENING PLATE","SIMPLIFY LIVE","LIVE")
    for c in components:
        require(re.fullmatch(r"[a-z0-9-]+",c["key"]) is not None, "Unsafe component key.")
        require(c["route"] in supported, f"Unsupported route: {c['route']}")
        if "PLATE" in c["route"]:
            require(c.get("source_width_px"), f"Plate route missing source_width_px: {c['key']}")
            require(0 < c.get("display_width_percent",100) <= 100,
                    f"Unsafe display width percent: {c['key']}")
            require(c.get("byte_budget",0) > 0, f"Plate route missing byte budget: {c['key']}")
        if "render_css_file" in c:
            f=(path.parent / c["render_css_file"]).resolve()
            require(f.is_relative_to(path.parent), "Profile CSS escapes profile directory.")
            b=f.read_bytes()
            require(digest(b)==c["render_css_sha256"],f"Render CSS hash mismatch for {c['key']}")
            c["_render_css"]=b.decode("utf-8")
    fp=p.get("quality_policy",{}).get("vertical_footprint")
    if fp:
        require(0 < fp.get("maximum_bundle_fraction",0) < 1,
                "vertical_footprint maximum_bundle_fraction must be between 0 and 1.")
        require(fp.get("viewport_width_px",0) > 0 and fp.get("viewport_height_px",0) > 0,
                "vertical_footprint viewport must be positive.")
    return p

def bind_profile(pub, p):
    require(pub.sha256==p["master_sha256"],"Profile names a different presentation authority.")
    require(digest(pub.members[p["reading_document"]])==p["reading_document_sha256"],
            "Packaged reading document does not match the profile.")
    doc=pub.docs[p["reading_document"]]
    bindings=[]
    for c in p["components"]:
        fig=only(doc,c["figure_xpath"],c["key"])
        require(E.QName(fig).localname=="figure","Routed target must be a figure.")
        require(digest(canonical(fig))==c["figure_canonical_sha256"],
                f"Source figure drift: {c['key']}")
        caps=fig.xpath("./x:figcaption",namespaces=NS)
        require(len(caps)==1 and caps[0].get("id"),"Each routed figure needs one identified caption.")
        source=None
        if c.get("source_xpath"):
            source=only(doc,c["source_xpath"],c["key"]+" source")
            require(digest(canonical(source))==c["source_canonical_sha256"],"Source-copy drift.")
        if c.get("visual_xpath"):
            visual=only(fig,c["visual_xpath"],c["key"]+" visual")
            require(not visual.xpath('.//x:a|.//*[@data-source-index or @data-editorial-id]',
                                     namespaces=NS),
                    "Plate visual contains links or source/editorial identities; manual route needed.")
            ids=visual.xpath('.//*[@id]')
            if ids:
                require(c.get("allow_local_svg_ids") is True,
                        "Plate visual contains IDs; allow only explicitly reviewed SVG-local IDs.")
                for node in ids:
                    require(E.QName(node).namespace=="http://www.w3.org/2000/svg" or
                            any(E.QName(a).namespace=="http://www.w3.org/2000/svg" for a in node.iterancestors()),
                            "Non-SVG ID found inside plate visual.")
            require(not any(has_class(visual,n) for n in LOCK_CLASSES),
                    "Operational source cannot be routed to an image.")
        bindings.append((c,fig,source))
    return doc,bindings

@contextmanager
def fresh_output(output, protected):
    """Publish completed runs atomically. Never erase/reuse an existing run."""
    output=Path(output).resolve()
    require(not output.exists(),f"Output already exists; choose a fresh run folder: {output}")
    for p in protected:
        pp=Path(p).resolve()
        require(output != pp and not pp.is_relative_to(output),
                "Output folder would contain a protected input.")
    output.parent.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory(prefix=".mfl-stage-",dir=output.parent) as temp:
        stage=Path(temp)/"run";stage.mkdir()
        yield stage
        stage.rename(output)

def dump(path, data):
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def package_report(members):
    """Check every XHTML resource/IDREF and every local referenced asset."""
    pubdocs={n:xml(b) for n,b in members.items() if n.endswith(".xhtml")}
    ids={}
    for n,d in pubdocs.items():
        values=d.xpath('//*[@id]/@id')
        require(len(values)==len(set(values)),f"Duplicate IDs in {n}")
        ids[n]=set(values)
    links=0; external=0; aria=0
    for n,d in pubdocs.items():
        for el in d.xpath('//*[@href or @src]'):
            for a in ("href","src"):
                href=el.get(a)
                if href is None:continue
                name,frag=resolve_member(n,href)
                if name is None: external+=1;continue
                require(name in members,f"Broken local resource: {n} -> {href}")
                if frag:require(frag in ids.get(name,set()),f"Broken fragment: {n} -> {href}")
                links+=1
        for el in d.xpath('//*[@aria-labelledby or @aria-describedby]'):
            for a in ("aria-labelledby","aria-describedby"):
                for frag in el.get(a,"").split():
                    require(frag in ids[n],f"Broken accessibility IDREF: {n} -> {frag}")
                    aria+=1
    return {"xhtml_documents":len(pubdocs),"ids":sum(map(len,ids.values())),
            "local_links_and_resources":links,"external_references":external,
            "aria_idrefs":aria,"status":"passed"}

def write_epub(path, members):
    """Stable ZIP order/timestamps; no platform-dependent source-path metadata."""
    with zipfile.ZipFile(path,"w") as z:
        for n,b in members.items():
            safe_member(n)
            zi=zipfile.ZipInfo(n,(2026,9,23,0,0,0))
            zi.create_system=3;zi.external_attr=0o100644<<16
            zi.compress_type=zipfile.ZIP_STORED if n=="mimetype" else zipfile.ZIP_DEFLATED
            z.writestr(zi,b,compresslevel=9)
    actual=read_zip(Path(path))
    require(actual==members,"Reopened probe differs from intended package.")
