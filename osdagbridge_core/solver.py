"""
Structural analysis and design solver for Plate Girder Bridges.
Computes dead load, live load distribution, design bending moment, design shear,
section capacities, and deflection limits per IRC:6, IRC:24, and IS 800:2007.
"""

import math
from typing import Dict, Any, List
from .models import (
    BridgeProject,
    DesignSummary,
    DesignCheckResult,
    STEEL_PROPERTIES,
)
from .validator import ProjectValidator, ValidationError


class BridgeSolver:
    """Solves structural design checks for a Plate Girder Bridge."""

    GAMMA_M0 = 1.10   # Partial safety factor for resistance governed by yielding (IS 800 Table 5)
    GAMMA_M1 = 1.25   # Partial safety factor for resistance governed by ultimate stress
    CONCRETE_DENSITY = 25.0  # kN/m^3 (Reinforced concrete)
    WEARING_COAT_DENSITY = 22.0 # kN/m^3 (Bituminous concrete)

    @classmethod
    def calculate_design(cls, project: BridgeProject) -> DesignSummary:
        # Verify inputs first
        validation = ProjectValidator.validate_project_payload(project.to_dict())
        if not validation.is_valid:
            errors = [e["message"] for e in validation.errors]
            raise ValidationError(f"Cannot solve invalid project: {'; '.join(errors)}", "project", "ERR_INVALID_DESIGN_INPUTS")

        geom = project.geometry
        girder = project.girder_dimensions
        steel_grade = project.steel_grade
        steel_props = STEEL_PROPERTIES.get(steel_grade, STEEL_PROPERTIES["E250"])
        fy = steel_props["fy"] # MPa (N/mm^2)
        E = steel_props["E"]   # MPa (N/mm^2)

        span = geom.span_length # meters
        L_mm = span * 1000.0

        # Girder geometry calculations (mm -> m)
        d_web = girder.web_depth           # mm
        t_web = girder.web_thickness       # mm
        b_flange = girder.flange_width     # mm
        t_flange = girder.flange_thickness # mm
        total_depth = d_web + 2 * t_flange # mm

        # Cross-sectional Area
        area_flanges = 2 * (b_flange * t_flange) # mm^2
        area_web = d_web * t_web                 # mm^2
        total_area = area_flanges + area_web     # mm^2

        # Moment of Inertia Ixx (mm^4)
        I_web = (t_web * (d_web ** 3)) / 12.0
        I_flanges_own = 2 * ((b_flange * (t_flange ** 3)) / 12.0)
        dist_flange_c = (d_web / 2.0) + (t_flange / 2.0)
        I_flanges_parallel = 2 * (b_flange * t_flange * (dist_flange_c ** 2))
        I_xx = I_web + I_flanges_own + I_flanges_parallel # mm^4

        # Elastic Section Modulus Ze (mm^3)
        y_max = total_depth / 2.0
        Z_e = I_xx / y_max

        # Plastic Section Modulus Zp (approx for I-section)
        Z_p = (b_flange * t_flange * (d_web + t_flange)) + (t_web * (d_web ** 2) / 4.0)

        # 1. Dead Loads (per girder)
        # Steel self weight (kN/m)
        steel_density_kn = steel_props["density"] * 9.81 / 1000.0 # ~ 0.77 kN/m^3 steel volume
        weight_girder = (total_area * 1e-6) * 78.5 # kN/m
        # Deck slab weight distributed to girder (kN/m)
        t_slab_m = geom.deck_slab_thickness / 1000.0
        deck_width_per_girder = geom.girder_spacing
        weight_slab = t_slab_m * deck_width_per_girder * cls.CONCRETE_DENSITY # kN/m
        # Wearing coat (kN/m)
        t_wc_m = geom.wearing_coat_thickness / 1000.0
        weight_wc = t_wc_m * deck_width_per_girder * cls.WEARING_COAT_DENSITY # kN/m
        # Cross bracing & stiffeners allowance (10% of girder weight)
        weight_bracing = 0.10 * weight_girder

        w_dead_total = weight_girder + weight_slab + weight_wc + weight_bracing # kN/m

        # Dead Load Bending Moment & Shear
        M_DL = (w_dead_total * (span ** 2)) / 8.0 # kNm
        V_DL = (w_dead_total * span) / 2.0         # kN

        # 2. Live Loads (IRC 70R / Class A simplified standard)
        # Impact factor per IRC:6 for steel bridges: 4.5 / (6.0 + span) <= 0.35 (min 0.10)
        impact_factor = min(0.35, max(0.10, 4.5 / (6.0 + span)))

        if "Class_70R" in project.vehicle_loading:
            # Class 70R tracked vehicle: 700 kN load over 4.57m bogie
            # Equivalent bending moment on span with lateral distribution
            p_veh = 700.0 / geom.number_of_main_girders # distributed share
            # Maximum moment under single axle or bogie
            M_LL_raw = (p_veh * span / 4.0) * 0.85
            V_LL_raw = p_veh * 0.75
        else:
            # Class A loading: 554 kN train load distributed
            p_veh = 554.0 / geom.number_of_main_girders
            M_LL_raw = (p_veh * span / 4.0) * 0.75
            V_LL_raw = p_veh * 0.65

        M_LL = M_LL_raw * (1.0 + impact_factor) # kNm
        V_LL = V_LL_raw * (1.0 + impact_factor) # kN

        # 3. Design Ultimate Loads (ULS combinations per IRC:6 Table 1)
        gamma_DL = 1.35
        gamma_LL = 1.50
        M_design = (gamma_DL * M_DL) + (gamma_LL * M_LL) # kNm
        V_design = (gamma_DL * V_DL) + (gamma_LL * V_LL) # kN

        # 4. Capacities (IS 800 Cl 8.2)
        # Moment Capacity Md = (fy * Z_p) / gamma_m0 (in N*mm -> / 1e6 -> kNm)
        M_capacity = (fy * Z_p) / (cls.GAMMA_M0 * 1e6) # kNm

        # Shear Capacity Vd = Av * (fy / sqrt(3)) / gamma_m0 (in N -> / 1000 -> kN)
        A_v = d_web * t_web # mm^2
        V_capacity = (A_v * (fy / math.sqrt(3.0))) / (cls.GAMMA_M0 * 1000.0) # kN

        # 5. Deflection (Serviceability Limit State under Live Load)
        # delta = (5 * w * L^4) / (384 * E * I) mm
        # Equivalent UDL for live load producing M_LL: w_eq = (8 * M_LL) / L^2 (kN/m)
        w_ll_eq = (8.0 * M_LL) / (span ** 2) # kN/m = N/mm
        # Deflection in mm:
        delta_ll = (5.0 * w_ll_eq * (L_mm ** 4)) / (384.0 * E * I_xx) # mm

        # Allowable deflection limit under IRC:24 Cl 505: Span / 800
        delta_allowable = L_mm / 800.0 # mm

        # 6. Safety Checks
        checks: List[DesignCheckResult] = []
        failure_reasons: List[str] = []

        # Moment check
        ratio_moment = M_design / M_capacity
        status_moment = "PASS" if ratio_moment <= 1.0 else "FAIL"
        checks.append(DesignCheckResult(
            check_name="Bending Moment Capacity Check",
            actual_value=round(M_design, 2),
            allowable_limit=round(M_capacity, 2),
            ratio=round(ratio_moment, 3),
            status=status_moment,
            unit="kNm",
            clause_reference="IS 800:2007 Cl 8.2.1.2 / IRC:24 Cl 507.2"
        ))
        if status_moment == "FAIL":
            failure_reasons.append(f"Design Moment ({M_design:.1f} kNm) exceeds capacity ({M_capacity:.1f} kNm) - Utilization: {ratio_moment:.2f}")

        # Shear check
        ratio_shear = V_design / V_capacity
        status_shear = "PASS" if ratio_shear <= 1.0 else "FAIL"
        checks.append(DesignCheckResult(
            check_name="Shear Force Capacity Check",
            actual_value=round(V_design, 2),
            allowable_limit=round(V_capacity, 2),
            ratio=round(ratio_shear, 3),
            status=status_shear,
            unit="kN",
            clause_reference="IS 800:2007 Cl 8.4.1 / IRC:24 Cl 508.1"
        ))
        if status_shear == "FAIL":
            failure_reasons.append(f"Design Shear ({V_design:.1f} kN) exceeds capacity ({V_capacity:.1f} kN) - Utilization: {ratio_shear:.2f}")

        # Live load deflection check
        ratio_deflection = delta_ll / delta_allowable
        status_deflection = "PASS" if ratio_deflection <= 1.0 else "FAIL"
        checks.append(DesignCheckResult(
            check_name="Live Load Deflection Check",
            actual_value=round(delta_ll, 2),
            allowable_limit=round(delta_allowable, 2),
            ratio=round(ratio_deflection, 3),
            status=status_deflection,
            unit="mm",
            clause_reference="IRC:24 Cl 505 / IS 800 Table 6 (L/800)"
        ))
        if status_deflection == "FAIL":
            failure_reasons.append(f"Live Load Deflection ({delta_ll:.2f} mm) exceeds limit ({delta_allowable:.2f} mm) - Utilization: {ratio_deflection:.2f}")

        # Web slenderness check
        slenderness = d_web / t_web
        max_slenderness = 200.0 # unstiffened/stiffened web limit without longitudinal stiffeners
        ratio_slender = slenderness / max_slenderness
        status_slender = "PASS" if ratio_slender <= 1.0 else "FAIL"
        checks.append(DesignCheckResult(
            check_name="Web Slenderness Check (d/tw)",
            actual_value=round(slenderness, 1),
            allowable_limit=max_slenderness,
            ratio=round(ratio_slender, 3),
            status=status_slender,
            unit="ratio",
            clause_reference="IS 800:2007 Cl 8.6.1.1 / IRC:24 Cl 509.3"
        ))
        if status_slender == "FAIL":
            failure_reasons.append(f"Web slenderness d/tw ({slenderness:.1f}) exceeds {max_slenderness}; buckling stiffeners required.")

        is_safe = len(failure_reasons) == 0

        return DesignSummary(
            project_id=project.project_id,
            is_safe=is_safe,
            total_dead_load_moment=round(M_DL, 2),
            total_live_load_moment=round(M_LL, 2),
            design_moment=round(M_design, 2),
            design_shear_force=round(V_design, 2),
            moment_capacity=round(M_capacity, 2),
            shear_capacity=round(V_capacity, 2),
            max_deflection=round(delta_ll, 2),
            allowable_deflection=round(delta_allowable, 2),
            checks=checks,
            failure_reasons=failure_reasons
        )
