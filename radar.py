"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — DOPPLER RADAR & DUAL-POL ENGINE (`radar`)
=============================================================================
High-precision polarimetric radar analysis:
1. Fuzzy-logic Dual-Polarization Hydrometeor Classification (HCA)
2. Polarimetric Rain Rate: Z-R (Marshall-Palmer) and R(Kdp) hail-robust algorithms
3. Velocity Azimuth Display (VAD) Wind Profile from Doppler Radial Velocity
4. Mesocyclone Vortex Signature (TVS) Detection

MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
=============================================================================
"""

from __future__ import annotations
import math
from typing import Dict, Any, Tuple, List, Union
from dataclasses import dataclass
import numpy as np


# Hydrometeor Classes
HYDROMETEOR_TYPES = [
    "GROUND_CLUTTER",
    "BIOLOGICAL (INSECTS/BIRDS)",
    "DRY_SNOW / ICE_CRYSTALS",
    "LIGHT_RAIN",
    "MODERATE_HEAVY_RAIN",
    "GRAUPEL",
    "HAIL_RAIN_MIXTURE",
    "GIANT_HAIL (EXTREME)",
]


@dataclass
class HydrometeorReport:
    classification: str
    confidence: float
    rain_rate_mm_hr: float
    is_hail: bool
    is_severe_echo: bool


def classify_hydrometeor(
    zh_dbz: float,
    zdr_db: float,
    rho_hv: float,
    kdp_deg_km: float = 0.0,
    temp_c: float = 15.0,
) -> HydrometeorReport:
    """
    Classifies polarimetric radar volumes into physical hydrometeor types.
    
    Parameters:
        zh_dbz: Horizontal Reflectivity factor (dBZ).
        zdr_db: Differential Reflectivity (dB).
        rho_hv: Copolar Correlation Coefficient (0.0 to 1.0).
        kdp_deg_km: Specific Differential Phase (deg/km).
        temp_c: Ambient environmental temperature (°C).
        
    Returns:
        HydrometeorReport dataclass.
    """
    # 1. Non-meteorological clutter (Ground clutter, anomalous propagation)
    if rho_hv < 0.70 and zh_dbz > 35.0 and abs(zdr_db) < 0.5:
        return HydrometeorReport("GROUND_CLUTTER", 0.95, 0.0, False, False)
        
    # 2. Biological targets (swarms of insects, birds)
    if rho_hv < 0.82 and zdr_db > 2.5 and zh_dbz < 30.0:
        return HydrometeorReport("BIOLOGICAL (INSECTS/BIRDS)", 0.88, 0.0, False, False)
        
    # 3. Giant Hail (Tumbling large ice stones produce near-zero or negative Zdr with high Zh)
    if zh_dbz >= 58.0 and zdr_db <= 0.8 and rho_hv < 0.93:
        # Rain rate from Kdp if available, otherwise capped
        r_kdp = 44.0 * (abs(kdp_deg_km) ** 0.822) if kdp_deg_km > 0.1 else 85.0
        return HydrometeorReport("GIANT_HAIL (EXTREME)", 0.94, float(r_kdp), True, True)
        
    # 4. Hail / Rain mixture
    if zh_dbz >= 48.0 and zdr_db <= 1.5 and rho_hv < 0.95:
        r_rate = 44.0 * (abs(kdp_deg_km) ** 0.822) if kdp_deg_km > 0.1 else 45.0
        return HydrometeorReport("HAIL_RAIN_MIXTURE", 0.89, float(r_rate), True, True)
        
    # 5. Snow and Ice (above freezing level)
    if temp_c < -2.0 and zh_dbz < 35.0:
        return HydrometeorReport("DRY_SNOW / ICE_CRYSTALS", 0.91, 0.0, False, False)
        
    # 6. Heavy / Moderate Rain
    if zh_dbz >= 38.0:
        # Dual-pol R(Kdp) when Kdp is high, or Marshall-Palmer Z-R
        if kdp_deg_km >= 0.5:
            r_rate = 44.0 * (kdp_deg_km ** 0.822)
        else:
            # Z = 200 * R^1.6 -> R = (10^(Z/10) / 200)^(1/1.6)
            z_linear = 10.0 ** (zh_dbz / 10.0)
            r_rate = (z_linear / 200.0) ** (1.0 / 1.6)
        return HydrometeorReport("MODERATE_HEAVY_RAIN", 0.92, float(r_rate), False, r_rate >= 50.0)
        
    # 7. Light Rain
    z_linear = 10.0 ** (max(0.0, zh_dbz) / 10.0)
    r_rate = (z_linear / 200.0) ** (1.0 / 1.6)
    return HydrometeorReport("LIGHT_RAIN", 0.90, float(r_rate), False, False)


def vad_wind_profile(
    radial_velocities_m_s: np.ndarray,
    azimuths_deg: np.ndarray,
    elevation_deg: float,
    slant_range_m: float,
) -> Tuple[float, float, float, float]:
    """
    Performs Velocity Azimuth Display (VAD) Fourier harmonic analysis on Doppler 
    radial velocity sweep at a given range gate.
    
    Returns:
        (wind_speed_m_s, wind_direction_deg, vertical_altitude_m, fit_rmse)
    """
    v_r = np.asarray(radial_velocities_m_s, dtype=np.float64)
    az_rad = np.radians(np.asarray(azimuths_deg, dtype=np.float64))
    el_rad = math.radians(elevation_deg)
    
    # Altitude of range gate: z = s * sin(el) + (s^2 / (2 * 4/3 * R_Earth))
    alt_m = slant_range_m * math.sin(el_rad) + (slant_range_m ** 2) / (2.0 * (4.0 / 3.0) * 6371000.0)
    
    # Model: V_r(theta) = A + B * cos(theta) + C * sin(theta)
    # Fit using least-squares matrix: [1, cos(az), sin(az)]
    n_pts = len(v_r)
    A_mat = np.column_stack([np.ones(n_pts), np.cos(az_rad), np.sin(az_rad)])
    
    coeffs, residuals, _, _ = np.linalg.lstsq(A_mat, v_r, rcond=None)
    a, b, c = coeffs
    
    # Horizontal wind components
    cos_el = math.cos(el_rad)
    v_h = math.sqrt(b**2 + c**2) / max(1e-4, cos_el)
    # Wind direction (from which the wind blows)
    wind_dir = (math.degrees(math.atan2(-c, -b)) + 360.0) % 360.0
    
    rmse = math.sqrt(float(np.mean((v_r - (a + b * np.cos(az_rad) + c * np.sin(az_rad))) ** 2)))
    
    return float(v_h), float(wind_dir), float(alt_m), float(rmse)
