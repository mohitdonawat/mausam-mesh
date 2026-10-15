"""
=============================================================================
⚡ MAUSAMMESH KISAN AGRO — PRECISION AGROMET STOICHIOMETRY & PUMP MATH
=============================================================================
Computes:
1. Exact Chemical Stoichiometry: NPK to Commercial Fertilizer Bags (DAP, Urea, MOP)
2. FAO-56 Penman-Monteith Evapotranspiration: ETc = Kc * ET0
3. Tubewell Electric/Diesel Irrigation Pump Runtime Clock in Hours & Minutes
=============================================================================
"""

import math
from typing import Dict, Any, Optional


class KisanAgroEngine:
    """
    Precision Agricultural Meteorology Engine.
    """

    CROP_LIBRARY = {
        "wheat": {"name": "Wheat (गेहूँ)", "default_npk": (120, 60, 40), "kc_stage": {"basal": 0.45, "cri": 0.75, "tillering": 1.05, "flowering": 1.15, "grain_filling": 0.70}},
        "rice": {"name": "Paddy / Rice (धान)", "default_npk": (100, 50, 50), "kc_stage": {"basal": 0.60, "tillering": 1.10, "panicle": 1.20, "grain_filling": 0.85}},
        "cotton": {"name": "Cotton (कपास)", "default_npk": (150, 60, 60), "kc_stage": {"basal": 0.45, "vegetative": 0.80, "flowering_boll": 1.15, "maturity": 0.65}},
        "mustard": {"name": "Mustard (सरसों)", "default_npk": (80, 40, 40), "kc_stage": {"basal": 0.40, "vegetative": 0.75, "flowering": 1.10, "siliqua": 0.60}},
        "sugarcane": {"name": "Sugarcane (गन्ना)", "default_npk": (250, 115, 115), "kc_stage": {"germination": 0.50, "tillering": 0.85, "grand_growth": 1.25, "maturity": 0.70}},
        "soybean": {"name": "Soybean (सोयाबीन)", "default_npk": (30, 80, 40), "kc_stage": {"basal": 0.40, "vegetative": 0.80, "flowering_pod": 1.15, "maturity": 0.55}},
    }

    @classmethod
    def calculate_fertilizer_balance(
        cls,
        crop: str = "wheat",
        acres: float = 2.0,
        growth_stage: str = "basal",
        target_n_kg_ha: Optional[float] = None,
        target_p_kg_ha: Optional[float] = None,
        target_k_kg_ha: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates stoichiometric conversion of pure elemental target NPK into exact 50kg/45kg commercial bags.
        DAP: 18% N, 46% P2O5
        Urea: 46% N
        MOP: 60% K2O
        """
        crop_data = cls.CROP_LIBRARY.get(crop.lower(), cls.CROP_LIBRARY["wheat"])
        def_n, def_p, def_k = crop_data["default_npk"]

        n_req = target_n_kg_ha if target_n_kg_ha is not None else def_n
        p_req = target_p_kg_ha if target_p_kg_ha is not None else def_p
        k_req = target_k_kg_ha if target_k_kg_ha is not None else def_k

        # Convert hectares to acres factor (1 hectare = 2.47105 acres)
        ha_area = acres / 2.47105

        total_p_needed = p_req * ha_area
        total_n_needed = n_req * ha_area
        total_k_needed = k_req * ha_area

        # 1. DAP Calculation (46% P2O5)
        dap_kg = total_p_needed / 0.46
        n_supplied_by_dap = dap_kg * 0.18

        # 2. Urea Calculation (46% N)
        remaining_n = max(0.0, total_n_needed - n_supplied_by_dap)
        urea_kg = remaining_n / 0.46

        # 3. MOP Calculation (60% K2O)
        mop_kg = total_k_needed / 0.60

        # Commercial bag counts
        dap_bags = round(dap_kg / 50.0, 1)      # 50kg standard DAP bags
        urea_bags = round(urea_kg / 45.0, 1)    # 45kg official Neem Coated Urea bags
        mop_bags = round(mop_kg / 50.0, 1)      # 50kg MOP bags

        return {
            "crop": crop_data["name"],
            "farm_acres": acres,
            "target_npk_ratio": f"{int(n_req)}:{int(p_req)}:{int(k_req)}",
            "dap_kg": round(dap_kg, 1),
            "dap_50kg_bags": dap_bags,
            "urea_kg": round(urea_kg, 1),
            "urea_45kg_bags": urea_bags,
            "mop_kg": round(mop_kg, 1),
            "mop_50kg_bags": mop_bags,
            "stage_advice": f"Stage [{growth_stage.upper()}]: Apply 100% DAP and 100% MOP at basal sowing. Split Urea into 50% Basal, 25% Tillering, 25% Flowering."
        }

    @classmethod
    def calculate_pump_runtime(
        cls,
        crop: str = "wheat",
        growth_stage: str = "basal",
        acres: float = 2.0,
        pump_hp: float = 5.0,
        et0_mm_day: float = 4.5,
        rainfall_mm: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates daily crop water evapotranspiration (ETc = Kc * ET0)
        and converts it into tubewell pump runtime hours.
        """
        crop_data = cls.CROP_LIBRARY.get(crop.lower(), cls.CROP_LIBRARY["wheat"])
        kc = crop_data["kc_stage"].get(growth_stage.lower(), 0.75)

        etc_mm = kc * et0_mm_day
        effective_rain = min(etc_mm, rainfall_mm * 0.75)
        net_irrigation_depth_mm = max(0.0, etc_mm - effective_rain)

        # 1 mm depth over 1 acre = 4046.86 liters
        total_water_liters = net_irrigation_depth_mm * acres * 4046.86

        # Standard tubewell discharge: ~28,000 Liters/hour per 5 HP motor
        discharge_lph = max(5000.0, pump_hp * 5600.0)
        runtime_hours = total_water_liters / discharge_lph

        hours_int = int(math.floor(runtime_hours))
        minutes_int = int(round((runtime_hours - hours_int) * 60))

        return {
            "crop_evapotranspiration_etc_mm": round(etc_mm, 2),
            "net_water_liters": round(total_water_liters, 0),
            "recommended_runtime_hours": round(runtime_hours, 2),
            "formatted_runtime": f"{hours_int} घंटे {minutes_int} मिनट",
            "pump_hp": pump_hp,
            "action_guidance": "सिंचाई की आवश्यकता नहीं है (बारिश पर्याप्त है)" if total_water_liters == 0 else f"अपने {int(pump_hp)} HP मोटर पंप को आज {hours_int} घंटे {minutes_int} मिनट चलाएं।"
        }


def calculate_fertilizer_balance(*args, **kwargs) -> Dict[str, Any]:
    return KisanAgroEngine.calculate_fertilizer_balance(*args, **kwargs)


def calculate_pump_runtime(*args, **kwargs) -> Dict[str, Any]:
    return KisanAgroEngine.calculate_pump_runtime(*args, **kwargs)
