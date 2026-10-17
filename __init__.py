"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — METEOROLOGICAL EDGE ENGINE
=============================================================================
Open-Source Global Python/Edge Library for:
1. WMO-No. 8 Atmospheric Tensor Quantization (50%-70% Payload Reduction)
2. O(1) Bilinear Coordinate Point Slicing in < 0.2ms
3. Convective Instability & Rational Flood Runoff (Q = CIA/360)
4. Kisan Agromet Stoichiometric NPK & FAO-56 Tubewell Pump Math
5. Multilingual Spoken Voice Distillation (Regional Directives)
=============================================================================
MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
=============================================================================
"""

__version__ = "1.2.0"
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
from .threat_solver import (
    ThreatSolver, 
    ThreatEvaluationResult, 
    evaluate_threat, 
    calculate_urban_runoff,
    calculate_scs_curve_number_runoff,
    SCSCurveNumberReport,
)
from .kisan_agro import KisanAgroEngine, calculate_fertilizer_balance, calculate_pump_runtime, calculate_et0_hargreaves
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
from . import severe
from . import hazards
from . import radar
from . import engine
from . import imd
from . import satellite
from . import transcoder
from . import ensemble
from .satellite import (
    INSATSatelliteEngine,
    diagnose_satellite_convection,
    ConvectiveCloudGrowthReport,
    radiance_to_brightness_temp,
    imsra_satellite_rain_rate,
    IMD_SATELLITE_CATALOG,
)
from .transcoder import (
    convert_grib2_to_mmesh,
    crop_grid_to_bbox,
)
from .ensemble import (
    EnsembleForecastGrid,
    EnsemblePointSummary,
    evaluate_ensemble_risk,
    IMD_RAINFALL_THRESHOLDS,
)
from .imd import (
    IMDIngestionEngine,
    fetch_imd_nowcast,
    fetch_imd_national_summary,
    IMD_CATEGORIES,
    IMD_DWR_STATIONS,
)
from .engine import MausamEngine, MasterAtmosphericReport
from .severe import (
    downdraft_cape,
    significant_tornado_parameter,
    hail_diagnostics,
    sweat_index,
    lightning_potential_index,
    LightningPotentialReport,
    evaluate_severe_diagnostics,
    SevereStormDiagnostics,
)
from .hazards import (
    detect_cloudburst,
    CloudburstAssessment,
    classify_cyclone,
    CycloneClassification,
    evaluate_kalbaisakhi,
    KalbaisakhiAlert,
    evaluate_heat_stress,
    HeatwaveHumanStress,
)
from .radar import (
    classify_hydrometeor,
    HydrometeorReport,
    vad_wind_profile,
    HYDROMETEOR_TYPES,
)
from .grib import MausamMeshGribDataset, Grib2Message
from .grib_streamer import MultiFileGribCatalog, GribBatchStreamer, INDIA_BBOX
from .grib_downloader import GribBulkDownloader, download_latest_operational_gfs
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
    "ThreatEvaluationResult",
    "evaluate_threat",
    "calculate_urban_runoff",
    "KisanAgroEngine",
    "calculate_fertilizer_balance",
    "calculate_pump_runtime",
    "calculate_et0_hargreaves",
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
    "MultiFileGribCatalog",
    "GribBatchStreamer",
    "INDIA_BBOX",
    "GribBulkDownloader",
    "download_latest_operational_gfs",
    "container",
    "MausamMeshQuantizer",
    "MausamMeshWriter",
    "MausamMeshReader",
    "auto",
    "auto_scan",
    "auto_detect_location",
    "resolve_location",
    "OFFLINE_GAZETTEER",
    "serve",
    "AutonomousAtmosphericVerdict",
    "AdaptiveAtmosphericLearner",
    "severe",
    "hazards",
    "radar",
    "engine",
    "MausamEngine",
    "MasterAtmosphericReport",
    "downdraft_cape",
    "significant_tornado_parameter",
    "hail_diagnostics",
    "sweat_index",
    "lightning_potential_index",
    "LightningPotentialReport",
    "evaluate_severe_diagnostics",
    "SevereStormDiagnostics",
    "detect_cloudburst",
    "CloudburstAssessment",
    "classify_cyclone",
    "CycloneClassification",
    "evaluate_kalbaisakhi",
    "KalbaisakhiAlert",
    "evaluate_heat_stress",
    "HeatwaveHumanStress",
    "classify_hydrometeor",
    "HydrometeorReport",
    "vad_wind_profile",
    "HYDROMETEOR_TYPES",
    "imd",
    "IMDIngestionEngine",
    "fetch_imd_nowcast",
    "fetch_imd_national_summary",
    "IMD_CATEGORIES",
    "IMD_DWR_STATIONS",
    "calculate_scs_curve_number_runoff",
    "SCSCurveNumberReport",
    "satellite",
    "INSATSatelliteEngine",
    "diagnose_satellite_convection",
    "ConvectiveCloudGrowthReport",
    "radiance_to_brightness_temp",
    "imsra_satellite_rain_rate",
    "IMD_SATELLITE_CATALOG",
    "transcoder",
    "convert_grib2_to_mmesh",
    "crop_grid_to_bbox",
    "ensemble",
    "EnsembleForecastGrid",
    "EnsemblePointSummary",
    "evaluate_ensemble_risk",
    "IMD_RAINFALL_THRESHOLDS",
]
