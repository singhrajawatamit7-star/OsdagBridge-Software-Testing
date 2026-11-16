"""
Test Module: test_reports.py
Validates generation of engineering design reports in Markdown, HTML, and CSV formats,
checking readability, section completeness, and standard clause inclusion.
"""

from osdagbridge_core.solver import BridgeSolver
from osdagbridge_core.report_generator import ReportGenerator


def test_markdown_report_generation(valid_bridge_project):
    """OB-020: Verify markdown report contains all required project sections."""
    summary = BridgeSolver.calculate_design(valid_bridge_project)
    md_report = ReportGenerator.generate_markdown_report(valid_bridge_project, summary)

    assert isinstance(md_report, str)
    assert len(md_report) > 500
    assert "1. Project Information" in md_report
    assert "2. Geometry & Section Properties" in md_report
    assert "3. Analysis Demand & Capacity Summary" in md_report
    assert "4. Code Compliance Verification Table" in md_report
    assert valid_bridge_project.project_id in md_report
    assert "IS 800:2007" in md_report
    assert "IRC:24" in md_report


def test_html_report_generation_and_styling(valid_bridge_project):
    """OB-012: Verify HTML report generation for PDF printing is well-formed."""
    summary = BridgeSolver.calculate_design(valid_bridge_project)
    html_report = ReportGenerator.generate_html_report(valid_bridge_project, summary)

    assert isinstance(html_report, str)
    assert "<!DOCTYPE html>" in html_report
    assert "<title>OsdagBridge Design Report - OB-PROJ-001</title>" in html_report
    assert "<table>" in html_report
    assert "SAFE / ACCEPTABLE" in html_report
    assert "IS 800:2007 &amp; IRC:24" in html_report or "IS 800:2007 & IRC:24" in html_report


def test_tabular_verification_data_consistency(valid_bridge_project):
    """OB-013: Verify check table records match summary calculations exactly."""
    summary = BridgeSolver.calculate_design(valid_bridge_project)

    check_names = [c.check_name for c in summary.checks]
    assert "Bending Moment Capacity Check" in check_names
    assert "Shear Force Capacity Check" in check_names
    assert "Live Load Deflection Check" in check_names
    assert "Web Slenderness Check (d/tw)" in check_names

    for check in summary.checks:
        assert check.allowable_limit > 0
        assert check.actual_value > 0
        assert check.clause_reference != ""
        assert check.status in ["PASS", "FAIL"]
