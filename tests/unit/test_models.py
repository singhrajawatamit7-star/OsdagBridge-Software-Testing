"""
Unit Tests: QA Data Models and Verification Structures
Verifies BridgeProject, BridgeGeometry, and PlateGirderDimensions models.
"""

import pytest
from osdagbridge_core.models import BridgeProject, BridgeGeometry, PlateGirderDimensions


@pytest.mark.unit
def test_qa_bridge_project_instantiation(sample_24m_data):
    """UT-MOD-01: Verify BridgeProject model instantiates correctly from dictionary."""
    proj = BridgeProject.from_dict(sample_24m_data)
    assert proj.project_id == "OB-PG-24M"
    assert proj.geometry.span_length == 24.0
    assert proj.girder_dimensions.web_depth == 1800.0


@pytest.mark.unit
def test_qa_bridge_project_json_serialization(sample_24m_data):
    """UT-MOD-02: Verify BridgeProject serializes to valid JSON string and deserializes intact."""
    proj = BridgeProject.from_dict(sample_24m_data)
    json_str = proj.to_json()
    assert isinstance(json_str, str)

    reconstructed = BridgeProject.from_json(json_str)
    assert reconstructed.project_id == proj.project_id
    assert reconstructed.geometry.span_length == proj.geometry.span_length
    assert reconstructed.girder_dimensions.flange_width == proj.girder_dimensions.flange_width


@pytest.mark.unit
def test_bridge_geometry_model_attributes():
    """UT-MOD-03: Verify BridgeGeometry model validates attribute structure."""
    geom = BridgeGeometry(
        span_length=20.0,
        carriageway_width=7.5,
        footpath_width_left=1.0,
        footpath_width_right=1.0,
        number_of_main_girders=3,
        girder_spacing=2.8,
        cross_girder_spacing=4.0,
        deck_slab_thickness=220.0,
        wearing_coat_thickness=75.0
    )
    assert geom.span_length == 20.0
    assert geom.number_of_main_girders == 3
    assert geom.girder_spacing == 2.8


@pytest.mark.unit
def test_plate_girder_dimensions_model():
    """UT-MOD-04: Verify PlateGirderDimensions model stores section parameters."""
    sec = PlateGirderDimensions(
        web_depth=1600.0,
        web_thickness=12.0,
        flange_width=450.0,
        flange_thickness=32.0,
        stiffener_spacing=1500.0,
        stiffener_thickness=10.0
    )
    assert sec.web_depth == 1600.0
    assert sec.web_thickness == 12.0
    assert sec.flange_width == 450.0
