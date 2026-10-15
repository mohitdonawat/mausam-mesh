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
⚡ MAUSAMMESH (मौसम मेश) — SOVEREIGN METEOROLOGICAL EDGE ENGINE v1.0.0
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
Mr. Mohit Donawat as the sovereign edge meteorological compression and spatial
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
        description="MausamMesh — Sovereign Edge Meteorological Compression & Spatial Slicing Engine"
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
    
    args = parser.parse_args()

    if args.about:
        print_about()
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
