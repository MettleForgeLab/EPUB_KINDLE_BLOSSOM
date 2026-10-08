from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

from PIL import Image

from mfl_adapter.__main__ import audit_publication_cli
from mfl_adapter.core import digest, write_epub
from mfl_adapter.publication_audit import (
    audit_publication,
    load_publication_policy,
)


def _jpeg() -> bytes:
    image=Image.new("RGB",(8,12),(240,240,240))
    buffer=io.BytesIO()
    image.save(buffer,format="JPEG",quality=90)
    return buffer.getvalue()


def _members(*, image_media_type: str="image/jpeg", broken_headers: bool=False):
    headers=(
        ' headers="missing"'
        if broken_headers
        else ""
    )

    return {
        "mimetype":b"application/epub+zip",
        "META-INF/container.xml":(
            b'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            b'<rootfiles><rootfile full-path="OEBPS/package.opf" '
            b'media-type="application/oebps-package+xml"/></rootfiles></container>'
        ),
        "OEBPS/package.opf":(
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
            '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<dc:title>Audit Test</dc:title>'
            '<dc:identifier id="uid">urn:test:audit</dc:identifier>'
            '<dc:language>en</dc:language>'
            '</metadata>'
            '<manifest>'
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
            '<item id="cover-doc" href="cover.xhtml" media-type="application/xhtml+xml"/>'
            '<item id="body" href="body.xhtml" media-type="application/xhtml+xml"/>'
            '<item id="style" href="styles/shared.css" media-type="text/css"/>'
            f'<item id="cover-image" href="assets/cover.jpg" media-type="{image_media_type}" properties="cover-image"/>'
            '</manifest>'
            '<spine><itemref idref="cover-doc"/><itemref idref="body"/></spine>'
            '</package>'
        ).encode("utf-8"),
        "OEBPS/nav.xhtml":(
            b'<html xmlns="http://www.w3.org/1999/xhtml" '
            b'xmlns:epub="http://www.idpf.org/2007/ops">'
            b'<head><title>Navigation</title></head><body>'
            b'<nav epub:type="toc"><ol><li><a href="body.xhtml">Body</a></li></ol></nav>'
            b'<nav epub:type="landmarks"><ol><li><a epub:type="bodymatter" href="body.xhtml">Start</a></li></ol></nav>'
            b'</body></html>'
        ),
        "OEBPS/cover.xhtml":(
            b'<html xmlns="http://www.w3.org/1999/xhtml">'
            b'<head><title>Cover</title><link rel="stylesheet" href="styles/shared.css"/></head>'
            b'<body><img src="assets/cover.jpg" alt="Cover"/></body></html>'
        ),
        "OEBPS/body.xhtml":(
            '<html xmlns="http://www.w3.org/1999/xhtml">'
            '<head><title>Body</title><link rel="stylesheet" href="styles/shared.css"/></head>'
            f'<body><h1 id="body-title">Body</h1><table><tr><td id="cell"{headers}>Text</td></tr></table></body>'
            '</html>'
        ).encode("utf-8"),
        "OEBPS/styles/shared.css":b"body { margin: 0; }\n",
        "OEBPS/assets/cover.jpg":_jpeg(),
    }


def _policy(epub: Path, image: bytes) -> dict:
    return {
        "expected_filename":epub.name,
        "expected_sha256":digest(epub.read_bytes()),
        "expected_bytes":epub.stat().st_size,
        "expected_members":8,
        "expected_manifest_items":5,
        "expected_spine_documents":2,
        "expected_spine":[
            "OEBPS/cover.xhtml",
            "OEBPS/body.xhtml",
        ],
        "expected_toc":[
            {"label":"Body","href":"body.xhtml"},
        ],
        "expected_landmarks":[
            {
                "label":"Start",
                "href":"body.xhtml",
                "type":"bodymatter",
            },
        ],
        "expected_stylesheets":[
            "OEBPS/styles/shared.css",
        ],
        "required_members":[
            "OEBPS/body.xhtml",
        ],
        "forbidden_members":[
            "OEBPS/old.xhtml",
        ],
        "required_assets":[
            {
                "member":"OEBPS/assets/cover.jpg",
                "sha256":digest(image),
                "bytes":len(image),
                "dimensions":[8,12],
                "media_type":"image/jpeg",
            },
        ],
        "required_text":[
            {
                "member":"OEBPS/body.xhtml",
                "text":"Text",
                "count":1,
            },
        ],
        "forbidden_text":[
            {
                "text":"review copy",
            },
        ],
    }


def test_publication_audit_passes_exact_policy(tmp_path):
    epub=tmp_path/"audit.epub"
    members=_members()
    write_epub(epub,members)
    policy=_policy(epub,members["OEBPS/assets/cover.jpg"])

    report=audit_publication(
        epub,
        expected_sha256=digest(epub.read_bytes()),
        policy={"policy_id":"test"},
        platform="test",
        platform_policy=policy,
    )

    assert report["status"]=="PASS"
    assert report["failure_count"]==0
    assert report["package"]["navigation"]["toc"][0]["href"]=="body.xhtml"
    assert report["renderer_review"]=="NOT INFERRED"
    assert report["human_acceptance"]=="NOT INFERRED"


def test_publication_audit_reports_media_type_extension_mismatch(tmp_path):
    epub=tmp_path/"audit.epub"
    write_epub(
        epub,
        _members(image_media_type="image/png"),
    )

    report=audit_publication(
        epub,
        expected_sha256=digest(epub.read_bytes()),
    )

    assert report["status"]=="FAIL"
    assert any(
        check["id"]=="manifest.media_extensions"
        and check["status"]=="FAIL"
        for check in report["checks"]
    )


def test_publication_audit_reports_extended_idref_failure(tmp_path):
    epub=tmp_path/"audit.epub"
    write_epub(
        epub,
        _members(broken_headers=True),
    )

    report=audit_publication(
        epub,
        expected_sha256=digest(epub.read_bytes()),
    )

    assert report["status"]=="FAIL"
    assert report["package"]["extended_idrefs"]["failures"]==[
        {
            "member":"OEBPS/body.xhtml",
            "attribute":"headers",
            "target":"missing",
        }
    ]


def test_publication_audit_reports_policy_residue(tmp_path):
    epub=tmp_path/"audit.epub"
    members=_members()
    members["OEBPS/body.xhtml"]=members["OEBPS/body.xhtml"].replace(
        b"Text",
        b"review copy",
    )
    write_epub(epub,members)
    policy=_policy(epub,members["OEBPS/assets/cover.jpg"])

    report=audit_publication(
        epub,
        expected_sha256=digest(epub.read_bytes()),
        policy={"policy_id":"test"},
        platform="test",
        platform_policy=policy,
    )

    assert report["status"]=="FAIL"
    assert any(
        check["id"].startswith("policy.forbidden_text")
        and check["status"]=="FAIL"
        for check in report["checks"]
    )


def test_publication_audit_cli_writes_report(tmp_path):
    epub=tmp_path/"audit.epub"
    write_epub(epub,_members())
    destination=tmp_path/"audit.json"

    exit_code=audit_publication_cli(
        argparse.Namespace(
            epub=str(epub),
            expected_sha256=digest(epub.read_bytes()),
            policy=None,
            platform=None,
            out=str(destination),
        )
    )

    assert exit_code==0
    report=json.loads(
        destination.read_text(encoding="utf-8")
    )
    assert report["status"]=="PASS"


def test_bht_frozen_release_policy_loads():
    root=Path(__file__).resolve().parents[1]
    policy_path=root/"profiles"/"bht_frozen_releases_001.json"

    policy,apple=load_publication_policy(
        policy_path,
        "apple",
    )
    _,kindle=load_publication_policy(
        policy_path,
        "kindle",
    )

    assert policy["policy_id"]=="bht-frozen-releases-001"
    assert apple["expected_sha256"]=="40ffe038e163a818335af9ba65a1380e84bb5cbfa69ac5eef11d1dc23781757b"
    assert kindle["expected_sha256"]=="225592b811b301200e9477e172269a0099152f1f94701a20bfcfc5961088c9d7"
