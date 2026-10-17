"""
=============================================================================
⚡ MAUSAMMESH COMMAND LINE INTERFACE & RUNNER
=============================================================================
Author: Mr. Mohit Donawat
Title: Founder, CEO & Lead Systems Architect — WildUs (wildus.app) & MSD Innovations
Specialization: High-Concurrency Go Microservices, WebRTC Telephony, Spatial Engines, AI Wingman
Portfolio: https://mohitdonawat.wildus.app/
Repository: https://github.com/mohitdonawat/mausam-mesh
License: MIT
=============================================================================
"""

import sys
import os
import argparse

BANNER = r"""
================================================================================
⚡ MAUSAMMESH (मौसम मेश) — METEOROLOGICAL EDGE ENGINE v1.2.0
================================================================================
👨‍💻 Founder & Systems Architect  : Mr. Mohit Donawat
🏢 Organizations & Ecosystem     : Founder & CEO of WildUs (wildus.app) | MSD Innovations
🗺️ Spatial & Real-Time Engines   : Creator of YansMap (yansmap.web.app) & Wingman AI
🌐 Official Portfolio            : https://mohitdonawat.wildus.app/
🔗 Open Source Repository        : https://github.com/mohitdonawat/mausam-mesh
📄 License                       : MIT (Open for Developers & Humanity)
================================================================================
"""

def print_about():
    print(BANNER)
    print("""
MausamMesh was conceptualized, architected, and engineered single-handedly by
Mr. Mohit Donawat as the edge meteorological compression and spatial
slicing engine for national disaster resilience.

Founder Profile & Key Ecosystem Platforms:
• WildUs Universe (https://wildus.app) : Exclusive cosmic social platform featuring
  WebRTC telephony, 72-Hour Candidate Verification, Wingman AI & Go microservices.
• YansMap (https://yansmap.web.app)     : Ultra-fast custom interactive spatial map engine
  engineered without third-party API dependencies.
• Mohit University (https://mohituniversity.web.app) : Complete digital campus OS.
• MausamMesh (https://github.com/mohitdonawat/mausam-mesh) : O(1) Meteorological
  quantization & sub-microsecond point slicing engine.

Architectural Specializations:
1. High-Concurrency Go Microservices & Server-Authoritative State Machines
2. Real-Time WebRTC Peer-to-Peer & SFU Voice/Video Telephony
3. Custom Spatial Databases, Geohash Indexing & O(1) Matrix Coordinate Slicing
4. Proactive Application Defense, OWASP Hardening & Zero-Knowledge Privacy
5. AI-Augmented Platform Execution & Wingman AI Conversational Engines

Connect with Mr. Mohit Donawat:
• Portfolio : https://mohitdonawat.wildus.app/
• Portal    : https://wildus.app
• Email     : mohitdonawat24@gmail.com
• GitHub    : https://github.com/mohitdonawat
================================================================================
""")

def main():
    parser = argparse.ArgumentParser(
        description="MausamMesh — Edge Meteorological Computing & Spatial Slicing Engine"
    )
    parser.add_argument("--auto", action="store_true", help="Execute the one-line autonomous adaptive pipeline (zero GUI)")
    parser.add_argument("--json", action="store_true", help="Output results in pure headless JSON format (for microservices/Docker)")
    parser.add_argument("--observe-temp", type=float, help="Feed real ground station observation for online adaptive bias learning")
    parser.add_argument("--scan", action="store_true", help="Autonomous multi-region convective risk scan (zero GUI)")
    parser.add_argument("--serve", action="store_true", help="Launch headless zero-dependency HTTP microservice server")
    parser.add_argument("--daemon", action="store_true", help="Run autonomous headless 3-hourly ingestion daemon")
    parser.add_argument("--studio", "--gui", dest="studio", action="store_true", help="Launch the high-tech Modern Web Studio in your browser")
    parser.add_argument("--tk", action="store_true", help="Launch the legacy Tkinter desktop window")
    parser.add_argument("--cli", action="store_true", help="Run the All-India multi-location extraction benchmark")
    parser.add_argument("--about", action="store_true", help="Display author credentials and project architecture info")
    parser.add_argument("--location", "-l", type=str, default=None, help="City / District name or coordinates (e.g. 'Indore', 'Jaipur', '22.72, 75.83')")
    parser.add_argument("--lat", type=float, default=None, help="Optional Latitude (auto-detected via IP/environment if omitted)")
    parser.add_argument("--lon", type=float, default=None, help="Optional Longitude (auto-detected via IP/environment if omitted)")
    parser.add_argument("--port", type=int, default=8989, help="Port to run Web Studio or Microservice server on")
    parser.add_argument("--download-grib", action="store_true", help="Download live real GRIB2 files from NOAA NOMADS / IMD")
    parser.add_argument("--grib-dest", type=str, default="grib_data", help="Directory to save downloaded GRIB2 files")
    parser.add_argument("--full-globe", action="store_true", help="Download full uncropped planetary GRIB files (default is India crop)")
    parser.add_argument("--imd", action="store_true", help="Fetch live All-India IMD National Warning summary from official WFS GeoServer")
    parser.add_argument("--imd-district", type=str, default=None, help="Fetch official IMD Nowcast warning for specific district (e.g. 'Mumbai', 'Delhi', 'Shimla')")
    parser.add_argument("--imd-radars", action="store_true", help="List all official operational IMD Doppler Weather Radar stations")
    parser.add_argument("--satellite", action="store_true", help="List operational INSAT-3D/3DR geostationary satellite channels and live product links")
    parser.add_argument("--ensemble", action="store_true", help="Run multi-model ensemble spread & Probability of Precipitation (PoP) assessment")
    parser.add_argument("--lpi", action="store_true", help="Evaluate Lightning Potential Index (LPI) & Damini siren trigger")
    parser.add_argument("--runoff", action="store_true", help="Evaluate USDA / CWC SCS Curve Number watershed runoff & discharge")
    parser.add_argument("--transcode", type=str, default=None, help="Transcode raw GRIB2 file to compressed .mmesh file")
    parser.add_argument("--mmesh-out", type=str, default=None, help="Output path for transcoded .mmesh file (defaults to input.mmesh)")
    
    args = parser.parse_args()

    if args.about:
        print_about()
        return

    # Legacy Tkinter Desktop GUI
    if args.tk:
        try:
            from .test_mausam_mesh_gfs_live import launch_gui
        except (ImportError, ValueError):
            from test_mausam_mesh_gfs_live import launch_gui
        launch_gui()
        return

    # Modern Web Studio Browser GUI
    if args.studio:
        try:
            from .studio import launch_studio
        except (ImportError, ValueError):
            from studio import launch_studio
        print(BANNER)
        print("🚀 Launching MausamMesh Meteorological Web Studio...")
        launch_studio(port=args.port, open_browser=True)
        return

    # Headless Zero-Dependency HTTP Microservice Server
    if args.serve:
        try:
            from .auto import serve
        except (ImportError, ValueError):
            from auto import serve
        micro_port = args.port if args.port != 8989 else 8080
        serve(port=micro_port)
        return

    # Headless Multi-Point Regional Grid Scan
    if args.scan:
        import json
        try:
            from .auto import auto_scan
        except (ImportError, ValueError):
            from auto import auto_scan
        verdicts = auto_scan(
            location=args.location,
            lat=args.lat,
            lon=args.lon,
        )
        if args.json:
            print(json.dumps([v.to_dict() for v in verdicts], indent=2))
        else:
            print("================================================================================")
            print("⚡ MAUSAMMESH AUTONOMOUS REGIONAL RISK MATRIX (ZERO-GUI)")
            print("================================================================================")
            for v in verdicts:
                print(f"[{v.alert_level:16s}] {v.location_tag:32s} | CAPE: {v.sbcape_j_kg:6.1f} J/kg | Shear: {v.bulk_shear_0_6km_m_s:4.1f} m/s | Mode: {v.storm_mode}")
        return

    # Headless Continuous Daemon Mode
    if args.daemon:
        try:
            from .sync_worker import MeshSyncWorker
        except (ImportError, ValueError):
            from sync_worker import MeshSyncWorker
        print("[MausamMesh] Starting Headless 3-Hourly Ingestion Daemon...")
        worker = MeshSyncWorker()
        worker.run_daemon(interval_seconds=10800)
        return

    # Real GRIB2 Telemetry Bulk Downloader
    if args.download_grib:
        try:
            from .grib_downloader import download_latest_operational_gfs
        except (ImportError, ValueError):
            from grib_downloader import download_latest_operational_gfs
        print(BANNER)
        print(f"🛰️ Ingesting real WMO GRIB2 telemetry files into '{args.grib_dest}'...")
        download_latest_operational_gfs(
            dest_dir=args.grib_dest,
            india_crop=not args.full_globe
        )
        return

    # IMD Live National Warning Summary
    if args.imd:
        try:
            from .imd import fetch_imd_national_summary
        except (ImportError, ValueError):
            from imd import fetch_imd_national_summary
        print(BANNER)
        summary = fetch_imd_national_summary()
        print("🇮🇳 INDIA METEOROLOGICAL DEPARTMENT (IMD) — SOVEREIGN NATIONAL SUMMARY")
        print(f" Total Districts Tracked : {summary['total_districts_tracked']}")
        print(f" Active Warning Districts: {summary['active_warning_districts']}")
        print(f" Data Source             : {summary['data_source']}")
        print(f" Pipeline Status         : {summary['status']}")
        return

    # IMD District-Wise Nowcast
    if args.imd_district:
        try:
            from .imd import fetch_imd_nowcast
        except (ImportError, ValueError):
            from imd import fetch_imd_nowcast
        print(BANNER)
        nowcast = fetch_imd_nowcast(args.imd_district)
        print(f"🇮🇳 IMD OFFICIAL NOWCAST: {nowcast['district']}")
        print(f" Date / Time of Issue : {nowcast.get('date')} {nowcast.get('time_of_issue', '')} | Valid Upto: {nowcast.get('valid_upto')} hrs")
        print(f" Severity Level       : {nowcast.get('severity_level')} (Color Code: {nowcast.get('color_code')})")
        print(f" Siren Trigger        : {'🚨 YES (CRITICAL HAZARD)' if nowcast.get('siren_trigger') else '🟢 NO (SAFE)'}")
        print(f" Max Rain Rate        : {nowcast.get('max_rain_rate_mm_hr', 0.0)} mm/hr")
        print(f" Active Categories    :")
        for c in nowcast.get('active_categories', []):
            print(f"   • [{c.get('code')}] {c.get('en')} / {c.get('hi')}")
        if nowcast.get('custom_message'):
            print(f" IMD Special Note     : {nowcast.get('custom_message')}")
        return

    # IMD Radar Stations Network
    if args.imd_radars:
        try:
            from .imd import IMDIngestionEngine
        except (ImportError, ValueError):
            from imd import IMDIngestionEngine
        print(BANNER)
        print("🛰️ IMD OPERATIONAL DOPPLER WEATHER RADAR (DWR) NETWORK:")
        print(f"{'CODE':<6} {'STATION NAME':<28} {'BAND':<8} {'RANGE':<10} {'COORDINATES'}")
        print("-" * 75)
        for r in IMDIngestionEngine.get_radar_network():
            print(f"{r['code']:<6} {r['name']:<28} {r['band']:<8} {r['range_km']} km    ({r['lat']:.2f}N, {r['lon']:.2f}E)")
        return

    # INSAT Geostationary Satellite Ingestion
    if args.satellite:
        try:
            from .satellite import INSAT_CHANNELS, IMD_SATELLITE_CATALOG
        except (ImportError, ValueError):
            from satellite import INSAT_CHANNELS, IMD_SATELLITE_CATALOG
        print(BANNER)
        print("🛰️ ISRO / IMD INSAT-3D & INSAT-3DR GEOSTATIONARY SATELLITE ENGINE:")
        print(f"{'CHANNEL':<8} {'WAVELENGTH':<16} {'RESOLUTION':<16} {'SPECTRUM / APPLICATION'}")
        print("-" * 75)
        for ch, meta in INSAT_CHANNELS.items():
            print(f"{ch:<8} {meta['wavelength_um']} µm{'':<10} {meta['resolution_km']} km{'':<11} Wavenumber: {meta['wavenumber_cm']} cm⁻¹")
        print("\n📡 OFFICIAL IMD SATELLITE SECTOR ENDPOINTS:")
        for name, url in IMD_SATELLITE_CATALOG.items():
            print(f"  • {name:<26}: {url}")
        return

    # Multi-Model Ensemble Spread & PoP Evaluation
    if args.ensemble:
        try:
            from .ensemble import evaluate_ensemble_risk
        except (ImportError, ValueError):
            from ensemble import evaluate_ensemble_risk
        print(BANNER)
        # Sample 11-member ensemble representing IMD NEPS
        sample_members = [15.0, 28.0, 82.0, 95.0, 110.0, 20.0, 72.0, 68.0, 45.0, 8.0, 135.0]
        ens = evaluate_ensemble_risk(sample_members, variable_name="APCP")
        print(f"⚡ MULTI-MEMBER ENSEMBLE SPREAD SYNTHESIS ({ens.member_count} Members):")
        print(f"  • Expected Rainfall Mean  : {ens.mean_val} mm (Spread σ: ±{ens.spread_std} mm)")
        print(f"  • Member Min / Max Range   : {ens.min_val} mm to {ens.max_val} mm")
        print(f"  • P10 / Median / P90       : {ens.p10} mm / {ens.median_p50} mm / {ens.p90} mm")
        print(f"  • PoP (>= 2.5mm Light)     : {ens.pop_light_pct}%")
        print(f"  • PoP (>= 64.5mm Heavy)    : {ens.pop_heavy_pct}% (IMD Yellow Alert Threshold)")
        print(f"  • PoP (>= 115.6mm V.Heavy) : {ens.pop_very_heavy_pct}% (IMD Orange Alert Threshold)")
        print(f"  • Model Confidence Score   : {ens.forecast_confidence_pct}%")
        print(f"  • Warning Verdict          : {ens.imd_alert_level}")
        print(f"  • Action Directive         : {ens.risk_directive}")
        return

    # Lightning Potential Index (LPI) & Damini Siren Evaluation
    if args.lpi:
        try:
            from .severe import lightning_potential_index
            from .auto import auto
        except (ImportError, ValueError):
            from severe import lightning_potential_index
            from auto import auto
        print(BANNER)
        v = auto(location=args.location, lat=args.lat, lon=args.lon)
        lpi_res = lightning_potential_index(
            sbcape_j_kg=v.sbcape_j_kg,
            pwat_mm=v.precipitable_water_mm,
            bulk_shear_0_6km_m_s=v.bulk_shear_0_6km_m_s,
        )
        print(f"⚡ LIGHTNING POTENTIAL INDEX (LPI) & DAMINI SIREN: {v.location_tag}")
        print(f"  • LPI Diagnostic Score     : {lpi_res.lpi_j_kg:.2f} J/kg")
        print(f"  • Flash Density Rate       : {lpi_res.flash_density_per_km2_hr:.2f} flashes/km²/hr")
        print(f"  • Updraft Vertical Speed   : {lpi_res.updraft_speed_w_m_s:.2f} m/s")
        print(f"  • Damini Warning Level     : {lpi_res.damini_warning_level}")
        print(f"  • 800Hz Siren Activation   : {'🚨 TRIGGERED (CRITICAL THREAT)' if lpi_res.siren_triggered else '🟢 SAFE'}")
        print(f"  • Safety Directive         : {lpi_res.directive}")
        return

    # USDA / CWC SCS Curve Number Watershed Runoff
    if args.runoff:
        try:
            from .threat_solver import calculate_scs_curve_number_runoff
            from .auto import auto
        except (ImportError, ValueError):
            from threat_solver import calculate_scs_curve_number_runoff
            from auto import auto
        print(BANNER)
        v = auto(location=args.location, lat=args.lat, lon=args.lon)
        rain_val = max(15.0, v.rain_rate_mm_hr * 3.0)
        q_res = calculate_scs_curve_number_runoff(
            rainfall_depth_mm=rain_val,
            curve_number=78.0,
            catchment_area_km2=10.0,
            storm_duration_hr=3.0,
        )
        print(f"🌊 CWC / USDA WATERSHED SCS-CN RUNOFF EVALUATION: {v.location_tag}")
        print(f"  • Rainfall Storm Depth (P) : {q_res.rainfall_depth_p_mm:.1f} mm (Duration: {q_res.storm_duration_hr:.1f} hr)")
        print(f"  • Soil Potential Storage(S): {q_res.retention_s_mm:.1f} mm (CN: {q_res.curve_number:.0f}, {q_res.antecedent_moisture_condition})")
        print(f"  • Initial Abstraction (Ia) : {q_res.initial_abstraction_ia_mm:.1f} mm")
        print(f"  • Direct Runoff Depth (Pe) : {q_res.runoff_depth_pe_mm:.2f} mm")
        print(f"  • Total Runoff Volume      : {q_res.runoff_volume_m3:,.0f} m³")
        print(f"  • Peak Flood Discharge (Qp): {q_res.peak_discharge_m3_s:.2f} m³/s")
        print(f"  • CWC Inundation Hazard    : {q_res.hazard_level}")
        return

    # GRIB2 to .mmesh Transcoder
    if args.transcode:
        try:
            from .transcoder import convert_grib2_to_mmesh
        except (ImportError, ValueError):
            from transcoder import convert_grib2_to_mmesh
        print(BANNER)
        src_path = args.transcode
        out_path = args.mmesh_out or (os.path.splitext(src_path)[0] + ".mmesh")
        print(f"🔄 Transcoding WMO GRIB2 '{src_path}' -> '{out_path}'...")
        res = convert_grib2_to_mmesh(src_path, out_path)
        print(f"[SUCCESS] Transcoded {res['layers_transcoded']} layers!")
        print(f"  • Original GRIB2 : {res['original_grib_bytes'] / (1024*1024):.2f} MB")
        print(f"  • Quantized .mmesh: {res['mmesh_bytes'] / (1024*1024):.2f} MB")
        print(f"  • Payload Saving : {res['payload_reduction_pct']}% reduction")
        return

    # Headless One-Line Autonomous Pipeline (Zero-input auto-detection or Custom Location)
    if args.auto or args.json or args.observe_temp is not None or args.location is not None:
        try:
            from .auto import auto
        except (ImportError, ValueError):
            from auto import auto
        verdict = auto(
            location=args.location,
            lat=args.lat,
            lon=args.lon,
            observed_temp_c=args.observe_temp
        )
        if args.json:
            print(verdict.to_json())
        else:
            print(f"[MAUSAMMESH AUTONOMOUS VERDICT] Location: {verdict.location_tag} (Lat: {verdict.latitude:.4f} N, Lon: {verdict.longitude:.4f} E)")
            print(f" Calibrated Temp : {verdict.calibrated_temp_c:.2f} C (Learned Bias: {verdict.learned_bias_delta_c:+0.2f} C)")
            print(f" Surface CAPE    : {verdict.sbcape_j_kg:.1f} J/kg | CIN: {verdict.sbcin_j_kg:.1f} J/kg")
            print(f" 0-6km Wind Shear: {verdict.bulk_shear_0_6km_m_s:.1f} m/s | 0-3km Helicity: {verdict.storm_relative_helicity_0_3km:.1f} m^2/s^2")
            print(f" Damini Siren    : {'🚨 TRIGGERED (CRITICAL LIGHTNING THREAT)' if verdict.damini_siren_active else '🟢 SAFE'} (LPI: {verdict.lightning_potential_index:.2f} J/kg, Flash Density: {verdict.lightning_flash_density_per_km2_hr:.2f}/km²/h)")
            print(f" Watershed Runoff: Pe: {verdict.watershed_runoff_depth_pe_mm:.2f} mm | Total Volume: {verdict.watershed_runoff_volume_m3:,.0f} m³")
            print(f" IMD Nowcast     : [{verdict.imd_severity_level}] {verdict.imd_active_category}")
            print(f" Storm Mode      : {verdict.storm_mode}")
            print(f" Alert Level     : {verdict.alert_level}")
            print(f" Action Directive: {verdict.actionable_directive}")
            print(f" Latency         : {verdict.pipeline_latency_ms:.2f} ms | RAM: {verdict.memory_footprint_mb} MB")
        return

    # If lat/lon passed without --json
    if args.lat is not None and args.lon is not None:
        try:
            from .auto import auto
        except (ImportError, ValueError):
            from auto import auto
        verdict = auto(lat=args.lat, lon=args.lon, observed_temp_c=args.observe_temp)
        print(f"Query Coordinates : Lat {args.lat} N, Lon {args.lon} E")
        print(f"Calibrated Temp   : {verdict.calibrated_temp_c} C (Bias: {verdict.learned_bias_delta_c:+0.2f} C)")
        print(f"Relative Humidity : {verdict.relative_humidity_pct} % | Wet-Bulb: {verdict.wet_bulb_temp_c} C")
        print(f"Surface CAPE      : {verdict.sbcape_j_kg} J/kg | Shear: {verdict.bulk_shear_0_6km_m_s} m/s")
        print(f"Hazard Alert      : {verdict.alert_level} ({verdict.storm_mode})")
        print(f"Action Directive  : {verdict.actionable_directive}")
        print(f"Pipeline Latency  : {verdict.pipeline_latency_ms} ms")
        return

    # If --cli explicitly requested
    if args.cli:
        print(BANNER)
        try:
            from .auto import auto
        except (ImportError, ValueError):
            from auto import auto
        verdict = auto(location=args.location, lat=args.lat, lon=args.lon)
        print(f"[MAUSAMMESH VERDICT] Location: {verdict.location_tag}")
        print(f" Calibrated Temp : {verdict.calibrated_temp_c:.2f} °C (Bias: {verdict.learned_bias_delta_c:+0.2f} °C)")
        print(f" Surface CAPE    : {verdict.sbcape_j_kg:.1f} J/kg | CIN: {verdict.sbcin_j_kg:.1f} J/kg")
        print(f" 0-6km Wind Shear: {verdict.bulk_shear_0_6km_m_s:.1f} m/s | 0-3km Helicity: {verdict.storm_relative_helicity_0_3km:.1f} m^2/s^2")
        print(f" Storm Mode      : {verdict.storm_mode}")
        print(f" Alert Level     : {verdict.alert_level}")
        print(f" Action Directive: {verdict.actionable_directive}")
        print(f" Latency         : {verdict.pipeline_latency_ms:.2f} ms | RAM: {verdict.memory_footprint_mb} MB")
        return

    # Default action: Launch the Modern Web Studio or print summary!
    try:
        from .studio import launch_studio
        print(BANNER)
        print("🚀 Launching MausamMesh Meteorological Web Studio...")
        launch_studio(port=args.port, open_browser=True)
    except Exception as e:
        print(BANNER)
        print(f"Notice: Web Studio not available ({e}). Running autonomous CLI engine:\n")
        try:
            from .auto import auto
        except (ImportError, ValueError):
            from auto import auto
        verdict = auto(location=args.location, lat=args.lat, lon=args.lon)
        print(f"[MAUSAMMESH VERDICT] Location: {verdict.location_tag}")
        print(f" Calibrated Temp : {verdict.calibrated_temp_c:.2f} °C")
        print(f" Surface CAPE    : {verdict.sbcape_j_kg:.1f} J/kg | Shear: {verdict.bulk_shear_0_6km_m_s:.1f} m/s")
        print(f" Alert Level     : {verdict.alert_level} ({verdict.storm_mode})")
        print(f" Action Directive: {verdict.actionable_directive}")
        return

if __name__ == "__main__":
    main()
