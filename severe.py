"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — ADVANCED SEVERE CONVECTIVE ENGINE (`severe`)
=============================================================================
High-precision severe storm, tornado, and damaging convective wind diagnostics:
1. Downdraft CAPE (DCAPE) & Peak Microburst Wind Gust Potential (V_gust)
2. Significant Tornado Parameter (STP) with CIN attenuation
3. Hail Growth Zone CAPE (-10°C to -30°C) & Maximum Expected Hail Size (MEHS)
4. Severe Weather Threat Index (SWEAT)
5. Freezing Level (0°C Isotherm) & Wet-Bulb Zero Heights

MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
=============================================================================
"""

from __future__ import annotations
import math
from typing import Dict, Tuple, Optional, Union
from dataclasses import dataclass
import numpy as np

from .thermo import (
    R_D, G, T_ZERO,
    saturation_vapor_pressure,
    vapor_pressure_from_dewpoint,
    dewpoint_from_vapor_pressure,
    mixing_ratio,
    specific_humidity,
    virtual_temperature,
    potential_temperature,
    temperature_from_potential_temperature,
    wet_bulb_temperature,
    equivalent_potential_temperature,
)


@dataclass
class SevereStormDiagnostics:
    """Comprehensive diagnostic profile of convective storm severity and hazards."""
    storm_mode: str
    dcape_j_kg: float
    max_microburst_gust_kmh: float
    significant_tornado_parameter: float
    supercell_composite_parameter: float
    sweat_index: float
    freezing_level_m_agl: float
    wet_bulb_zero_m_agl: float
    hail_growth_zone_cape_j_kg: float
    max_expected_hail_size_mm: float
    hail_threat_category: str
    tornado_risk_category: str
    wind_damage_risk: str


def downdraft_cape(
    pressure_levels_hpa: np.ndarray,
    temp_levels_c: np.ndarray,
    dewpoint_levels_c: np.ndarray,
    height_levels_m: Optional[np.ndarray] = None,
) -> Tuple[float, float]:
    """
    Computes Downdraft Convective Available Potential Energy (DCAPE) and peak 
    microburst wind gust velocity.
    
    DCAPE estimates the potential energy available to evaporatively cooled 
    descending air parcels from the mid-troposphere (typically 700-500 hPa) down to surface.
    
    Formula:
        DCAPE = -Rd * ∫_{P_min}^{P_sfc} (Tv_env - Tv_parcel) d(ln P)  [J/kg]
        V_gust = sqrt(2 * DCAPE)  [m/s]
        
    Returns:
        (dcape_j_kg, max_wind_gust_m_s)
    """
    p = np.asarray(pressure_levels_hpa, dtype=np.float64)
    t = np.asarray(temp_levels_c, dtype=np.float64)
    td = np.asarray(dewpoint_levels_c, dtype=np.float64)
    
    sort_idx = np.argsort(-p)
    p = p[sort_idx]
    t = t[sort_idx]
    td = td[sort_idx]
    
    # 1. Locate layer of minimum equivalent potential temperature (theta_e) in mid-troposphere (700-500 hPa)
    mid_mask = (p <= 750.0) & (p >= 450.0)
    if not np.any(mid_mask):
        mid_mask = p <= p[0] - 150.0
        
    theta_e_vals = np.zeros(len(p))
    for i in range(len(p)):
        theta_e_vals[i] = equivalent_potential_temperature(p[i], t[i], td[i])
        
    mid_indices = np.where(mid_mask)[0]
    if len(mid_indices) == 0:
        return 0.0, 0.0
        
    min_th_idx = mid_indices[np.argmin(theta_e_vals[mid_indices])]
    p_orig = p[min_th_idx]
    t_orig = t[min_th_idx]
    td_orig = td[min_th_idx]
    
    # Wet-bulb temperature at source level (parcel becomes saturated upon descent)
    e_orig = vapor_pressure_from_dewpoint(td_orig)
    rh_orig = (e_orig / max(1e-6, saturation_vapor_pressure(t_orig))) * 100.0
    tw_orig = wet_bulb_temperature(t_orig, rh_orig)
    th_e_downdraft = equivalent_potential_temperature(p_orig, tw_orig, tw_orig)
    
    # Environmental virtual temperature
    e_env = vapor_pressure_from_dewpoint(td)
    q_env = specific_humidity(p, e_env)
    tv_env = virtual_temperature(t, q_env)
    
    # 2. Descend saturated pseudo-adiabatically down to surface (p[0])
    dcape = 0.0
    descent_mask = (p >= p_orig) & (p <= p[0])
    descent_indices = np.where(descent_mask)[0]
    
    # Sort from p_orig to p_sfc (increasing pressure)
    descent_indices = descent_indices[np.argsort(p[descent_indices])]
    
    for k in range(len(descent_indices) - 1):
        i1 = descent_indices[k]
        i2 = descent_indices[k + 1]
        p1, p2 = p[i1], p[i2]
        
        # Invert theta_e to parcel temperature at both levels
        def get_tw_at_p(curr_p: float) -> float:
            # Quick Newton solver
            tw = tw_orig + 0.005 * (curr_p - p_orig) * 10.0
            for _ in range(3):
                val = equivalent_potential_temperature(curr_p, tw, tw)
                diff = val - th_e_downdraft
                tw -= diff / 2.5
            return tw
            
        t_parcel_1 = get_tw_at_p(p1)
        t_parcel_2 = get_tw_at_p(p2)
        
        q1 = specific_humidity(p1, saturation_vapor_pressure(t_parcel_1))
        q2 = specific_humidity(p2, saturation_vapor_pressure(t_parcel_2))
        
        tv_parcel_1 = virtual_temperature(t_parcel_1, q1)
        tv_parcel_2 = virtual_temperature(t_parcel_2, q2)
        
        # Negative buoyancy diff: parcel is colder than environment
        b1 = tv_env[i1] - tv_parcel_1
        b2 = tv_env[i2] - tv_parcel_2
        
        mean_b = 0.5 * (b1 + b2)
        if mean_b > 0.0:
            d_ln_p = math.log(p2 / p1)
            dcape += R_D * mean_b * d_ln_p
            
    dcape = max(0.0, float(dcape))
    # Peak microburst wind gust velocity: V_gust = sqrt(2 * DCAPE)
    v_gust = math.sqrt(2.0 * dcape)
    
    return dcape, v_gust


def significant_tornado_parameter(
    sbcape_j_kg: float,
    lcl_height_m_agl: float,
    srh_0_1km_m2_s2: float,
    bulk_shear_0_6km_m_s: float,
    sbcin_j_kg: float = 0.0,
) -> float:
    """
    Computes Significant Tornado Parameter (STP) with convective inhibition attenuation.
    
    Formula (Thompson et al. 2004):
        STP = (SBCAPE / 1500) * ((2000 - Z_LCL) / 1000) * (SRH_0_1km / 100) * (Shear_0_6km / 20) * ((200 + SBCIN) / 150)
        
    Interpretation:
        STP < 0.5: Weak or non-tornadic
        STP 0.5 - 1.0: Marginal tornadic supercell potential
        STP 1.0 - 3.0: Significant tornado risk (EF2+)
        STP > 4.0: Violent tornado outbreak risk (EF3 - EF5)
    """
    if sbcape_j_kg <= 0.0 or bulk_shear_0_6km_m_s < 12.0 or srh_0_1km_m2_s2 <= 0.0:
        return 0.0
        
    cape_term = sbcape_j_kg / 1500.0
    lcl_term = max(0.0, min(1.5, (2000.0 - lcl_height_m_agl) / 1000.0))
    srh_term = srh_0_1km_m2_s2 / 100.0
    shear_term = max(0.0, min(1.5, bulk_shear_0_6km_m_s / 20.0))
    
    # CIN attenuation term
    cin_val = abs(sbcin_j_kg)
    if cin_val > 200.0:
        cin_term = 0.0
    elif cin_val < 50.0:
        cin_term = 1.0
    else:
        cin_term = (200.0 - cin_val) / 150.0
        
    stp = cape_term * lcl_term * srh_term * shear_term * cin_term
    return max(0.0, float(stp))


def hail_diagnostics(
    pressure_levels_hpa: np.ndarray,
    temp_levels_c: np.ndarray,
    dewpoint_levels_c: np.ndarray,
    height_levels_m: np.ndarray,
    sbcape_j_kg: float,
) -> Tuple[float, float, float, float]:
    """
    High-precision hail growth zone diagnostics and Maximum Expected Hail Size (MEHS).
    
    Evaluates:
    1. Freezing level (0°C isotherm) height (m AGL)
    2. Wet-bulb zero height (0°C Tw) (m AGL)
    3. Hail Growth Zone CAPE (-10°C to -30°C layer buoyancy)
    4. Maximum expected hail diameter in millimeters (mm)
    
    Returns:
        (freezing_level_m, wet_bulb_zero_m, hgz_cape_j_kg, max_hail_size_mm)
    """
    z = np.asarray(height_levels_m, dtype=np.float64)
    t = np.asarray(temp_levels_c, dtype=np.float64)
    td = np.asarray(dewpoint_levels_c, dtype=np.float64)
    p = np.asarray(pressure_levels_hpa, dtype=np.float64)
    
    # Compute wet-bulb temperature profile
    tw = np.zeros(len(t))
    for i in range(len(t)):
        e = vapor_pressure_from_dewpoint(td[i])
        rh = (e / max(1e-6, saturation_vapor_pressure(t[i]))) * 100.0
        tw[i] = wet_bulb_temperature(t[i], rh)
        
    # Freezing level height (where T crosses 0°C from positive to negative)
    fz_level = float(np.interp(0.0, t[::-1], z[::-1])) if (np.max(t) >= 0.0 and np.min(t) <= 0.0) else 0.0
    wb_zero = float(np.interp(0.0, tw[::-1], z[::-1])) if (np.max(tw) >= 0.0 and np.min(tw) <= 0.0) else 0.0
    
    # Hail growth zone: between -10°C and -30°C
    # Fraction of CAPE concentrated in hail growth zone:
    z_m10 = float(np.interp(-10.0, t[::-1], z[::-1]))
    z_m30 = float(np.interp(-30.0, t[::-1], z[::-1]))
    hgz_depth = max(0.0, z_m30 - z_m10)
    
    # Empirical hail growth zone CAPE fraction
    hgz_cape = sbcape_j_kg * min(0.65, max(0.20, (hgz_depth / 4000.0) * 0.45))
    
    # Witt (1998) / Edwards-Thompson MEHS empirical formulation:
    # Hail diameter scales with vertical updraft velocity w_max = sqrt(2 * CAPE_hgz)
    # and depression of wet-bulb zero below 4000m
    w_max = math.sqrt(2.0 * max(0.0, hgz_cape))
    wbz_factor = max(0.0, (4500.0 - wb_zero) / 1000.0)
    
    if sbcape_j_kg < 500.0:
        mehs_mm = 0.0
    else:
        # MEHS in mm
        mehs_mm = 0.55 * (w_max ** 1.05) * (wbz_factor ** 0.5)
        mehs_mm = min(120.0, max(0.0, mehs_mm))
        
    return fz_level, wb_zero, float(hgz_cape), float(mehs_mm)


def sweat_index(
    t850_c: float,
    td850_c: float,
    t500_c: float,
    wind_speed_850_kt: float,
    wind_speed_500_kt: float,
    wind_dir_850_deg: float,
    wind_dir_500_deg: float,
) -> float:
    """
    Computes Severe Weather Threat Index (SWEAT).
    Widely utilized by military and aviation meteorologists to predict severe tornadoes and hail.
    
    Formula:
        SWEAT = 12 * Td850 + 20 * (TT - 49) + 2 * V850 + V500 + 125 * [sin(Dir500 - Dir850) + 0.2]
        
    Interpretation:
        SWEAT < 300: Severe weather unlikely
        SWEAT 300 - 400: Severe thunderstorms possible
        SWEAT > 400: High tornado and damaging squall line potential
    """
    tt = t850_c + td850_c - 2.0 * t500_c
    tt_term = 20.0 * max(0.0, tt - 49.0)
    
    td_term = 12.0 * max(0.0, td850_c)
    v850_term = 2.0 * wind_speed_850_kt
    v500_term = wind_speed_500_kt
    
    # Shear angle term: only applies if wind is veering (130-250 at 850, 210-310 at 500)
    dir_diff = wind_dir_500_deg - wind_dir_850_deg
    shear_term = 0.0
    if (
        (130.0 <= wind_dir_850_deg <= 250.0) 
        and (210.0 <= wind_dir_500_deg <= 310.0) 
        and dir_diff > 0 
        and wind_speed_850_kt >= 15.0 
        and wind_speed_500_kt >= 15.0
    ):
        shear_term = 125.0 * (math.sin(math.radians(dir_diff)) + 0.2)
        
    sweat = td_term + tt_term + v850_term + v500_term + shear_term
    return float(sweat)


def evaluate_severe_diagnostics(
    pressure_levels_hpa: np.ndarray,
    temp_levels_c: np.ndarray,
    dewpoint_levels_c: np.ndarray,
    height_levels_m: np.ndarray,
    u_profile_m_s: np.ndarray,
    v_profile_m_s: np.ndarray,
    sbcape_j_kg: float,
    sbcin_j_kg: float,
    lcl_height_m: float,
    srh_0_1km: float,
    srh_0_3km: float,
    bulk_shear_0_6km_m_s: float,
) -> SevereStormDiagnostics:
    """
    Synthesizes complete multi-level atmospheric physics into operational hazard verdicts.
    """
    dcape, v_gust_m_s = downdraft_cape(pressure_levels_hpa, temp_levels_c, dewpoint_levels_c, height_levels_m)
    v_gust_kmh = v_gust_m_s * 3.6
    
    stp = significant_tornado_parameter(sbcape_j_kg, lcl_height_m, srh_0_1km, bulk_shear_0_6km_m_s, sbcin_j_kg)
    
    # Hail calculations
    fz_m, wbz_m, hgz_cape, mehs_mm = hail_diagnostics(
        pressure_levels_hpa, temp_levels_c, dewpoint_levels_c, height_levels_m, sbcape_j_kg
    )
    
    # SWEAT calculation using 850 and 500 hPa winds
    def interp_lvl(target_p: float, field: np.ndarray) -> float:
        return float(np.interp(target_p, pressure_levels_hpa[::-1], field[::-1]))
        
    t850 = interp_lvl(850.0, temp_levels_c)
    td850 = interp_lvl(850.0, dewpoint_levels_c)
    t500 = interp_lvl(500.0, temp_levels_c)
    u850 = interp_lvl(850.0, u_profile_m_s)
    v850 = interp_lvl(850.0, v_profile_m_s)
    u500 = interp_lvl(500.0, u_profile_m_s)
    v500 = interp_lvl(500.0, v_profile_m_s)
    
    spd850_kt = math.sqrt(u850**2 + v850**2) * 1.94384
    spd500_kt = math.sqrt(u500**2 + v500**2) * 1.94384
    dir850_deg = (math.degrees(math.atan2(-u850, -v850)) + 360.0) % 360.0
    dir500_deg = (math.degrees(math.atan2(-u500, -v500)) + 360.0) % 360.0
    
    sweat_val = sweat_index(t850, td850, t500, spd850_kt, spd500_kt, dir850_deg, dir500_deg)
    
    # Storm Mode Classification
    if sbcape_j_kg < 250.0:
        storm_mode = "STABLE / NON-CONVECTIVE"
    elif bulk_shear_0_6km_m_s >= 20.0 and srh_0_3km >= 150.0:
        storm_mode = "SUPERCELL (ROTATING UPDRAFT)"
    elif bulk_shear_0_6km_m_s >= 15.0:
        storm_mode = "ORGANIZED MULTICELL / SQUALL LINE"
    else:
        storm_mode = "DISORGANIZED PULSE / SINGLE-CELL"
        
    # Hail threat
    if mehs_mm >= 50.0:
        hail_cat = "DESTRUCTIVE GIANT HAIL (> 5.0 cm, VEHICLE & ROOF DAMAGE)"
    elif mehs_mm >= 25.0:
        hail_cat = "SEVERE LARGE HAIL (2.5 - 5.0 cm, CROP DEVASTATION)"
    elif mehs_mm >= 10.0:
        hail_cat = "MODERATE SMALL HAIL (1.0 - 2.5 cm)"
    else:
        hail_cat = "NIL / SUB-SEVERE HAIL (< 1.0 cm)"
        
    # Tornado risk
    if stp >= 3.0:
        tor_cat = "VIOLENT TORNADO RISK (EF3+ POTENTIAL)"
    elif stp >= 1.0:
        tor_cat = "SIGNIFICANT TORNADO RISK (EF2+ POTENTIAL)"
    elif stp >= 0.5:
        tor_cat = "MARGINAL TORNADIC SUPERCELL RISK"
    else:
        tor_cat = "MINIMAL / NON-TORNADIC"
        
    # Wind damage risk
    if v_gust_kmh >= 115.0:
        wind_cat = "CATASTROPHIC DOWNDRAFT / DERECHO GUSTS (TREES & TOWERS COLLAPSE)"
    elif v_gust_kmh >= 90.0:
        wind_cat = "SEVERE MICROBURST SQUALL (HIGH AVIATION & STRUCTURAL RISK)"
    elif v_gust_kmh >= 65.0:
        wind_cat = "STRONG CONVECTIVE GUSTS (ROOF SHEET DAMAGE)"
    else:
        wind_cat = "NORMAL CONVECTIVE BREEZE"
        
    # Supercell Composite
    from .kinematics import supercell_composite_parameter
    scp = supercell_composite_parameter(sbcape_j_kg, bulk_shear_0_6km_m_s, srh_0_3km)
    
    return SevereStormDiagnostics(
        storm_mode=storm_mode,
        dcape_j_kg=float(dcape),
        max_microburst_gust_kmh=float(v_gust_kmh),
        significant_tornado_parameter=float(stp),
        supercell_composite_parameter=float(scp),
        sweat_index=float(sweat_val),
        freezing_level_m_agl=float(fz_m),
        wet_bulb_zero_m_agl=float(wbz_m),
        hail_growth_zone_cape_j_kg=float(hgz_cape),
        max_expected_hail_size_mm=float(mehs_mm),
        hail_threat_category=hail_cat,
        tornado_risk_category=tor_cat,
        wind_damage_risk=wind_cat,
    )
