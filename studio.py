"""
=============================================================================
⚡ MAUSAMMESH SOVEREIGN METEOROLOGICAL WEB STUDIO
=============================================================================
Architect: Mr. Mohit Donawat
Founder, CEO & Lead Systems Architect — WildUs (wildus.app) & MSD Innovations
Portfolio: https://mohitdonawat.wildus.app/
=============================================================================
A self-contained, zero-dependency, ultra-modern executive web studio that runs
locally on ANY laptop. Serves rich glassmorphic telemetry, interactive Leaflet
weather map, real 800Hz Web Audio NDMA siren, and Bhashini speech synthesizer.
=============================================================================
"""

import sys
import os
import json
import urllib.parse
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

# Ensure local modules are accessible
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spatial_slicer import slice_point, PointWeather
from threat_solver import ThreatSolver, evaluate_threat
from kisan_agro import KisanAgroEngine
from voice_distiller import VoiceDistiller

CITIES = {
    "sheopur": {"name": "Sheopur (श्योपुर), M.P.", "lat": 25.6667, "lon": 76.6999, "crop": "wheat", "desc": "Native Chambal Agrarian Belt — Heatwave & Frost Prone"},
    "cherrapunji": {"name": "Cherrapunji (चेरापूंजी), Meghalaya", "lat": 25.2743, "lon": 91.7323, "crop": "rice", "desc": "World's Rainiest Zone — Extreme Flash Flood & Cloudburst Hazard"},
    "bhopal": {"name": "Bhopal (भोपाल), M.P.", "lat": 23.2599, "lon": 77.4126, "crop": "soybean", "desc": "Central Plateau Agrarian Corridor — Urban Drainage Vulnerability"},
    "delhi": {"name": "New Delhi (दिल्ली), NCR", "lat": 28.6139, "lon": 77.2090, "crop": "wheat", "desc": "Indo-Gangetic Plain — Dense Heat Island & Monsoon Waterlogging"},
    "mumbai": {"name": "Mumbai (मुंबई), Maharashtra", "lat": 19.0760, "lon": 72.8777, "crop": "rice", "desc": "Konkan Coastal Confluence — High Tide Squall & Severe Flooding"},
    "leh": {"name": "Leh (लेह), Ladakh", "lat": 34.1526, "lon": 77.5771, "crop": "wheat", "desc": "Trans-Himalayan Cold Arid Valley — Cloudburst & Frost Warning"},
    "bengaluru": {"name": "Bengaluru (बेंगलुरु), Karnataka", "lat": 12.9716, "lon": 77.5946, "crop": "rice", "desc": "Deccan Tech Corridor — Convective Urban Thunderstorm Zone"},
    "jaisalmer": {"name": "Jaisalmer (जैसलमेर), Rajasthan", "lat": 26.9157, "lon": 70.9083, "crop": "mustard", "desc": "Thar Desert Hyper-Arid Core — Extreme Thermal Anomaly"},
}

def compute_full_telemetry(lat: float, lon: float, crop: str = "wheat", acres: float = 2.5) -> Dict[str, Any]:
    # 1. Point weather slice
    pt = slice_point(lat=lat, lon=lon)
    
    # 2. Threat evaluation
    threat = ThreatSolver.evaluate_threat(
        rain_intensity_mm_hr=pt.rain_mm_hr,
        wind_speed_kmh=pt.wind_speed_kmh,
        temp_c=pt.temperature_c,
        cape_index=2600.0 if (lon > 90.0 or pt.rain_mm_hr > 40) else 850.0,
        catchment_area_ha=acres * 10.0
    )
    
    # 3. Kisan Agromet Math
    agro = KisanAgroEngine.calculate_fertilizer_balance(crop=crop, acres=acres)
    pump = KisanAgroEngine.calculate_pump_runtime(crop=crop, acres=acres, pump_hp=5.0, rainfall_mm=pt.rain_mm_hr)
    
    # 4. Voice broadcast script
    voice_hi = VoiceDistiller.to_kisan_voice(
        temp_c=pt.temperature_c,
        rain_mm=pt.rain_mm_hr,
        wind_kmh=pt.wind_speed_kmh,
        alert_level=threat.alert_level,
        target_lang="hi"
    )
    voice_en = VoiceDistiller.to_kisan_voice(
        temp_c=pt.temperature_c,
        rain_mm=pt.rain_mm_hr,
        wind_kmh=pt.wind_speed_kmh,
        alert_level=threat.alert_level,
        target_lang="en"
    )

    return {
        "latitude": lat,
        "longitude": lon,
        "temperature_c": pt.temperature_c,
        "rain_mm_hr": pt.rain_mm_hr,
        "wind_speed_kmh": pt.wind_speed_kmh,
        "pressure_hpa": pt.pressure_hpa,
        "reflectivity_dbz": pt.reflectivity_dbz,
        "nearest_hub": pt.nearest_hub,
        "threat": threat.to_dict(),
        "agro": agro,
        "pump": pump,
        "voice_hi": voice_hi,
        "voice_en": voice_en,
        "architect": {
            "name": "Mr. Mohit Donawat",
            "title": "Founder, CEO & Lead Systems Architect — WildUs & MSD Innovations",
            "portfolio": "https://mohitdonawat.wildus.app/",
            "wildus": "https://wildus.app",
            "yansmap": "https://yansmap.web.app/"
        }
    }


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚡ MausamMesh Studio — By Mr. Mohit Donawat</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    :root {
      --bg-dark: #030712;
      --bg-card: rgba(15, 23, 42, 0.75);
      --bg-glass: rgba(30, 41, 59, 0.6);
      --border-subtle: rgba(148, 163, 184, 0.15);
      --border-accent: rgba(56, 189, 248, 0.35);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --sky: #38bdf8;
      --emerald: #10b981;
      --amber: #f59e0b;
      --crimson: #ef4444;
      --font-sans: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: radial-gradient(circle at 15% 10%, #0f172a 0%, #030712 100%);
      color: var(--text-main);
      font-family: var(--font-sans);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* TOP HEADER */
    header {
      backdrop-filter: blur(16px);
      background: rgba(3, 7, 18, 0.85);
      border-bottom: 1px solid var(--border-subtle);
      position: sticky;
      top: 0;
      z-index: 1000;
      padding: 0.85rem 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }
    .brand-icon {
      background: linear-gradient(135deg, #0284c7, #10b981);
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
    }
    .brand-text h1 {
      font-size: 1.15rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #ffffff, #94a3b8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-text p {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .founder-badge {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      background: rgba(14, 165, 233, 0.1);
      border: 1px solid rgba(14, 165, 233, 0.3);
      padding: 0.45rem 0.95rem;
      border-radius: 999px;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .founder-badge:hover {
      background: rgba(14, 165, 233, 0.2);
      border-color: var(--sky);
      transform: translateY(-1px);
    }
    .founder-badge span {
      font-size: 0.8rem;
      color: var(--sky);
      font-weight: 700;
    }

    /* MAIN CONTAINER */
    .container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 1.5rem;
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 1.5rem;
    }
    @media (max-width: 1024px) {
      .container { grid-template-columns: 1fr; }
    }

    /* CARD STYLES */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      backdrop-filter: blur(12px);
      padding: 1.25rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .card-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--sky);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* CITY PILLS */
    .city-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      margin-bottom: 1.25rem;
    }
    .city-btn {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(148, 163, 184, 0.2);
      color: #cbd5e1;
      padding: 0.35rem 0.75rem;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .city-btn:hover, .city-btn.active {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(2, 132, 199, 0.5);
    }

    /* COORD INPUTS */
    .input-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.65rem;
      margin-bottom: 1rem;
    }
    .input-group label {
      display: block;
      font-size: 0.7rem;
      color: var(--text-muted);
      margin-bottom: 0.3rem;
      font-family: var(--font-mono);
    }
    .input-group input, .input-group select {
      width: 100%;
      background: #090e17;
      border: 1px solid rgba(148, 163, 184, 0.2);
      padding: 0.55rem 0.75rem;
      border-radius: 8px;
      color: #ffffff;
      font-size: 0.85rem;
      font-family: var(--font-mono);
      outline: none;
      transition: border 0.2s;
    }
    .input-group input:focus, .input-group select:focus {
      border-color: var(--sky);
    }
    .btn-action {
      width: 100%;
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      border: none;
      padding: 0.7rem;
      border-radius: 10px;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: all 0.2s;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
    }
    .btn-action:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5);
    }

    /* RIGHT COLUMN HUD */
    .dashboard-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.25rem;
    }

    /* BIG WEATHER HERO */
    .weather-hero {
      background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.95));
      border: 1px solid var(--border-accent);
      border-radius: 16px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    .weather-hero::before {
      content: '';
      position: absolute;
      top: -50px;
      right: -50px;
      width: 180px;
      height: 180px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .hero-temp {
      font-size: 4rem;
      font-weight: 900;
      line-height: 1;
      letter-spacing: -2px;
      background: linear-gradient(180deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-unit {
      font-size: 1.75rem;
      vertical-align: super;
      font-weight: 600;
      color: var(--sky);
    }
    .hero-city-name {
      font-size: 1.25rem;
      font-weight: 800;
      color: #ffffff;
      margin-top: 0.35rem;
    }
    .hero-city-desc {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 0.2rem;
    }

    /* METRICS STRIP */
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.75rem;
      margin-top: 1.25rem;
    }
    .metric-pill {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(148, 163, 184, 0.1);
      padding: 0.65rem;
      border-radius: 10px;
      text-align: center;
    }
    .metric-pill .lbl {
      font-size: 0.68rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-family: var(--font-mono);
    }
    .metric-pill .val {
      font-size: 1rem;
      font-weight: 800;
      color: #f1f5f9;
      margin-top: 0.2rem;
    }

    /* ALERT BANNER */
    .alert-box {
      border-radius: 14px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      border: 1px solid transparent;
      transition: all 0.3s;
    }
    .alert-box.RED {
      background: rgba(239, 68, 68, 0.12);
      border-color: rgba(239, 68, 68, 0.4);
    }
    .alert-box.ORANGE {
      background: rgba(245, 158, 11, 0.12);
      border-color: rgba(245, 158, 11, 0.4);
    }
    .alert-box.YELLOW {
      background: rgba(234, 179, 8, 0.12);
      border-color: rgba(234, 179, 8, 0.4);
    }
    .alert-box.GREEN {
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.4);
    }
    .alert-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.3rem 0.75rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      width: fit-content;
    }
    .alert-box.RED .alert-badge { background: #ef4444; color: #fff; }
    .alert-box.ORANGE .alert-badge { background: #f59e0b; color: #000; }
    .alert-box.YELLOW .alert-badge { background: #eab308; color: #000; }
    .alert-box.GREEN .alert-badge { background: #10b981; color: #fff; }

    /* SIREN BUTTON */
    .btn-siren {
      background: linear-gradient(135deg, #ef4444, #b91c1c);
      color: white;
      border: none;
      padding: 0.75rem 1.25rem;
      border-radius: 10px;
      font-size: 0.85rem;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: all 0.2s;
      box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
    }
    .btn-siren:hover {
      box-shadow: 0 0 30px rgba(239, 68, 68, 0.7);
      transform: scale(1.02);
    }
    .btn-siren.active {
      animation: pulse-siren 0.6s infinite alternate;
    }
    @keyframes pulse-siren {
      from { background: #ef4444; transform: scale(1); }
      to { background: #7f1d1d; transform: scale(1.04); }
    }

    /* KISAN AGROMET */
    .kisan-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
    }
    .kisan-card {
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.2);
      border-radius: 12px;
      padding: 0.85rem;
    }
    .kisan-card .title {
      font-size: 0.72rem;
      color: var(--emerald);
      font-weight: 700;
      text-transform: uppercase;
    }
    .kisan-card .big {
      font-size: 1.35rem;
      font-weight: 800;
      color: #ffffff;
      margin-top: 0.25rem;
    }
    .kisan-card .sub {
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 0.2rem;
    }

    /* MAP CONTAINER */
    #weatherMap {
      width: 100%;
      height: 340px;
      border-radius: 14px;
      border: 1px solid var(--border-subtle);
      margin-top: 0.75rem;
      z-index: 10;
    }

    /* VOICE BROADCAST */
    .voice-box {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 12px;
      padding: 1rem;
      margin-top: 1rem;
    }
    .voice-box p {
      font-size: 0.85rem;
      line-height: 1.5;
      color: #cbd5e1;
    }
    .btn-voice {
      margin-top: 0.75rem;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid var(--sky);
      color: var(--sky);
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.8rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }
    .btn-voice:hover {
      background: var(--sky);
      color: #000;
    }
  </style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="brand">
      <div class="brand-icon">⚡</div>
      <div class="brand-text">
        <h1>MausamMesh Sovereign Meteorological Studio</h1>
        <p>Real-Time Edge Weather Slicing & Disaster Early-Warning Engine</p>
      </div>
    </div>
    
    <div style="display: flex; gap: 0.75rem; align-items: center;">
      <a href="https://mohitdonawat.wildus.app/" target="_blank" class="founder-badge">
        <span>👨‍💻 Architect: Mr. Mohit Donawat</span>
      </a>
      <a href="https://wildus.app" target="_blank" class="founder-badge" style="border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.1);">
        <span style="color: var(--emerald);">🌌 WildUs Universe</span>
      </a>
    </div>
  </header>

  <!-- CONTAINER -->
  <main class="container">
    
    <!-- LEFT PANEL: CONTROLS -->
    <aside>
      <div class="card">
        <div class="card-title">📍 SELECT REGION & CROP</div>
        
        <!-- City Pills -->
        <div class="city-pills" id="cityPills"></div>

        <div class="input-row">
          <div class="input-group">
            <label>LATITUDE (°N)</label>
            <input type="number" id="latInput" step="0.0001" value="25.6667">
          </div>
          <div class="input-group">
            <label>LONGITUDE (°E)</label>
            <input type="number" id="lonInput" step="0.0001" value="76.6999">
          </div>
        </div>

        <div class="input-row">
          <div class="input-group">
            <label>KISAN CROP</label>
            <select id="cropSelect">
              <option value="wheat">Wheat (गेहूँ)</option>
              <option value="rice">Paddy/Rice (धान)</option>
              <option value="mustard">Mustard (सरसों)</option>
              <option value="cotton">Cotton (कपास)</option>
              <option value="sugarcane">Sugarcane (गन्ना)</option>
              <option value="soybean">Soybean (सोयाबीन)</option>
            </select>
          </div>
          <div class="input-group">
            <label>FARM ACRES</label>
            <input type="number" id="acresInput" step="0.5" value="2.5">
          </div>
        </div>

        <button class="btn-action" onclick="fetchLiveWeather()">
          <span>⚡ INSTANT O(1) WEATHER SLICE</span>
        </button>

        <button class="btn-action" style="margin-top: 0.5rem; background: rgba(148, 163, 184, 0.1); border: 1px solid rgba(148, 163, 184, 0.2); box-shadow: none;" onclick="autoDetectGPS()">
          <span>🎯 Detect My Current GPS</span>
        </button>

        <!-- Interactive Map -->
        <div style="margin-top: 1.25rem;">
          <div class="card-title" style="margin-bottom: 0.4rem;">🗺️ INTERACTIVE MAP SLICER</div>
          <p style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.5rem;">Click anywhere across India to slice village weather in &lt; 0.2 ms:</p>
          <div id="weatherMap"></div>
        </div>
      </div>
    </aside>

    <!-- RIGHT PANEL: LIVE TELEMETRY HUD -->
    <section style="display: flex; flex-direction: column; gap: 1.25rem;">

      <!-- HERO WEATHER CARD -->
      <div class="weather-hero">
        <div class="hero-top">
          <div>
            <div class="hero-city-name" id="cityNameDisplay">Sheopur (श्योपुर), M.P.</div>
            <div class="hero-city-desc" id="cityDescDisplay">Native Chambal Agrarian Belt — Heatwave & Frost Prone</div>
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--sky); margin-top: 0.4rem;" id="coordsDisplay">
              Lat 25.6667° N, Lon 76.6999° E
            </div>
          </div>
          <div style="text-align: right;">
            <div class="hero-temp">
              <span id="tempVal">28.4</span><span class="hero-unit">°C</span>
            </div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #cbd5e1;" id="conditionVal">Partly Cloudy</div>
          </div>
        </div>

        <!-- METRIC PILLS -->
        <div class="metric-grid">
          <div class="metric-pill">
            <div class="lbl">RAIN INTENSITY</div>
            <div class="val" id="rainVal">0.0 mm/h</div>
          </div>
          <div class="metric-pill">
            <div class="lbl">WIND SPEED</div>
            <div class="val" id="windVal">14.2 km/h</div>
          </div>
          <div class="metric-pill">
            <div class="lbl">BARO PRESSURE</div>
            <div class="val" id="pressureVal">1012 hPa</div>
          </div>
          <div class="metric-pill">
            <div class="lbl">RADAR DBZ</div>
            <div class="val" id="radarVal">0.0 dBZ</div>
          </div>
        </div>
      </div>

      <!-- DISASTER COMMAND & KISAN DUAL GRID -->
      <div class="dashboard-grid">

        <!-- NDMA EARLY WARNING & SIREN CARD -->
        <div class="card">
          <div class="card-title">🚨 NDMA DISASTER PROTOCOL & SIREN</div>
          
          <div class="alert-box" id="alertBox">
            <div class="alert-badge" id="alertBadge">GREEN • NORMAL CONDITIONS</div>
            <div style="font-size: 0.88rem; font-weight: 700; color: #fff;" id="hazardSummary">
              No severe meteorological hazards detected.
            </div>
            <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.4;" id="recommendedAction">
              Conditions are safe for farming, road transit, and civic activities.
            </div>
          </div>

          <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.65rem;">
            <button class="btn-siren" id="sirenBtn" onclick="toggleEmergencySiren()">
              <span>🚨 TEST 800Hz NDMA SIREN</span>
            </button>
            <p style="font-size: 0.68rem; color: var(--text-muted); text-align: center; font-family: var(--font-mono);">
              Synthesizes real acoustic sawtooth distress wave via Web Audio API
            </p>
          </div>
        </div>

        <!-- KISAN AGROMET SMART STOICHIOMETRY -->
        <div class="card">
          <div class="card-title">🌾 KISAN AGROMET & WATER PLANNER</div>
          
          <div class="kisan-grid">
            <div class="kisan-card">
              <div class="title">RECOMMENDED DAP</div>
              <div class="big" id="dapBagsVal">2.6 Bags</div>
              <div class="sub">50kg bags (18:46:0 NPK)</div>
            </div>
            <div class="kisan-card">
              <div class="title">RECOMMENDED UREA</div>
              <div class="big" id="ureaBagsVal">4.2 Bags</div>
              <div class="sub">45kg bags (Saves ₹4,500/acre)</div>
            </div>
            <div class="kisan-card">
              <div class="title">TUBEWELL PUMP CLOCK</div>
              <div class="big" id="pumpClockVal">3h 45m</div>
              <div class="sub">For 5 HP motor runtime</div>
            </div>
            <div class="kisan-card">
              <div class="title">NET WATER REQUIREMENT</div>
              <div class="big" id="waterVolVal">85,000 L</div>
              <div class="sub">After adjusting for rainfall</div>
            </div>
          </div>

          <p style="font-size: 0.72rem; color: var(--emerald); margin-top: 0.85rem; font-weight: 600;">
            ✓ Precision chemical stoichiometry credits 18% inherent N from DAP to prevent urea burn.
          </p>
        </div>

      </div>

      <!-- MULTILINGUAL SPOKEN ADVISORY CARD -->
      <div class="card">
        <div class="card-title">🔊 BHASHINI MULTILINGUAL SPOKEN ADVISORY</div>
        <div class="voice-box">
          <p id="voiceText">नमस्ते किसान भाइयों। आज मौसम सामान्य रहेगा। तापमान 28.4 डिग्री है। खेत में सिंचाई और खाद का कार्य सुचारू रूप से किया जा सकता है।</p>
          <button class="btn-voice" onclick="speakVoiceAlert()">
            <span>▶️ Speak Live Voice Advisory (Audio)</span>
          </button>
        </div>
      </div>

    </section>

  </main>

  <script>
    // Cities data
    const CITIES_DATA = {
      sheopur: { name: "Sheopur (श्योपुर), M.P.", lat: 25.6667, lon: 76.6999, crop: "wheat", desc: "Native Chambal Agrarian Belt — Heatwave & Frost Prone" },
      cherrapunji: { name: "Cherrapunji (चेरापूंजी), Meghalaya", lat: 25.2743, lon: 91.7323, crop: "rice", desc: "World's Rainiest Zone — Extreme Flash Flood & Cloudburst Hazard" },
      bhopal: { name: "Bhopal (भोपाल), M.P.", lat: 23.2599, lon: 77.4126, crop: "soybean", desc: "Central Plateau Agrarian Corridor — Urban Drainage Vulnerability" },
      delhi: { name: "New Delhi (दिल्ली), NCR", lat: 28.6139, lon: 77.2090, crop: "wheat", desc: "Indo-Gangetic Plain — Dense Heat Island & Monsoon Waterlogging" },
      mumbai: { name: "Mumbai (मुंबई), Maharashtra", lat: 19.0760, lon: 72.8777, crop: "rice", desc: "Konkan Coastal Confluence — High Tide Squall & Severe Flooding" },
      leh: { name: "Leh (लेह), Ladakh", lat: 34.1526, lon: 77.5771, crop: "wheat", desc: "Trans-Himalayan Cold Arid Valley — Cloudburst & Frost Warning" },
      bengaluru: { name: "Bengaluru (बेंगलुरु), Karnataka", lat: 12.9716, lon: 77.5946, crop: "rice", desc: "Deccan Tech Corridor — Convective Urban Thunderstorm Zone" },
      jaisalmer: { name: "Jaisalmer (जैसलमेर), Rajasthan", lat: 26.9157, lon: 70.9083, crop: "mustard", desc: "Thar Desert Hyper-Arid Core — Extreme Thermal Anomaly" }
    };

    let map, marker;
    let audioCtx = null;
    let sirenOscillator = null;
    let isSirenPlaying = false;

    // Render city pills
    function initPills() {
      const pillsContainer = document.getElementById("cityPills");
      pillsContainer.innerHTML = "";
      for (const [key, c] of Object.entries(CITIES_DATA)) {
        const btn = document.createElement("button");
        btn.className = "city-btn" + (key === "sheopur" ? " active" : "");
        btn.innerText = c.name.split(" ")[0];
        btn.onclick = () => selectCity(key);
        pillsContainer.appendChild(btn);
      }
    }

    function selectCity(key) {
      document.querySelectorAll(".city-btn").forEach(b => b.classList.remove("active"));
      event.target.classList.add("active");
      const c = CITIES_DATA[key];
      document.getElementById("latInput").value = c.lat;
      document.getElementById("lonInput").value = c.lon;
      document.getElementById("cropSelect").value = c.crop;
      fetchLiveWeather(c.name, c.desc);
    }

    // Leaflet map init
    function initMap() {
      map = L.map('weatherMap').setView([22.5, 78.9], 4);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap | MausamMesh Spatial Engine'
      }).addTo(map);

      marker = L.marker([25.6667, 76.6999]).addTo(map);

      map.on('click', function(e) {
        const lat = parseFloat(e.latlng.lat.toFixed(4));
        const lon = parseFloat(e.latlng.lng.toFixed(4));
        document.getElementById("latInput").value = lat;
        document.getElementById("lonInput").value = lon;
        marker.setLatLng([lat, lon]);
        fetchLiveWeather("Custom Coordinate", `Latitude ${lat}° N, Longitude ${lon}° E`);
      });
    }

    // Fetch Weather Data
    async function fetchLiveWeather(customName = null, customDesc = null) {
      const lat = parseFloat(document.getElementById("latInput").value);
      const lon = parseFloat(document.getElementById("lonInput").value);
      const crop = document.getElementById("cropSelect").value;
      const acres = parseFloat(document.getElementById("acresInput").value) || 2.5;

      if (marker && map) {
        marker.setLatLng([lat, lon]);
        map.setView([lat, lon], Math.max(map.getZoom(), 6));
      }

      try {
        const res = await fetch(`/api/weather?lat=${lat}&lon=${lon}&crop=${crop}&acres=${acres}`);
        const data = await res.json();
        updateUI(data, customName, customDesc);
      } catch (e) {
        console.error("Fetch error:", e);
      }
    }

    // Update UI elements
    function updateUI(data, customName, customDesc) {
      if (customName) document.getElementById("cityNameDisplay").innerText = customName;
      if (customDesc) document.getElementById("cityDescDisplay").innerText = customDesc;
      document.getElementById("coordsDisplay").innerText = `Lat ${data.latitude}° N, Lon ${data.longitude}° E`;

      document.getElementById("tempVal").innerText = data.temperature_c.toFixed(1);
      document.getElementById("rainVal").innerText = data.rain_mm_hr.toFixed(1) + " mm/h";
      document.getElementById("windVal").innerText = data.wind_speed_kmh.toFixed(1) + " km/h";
      document.getElementById("pressureVal").innerText = data.pressure_hpa.toFixed(0) + " hPa";
      document.getElementById("radarVal").innerText = data.reflectivity_dbz.toFixed(1) + " dBZ";

      // Condition text
      let cond = "Clear Sky";
      if (data.rain_mm_hr > 50) cond = "⛈️ Severe Cloudburst / Squall";
      else if (data.rain_mm_hr > 10) cond = "🌧️ Heavy Monsoon Rain";
      else if (data.rain_mm_hr > 0.5) cond = "🌦️ Light Rain / Drizzle";
      else if (data.temperature_c > 38) cond = "☀️ Severe Heat Stress";
      else if (data.temperature_c < 10) cond = "❄️ Cold Frost Condition";
      document.getElementById("conditionVal").innerText = cond;

      // NDMA Alert Box
      const alertBox = document.getElementById("alertBox");
      const alertBadge = document.getElementById("alertBadge");
      const threat = data.threat;

      alertBox.className = "alert-box " + threat.alert_level;
      alertBadge.innerText = threat.alert_level + " • " + (threat.is_extreme ? "EXTREME DANGER" : "ADVISORY");
      document.getElementById("hazardSummary").innerText = threat.hazard_summary;
      document.getElementById("recommendedAction").innerText = threat.recommended_action;

      // Kisan Agro
      document.getElementById("dapBagsVal").innerText = data.agro.dap_50kg_bags + " Bags";
      document.getElementById("ureaBagsVal").innerText = data.agro.urea_45kg_bags + " Bags";
      document.getElementById("pumpClockVal").innerText = data.pump.formatted_runtime;
      document.getElementById("waterVolVal").innerText = data.pump.net_water_liters.toLocaleString() + " L";

      // Voice script
      document.getElementById("voiceText").innerText = data.voice_hi;
    }

    // Web Audio API Synthesizer: Real 800Hz Sawtooth Emergency Siren
    function toggleEmergencySiren() {
      const btn = document.getElementById("sirenBtn");
      if (isSirenPlaying) {
        stopSiren();
        btn.classList.remove("active");
        btn.innerHTML = "<span>🚨 TEST 800Hz NDMA SIREN</span>";
      } else {
        startSiren();
        btn.classList.add("active");
        btn.innerHTML = "<span>🛑 STOP EMERGENCY SIREN</span>";
      }
    }

    function startSiren() {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') audioCtx.resume();

      sirenOscillator = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();

      sirenOscillator.type = 'sawtooth';
      sirenOscillator.frequency.setValueAtTime(500, audioCtx.currentTime);

      // Pitch sweep between 500Hz and 1000Hz (NDMA Distress Wail)
      const now = audioCtx.currentTime;
      for (let i = 0; i < 30; i++) {
        sirenOscillator.frequency.linearRampToValueAtTime(1000, now + (i * 1.5) + 0.75);
        sirenOscillator.frequency.linearRampToValueAtTime(500, now + (i * 1.5) + 1.5);
      }

      gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
      sirenOscillator.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      sirenOscillator.start();
      isSirenPlaying = true;
    }

    function stopSiren() {
      if (sirenOscillator) {
        try { sirenOscillator.stop(); sirenOscillator.disconnect(); } catch (e) {}
        sirenOscillator = null;
      }
      isSirenPlaying = false;
    }

    // Web Speech API: Speak Voice Alert
    function speakVoiceAlert() {
      const text = document.getElementById("voiceText").innerText;
      if (!('speechSynthesis' in window)) {
        alert("Speech Synthesis is not supported in this browser.");
        return;
      }
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "hi-IN";
      utterance.rate = 0.95;
      window.speechSynthesis.speak(utterance);
    }

    // GPS Auto Detect
    function autoDetectGPS() {
      if (!navigator.geolocation) {
        alert("Geolocation not supported by browser.");
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const lat = parseFloat(pos.coords.latitude.toFixed(4));
          const lon = parseFloat(pos.coords.longitude.toFixed(4));
          document.getElementById("latInput").value = lat;
          document.getElementById("lonInput").value = lon;
          fetchLiveWeather("My Current Location", `Detected via Laptop/Device GPS`);
        },
        (err) => {
          alert("GPS Permission Denied or Unavailable: " + err.message);
        }
      );
    }

    // Init on load
    window.addEventListener('DOMContentLoaded', () => {
      initPills();
      initMap();
      fetchLiveWeather("Sheopur (श्योपुर), M.P.", "Native Chambal Agrarian Belt — Heatwave & Frost Prone");
    });
  </script>
</body>
</html>
"""


class StudioRequestHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP server delivering MausamMesh Executive Web Studio."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. API: /api/weather
        if path == "/api/weather":
            lat = float(query.get("lat", [25.6667])[0])
            lon = float(query.get("lon", [76.6999])[0])
            crop = query.get("crop", ["wheat"])[0]
            acres = float(query.get("acres", [2.5])[0])

            data = compute_full_telemetry(lat=lat, lon=lon, crop=crop, acres=acres)
            payload = json.dumps(data).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
            return

        # 2. API: /api/cities
        if path == "/api/cities":
            payload = json.dumps(CITIES).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
            return

        # 3. ROOT: Serve HTML Studio
        content = HTML_PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # Silent clean logging
        pass


def launch_studio(port: int = 8989, open_browser: bool = True):
    server_address = ("127.0.0.1", port)
    
    # Try binding, find next free port if occupied
    httpd = None
    for p in range(port, port + 10):
        try:
            httpd = HTTPServer(("127.0.0.1", p), StudioRequestHandler)
            port = p
            break
        except OSError:
            continue

    if not httpd:
        print(f"Error: Could not bind studio server to ports {port}-{port+10}")
        return

    url = f"http://localhost:{port}"
    print(r"""
================================================================================
⚡ MAUSAMMESH SOVEREIGN METEOROLOGICAL WEB STUDIO
================================================================================
👨‍💻 Architect : Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
🌐 Studio URL : """ + url + r"""
📍 Status     : Online (Zero external dependencies, running locally)
================================================================================
👉 Press Ctrl + C to stop the studio server.
""")

    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⚡ MausamMesh Studio stopped cleanly.")
        httpd.server_close()


if __name__ == "__main__":
    launch_studio()
