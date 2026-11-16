"""Basic integration checks against the official OsdagBridge checkout."""

import importlib.util
import os
from pathlib import Path
import sys

DEFAULT_OFFICIAL_PATH = Path.home() / "Documents" / "OsdagQAWork" / "OsdagBridge"
OFFICIAL_ROOT = Path(
    os.environ.get("OSDAGBRIDGE_ROOT", str(DEFAULT_OFFICIAL_PATH))
).resolve()


def test_official_repository_exists():
    assert OFFICIAL_ROOT.is_dir(), (
        f"Set OSDAGBRIDGE_ROOT to the official OsdagBridge directory. Looked at: {OFFICIAL_ROOT}"
    )


def test_official_source_exists():
    source = OFFICIAL_ROOT / "src" / "osdagbridge"
    assert source.is_dir(), "Official application source was not found."


def test_official_package_is_discoverable():
    source = OFFICIAL_ROOT / "src"
    sys.path.insert(0, str(source))
    spec = importlib.util.find_spec("osdagbridge")
    assert spec is not None, "Official package cannot be discovered."
    locations = spec.submodule_search_locations or []
    expected = (source / "osdagbridge").resolve()
    assert any(
        Path(location).resolve() == expected
        for location in locations
    ), "Package is not resolving to the official source."


def test_official_core_is_discoverable():
    source = OFFICIAL_ROOT / "src"
    sys.path.insert(0, str(source))
    spec = importlib.util.find_spec("osdagbridge.core")
    assert spec is not None, "Official core package was not found."
