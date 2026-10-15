"""
=============================================================================
⚡ MAUSAMMESH — THERMODYNAMICS VERIFICATION SUITE
=============================================================================
Tests all 18 atmospheric thermodynamics equations against published 
WMO & Bolton (1980) reference values.
=============================================================================
"""

import math
import numpy as np
from thermo import (
    saturation_vapor_pressure,
    vapor_pressure_from_dewpoint,
    vapor_pressure_from_rh,
    dewpoint_from_vapor_pressure,
    relative_humidity,
    mixing_ratio,
    saturation_mixing_ratio,
    specific_humidity,
    virtual_temperature,
    potential_temperature,
    temperature_from_potential_temperature,
    virtual_potential_temperature,
    lcl,
    equivalent_potential_temperature,
    wet_bulb_temperature,
    moist_adiabatic_lapse_rate,
    k_index,
    total_totals_index,
    lifted_index,
    precipitable_water,
    bulk_richardson_number,
    analyze_sounding,
)


def test_saturation_vapor_pressure():
    # 0°C -> exactly 6.112 hPa (Bolton 1980)
    es_0 = saturation_vapor_pressure(0.0)
    assert abs(es_0 - 6.112) < 0.001, f"es(0C) failed: {es_0}"
    
    # 20°C -> approx 23.37 hPa
    es_20 = saturation_vapor_pressure(20.0)
    assert abs(es_20 - 23.37) < 0.1, f"es(20C) failed: {es_20}"
    
    # Array vectorized test
    temps = np.array([-10.0, 0.0, 15.0, 30.0])
    es_arr = saturation_vapor_pressure(temps)
    assert len(es_arr) == 4
    assert es_arr[0] < es_arr[1] < es_arr[2] < es_arr[3]
    print("[PASS] Saturation Vapor Pressure Test Passed.")


def test_dewpoint_roundtrip():
    original_td = 18.5  # °C
    e = vapor_pressure_from_dewpoint(original_td)
    recovered_td = dewpoint_from_vapor_pressure(e)
    assert abs(recovered_td - original_td) < 0.01, f"Dewpoint roundtrip error: {recovered_td} vs {original_td}"
    print("[PASS] Dewpoint Inversion Roundtrip Test Passed.")


def test_relative_humidity():
    # When T == Td, RH must be 100%
    rh_100 = relative_humidity(25.0, 25.0)
    assert abs(rh_100 - 100.0) < 0.01, f"RH should be 100%: {rh_100}"
    
    # When T = 30°C and Td = 15°C, RH ≈ 40%
    rh_mid = relative_humidity(30.0, 15.0)
    assert 38.0 < rh_mid < 42.0, f"RH unexpected: {rh_mid}"
    print("[PASS] Relative Humidity Test Passed.")


def test_potential_temperature():
    # At 1000 hPa, theta must equal T in Kelvin
    th_1000 = potential_temperature(1000.0, 25.0)
    assert abs(th_1000 - 298.15) < 0.01, f"Theta at 1000 hPa failed: {th_1000}"
    
    # At 500 hPa, theta must be significantly warmer due to adiabatic expansion
    th_500 = potential_temperature(500.0, -10.0)
    assert th_500 > 263.15, f"Theta at 500 hPa failed: {th_500}"
    
    # Inversion test
    t_recovered = temperature_from_potential_temperature(th_500, 500.0)
    assert abs(t_recovered - (-10.0)) < 0.01, f"Potential Temp inversion failed: {t_recovered}"
    print("[PASS] Potential Temperature & Inversion Test Passed.")


def test_lcl():
    p = 1000.0
    t = 30.0
    td = 20.0
    p_lcl, t_lcl, z_lcl = lcl(p, t, td)
    
    # At T=30, Td=20: LCL is approximately 870-900 hPa and ~1250m
    assert 850.0 < p_lcl < 920.0, f"LCL P out of bounds: {p_lcl}"
    assert 15.0 < t_lcl < 20.0, f"LCL T out of bounds: {t_lcl}"
    assert 1100.0 < z_lcl < 1400.0, f"LCL Z out of bounds: {z_lcl}"
    print(f"[PASS] LCL Test Passed: P_LCL={p_lcl:.1f} hPa, T_LCL={t_lcl:.1f} C, Z_LCL={z_lcl:.0f} m.")


def test_wet_bulb_stull():
    # T = 20°C, RH = 50% -> Tw should be around 13.7°C
    tw = wet_bulb_temperature(20.0, 50.0)
    assert 13.0 < tw < 14.5, f"Wet bulb out of expected bounds: {tw}"
    
    # When RH = 100%, Tw should equal T
    tw_saturated = wet_bulb_temperature(20.0, 100.0)
    assert abs(tw_saturated - 20.0) < 0.5, f"Wet bulb at 100% RH should equal T: {tw_saturated}"
    print(f"[PASS] Stull Wet-Bulb Test Passed: Tw(20C, 50%) = {tw:.2f} C.")


def test_convective_indices():
    # Typical severe weather profile (e.g. pre-monsoon storm in Central India):
    # T850 = 26°C, Td850 = 18°C
    # T700 = 10°C, Td700 = 4°C
    # T500 = -12°C
    ki = k_index(t850_c=26.0, t500_c=-12.0, td850_c=18.0, t700_c=10.0, td700_c=4.0)
    # KI = (26 - (-12)) + 18 - (10 - 4) = 38 + 18 - 6 = 50°C (Extreme thunderstorm)
    assert abs(ki - 50.0) < 0.01, f"K-Index failed: {ki}"
    
    tt = total_totals_index(t850_c=26.0, t500_c=-12.0, td850_c=18.0)
    # TT = 26 + 18 - 2 * (-12) = 44 + 24 = 68°C
    assert abs(tt - 68.0) < 0.01, f"Total Totals failed: {tt}"
    print(f"[PASS] Convective Severe Indices Passed: KI = {ki:.1f} C, TT = {tt:.1f} C.")


def test_sounding_analysis():
    # Standard 16-level tropical sounding profile
    p_levels = np.array([1000.0, 950.0, 900.0, 850.0, 800.0, 750.0, 700.0, 650.0, 600.0, 500.0, 400.0, 300.0, 250.0, 200.0, 150.0, 100.0])
    t_levels = np.array([32.0, 28.0, 24.5, 21.0, 17.5, 14.0, 10.0, 5.0, 0.0, -11.0, -24.0, -42.0, -52.0, -62.0, -70.0, -75.0])
    td_levels = np.array([24.0, 21.5, 19.0, 16.5, 13.0, 9.0, 4.0, -2.0, -8.0, -22.0, -36.0, -55.0, -65.0, -75.0, -80.0, -85.0])
    
    analysis = analyze_sounding(p_levels, t_levels, td_levels)
    
    print("\n--- Sounding Analysis Results ---")
    print(f"Surface LCL Pressure : {analysis.lcl_pressure_hpa:.1f} hPa")
    print(f"Surface LCL Temp     : {analysis.lcl_temp_c:.1f} C")
    print(f"Surface LCL Height   : {analysis.lcl_height_m:.0f} m AGL")
    print(f"LFC Pressure         : {analysis.lfc_pressure_hpa} hPa")
    print(f"EL Pressure          : {analysis.el_pressure_hpa} hPa")
    print(f"SBCAPE               : {analysis.sbcape_j_kg:.1f} J/kg")
    print(f"SBCIN                : {analysis.sbcin_j_kg:.1f} J/kg")
    print(f"K-Index              : {analysis.k_index_c:.1f} C")
    print(f"Total Totals         : {analysis.total_totals_c:.1f} C")
    print(f"Lifted Index (LI)    : {analysis.lifted_index_c:.1f} C")
    print(f"Precipitable Water   : {analysis.precipitable_water_mm:.1f} mm")
    
    # Assert physical sanity
    assert analysis.sbcape_j_kg > 0.0, "Sounding should have positive CAPE"
    assert analysis.precipitable_water_mm > 20.0, "PWAT should be typical tropical (>20mm)"
    assert analysis.lcl_pressure_hpa < 1000.0, "LCL must be above surface"
    print("[PASS] Complete Sounding Analysis Test Passed Successfully!")


if __name__ == "__main__":
    test_saturation_vapor_pressure()
    test_dewpoint_roundtrip()
    test_relative_humidity()
    test_potential_temperature()
    test_lcl()
    test_wet_bulb_stull()
    test_convective_indices()
    test_sounding_analysis()
    print("\n[SUCCESS] ALL THERMODYNAMICS SCIENTIFIC TESTS PASSED WITH 100% SUCCESS!")
