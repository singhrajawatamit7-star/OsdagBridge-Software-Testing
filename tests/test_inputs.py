"""
Test Module: test_inputs.py
Validates input field validation, boundary value conditions, data types,
and negative test cases for OsdagBridge plate girder projects.
"""

try:
    import pytest
except ImportError:
    class _PytestShim:
        pass
    pytest = _PytestShim()

from osdagbridge_core.validator import ProjectValidator


def test_valid_project_input_passes(valid_project_dict):
    """Verify that a standard valid 24m plate girder payload passes validation."""
    result = ProjectValidator.validate_project_payload(valid_project_dict)
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_empty_required_project_name(valid_project_dict):
    """OB-003: Verify leaving required field empty triggers ERR_REQUIRED_FIELD_EMPTY."""
    payload = dict(valid_project_dict)
    payload["project_name"] = "   "  # whitespace only
    result = ProjectValidator.validate_project_payload(payload)
    assert result.is_valid is False
    codes = [e["code"] for e in result.errors]
    assert "ERR_REQUIRED_FIELD_EMPTY" in codes


def test_negative_span_rejected(valid_project_dict):
    """OB-005: Verify negative span length is rejected."""
    payload = dict(valid_project_dict)
    payload["geometry"] = dict(valid_project_dict["geometry"])
    payload["geometry"]["span_length"] = -24.0
    result = ProjectValidator.validate_project_payload(payload)
    assert result.is_valid is False
    codes = [e["code"] for e in result.errors]
    assert "ERR_NEGATIVE_OR_ZERO_INPUT" in codes


def test_zero_span_rejected(valid_project_dict):
    """Verify zero span length is rejected."""
    payload = dict(valid_project_dict)
    payload["geometry"] = dict(valid_project_dict["geometry"])
    payload["geometry"]["span_length"] = 0.0
    result = ProjectValidator.validate_project_payload(payload)
    assert result.is_valid is False
    codes = [e["code"] for e in result.errors]
    assert "ERR_NEGATIVE_OR_ZERO_INPUT" in codes


def test_boundary_values_span(valid_project_dict):
    """OB-004: Test lower and upper boundary values for span (5.0m to 60.0m)."""
    # Min span: 5.0m -> Should pass
    payload_min = dict(valid_project_dict)
    payload_min["geometry"] = dict(valid_project_dict["geometry"])
    payload_min["geometry"]["span_length"] = 5.0
    res_min = ProjectValidator.validate_project_payload(payload_min)
    assert res_min.is_valid is True

    # Below min span: 4.0m -> Should fail
    payload_below = dict(valid_project_dict)
    payload_below["geometry"] = dict(valid_project_dict["geometry"])
    payload_below["geometry"]["span_length"] = 4.0
    res_below = ProjectValidator.validate_project_payload(payload_below)
    assert res_below.is_valid is False
    assert any(e["code"] == "ERR_BELOW_MIN_LIMIT" for e in res_below.errors)

    # Max span: 60.0m -> Should pass
    payload_max = dict(valid_project_dict)
    payload_max["geometry"] = dict(valid_project_dict["geometry"])
    payload_max["geometry"]["span_length"] = 60.0
    res_max = ProjectValidator.validate_project_payload(payload_max)
    assert res_max.is_valid is True

    # Exceeds max span: 75.0m -> Should fail
    payload_above = dict(valid_project_dict)
    payload_above["geometry"] = dict(valid_project_dict["geometry"])
    payload_above["geometry"]["span_length"] = 75.0
    res_above = ProjectValidator.validate_project_payload(payload_above)
    assert res_above.is_valid is False
    assert any(e["code"] == "ERR_EXCEEDS_MAX_LIMIT" for e in res_above.errors)


def test_non_numeric_characters_rejected(valid_project_dict):
    """OB-005: Verify entering alphabetic characters in numeric field is caught."""
    payload = dict(valid_project_dict)
    payload["girder_dimensions"] = dict(valid_project_dict["girder_dimensions"])
    payload["girder_dimensions"]["web_depth"] = "ABC123DEPTH"
    result = ProjectValidator.validate_project_payload(payload)
    assert result.is_valid is False
    codes = [e["code"] for e in result.errors]
    assert "ERR_INVALID_DATA_TYPE" in codes


def test_corrosion_web_thickness_minimum_limit(valid_project_dict):
    """Verify web thickness below IRC:24 corrosion threshold (8.0mm) is rejected."""
    payload = dict(valid_project_dict)
    payload["girder_dimensions"] = dict(valid_project_dict["girder_dimensions"])
    payload["girder_dimensions"]["web_thickness"] = 6.0  # 6mm < 8mm
    result = ProjectValidator.validate_project_payload(payload)
    assert result.is_valid is False
    assert any(e["code"] == "ERR_BELOW_MIN_LIMIT" for e in result.errors)


def test_unsupported_steel_grade_rejected(valid_project_dict):
    """Verify non-standard steel grade is rejected."""
    payload = dict(valid_project_dict)
    payload["steel_grade"] = "UNKNOWN_STEEL_A36"
    result = ProjectValidator.validate_project_payload(payload)
    assert result.is_valid is False
    assert any(e["code"] == "ERR_INVALID_STEEL_GRADE" for e in result.errors)


def test_minimum_girders_count(valid_project_dict):
    """Verify a bridge project requires at least 2 longitudinal main girders."""
    payload = dict(valid_project_dict)
    payload["geometry"] = dict(valid_project_dict["geometry"])
    payload["geometry"]["number_of_main_girders"] = 1
    result = ProjectValidator.validate_project_payload(payload)
    assert result.is_valid is False
    assert any(e["code"] == "ERR_MIN_GIRDERS_REQUIRED" for e in result.errors)


def test_web_slenderness_warning(valid_project_dict):
    """OB-016: Verify warning flagged when web slenderness d/tw exceeds 200."""
    payload = dict(valid_project_dict)
    payload["girder_dimensions"] = dict(valid_project_dict["girder_dimensions"])
    # web depth 2000, web thickness 8 -> slenderness = 250 > 200
    payload["girder_dimensions"]["web_depth"] = 2000.0
    payload["girder_dimensions"]["web_thickness"] = 8.0
    result = ProjectValidator.validate_project_payload(payload)
    assert any(w["code"] == "WARN_HIGH_SLENDERNESS" for w in result.warnings)


def test_negative_fixture_suite(invalid_test_cases):
    """Iterate through invalid_inputs.json fixtures and assert all fail with expected codes."""
    for case in invalid_test_cases:
        cid = case["case_id"]
        expected_code = case["expected_error_code"]
        payload = case["payload"]
        result = ProjectValidator.validate_project_payload(payload)
        assert result.is_valid is False, f"Case {cid} was expected to fail validation but passed."
        error_codes = [e["code"] for e in result.errors]
        assert expected_code in error_codes, f"Case {cid} expected code {expected_code}, got {error_codes}"
