"""
Pytest configuration and shared test fixtures for OsdagBridge QA Suite.
Supports testing both official OsdagBridge modules and QA verification utilities.
"""

import os
import sys
import json
from pathlib import Path
import pytest

# Project root directory
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Official OsdagBridge source directory resolution
candidate_paths = []
if "OSDAGBRIDGE_SRC" in os.environ:
    candidate_paths.append(Path(os.environ["OSDAGBRIDGE_SRC"]).resolve())
candidate_paths.append(ROOT_DIR.parent / "OsdagBridge" / "src")
candidate_paths.append(Path.home() / "Documents" / "OsdagQAWork" / "OsdagBridge" / "src")

OFFICIAL_SRC = candidate_paths[0]
for p in candidate_paths:
    try:
        if p.is_dir():
            OFFICIAL_SRC = p
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
            break
    except OSError:
        continue

# Upstream OsdagBridge bug guard (OB-BUG-008):
# Official src/osdagbridge/core/__init__.py has 'from .models import *'
# but models.py is omitted from the official repository source tree.
# We supply a module shim so submodules can be discovered and tested cleanly.
import types
if "osdagbridge.core.models" not in sys.modules:
#    sys.modules["osdagbridge.core.models"] = types.ModuleType("osdagbridge.core.models")


@pytest.fixture(scope="session")
def project_root() -> Path:
    return ROOT_DIR


@pytest.fixture(scope="session")
def official_source_root() -> Path:
    return OFFICIAL_SRC


@pytest.fixture(scope="session")
def sample_24m_path(project_root) -> Path:
    return project_root / "test_data" / "valid_inputs" / "24m_plate_girder.json"


@pytest.fixture(scope="session")
def sample_16m_path(project_root) -> Path:
    return project_root / "test_data" / "valid_inputs" / "16m_single_lane.json"


@pytest.fixture(scope="session")
def sample_invalid_span_path(project_root) -> Path:
    return project_root / "test_data" / "invalid_inputs" / "negative_span.json"


@pytest.fixture
def sample_24m_data(sample_24m_path) -> dict:
    with open(sample_24m_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def sample_16m_data(sample_16m_path) -> dict:
    with open(sample_16m_path, "r", encoding="utf-8") as f:
        return json.load(f)


from osdagbridge_core.models import BridgeProject


@pytest.fixture(scope="session")
def valid_project_json_path(project_root) -> Path:
    return project_root / "test_data" / "valid_inputs.json"


@pytest.fixture(scope="session")
def invalid_project_json_path(project_root) -> Path:
    return project_root / "test_data" / "invalid_inputs.json"


@pytest.fixture(scope="session")
def reference_design_json_path(project_root) -> Path:
    return project_root / "test_data" / "reference_design_irc.json"


@pytest.fixture
def valid_project_dict(valid_project_json_path) -> dict:
    with open(valid_project_json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def valid_bridge_project(valid_project_dict) -> BridgeProject:
    return BridgeProject.from_dict(valid_project_dict)


@pytest.fixture
def invalid_test_cases(invalid_project_json_path) -> list:
    with open(invalid_project_json_path, "r", encoding="utf-8") as f:
        return json.load(f).get("test_cases", [])


@pytest.fixture
def reference_irc_data(reference_design_json_path) -> dict:
    with open(reference_design_json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def official_plate_girder_dto():
    """Returns an instance of the official PlateGirderDTO if available."""
    try:
        from osdagbridge.core.bridge_types.plate_girder.dto import PlateGirderDTO
        return PlateGirderDTO(name="NH48_PlateGirder_24m")
    except ImportError:
        pytest.skip("Official osdagbridge package not found in Python environment.")
