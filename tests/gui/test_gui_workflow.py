"""
GUI and Desktop Workflow Tests
Verifies application launch bootstrap, desktop main entry points,
CLI interface commands, and UI event workflow simulation.
"""

import sys
from io import StringIO
import pytest


def test_official_desktop_main_start():
    """GUI-01: Verify official desktop start function executes cleanly."""
    try:
        from osdagbridge.desktop.main import start

        # Capture console stdout from start()
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        try:
            start()
        finally:
            sys.stdout = old_stdout

        output = buffer.getvalue()
        assert "Starting desktop UI" in output
    except ImportError as e:
        pytest.skip(f"Official desktop module not found: {e}")


def test_official_cli_entry_points():
    """GUI-02: Verify official CLI commands module is discoverable and imports."""
    try:
        import osdagbridge.cli.commands as cli_commands
        assert cli_commands is not None
    except ImportError as e:
        pytest.skip(f"Official CLI module not found: {e}")


def test_simulated_ui_project_creation_workflow(sample_24m_data):
    """GUI-03: Simulate user creating new project and entering parameters."""
    from osdagbridge_core.models import BridgeProject

    # Simulate UI form data entry
    ui_state = {
        "active_tab": "Project Setup",
        "inputs": sample_24m_data,
        "is_saved": False
    }

    assert ui_state["active_tab"] == "Project Setup"
    project = BridgeProject.from_dict(ui_state["inputs"])
    assert project.project_id == "OB-PG-24M"
    ui_state["is_saved"] = True
    assert ui_state["is_saved"] is True


def test_simulated_ui_validation_error_state(sample_24m_data):
    """GUI-04: Simulate UI displaying error state when user enters negative span."""
    from osdagbridge_core.validator import ProjectValidator

    bad_inputs = dict(sample_24m_data)
    bad_inputs["geometry"] = dict(sample_24m_data["geometry"])
    bad_inputs["geometry"]["span_length"] = -15.0

    validation = ProjectValidator.validate_project_payload(bad_inputs)
    assert validation.is_valid is False

    # Simulate UI error badge mapping
    ui_error_banners = [f"{e['field']}: {e['message']}" for e in validation.errors]
    assert len(ui_error_banners) > 0
    assert any("span_length" in msg for msg in ui_error_banners)


def test_simulated_ui_design_run_and_results(sample_24m_data):
    """GUI-05: Simulate UI triggering design calculation and populating results tab."""
    from osdagbridge_core.models import BridgeProject
    from osdagbridge_core.solver import BridgeSolver

    project = BridgeProject.from_dict(sample_24m_data)
    summary = BridgeSolver.calculate_design(project)

    ui_results_tab = {
        "is_calculated": True,
        "safety_badge": "SAFE" if summary.is_safe else "UNSAFE",
        "moment_ratio": summary.design_moment / summary.moment_capacity,
        "checks_count": len(summary.checks)
    }

    assert ui_results_tab["is_calculated"] is True
    assert ui_results_tab["safety_badge"] == "SAFE"
    assert ui_results_tab["moment_ratio"] < 1.0
    assert ui_results_tab["checks_count"] == 4
