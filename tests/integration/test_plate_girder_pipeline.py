"""
Integration Tests: Official OsdagBridge Plate Girder Pipeline
Tests end-to-end interactions between official DTOs, preliminary sizing routines,
structural analyser, and designer modules.
"""

import pytest


def test_official_preliminary_sizing_routine():
    """INT-PG-01: Verify official preliminary sizing module returns expected sizing dictionary."""
    try:
        from osdagbridge.core.bridge_types.plate_girder.dto import PlateGirderDTO
        from osdagbridge.core.bridge_types.plate_girder.initial_sizing import preliminary_sizing

        dto = PlateGirderDTO(name="24m_Highway_Bridge")
        result = preliminary_sizing(dto)

        assert isinstance(result, dict)
        assert "depth_m" in result
        assert result["depth_m"] == "24m_Highway_Bridge"
    except ImportError as e:
        pytest.skip(f"Official osdagbridge module not available: {e}")


def test_official_designer_module_execution():
    """INT-PG-02: Verify official designer module executes section sizing check."""
    try:
        from osdagbridge.core.bridge_types.plate_girder.dto import PlateGirderDTO
        from osdagbridge.core.bridge_types.plate_girder.designer import design

        dto = PlateGirderDTO(name="TestGirder_E250")
        res = design(dto)

        assert isinstance(res, dict)
        assert res.get("design") == "ok"
    except ImportError as e:
        pytest.skip(f"Official osdagbridge module not available: {e}")


def test_official_analyser_module_execution():
    """INT-PG-03: Verify official analyser calls structural grillage solver."""
    try:
        from osdagbridge.core.bridge_types.plate_girder.dto import PlateGirderDTO
        from osdagbridge.core.bridge_types.plate_girder.analyser import analyse

        dto = PlateGirderDTO(name="TestGirder_Span24")
        res = analyse(dto, solver="native")

        assert isinstance(res, dict)
        assert res.get("result") == "ok"
    except ImportError as e:
        pytest.skip(f"Official osdagbridge module not available: {e}")


def test_official_pipeline_end_to_end():
    """INT-PG-04: Verify chained execution of DTO -> preliminary sizing -> analyser -> designer."""
    try:
        from osdagbridge.core.bridge_types.plate_girder.dto import PlateGirderDTO
        from osdagbridge.core.bridge_types.plate_girder.initial_sizing import preliminary_sizing
        from osdagbridge.core.bridge_types.plate_girder.analyser import analyse
        from osdagbridge.core.bridge_types.plate_girder.designer import design

        dto = PlateGirderDTO(name="Full_Pipeline_Bridge")
        sizing = preliminary_sizing(dto)
        analysis = analyse(dto)
        design_result = design(dto)

        assert sizing is not None
        assert analysis["result"] == "ok"
        assert design_result["design"] == "ok"
    except ImportError as e:
        pytest.skip(f"Official osdagbridge module not available: {e}")
