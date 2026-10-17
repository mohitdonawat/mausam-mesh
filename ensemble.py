"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — MULTI-MODEL ENSEMBLE SPREAD & PoP ENGINE (`ensemble`)
=============================================================================
High-performance probabilistic numerical weather prediction (EPS) engine.
Models uncertainty across multi-member ensembles (e.g., IMD NEPS 11-member,
NOAA GEFS 21-member, ECMWF EPS 51-member).

Solves:
1. Ensemble Mean (μ) and Ensemble Spread (σ)
2. Probability of Exceedance / Probability of Precipitation (PoP)
3. Official IMD Rainfall Risk Thresholds (Light, Moderate, Heavy, Very Heavy, Extremely Heavy)
4. Village-level Point Probabilistic Quantiles (P10, P50, P90, IQR)
5. Atmospheric Predictability & Spread-to-Skill Diagnostic

MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
=============================================================================
"""

from __future__ import annotations
import math
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
import numpy as np


# =============================================================================
# OFFICIAL IMD 24-HOUR RAINFALL SEVERITY THRESHOLDS (mm)
# =============================================================================
IMD_RAINFALL_THRESHOLDS = {
    "LIGHT_RAIN": 2.5,          # >= 2.5 mm
    "MODERATE_RAIN": 15.6,      # >= 15.6 mm
    "HEAVY_RAIN": 64.5,         # >= 64.5 mm (IMD Yellow Alert)
    "VERY_HEAVY_RAIN": 115.6,   # >= 115.6 mm (IMD Orange Alert)
    "EXTREMELY_HEAVY": 204.5,   # >= 204.5 mm (IMD Red Alert)
}


@dataclass
class EnsemblePointSummary:
    """Probabilistic forecast synthesis at a single geographic coordinate."""
    variable_name: str
    member_count: int
    mean_val: float
    spread_std: float
    median_p50: float
    p10: float
    p90: float
    min_val: float
    max_val: float
    pop_light_pct: float
    pop_heavy_pct: float
    pop_very_heavy_pct: float
    forecast_confidence_pct: float
    imd_alert_level: str
    risk_directive: str


class EnsembleForecastGrid:
    """
    Multi-member atmospheric ensemble tensor processor.
    Accepts 3D array of shape (N_members, N_rows, N_cols).
    """
    def __init__(
        self,
        ensemble_tensor: np.ndarray,
        variable_name: str = "APCP",
        lat_grid: Optional[np.ndarray] = None,
        lon_grid: Optional[np.ndarray] = None,
    ):
        tensor = np.asarray(ensemble_tensor, dtype=np.float32)
        if tensor.ndim != 3:
            raise ValueError(f"Ensemble tensor must be 3-dimensional (members, rows, cols), got shape {tensor.shape}")
            
        self.data = tensor
        self.n_members, self.n_rows, self.n_cols = tensor.shape
        self.variable_name = variable_name
        self.lat_grid = lat_grid
        self.lon_grid = lon_grid

    def mean(self) -> np.ndarray:
        """Computes pixel-wise ensemble mean (expected value)."""
        return np.mean(self.data, axis=0)

    def spread(self) -> np.ndarray:
        """Computes pixel-wise ensemble spread (sample standard deviation)."""
        if self.n_members < 2:
            return np.zeros((self.n_rows, self.n_cols), dtype=np.float32)
        return np.std(self.data, axis=0, ddof=1)

    def percentile(self, q: float) -> np.ndarray:
        """Computes pixel-wise percentile slice (e.g. q=10, 50, 90)."""
        return np.percentile(self.data, q=q, axis=0)

    def probability_of_exceedance(self, threshold: float) -> np.ndarray:
        """
        Computes probability (%) that values exceed given threshold.
        PoP = (Count(x >= threshold) / N_members) * 100.0
        """
        exceed_count = np.sum(self.data >= threshold, axis=0)
        return (exceed_count.astype(np.float32) / float(self.n_members)) * 100.0

    def compute_imd_rainfall_probabilities(self) -> Dict[str, np.ndarray]:
        """
        Calculates Pan-India spatial probability maps for all official IMD rainfall classes:
        Light (2.5mm), Moderate (15.6mm), Heavy (64.5mm), Very Heavy (115.6mm), Extremely Heavy (204.5mm).
        """
        result = {}
        for cat_name, thresh in IMD_RAINFALL_THRESHOLDS.items():
            result[cat_name] = self.probability_of_exceedance(thresh)
        return result

    def extract_point_distribution(
        self,
        row_idx: int,
        col_idx: int
    ) -> EnsemblePointSummary:
        """
        Extracts complete probability density distribution for a single grid cell.
        """
        r = max(0, min(self.n_rows - 1, row_idx))
        c = max(0, min(self.n_cols - 1, col_idx))
        
        sample = self.data[:, r, c]
        mean_v = float(np.mean(sample))
        std_v = float(np.std(sample, ddof=1)) if self.n_members > 1 else 0.0
        p10_v = float(np.percentile(sample, 10))
        p50_v = float(np.percentile(sample, 50))
        p90_v = float(np.percentile(sample, 90))
        min_v = float(np.min(sample))
        max_v = float(np.max(sample))
        
        pop_light = float((np.sum(sample >= IMD_RAINFALL_THRESHOLDS["LIGHT_RAIN"]) / self.n_members) * 100.0)
        pop_heavy = float((np.sum(sample >= IMD_RAINFALL_THRESHOLDS["HEAVY_RAIN"]) / self.n_members) * 100.0)
        pop_vheavy = float((np.sum(sample >= IMD_RAINFALL_THRESHOLDS["VERY_HEAVY_RAIN"]) / self.n_members) * 100.0)
        pop_extreme = float((np.sum(sample >= IMD_RAINFALL_THRESHOLDS["EXTREMELY_HEAVY"]) / self.n_members) * 100.0)
        
        # Relative spread-to-mean coefficient of variation for forecast confidence
        cov = (std_v / max(1.0, abs(mean_v))) if mean_v > 0 else 0.0
        confidence = float(max(15.0, min(99.0, (1.0 - min(1.0, cov * 0.5)) * 100.0)))
        
        if pop_extreme >= 30.0 or pop_vheavy >= 60.0:
            alert = "RED (EXTREME HIGH RISK)"
            directive = "🚨 अधिकांश मॉडल अति-भीषण वर्षा की पुष्टि कर रहे हैं! बाढ़ की चेतावनी, निचले इलाकों से सुरक्षित दूरी बनाएं।"
        elif pop_vheavy >= 30.0 or pop_heavy >= 60.0:
            alert = "ORANGE (SEVERE ALERT)"
            directive = "⚠️ मॉडल स्प्रेड में भारी वर्षा की उच्च संभावना। जलजमाव व यातायात अवरोध की तैयारी रखें।"
        elif pop_heavy >= 30.0 or pop_light >= 75.0:
            alert = "YELLOW (WATCH / ADVISORY)"
            directive = "वर्षा की सामान्य से मध्यम संभावना। नियमित मौसम अपडेट पर नज़र रखें।"
        else:
            alert = "GREEN (MINIMAL RISK)"
            directive = "मॉडल सहमति: मौसम सामान्य एवं शांत रहने का अनुमान।"
            
        return EnsemblePointSummary(
            variable_name=self.variable_name,
            member_count=self.n_members,
            mean_val=float(round(mean_v, 2)),
            spread_std=float(round(std_v, 2)),
            median_p50=float(round(p50_v, 2)),
            p10=float(round(p10_v, 2)),
            p90=float(round(p90_v, 2)),
            min_val=float(round(min_v, 2)),
            max_val=float(round(max_v, 2)),
            pop_light_pct=float(round(pop_light, 1)),
            pop_heavy_pct=float(round(pop_heavy, 1)),
            pop_very_heavy_pct=float(round(pop_vheavy, 1)),
            forecast_confidence_pct=float(round(confidence, 1)),
            imd_alert_level=alert,
            risk_directive=directive,
        )


def evaluate_ensemble_risk(
    member_forecasts: List[float],
    variable_name: str = "APCP"
) -> EnsemblePointSummary:
    """
    Convenience function to evaluate probabilistic risk directly from a 1D list 
    of ensemble member forecasts (e.g. 11 or 21 values for a single village).
    """
    arr = np.asarray(member_forecasts, dtype=np.float32).reshape((-1, 1, 1))
    grid = EnsembleForecastGrid(arr, variable_name=variable_name)
    return grid.extract_point_distribution(0, 0)
