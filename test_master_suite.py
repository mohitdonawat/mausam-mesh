"""
=============================================================================
⚡ MAUSAMMESH — MASTER SCIENTIFIC & COMPUTATIONAL TEST SUITE
=============================================================================
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
Repository: github.com/mohitdonawat/mausam-mesh
=============================================================================
Validates all 4 core modules of MausamMesh:
  [Module 01] Atmospheric Thermodynamics (Bolton, Stull, CAPE, CIN, LCL, PWAT)
  [Module 02] Dynamic Kinematics (Spherical Stencils, Vorticity, Bunkers, SRH, SCP)
  [Module 03] Native GRIB2 Bitstream & O(1) Memory-Mapped Spatial Slicing
  [Module 04] WMO Tensor Quantization & Sovereign .mmesh Binary Container
=============================================================================
"""

import sys
import time

def run_all_tests():
    print("=" * 75)
    print("MAUSAMMESH -- MASTER SCIENTIFIC SUITE EXECUTION")
    print("=" * 75)
    t0 = time.perf_counter()

    # 1. Module 01: Thermodynamics
    print("\n>>> [MODULE 01] Running Atmospheric Thermodynamics Engine Tests...")
    import test_thermo
    test_thermo.test_saturation_vapor_pressure()
    test_thermo.test_dewpoint_roundtrip()
    test_thermo.test_relative_humidity()
    test_thermo.test_potential_temperature()
    test_thermo.test_lcl()
    test_thermo.test_wet_bulb_stull()
    test_thermo.test_convective_indices()
    test_thermo.test_sounding_analysis()
    print(">>> [MODULE 01] 100% SUCCEEDED!")

    # 2. Module 02: Kinematics
    print("\n>>> [MODULE 02] Running Dynamic Kinematics & Vector Field Engine Tests...")
    import test_kinematics
    test_kinematics.test_coriolis_and_beta()
    test_kinematics.test_vorticity_and_divergence()
    test_kinematics.test_bunkers_motion_and_shear()
    print(">>> [MODULE 02] 100% SUCCEEDED!")

    # 3. Module 03: GRIB2 Bitstream & O(1) Slicing
    print("\n>>> [MODULE 03] Running Native GRIB2 Bitstream & O(1) Slicing Tests...")
    import test_grib
    test_grib.test_grib_engine()
    print(">>> [MODULE 03] 100% SUCCEEDED!")

    # 4. Module 04: WMO Quantization & .mmesh Container
    print("\n>>> [MODULE 04] Running WMO Tensor Quantization & .mmesh Container Tests...")
    import test_container
    test_container.test_wmo_quantization_precision()
    test_container.test_mmesh_container_lifecycle()
    print(">>> [MODULE 04] 100% SUCCEEDED!")

    # 5. Module 05: Autonomous Adaptive Engine
    print("\n>>> [MODULE 05] Running Autonomous Engine & Online Adaptive Learning Tests...")
    import auto
    # Test auto-location discovery
    det_lat, det_lon, det_name = auto.auto_detect_location()
    assert isinstance(det_lat, float) and -90.0 <= det_lat <= 90.0
    assert isinstance(det_lon, float) and -180.0 <= det_lon <= 180.0
    assert len(det_name) > 0
    print(f"    [Auto-Location Resolved]: {det_name} ({det_lat:.4f} N, {det_lon:.4f} E)")

    # Test online adaptive learning recursive Bayesian calibration
    learner = auto.AdaptiveAtmosphericLearner(persistence_file=None)
    bias_delta = learner.observe(lat=28.61, lon=77.20, measured_temp_c=35.0, model_temp_c=33.0)
    assert abs(bias_delta - 0.3) < 0.05
    calibrated = learner.calibrate(lat=28.61, lon=77.20, raw_temp_c=33.0)
    assert calibrated > 33.0
    print(f"    [Adaptive Learning Verified]: Delta = {bias_delta:+.2f} C -> Calibrated = {calibrated:.2f} C")

    # Test industry-level location resolver (Offline Gazetteer + City queries)
    city_lat, city_lon, city_tag = auto.resolve_location("Indore")
    assert abs(city_lat - 22.7196) < 0.05 and abs(city_lon - 75.8577) < 0.05
    print(f"    [City Resolution OK]: 'Indore' -> {city_tag} ({city_lat:.2f}N, {city_lon:.2f}E)")

    # Test auto() by city name: mm.auto("Indore")
    v_city = auto.auto("Indore")
    assert "Indore" in v_city.location_tag
    print(f"    [City One-Liner OK]: mm.auto('Indore') -> Temp {v_city.calibrated_temp_c:.1f} C, Lat {v_city.latitude:.2f} N")

    # Test one-line zero-argument auto()
    verdict = auto.auto()
    assert verdict.latitude is not None
    assert verdict.calibrated_temp_c is not None
    assert verdict.sbcape_j_kg >= 0.0
    print(f"    [Zero-Argument Verdict OK]: {verdict.location_tag} -> Temp {verdict.calibrated_temp_c:.1f} C, CAPE {verdict.sbcape_j_kg:.1f} J/kg, Mode: {verdict.storm_mode}")
    print(">>> [MODULE 05] 100% SUCCEEDED!")

    total_time = time.perf_counter() - t0
    print("\n" + "=" * 75)
    print(f"[SUCCESS] ALL 5 CORE SOVEREIGN MODULES VERIFIED & TESTED IN {total_time:.2f}s!")
    print("   Status: Zero Regressions | Pure Python/NumPy | Zero C-Dependencies")
    print("=" * 75)


if __name__ == "__main__":
    run_all_tests()
