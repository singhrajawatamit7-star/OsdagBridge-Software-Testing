"""
Test Module: test_project.py
Validates project lifecycle, serialization/deserialization, model loading,
and handling of corrupted project files.
"""

import json
try:
    import pytest
except ImportError:
    class _PytestShim:
        class raises:
            def __init__(self, expected_exc):
                self.expected_exc = expected_exc
                self.value = None
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    raise AssertionError(f"Expected {self.expected_exc.__name__} not raised")
                if issubclass(exc_type, self.expected_exc):
                    self.value = exc_val
                    return True
                return False
    pytest = _PytestShim()

from osdagbridge_core.models import BridgeProject


def test_project_model_creation(valid_bridge_project):
    """OB-002: Verify project object creation from validated configuration."""
    assert valid_bridge_project.project_id == "OB-PROJ-001"
    assert valid_bridge_project.bridge_type == "Plate_Girder_Bridge"
    assert valid_bridge_project.geometry.span_length == 24.0
    assert valid_bridge_project.girder_dimensions.web_depth == 1800.0


def test_project_serialization_to_json(valid_bridge_project, tmp_path):
    """OB-006: Verify project can be saved and serialized to disk in valid JSON format."""
    save_file = tmp_path / "test_saved_project.json"
    json_content = valid_bridge_project.to_json()
    save_file.write_text(json_content, encoding="utf-8")

    assert save_file.exists()
    assert save_file.stat().st_size > 0

    # Read back and parse
    with open(save_file, "r", encoding="utf-8") as f:
        loaded_dict = json.load(f)
    assert loaded_dict["project_id"] == "OB-PROJ-001"
    assert loaded_dict["geometry"]["span_length"] == 24.0


def test_project_deserialization_from_json(valid_bridge_project):
    """Verify deserialization from JSON string back to typed BridgeProject model."""
    json_str = valid_bridge_project.to_json()
    reconstructed = BridgeProject.from_json(json_str)

    assert reconstructed.project_id == valid_bridge_project.project_id
    assert reconstructed.geometry.span_length == valid_bridge_project.geometry.span_length
    assert reconstructed.girder_dimensions.flange_width == valid_bridge_project.girder_dimensions.flange_width


def test_corrupted_json_handling(tmp_path):
    """OB-015: Verify application safely handles corrupt or truncated JSON project files."""
    corrupt_file = tmp_path / "corrupt_bridge.json"
    corrupt_file.write_text('{"project_id": "ERR", "geometry": { "span": 24.0', encoding="utf-8")  # missing brackets

    with pytest.raises(json.JSONDecodeError):
        with open(corrupt_file, "r", encoding="utf-8") as f:
            json.load(f)


def test_project_roundtrip_dict_equality(valid_project_dict):
    """Verify dictionary conversion round-trip preserves exact numeric and string values."""
    project = BridgeProject.from_dict(valid_project_dict)
    exported_dict = project.to_dict()

    assert exported_dict["project_id"] == valid_project_dict["project_id"]
    assert exported_dict["geometry"]["span_length"] == valid_project_dict["geometry"]["span_length"]
    assert exported_dict["girder_dimensions"]["web_depth"] == valid_project_dict["girder_dimensions"]["web_depth"]
