"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — MASTER METEOROLOGICAL ENGINE (`engine`)
=============================================================================
Unified Meteorological & Hazard Intelligence Engine.
Connects Thermodynamics, Spherical Kinematics, Native GRIB2 Bitstream,
WMO Quantization, and Regional Early-Warning Intelligence
into a single cohesive, high-performance Python API.

MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
=============================================================================
"""

from __future__ import annotations
import math
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
import numpy as np

# Core submodules
try:
    from .thermo import (
        analyze_sounding, 
        SoundingAnalysis, 
        wet_bulb_temperature,
        saturation_vapor_pressure,
    )
    from .kinematics import (
        bulk_shear, 
        bunkers_storm_motion, 
        storm_relative_helicity, 
        supercell_composite_parameter,
    )
    from .severe import (
        evaluate_severe_diagnostics,
        SevereStormDiagnostics,
        downdraft_cape,
        significant_tornado_parameter,
        hail_diagnostics,
        lightning_potential_index,
        LightningPotentialReport,
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
    from .threat_solver import ThreatSolver, ThreatEvaluationResult, calculate_scs_curve_number_runoff, SCSCurveNumberReport
    from .satellite import diagnose_satellite_convection, ConvectiveCloudGrowthReport
    from .ensemble import evaluate_ensemble_risk, EnsemblePointSummary, EnsembleForecastGrid
    from .transcoder import convert_grib2_to_mmesh
    from .kisan_agro import KisanAgroEngine
    from .grib import MausamMeshGribDataset
    from .container import (
        MausamMeshQuantizer,
        MausamMeshWriter,
        MausamMeshReader,
    )
except (ImportError, ValueError):
    from thermo import (
        analyze_sounding, 
        SoundingAnalysis, 
        wet_bulb_temperature,
        saturation_vapor_pressure,
    )
    from kinematics import (
        bulk_shear, 
        bunkers_storm_motion, 
        storm_relative_helicity, 
        supercell_composite_parameter,
    )
    from severe import (
        evaluate_severe_diagnostics,
        SevereStormDiagnostics,
        downdraft_cape,
        significant_tornado_parameter,
        hail_diagnostics,
        lightning_potential_index,
        LightningPotentialReport,
    )
    from hazards import (
        detect_cloudburst,
        CloudburstAssessment,
        classify_cyclone,
        CycloneClassification,
        evaluate_kalbaisakhi,
        KalbaisakhiAlert,
        evaluate_heat_stress,
        HeatwaveHumanStress,
    )
    from radar import (
        classify_hydrometeor,
        HydrometeorReport,
        vad_wind_profile,
        HYDROMETEOR_TYPES,
    )
    from threat_solver import ThreatSolver, ThreatEvaluationResult, calculate_scs_curve_number_runoff, SCSCurveNumberReport
    from satellite import diagnose_satellite_convection, ConvectiveCloudGrowthReport
    from ensemble import evaluate_ensemble_risk, EnsemblePointSummary, EnsembleForecastGrid
    from transcoder import convert_grib2_to_mmesh
    from kisan_agro import KisanAgroEngine
    from grib import MausamMeshGribDataset
    from container import (
        MausamMeshQuantizer,
        MausamMeshWriter,
        MausamMeshReader,
    )


@dataclass
class MasterAtmosphericReport:
    """Consolidated high-level atmospheric assessment."""
    storm_mode: str
    sbcape_j_kg: float
    sbcin_j_kg: float
    lcl_height_m_agl: float
    dcape_j_kg: float
    peak_gust_kmh: float
    shear_0_6km_m_s: float
    srh_0_3km_m2_s2: float
    significant_tornado_parameter: float
    supercell_composite_parameter: float
    sweat_index: float
    max_hail_size_mm: float
    hail_threat: str
    tornado_risk: str
    wind_risk: str
    precipitable_water_mm: float
    k_index_c: float
    total_totals_c: float
    lightning: Optional[LightningPotentialReport] = None


class MausamEngine:
    """
    Master High-Level Meteorological & Disaster Intelligence Engine.
    """
    def __init__(self, standalone_mode: bool = True):
        self.standalone_mode = standalone_mode

    # =========================================================================
    # 1. SOUNDING & SEVERE WEATHER DIAGNOSTICS
    # =========================================================================
    def diagnose_sounding(
        self,
        pressure_levels_hpa: np.ndarray,
        temp_levels_c: np.ndarray,
        dewpoint_levels_c: np.ndarray,
        u_wind_m_s: np.ndarray,
        v_wind_m_s: np.ndarray,
        height_levels_m: Optional[np.ndarray] = None,
    ) -> MasterAtmosphericReport:
        """
        Runs end-to-end multi-layer thermodynamics and kinematic synthesis.
        Executes in < 0.005 seconds.
        """
        p = np.asarray(pressure_levels_hpa, dtype=np.float64)
        t = np.asarray(temp_levels_c, dtype=np.float64)
        td = np.asarray(dewpoint_levels_c, dtype=np.float64)
        u = np.asarray(u_wind_m_s, dtype=np.float64)
        v = np.asarray(v_wind_m_s, dtype=np.float64)

        # Sort descending from surface (high P) to top of atmosphere (low P)
        sort_idx = np.argsort(-p)
        p = p[sort_idx]
        t = t[sort_idx]
        td = td[sort_idx]
        u = u[sort_idx]
        v = v[sort_idx]
        
        # Approximate heights via hypsometric equation if not supplied
        if height_levels_m is None:
            z = np.zeros(len(p))
            z[0] = 0.0
            for i in range(len(p) - 1):
                p1, p2 = p[i], p[i + 1]
                t_mean = 0.5 * (t[i] + t[i + 1]) + 273.15
                dz = (287.058 * t_mean / 9.80665) * math.log(max(1e-3, p1 / max(1e-3, p2)))
                z[i + 1] = z[i] + dz
        else:
            z = np.asarray(height_levels_m, dtype=np.float64)[sort_idx]

        # 1. Core Thermodynamics
        thermo_res = analyze_sounding(p, t, td, z)

        # 2. Kinematics (Shear, Bunkers, Helicity)
        _, _, shear_0_6km = bulk_shear(u, v, z, depth_m=6000.0)
        c_right, _ = bunkers_storm_motion(u, v, z)
        c_rx, c_ry = c_right
        srh_1km = storm_relative_helicity(u, v, z, c_rx, c_ry, depth_m=1000.0)
        srh_3km = storm_relative_helicity(u, v, z, c_rx, c_ry, depth_m=3000.0)

        # 3. Severe Storm Hazards
        sev = evaluate_severe_diagnostics(
            pressure_levels_hpa=p,
            temp_levels_c=t,
            dewpoint_levels_c=td,
            height_levels_m=z,
            u_profile_m_s=u,
            v_profile_m_s=v,
            sbcape_j_kg=thermo_res.sbcape_j_kg,
            sbcin_j_kg=thermo_res.sbcin_j_kg,
            lcl_height_m=thermo_res.lcl_height_m,
            srh_0_1km=srh_1km,
            srh_0_3km=srh_3km,
            bulk_shear_0_6km_m_s=shear_0_6km,
        )

        return MasterAtmosphericReport(
            storm_mode=sev.storm_mode,
            sbcape_j_kg=float(round(thermo_res.sbcape_j_kg, 1)),
            sbcin_j_kg=float(round(thermo_res.sbcin_j_kg, 1)),
            lcl_height_m_agl=float(round(thermo_res.lcl_height_m, 0)),
            dcape_j_kg=float(round(sev.dcape_j_kg, 1)),
            peak_gust_kmh=float(round(sev.max_microburst_gust_kmh, 1)),
            shear_0_6km_m_s=float(round(shear_0_6km, 1)),
            srh_0_3km_m2_s2=float(round(srh_3km, 1)),
            significant_tornado_parameter=float(round(sev.significant_tornado_parameter, 2)),
            supercell_composite_parameter=float(round(sev.supercell_composite_parameter, 2)),
            sweat_index=float(round(sev.sweat_index, 1)),
            max_hail_size_mm=float(round(sev.max_expected_hail_size_mm, 1)),
            hail_threat=sev.hail_threat_category,
            tornado_risk=sev.tornado_risk_category,
            wind_risk=sev.wind_damage_risk,
            precipitable_water_mm=float(round(thermo_res.precipitable_water_mm, 1)),
            k_index_c=float(round(thermo_res.k_index_c, 1)),
            total_totals_c=float(round(thermo_res.total_totals_c, 1)),
            lightning=sev.lightning,
        )

    # =========================================================================
    # 2. REGIONAL EARLY-WARNING CONVENIENCE FACADES
    # =========================================================================
    def check_lightning(
        self,
        pressure_levels_hpa: np.ndarray,
        temp_levels_c: np.ndarray,
        dewpoint_levels_c: np.ndarray,
        height_levels_m: np.ndarray,
        sbcape_j_kg: float,
        precipitable_water_mm: float = 35.0,
        bulk_shear_0_6km_m_s: float = 12.0,
    ) -> LightningPotentialReport:
        """
        Direct Damini lightning siren and LPI charge separation assessment.
        """
        return lightning_potential_index(
            pressure_levels_hpa=pressure_levels_hpa,
            temp_levels_c=temp_levels_c,
            dewpoint_levels_c=dewpoint_levels_c,
            height_levels_m=height_levels_m,
            sbcape_j_kg=sbcape_j_kg,
            precipitable_water_mm=precipitable_water_mm,
            bulk_shear_0_6km_m_s=bulk_shear_0_6km_m_s,
        )

    def check_cloudburst(
        self,
        rainfall_rate_mm_hr: float,
        terrain_slope_deg: float = 20.0,
        precipitable_water_mm: float = 55.0,
    ) -> CloudburstAssessment:
        return detect_cloudburst(rainfall_rate_mm_hr, terrain_slope_deg, precipitable_water_mm)

    def classify_cyclone(
        self,
        max_sustained_wind_kmh: float,
        central_pressure_hpa: float = 980.0,
    ) -> CycloneClassification:
        return classify_cyclone(max_sustained_wind_kmh, central_pressure_hpa)

    def check_heat_stress(
        self,
        temp_c: float,
        rh_pct: float,
        wind_speed_kmh: float = 15.0,
        wind_direction_deg: float = 290.0,
    ) -> HeatwaveHumanStress:
        return evaluate_heat_stress(temp_c, rh_pct, wind_speed_kmh, wind_direction_deg)

    def check_norwester(
        self,
        dewpoint_c: float,
        rh_700_pct: float,
        cape_j_kg: float,
        shear_0_6km_m_s: float,
    ) -> KalbaisakhiAlert:
        return evaluate_kalbaisakhi(dewpoint_c, rh_700_pct, cape_j_kg, shear_0_6km_m_s)

    # =========================================================================
    # 3. DOPPLER RADAR & HYDROMETEOR INTELLIGENCE
    # =========================================================================
    def analyze_radar_echo(
        self,
        zh_dbz: float,
        zdr_db: float,
        rho_hv: float,
        kdp_deg_km: float = 0.0,
        temp_c: float = 15.0,
    ) -> HydrometeorReport:
        """Classifies polarimetric radar volume into physical hydrometeor types."""
        return classify_hydrometeor(zh_dbz, zdr_db, rho_hv, kdp_deg_km, temp_c)

    def vad_wind(
        self,
        radial_velocities_m_s: np.ndarray,
        azimuths_deg: np.ndarray,
        elevation_deg: float,
        slant_range_m: float,
    ) -> Tuple[float, float, float, float]:
        """Calculates VAD horizontal wind profile from Doppler radial velocities."""
        return vad_wind_profile(radial_velocities_m_s, azimuths_deg, elevation_deg, slant_range_m)

    # =========================================================================
    # 4. KISAN AGROMET & DISASTER THREAT EVALUATION
    # =========================================================================
    def evaluate_threat(self, **kwargs) -> ThreatEvaluationResult:
        """Evaluates multivariate atmospheric and hydrological flood threat."""
        return ThreatSolver.evaluate_threat(**kwargs)

    def calculate_fertilizer(self, **kwargs) -> Dict[str, Any]:
        """Calculates stoichiometric NPK to commercial fertilizer bags."""
        return KisanAgroEngine.calculate_fertilizer_balance(**kwargs)

    def calculate_irrigation_pump(self, **kwargs) -> Dict[str, Any]:
        """Calculates FAO-56 crop water evapotranspiration and pump runtime."""
        return KisanAgroEngine.calculate_pump_runtime(**kwargs)

    # =========================================================================
    # 5. GRIB2 & .mmesh EDGE FILE UTILITIES
    # =========================================================================
    def open_grib(self, filepath: str) -> MausamMeshGribDataset:
        """Opens GRIB2 file using zero-C memory-mapped parser."""
        return MausamMeshGribDataset(filepath)

    def open_mmesh(self, filepath: str) -> MausamMeshReader:
        """Opens WMO .mmesh container."""
        return MausamMeshReader(filepath)

    def transcode_grib2_to_mmesh(
        self,
        grib_filepath: str,
        output_mmesh_path: str,
        variables: Optional[List[str]] = None,
        bit_depth: int = 16,
    ) -> Dict[str, Any]:
        """Transcodes large raw GRIB2 file to ultra-compact quantized .mmesh file."""
        return convert_grib2_to_mmesh(
            grib_filepath=grib_filepath,
            output_mmesh_path=output_mmesh_path,
            variables=variables,
            bit_depth=bit_depth,
        )

    # =========================================================================
    # 6. SATELLITE, HYDROLOGICAL & ENSEMBLE ADVANCED ENGINES
    # =========================================================================
    def evaluate_watershed_runoff(
        self,
        rainfall_depth_mm: float,
        catchment_area_ha: float,
        hydrologic_soil_group: str = "C",
        land_use: str = "mixed_agricultural",
        antecedent_rainfall_5day_mm: float = 25.0,
    ) -> SCSCurveNumberReport:
        """Calculates rural watershed direct runoff depth and peak discharge via SCS-CN method."""
        return calculate_scs_curve_number_runoff(
            rainfall_depth_mm=rainfall_depth_mm,
            catchment_area_ha=catchment_area_ha,
            hydrologic_soil_group=hydrologic_soil_group,
            land_use=land_use,
            antecedent_rainfall_5day_mm=antecedent_rainfall_5day_mm,
        )

    def check_satellite_convection(
        self,
        tb_t1_c: float,
        tb_t2_c: float,
        time_delta_min: float = 15.0,
    ) -> ConvectiveCloudGrowthReport:
        """Detects explosive cumulonimbus updrafts and overshooting tops from INSAT satellite frames."""
        return diagnose_satellite_convection(tb_t1_c, tb_t2_c, time_delta_min=time_delta_min)

    def evaluate_ensemble_risk(
        self,
        member_forecasts: List[float],
        variable_name: str = "APCP",
    ) -> EnsemblePointSummary:
        """Computes probabilistic spread, PoP, and IMD warning thresholds across ensemble members."""
        return evaluate_ensemble_risk(member_forecasts, variable_name=variable_name)

