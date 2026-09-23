from types import SimpleNamespace

from lxml import etree as E

from mfl_adapter.probe import (
    DC,
    EPUB,
    NS,
    OPF,
    ACCESSIBILITY_DISCOVERY_METADATA,
    add_accessibility_discovery_metadata,
    probe_toc,
    publication_language,
)


def test_probe_language_is_derived_from_source_opf():
    package=E.Element("{"+OPF+"}package",nsmap={None:OPF,"dc":DC})
    metadata=E.SubElement(package,"{"+OPF+"}metadata")
    language=E.SubElement(metadata,"{"+DC+"}language")
    language.text="en"

    pub=SimpleNamespace(opf=package)

    assert publication_language(pub) == "en"


def test_probe_accessibility_discovery_metadata_is_truthful_and_bounded():
    package=E.Element("{"+OPF+"}package",nsmap={None:OPF})
    metadata=E.SubElement(package,"{"+OPF+"}metadata")

    add_accessibility_discovery_metadata(metadata)

    actual=[
        (node.get("property"), (node.text or "").strip())
        for node in metadata.findall("{"+OPF+"}meta")
    ]

    assert actual == list(ACCESSIBILITY_DISCOVERY_METADATA)

    properties=[prop for prop,value in actual]

    assert "schema:accessModeSufficient" in properties
    assert "schema:accessibilityFeature" in properties
    assert "schema:accessibilityHazard" in properties

    assert "dcterms:conformsTo" not in properties
    assert "a11y:certifiedBy" not in properties
    assert "a11y:certifierCredential" not in properties
    assert "a11y:certifierReport" not in properties


def test_probe_toc_exposes_matching_aria_role():
    toc=probe_toc()

    assert toc.get("{"+EPUB+"}type") == "toc"
    assert toc.get("role") == "doc-toc"
    assert toc.get("id") == "toc"
