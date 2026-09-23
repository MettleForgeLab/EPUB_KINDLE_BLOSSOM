from __future__ import annotations
import argparse
import io
import json
import os
from pathlib import Path
import zipfile

import pytest
from PIL import Image
from mfl_adapter.core import (
    AdapterError,Publication,NS,canonical,digest,xml,fresh_output,load_profile,
    bind_profile,only,package_report,read_zip,safe_member,resolve_member,write_epub,
)
from mfl_adapter.render import geometry_checks,optimize_png,plan_vertical_footprint

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/"profiles/bht_milestone_001.json"
PROFILE2=ROOT/"profiles/bht_milestone_002.json"
MASTER_ENV=os.environ.get("MFL_TEST_MASTER")
RUN_ENV=os.environ.get("MFL_TEST_RUN")

def mini_members():
    return {
      "mimetype":b"application/epub+zip",
      "META-INF/container.xml":b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/package.opf"/></rootfiles></container>',
      "OEBPS/package.opf":b'<package xmlns="http://www.idpf.org/2007/opf" version="3.0"><metadata/><manifest><item id="a" href="a.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="a"/></spine></package>',
      "OEBPS/a.xhtml":b'<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Test</title></head><body><h1 id="h">Test</h1><p><a href="#h">Return</a></p></body></html>',
    }

@pytest.fixture
def small(tmp_path):
    p=tmp_path/"book.epub";write_epub(p,mini_members());return p

def test_valid_hash_and_manifest(small):
    p=Publication(small,digest(small.read_bytes()))
    assert p.spine==["OEBPS/a.xhtml"]
    p.unchanged()

def test_wrong_hash_stops(small):
    with pytest.raises(AdapterError,match="SHA-256 mismatch"):
        Publication(small,"0"*64)

def test_expected_hash_required(small):
    with pytest.raises(AdapterError,match="expected EPUB SHA"):
        Publication(small,"")

@pytest.mark.parametrize("name",["../escape","/abs","C:/temp","x\\y","x/../../escape"])
def test_zip_paths_refused(name):
    with pytest.raises(AdapterError):
        safe_member(name)

def test_entity_refused():
    with pytest.raises(AdapterError,match="DTD/entity"):
        xml(b'<!DOCTYPE x [<!ENTITY e SYSTEM "file:///etc/passwd">]><x>&e;</x>')

def test_html5_doctype_allowed():
    assert xml(b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"/>') is not None

def test_external_dtd_refused():
    with pytest.raises(AdapterError,match="DTD/entity"):
        xml(b'<!DOCTYPE html SYSTEM "https://example.invalid/schema.dtd"><html/>')

def test_output_existing_refused(tmp_path):
    out=tmp_path/"present";out.mkdir();f=out/"keep";f.write_text("intact")
    with pytest.raises(AdapterError,match="already exists"):
        with fresh_output(out,[]):pass
    assert f.read_text()=="intact"

def test_failed_transaction_has_no_published_output(tmp_path):
    out=tmp_path/"run"
    with pytest.raises(RuntimeError):
        with fresh_output(out,[]) as stage:
            (stage/"partial").write_text("not published")
            raise RuntimeError("deliberate")
    assert not out.exists()

def test_protected_input_under_output_refused(tmp_path):
    with pytest.raises(AdapterError,match="protected"):
        with fresh_output(tmp_path/"new",[tmp_path/"new"/"input.epub"]):pass

def test_successful_transaction(tmp_path):
    out=tmp_path/"run"
    with fresh_output(out,[]) as stage:(stage/"record").write_text("done")
    assert (out/"record").read_text()=="done"

def test_link_resolution():
    assert resolve_member("OEBPS/entry.xhtml","#h")==("OEBPS/entry.xhtml","h")
    assert resolve_member("OEBPS/entry.xhtml","other.xhtml#s")==("OEBPS/other.xhtml","s")
    assert resolve_member("OEBPS/entry.xhtml","https://example.invalid/#a")== (None,"a")

def test_broken_idref_is_error():
    m=mini_members()
    m["OEBPS/a.xhtml"]=m["OEBPS/a.xhtml"].replace(b'href="#h"',b'href="#absent"')
    with pytest.raises(AdapterError,match="Broken fragment"):package_report(m)

def test_broken_aria_is_error():
    m=mini_members()
    m["OEBPS/a.xhtml"]=m["OEBPS/a.xhtml"].replace(b'<p>',b'<p aria-labelledby="absent">')
    with pytest.raises(AdapterError,match="accessibility"):package_report(m)

def test_duplicate_ids_are_error():
    m=mini_members()
    m["OEBPS/a.xhtml"]=m["OEBPS/a.xhtml"].replace(b'<p>',b'<p id="h">')
    with pytest.raises(AdapterError,match="Duplicate"):package_report(m)

def test_zip_deterministic(small,tmp_path):
    second=tmp_path/"second.epub";write_epub(second,mini_members())
    assert small.read_bytes()==second.read_bytes()

def test_profile_loads_and_routes_four():
    p=load_profile(PROFILE)
    assert len(p["components"])==4
    assert [c["route"] for c in p["components"]]==["FIELD PLATE","MEDIUM PLATE","SIMPLIFY LIVE","LIVE"]

def test_modified_render_css_stops(tmp_path):
    import shutil
    p=tmp_path/"profile";shutil.copytree(ROOT/"profiles",p)
    with (p/"field-render.css").open("a") as f:f.write("\nchanged")
    with pytest.raises(AdapterError,match="Render CSS hash"):
        load_profile(p/"bht_milestone_001.json")

def test_locked_text_hash_sees_punctuation():
    a=xml(b'<p>Gravity is not command.</p>')
    b=xml(b'<p>Gravity is not command!</p>')
    assert canonical(a)!=canonical(b)

def test_palette_is_not_silently_promoted(tmp_path):
    (tmp_path/"plates").mkdir();(tmp_path/"diagnostics").mkdir()
    im=Image.new("RGB",(64,64))
    im.putdata([(x*4,y*4,(x+y)*2) for y in range(64) for x in range(64)])
    b=io.BytesIO();im.save(b,format="PNG")
    r=optimize_png(b.getvalue(),tmp_path/"plates"/"sample.png")
    assert not r["palette_pixel_identical"]
    assert r["selected"]=="lossless RGB"
    assert Image.open(tmp_path/"plates"/"sample.png").convert("RGB").tobytes()==im.tobytes()

def test_geometry_can_fail():
    m={"children":[
      {"cls":cls,"rect":{"x":x,"y":y,"w":20,"h":20}}
      for cls,x,y in [("center",50,50),("place north",50,90),
                      ("place south",50,10),("place east",90,50),("place west",10,50)]
    ]}
    assert not geometry_checks("compass",m)["north_above"]

@pytest.mark.skipif(not MASTER_ENV,reason="Set MFL_TEST_MASTER for exact BHT integration tests.")
def test_master_integration():
    p=load_profile(PROFILE);pub=Publication(MASTER_ENV,p["master_sha256"])
    d,bind=bind_profile(pub,p)
    from mfl_adapter.core import locked_regions
    assert len(d.xpath("//x:figure",namespaces=NS))==69
    assert len(locked_regions(d))==94
    assert len(bind)==4
    pub.unchanged()

@pytest.mark.skipif(not MASTER_ENV or not RUN_ENV,reason="Set MFL_TEST_MASTER and MFL_TEST_RUN.")
def test_run_independently_verifies():
    from mfl_adapter.__main__ import verify
    verify(argparse.Namespace(run=RUN_ENV,epub=MASTER_ENV))

@pytest.mark.skipif(not RUN_ENV,reason="Set MFL_TEST_RUN.")
def test_probe_is_small_not_full_book():
    run=Path(RUN_ENV)
    profile=load_profile(next((run/"profile").glob("*.json")))
    probe=run/profile.get("output_epub","MFL_BHT_COMPONENT_PROBE.epub")
    if not probe.exists() and (run/"MFL_BHT_FOUR_CASE_PROBE_001.epub").exists():
        probe=run/"MFL_BHT_FOUR_CASE_PROBE_001.epub"
    m=read_zip(probe)
    docs=[xml(b) for n,b in m.items() if n.endswith(".xhtml")]
    expected_figures=len(profile["components"])
    expected_sources=sum(1 for c in profile["components"] if c.get("source_xpath"))
    assert sum(len(d.xpath("//x:figure",namespaces=NS)) for d in docs)==expected_figures
    assert sum(len(d.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," canonical-copy ")]')) for d in docs)==expected_sources
    assert not any(b"display:none" in b.replace(b" ",b"") for n,b in m.items() if n.endswith(".css"))


def test_second_batch_profile_loads_and_routes_four():
    p=load_profile(PROFILE2)
    assert p["profile_version"]==2
    assert p["mode"]=="component-extract-probe"
    assert [c["route"] for c in p["components"]]==["MEDIUM PLATE","SMALL PLATE","SIMPLIFY LIVE","MEDIUM PLATE"]
    assert p["quality_policy"]["vertical_footprint"]["maximum_bundle_fraction"]==pytest.approx(.72)

def test_vertical_footprint_scales_tall_plate_and_reserves_caption():
    component={
        "key":"tall","display_width_percent":100,"minimum_display_width_percent":30,
        "display_max_em":40
    }
    profile={"quality_policy":{
        "small_viewport_px":320,"page_padding_px":12,"base_font_px":16,
        "vertical_footprint":{
            "viewport_width_px":320,"viewport_height_px":800,"page_padding_px":12,
            "maximum_bundle_fraction":.60,"caption_reserve_px":70,
            "description_link_reserve_px":30,"breathing_reserve_px":20,
            "keep_together_when_safe":True
        }
    }}
    plan=plan_vertical_footprint(component,{"width":1000,"height":2000},profile)
    assert plan["planned_width_percent"] < 100
    assert plan["estimated_bundle_height_px"] <= plan["bundle_height_budget_px"] + .5
    assert plan["keep_together_eligible"] is True

def test_vertical_footprint_refuses_below_component_minimum():
    component={
        "key":"too-tall","display_width_percent":100,"minimum_display_width_percent":80,
        "display_max_em":40
    }
    profile={"quality_policy":{
        "small_viewport_px":320,"page_padding_px":12,"base_font_px":16,
        "vertical_footprint":{
            "viewport_width_px":320,"viewport_height_px":500,"page_padding_px":12,
            "maximum_bundle_fraction":.50,"caption_reserve_px":100,
            "description_link_reserve_px":50,"breathing_reserve_px":20,
            "keep_together_when_safe":True
        }
    }}
    with pytest.raises(AdapterError,match="minimum display width"):
        plan_vertical_footprint(component,{"width":1000,"height":3000},profile)
