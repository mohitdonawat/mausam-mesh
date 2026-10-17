# ⚡ Module 06: Severe Hazards, Lightning Potential Index & Damini Siren Engine (`severe`, `hazards`)
**Architecture Specification & Engineering Treatise**  
**Author:** Mr. Mohit Donawat (Founder, CEO & Lead Systems Architect — WildUs & MSD Innovations)  
**Package:** `mausam-mesh` | **Version:** `1.1.0` | **License:** MIT

---

## 1. 🎯 Executive Purpose: Operational Severe Convective Defense

In the Indian subcontinent, severe convective phenomena cause massive loss of life and agricultural catastrophe each year:
- **Cloud-to-Ground Lightning Strikes**: Responsible for over 2,500 farmer deaths annually in Uttar Pradesh, Bihar, Madhya Pradesh, Odisha, and Maharashtra.
- **Microburst Downdrafts & Squall Lines**: Inverted-V dry downdrafts and Kalbaisakhi (Nor'westers) flattening crops and toppling power transmission towers with $> 100\text{ km/h}$ gusts.
- **Destructive Giant Hail**: Deep Hail Growth Zone (HGZ) updrafts producing $> 5\text{ cm}$ stones obliterating wheat, mustard, and horticulture.
- **Violent Tornadic Supercells & Himalayan Cloudbursts**: Concentrated vorticity and steep orographic funneling triggering flash floods in Uttarakhand and Himachal Pradesh.

`MausamMesh` integrates these convective diagnostic equations into pure, zero-dependency Python/NumPy algorithms aligned directly with **IMD (India Meteorological Department)**, **IITM Damini**, and **NDMA (National Disaster Management Authority)** standards.

---

## 2. ⚡ Lightning Potential Index (LPI) & Damini Siren Physics

The **Lightning Potential Index (LPI)** predicts the localized risk and flash density of cloud-to-ground lightning strikes by modeling non-inductive dipolar charge separation in the mixed-phase zone.

### 2.1 The Mixed-Phase Charging Zone ($-10^\circ\text{C}$ to $-25^\circ\text{C}$)
Atmospheric electricity is primarily generated between the $-10^\circ\text{C}$ and $-25^\circ\text{C}$ isotherms where supercooled liquid water, small ice crystals, and graupel coexist:
- Upward-moving ice crystals collide with heavier descending graupel pellets.
- Negative charge is transferred to the heavier graupel, while positive charge accumulates on smaller ice crystals carried upward into the anvil.
- The resulting intense vertical electric dipole triggers cloud-to-ground dielectric breakdown.

### 2.2 Mathematical Formulation (Yair et al., 2010):

$$\text{LPI} = \frac{1}{V} \int \int \int_{\text{charging zone}} w^2 \, \varepsilon(T) \, q_m \, dx \, dy \, dz \quad \left[\text{J/kg}\right]$$

In column diagnostic mode:
$$w_{\text{updraft}} = \sqrt{2 \times \text{CAPE}_{\text{charging\_zone}}}$$

$$\text{CAPE}_{\text{charging\_zone}} = \text{SBCAPE} \times \min\left(0.60, \max\left(0.12, \frac{Z_{-25^\circ\text{C}} - Z_{-10^\circ\text{C}}}{3500} \times 0.45\right)\right)$$

$$\text{LPI} = \frac{1}{2} w_{\text{updraft}}^2 \times \min\left(1.6, \max\left(0.4, \frac{\text{PWAT}}{30}\right)\right) \times \min\left(1.4, \max\left(0.5, \frac{\text{Shear}_{0-6\text{km}}}{15}\right)\right) \times \frac{1}{10}$$

### 2.3 Flash Rate Density ($\text{flashes} / \text{km}^2 / \text{hr}$):

$$\text{Flash Density} = 0.04 \times (\text{LPI})^{1.35} \quad (\text{for } \text{LPI} \ge 0.5)$$

### 2.4 Damini Warning Thresholds & Siren Activation:
| LPI Value | Risk Category | Flash Density | Siren Trigger | Action Directive |
| :--- | :--- | :--- | :---: | :--- |
| $\ge 35.0\text{ J/kg}$ | **EXTREME (CRITICAL DAMINI RED ALERT)** | $> 5.0 / \text{km}^2\text{/hr}$ | **YES** | 🚨 प्राणघातक आकाशीय बिजली का भीषण खतरा! खुले खेतों से तुरंत पक्के मकान में शरण लें। |
| $14.0 - 34.9\text{ J/kg}$ | **HIGH (SEVERE LIGHTNING THREAT)** | $1.5 - 5.0 / \text{km}^2\text{/hr}$ | **YES** | ⚠️ आकाशीय बिजली की तीव्र संभावना। किसान भाई खुले खेतों में काम तुरंत बंद करें। |
| $3.0 - 13.9\text{ J/kg}$ | **MODERATE (ISOLATED STRIKES)** | $0.2 - 1.5 / \text{km}^2\text{/hr}$ | NO | काले घने बादलों पर नज़र रखें; गर्जना सुनते ही सुरक्षित आश्रय लें। |
| $< 3.0\text{ J/kg}$ | **LOW (MINIMAL LIGHTNING RISK)** | $< 0.2 / \text{km}^2\text{/hr}$ | NO | सामान्य कृषि एवं बाहरी कार्य सुरक्षित हैं। |

---

## 3. 💨 Downdraft CAPE (DCAPE) & Peak Microburst Gusts

Downdraft CAPE calculates the maximum kinetic energy of a parcel descending saturated pseudo-adiabatically from mid-tropospheric minimum equivalent potential temperature ($\theta_e$) down to the surface:

$$\text{DCAPE} = -R_d \int_{P_{\min}}^{P_{\text{sfc}}} (T_{v,\text{env}} - T_{v,\text{parcel}}) \, d(\ln P) \quad \left[\text{J/kg}\right]$$

### Peak Microburst Wind Gust Velocity ($V_{\text{gust}}$):

$$V_{\text{gust}} = \sqrt{2 \times \text{DCAPE}} \quad \left[\text{m/s}\right]$$

$$V_{\text{gust},\text{km/h}} = V_{\text{gust}} \times 3.6$$

| DCAPE Range | Peak Gust Speed | Damage Potential |
| :--- | :--- | :--- |
| $> 1000\text{ J/kg}$ | $> 115\text{ km/h}$ | **Catastrophic Derecho / Macroburst**: Large trees uprooted, tin sheds blown off, transmission line collapse. |
| $600 - 1000\text{ J/kg}$ | $90 - 115\text{ km/h}$ | **Severe Microburst Squall**: High aviation hazard, tree limb snapping, structural damage. |
| $300 - 600\text{ J/kg}$ | $65 - 90\text{ km/h}$ | **Strong Convective Gusts**: Dust-raising wind, temporary hoardings at risk. |
| $< 300\text{ J/kg}$ | $< 65\text{ km/h}$ | **Normal Convective Breeze**: Sub-severe. |

---

## 4. 🌪️ Significant Tornado Parameter (STP) & Supercells

$$\text{STP} = \left(\frac{\text{SBCAPE}}{1500}\right) \times \left(\frac{2000 - Z_{\text{LCL}}}{1000}\right) \times \left(\frac{\text{SRH}_{0-1\text{km}}}{100}\right) \times \left(\frac{\text{Shear}_{0-6\text{km}}}{20}\right) \times \left(\frac{200 + \text{SBCIN}}{150}\right)$$

* $\text{STP} < 0.5$: Minimal tornadic potential.
* $\text{STP} \in [0.5, 1.0]$: Marginal tornadic supercell potential.
* $\text{STP} \in [1.0, 3.0]$: Significant tornado potential (EF2+).
* $\text{STP} > 3.0$: Violent tornado outbreak risk (EF3–EF5).

---

## 5. 🧊 Hail Growth Zone (HGZ) & Maximum Expected Hail Size (MEHS)

The Hail Growth Zone is situated between $-10^\circ\text{C}$ and $-30^\circ\text{C}$ where supercooled water accretes onto hail embryos without immediately freezing dry or shedding:

$$\text{HGZ CAPE} = \int_{Z_{-10^\circ\text{C}}}^{Z_{-30^\circ\text{C}}} g \left(\frac{T_{v,\text{parcel}} - T_{v,\text{env}}}{T_{v,\text{env}}}\right) dz$$

$$\text{MEHS} = 5.0 \times \left(\frac{\text{HGZ CAPE}}{100}\right)^{0.65} \times \left(\frac{\text{Shear}_{0-6\text{km}}}{15}\right)^{0.4} \quad \left[\text{mm}\right]$$

---

## 6. 🌊 Himalayan Cloudburst & Cyclone Surge Diagnostics

### 6.1 Orographic Cloudburst Engine (`detect_cloudburst`):
Triggers when rainfall exceeds $100\text{ mm/hr}$ in steep Himalayan / Western Ghats valleys:
* Orographic funneling ratio $\xi = 1.0 + \sin(\theta_{\text{slope}}) \times 1.4$.
* Evacuation lead time calculation for downstream riverine villages.

### 6.2 IMD Tropical Cyclone Classification (`classify_cyclone`):
Strictly adheres to official IMD 3-minute sustained wind speed criteria:
* **D**: Depression ($31 - 49\text{ km/h}$)
* **DD**: Deep Depression ($50 - 61\text{ km/h}$)
* **CS**: Cyclonic Storm ($62 - 88\text{ km/h}$)
* **SCS**: Severe Cyclonic Storm ($89 - 117\text{ km/h}$)
* **VSCS**: Very Severe Cyclonic Storm ($118 - 166\text{ km/h}$)
* **ESCS**: Extremely Severe Cyclonic Storm ($167 - 221\text{ km/h}$)
* **Super Cyclone**: $\ge 222\text{ km/h}$ (e.g. 1999 Odisha, Super Cyclone Amphan)
* Estimates peak storm surge inundation height ($m$) via bathymetric drop formulas.

---

## 7. 💻 Production Python Code Sample

```python
import numpy as np
import mausam_mesh as mm

# Pressure, Temperature, Dewpoint, Height, Wind profiles
p = np.array([1000.0, 925.0, 850.0, 700.0, 500.0, 300.0, 200.0])
t = np.array([35.0, 28.0, 23.0, 11.0, -11.0, -36.0, -56.0])
td = np.array([24.0, 20.0, 17.0, 5.0, -16.0, -42.0, -65.0])
z = np.array([120.0, 810.0, 1540.0, 3180.0, 5890.0, 9650.0, 12400.0])

# 1. Direct Damini LPI Assessment
lpi_report = mm.lightning_potential_index(
    pressure_levels_hpa=p,
    temp_levels_c=t,
    dewpoint_levels_c=td,
    height_levels_m=z,
    sbcape_j_kg=3200.0,
    precipitable_water_mm=48.0,
    bulk_shear_0_6km_m_s=22.0
)

print(f"LPI Index: {lpi_report.lpi_j_kg} J/kg")
print(f"Risk Category: {lpi_report.lightning_risk_category}")
print(f"Flash Density: {lpi_report.flash_rate_density_per_km2_hr} strikes/km²/hr")
print(f"Siren Trigger: {lpi_report.siren_trigger}")
print(f"Directive: {lpi_report.safety_directive}")

# 2. Complete Severe Storm Diagnostics
u = np.array([-3.0, 2.0, 8.0, 18.0, 28.0, 40.0, 32.0])
v = np.array([5.0, 10.0, 14.0, 12.0, 8.0, -2.0, -6.0])

sev = mm.evaluate_severe_diagnostics(
    pressure_levels_hpa=p,
    temp_levels_c=t,
    dewpoint_levels_c=td,
    height_levels_m=z,
    u_profile_m_s=u,
    v_profile_m_s=v,
    sbcape_j_kg=3200.0,
    sbcin_j_kg=-18.0,
    lcl_height_m=850.0,
    srh_0_1km=180.0,
    srh_0_3km=280.0,
    bulk_shear_0_6km_m_s=22.0
)

print(f"Storm Mode: {sev.storm_mode}")
print(f"DCAPE: {sev.dcape_j_kg:.1f} J/kg | Peak Gust: {sev.max_microburst_gust_kmh:.1f} km/h")
print(f"Max Expected Hail Size: {sev.max_expected_hail_size_mm:.1f} mm")
print(f"STP: {sev.significant_tornado_parameter:.2f}")
```
