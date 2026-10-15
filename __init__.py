"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — THE SOVEREIGN METEOROLOGICAL EDGE ENGINE
=============================================================================
Open-Source Global Python/Edge Library for:
1. 95% Atmospheric Matrix Quantization (Float32 -> Int8 Mesh)
2. O(1) Bilinear Coordinate Point Slicing in < 0.2ms
3. Convective Instability & Rational Flood Runoff (Q = CIA/360)
4. Kisan Agromet Stoichiometric NPK & FAO-56 Tubewell Pump Math
5. Multilingual 22-Language Spoken Voice Distillation (Bhashini-Aligned)
=============================================================================
MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
=============================================================================
"""

__version__ = "1.0.3"
__author__ = "Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)"
__portfolio__ = "https://mohitdonawat.wildus.app/"
__license__ = "MIT"

from .quantizer import (
    AtmosphericQuantizer, 
    quantize_grid, 
    dequantize_grid,
    quantize_log,
    dequantize_log,
    quantize_precipitation_extreme,
    dequantize_precipitation_extreme,
)
from .spatial_slicer import SpatialSlicer, slice_point, bilinear_interpolate
from .threat_solver import ThreatSolver, evaluate_threat, calculate_urban_runoff
from .kisan_agro import KisanAgroEngine, calculate_fertilizer_balance, calculate_pump_runtime
from .voice_distiller import VoiceDistiller, to_kisan_voice
from .sync_worker import MeshSyncWorker
from .studio import launch_studio
gui = launch_studio
studio = launch_studio
from . import thermo
from . import kinematics
from . import grib
from . import container
from . import auto as auto_engine
from .grib import MausamMeshGribDataset, Grib2Message
from .container import MausamMeshQuantizer, MausamMeshWriter, MausamMeshReader
from .auto import (
    auto, 
    auto_scan, 
    auto_detect_location, 
    resolve_location,
    OFFLINE_GAZETTEER,
    serve, 
    AutonomousAtmosphericVerdict, 
    AdaptiveAtmosphericLearner
)
from .thermo import (
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
    SoundingAnalysis,
    analyze_sounding,
)
from .kinematics import (
    coriolis_parameter,
    beta_parameter,
    spherical_gradient,
    geostrophic_wind,
    ageostrophic_wind,
    thermal_wind,
    divergence,
    relative_vorticity,
    absolute_vorticity,
    advection,
    potential_vorticity_isobaric,
    bulk_shear,
    bunkers_storm_motion,
    storm_relative_helicity,
    supercell_composite_parameter,
)

__all__ = [
    "AtmosphericQuantizer",
    "quantize_grid",
    "dequantize_grid",
    "quantize_log",
    "dequantize_log",
    "quantize_precipitation_extreme",
    "dequantize_precipitation_extreme",
    "SpatialSlicer",
    "slice_point",
    "bilinear_interpolate",
    "ThreatSolver",
    "evaluate_threat",
    "calculate_urban_runoff",
    "KisanAgroEngine",
    "calculate_fertilizer_balance",
    "calculate_pump_runtime",
    "VoiceDistiller",
    "to_kisan_voice",
    "MeshSyncWorker",
    "launch_studio",
    "gui",
    "studio",
    "thermo",
    "kinematics",
    "saturation_vapor_pressure",
    "vapor_pressure_from_dewpoint",
    "vapor_pressure_from_rh",
    "dewpoint_from_vapor_pressure",
    "relative_humidity",
    "mixing_ratio",
    "saturation_mixing_ratio",
    "specific_humidity",
    "virtual_temperature",
    "potential_temperature",
    "temperature_from_potential_temperature",
    "virtual_potential_temperature",
    "lcl",
    "equivalent_potential_temperature",
    "wet_bulb_temperature",
    "moist_adiabatic_lapse_rate",
    "k_index",
    "total_totals_index",
    "lifted_index",
    "precipitable_water",
    "bulk_richardson_number",
    "SoundingAnalysis",
    "analyze_sounding",
    "coriolis_parameter",
    "beta_parameter",
    "spherical_gradient",
    "geostrophic_wind",
    "ageostrophic_wind",
    "thermal_wind",
    "divergence",
    "relative_vorticity",
    "absolute_vorticity",
    "advection",
    "potential_vorticity_isobaric",
    "bulk_shear",
    "bunkers_storm_motion",
    "storm_relative_helicity",
    "supercell_composite_parameter",
    "grib",
    "MausamMeshGribDataset",
    "Grib2Message",
    "container",
    "MausamMeshQuantizer",
    "MausamMeshWriter",
    "MausamMeshReader",
    "auto",
    "auto_scan",
    "auto_detect_location",
    "serve",
    "AutonomousAtmosphericVerdict",
    "AdaptiveAtmosphericLearner",
]
