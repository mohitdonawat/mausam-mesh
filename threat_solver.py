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
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class SCSCurveNumberReport:
    """Hydrological agricultural/watershed runoff evaluation via USDA/CWC SCS-CN method."""
    rainfall_depth_mm: float
    catchment_area_ha: float
    hydrologic_soil_group: str
    land_use: str
    curve_number_amc2: float
    adjusted_curve_number: float
    amc_condition: str
    potential_retention_s_mm: float
    initial_abstraction_ia_mm: float
    direct_runoff_depth_pe_mm: float
    total_runoff_volume_m3: float
    peak_discharge_qp_m3s: float
    time_of_concentration_hr: float
    time_to_peak_hr: float
    infiltration_depth_mm: float
    runoff_coefficient_eq: float
    flood_risk_category: str
    advisory: str

    @property
    def runoff_depth_pe_mm(self) -> float:
        return self.direct_runoff_depth_pe_mm

    @property
    def runoff_volume_m3(self) -> float:
        return self.total_runoff_volume_m3

    @property
    def peak_discharge_m3_s(self) -> float:
        return self.peak_discharge_qp_m3s

    @property
    def retention_s_mm(self) -> float:
        return self.potential_retention_s_mm

    @property
    def hazard_level(self) -> str:
        return self.flood_risk_category

    @property
    def rainfall_depth_p_mm(self) -> float:
        return self.rainfall_depth_mm

    @property
    def curve_number(self) -> float:
        return self.adjusted_curve_number

    @property
    def antecedent_moisture_condition(self) -> str:
        return self.amc_condition

    @property
    def storm_duration_hr(self) -> float:
        return 3.0


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


class ThreatSolver:
    """
    Meteorological Early Warning Evaluation Engine.
    Aligned with IMD (India Meteorological Department) and NDMA (National Disaster Management Authority) Standards.
    """

    # Rational Method Surface Permeability Coefficients (C) - ASCE & IRC Standards
    SURFACE_COEFFICIENTS = {
        "concrete": 0.90,
        "asphalt_roads": 0.85,
        "commercial_dense": 0.82,
        "residential_suburban": 0.50,
        "parks_gardens": 0.20,
        "agricultural_loam": 0.18,
        "forest_soil": 0.12,
    }

    @classmethod
    def calculate_urban_runoff(
        cls,
        rainfall_intensity_mm_hr: float,
        catchment_area_ha: float,
        surface_type: str = "concrete",
        drain_carrying_capacity_m3s: float = 2.5,
        depression_storage_fraction: float = 0.20,
        storm_duration_hr: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Calculates peak flood runoff discharge and actual inundation ponding depth:
        
        1. Peak Discharge:
           Q = (C * I * A) / 360  [m³/s]
           (C: dimensionless runoff coefficient, I: mm/hr, A: hectares, 360: conversion factor)
           
        2. Mass Balance Inundation Hydrodynamics:
           Excess Volume V_flood = max(0, Q - Q_drain) * (3600 * storm_duration_hr)  [m³]
           Ponding Depth = V_flood / (depression_storage_fraction * catchment_area_m²) * 100  [cm]
        """
        if rainfall_intensity_mm_hr <= 0.0 or catchment_area_ha <= 0.0:
            return {
                "runoff_discharge_m3s": 0.0,
                "surface_permeability_c": cls.SURFACE_COEFFICIENTS.get(surface_type.lower(), 0.50),
                "drain_overloaded": False,
                "waterlogging_depth_cm": 0.0,
                "risk_status": "SAFE_NO_PRECIPITATION"
            }

        c = cls.SURFACE_COEFFICIENTS.get(surface_type.lower(), 0.50)
        q_m3s = (c * rainfall_intensity_mm_hr * catchment_area_ha) / 360.0

        is_overloaded = q_m3s > drain_carrying_capacity_m3s
        
        # Real physical flood ponding depth via volume-area conservation
        if is_overloaded:
            excess_q = q_m3s - drain_carrying_capacity_m3s
            volume_m3 = excess_q * (3600.0 * max(0.25, min(6.0, storm_duration_hr)))
            ponding_area_m2 = max(100.0, (catchment_area_ha * 10000.0) * max(0.05, min(0.50, depression_storage_fraction)))
            waterlogging_depth_cm = round((volume_m3 / ponding_area_m2) * 100.0, 1)
        else:
            waterlogging_depth_cm = 0.0

        if waterlogging_depth_cm >= 45.0:
            risk = "CRITICAL_CATASTROPHIC_INUNDATION"
        elif waterlogging_depth_cm >= 15.0:
            risk = "SEVERE_STREET_WATERLOGGING"
        elif is_overloaded:
            risk = "MODERATE_LOCAL_WATERLOGGING"
        else:
            risk = "SAFE_GRAVITY_DRAINAGE"

        return {
            "runoff_discharge_m3s": round(q_m3s, 2),
            "surface_permeability_c": c,
            "drain_overloaded": is_overloaded,
            "waterlogging_depth_cm": waterlogging_depth_cm,
            "risk_status": risk
        }

    # USDA NRCS / Central Water Commission (CWC) Curve Number Table (AMC-II)
    CURVE_NUMBER_TABLE: Dict[Tuple[str, str], int] = {
        ("fallow_bare", "A"): 77, ("fallow_bare", "B"): 86, ("fallow_bare", "C"): 91, ("fallow_bare", "D"): 94,
        ("row_crops_straight", "A"): 67, ("row_crops_straight", "B"): 78, ("row_crops_straight", "C"): 85, ("row_crops_straight", "D"): 89,
        ("row_crops_contoured", "A"): 65, ("row_crops_contoured", "B"): 75, ("row_crops_contoured", "C"): 82, ("row_crops_contoured", "D"): 86,
        ("small_grains_paddy", "A"): 63, ("small_grains_paddy", "B"): 75, ("small_grains_paddy", "C"): 83, ("small_grains_paddy", "D"): 87,
        ("pasture_grassland", "A"): 49, ("pasture_grassland", "B"): 69, ("pasture_grassland", "C"): 79, ("pasture_grassland", "D"): 84,
        ("forest_dense", "A"): 36, ("forest_dense", "B"): 60, ("forest_dense", "C"): 70, ("forest_dense", "D"): 77,
        ("mixed_agricultural", "A"): 62, ("mixed_agricultural", "B"): 74, ("mixed_agricultural", "C"): 82, ("mixed_agricultural", "D"): 86,
        ("commercial_industrial", "A"): 89, ("commercial_industrial", "B"): 92, ("commercial_industrial", "C"): 94, ("commercial_industrial", "D"): 95,
    }

    @classmethod
    def calculate_scs_curve_number_runoff(
        cls,
        rainfall_depth_mm: float,
        catchment_area_ha: Optional[float] = None,
        hydrologic_soil_group: str = "C",
        land_use: str = "mixed_agricultural",
        antecedent_rainfall_5day_mm: float = 25.0,
        slope_pct: float = 2.0,
        flow_length_m: float = 1000.0,
        initial_abstraction_ratio: float = 0.05,
        *,
        curve_number: Optional[float] = None,
        catchment_area_km2: Optional[float] = None,
        storm_duration_hr: Optional[float] = None,
        antecedent_moisture_condition: Optional[str] = None,
    ) -> SCSCurveNumberReport:
        """
        Calculates direct watershed runoff depth and peak discharge using the 
        USDA NRCS / Indian Central Water Commission (CWC) Curve Number (SCS-CN) method.
        """
        if catchment_area_ha is None:
            catchment_area_ha = (catchment_area_km2 * 100.0) if catchment_area_km2 is not None else 100.0

        soil_grp = hydrologic_soil_group.strip().upper()
        if soil_grp not in ("A", "B", "C", "D"):
            soil_grp = "C"
            
        l_use = land_use.strip().lower()
        if curve_number is not None:
            cn_amc2 = float(curve_number)
        else:
            cn_amc2 = float(cls.CURVE_NUMBER_TABLE.get((l_use, soil_grp), 80))
        
        # 1. Determine Antecedent Moisture Condition (AMC)
        if antecedent_moisture_condition is not None:
            amc = str(antecedent_moisture_condition)
            cn = cn_amc2
        elif antecedent_rainfall_5day_mm < 13.0:
            amc = "AMC-I (DRY)"
            cn = cn_amc2 / (2.281 - 0.01281 * cn_amc2)
        elif antecedent_rainfall_5day_mm > 28.0:
            amc = "AMC-III (SATURATED/WET)"
            cn = cn_amc2 / (0.427 + 0.00573 * cn_amc2)
        else:
            amc = "AMC-II (NORMAL)"
            cn = cn_amc2
            
        cn = float(min(98.0, max(30.0, cn)))
        
        # 2. Potential Maximum Soil Water Retention S (mm)
        s_retention = (25400.0 / cn) - 254.0
        
        # 3. Initial Abstraction Ia (mm)
        ia = float(initial_abstraction_ratio * s_retention)
        
        p = max(0.0, float(rainfall_depth_mm))
        
        # 4. Direct Runoff Depth Pe (mm)
        if p <= ia:
            pe = 0.0
        else:
            pe = ((p - ia) ** 2.0) / (p - ia + s_retention)
            
        # 5. Total Runoff Volume (m³)
        vol_m3 = pe * (catchment_area_ha * 10.0)
        
        # 6. Time of Concentration tc (Kirpich formula) & Time to Peak tp (hours)
        slope_val = max(0.1, slope_pct) / 100.0
        fl_val = max(50.0, flow_length_m)
        tc_hr = 0.0195 * (fl_val ** 0.77) * (slope_val ** -0.385) / 60.0
        tc_hr = float(min(48.0, max(0.20, tc_hr)))
        tp_hr = float(0.6 * tc_hr + 0.25)
        
        # 7. Peak Discharge Qp (m³/s) via SCS Triangular Hydrograph: Qp = (0.208 * A_km² * Pe) / tp
        area_km2 = catchment_area_ha / 100.0
        qp_m3s = (0.208 * area_km2 * pe) / tp_hr if tp_hr > 0.0 else 0.0
        
        # Infiltration & Equivalent runoff coefficient
        inf_mm = max(0.0, p - ia - pe)
        ceq = float(pe / p) if p > 0.0 else 0.0
        
        # Risk classification
        if pe >= 90.0 or qp_m3s >= 40.0:
            risk = "CRITICAL_CATASTROPHIC_WATERSHED_FLOOD"
            adv = "🚨 भारी जलभराव व नदी-नालों में बाढ़ की चेतावनी! निचले इलाकों से तुरंत सुरक्षित स्थानों पर जाएं।"
        elif pe >= 45.0 or qp_m3s >= 15.0:
            risk = "SEVERE_AGRICULTURAL_INUNDATION"
            adv = "⚠️ खेतों में तीव्र जलभराव की संभावना। मेड़ों को सुरक्षित रखें व जल निकासी के प्रबंध करें।"
        elif pe >= 12.0:
            risk = "MODERATE_WATERSHED_RUNOFF"
            adv = "मध्यम स्तर का बहाव। खेत-तालाबों में वर्षा जल संचयन के लिए अनुकूल।"
        else:
            risk = "MINIMAL_RUNOFF_HIGH_INFILTRATION"
            adv = "वर्षा का अधिकांश जल भूमि में समाहित। फसलों के लिए लाभकारी।"
            
        return SCSCurveNumberReport(
            rainfall_depth_mm=float(round(p, 1)),
            catchment_area_ha=float(round(catchment_area_ha, 1)),
            hydrologic_soil_group=soil_grp,
            land_use=l_use,
            curve_number_amc2=float(round(cn_amc2, 1)),
            adjusted_curve_number=float(round(cn, 1)),
            amc_condition=amc,
            potential_retention_s_mm=float(round(s_retention, 1)),
            initial_abstraction_ia_mm=float(round(ia, 1)),
            direct_runoff_depth_pe_mm=float(round(pe, 1)),
            total_runoff_volume_m3=float(round(vol_m3, 0)),
            peak_discharge_qp_m3s=float(round(qp_m3s, 2)),
            time_of_concentration_hr=float(round(tc_hr, 2)),
            time_to_peak_hr=float(round(tp_hr, 2)),
            infiltration_depth_mm=float(round(inf_mm, 1)),
            runoff_coefficient_eq=float(round(ceq, 3)),
            flood_risk_category=risk,
            advisory=adv,
        )

    @classmethod
    def evaluate_threat(
        cls,
        rain_intensity_mm_hr: Optional[float] = None,
        wind_speed_kmh: Optional[float] = None,
        temp_c: Optional[float] = None,
        cape_index: Optional[float] = None,
        bulk_shear_m_s: Optional[float] = None,
        srh_m2_s2: Optional[float] = None,
        catchment_area_ha: float = 25.0,
        surface_type: str = "concrete",
        imd_code: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        location: Optional[str] = None,
    ) -> ThreatEvaluationResult:
        """
        Harmonizes multi-variate atmospheric & hydrological conditions into 
        Standard NDMA (National Disaster Management Authority) / IMD Color Protocols.
        Automatically resolves live meteorological telemetry if lat/lon/location are provided.
        """
        # Auto-resolve live telemetry from MausamMesh pipeline if requested
        if (lat is not None or location is not None) and (rain_intensity_mm_hr is None or cape_index is None):
            try:
                from .auto import auto
            except (ImportError, ValueError):
                try:
                    from auto import auto
                except Exception:
                    auto = None

            if auto is not None:
                try:
                    verdict = auto(location=location, lat=lat, lon=lon)
                    if rain_intensity_mm_hr is None:
                        rain_intensity_mm_hr = max(0.0, float(getattr(verdict, "rain_rate_mm_hr", 0.0)))
                    if wind_speed_kmh is None:
                        wind_speed_kmh = verdict.peak_microburst_gust_kmh
                    if temp_c is None:
                        temp_c = verdict.calibrated_temp_c
                    if cape_index is None:
                        cape_index = verdict.sbcape_j_kg
                    if bulk_shear_m_s is None:
                        bulk_shear_m_s = verdict.bulk_shear_0_6km_m_s
                    if srh_m2_s2 is None:
                        srh_m2_s2 = verdict.storm_relative_helicity_0_3km
                except Exception:
                    pass

        # Fallback to realistic standard baselines
        r_intensity = rain_intensity_mm_hr if rain_intensity_mm_hr is not None else 0.0
        w_speed = wind_speed_kmh if wind_speed_kmh is not None else 15.0
        t_val = temp_c if temp_c is not None else 30.0
        c_idx = cape_index if cape_index is not None else 800.0
        b_shear = bulk_shear_m_s if bulk_shear_m_s is not None else 8.0
        s_srh = srh_m2_s2 if srh_m2_s2 is not None else 40.0

        runoff_res = cls.calculate_urban_runoff(
            rainfall_intensity_mm_hr=r_intensity,
            catchment_area_ha=catchment_area_ha,
            surface_type=surface_type
        )

        # 1. RED ALERT Conditions (Scientific criteria aligned with IMD/NDMA):
        # - Cloudburst intensity (>= 100 mm/hr) or Extreme flash-flood rain (>= 50 mm/hr)
        # - Cyclone / Severe Gale wind (>= 88 km/h, Beaufort 10+)
        # - Severe Rotating Supercell / Severe Convection: CAPE >= 2500 & Shear >= 18 m/s & SRH >= 150
        # - Lethal Heatwave: Temp >= 45°C
        # - IMD Official Red categories (cat14: Severe Thunderstorm > 62-87 kmph gusts, cat15: >87 kmph, cat17: Hailstorm, cat19: Severe Lightning >60%)
        is_red = (
            r_intensity >= 50.0 or
            w_speed >= 88.0 or
            t_val >= 45.0 or
            (c_idx >= 2500.0 and b_shear >= 18.0 and s_srh >= 150.0) or
            runoff_res["waterlogging_depth_cm"] >= 45.0 or
            imd_code in ["cat14", "cat15", "cat17", "cat19"]
        )

        # 2. ORANGE ALERT Conditions:
        is_orange = (
            not is_red and (
                r_intensity >= 18.0 or
                w_speed >= 60.0 or
                t_val >= 42.0 or
                (c_idx >= 1600.0 and b_shear >= 14.0) or
                runoff_res["waterlogging_depth_cm"] >= 15.0 or
                imd_code in ["cat7", "cat8", "cat9", "cat10", "cat11", "cat12", "cat13"]
            )
        )

        # 3. YELLOW ALERT Conditions:
        is_yellow = (
            not is_red and not is_orange and (
                r_intensity >= 5.0 or
                w_speed >= 38.0 or
                t_val >= 39.0 or
                c_idx >= 1000.0 or
                imd_code in ["cat2", "cat3", "cat4", "cat5", "cat6"]
            )
        )

        if is_red:
            level = "RED"
            is_extreme = True
            action = "IMMEDIATE EVACUATION / MOVE TO SAFE HIGH GROUND: Severe convective thunderstorm, flash flood, or extreme wind danger active."
            summary = f"RED ALERT: Extreme Rainfall ({r_intensity:.1f} mm/hr), Wind {w_speed:.1f} km/h, CAPE {c_idx:.0f} J/kg, Shear {b_shear:.1f} m/s."
            alert_state = "ACTIVE"
        elif is_orange:
            level = "ORANGE"
            is_extreme = False
            action = "BE PREPARED: Secure property, charge emergency communications, avoid waterlogged underpasses and open electrical poles."
            summary = f"ORANGE ALERT: Heavy Precipitation ({r_intensity:.1f} mm/hr), Wind Gusts {w_speed:.1f} km/h."
            alert_state = "ACTIVE"
        elif is_yellow:
            level = "YELLOW"
            is_extreme = False
            action = "WEATHER ADVISORY: Carry rain protection, monitor official IMD radar bulletins during transit."
            summary = f"YELLOW ADVISORY: Moderate weather conditions ({r_intensity:.1f} mm/hr, wind {w_speed:.1f} km/h)."
            alert_state = "STANDBY"
        else:
            level = "GREEN"
            is_extreme = False
            action = "Normal meteorological conditions. Routine outdoor and agricultural activities safe."
            summary = "GREEN: Normal conditions."
            alert_state = "STANDBY"

        alert_protocol = {
            "status": alert_state,
            "severity": level,
            "cell_broadcast_channel": "CB-4370",
            "action_directive": action,
            "siren_trigger": is_red,
            "sound_frequency_hz": 800.0 if is_red else (600.0 if is_orange else 0.0),
            "vibration_ms": [500, 200, 500, 200, 1000] if is_red else ([300, 200, 300] if is_orange else [])
        }

        return ThreatEvaluationResult(
            alert_level=level,
            hazard_summary=summary,
            is_extreme=is_extreme,
            alert_protocol=alert_protocol,
            flood_runoff_discharge_m3s=runoff_res["runoff_discharge_m3s"],
            waterlogging_risk=runoff_res["risk_status"],
            shelter_dispatch_needed=is_red or runoff_res["risk_status"] in ["CRITICAL_CATASTROPHIC_INUNDATION", "SEVERE_STREET_WATERLOGGING"],
            recommended_action=action
        )


def evaluate_threat(*args, **kwargs) -> ThreatEvaluationResult:
    return ThreatSolver.evaluate_threat(*args, **kwargs)


def calculate_urban_runoff(*args, **kwargs) -> Dict[str, Any]:
    return ThreatSolver.calculate_urban_runoff(*args, **kwargs)


def calculate_scs_curve_number_runoff(*args, **kwargs) -> SCSCurveNumberReport:
    return ThreatSolver.calculate_scs_curve_number_runoff(*args, **kwargs)

