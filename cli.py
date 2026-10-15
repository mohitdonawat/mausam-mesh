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
    parser.add_argument("--gui", action="store_true", help="Launch the high-tech Tkinter Desktop GUI Studio")
    parser.add_argument("--cli", action="store_true", help="Run the All-India multi-location extraction benchmark")
    parser.add_argument("--about", action="store_true", help="Display author credentials and project architecture info")
    parser.add_argument("--lat", type=float, help="Latitude for instant weather slice")
    parser.add_argument("--lon", type=float, help="Longitude for instant weather slice")
    
    args = parser.parse_args()

    if args.about:
        print_about()
        return

    # If lat/lon passed
    if args.lat is not None and args.lon is not None:
        print(BANNER)
        from .spatial_slicer import slice_point
        from .threat_solver import evaluate_threat
        
        pt = slice_point(lat=args.lat, lon=args.lon)
        threat = evaluate_threat(rain_intensity_mm_hr=pt.rain_mm_hr, temp_c=pt.temperature_c)
        print(f"📍 Query Coordinates : Lat {args.lat}° N, Lon {args.lon}° E")
        print(f"🌡️ Temperature       : {pt.temperature_c} °C")
        print(f"🌧️ Rain Rate         : {pt.rain_mm_hr} mm/hr")
        print(f"💨 Wind Speed        : {pt.wind_kmh} km/h")
        print(f"🚨 Hazard Alert      : {threat.alert_level} ({threat.hazard_summary})")
        print(f"📢 Siren Protocol    : {threat.siren_protocol.get('tone', 'NORMAL')}")
        return

    # If --gui or no arguments on desktop, try launching GUI, otherwise CLI
    if args.gui or (not args.cli and len(sys.argv) == 1):
        try:
            from .test_mausam_mesh_gfs_live import launch_gui
            print(BANNER)
            print("🚀 Launching MausamMesh Desktop Studio GUI...")
            launch_gui()
            return
        except Exception as e:
            print(BANNER)
            print(f"Notice: GUI could not be launched directly ({e}). Falling back to CLI mode.\n")
            from .test_mausam_mesh_gfs_live import run_cli_all
            run_cli_all()
            return

    # Default CLI mode
    print(BANNER)
    from .test_mausam_mesh_gfs_live import run_cli_all
    run_cli_all()

if __name__ == "__main__":
    main()
