"""
Pytest configuration and shared test fixtures for OsdagBridge QA suite.
"""

import os
import sys
import json
from pathlib import Path

# Safe pytest import with fallback
try:
    import pytest
except ImportError:
    class _PytestShim:
        @staticmethod
        def fixture(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
    pytest = _PytestShim()

# Ensure root directory and osdagbridge_core are discoverable
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from osdagbridge_core.models import BridgeProject


@pytest.fixture(scope="session")
def project_root() -> Path:
    return ROOT_DIR


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
        data = json.load(f)
        return data.get("test_cases", [])


@pytest.fixture
def reference_irc_data(reference_design_json_path) -> dict:
    with open(reference_design_json_path, "r", encoding="utf-8") as f:
        return json.load(f)
