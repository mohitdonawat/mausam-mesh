"""
=============================================================================
⚡ MAUSAMMESH THREAT SOLVER — ATMOSPHERIC INSTABILITY & RUNOFF ENGINE
=============================================================================
Solves:
1. Convective Available Potential Energy (CAPE) Lightning & Hail Hazard Index
2. Hydrological Rational Runoff: Q = (C * I * A) / 360 (m³/s)
3. Severe Weather Warning Protocols & NDMA CAP Standards
=============================================================================
"""

import math
from typing import Dict, Any, Optional, List


class ThreatEvaluationResult:
    """Detailed disaster risk and early warning evaluation."""
    def __init__(
        self,
        alert_level: str,
        hazard_summary: str,
        is_extreme: bool,
        alert_protocol: Dict[str, Any],
        flood_runoff_discharge_m3s: float,
        waterlogging_risk: str,
        shelter_dispatch_needed: bool,
        recommended_action: str
    ):
        self.alert_level = alert_level
        self.hazard_summary = hazard_summary
        self.is_extreme = is_extreme
        self.alert_protocol = alert_protocol
        self.flood_runoff_discharge_m3s = flood_runoff_discharge_m3s
        self.waterlogging_risk = waterlogging_risk
        self.shelter_dispatch_needed = shelter_dispatch_needed
        self.recommended_action = recommended_action

    @property
    def siren_protocol(self) -> Dict[str, Any]:
        """Backward-compatible alias for alert_protocol."""
        return self.alert_protocol

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_level": self.alert_level,
            "hazard_summary": self.hazard_summary,
            "is_extreme": self.is_extreme,
            "alert_protocol": self.alert_protocol,
            "flood_runoff_discharge_m3s": round(self.flood_runoff_discharge_m3s, 2),
            "waterlogging_risk": self.waterlogging_risk,
            "shelter_dispatch_needed": self.shelter_dispatch_needed,
            "recommended_action": self.recommended_action,
        }
            "shelter_dispatch_needed": self.shelter_dispatch_needed,
            "recommended_action": self.recommended_action,
        }


class ThreatSolver:
    """
    Sovereign Early Warning Evaluation Engine.
    """

    # Rational Runoff Surface Permeability Coefficients (C)
    SURFACE_COEFFICIENTS = {
        "concrete": 0.90,
        "asphalt_roads": 0.85,
        "commercial_dense": 0.85,
        "residential_suburban": 0.50,
        "parks_gardens": 0.25,
        "agricultural_loam": 0.20,
        "forest_soil": 0.15,
    }

    @classmethod
    def calculate_urban_runoff(
        cls,
        rainfall_intensity_mm_hr: float,
        catchment_area_ha: float,
        surface_type: str = "concrete",
        drain_carrying_capacity_m3s: float = 2.5
    ) -> Dict[str, Any]:
        """
        Calculates peak flood runoff discharge using the Rational Method:
        Q = (C * I * A) / 360  [m³/s]
        """
        c = cls.SURFACE_COEFFICIENTS.get(surface_type.lower(), 0.90)
        q_m3s = (c * rainfall_intensity_mm_hr * catchment_area_ha) / 360.0

        is_overloaded = q_m3s > drain_carrying_capacity_m3s
        waterlogging_depth_cm = round(max(0.0, (q_m3s - drain_carrying_capacity_m3s) * 12.0), 1) if is_overloaded else 0.0

        return {
            "runoff_discharge_m3s": round(q_m3s, 2),
            "surface_permeability_c": c,
            "drain_overloaded": is_overloaded,
            "waterlogging_depth_cm": waterlogging_depth_cm,
            "risk_status": "CRITICAL_INUNDATION" if waterlogging_depth_cm > 15.0 else ("MODERATE_WATERLOGGING" if is_overloaded else "SAFE_DRAINAGE")
        }

    @classmethod
    def evaluate_threat(
        cls,
        rain_intensity_mm_hr: float = 0.0,
        wind_speed_kmh: float = 15.0,
        temp_c: float = 30.0,
        cape_index: float = 800.0,
        catchment_area_ha: float = 25.0,
        surface_type: str = "concrete",
        imd_code: Optional[str] = None
    ) -> ThreatEvaluationResult:
        """
        Harmonizes atmospheric parameters into NDMA compliant severity levels.
        """
        runoff_res = cls.calculate_urban_runoff(
            rainfall_intensity_mm_hr=rain_intensity_mm_hr,
            catchment_area_ha=catchment_area_ha,
            surface_type=surface_type
        )

        # RED ALERT Condition
        is_red = (
            rain_intensity_mm_hr >= 25.0 or
            wind_speed_kmh >= 65.0 or
            temp_c >= 44.0 or
            cape_index >= 2000.0 or
            imd_code in ["cat14", "cat15", "cat17", "cat19"]
        )

        # ORANGE ALERT Condition
        is_orange = (
            rain_intensity_mm_hr >= 7.0 or
            wind_speed_kmh >= 38.0 or
            temp_c >= 40.0 or
            cape_index >= 1200.0 or
            imd_code in ["cat7", "cat8", "cat9", "cat10", "cat11", "cat12", "cat13"]
        )

        if is_red:
            level = "RED"
            is_extreme = True
            action = "IMMEDIATE EVACUATION / MOVE TO SAFE HIGH GROUND: Severe convective thunderstorm and flash flood danger active."
            summary = f"RED ALERT: Extreme Rainfall ({rain_intensity_mm_hr} mm/hr), Lightning CAPE {cape_index:.0f} J/kg, Wind {wind_speed_kmh} km/h."
            alert_state = "ACTIVE"
        elif is_orange:
            level = "ORANGE"
            is_extreme = False
            action = "BE PREPARED: Charge emergency lights, stay away from low-lying drains, avoid open fields during thunderstorm."
            summary = f"ORANGE ALERT: Heavy Precipitation ({rain_intensity_mm_hr} mm/hr), Wind Gusts {wind_speed_kmh} km/h."
            alert_state = "ACTIVE"
        elif rain_intensity_mm_hr > 0.0 or wind_speed_kmh >= 22.0:
            level = "YELLOW"
            is_extreme = False
            action = "WEATHER ADVISORY: Carry umbrella, stay updated with official meteorological bulletins."
            summary = f"YELLOW ADVISORY: Active precipitation ({rain_intensity_mm_hr} mm/hr)."
            alert_state = "STANDBY"
        else:
            level = "GREEN"
            is_extreme = False
            action = "Normal meteorological conditions. Routine outdoor activities safe."
            summary = "GREEN: Normal conditions."
            alert_state = "STANDBY"

        alert_protocol = {
            "status": alert_state,
            "severity": level,
            "cell_broadcast_channel": "CB-4370",
            "action_directive": action,
            "vibration_ms": [500, 200, 500, 200, 1000] if is_red else []
        }

        return ThreatEvaluationResult(
            alert_level=level,
            hazard_summary=summary,
            is_extreme=is_extreme,
            alert_protocol=alert_protocol,
            flood_runoff_discharge_m3s=runoff_res["runoff_discharge_m3s"],
            waterlogging_risk=runoff_res["risk_status"],
            shelter_dispatch_needed=is_red or runoff_res["risk_status"] == "CRITICAL_INUNDATION",
            recommended_action=action
        )


def evaluate_threat(*args, **kwargs) -> ThreatEvaluationResult:
    return ThreatSolver.evaluate_threat(*args, **kwargs)


def calculate_urban_runoff(*args, **kwargs) -> Dict[str, Any]:
    return ThreatSolver.calculate_urban_runoff(*args, **kwargs)
