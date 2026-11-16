"""
Test Module: test_design.py
Validates structural engineering design calculations, capacity formulas,
IRC:6 / IRC:24 code compliance checks, deflection limits, and solver edge cases.
"""

try:
    import pytest
except ImportError:
    class _PytestShim:
        @staticmethod
        def approx(expected, rel=1e-2):
            class ApproxVal:
                def __init__(self, val, rel):
                    self.val = val
                    self.rel = rel
                def __eq__(self, other):
                    return abs(other - self.val) <= abs(self.val * self.rel)
                def __repr__(self):
                    return f"approx({self.val} +/- {self.rel*100}%)"
            return ApproxVal(expected, rel)

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
from osdagbridge_core.solver import BridgeSolver
from osdagbridge_core.validator import ValidationError


def test_standard_24m_design_solver(valid_bridge_project):
    """OB-007: Run valid design on standard 24m plate girder bridge."""
    summary = BridgeSolver.calculate_design(valid_bridge_project)

    assert summary.project_id == "OB-PROJ-001"
    assert summary.is_safe is True
    assert summary.design_moment > 0
    assert summary.moment_capacity > summary.design_moment
    assert summary.shear_capacity > summary.design_shear_force
    assert len(summary.checks) == 4
    assert len(summary.failure_reasons) == 0


def test_design_verification_against_irc_reference(valid_bridge_project, reference_irc_data):
    """Verify calculated moment and shear capacities match IRC:24 reference benchmark tolerances."""
    summary = BridgeSolver.calculate_design(valid_bridge_project)
    tolerances = reference_irc_data["expected_engineering_tolerances"]

    # Check Moment Capacity range
    assert tolerances["moment_capacity_knm_min"] <= summary.moment_capacity <= tolerances["moment_capacity_knm_max"], \
        f"Moment capacity {summary.moment_capacity} kNm outside tolerance [{tolerances['moment_capacity_knm_min']}, {tolerances['moment_capacity_knm_max']}]"

    # Check Shear Capacity range
    assert tolerances["shear_capacity_kn_min"] <= summary.shear_capacity <= tolerances["shear_capacity_kn_max"], \
        f"Shear capacity {summary.shear_capacity} kN outside tolerance [{tolerances['shear_capacity_kn_min']}, {tolerances['shear_capacity_kn_max']}]"

    # Check Overall Status
    assert summary.is_safe is (tolerances["overall_safety_status"] == "PASS")


def test_live_load_deflection_limit_l_800(valid_bridge_project):
    """OB-018: Verify live load deflection conforms strictly to IRC:24 Cl 505 limit (L/800)."""
    summary = BridgeSolver.calculate_design(valid_bridge_project)

    span_mm = valid_bridge_project.geometry.span_length * 1000.0
    expected_allowable = span_mm / 800.0  # 24,000 / 800 = 30.0 mm

    assert summary.allowable_deflection == pytest.approx(expected_allowable, rel=1e-2)
    assert summary.max_deflection <= summary.allowable_deflection
    ratio = summary.max_deflection / summary.allowable_deflection
    assert ratio <= 1.0


def test_modify_section_and_rerun_design(valid_bridge_project):
    """OB-014: Verify modifying flange thickness dynamically increases moment capacity."""
    initial_summary = BridgeSolver.calculate_design(valid_bridge_project)
    initial_md = initial_summary.moment_capacity

    # Increase flange thickness from 36mm to 44mm
    valid_bridge_project.girder_dimensions.flange_thickness = 44.0
    updated_summary = BridgeSolver.calculate_design(valid_bridge_project)
    updated_md = updated_summary.moment_capacity

    assert updated_md > initial_md, "Increasing flange thickness must increase section moment capacity."


def test_extreme_span_failure(valid_project_dict):
    """OB-017: Verify 60m extreme span exceeds deflection limits with default girder sections."""
    payload = dict(valid_project_dict)
    payload["geometry"] = dict(valid_project_dict["geometry"])
    payload["geometry"]["span_length"] = 60.0  # extreme span

    project_60m = BridgeProject.from_dict(payload)
    summary = BridgeSolver.calculate_design(project_60m)

    # 60m span with 1.8m web will fail deflection or moment
    assert summary.is_safe is False
    assert len(summary.failure_reasons) > 0


def test_material_grade_yield_scaling(valid_project_dict):
    """OB-019: Verify capacity ratio between E350 (fy=350) and E250 (fy=250) equals 1.40."""
    payload_e250 = dict(valid_project_dict)
    payload_e250["steel_grade"] = "E250"
    proj_e250 = BridgeProject.from_dict(payload_e250)
    summary_e250 = BridgeSolver.calculate_design(proj_e250)

    payload_e350 = dict(valid_project_dict)
    payload_e350["steel_grade"] = "E350"
    proj_e350 = BridgeProject.from_dict(payload_e350)
    summary_e350 = BridgeSolver.calculate_design(proj_e350)

    scaling_ratio = summary_e350.moment_capacity / summary_e250.moment_capacity
    expected_ratio = 350.0 / 250.0  # 1.40
    assert scaling_ratio == pytest.approx(expected_ratio, rel=1e-3)


def test_solver_prevents_execution_on_invalid_inputs(valid_project_dict):
    """OB-008: Verify solver prevents execution and raises ValidationError when input is invalid."""
    payload = dict(valid_project_dict)
    payload["geometry"] = dict(valid_project_dict["geometry"])
    payload["geometry"]["span_length"] = -10.0  # invalid negative span

    invalid_proj = BridgeProject.from_dict(payload)
    with pytest.raises(ValidationError) as excinfo:
        BridgeSolver.calculate_design(invalid_proj)
    assert "ERR_INVALID_DESIGN_INPUTS" in str(excinfo.value.error_code)
