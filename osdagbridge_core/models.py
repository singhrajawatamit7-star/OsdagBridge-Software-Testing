"""
Data models and schemas for OsdagBridge Plate Girder Bridge designs.
Conforms to IRC:6 (Loads and Stresses), IRC:24 (Steel Road Bridges), and IS 800:2007.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
import json

SUPPORTED_STEEL_GRADES = ["E250", "E300", "E350", "E410", "E450"]
SUPPORTED_CONCRETE_GRADES = ["M25", "M30", "M35", "M40", "M45", "M50"]
SUPPORTED_VEHICLE_LOADS = ["IRC_Class_70R_Tracked", "IRC_Class_70R_Wheeled", "IRC_Class_A", "IRC_Class_B"]

STEEL_PROPERTIES = {
    "E250": {"fy": 250.0, "fu": 410.0, "E": 200000.0, "density": 78.5},
    "E300": {"fy": 300.0, "fu": 440.0, "E": 200000.0, "density": 78.5},
    "E350": {"fy": 350.0, "fu": 490.0, "E": 200000.0, "density": 78.5},
    "E410": {"fy": 410.0, "fu": 540.0, "E": 200000.0, "density": 78.5},
    "E450": {"fy": 450.0, "fu": 570.0, "E": 200000.0, "density": 78.5},
}


@dataclass
class BridgeGeometry:
    span_length: float               # in meters (effective span)
    carriageway_width: float         # in meters
    footpath_width_left: float = 1.0       # in meters
    footpath_width_right: float = 1.0      # in meters
    number_of_main_girders: int = 3        # count (typically 2 to 6)
    girder_spacing: float = 2.8            # in meters
    cross_girder_spacing: float = 4.0      # in meters
    deck_slab_thickness: float = 220.0     # in mm (typical 200 - 300 mm)
    wearing_coat_thickness: float = 75.0   # in mm (typical 50 - 100 mm)


@dataclass
class PlateGirderDimensions:
    web_depth: float                 # in mm
    web_thickness: float             # in mm
    flange_width: float              # in mm
    flange_thickness: float          # in mm
    stiffener_spacing: float         # in mm
    stiffener_thickness: float       # in mm


@dataclass
class BridgeProject:
    project_id: str
    project_name: str
    location: str
    engineer_name: str
    bridge_type: str                 # "Plate_Girder_Bridge"
    steel_grade: str
    concrete_grade: str
    vehicle_loading: str
    geometry: BridgeGeometry
    girder_dimensions: PlateGirderDimensions
    custom_notes: Optional[str] = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BridgeProject":
        geom_data = dict(data["geometry"])
        geom_data.setdefault("footpath_width_left", 1.0)
        geom_data.setdefault("footpath_width_right", 1.0)
        geom_data.setdefault("number_of_main_girders", 3)
        geom_data.setdefault("girder_spacing", 2.8)
        geom_data.setdefault("cross_girder_spacing", 4.0)
        geom_data.setdefault("deck_slab_thickness", 220.0)
        geom_data.setdefault("wearing_coat_thickness", 75.0)

        girder_data = dict(data["girder_dimensions"])
        girder_data.setdefault("stiffener_spacing", 1500.0)
        girder_data.setdefault("stiffener_thickness", 12.0)

        geometry = BridgeGeometry(**geom_data)
        girder_dimensions = PlateGirderDimensions(**girder_data)
        return cls(
            project_id=data["project_id"],
            project_name=data.get("project_name", "Untitled Bridge"),
            location=data.get("location", "Default Location"),
            engineer_name=data.get("engineer_name", "QA Engineer"),
            bridge_type=data.get("bridge_type", "Plate_Girder_Bridge"),
            steel_grade=data.get("steel_grade", "E250"),
            concrete_grade=data.get("concrete_grade", "M30"),
            vehicle_loading=data.get("vehicle_loading", "IRC_Class_70R_Tracked"),
            geometry=geometry,
            girder_dimensions=girder_dimensions,
            custom_notes=data.get("custom_notes", "")
        )

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "BridgeProject":
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class DesignCheckResult:
    check_name: str
    actual_value: float
    allowable_limit: float
    ratio: float                     # actual / allowable
    status: str                      # "PASS" or "FAIL"
    unit: str
    clause_reference: str


@dataclass
class DesignSummary:
    project_id: str
    is_safe: bool
    total_dead_load_moment: float    # kNm
    total_live_load_moment: float    # kNm
    design_moment: float             # kNm
    design_shear_force: float        # kN
    moment_capacity: float           # kNm
    shear_capacity: float            # kN
    max_deflection: float            # mm
    allowable_deflection: float      # mm
    checks: List[DesignCheckResult] = field(default_factory=list)
    failure_reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
