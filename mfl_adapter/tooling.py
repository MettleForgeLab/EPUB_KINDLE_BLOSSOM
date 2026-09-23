"""Discovery of optional external publishing tools.

Discovery is read-only. Nothing here downloads, installs, or runs a validator.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from pathlib import Path
import shutil


@dataclass(frozen=True)
class ToolDiscovery:
    name: str
    available: bool
    invocation: str | None
    source: str | None
    expected_version: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _existing(path: str | os.PathLike | None) -> str | None:
    if not path:
        return None
    p = Path(path).expanduser()
    if p.is_file():
        return str(p.resolve())
    return None


def discover_command(
    name: str,
    executable_names: tuple[str, ...],
    *,
    explicit: str | None = None,
    env_var: str | None = None,
    project_candidates: tuple[Path, ...] = (),
    expected_version: str | None = None,
) -> ToolDiscovery:
    found = _existing(explicit)
    if found:
        return ToolDiscovery(
            name, True, found, "explicit", expected_version
        )

    if env_var:
        found = _existing(os.environ.get(env_var))
        if found:
            return ToolDiscovery(
                name, True, found, f"environment:{env_var}",
                expected_version
            )

    for executable in executable_names:
        found = shutil.which(executable)
        if found:
            return ToolDiscovery(
                name, True, str(Path(found).resolve()),
                "PATH", expected_version
            )

    for candidate in project_candidates:
        found = _existing(candidate)
        if found:
            return ToolDiscovery(
                name, True, found, "project-local",
                expected_version
            )

    return ToolDiscovery(
        name, False, None, None, expected_version
    )


def discover_epubcheck(
    project_root: str | os.PathLike,
    explicit: str | None = None,
) -> ToolDiscovery:
    root = Path(project_root)

    candidates = (
        root / "tools" / "epubcheck" / "epubcheck.bat",
        root / "tools" / "epubcheck" / "epubcheck.jar",
    )

    return discover_command(
        "EPUBCheck",
        ("epubcheck", "epubcheck.bat"),
        explicit=explicit,
        env_var="MFL_EPUBCHECK",
        project_candidates=candidates,
        expected_version="5.4.0",
    )


def discover_ace(
    project_root: str | os.PathLike,
    explicit: str | None = None,
) -> ToolDiscovery:
    root = Path(project_root)

    candidates = (
        root / "tools" / "ace" / "ace.cmd",
        root / "tools" / "ace" / "ace.exe",
    )

    return discover_command(
        "Ace by DAISY",
        ("ace", "ace.cmd"),
        explicit=explicit,
        env_var="MFL_ACE",
        project_candidates=candidates,
        expected_version="1.4.6",
    )


def discover_optional_tools(
    project_root: str | os.PathLike,
) -> dict:
    root = Path(project_root)

    return {
        "epubcheck": discover_epubcheck(root).to_dict(),
        "ace": discover_ace(root).to_dict(),
        "calibre": discover_command(
            "Calibre ebook-convert",
            ("ebook-convert", "ebook-convert.exe"),
        ).to_dict(),
        "sigil": discover_command(
            "Sigil",
            ("sigil", "sigil.exe"),
        ).to_dict(),
        "kindle_previewer": discover_command(
            "Kindle Previewer",
            (
                "kindlepreviewer",
                "kindlepreviewer.exe",
                "KindlePreviewer.exe",
            ),
        ).to_dict(),
    }
