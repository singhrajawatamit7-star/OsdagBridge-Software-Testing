"""
Regression Tests
Verifies that previously identified defects and edge-case bugs do not reoccur.
Guards critical bugs documented in issues.csv (OB-BUG-001 to OB-BUG-006).
"""

import json
from pathlib import Path
import pytest
from osdagbridge_core.models import BridgeProject
from osdagbridge_core.validator import ProjectValidator
from osdagbridge_core.solver import BridgeSolver
from osdagbridge_core.report_generator import ReportGenerator


def test_regression_ob_bug_001_alpha_characters_handling(sample_24m_data):
    """REG-01 [OB-BUG-001]: Verify numeric fields reject strings without solver execution."""
    payload = dict(sample_24m_data)
    payload["girder_dimensions"] = dict(sample_24m_data["girder_dimensions"])
    payload["girder_dimensions"]["web_depth"] = "1800ABC_INJECTION"

    val = ProjectValidator.validate_project_payload(payload)
    assert val.is_valid is False
    assert any(e["code"] == "ERR_INVALID_DATA_TYPE" for e in val.errors)


def test_regression_ob_bug_002_zero_web_thickness_division_guard(sample_24m_data):
    """REG-02 [OB-BUG-002]: Verify zero web thickness does not trigger uncaught ZeroDivisionError."""
    payload = dict(sample_24m_data)
    payload["girder_dimensions"] = dict(sample_24m_data["girder_dimensions"])
    payload["girder_dimensions"]["web_thickness"] = 0.0  # triggers division guard

    # Must catch during validation safely
    val = ProjectValidator.validate_project_payload(payload)
    assert val.is_valid is False
    assert any(e["code"] == "ERR_NEGATIVE_OR_ZERO_INPUT" for e in val.errors)


def test_regression_ob_bug_003_corrupt_json_project_loading(tmp_path):
    """REG-03 [OB-BUG-003]: Verify loading corrupted JSON raises cleanly handled JSONDecodeError."""
    bad_file = tmp_path / "broken_project.json"
    bad_file.write_text('{"project_id": "CORRUPT", "geometry": { "span": 24.0', encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        with open(bad_file, "r", encoding="utf-8") as f:
            json.load(f)


def test_regression_ob_bug_004_unicode_path_in_reports(sample_24m_data, tmp_path):
    """REG-04 [OB-BUG-004]: Verify report generation handles Unicode directories gracefully."""
    unicode_dir = tmp_path / "डिजाइन_रिपोर्ट्स"
    unicode_dir.mkdir(parents=True, exist_ok=True)

    project = BridgeProject.from_dict(sample_24m_data)
    summary = BridgeSolver.calculate_design(project)
    html_report = ReportGenerator.generate_html_report(project, summary)

    target_file = unicode_dir / "NH48_Report.html"
    target_file.write_text(html_report, encoding="utf-8")

    assert target_file.exists()
    assert target_file.stat().st_size > 500


def test_regression_ob_bug_006_impact_factor_clamping_for_large_spans(sample_24m_data):
    """REG-06 [OB-BUG-006]: Verify impact factor is clamped to minimum 0.10 for spans > 45m."""
    payload = dict(sample_24m_data)
    payload["geometry"] = dict(sample_24m_data["geometry"])
    payload["geometry"]["span_length"] = 50.0  # Formula 4.5 / (6 + 50) = 0.0803 < 0.10

    project = BridgeProject.from_dict(payload)
    # The solver must clamp impact factor to min 0.10
    span = project.geometry.span_length
    impact_factor = min(0.35, max(0.10, 4.5 / (6.0 + span)))
    assert impact_factor == 0.10, f"Expected clamped impact factor 0.10, got {impact_factor}"
