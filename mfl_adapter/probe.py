"""Isolated component test book: intentionally NOT a full BHT Kindle edition."""
from __future__ import annotations
import json
from pathlib import Path
from lxml import etree as E
from .core import (X,EPUB,OPF,DC,NS,require,digest,canonical,detached,
                   text,only,resolve_member,package_report,write_epub,xml)
from .render import load,launch,MEASURE
from playwright.sync_api import sync_playwright
import base64

CSS = """/* Test-harness CSS only. No retail CSS is propagated. */
html, body { margin:0; padding:0; }
body { font-family:Georgia,serif; line-height:1.5; padding:0 12px; }
h1 { font-size:1.4em; margin:0.7em 0; }
h2 { font-size:1.25em; margin:1em 0 0.6em; }
h3 { font-size:1.2em; margin:1em 0 0.6em; }
p { margin:0 0 1em; text-indent:0; }
.probe-notice { font:0.82em/1.4 Arial,sans-serif; padding:0.7em 0; border-bottom:1px solid #999; }
.probe-meta { font:0.8em/1.4 Arial,sans-serif; }
.source-excerpt { margin:1.3em 0; }
.canonical-copy p { margin:0 0 1em; }
.line-group span { display:inline; }
figure { margin:1em auto; padding:0; width:100%; }
figure img { display:block; width:100%; height:auto; margin:0 auto; }
figcaption { margin:0.6em 0 0.7em; font:0.88em/1.4 Arial,sans-serif; text-align:left; }
figcaption > span { display:block; margin-bottom:0.25em; font-size:0.9em; font-weight:bold; }
.live-steps { margin:0.8em 0; padding:0 0 0 1.5em; }
.live-steps li { margin:0 0 0.8em; padding:0.6em; border:1px solid #777; }
.figure-held { font-style:italic; }
.probe-nav ol { padding-left:1.3em; }
.probe-nav li { margin:0.5em 0; padding:0.35em 0; }
.probe-nav a, .desc-link a { display:block; }
.desc-link { font-size:0.88em; margin:0.45em 0 0; }
.plate-bundle { width:100%; margin:1em auto; }
.plate-bundle figure { margin:0 auto; }
.plate-bundle.footprint-safe { break-inside:avoid; page-break-inside:avoid; }
.description ul { padding-left:1.3em; }
"""

def el(tag,body=None,**attrs):
    n=E.Element("{"+X+"}"+tag)
    for k,v in attrs.items():n.set(k.replace("_","-"),str(v))
    if body is not None:n.text=body
    return n

def docbytes(title,children):
    d=E.Element("{"+X+"}html",nsmap={None:X,"epub":EPUB})
    d.set("lang","en"); d.set("{http://www.w3.org/XML/1998/namespace}lang","en")
    h=E.SubElement(d,"{"+X+"}head")
    h.append(el("meta",charset="utf-8"));h.append(el("title",title))
    h.append(el("link",rel="stylesheet",type="text/css",href="probe.css"))
    b=E.SubElement(d,"{"+X+"}body")
    for n in children:b.append(n)
    s=E.tostring(d,encoding="unicode")
    import re
    s=re.sub(r"<(div|span|i|b|p|section|article|a)(\s[^<>]*?)?\s*/>",
             lambda m:f"<{m[1]}{m[2] or ''}></{m[1]}>",s)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'+s).encode("utf-8")

def metadata_element(tag, value):
    e=E.Element("{"+DC+"}"+tag);e.text=value;return e


def publication_language(pub):
    values=pub.opf.xpath(
        "./opf:metadata/dc:language/text()",
        namespaces=NS,
    )
    require(values, "Source publication is missing dc:language.")
    language=values[0].strip()
    require(language, "Source publication dc:language is empty.")
    return language


ACCESSIBILITY_DISCOVERY_METADATA = (
    ("schema:accessMode", "textual"),
    ("schema:accessMode", "visual"),
    ("schema:accessModeSufficient", "textual,visual"),
    ("schema:accessibilityFeature", "alternativeText"),
    ("schema:accessibilityFeature", "readingOrder"),
    ("schema:accessibilityFeature", "tableOfContents"),
    ("schema:accessibilityHazard", "none"),
    (
        "schema:accessibilitySummary",
        "Visual diagrams include concise alternative text and linked "
        "extended descriptions in this engineering probe. Human review "
        "of the extended descriptions remains open.",
    ),
)


def add_accessibility_discovery_metadata(meta):
    for prop,value in ACCESSIBILITY_DISCOVERY_METADATA:
        node=E.SubElement(meta,"{"+OPF+"}meta",property=prop)
        node.text=value


def probe_toc():
    toc=el("nav",id="toc",role="doc-toc")
    toc.set("{"+EPUB+"}type","toc")
    return toc


def assemble(pub,profile,doc,bindings,out,render):
    members={"mimetype":b"application/epub+zip",
             "META-INF/container.xml":b'<?xml version="1.0" encoding="UTF-8"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',
             "OEBPS/probe.css":CSS.encode()}
    records=[]; captions=[];sources=[];desc_children=[]
    plate_results={r["key"]:r for r in render.get("plates",[])}
    title=profile.get("probe_title","BHT — MFL Visual Adapter component engineering probe")
    notice=profile.get("probe_notice","ENGINEERING PROBE — isolated samples, not the book and not a retail edition. Source excerpts remain locked. Visual acceptance is open.")
    front=[el("h1",title),el("p",notice,**{"class":"probe-notice"}),
           el("p",f"Built from the verified retail master. Only these {len(profile['components'])} component treatments are tested. Other chapters and navigation are intentionally not included.")]
    nav=el("nav",**{"class":"probe-nav","aria-label":"Component tests"})
    ol=el("ol");nav.append(ol);front.append(nav)
    routes=[]
    for order,(c,fig,source) in enumerate(bindings,1):
        filename=f"{order:02d}-{c['key']}.xhtml";routes.append((filename,c["key"]))
        li=el("li");li.append(el("a",f"{order}. {c['key']} — {c['route']}",href=filename));ol.append(li)
        heading=el("h2",f"{order}. {c['key']} — {c['route']}",id="mfl-case-"+c["key"])
        children=[el("p",notice,**{"class":"probe-notice"}),heading]
        sample=el("section",**{"class":"sample","data-probe-source-standing":"excerpt-only"})
        children.append(sample)
        if source is not None:
            section=el("section",id=c["source_section_id"],**{"class":"source-excerpt"})
            h=only(doc,f'//*[@id="{c["source_section_id"]}"]//x:header/x:h3',"source heading")
            section.append(detached(h))
            section.append(el("p","Locked source excerpt · "+c["source_title"],**{"class":"probe-meta"}))
            section.append(detached(source));sample.append(section)
            sources.append({"key":c["key"],"document":"OEBPS/"+filename,
                            "original_sha256":digest(canonical(source)),"original":source})
        newfig=detached(fig)
        original_caption=only(fig,"./x:figcaption","caption")
        if "PLATE" in c["route"]:
            old=only(newfig,c["visual_xpath"],"visual")
            image=el("img",src="assets/"+c["key"]+".png",alt=c["alt"],
                     **{"class":"mfl-plate","data-mfl-adaptation":c["key"]})
            old.getparent().replace(old,image)
            cap=only(newfig,"./x:figcaption","live caption")
            newfig.remove(cap);newfig.append(cap)
            footprint=plate_results[c["key"]]["vertical_footprint"]
            planned=footprint["planned_width_percent"]
            maxem=c.get("display_max_em")
            style=f"width:{planned:.2f}%;"
            if maxem: style+=f"max-width:{maxem}em;"
            newfig.set("style",style)
            members["OEBPS/assets/"+c["key"]+".png"]=(out/"plates"/(c["key"]+".png")).read_bytes()
            bundle_class="plate-bundle"
            if footprint.get("keep_together_eligible"): bundle_class+=" footprint-safe"
            bundle=el("div",**{"class":bundle_class,
                               "data-mfl-footprint-budget":"active" if footprint.get("policy_active") else "inactive"})
            bundle.append(newfig)
            link=el("p",**{"class":"desc-link"})
            link.append(el("a","Extended description: "+c["key"],
                           href="descriptions.xhtml#mfl-desc-"+c["key"],id="mfl-desc-link-"+c["key"]))
            bundle.append(link);sample.append(bundle)
            description=el("section",id="mfl-desc-"+c["key"],**{"class":"description"})
            description.append(el("h2","Extended description: "+c["key"]))
            description.append(el("p",c["description"]))
            ul=el("ul")
            for lab in c["required_labels"]:ul.append(el("li",lab))
            description.append(ul)
            description.append(el("p","This description is new editorial accessibility text for the probe; Porter review is pending.",
                                  **{"class":"probe-meta"}))
            back=el("p");back.append(el("a","Return to the figure",href=filename+"#mfl-desc-link-"+c["key"]))
            description.append(back);desc_children.append(description)
        elif c["route"]=="SIMPLIFY LIVE":
            old=only(newfig,c["visual_xpath"],"live visual")
            transform=c.get("live_transform")
            if transform:
                item_xpath=transform["item_xpath"]
                orig_steps=old.xpath(item_xpath,namespaces=NS)
                expected=transform["expected"]
                require(len(orig_steps)==len(expected),f"{c['key']} live transform item count differs from profile.")
                for child,want in zip(orig_steps,expected):
                    require(text(child)==want,f"{c['key']} live transform wording/order differs from profile.")
                seq=el(transform.get("container_tag","ol"),
                       **{"class":"live-steps","aria-label":transform.get("aria_label","Ordered editorial relation")})
                for child in orig_steps:
                    row=detached(child)
                    row.tag="{"+X+"}"+transform.get("item_tag","li")
                    row.attrib.clear()
                    seq.append(row)
            else:
                orig_steps=list(old)
                require(len(orig_steps)==len(c["sequence"]),f"{c['key']} sequence item count differs from profile.")
                for child,want in zip(orig_steps,c["sequence"]):
                    require(text(child)==want,f"{c['key']} wording/order differs from profile.")
                seq=el("ol",**{"class":"live-steps","aria-label":c.get("sequence_aria_label","Ordered editorial relation")})
                for child in orig_steps:
                    row=detached(child); row.tag="{"+X+"}li";row.attrib.clear();seq.append(row)
            old.getparent().replace(old,seq)
            sample.append(newfig)
        else:
            for image in newfig.xpath(".//x:img[@src]",namespaces=NS):
                name,_=resolve_member(profile["reading_document"],image.get("src"))
                members[name]=pub.members[name]
            sample.append(newfig)
        footer=el("p");footer.append(el("a","Return to probe contents",href="index.xhtml"))
        children.append(footer)
        members["OEBPS/"+filename]=docbytes(c["key"],children)
        captions.append({"key":c["key"],"document":"OEBPS/"+filename,
                         "id":c["caption_id"],"sha256":digest(canonical(original_caption))})
        r={"key":c["key"],"route":c["route"],"document":"OEBPS/"+filename,
           "source_figure_sha256":digest(canonical(fig)),
           "output_figure_sha256":digest(canonical(newfig)),
           "caption_preserved":digest(canonical(only(newfig,"./x:figcaption")))==digest(canonical(original_caption)),
           "source_wording_changed":False,"source_standing_changed":False,
           "accessibility_change":(
               "Pixel labels have concise alt plus a visible linked description and return link; caption remains live."
               if "PLATE" in c["route"] else
               "Previously aria-hidden editorial diagram becomes exposed ordered live text."
               if c["route"]=="SIMPLIFY LIVE" else "Original image, alt and caption unchanged."),
           "omissions":"This harness intentionally omits the rest of the publication; omission is not a full-book adaptation."}
        if c["route"]=="LIVE":require(canonical(newfig)==canonical(fig),"Existing figure drift.")
        records.append(r)
    members["OEBPS/index.xhtml"]=docbytes(title,front)
    members["OEBPS/descriptions.xhtml"]=docbytes("Probe extended descriptions",desc_children)
    toc=probe_toc()
    toc.append(el("h2","Probe contents"));tl=el("ol");toc.append(tl)
    for f,key in [("index.xhtml","Probe introduction"),*routes,("descriptions.xhtml","Extended descriptions")]:
        li=el("li");li.append(el("a",key,href=f));tl.append(li)
    members["OEBPS/nav.xhtml"]=docbytes("Probe contents",[toc])
    language=publication_language(pub)
    package=E.Element("{"+OPF+"}package",nsmap={None:OPF})
    package.set("version","3.0");package.set("unique-identifier","probe-id")
    package.set("{http://www.w3.org/XML/1998/namespace}lang",language)
    meta=E.SubElement(package,"{"+OPF+"}metadata",nsmap={"dc":DC})
    ident=metadata_element("identifier","urn:mfl:probe:"+digest((pub.sha256+profile["_profile_sha256"]).encode())[:32])
    ident.set("id","probe-id");meta.append(ident)
    meta.append(metadata_element("title",title));meta.append(metadata_element("language",language))
    meta.append(metadata_element("creator","Porter Winston"))
    add_accessibility_discovery_metadata(meta)
    for right in pub.opf.xpath("./opf:metadata/dc:rights",namespaces=NS):meta.append(detached(right))
    mod=E.SubElement(meta,"{"+OPF+"}meta",property="dcterms:modified");mod.text="2026-09-23T00:00:00Z"
    manifest=E.SubElement(package,"{"+OPF+"}manifest");ids={}
    for n in members:
        if not n.startswith("OEBPS/"):continue
        relative=n.removeprefix("OEBPS/");rid="r"+str(len(ids));ids[n]=rid
        mime="application/xhtml+xml" if n.endswith(".xhtml") else "text/css" if n.endswith(".css") else "image/png"
        item=E.SubElement(manifest,"{"+OPF+"}item",id=rid,href=relative)
        item.set("media-type",mime)
        if relative=="nav.xhtml":item.set("properties","nav")
    spine=E.SubElement(package,"{"+OPF+"}spine")
    for f in ["index.xhtml",*[f for f,key in routes],"descriptions.xhtml"]:
        e=E.SubElement(spine,"{"+OPF+"}itemref",idref=ids["OEBPS/"+f])
        if f=="descriptions.xhtml":e.set("linear","no")
    members["OEBPS/package.opf"]=E.tostring(package,encoding="utf-8",xml_declaration=True)
    package_report(members)
    for rec in captions:
        actual=only(xml(members[rec["document"]]),f'//*[@id="{rec["id"]}"]')
        require(digest(canonical(actual))==rec["sha256"],"Caption drift after serialization.")
    for rec in sources:
        d=xml(members[rec["document"]])
        actual=only(d,'//x:article[contains(concat(" ",normalize-space(@class)," ")," canonical-copy ")]')
        require(canonical(actual)==canonical(rec["original"]),"Locked source-copy drift after serialization.")
        del rec["original"]
    write_epub(out/profile.get("output_epub","MFL_BHT_COMPONENT_PROBE.epub"),members)
    return members,{"components":records,"source_copies":sources,"captions":captions,
                    "checks":package_report(members),"included_locked_regions":len(sources),
                    "full_book_source_preservation":"Not claimed: this is an explicitly excerpt-only harness."}

def render_checks(members,profile,out,executable=None):
    """Chromium layout diagnostics, never Kindle Previewer evidence."""
    measurements=[]
    with sync_playwright() as p:
        browser=launch(p,executable)
        for width,height,font in [(320,800,16),(600,900,16),(360,800,24)]:
            for index,c in enumerate(profile["components"],1):
                name=f"OEBPS/{index:02d}-{c['key']}.xhtml"
                d=xml(members[name])
                for link in d.xpath('//x:link[@rel="stylesheet"]',namespaces=NS):
                    link.getparent().replace(link,el("style",members["OEBPS/probe.css"].decode()+
                                                    f"\nbody {{font-size:{font}px;}}"))
                for img in d.xpath("//x:img",namespaces=NS):
                    path,_=resolve_member(name,img.get("src"))
                    img.set("src","data:image/png;base64,"+base64.b64encode(members[path]).decode())
                page=browser.new_page(viewport={"width":width,"height":height})
                load(page,E.tostring(d,encoding="unicode"))
                fig=page.locator(f'figure[aria-labelledby="{c["caption_id"]}"]')
                m=fig.evaluate(MEASURE)
                horizontal=page.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")
                require(horizontal,f"Horizontal overflow in probe {c['key']} at {width}")
                image=fig.locator("img");ratio_pass=None
                if image.count():
                    a=image.evaluate("e=>({w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height,nw:e.naturalWidth,nh:e.naturalHeight})")
                    ratio_pass=abs(a["w"]/a["h"]-a["nw"]/a["nh"])<0.01
                    require(ratio_pass,"Probe image aspect ratio drift.")
                footprint_measurement=None
                if "PLATE" in c["route"]:
                    bundle=page.locator(".plate-bundle")
                    require(bundle.count()==1,f"Expected one plate bundle for {c['key']}.")
                    br=bundle.evaluate("e=>e.getBoundingClientRect().height")
                    fp=profile.get("quality_policy",{}).get("vertical_footprint")
                    if fp and width==fp["viewport_width_px"] and font==profile.get("quality_policy",{}).get("base_font_px",16):
                        budget=fp["viewport_height_px"]*fp["maximum_bundle_fraction"]
                        require(br<=budget+2,
                                f"Measured plate/caption bundle exceeds vertical-footprint budget for {c['key']}: {br:.1f}px > {budget:.1f}px.")
                    footprint_measurement=br
                if c["route"]=="SIMPLIFY LIVE":
                    labels=fig.locator(".live-steps > li").all_inner_texts()
                    expected=(c.get("live_transform") or {}).get("expected",c.get("sequence",[]))
                    require([" ".join(x.split()) for x in labels]==expected,"Live sequence changed in renderer.")
                screenshot=f"{index:02d}-{c['key']}-{width}px-{font}font-CHROMIUM.png"
                page.screenshot(path=str(out/"diagnostics"/screenshot),full_page=True,animations="disabled")
                measurements.append({"case":c["key"],"viewport":[width,height],"font_px":font,
                                     "horizontal_overflow":not horizontal,"image_aspect_preserved":ratio_pass,
                                     "figure_box":[m["width"],m["height"]],"bundle_height_px":footprint_measurement,
                                     "screenshot":screenshot,"kindle_pagination":"not tested"})
                page.close()
        browser.close()
    return measurements
