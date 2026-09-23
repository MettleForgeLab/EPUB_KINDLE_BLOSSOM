"""Command line: inspect, build-probe, verify, doctor. Never publishes or edits the master."""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import shutil
import zipfile
import sys
from pathlib import Path

from . import __version__
from .core import (AdapterError,Publication,load_profile,bind_profile,digest,require,dump,
                   fresh_output,package_report,read_zip,xml,canonical,only,NS)
from .inspect import plan

def report_text(pub,profile,render,verification,qa,epub_bytes):
    plate_total=sum(p["optimization"]["selected_bytes"] for p in render["plates"])
    lines=[
        f"# MFL Kindle Visual Adapter {__version__} — Component probe run record","",
        f"**Profile:** `{profile.get('profile_id')}`",
        f"**Scope:** {len(profile['components'])} isolated component treatments; NOT the complete BHT book or a retail Kindle candidate.",
        "**Human acceptance:** open. **Kindle conversion/pagination:** NOT RUN in this environment.",
        "", "## Custody",
        f"- Master EPUB SHA-256: `{pub.sha256}`",
        f"- Packaged reading-document SHA-256: `{profile['reading_document_sha256']}`",
        f"- Routing profile SHA-256: `{profile['_profile_sha256']}`",
        f"- Probe EPUB SHA-256: `{digest(epub_bytes)}`","",
        "## Routed treatments",
    ]
    for i,c in enumerate(profile["components"],1):
        lines.append(f"{i}. **{c['key']} — {c['route']}** — {c['reason']}")
    lines += ["","## Vertical-footprint planning"]
    fp=profile.get("quality_policy",{}).get("vertical_footprint")
    if fp:
        lines += [
            f"- Reference viewport: {fp['viewport_width_px']} × {fp['viewport_height_px']} CSS px.",
            f"- Maximum plate/caption/link bundle: {fp['maximum_bundle_fraction']*100:.1f}% of reference viewport height.",
            f"- Caption reserve: {fp.get('caption_reserve_px',0)} px; description-link reserve: {fp.get('description_link_reserve_px',0)} px; breathing reserve: {fp.get('breathing_reserve_px',0)} px.",
            "- A plate bundle receives keep-together CSS only when the engineering budget says the whole image/caption/link unit fits inside the configured height allowance.",
            "- This budget is local engineering evidence, not a promise about Kindle pagination.",
        ]
    else:
        lines.append("- No active vertical-footprint policy in this profile.")
    for r in render["plates"]:
        o=r["optimization"];v=r["vertical_footprint"]
        lines += [
            f"### {r['key']}",
            f"- Final plate: {o['width']} × {o['height']} px; {o['selected_bytes']:,} bytes; SHA-256 `{o['selected_sha256']}`.",
            f"- Requested display width: {v['requested_width_percent']:.1f}%; planned: {v['planned_width_percent']:.1f}% ({v['planned_display_width_px']:.1f}px at reference width).",
            f"- Estimated image height: {v['estimated_image_height_px']:.1f}px; estimated bundle height: {v['estimated_bundle_height_px'] if v['estimated_bundle_height_px'] is not None else 'n/a'}; budget: {v['bundle_height_budget_px'] if v['bundle_height_budget_px'] is not None else 'n/a'}.",
            f"- Keep-together eligible: {v['keep_together_eligible']}. Effective minimum label size at planned footprint: {r['minimum_effective_label_px_at_reference']:.2f}px.",
            f"- Byte budget: {r['budget_bytes']:,}; within budget: {r['within_budget']}.",
        ]
    lines += [
        "",f"**Selected new plates combined:** {plate_total:,} bytes ({plate_total/1_000_000:.3f} MB).",
        f"**Probe EPUB size:** {len(epub_bytes):,} bytes.","",
        "## Verification",
        f"- Included locked source-copy regions canonically identical: {verification['included_locked_regions']}.",
        f"- Structural package checks: {json.dumps(verification['checks'],ensure_ascii=False)}",
        f"- Local layout samples: {len(qa)}.",
        "- Plate/caption bundles are remeasured at the reference viewport; builds fail if an eligible bundle exceeds its configured footprint budget.",
        "- Links, description round trips and accessibility IDREFs resolve structurally.",
        "- Input hash is rechecked before output publication.",
        "- Local Chromium screenshots are not Kindle Previewer evidence.","",
        "## Boundaries",
        "The retail master is the only presentation input. The probe deliberately omits the rest of the book.",
        "Generated accessibility descriptions remain editorial text pending Porter review.",
        "No KDP upload, publication action, rights decision or full-book conversion occurs here.","",
        "## Next check",
        "Open the generated probe in Kindle Previewer. Judge plate/caption adjacency, intended visual scale, live simplifications, description round trips, and enlarged-text behavior.",
        "**Tool milestone:** local engineering pass only. **Full Kindle build:** not authorized by this record.","",
    ]
    return "\n".join(lines)

def inspect(args):
    p=load_profile(args.profile)
    pub=Publication(args.epub,p["master_sha256"])
    doc,bindings=bind_profile(pub,p)
    with fresh_output(args.out,[pub.path,args.profile]) as out:
        dump(out/"input-inventory.json",pub.inventory())
        dump(out/"routing-plan.json",plan(pub,p,doc,bindings))
        pub.unchanged()
    print(f"Inspection created: {Path(args.out).resolve()}")

def build(args):
    from .render import render_plates
    from .probe import assemble,render_checks
    from .profile_planning import (
        build_findings,
        plan_profile,
        require_pre_render_resolved,
    )
    p=load_profile(args.profile)
    pub=Publication(args.epub,p["master_sha256"])
    doc,bindings=bind_profile(pub,p)
    with fresh_output(args.out,[pub.path,args.profile]) as out:
        dump(out/"input-inventory.json",pub.inventory())
        dump(out/"routing-plan.json",plan(pub,p,doc,bindings))

        pre_device_plan=plan_profile(args.profile)
        dump(
            out/"DEVICE_PLAN_PRE.json",
            pre_device_plan,
        )
        require_pre_render_resolved(pre_device_plan)

        # Store the exact profile and render-only treatments for this run.
        audit_profile={k:v for k,v in p.items() if not k.startswith("_")}
        for c in audit_profile["components"]: c.pop("_render_css",None)
        # Reload: audit copy operations must not consume runtime CSS.
        p=load_profile(args.profile)
        (out/"profile").mkdir()
        (out/"profile"/Path(args.profile).name).write_bytes(Path(args.profile).read_bytes())
        for c in p["components"]:
            if c.get("render_css_file"):
                (out/"profile"/c["render_css_file"]).write_bytes((Path(args.profile).parent/c["render_css_file"]).read_bytes())
        rendering=render_plates(pub,p,out,args.chromium)
        dump(out/"render-metrics.json",rendering)

        post_device_plan=plan_profile(
            args.profile,
            run_dir=out,
        )
        dump(
            out/"DEVICE_PLAN_POST.json",
            post_device_plan,
        )

        findings=build_findings(post_device_plan)
        dump(
            out/"BUILD_FINDINGS.json",
            {
                "schema":"mfl.build-findings/1",
                "finding_count":len(findings),
                "findings":findings,
            },
        )

        members,verification=assemble(pub,p,doc,bindings,out,rendering)
        dump(out/"transformations.json",verification)
        qa=render_checks(members,p,out,args.chromium)
        dump(out/"local-layout-checks.json",qa)
        epub=out/p.get("output_epub","MFL_BHT_COMPONENT_PROBE.epub")
        record=report_text(pub,p,rendering,verification,qa,epub.read_bytes())
        (out/"RUN_RECORD.md").write_text(record,encoding="utf-8")
        pub.unchanged()
        outputs=[{"path":str(f.relative_to(out)).replace("\\","/"),"bytes":f.stat().st_size,"sha256":digest(f.read_bytes())}
                 for f in sorted(out.rglob("*")) if f.is_file()]
        manifest={
            "tool_version":__version__,"status":"bounded component prototype; acceptance open",
            "source_epub_sha256":pub.sha256,"source_book_sha256":p["reading_document_sha256"],
            "profile_sha256":p["_profile_sha256"],
            "probe_sha256":digest(epub.read_bytes()),
            "code_files":[{"path":f.name,"sha256":digest(f.read_bytes())}
                          for f in sorted(Path(__file__).parent.glob("*.py"))],
            "mutated_inputs":False,"kindle_tested":False,
            "outputs":outputs,
        }
        dump(out/"MANIFEST.json",manifest)
        targets=[out/r["path"] for r in outputs]+[out/"MANIFEST.json"]
        (out/"SHA256SUMS.sha256").write_text(
            "".join(f"{digest(f.read_bytes())}  {f.relative_to(out).as_posix()}\n" for f in targets),encoding="utf-8")
        pub.unchanged()
    print(f"Built component probe: {Path(args.out).resolve()}")
    print(json.dumps({"epub_sha256":manifest["probe_sha256"],
                      "master_unchanged":pub.sha256,"kindle_tested":False},indent=2))

def verify(args):
    out=Path(args.run).resolve()
    m=json.loads((out/"MANIFEST.json").read_text(encoding="utf-8"))
    pub=Publication(args.epub,m["source_epub_sha256"])
    for r in m["outputs"]:
        f=(out/r["path"]).resolve()
        require(f.is_relative_to(out),"Manifest path escapes run directory.")
        require(f.is_file() and f.stat().st_size==r["bytes"] and digest(f.read_bytes())==r["sha256"],
                f"Run artifact changed: {r['path']}")
    for line in (out/"SHA256SUMS.sha256").read_text(encoding="utf-8").splitlines():
        wanted,name=line.split("  ",1);f=(out/name).resolve()
        require(f.is_relative_to(out) and f.is_file() and digest(f.read_bytes())==wanted,
                f"Run checksum mismatch: {name}")
    p=load_profile(next((out/"profile").glob("*.json")))
    probe=out/p.get("output_epub","MFL_BHT_COMPONENT_PROBE.epub")
    if not probe.exists() and (out/"MFL_BHT_FOUR_CASE_PROBE_001.epub").exists():
        probe=out/"MFL_BHT_FOUR_CASE_PROBE_001.epub"  # v0.1 compatibility
    require(digest(probe.read_bytes())==m["probe_sha256"],"Probe hash mismatch.")
    contents=read_zip(probe);result=package_report(contents)
    # Re-derive protected reference elements from the authoritative master.
    doc,bindings=bind_profile(pub,p)
    for index,(c,fig,source) in enumerate(bindings,1):
        d=xml(contents[f"OEBPS/{index:02d}-{c['key']}.xhtml"])
        cap=only(d,f'//*[@id="{c["caption_id"]}"]')
        require(canonical(cap)==canonical(only(fig,"./x:figcaption")),"Caption changed.")
        if source is not None:
            actual=only(d,'//x:article[contains(concat(" ",normalize-space(@class)," ")," canonical-copy ")]')
            require(canonical(actual)==canonical(source),"Source excerpt changed.")
        if c["route"]=="LIVE":
            actual=only(d,c["figure_xpath"])
            require(canonical(actual)==canonical(fig),"Existing image figure changed.")
            for image in actual.xpath(".//x:img",namespaces=NS):
                name,_=__import__("mfl_adapter.core",fromlist=["resolve_member"]).resolve_member(p["reading_document"],image.get("src"))
                require(contents[name]==pub.members[name],"White Room image changed.")
    pub.unchanged()
    print(json.dumps({"verification":"passed","kindle_tested":False,"package":result},indent=2))



def plan_profile_cli(args):
    from .profile_planning import plan_profile

    kwargs={
        "run_dir":args.run,
        "reserve_ratio":args.reserve_ratio,
        "overbuilt_headroom":args.overbuilt_headroom,
    }

    if args.devices:
        kwargs["device_keys"]=tuple(args.devices)

    report=plan_profile(
        args.profile,
        **kwargs,
    )

    payload=json.dumps(
        report,
        indent=2,
    )

    if args.out:
        destination=Path(args.out)
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        destination.write_text(
            payload+"\n",
            encoding="utf-8",
        )

    print(payload)
    return 0


def plan_plate_cli(args):
    from .device_profiles import plan_plate

    kwargs = {
        "source_width_px": args.width,
        "source_height_px": args.height,
        "display_fraction": args.display_fraction,
        "reserve_ratio": args.reserve_ratio,
    }

    if args.devices:
        kwargs["device_keys"] = tuple(args.devices)

    report = plan_plate(**kwargs)

    payload = json.dumps(
        report,
        indent=2,
    )

    if args.out:
        destination = Path(args.out)
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        destination.write_text(
            payload + "\n",
            encoding="utf-8",
        )

    print(payload)
    return 0


def validate(args):
    from .validation import run_validation

    root=Path(__file__).resolve().parent.parent

    with fresh_output(
        args.out,
        [Path(args.epub)],
    ) as out:
        report=run_validation(
            args.epub,
            project_root=root,
            output_dir=out,
            java=args.java,
            epubcheck=args.epubcheck,
            ace=args.ace,
        )

    print(
        json.dumps(
            {
                "validation":report["overall_automated_status"],
                "epub_sha256":report["publication"]["sha256"],
                "kindle_previewer":"NOT RUN",
                "human_acceptance":"NOT RUN",
            },
            indent=2,
        )
    )

    if report["overall_automated_status"] == "PASS":
        return 0

    if report["overall_automated_status"] == "FINDINGS":
        return 3

    return 2


def doctor(args):
    versions={}
    for name in ("lxml","Pillow","playwright","tinycss2","cssselect2","pytest"):
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:versions[name]="not installed"
    print(json.dumps({"python":sys.version,"versions":versions,
                      "chromium_on_path":shutil.which("chromium"),
                      "kindle_previewer_on_path":shutil.which("kindlepreviewer"),
                      "epubcheck_on_path":shutil.which("epubcheck"),
                      "external_commands_run":False},indent=2))

def main():
    ap=argparse.ArgumentParser(description="MFL visual adapter v0.4 — immutable master / bounded component probes")
    sub=ap.add_subparsers(dest="command",required=True)
    for command,func in (("inspect",inspect),("build-probe",build)):
        p=sub.add_parser(command);p.set_defaults(func=func)
        p.add_argument("--epub",required=True);p.add_argument("--profile",required=True);p.add_argument("--out",required=True)
        if command=="build-probe":p.add_argument("--chromium",default=None)
    p=sub.add_parser("verify");p.set_defaults(func=verify);p.add_argument("--run",required=True);p.add_argument("--epub",required=True)

    p=sub.add_parser("plan-profile")
    p.set_defaults(func=plan_profile_cli)
    p.add_argument("--profile",required=True)
    p.add_argument("--run",default=None)
    p.add_argument(
        "--device",
        dest="devices",
        action="append",
        default=None,
    )
    p.add_argument(
        "--reserve-ratio",
        type=float,
        default=1.25,
    )
    p.add_argument(
        "--overbuilt-headroom",
        type=float,
        default=1.50,
    )
    p.add_argument("--out",default=None)

    p=sub.add_parser("plan-plate")
    p.set_defaults(func=plan_plate_cli)
    p.add_argument("--width",type=int,required=True)
    p.add_argument("--height",type=int,required=True)
    p.add_argument(
        "--display-fraction",
        type=float,
        required=True,
    )
    p.add_argument(
        "--device",
        dest="devices",
        action="append",
        default=None,
    )
    p.add_argument(
        "--reserve-ratio",
        type=float,
        default=1.25,
    )
    p.add_argument("--out",default=None)

    p=sub.add_parser("validate")
    p.set_defaults(func=validate)
    p.add_argument("--epub",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--java",default=None)
    p.add_argument("--epubcheck",default=None)
    p.add_argument("--ace",default=None)

    p=sub.add_parser("doctor");p.set_defaults(func=doctor)
    args=ap.parse_args()
    try:
        return args.func(args) or 0
    except (AdapterError,OSError,ValueError,KeyError,zipfile.BadZipFile) as exc:
        print(f"STOP: {exc}",file=sys.stderr);return 2

if __name__=="__main__":
    import zipfile
    raise SystemExit(main())
