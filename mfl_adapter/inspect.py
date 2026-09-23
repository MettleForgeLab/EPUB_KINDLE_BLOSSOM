"""Rule-based risk inventory. Routing is explicit profile data, not inferred authority."""
from __future__ import annotations
import re
import tinycss2
import cssselect2
from .core import NS, record_node

def css_inventory(doc):
    matcher=cssselect2.Matcher();rules=[];errors=[]
    def walk(tokens, context, sheet):
        for token in tokens:
            if token.type=="at-rule" and token.content is not None:
                walk(tinycss2.parse_rule_list(token.content,skip_comments=True,skip_whitespace=True),
                     context+[f"@{token.at_keyword} "+tinycss2.serialize(token.prelude).strip()],sheet)
            elif token.type=="qualified-rule":
                selector=tinycss2.serialize(token.prelude).strip()
                declarations=tinycss2.serialize(token.content).strip()
                idx=len(rules)
                rules.append({"sheet":sheet,"line":token.source_line,
                              "context":context,"selector":selector,"declarations":declarations})
                try:
                    for sel in cssselect2.compile_selector_list(selector):
                        matcher.add_selector(sel,idx)
                except cssselect2.SelectorError as exc:
                    errors.append({"selector":selector,"error":str(exc)})
    for num,style in enumerate(doc.xpath("//x:style",namespaces=NS),1):
        walk(tinycss2.parse_stylesheet(style.text or "",skip_comments=True,skip_whitespace=True),[],num)
    wrapper=cssselect2.ElementWrapper.from_xml_root(doc)
    matches={}
    for el in wrapper.iter_subtree():
        hits={hit[-1] for hit in matcher.match(el)}
        matches[el.etree_element]=hits
    return rules,matches,errors

def plan(pub,p,doc,bindings):
    rules,matches,errors=css_inventory(doc)
    decisions=[]
    for c,fig,source in bindings:
        # Include ancestor rules as well as descendants: inheritance/cascade matters.
        elements=list(fig.iter())+list(fig.iterancestors())
        hits=sorted(set().union(*(matches.get(el,set()) for el in elements)))
        matching=[rules[i] for i in hits]
        declarations=" ".join(r["declarations"] for r in matching).lower()
        signals=[]
        patterns={
            "grid layout rule":r"display\s*:\s*grid",
            "absolute positioning rule":r"position\s*:\s*absolute",
            "gradient rule":r"(?:radial|linear)-gradient",
            "transform rule":r"transform\s*:",
            "fixed/minimum height rule":r"(?:min-height|height)\s*:",
            "display:none rule":r"display\s*:\s*none",
        }
        for name,pat in patterns.items():
            if re.search(pat,declarations):signals.append(name)
        decisions.append({
            "key":c["key"],"route":c["route"],"reason":c["reason"],
            "routing_authority":"explicit human-reviewable four-case profile",
            "source":record_node(doc,fig),
            "source_copy":record_node(doc,source) if source is not None else None,
            "css_signals":signals,
            "matching_rule_candidates":matching,
            "cascade_limit":"Static selector matches include conditional media rules and inherited rules; browser-computed values are recorded separately.",
            "display_max_em":c.get("display_max_em"),
            "render_source_width_px":c.get("source_width_px"),
            "render_transform":c.get("render_transform"),
        })
    return {"status":"prototype routing only","automatic_semantic_classification":False,
            "profile_sha256":p["_profile_sha256"],"components":decisions,
            "css_parse_warnings":errors}
