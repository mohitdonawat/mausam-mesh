"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — REGIONAL HAZARD & DISASTER INTELLIGENCE (`hazards`)
=============================================================================
Sovereign early-warning detectors customized for the unique meteorological 
regimes of the Indian subcontinent and global tropical zones:
1. Himalayan & Western Ghats Cloudburst Detection Engine (Rain >= 100 mm/hr)
2. Official IMD Tropical Cyclone Classification & Storm Surge Estimator
3. Kalbaisakhi (Nor'wester) Violent Convective Squall Line Detector
4. Wet-Bulb Temperature (Tw) Human Physiological Survivability & Loo Heatwave Suite

MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
=============================================================================
"""

from __future__ import annotations
import math
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
import numpy as np

from .thermo import wet_bulb_temperature


# =============================================================================
# 1. CLOUDBURST DETECTION ENGINE
# =============================================================================

@dataclass
class CloudburstAssessment:
    is_cloudburst: bool
    rainfall_rate_mm_hr: float
    terrain_slope_deg: float
    precipitable_water_mm: float
    lcl_height_m: float
    alert_level: str
    impact_verdict: str
    recommended_evacuation_lead_min: int


def detect_cloudburst(
    rainfall_rate_mm_hr: float,
    terrain_slope_deg: float = 20.0,
    precipitable_water_mm: float = 55.0,
    lcl_height_m: float = 650.0,
    convective_cell_speed_kmh: float = 12.0,
) -> CloudburstAssessment:
    """
    Evaluates whether an atmospheric convective signature qualifies as a catastrophic Cloudburst.
    
    Standard IMD / WMO Definition:
        Rainfall >= 100 mm/hour over a localized geographical area (~20 to 30 km²).
        Frequently occurs in steep Himalayan / Western Ghat valleys (Uttarakhand, H.P., J&K, Kerala).
    """
    is_cloudburst = False
    lead_time = 0
    
    # Primary rainfall threshold
    if rainfall_rate_mm_hr >= 100.0:
        is_cloudburst = True
        alert = "CRITICAL_RED_ALERT"
        verdict = "CONFIRMED CATASTROPHIC CLOUDBURST IN PROGRESS: IMMEDIATE DEBRIS FLOW & FLASH FLOOD"
        lead_time = 15
    elif rainfall_rate_mm_hr >= 65.0 and terrain_slope_deg >= 15.0 and precipitable_water_mm >= 50.0:
        is_cloudburst = True
        alert = "HIGH_ORANGE_ALERT"
        verdict = "OROGRAPHIC CLOUDBURST FORMATION IMMINENT: STEEP MOUNTAIN SLOPES SATURATED"
        lead_time = 30
    elif rainfall_rate_mm_hr >= 45.0:
        alert = "MODERATE_YELLOW_ALERT"
        verdict = "SEVERE TORRENTIAL DOWNPOUR: WATCH FOR RIVER GAUGE SPIKES"
        lead_time = 60
    else:
        alert = "NORMAL_GREEN"
        verdict = "NO IMMEDIATE CLOUDBURST THREAT"
        lead_time = 0
        
    return CloudburstAssessment(
        is_cloudburst=is_cloudburst,
        rainfall_rate_mm_hr=float(rainfall_rate_mm_hr),
        terrain_slope_deg=float(terrain_slope_deg),
        precipitable_water_mm=float(precipitable_water_mm),
        lcl_height_m=float(lcl_height_m),
        alert_level=alert,
        impact_verdict=verdict,
        recommended_evacuation_lead_min=lead_time,
    )


# =============================================================================
# 2. OFFICIAL IMD TROPICAL CYCLONE CLASSIFICATION & STORM SURGE
# =============================================================================

@dataclass
class CycloneClassification:
    category_code: str
    category_name: str
    max_sustained_winds_kmh: float
    max_gusts_kmh: float
    central_pressure_hpa: float
    estimated_storm_surge_m: float
    destruction_potential: str
    coastal_evacuation_radius_km: float


def classify_cyclone(
    max_sustained_wind_kmh: float,
    central_pressure_hpa: float = 980.0,
    radius_of_max_winds_km: float = 35.0,
) -> CycloneClassification:
    """
    Classifies tropical cyclone intensity according to the official India Meteorological 
    Department (IMD) 3-minute sustained wind scale and estimates coastal storm surge.
    
    IMD Categorization:
        < 31 km/h: Low Pressure Area (LPA)
        31 - 49 km/h: Well Marked Low (WML)
        50 - 61 km/h: Depression (D)
        62 - 88 km/h: Deep Depression (DD)
        89 - 117 km/h: Cyclonic Storm (CS)
        118 - 166 km/h: Severe Cyclonic Storm (SCS)
        167 - 221 km/h: Very Severe Cyclonic Storm (VSCS)
        222 - 305 km/h: Extremely Severe Cyclonic Storm (ESCS)
        > 305 km/h: Super Cyclonic Storm (SuCS)
    """
    v = max_sustained_wind_kmh
    # Peak gusts are typically 1.25x to 1.35x sustained winds
    gusts = v * 1.30
    
    # Bathymetric inverted barometer + wind stress storm surge estimation
    # Delta P in hPa
    dp = max(0.0, 1013.25 - central_pressure_hpa)
    # Hydrostatic water rise: ~1 cm per 1 hPa pressure drop
    static_surge_m = dp * 0.01
    # Dynamic wind pile-up: scales quadratically with wind velocity over shallow shelf
    dynamic_surge_m = (v / 85.0) ** 2.1
    surge_m = min(12.0, static_surge_m + dynamic_surge_m)
    
    if v >= 222.0:
        cat_code = "SuCS" if v > 305.0 else "ESCS"
        cat_name = "SUPER CYCLONIC STORM" if v > 305.0 else "EXTREMELY SEVERE CYCLONIC STORM"
        impact = "CATASTROPHIC TOTAL DEVASTATION: ROOFS BLOWN OFF, CONCRETE TOWERS TOPPLED, COAST INUNDATED"
        evac_km = 80.0
    elif v >= 167.0:
        cat_code = "VSCS"
        cat_name = "VERY SEVERE CYCLONIC STORM"
        impact = "EXTENSIVE DAMAGE TO PUCCA AND KUTCHA HOUSES, UPROOTED COMMUNICATIONS & POWER LINES"
        evac_km = 50.0
    elif v >= 118.0:
        cat_code = "SCS"
        cat_name = "SEVERE CYCLONIC STORM"
        impact = "SIGNIFICANT TREE UPROOTING, FISHING BAN MANDATORY, COASTAL EROSION"
        evac_km = 30.0
    elif v >= 89.0:
        cat_code = "CS"
        cat_name = "CYCLONIC STORM"
        impact = "MINOR COASTAL FLOODING, DAMAGE TO THATCHED HUTS, HIGH WAVE HAZARDS"
        evac_km = 15.0
    elif v >= 62.0:
        cat_code = "DD"
        cat_name = "DEEP DEPRESSION"
        impact = "HEAVY TO VERY HEAVY RAINFALL, ROUGH SEAS, MARINERS ADVISED NOT TO VENTURE"
        evac_km = 0.0
    elif v >= 50.0:
        cat_code = "D"
        cat_name = "DEPRESSION"
        impact = "MONSOON DEPRESSION SQUALLS AND LOCALIZED URBAN WATERLOGGING"
        evac_km = 0.0
    elif v >= 31.0:
        cat_code = "WML"
        cat_name = "WELL MARKED LOW PRESSURE"
        impact = "ORGANIZED CONVECTION AND FRESH MONSOON SURGE"
        evac_km = 0.0
    else:
        cat_code = "LPA"
        cat_name = "LOW PRESSURE AREA"
        impact = "GENERAL MOISTURE INFLOW AND SCATTERED RAINFALL"
        evac_km = 0.0
        
    return CycloneClassification(
        category_code=cat_code,
        category_name=cat_name,
        max_sustained_winds_kmh=float(v),
        max_gusts_kmh=float(gusts),
        central_pressure_hpa=float(central_pressure_hpa),
        estimated_storm_surge_m=float(round(surge_m, 2)),
        destruction_potential=impact,
        coastal_evacuation_radius_km=float(evac_km),
    )


# =============================================================================
# 3. KALBAISAKHI (NOR'WESTER) VIOLENT SQUALL DETECTOR
# =============================================================================

@dataclass
class KalbaisakhiAlert:
    is_detected: bool
    threat_level: str
    expected_squall_wind_kmh: float
    lightning_density_index: float
    tactical_instructions: str


def evaluate_kalbaisakhi(
    surface_dewpoint_c: float,
    mid_level_rh_700_pct: float,
    sbcape_j_kg: float,
    bulk_shear_0_6km_m_s: float,
    hour_utc: int = 9,
) -> KalbaisakhiAlert:
    """
    Detects the severe pre-monsoon convective squall lines (Nor'westers / Kalbaisakhi) 
    in Eastern India (West Bengal, Odisha, Jharkhand, Bihar, Assam).
    
    Synoptic Signature:
        1. Moist low-level maritime air from Bay of Bengal (Td >= 22°C).
        2. Dry elevated mid-tropospheric layer from Chota Nagpur plateau (RH_700 <= 45%).
        3. Extreme instability (CAPE >= 2500 J/kg) with strong deep-layer shear (>= 18 m/s).
    """
    detected = False
    
    if (
        surface_dewpoint_c >= 21.0
        and mid_level_rh_700_pct <= 48.0
        and sbcape_j_kg >= 2200.0
        and bulk_shear_0_6km_m_s >= 16.0
    ):
        detected = True
        squall_wind = min(130.0, 60.0 + (sbcape_j_kg / 2500.0) * 35.0 + bulk_shear_0_6km_m_s * 1.2)
        lightning_idx = min(10.0, (sbcape_j_kg / 1000.0) * 2.2)
        threat = "EXTREME_SQUALL_ALERT"
        instructions = (
            "KALBAISAKHI / NOR'WESTER SQUALL APPROACHING FAST: Secure tea gardens, "
            "halt riverboat ferry crossings on Hooghly/Padma, take immediate shelter from severe lightning."
        )
    elif sbcape_j_kg >= 1500.0 and surface_dewpoint_c >= 19.0:
        squall_wind = 55.0
        lightning_idx = 4.5
        threat = "MODERATE_CONVECTIVE_WATCH"
        instructions = "Isolated thunderstorm activity likely during late afternoon/evening hours."
    else:
        squall_wind = 25.0
        lightning_idx = 1.0
        threat = "NORMAL_CONDITIONS"
        instructions = "No severe Kalbaisakhi squalls expected."
        
    return KalbaisakhiAlert(
        is_detected=detected,
        threat_level=threat,
        expected_squall_wind_kmh=float(round(squall_wind, 1)),
        lightning_density_index=float(round(lightning_idx, 1)),
        tactical_instructions=instructions,
    )


# =============================================================================
# 4. WET-BULB HUMAN SURVIVABILITY & LOO HEATWAVE SUITE
# =============================================================================

@dataclass
class HeatwaveHumanStress:
    temp_ambient_c: float
    relative_humidity_pct: float
    wet_bulb_temp_c: float
    heat_index_c: float
    physiological_risk_level: str
    max_safe_outdoor_work_minutes: int
    is_deadly_survivability_exceeded: bool
    is_loo_desert_heatwave: bool


def evaluate_heat_stress(
    temp_c: float,
    rh_pct: float,
    wind_speed_kmh: float = 15.0,
    wind_direction_deg: float = 290.0, # NW wind (desert flow)
) -> HeatwaveHumanStress:
    """
    Evaluates human physiological heat stress, Wet-Bulb Temperature (Tw) survivability, 
    and North Indian 'Loo' desert wind advection.
    
    Critical Physics:
        Human core temperature is 37°C. The human body cools exclusively through evaporative sweat.
        - Tw >= 31°C: Severe heat exhaustion, organ stress. Outdoor work becomes medically unsafe.
        - Tw >= 35°C: FATAL PHYSIOLOGICAL THRESHOLD. Evaporative cooling ceases; core temp rises uncontrollably.
    """
    tw = wet_bulb_temperature(temp_c, rh_pct)
    
    # Steadman / Rothfusz Heat Index empirical formulation
    t_f = temp_c * 1.8 + 32.0
    rh = max(0.0, min(100.0, rh_pct))
    
    if t_f < 80.0:
        hi_f = 0.5 * (t_f + 61.0 + ((t_f - 68.0) * 1.2) + (rh * 0.094))
    else:
        hi_f = (
            -42.379
            + 2.04901523 * t_f
            + 10.14333127 * rh
            - 0.22475541 * t_f * rh
            - 0.00683783 * (t_f ** 2)
            - 0.05481717 * (rh ** 2)
            + 0.00122874 * (t_f ** 2) * rh
            + 0.00085282 * t_f * (rh ** 2)
            - 0.00000199 * (t_f ** 2) * (rh ** 2)
        )
    hi_c = (hi_f - 32.0) / 1.8
    
    # Loo wind detection (Hot dry westerly/northwesterly winds across Rajasthan/M.P./U.P./Delhi)
    is_loo = False
    if temp_c >= 40.0 and rh_pct <= 25.0 and (240.0 <= wind_direction_deg <= 330.0) and wind_speed_kmh >= 15.0:
        is_loo = True
        
    is_deadly = False
    if tw >= 35.0:
        is_deadly = True
        risk = "FATAL_HYPERTHERMIA_EXCEEDED (HUMAN SURVIVABILITY LIMIT BROKEN)"
        work_mins = 0
    elif tw >= 31.0 or hi_c >= 54.0:
        risk = "EXTREME_DANGER_HEAT_STROKE_IMMINENT"
        work_mins = 15
    elif tw >= 28.0 or hi_c >= 41.0:
        risk = "DANGER_SEVERE_HEAT_EXHAUSTION_LIKELY"
        work_mins = 45
    elif hi_c >= 32.0:
        risk = "EXTREME_CAUTION_HEAT_FATIGUE_POSSIBLE"
        work_mins = 120
    else:
        risk = "SAFE_COMFORT_ZONE"
        work_mins = 480
        
    return HeatwaveHumanStress(
        temp_ambient_c=float(temp_c),
        relative_humidity_pct=float(rh_pct),
        wet_bulb_temp_c=float(round(tw, 2)),
        heat_index_c=float(round(hi_c, 2)),
        physiological_risk_level=risk,
        max_safe_outdoor_work_minutes=work_mins,
        is_deadly_survivability_exceeded=is_deadly,
        is_loo_desert_heatwave=is_loo,
    )
