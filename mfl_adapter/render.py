"""Offline Chromium rendering of exact source components plus explicit render-only treatments."""
from __future__ import annotations
import base64
import copy
import io
import importlib.metadata
import math
import os
from pathlib import Path
import platform
import shutil

from PIL import Image, ImageChops, ImageStat, ImageCms
from playwright.sync_api import sync_playwright
from lxml import etree as E
from .core import (AdapterError,NS,digest,require,detached,only,resolve_member,dump)

LOAD_XML = """s => {
 const d=new DOMParser().parseFromString(s,"application/xhtml+xml");
 if(d.querySelector("parsererror")) throw Error("Browser XML parse failed");
 document.replaceChild(document.importNode(d.documentElement,true),document.documentElement);
}"""

MEASURE = """e => {
 const root=e.getBoundingClientRect();
 const rect=r=>({x:r.x-root.x,y:r.y-root.y,w:r.width,h:r.height});
 const texts=[];
 const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);
 while(walker.nextNode()){
   const n=walker.currentNode, p=n.parentElement, t=n.textContent.trim();
   if(!t || !p)continue;
   const s=getComputedStyle(p); if(s.display==="none"||s.visibility==="hidden")continue;
   const range=document.createRange(); range.selectNodeContents(n);
   for(const r of range.getClientRects()) if(r.width&&r.height)
     texts.push({text:t,font_px:parseFloat(s.fontSize),font_family:s.fontFamily,
                 color:s.color,rect:rect(r)});
 }
 const children=[...e.querySelectorAll("*")].map(n=>{
   const r=n.getBoundingClientRect(),s=getComputedStyle(n);
   return {tag:n.tagName,cls:n.getAttribute("class")||"",
           text:(n.innerText||n.textContent||"").trim(),
           display:s.display,position:s.position,rect:rect(r)};
 }).filter(v=>v.rect.w&&v.rect.h);
 const transparent=s=>s==="transparent"||s==="rgba(0, 0, 0, 0)";
 let n=e, backdrop="rgb(255, 255, 255)";
 while(n){const s=getComputedStyle(n);if(!transparent(s.backgroundColor)){backdrop=s.backgroundColor;break;}n=n.parentElement;}
 return {width:root.width,height:root.height,backdrop,root_style:{
   display:getComputedStyle(e).display,position:getComputedStyle(e).position,
   background:getComputedStyle(e).background},text_boxes:texts,children};
}"""

def browser_executable(explicit=None):
    if explicit:
        require(Path(explicit).is_file(),f"Chromium executable unavailable: {explicit}")
        return str(Path(explicit).resolve())
    return shutil.which("chromium") or shutil.which("chromium-browser") or None

def render_xml(pub,docname):
    d=copy.deepcopy(pub.docs[docname])
    # Data URLs refer only to exact locally packaged image bytes. No internet fetch.
    for image in d.xpath("//x:img[@src]",namespaces=NS):
        name,_=resolve_member(docname,image.get("src"))
        require(name in pub.members,"External image is not permitted in offline render.")
        image.set("src","data:image/png;base64,"+base64.b64encode(pub.members[name]).decode())
    require(not d.xpath('//x:link[@rel="stylesheet"]',namespaces=NS),
            "v0.1 render profile requires embedded CSS; external-CSS publications can be inspected, not rendered yet.")
    return E.tostring(d,encoding="unicode")

def launch(p,executable=None):
    args=[]
    if hasattr(os,"geteuid") and os.geteuid()==0: args.append("--no-sandbox")
    return p.chromium.launch(headless=True,executable_path=browser_executable(executable),args=args)

def load(page, content):
    page.route("**/*",lambda route:route.abort())  # renderer has no internet dependency
    page.evaluate(LOAD_XML, content)
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(150)

def metrics(page,selector):
    el=page.locator(selector)
    require(el.count()==1,f"Browser selector not unique: {selector}")
    el.scroll_into_view_if_needed()
    return el, el.evaluate(MEASURE)

def capture_bounds(m):
    """Return the root box expanded to visible descendant/text overflow."""
    min_x=0.0; min_y=0.0; max_x=float(m["width"]); max_y=float(m["height"])
    for item in [*m.get("children",[]),*m.get("text_boxes",[])]:
        r=item["rect"]
        if not r["w"] or not r["h"]: continue
        min_x=min(min_x,float(r["x"])); min_y=min(min_y,float(r["y"]))
        max_x=max(max_x,float(r["x"])+float(r["w"]))
        max_y=max(max_y,float(r["y"])+float(r["h"]))
    return {"x":min_x,"y":min_y,"width":max_x-min_x,"height":max_y-min_y}

def capture(page,element,m,allow_overflow=False,path=None):
    bounds=capture_bounds(m)
    overflow=(bounds["x"] < -0.5 or bounds["y"] < -0.5 or
              bounds["width"] > m["width"]+1 or bounds["height"] > m["height"]+1)
    if overflow:
        require(allow_overflow,
                "Visible component content overflows its root box; profile must explicitly allow bounded visual overflow.")
        require(bounds["width"] <= m["width"]*1.35 and bounds["height"] <= m["height"]*1.35,
                "Allowed visual overflow exceeds the renderer safety limit.")
    box=element.bounding_box()
    require(box is not None,"Component has no browser bounding box.")
    clip={"x":box["x"]+bounds["x"],"y":box["y"]+bounds["y"],
          "width":bounds["width"],"height":bounds["height"]}
    raw=page.screenshot(path=str(path) if path else None,clip=clip,
                        animations="disabled",caret="hide",omit_background=False)
    return raw,bounds,overflow

def geometry_checks(key,m):
    byclass={v["cls"]:v for v in m["children"] if v["cls"]}
    def mid(cls):
        r=byclass[cls]["rect"];return r["x"]+r["w"]/2,r["y"]+r["h"]/2
    if key=="compass":
        cx,cy=mid("center"); nx,ny=mid("place north"); ex,ey=mid("place east")
        sx,sy=mid("place south");wx,wy=mid("place west")
        return {"north_above":ny<cy,"south_below":sy>cy,"west_left":wx<cx,
                "east_right":ex>cx,"north_south_centered":abs(nx-cx)<2 and abs(sx-cx)<2}
    if key=="jules-field":
        cx,cy=mid("field-center")
        return {"arrived_upper_left":mid("field-node n1")[0]<cx and mid("field-node n1")[1]<cy,
                "surrounding_upper_right":mid("field-node n2")[0]>cx and mid("field-node n2")[1]<cy,
                "uncertainty_left":mid("field-node n3")[0]<cx,
                "pressure_right":mid("field-node n4")[0]>cx,
                "consequence_below":mid("field-node n5")[1]>cy,
                "remain_visible_below":mid("field-node n6")[1]>cy}
    return {}

def deterministic_png_bytes(image):
    """Encode pixels without volatile renderer/session metadata.

    A fresh Pillow image is constructed from pixel data so ICC profiles,
    text chunks, timestamps, DPI hints, and other source metadata cannot
    leak into the admitted plate artifact.

    The encoding parameters are fixed. Given the same Pillow/zlib runtime
    and the same pixels/palette, this produces the same PNG bytes.
    """
    if image.mode == "P":
        clean=Image.frombytes("P",image.size,image.tobytes())
        palette=image.getpalette()
        require(palette is not None,"Palette image is missing its palette.")
        clean.putpalette(palette)
    elif image.mode in ("L","RGB","RGBA"):
        clean=Image.frombytes(image.mode,image.size,image.tobytes())
    else:
        converted=image.convert("RGB")
        clean=Image.frombytes("RGB",converted.size,converted.tobytes())

    buf=io.BytesIO()
    clean.save(
        buf,
        format="PNG",
        optimize=False,
        compress_level=9,
    )
    return buf.getvalue()


def optimize_png(raw, dest):
    with Image.open(io.BytesIO(raw)) as im:
        rgb=im.convert("RGB")

        lossless=deterministic_png_bytes(rgb)

        with Image.open(io.BytesIO(lossless)) as check:
            admitted=check.convert("RGB")
            require(
                ImageChops.difference(rgb,admitted).getbbox() is None,
                "Lossless optimizer changed pixels.",
            )

        pal=rgb.quantize(
            colors=256,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.NONE,
        )

        quantized=deterministic_png_bytes(pal)

        diff=ImageChops.difference(rgb,pal.convert("RGB"))
        pixel_identical=diff.getbbox() is None

        chosen=(
            quantized
            if pixel_identical and len(quantized)<len(lossless)
            else lossless
        )

        dest.write_bytes(chosen)

        preview=(
            dest.parent.parent
            /"diagnostics"
            /(dest.stem+"-palette-REVIEW-ONLY.png")
        )
        preview.write_bytes(quantized)

        gray=rgb.convert("L")
        gray_path=preview.with_name(
            dest.stem+"-grayscale-SIMULATION.png"
        )
        gray_path.write_bytes(deterministic_png_bytes(gray))

        return {
            "source_capture_bytes":len(raw),
            "lossless_rgb_bytes":len(lossless),
            "palette_candidate_bytes":len(quantized),
            "palette_pixel_identical":pixel_identical,
            "palette_max_channel_error":max(
                x[1] for x in diff.getextrema()
            ),
            "palette_mean_absolute_error":ImageStat.Stat(diff).mean,
            "selected":(
                "palette pixel-identical"
                if chosen==quantized
                else "lossless RGB"
            ),
            "selected_bytes":len(chosen),
            "selected_sha256":digest(chosen),
            "color_space":(
                "opaque RGB; renderer ICC metadata stripped; "
                "deterministic PNG encoding"
            ),
            "png_metadata_policy":"pixel content only",
            "width":rgb.width,
            "height":rgb.height,
        }

def plan_vertical_footprint(component, optimization, profile):
    """Plan displayed plate width against a reference viewport and live-caption reserve.

    This is an engineering budget, not a Kindle pagination promise. The output is
    later measured again in the assembled probe before a keep-together class is
    considered safe.
    """
    q=profile.get("quality_policy",{})
    policy=q.get("vertical_footprint")
    base_font=float(q.get("base_font_px",16))
    requested_percent=float(component.get("display_width_percent",100))
    if not policy:
        small=float(q["small_viewport_px"])-2*float(q["page_padding_px"])
        requested=min(small*requested_percent/100,
                      float(component.get("display_max_em",10_000))*base_font)
        return {
            "policy_active":False,
            "viewport_width_px":q.get("small_viewport_px"),
            "viewport_height_px":None,
            "available_width_px":small,
            "requested_width_percent":requested_percent,
            "planned_width_percent":100*requested/small,
            "planned_display_width_px":requested,
            "estimated_image_height_px":requested*optimization["height"]/optimization["width"],
            "live_text_reserve_px":0,
            "bundle_height_budget_px":None,
            "estimated_bundle_height_px":None,
            "keep_together_eligible":False,
        }
    viewport_w=float(policy["viewport_width_px"])
    viewport_h=float(policy["viewport_height_px"])
    padding=float(policy.get("page_padding_px",q.get("page_padding_px",0)))
    available=max(1,viewport_w-2*padding)
    requested=available*requested_percent/100
    if component.get("display_max_em"):
        requested=min(requested,float(component["display_max_em"])*base_font)
    budget=viewport_h*float(policy["maximum_bundle_fraction"])
    live_reserve=(
        float(policy.get("caption_reserve_px",0))
        +float(policy.get("description_link_reserve_px",0))
        +float(policy.get("breathing_reserve_px",0))
    )
    max_image_h=max(1,budget-live_reserve)
    aspect=optimization["width"]/optimization["height"]
    width_by_height=max_image_h*aspect
    planned=max(1,min(requested,width_by_height,available))
    planned_percent=100*planned/available
    min_percent=float(component.get("minimum_display_width_percent",0))
    require(planned_percent+1e-6>=min_percent,
            f"{component['key']} cannot meet vertical-footprint budget without shrinking below "
            f"its minimum display width ({planned_percent:.1f}% < {min_percent:.1f}%).")
    image_h=planned/aspect
    estimated=image_h+live_reserve
    safe=estimated<=budget+0.5
    require(safe,f"Vertical footprint planning failed for {component['key']}.")
    return {
        "policy_active":True,
        "viewport_width_px":viewport_w,
        "viewport_height_px":viewport_h,
        "available_width_px":available,
        "requested_width_percent":requested_percent,
        "planned_width_percent":planned_percent,
        "planned_display_width_px":planned,
        "estimated_image_height_px":image_h,
        "live_text_reserve_px":live_reserve,
        "bundle_height_budget_px":budget,
        "estimated_bundle_height_px":estimated,
        "keep_together_eligible":bool(policy.get("keep_together_when_safe",True) and safe),
        "policy_note":"Engineering footprint budget only; Kindle pagination still requires human/Previewer verification.",
    }

def render_plates(pub,profile,out,executable=None):
    from .profile_planning import byte_budget_status

    (out/"plates").mkdir();(out/"diagnostics").mkdir()
    content=render_xml(pub,profile["reading_document"])
    results=[]
    with sync_playwright() as p:
        browser=launch(p,executable)
        version=browser.version
        for c in profile["components"]:
            if "PLATE" not in c["route"]:continue
            # Exact source reference rendered before the label-legibility overlay.
            page=browser.new_page(viewport=profile["canonical_viewport"],device_scale_factor=1)
            load(page,content)
            el,before=metrics(page,c["render_selector"])
            _,before_capture,before_overflow=capture(
                page,el,before,c.get("allow_visual_overflow",False),
                out/"diagnostics"/f"{c['key']}-MASTER-REFERENCE.png")
            before["capture_bounds"]=before_capture
            before["visual_overflow_captured"]=before_overflow
            page.add_style_tag(content=c["_render_css"])
            el,after=metrics(page,c["render_selector"])
            after_capture=capture_bounds(after)
            ratio=c["source_width_px"]/after_capture["width"]
            page.close()
            require(ratio<=8,"Requested raster resolution exceeds v0.1 renderer scale limit.")
            page=browser.new_page(viewport=profile["canonical_viewport"],device_scale_factor=ratio)
            load(page,content)
            page.add_style_tag(content=c["_render_css"])
            el,after=metrics(page,c["render_selector"])
            # Background of crop comes from nearest opaque source ancestor, not guessed by designer.
            page.add_style_tag(content=c["render_selector"]+" { background-color: "+after["backdrop"]+" !important; }")
            el,after=metrics(page,c["render_selector"])
            require(after["text_boxes"],"Plate contains no measured text.")
            tol=1.25
            clipped=[t for t in after["text_boxes"] if
                     t["rect"]["x"] < -tol or t["rect"]["y"] < -tol or
                     t["rect"]["x"]+t["rect"]["w"]>after["width"]+tol or
                     t["rect"]["y"]+t["rect"]["h"]>after["height"]+tol]
            if clipped:
                require(c.get("allow_visual_overflow",False),
                        f"Visible label clipping in {c['key']}: {clipped}")
            relation=geometry_checks(c["key"],after)
            require(all(relation.values()),f"Relational geometry failed for {c['key']}")
            # Check displayed text using the browser's line-break aware innerText.
            displayed=" ".join(el.inner_text().split())
            for label in c["required_labels"]:
                require(label in displayed,f"Missing label in plate: {label}")
            raw,final_capture,overflow_captured=capture(
                page,el,after,c.get("allow_visual_overflow",False))
            after["capture_bounds"]=final_capture
            after["visual_overflow_captured"]=overflow_captured
            # Fractional DPR can add one edge pixel. Record the tiny final resampling.
            im=Image.open(io.BytesIO(raw)).convert("RGB")
            original_size=im.size
            if im.width != c["source_width_px"]:
                im=im.resize((c["source_width_px"],round(im.height*c["source_width_px"]/im.width)),Image.Resampling.LANCZOS)
                buf=io.BytesIO();im.save(buf,format="PNG");raw=buf.getvalue()
            plate=out/"plates"/f"{c['key']}.png"
            opt=optimize_png(raw,plate)

            byte_status,byte_utilization=byte_budget_status(
                opt["selected_bytes"],
                c.get("byte_budget"),
            )

            footprint=plan_vertical_footprint(c,opt,profile)
            min_font=min(t["font_px"] for t in after["text_boxes"])
            display_px=footprint["planned_display_width_px"]
            effective=min_font*display_px/after["capture_bounds"]["width"]
            local_legible=effective>=profile["quality_policy"]["minimum_effective_label_px"]
            require(local_legible,
                    f"{c['key']} fails profile's effective label-size floor at its planned display footprint "
                    f"({effective:.2f}px). Increase the allowed footprint or explicitly revise render-only label layout; "
                    "more source pixels alone do not help.")
            results.append({
                "key":c["key"],"route":c["route"],"selector":c["render_selector"],
                "reference":before,"derivative":after,"geometry_assertions":relation,
                "render_css_file":c["render_css_file"],"render_css_sha256":c["render_css_sha256"],
                "render_transform":c["render_transform"],"source_pixel_capture_size":original_size,
                "crop_rule":("Component box expanded only to explicitly allowed visible overflow; live caption excluded." if overflow_captured else "Exact component box, excluding live caption; intentional internal negative space retained."),
                "optimization":opt,"minimum_effective_label_px_at_reference":effective,
                "provisional_local_legibility_floor_pass":local_legible,
                "vertical_footprint":footprint,
                "budget_bytes":c.get("byte_budget"),
                "byte_status":byte_status,
                "byte_budget_utilization":byte_utilization,
                "within_budget":(
                    c.get("byte_budget") is None
                    or opt["selected_bytes"]<=c["byte_budget"]
                ),
                "human_visual_acceptance":"open","kindle_rendering":"not tested",
            })
            page.close()
        browser.close()
    return {"browser":"Chromium "+version,"platform":platform.platform(),
            "runtime_versions":{k:importlib.metadata.version(k) for k in ("playwright","Pillow","lxml")},
            "reference_renderer":"XML DOMParser into a blank page; packaged images embedded as data URLs. No external resource requests allowed.",
            "font_limit":"Uses installed fallback fonts, no font binaries bundled. Different machines may produce different raster bytes.",
            "plates":results}
