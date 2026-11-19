"""
Unit Tests: Data Models and DTOs
Verifies official OsdagBridge PlateGirderDTO structures and QA data models.
"""

import json
import pytest
from osdagbridge_core.models import BridgeProject, BridgeGeometry, PlateGirderDimensions


def test_official_plate_girder_dto_instantiation(official_plate_girder_dto):
    """UT-MOD-01: Verify official PlateGirderDTO instantiates with name attribute."""
    assert hasattr(official_plate_girder_dto, "name")
    assert official_plate_girder_dto.name == "NH48_PlateGirder_24m"


def test_official_plate_girder_dto_string_representation(official_plate_girder_dto):
    """UT-MOD-02: Verify PlateGirderDTO string representation format."""
    rep = repr(official_plate_girder_dto)
    assert "PlateGirderDTO" in rep
    assert "NH48_PlateGirder_24m" in rep


def test_qa_bridge_project_instantiation(sample_24m_data):
    """UT-MOD-03: Verify BridgeProject model instantiates correctly from dictionary."""
    proj = BridgeProject.from_dict(sample_24m_data)
    assert proj.project_id == "OB-PG-24M"
    assert proj.geometry.span_length == 24.0
    assert proj.girder_dimensions.web_depth == 1800.0


def test_qa_bridge_project_json_serialization(sample_24m_data):
    """UT-MOD-04: Verify BridgeProject serializes to valid JSON string and deserializes intact."""
    proj = BridgeProject.from_dict(sample_24m_data)
    json_str = proj.to_json()
    assert isinstance(json_str, str)

    reconstructed = BridgeProject.from_json(json_str)
    assert reconstructed.project_id == proj.project_id
    assert reconstructed.geometry.span_length == proj.geometry.span_length
    assert reconstructed.girder_dimensions.flange_width == proj.girder_dimensions.flange_width


def test_bridge_geometry_model_attributes():
    """UT-MOD-05: Verify BridgeGeometry model validates attribute structure."""
    geom = BridgeGeometry(
        span_length=20.0,
        carriageway_width=7.5,
        footpath_width_left=1.0,
        footpath_width_right=1.0,
        number_of_main_girders=3,
        girder_spacing=2.5,
        cross_girder_spacing=4.0,
        deck_slab_thickness=210.0,
        wearing_coat_thickness=65.0
    )
    assert geom.span_length == 20.0
    assert geom.number_of_main_girders == 3
    assert geom.deck_slab_thickness == 210.0
