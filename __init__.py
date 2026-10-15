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

__version__ = "1.0.1"
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
]
