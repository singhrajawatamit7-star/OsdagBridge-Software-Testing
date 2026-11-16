"""
Input validation engine for OsdagBridge projects.
Enforces geometric constraints, material validations, and boundary checks
per IRC:24, IRC:6, and IS 800 standards.
"""

from typing import Dict, Any, List, Tuple
from .models import (
    SUPPORTED_STEEL_GRADES,
    SUPPORTED_CONCRETE_GRADES,
    SUPPORTED_VEHICLE_LOADS,
)


class ValidationError(Exception):
    """Custom exception raised when an input fails validation checks."""
    def __init__(self, message: str, field_name: str, error_code: str):
        super().__init__(message)
        self.field_name = field_name
        self.error_code = error_code


class ValidationResult:
    def __init__(self, is_valid: bool, errors: List[Dict[str, str]] = None, warnings: List[Dict[str, str]] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

    def add_error(self, field: str, message: str, code: str):
        self.is_valid = False
        self.errors.append({"field": field, "message": message, "code": code})

    def add_warning(self, field: str, message: str, code: str):
        self.warnings.append({"field": field, "message": message, "code": code})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
        }


class ProjectValidator:
    """Validates raw dictionaries or project models for OsdagBridge."""

    MIN_SPAN = 5.0       # meters
    MAX_SPAN = 60.0      # meters
    MIN_CARRIAGEWAY = 3.5  # meters (single lane min)
    MAX_CARRIAGEWAY = 30.0 # meters
    MIN_WEB_THICKNESS = 8.0 # mm (IRC:24 minimum corrosion allowance for bridge steel)
    MIN_FLANGE_THICKNESS = 10.0 # mm
    MIN_WEB_DEPTH = 500.0   # mm
    MAX_WEB_DEPTH = 4500.0  # mm

    @classmethod
    def validate_project_payload(cls, data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)

        if not isinstance(data, dict):
            result.add_error("payload", "Project payload must be a JSON dictionary.", "ERR_TYPE_INVALID")
            return result

        # 1. Project Metadata Checks
        required_meta = ["project_id", "project_name", "location", "engineer_name", "steel_grade", "concrete_grade", "vehicle_loading"]
        for field in required_meta:
            val = data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                result.add_error(field, f"Field '{field}' is required and cannot be empty.", "ERR_REQUIRED_FIELD_EMPTY")

        # 2. Materials & Loading validation
        steel = data.get("steel_grade")
        if steel and steel not in SUPPORTED_STEEL_GRADES:
            result.add_error("steel_grade", f"Unsupported steel grade '{steel}'. Supported: {SUPPORTED_STEEL_GRADES}", "ERR_INVALID_STEEL_GRADE")

        concrete = data.get("concrete_grade")
        if concrete and concrete not in SUPPORTED_CONCRETE_GRADES:
            result.add_error("concrete_grade", f"Unsupported concrete grade '{concrete}'. Supported: {SUPPORTED_CONCRETE_GRADES}", "ERR_INVALID_CONCRETE_GRADE")

        vehicle = data.get("vehicle_loading")
        if vehicle and vehicle not in SUPPORTED_VEHICLE_LOADS:
            result.add_error("vehicle_loading", f"Unsupported vehicle loading '{vehicle}'. Supported: {SUPPORTED_VEHICLE_LOADS}", "ERR_INVALID_VEHICLE_LOAD")

        # 3. Geometry Validation
        geom = data.get("geometry")
        if not isinstance(geom, dict):
            result.add_error("geometry", "Geometry configuration block is missing or not a dictionary.", "ERR_GEOMETRY_MISSING")
        else:
            cls._validate_geometry(geom, result)

        # 4. Girder Dimensions Validation
        girder = data.get("girder_dimensions")
        if not isinstance(girder, dict):
            result.add_error("girder_dimensions", "Girder dimensions configuration block is missing or not a dictionary.", "ERR_GIRDER_MISSING")
        else:
            cls._validate_girder_dimensions(girder, result)

        return result

    @classmethod
    def _validate_geometry(cls, geom: Dict[str, Any], result: ValidationResult):
        numeric_fields = {
            "span_length": (cls.MIN_SPAN, cls.MAX_SPAN, "Span length (m)"),
            "carriageway_width": (cls.MIN_CARRIAGEWAY, cls.MAX_CARRIAGEWAY, "Carriageway width (m)"),
            "girder_spacing": (1.0, 6.0, "Girder spacing (m)"),
            "cross_girder_spacing": (2.0, 10.0, "Cross girder spacing (m)"),
            "deck_slab_thickness": (150.0, 500.0, "Deck slab thickness (mm)"),
            "wearing_coat_thickness": (40.0, 150.0, "Wearing coat thickness (mm)")
        }

        for field, (min_val, max_val, desc) in numeric_fields.items():
            if field not in geom:
                result.add_error(f"geometry.{field}", f"Missing required parameter '{field}'", "ERR_REQUIRED_FIELD_EMPTY")
                continue
            val = geom[field]
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                result.add_error(f"geometry.{field}", f"Field '{field}' must be a numeric value, got '{type(val).__name__}'", "ERR_INVALID_DATA_TYPE")
                continue
            if val <= 0:
                result.add_error(f"geometry.{field}", f"Value for '{desc}' must be positive, got {val}", "ERR_NEGATIVE_OR_ZERO_INPUT")
                continue
            if val < min_val:
                result.add_error(f"geometry.{field}", f"Value {val} is below minimum allowable limit ({min_val}) for {desc}", "ERR_BELOW_MIN_LIMIT")
            elif val > max_val:
                result.add_error(f"geometry.{field}", f"Value {val} exceeds maximum allowable limit ({max_val}) for {desc}", "ERR_EXCEEDS_MAX_LIMIT")

        # Girder count check
        num_girders = geom.get("number_of_main_girders")
        if num_girders is not None:
            if not isinstance(num_girders, int) or isinstance(num_girders, bool):
                result.add_error("geometry.number_of_main_girders", "Main girders count must be an integer >= 2", "ERR_INVALID_DATA_TYPE")
            elif num_girders < 2:
                result.add_error("geometry.number_of_main_girders", "At least 2 main girders are required for a plate girder bridge system.", "ERR_MIN_GIRDERS_REQUIRED")
            elif num_girders > 10:
                result.add_warning("geometry.number_of_main_girders", "More than 8 main girders is unusually high for standard plate girder road bridges.", "WARN_HIGH_GIRDER_COUNT")

    @classmethod
    def _validate_girder_dimensions(cls, girder: Dict[str, Any], result: ValidationResult):
        dimension_fields = {
            "web_depth": (cls.MIN_WEB_DEPTH, cls.MAX_WEB_DEPTH, "Web depth (mm)"),
            "web_thickness": (cls.MIN_WEB_THICKNESS, 60.0, "Web thickness (mm)"),
            "flange_width": (150.0, 1200.0, "Flange width (mm)"),
            "flange_thickness": (cls.MIN_FLANGE_THICKNESS, 100.0, "Flange thickness (mm)"),
            "stiffener_spacing": (500.0, 5000.0, "Stiffener spacing (mm)"),
            "stiffener_thickness": (6.0, 40.0, "Stiffener thickness (mm)")
        }

        for field, (min_val, max_val, desc) in dimension_fields.items():
            if field not in girder:
                result.add_error(f"girder_dimensions.{field}", f"Missing girder parameter '{field}'", "ERR_REQUIRED_FIELD_EMPTY")
                continue
            val = girder[field]
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                result.add_error(f"girder_dimensions.{field}", f"Field '{field}' must be a numeric value, got '{type(val).__name__}'", "ERR_INVALID_DATA_TYPE")
                continue
            if val <= 0:
                result.add_error(f"girder_dimensions.{field}", f"Value for '{desc}' must be positive, got {val}", "ERR_NEGATIVE_OR_ZERO_INPUT")
                continue
            if val < min_val:
                result.add_error(f"girder_dimensions.{field}", f"Value {val} is below minimum allowable limit ({min_val}) for {desc}", "ERR_BELOW_MIN_LIMIT")
            elif val > max_val:
                result.add_error(f"girder_dimensions.{field}", f"Value {val} exceeds maximum allowable limit ({max_val}) for {desc}", "ERR_EXCEEDS_MAX_LIMIT")

        # Slenderness check d/tw
        web_d = girder.get("web_depth")
        web_t = girder.get("web_thickness")
        if isinstance(web_d, (int, float)) and isinstance(web_t, (int, float)) and web_t > 0:
            slenderness = web_d / web_t
            if slenderness > 200.0:
                result.add_warning("girder_dimensions.web_slenderness", f"Web slenderness d/tw = {slenderness:.1f} exceeds 200; intermediate longitudinal stiffeners required per IS 800 Cl 8.4.2.", "WARN_HIGH_SLENDERNESS")
