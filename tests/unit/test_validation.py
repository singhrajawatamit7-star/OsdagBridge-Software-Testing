"""
Unit Tests: Input Validation Engine
Validates geometric boundaries, material grades, corrosion allowances,
and error handling per IRC:24 and IS 800 standards.
"""

import pytest
from osdagbridge_core.validator import ProjectValidator


def test_valid_24m_project_payload(sample_24m_data):
    """UT-VAL-01: Verify valid 24m plate girder configuration passes validation."""
    result = ProjectValidator.validate_project_payload(sample_24m_data)
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_valid_16m_single_lane_payload(sample_16m_data):
    """UT-VAL-02: Verify valid 16m single-lane bridge payload passes validation."""
    result = ProjectValidator.validate_project_payload(sample_16m_data)
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_empty_required_project_id(sample_24m_data):
    """UT-VAL-03: Verify empty project_id is caught with ERR_REQUIRED_FIELD_EMPTY."""
    payload = dict(sample_24m_data)
    payload["project_id"] = ""
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_REQUIRED_FIELD_EMPTY" and e["field"] == "project_id" for e in res.errors)


def test_negative_span_rejected(sample_24m_data):
    """UT-VAL-04: Verify negative span length is rejected with ERR_NEGATIVE_OR_ZERO_INPUT."""
    payload = dict(sample_24m_data)
    payload["geometry"] = dict(sample_24m_data["geometry"])
    payload["geometry"]["span_length"] = -24.0
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_NEGATIVE_OR_ZERO_INPUT" for e in res.errors)


def test_zero_span_rejected(sample_24m_data):
    """UT-VAL-05: Verify zero span length is rejected."""
    payload = dict(sample_24m_data)
    payload["geometry"] = dict(sample_24m_data["geometry"])
    payload["geometry"]["span_length"] = 0.0
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_NEGATIVE_OR_ZERO_INPUT" for e in res.errors)


def test_span_lower_boundary_limit(sample_24m_data):
    """UT-VAL-06: Verify span below 5.0m triggers ERR_BELOW_MIN_LIMIT."""
    payload = dict(sample_24m_data)
    payload["geometry"] = dict(sample_24m_data["geometry"])
    payload["geometry"]["span_length"] = 4.2
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_BELOW_MIN_LIMIT" for e in res.errors)


def test_span_upper_boundary_limit(sample_24m_data):
    """UT-VAL-07: Verify span exceeding 60.0m triggers ERR_EXCEEDS_MAX_LIMIT."""
    payload = dict(sample_24m_data)
    payload["geometry"] = dict(sample_24m_data["geometry"])
    payload["geometry"]["span_length"] = 72.0
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_EXCEEDS_MAX_LIMIT" for e in res.errors)


def test_web_thickness_corrosion_limit(sample_24m_data):
    """UT-VAL-08: Verify web thickness below IRC:24 corrosion threshold (8mm) fails."""
    payload = dict(sample_24m_data)
    payload["girder_dimensions"] = dict(sample_24m_data["girder_dimensions"])
    payload["girder_dimensions"]["web_thickness"] = 6.0
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_BELOW_MIN_LIMIT" for e in res.errors)


def test_alphabetic_characters_in_numeric_field(sample_24m_data):
    """UT-VAL-09: Verify string injected in web_depth triggers ERR_INVALID_DATA_TYPE."""
    payload = dict(sample_24m_data)
    payload["girder_dimensions"] = dict(sample_24m_data["girder_dimensions"])
    payload["girder_dimensions"]["web_depth"] = "ALPHA_NOT_NUMERIC"
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_INVALID_DATA_TYPE" for e in res.errors)


def test_unsupported_steel_grade(sample_24m_data):
    """UT-VAL-10: Verify unsupported steel grade triggers ERR_INVALID_STEEL_GRADE."""
    payload = dict(sample_24m_data)
    payload["steel_grade"] = "ASTM_A992_UNSUPPORTED"
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_INVALID_STEEL_GRADE" for e in res.errors)


def test_minimum_two_girders_enforced(sample_24m_data):
    """UT-VAL-11: Verify bridge with single girder triggers ERR_MIN_GIRDERS_REQUIRED."""
    payload = dict(sample_24m_data)
    payload["geometry"] = dict(sample_24m_data["geometry"])
    payload["geometry"]["number_of_main_girders"] = 1
    res = ProjectValidator.validate_project_payload(payload)
    assert res.is_valid is False
    assert any(e["code"] == "ERR_MIN_GIRDERS_REQUIRED" for e in res.errors)


def test_web_slenderness_boundary_warning(sample_24m_data):
    """UT-VAL-12: Verify warning raised when web slenderness d/tw > 200 per IS 800."""
    payload = dict(sample_24m_data)
    payload["girder_dimensions"] = dict(sample_24m_data["girder_dimensions"])
    payload["girder_dimensions"]["web_depth"] = 2000.0
    payload["girder_dimensions"]["web_thickness"] = 8.0  # ratio = 250 > 200
    res = ProjectValidator.validate_project_payload(payload)
    assert any(w["code"] == "WARN_HIGH_SLENDERNESS" for w in res.warnings)
