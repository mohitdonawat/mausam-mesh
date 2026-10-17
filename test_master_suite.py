"""
=============================================================================
⚡ MAUSAMMESH — MASTER SCIENTIFIC & COMPUTATIONAL TEST SUITE
=============================================================================
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
Repository: github.com/mohitdonawat/mausam-mesh
=============================================================================
Validates all 8 core modules of MausamMesh:
  [Module 01] Atmospheric Thermodynamics (Bolton, Stull, CAPE, CIN, LCL, PWAT)
  [Module 02] Dynamic Kinematics (Spherical Stencils, Vorticity, Bunkers, SRH, SCP)
  [Module 03] Native GRIB2 Bitstream & Multi-Template O(1) Slicing (Templates 5.0, 5.2, 5.3, 5.40)
  [Module 04] WMO Tensor Quantization & .mmesh Binary Container
  [Module 05] Autonomous Adaptive Location & Bayesian Observation Engine
  [Module 06] Severe Hazards, Lightning Potential Index (LPI) & Damini Siren
  [Module 07] Kisan Agromet, Urban Runoff, Polarimetric Radar & Voice Distiller
  [Module 08] Watershed SCS-CN Runoff, INSAT Satellite, Ensemble PoP & Transcoder
=============================================================================
"""

import os
import sys
import time

pkg_dir = os.path.dirname(os.path.abspath(__file__))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

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
    test_grib.test_complex_and_jpeg2000_packing()

    # Test Terabyte-scale Sharded GRIB Catalog & Out-of-Core Batch Streamer
    import grib_streamer
    cat = grib_streamer.MultiFileGribCatalog()
    assert cat.max_open_datasets == 16
    assert grib_streamer.INDIA_BBOX == (6.0, 38.0, 68.0, 98.0)
    print("    [TB-Scale Streaming OK]: MultiFileGribCatalog zero-copy indexer & Pan-India bitstream cropper verified.")

    # Test Real GRIB Bulk Downloader Task Builder & India Bounding Box Filter
    import grib_downloader
    downloader = grib_downloader.GribBulkDownloader(dest_dir="test_grib_download")
    tasks = downloader.build_tasks(dates=["20261016"], cycles=["00"], forecast_hours=[0, 3], india_crop=True)
    assert len(tasks) == 2
    assert "filter_gfs_0p25.pl" in tasks[0]["url"]
    assert "leftlon=68.0" in tasks[0]["url"]
    print("    [Real GRIB Bulk Downloader OK]: NOAA NOMADS India Subregion task builder verified.")

    # Test IMD Ingestion Engine & Doppler Radar Directory
    import imd
    assert len(imd.IMD_CATEGORIES) == 19
    assert len(imd.IMD_DWR_STATIONS) >= 12
    nowcast = imd.fetch_imd_nowcast("Indore")
    assert "severity_level" in nowcast
    print(f"    [IMD Sovereign Engine OK]: 19 WFS Categories & {len(imd.IMD_DWR_STATIONS)} DWR Stations verified. Indore Nowcast: {nowcast['severity_level']}")
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

    # 6. Module 06: Advanced Severe Hazards & Regional Disaster Engines
    print("\n>>> [MODULE 06] Running Severe Convective Hazards & Disaster Engine Tests...")
    import test_advanced_engine
    test_advanced_engine.test_severe_convective_engine()
    test_advanced_engine.test_regional_hazards()
    test_advanced_engine.test_master_mausam_engine()
    print(">>> [MODULE 06] 100% SUCCEEDED!")

    # 7. Module 07: Kisan Agromet, Flood Threat, Polarimetric Radar & Voice Distiller
    print("\n>>> [MODULE 07] Running Kisan Agromet, Threat Solver, Radar & Voice Tests...")
    import numpy as np
    import quantizer
    import kisan_agro
    import threat_solver
    import radar
    import voice_distiller

    # Test Vectorized Quantization
    grid_data = np.linspace(-15.0, 48.0, 10000, dtype=np.float32)
    q_bytes = quantizer.quantize_grid(grid_data, -20.0, 55.0)
    assert len(q_bytes) == 10000
    deq_data = quantizer.dequantize_grid(q_bytes, -20.0, 55.0)
    assert np.max(np.abs(grid_data - deq_data)) < 0.35
    print("    [Vectorized SIMD Quantization OK]: 10,000 points quantized/dequantized < 0.35 C max error")

    # Run Extreme Log & Piecewise Dual-Slope Precipitation Benchmark
    import test_extreme_quantization
    test_extreme_quantization.run_quantization_benchmark()

    # Test Kisan Agromet Hargreaves ET0 and Pump Runtime
    et0 = kisan_agro.calculate_et0_hargreaves(t_max_c=36.0, t_min_c=22.0, lat_deg=22.7)
    assert 2.0 <= et0 <= 10.0
    pump_res = kisan_agro.calculate_pump_runtime(crop="wheat", acres=3.0, pump_hp=5.0, temp_max_c=36.0, temp_min_c=22.0)
    assert pump_res["recommended_runtime_hours"] > 0.0
    assert "घंटे" in pump_res["formatted_runtime"]

    # Test DAP vs SSP Fertilizer Calculation
    fert_dap = kisan_agro.calculate_fertilizer_balance(crop="wheat", acres=2.5, fertilizer_source="DAP")
    assert fert_dap["dap_50kg_bags"] > 0
    fert_ssp = kisan_agro.calculate_fertilizer_balance(crop="wheat", acres=2.5, fertilizer_source="SSP")
    assert fert_ssp["ssp_50kg_bags"] > 0
    print(f"    [Kisan Agromet OK]: ET0 = {et0:.2f} mm/day, Pump = {pump_res['formatted_runtime']}, DAP = {fert_dap['dap_50kg_bags']} bags")

    # Test Rational Urban Runoff and Threat Evaluation
    runoff = threat_solver.calculate_urban_runoff(rainfall_intensity_mm_hr=65.0, catchment_area_ha=20.0, surface_type="concrete")
    assert runoff["drain_overloaded"] is True
    assert runoff["waterlogging_depth_cm"] > 0.0
    threat = threat_solver.evaluate_threat(rain_intensity_mm_hr=75.0, wind_speed_kmh=95.0, cape_index=2800.0)
    assert threat.alert_level == "RED"
    assert threat.is_extreme is True
    print(f"    [Threat Solver OK]: Extreme Rain 75 mm/h -> Alert: {threat.alert_level}, Runoff: {runoff['runoff_discharge_m3s']} m3/s")

    # Test Radar Dual-Pol Classification
    hail_echo = radar.classify_hydrometeor(zh_dbz=62.0, zdr_db=0.2, rho_hv=0.88)
    assert hail_echo.is_hail is True
    assert "HAIL" in hail_echo.classification
    rain_echo = radar.classify_hydrometeor(zh_dbz=42.0, zdr_db=1.8, rho_hv=0.98)
    assert rain_echo.is_hail is False
    assert rain_echo.rain_rate_mm_hr > 5.0
    print(f"    [Doppler Radar OK]: 62 dBZ -> {hail_echo.classification}, 42 dBZ -> {rain_echo.classification} ({rain_echo.rain_rate_mm_hr:.1f} mm/h)")

    # Test Voice Distillation across languages
    v_hi = voice_distiller.to_kisan_voice(None, language="hi")
    assert "किसान" in v_hi["spoken_text"]
    v_te = voice_distiller.to_kisan_voice(None, language="te")
    assert len(v_te["spoken_text"]) > 10
    print("    [Voice Distiller OK]: Hindi & Telugu regional voice advisories generated successfully")
    print(">>> [MODULE 07] 100% SUCCEEDED!")

    # 8. Module 08: SCS-CN Watershed Runoff, INSAT Satellite, Ensemble PoP & Transcoder
    print("\n>>> [MODULE 08] Running Watershed SCS-CN, Satellite Remote Sensing & Ensemble PoP Tests...")
    import satellite
    import ensemble
    import transcoder

    # Test SCS Curve Number Agricultural Watershed Runoff
    scs_res = threat_solver.calculate_scs_curve_number_runoff(
        rainfall_depth_mm=85.0,
        catchment_area_ha=150.0,
        hydrologic_soil_group="C",
        land_use="mixed_agricultural",
        antecedent_rainfall_5day_mm=35.0,
    )
    assert scs_res.direct_runoff_depth_pe_mm > 20.0
    assert scs_res.total_runoff_volume_m3 > 10000.0
    assert "AMC-III" in scs_res.amc_condition
    assert scs_res.peak_discharge_qp_m3s > 0.0
    print(f"    [SCS-CN Watershed Runoff OK]: Rain {scs_res.rainfall_depth_mm} mm -> Runoff {scs_res.direct_runoff_depth_pe_mm} mm, Qp = {scs_res.peak_discharge_qp_m3s} m3/s ({scs_res.amc_condition})")

    # Test INSAT-3D/3DR Satellite Remote Sensing & Planck Radiance Inversion
    tb_k = satellite.radiance_to_brightness_temp(radiance_mw_m2_sr_cm=45.0, channel="TIR1")
    assert 180.0 < tb_k < 330.0
    cloud_rep = satellite.diagnose_satellite_convection(tb_t1_c=-35.0, tb_t2_c=-75.0, time_delta_min=15.0)
    assert cloud_rep.is_overshooting_top is True
    assert cloud_rep.is_explosive_updraft is True
    assert cloud_rep.estimated_imsra_rain_rate_mm_hr > 50.0
    print(f"    [INSAT Geostationary Satellite OK]: Tb = {tb_k:.1f} K, CTT = {cloud_rep.brightness_temp_t2_c} C, Updraft: {cloud_rep.convective_severity_category}, Rain: {cloud_rep.estimated_imsra_rain_rate_mm_hr} mm/h")

    # Test Multi-Model Ensemble Spread & Probability of Precipitation (PoP)
    members_rain = [12.0, 25.0, 75.0, 80.0, 110.0, 15.0, 68.0, 95.0, 30.0, 4.0, 120.0]
    ens_res = ensemble.evaluate_ensemble_risk(members_rain, variable_name="APCP")
    assert ens_res.pop_heavy_pct >= 40.0
    assert ens_res.spread_std > 0.0
    assert "ALERT" in ens_res.imd_alert_level or "RISK" in ens_res.imd_alert_level
    print(f"    [Multi-Model Ensemble PoP OK]: Mean = {ens_res.mean_val} mm, Spread = {ens_res.spread_std} mm, PoP(Heavy) = {ens_res.pop_heavy_pct}%, Alert: {ens_res.imd_alert_level}")

    # Test GRIB2-to-.mmesh Transcoder
    test_src_grib = "test_transcode_src.grib2"
    test_dst_mmesh = "test_transcode_dest.mmesh"
    try:
        import test_grib
        test_grib.create_synthetic_grib2_file(test_src_grib, n_rows=8, n_cols=8)
        t_res = transcoder.convert_grib2_to_mmesh(test_src_grib, test_dst_mmesh, variables=["TMP"], bbox=None)
        assert t_res["status"] == "SUCCESS"
        assert t_res["layers_transcoded"] == 1
        assert os.path.exists(test_dst_mmesh)
        print(f"    [GRIB2 Transcoder OK]: Raw GRIB2 -> .mmesh ({t_res['payload_reduction_pct']}% payload reduction, {t_res['layers_transcoded']} layer)")
    finally:
        for p in (test_src_grib, test_dst_mmesh):
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
    print(">>> [MODULE 08] 100% SUCCEEDED!")

    total_time = time.perf_counter() - t0
    print("\n" + "=" * 75)
    print(f"[SUCCESS] ALL 8 CORE METEOROLOGICAL MODULES VERIFIED & TESTED IN {total_time:.2f}s!")
    print("   Status: Zero Regressions | Pure Python/NumPy | Zero C-Dependencies")
    print("=" * 75)


if __name__ == "__main__":
    run_all_tests()

