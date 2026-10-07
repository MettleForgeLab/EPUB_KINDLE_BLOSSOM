from __future__ import annotations

import pytest

from mfl_adapter.core import AdapterError
from mfl_adapter.render import capture


def test_capture_overflow_error_names_component():
    metrics = {
        "width": 100,
        "height": 100,
        "children": [
            {
                "rect": {
                    "x": 0,
                    "y": 0,
                    "w": 112,
                    "h": 10,
                }
            }
        ],
        "text_boxes": [],
    }

    with pytest.raises(AdapterError) as excinfo:
        capture(
            None,
            None,
            metrics,
            allow_overflow=False,
            label="east-provisional-plan",
        )

    message = str(excinfo.value)

    assert message.startswith("east-provisional-plan: ")
    assert "Visible component content overflows its root box" in message
