"""Basic integration checks against the official OsdagBridge checkout."""

import importlib.util
import os
from pathlib import Path
import sys

# Candidate resolution for official OsdagBridge checkout:
# 1. Environment variable OSDAGBRIDGE_ROOT
# 2. Sibling directory relative to project root (e.g. scratch or OsdagQAWork)
# 3. Documents/OsdagQAWork/OsdagBridge
candidate_roots = []
if "OSDAGBRIDGE_ROOT" in os.environ:
    candidate_roots.append(Path(os.environ["OSDAGBRIDGE_ROOT"]).resolve())
project_root = Path(__file__).resolve().parents[2]
candidate_roots.append((project_root.parent / "OsdagBridge").resolve())
candidate_roots.append((Path.home() / "Documents" / "OsdagQAWork" / "OsdagBridge").resolve())

OFFICIAL_ROOT = candidate_roots[0]
for cr in candidate_roots:
    try:
        if cr.is_dir():
            OFFICIAL_ROOT = cr
            break
    except OSError:
        continue


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
