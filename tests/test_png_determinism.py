from __future__ import annotations

import io
import struct

from PIL import Image

from mfl_adapter.render import (
    deterministic_png_bytes,
    optimize_png,
)


def png_chunks(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"

    pos=8
    chunks=[]

    while pos < len(data):
        length=struct.unpack(">I",data[pos:pos+4])[0]
        kind=data[pos+4:pos+8].decode("ascii")
        payload=data[pos+8:pos+8+length]

        chunks.append((kind,payload))
        pos += 12 + length

    return chunks


def test_deterministic_png_is_byte_identical_and_metadata_clean():
    image=Image.new(
        "RGB",
        (37,29),
        (21,72,143),
    )

    first=deterministic_png_bytes(image)
    second=deterministic_png_bytes(image)

    assert first == second

    names=[
        kind
        for kind,payload in png_chunks(first)
    ]

    assert names[0] == "IHDR"
    assert names[-1] == "IEND"

    assert "iCCP" not in names
    assert "tEXt" not in names
    assert "zTXt" not in names
    assert "tIME" not in names


def test_optimizer_converges_identical_pixels_despite_input_icc(tmp_path):
    image=Image.new(
        "RGB",
        (48,32),
        (43,91,177),
    )

    def source_png(icc_bytes):
        buf=io.BytesIO()

        image.save(
            buf,
            format="PNG",
            icc_profile=icc_bytes,
        )

        return buf.getvalue()

    raw_a=source_png(b"A"*128)
    raw_b=source_png(b"B"*128)

    assert raw_a != raw_b

    plates=tmp_path/"plates"
    diagnostics=tmp_path/"diagnostics"

    plates.mkdir()
    diagnostics.mkdir()

    dest_a=plates/"a.png"
    dest_b=plates/"b.png"

    result_a=optimize_png(raw_a,dest_a)
    result_b=optimize_png(raw_b,dest_b)

    assert dest_a.read_bytes() == dest_b.read_bytes()
    assert (
        result_a["selected_sha256"]
        == result_b["selected_sha256"]
    )

    names=[
        kind
        for kind,payload in png_chunks(dest_a.read_bytes())
    ]

    assert "iCCP" not in names
    assert result_a["png_metadata_policy"] == "pixel content only"
