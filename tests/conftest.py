"""Shared fixtures for OsdagBridge QA tests."""
import json
import os
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Official OsdagBridge Application Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def project_root():
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def official_root():
    value = os.environ.get("OSDAGBRIDGE_ROOT")
    if not value:
        # Check standard default locations before failing
        candidates = [
            PROJECT_ROOT.parent / "OsdagBridge",
            Path.home() / "Documents" / "OsdagQAWork" / "OsdagBridge",
        ]
        for c in candidates:
            try:
                if c.is_dir():
                    value = str(c)
                    break
            except OSError:
                pass
    if not value:
        pytest.fail(
            "OSDAGBRIDGE_ROOT is not set. "
            "Set it to the official OsdagBridge checkout."
        )
    root = Path(value).resolve()
    if not root.is_dir():
        pytest.fail(f"Official repository not found: {root}")
    return root


@pytest.fixture(scope="session")
def official_source(official_root):
    source = official_root / "src"
    if not (source / "osdagbridge").is_dir():
        pytest.fail("Official src/osdagbridge directory is missing.")
    return source


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sample_24m_data(project_root):
    path = project_root / "test_data" / "valid_inputs" / "24m_plate_girder.json"
    assert path.is_file(), f"Missing test fixture: {path}"
    return load_json(path)


@pytest.fixture
def sample_16m_data(project_root):
    path = project_root / "test_data" / "valid_inputs" / "16m_single_lane.json"
    assert path.is_file(), f"Missing test fixture: {path}"
    return load_json(path)


# ---------------------------------------------------------------------------
# Independent QA Reference Utility Fixtures (Decoupled from Official Source)
# ---------------------------------------------------------------------------
@pytest.fixture
def valid_project_dict(project_root):
    """Base dictionary loaded from test_data/valid_inputs.json for QA utility tests."""
    path = project_root / "test_data" / "valid_inputs.json"
    return load_json(path)


@pytest.fixture
def valid_bridge_payload(valid_project_dict):
    """Payload fixture for QA reference validator and solver testing."""
    return valid_project_dict


@pytest.fixture
def valid_bridge_project(valid_project_dict):
    """BridgeProject object for QA reference solver verification."""
    from osdagbridge_core.models import BridgeProject
    return BridgeProject.from_dict(valid_project_dict)


@pytest.fixture
def reference_irc_data(project_root):
    """IRC:24-2010 design handbook benchmark values for reference comparison."""
    path = project_root / "test_data" / "reference_design_irc.json"
    if not path.is_file():
        path = project_root / "test_data" / "sample_projects" / "reference_design_irc.json"
    return load_json(path)


@pytest.fixture
def invalid_test_cases(project_root):
    """Negative boundary fixtures for QA validator boundary testing."""
    path = project_root / "test_data" / "invalid_inputs.json"
    if path.is_file():
        return load_json(path).get("test_cases", [])
    return []
