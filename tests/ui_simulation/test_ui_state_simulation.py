"""
Simulated UI Workflow State Tests.
These tests verify simulated UI workflow states using QA test utilities.
They do not automate the official OsdagBridge desktop interface.
"""

import pytest
from osdagbridge_core.models import BridgeProject
from osdagbridge_core.validator import ProjectValidator
from osdagbridge_core.solver import BridgeSolver


@pytest.mark.simulation
def test_simulated_ui_project_creation_workflow(sample_24m_data):
    """Simulate user creating new project and entering parameters in UI form."""
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


@pytest.mark.simulation
def test_simulated_ui_validation_error_state(sample_24m_data):
    """Simulate UI displaying error banners when user enters negative span length."""
    bad_inputs = dict(sample_24m_data)
    bad_inputs["geometry"] = dict(sample_24m_data["geometry"])
    bad_inputs["geometry"]["span_length"] = -15.0

    validation = ProjectValidator.validate_project_payload(bad_inputs)
    assert validation.is_valid is False

    ui_error_banners = [f"{e['field']}: {e['message']}" for e in validation.errors]
    assert len(ui_error_banners) > 0
    assert any("span_length" in msg for msg in ui_error_banners)


@pytest.mark.simulation
def test_simulated_ui_design_run_and_results(sample_24m_data):
    """Simulate UI triggering design calculation and populating results card."""
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
