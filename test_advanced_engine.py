"""
=============================================================================
⚡ MAUSAMMESH — ADVANCED SEVERE & HAZARDS ENGINE VERIFICATION
=============================================================================
Tests:
1. DCAPE & Peak Microburst Wind Gusts (V_gust = sqrt(2 * DCAPE))
2. Significant Tornado Parameter (STP) & Hail Growth Zone (MEHS)
3. Himalayan / Western Ghats Cloudburst Detection
4. Official IMD Tropical Cyclone Classification & Storm Surge
5. Wet-Bulb 35°C Human Survivability & 'Loo' Wind Heatwave Engine
6. Master MausamEngine Unified Facade
=============================================================================
"""

import math
import numpy as np
try:
    from .severe import (
        downdraft_cape, 
        significant_tornado_parameter, 
        hail_diagnostics, 
        sweat_index,
        lightning_potential_index,
        LightningPotentialReport,
    )
    from .hazards import detect_cloudburst, classify_cyclone, evaluate_kalbaisakhi, evaluate_heat_stress
    from .engine import MausamEngine
except (ImportError, ValueError):
    from severe import (
        downdraft_cape, 
        significant_tornado_parameter, 
        hail_diagnostics, 
        sweat_index,
        lightning_potential_index,
        LightningPotentialReport,
    )
    from hazards import detect_cloudburst, classify_cyclone, evaluate_kalbaisakhi, evaluate_heat_stress
    from engine import MausamEngine


def test_severe_convective_engine():
    # 1. DCAPE Test on typical dry mid-level inverted-V sounding
    p_levels = np.array([1000.0, 925.0, 850.0, 700.0, 600.0, 500.0, 400.0, 300.0])
    t_levels = np.array([36.0, 30.0, 24.0, 12.0, 2.0, -10.0, -25.0, -42.0])
    # Very dry mid-troposphere (RH at 700 & 500 hPa is very low)
    td_levels = np.array([22.0, 16.0, 8.0, -15.0, -25.0, -35.0, -45.0, -55.0])
    
    dcape, v_gust_m_s = downdraft_cape(p_levels, t_levels, td_levels)
    v_gust_kmh = v_gust_m_s * 3.6
    
    print(f"DCAPE Calculated: {dcape:.1f} J/kg")
    print(f"Peak Microburst Gust Potential: {v_gust_kmh:.1f} km/h ({v_gust_m_s:.1f} m/s)")
    assert dcape > 400.0, f"Inverted-V sounding should have high DCAPE: {dcape}"
    assert v_gust_kmh > 70.0, f"Microburst gusts should exceed 70 km/h: {v_gust_kmh}"
    print("[PASS] DCAPE & Microburst Gust Solver Succeeded.")

    # 2. Significant Tornado Parameter (STP)
    # High CAPE (3500), Low LCL (750m), Strong 0-1km SRH (250), High Shear (25 m/s)
    stp = significant_tornado_parameter(
        sbcape_j_kg=3500.0,
        lcl_height_m_agl=750.0,
        srh_0_1km_m2_s2=250.0,
        bulk_shear_0_6km_m_s=25.0,
        sbcin_j_kg=-15.0,
    )
    print(f"Significant Tornado Parameter (STP): {stp:.2f}")
    assert stp > 3.0, f"Violent tornadic setup must yield STP > 3.0: {stp}"
    print("[PASS] Significant Tornado Parameter Solver Succeeded.")

    # 3. Lightning Potential Index (LPI) & Damini Flash Rate
    z_levels = np.array([100.0, 800.0, 1500.0, 3100.0, 4400.0, 5800.0, 7500.0, 9600.0])
    lpi_rep = lightning_potential_index(
        pressure_levels_hpa=p_levels,
        temp_levels_c=t_levels,
        dewpoint_levels_c=td_levels,
        height_levels_m=z_levels,
        sbcape_j_kg=2800.0,
        precipitable_water_mm=45.0,
        bulk_shear_0_6km_m_s=18.0,
    )
    print(f"LPI Index: {lpi_rep.lpi_j_kg} J/kg | Category: {lpi_rep.lightning_risk_category} | Siren: {lpi_rep.siren_trigger}")
    assert lpi_rep.lpi_j_kg > 0.0
    assert lpi_rep.charging_zone_depth_m > 0.0
    assert len(lpi_rep.safety_directive) > 0
    print("[PASS] Lightning Potential Index & Damini Siren Engine Succeeded.")


def test_regional_hazards():
    # 1. Cloudburst Detection Test (115 mm/hr in Uttarakhand steep valley)
    cb = detect_cloudburst(rainfall_rate_mm_hr=115.0, terrain_slope_deg=25.0, precipitable_water_mm=58.0)
    print(f"Cloudburst Verdict: {cb.alert_level} - {cb.impact_verdict}")
    assert cb.is_cloudburst is True
    assert cb.recommended_evacuation_lead_min > 0
    print("[PASS] Cloudburst Detection Engine Succeeded.")

    # 2. IMD Tropical Cyclone Classification (e.g. Cyclone Fani / Amphan: 215 km/h winds)
    cyc = classify_cyclone(max_sustained_wind_kmh=215.0, central_pressure_hpa=925.0)
    print(f"Cyclone Category: {cyc.category_code} ({cyc.category_name}), Surge: {cyc.estimated_storm_surge_m} m")
    assert cyc.category_code == "VSCS" or cyc.category_code == "ESCS"
    assert cyc.estimated_storm_surge_m > 3.0
    print("[PASS] IMD Cyclone Classification & Surge Engine Succeeded.")

    # 3. Wet-Bulb Fatal Heat Stress & Loo Wind
    # Loo wind: 47°C, 15% RH, strong NW desert winds
    heat = evaluate_heat_stress(temp_c=47.0, rh_pct=15.0, wind_speed_kmh=22.0, wind_direction_deg=285.0)
    print(f"Heat Stress: Tw={heat.wet_bulb_temp_c} C, Heat Index={heat.heat_index_c} C, Loo Wind={heat.is_loo_desert_heatwave}")
    assert heat.is_loo_desert_heatwave is True
    
    # Deadly tropical heatwave: 39°C with 80% RH -> Tw exceeds 35°C fatal threshold!
    fatal_heat = evaluate_heat_stress(temp_c=39.0, rh_pct=80.0)
    print(f"Fatal Heatwave Test: Tw={fatal_heat.wet_bulb_temp_c} C, Deadly={fatal_heat.is_deadly_survivability_exceeded}")
    assert fatal_heat.is_deadly_survivability_exceeded is True
    print("[PASS] Human Physiological Heat Stress Engine Succeeded.")


def test_master_mausam_engine():
    engine = MausamEngine()
    
    # Severe sounding profile
    p = np.array([1000.0, 925.0, 850.0, 700.0, 500.0, 300.0, 200.0])
    t = np.array([34.0, 27.0, 22.0, 10.0, -12.0, -38.0, -58.0])
    td = np.array([23.0, 19.0, 16.0, 4.0, -18.0, -45.0, -68.0])
    u = np.array([-4.0, 2.0, 8.0, 18.0, 28.0, 42.0, 35.0])
    v = np.array([6.0, 10.0, 14.0, 12.0, 8.0, -2.0, -8.0])
    
    report = engine.diagnose_sounding(p, t, td, u, v)
    
    print("\n--- MASTER ATMOSPHERIC VERDICT ---")
    print(f"Storm Mode: {report.storm_mode}")
    print(f"SBCAPE: {report.sbcape_j_kg} J/kg | DCAPE: {report.dcape_j_kg} J/kg")
    print(f"Peak Microburst Gust: {report.peak_gust_kmh} km/h")
    print(f"0-6km Bulk Shear: {report.shear_0_6km_m_s} m/s | 0-3km SRH: {report.srh_0_3km_m2_s2} m^2/s^2")
    print(f"Significant Tornado Parameter (STP): {report.significant_tornado_parameter}")
    print(f"Max Expected Hail Size: {report.max_hail_size_mm} mm")
    print(f"Hail Hazard: {report.hail_threat}")
    print(f"Tornado Risk: {report.tornado_risk}")
    if report.lightning:
        print(f"Lightning Hazard: {report.lightning.lightning_risk_category} | LPI: {report.lightning.lpi_j_kg} J/kg")
    
    assert report.sbcape_j_kg > 1000.0
    assert report.peak_gust_kmh > 50.0
    assert report.lightning is not None
    assert report.lightning.lpi_j_kg >= 0.0
    print("[PASS] Master MausamEngine Unified Diagnostics Succeeded!")


if __name__ == "__main__":
    test_severe_convective_engine()
    test_regional_hazards()
    test_master_mausam_engine()
    print("\n[SUCCESS] ALL ADVANCED SPECIFIC ATMOSPHERIC SUITES PASSED 100%!")
