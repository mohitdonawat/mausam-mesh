# ⚡ Module 08: Watershed SCS-CN Runoff, INSAT Satellite & Ensemble PoP (`threat_solver`, `satellite`, `ensemble`, `transcoder`)
**Architecture Specification & Engineering Treatise**  
**Author:** Mr. Mohit Donawat (Founder, CEO & Lead Systems Architect — WildUs & MSD Innovations)  
**Package:** `mausam-mesh` | **Version:** `1.1.0` | **License:** MIT

---

## 1. 🎯 Executive Purpose: Sovereign Disaster Intelligence & Spaceborne Remote Sensing

Module 08 bridges spaceborne remote sensing, physical hydrology, and numerical weather prediction (NWP) uncertainty modeling:
1. **SCS-CN Rural & Agricultural Watershed Runoff Engine**: Solves infiltration, soil retention, and direct runoff depth for Indian agricultural soils (Black Cotton, Alluvial, Red Sandy Loam) across Antecedent Moisture Conditions (AMC-I, II, III).
2. **ISRO / IMD INSAT-3D & INSAT-3DR Geostationary Satellite Engine**: Inverts Planck's radiation law on TIR-1 (10.8µm) and Water Vapor (6.8µm) spectral radiance, tracks rapid cloud top cooling rates ($\Delta T_B / \Delta t \le -16^\circ\text{C/hr}$), detects Over-Shooting Tops (OST), and calculates precipitation rates via the IMSRA algorithm.
3. **Multi-Model Ensemble Spread & Probability of Precipitation (PoP)**: Quantifies atmospheric forecast uncertainty across multi-member ensembles (e.g. IMD NEPS 11-member, NOAA GEFS 21-member, ECMWF EPS 51-member) and evaluates spatial probability maps across official IMD rainfall warning categories.
4. **Direct GRIB2-to-`.mmesh` Transcoder Pipeline**: Converts multi-hundred megabyte raw GRIB2 files into compact, WMO-quantized `.mmesh` containers with regional geographic bounding box cropping, achieving **80%–95% file size compression**.

---

## 2. 🌊 USDA / CWC SCS Curve Number (SCS-CN) Runoff Engine

Unlike the Rational Method ($Q = CIA/360$) which is only valid for small urban catchments ($< 50\text{ ha}$), the **USDA NRCS / Indian Central Water Commission (CWC)** Curve Number method models real infiltration and surface runoff over entire rural watersheds and river basins.

### 2.1 Hydrologic Soil Groups (HSG):
* **Group A**: Deep sand, loess, aggregated silts. High infiltration rate ($> 7.5\text{ mm/hr}$).
* **Group B**: Sandy loam, shallow loess. Moderate infiltration rate ($3.8 - 7.5\text{ mm/hr}$).
* **Group C**: Clay loams, shallow soils, high clay content. Low infiltration rate ($1.3 - 3.8\text{ mm/hr}$).
* **Group D**: Heavy swelling clays (e.g., Indian Black Cotton Soil), soils with permanent high water table. Very low infiltration rate ($< 1.3\text{ mm/hr}$).

### 2.2 Antecedent Moisture Condition (AMC) Categorization:
Based on cumulative 5-day prior rainfall ($P_5$):
* **AMC-I (Dry)**: $P_5 < 13\text{ mm}$ (dormant season) or $P_5 < 36\text{ mm}$ (growing season).
* **AMC-II (Normal / Average)**: $13\text{ mm} \le P_5 \le 28\text{ mm}$ (dormant) or $36\text{ mm} \le P_5 \le 53\text{ mm}$ (growing).
* **AMC-III (Saturated / Wet)**: $P_5 > 28\text{ mm}$ (dormant) or $P_5 > 53\text{ mm}$ (growing).

### 2.3 Mathematical CN Conversion Formulas:

$$\text{CN}_{\text{I}} = \frac{\text{CN}_{\text{II}}}{2.281 - 0.01281 \times \text{CN}_{\text{II}}}$$

$$\text{CN}_{\text{III}} = \frac{\text{CN}_{\text{II}}}{0.427 + 0.00573 \times \text{CN}_{\text{II}}}$$

### 2.4 Potential Maximum Soil Retention ($S$) & Initial Abstraction ($I_a$):

$$S = \frac{25400}{\text{CN}} - 254 \quad \left[\text{mm}\right]$$

$$I_a = \lambda \times S \quad \left[\text{mm}\right]$$

> **Indian Monsoon Calibration**: While standard USDA guidelines set $\lambda = 0.20$, the Indian Central Water Commission (CWC) and Ministry of Agriculture establish $\lambda = 0.05$ for Indian tropical catchments due to crusting and rapid saturation of clay soils.

### 2.5 Direct Surface Runoff Depth ($P_e$):

$$P_e = 0 \quad (\text{if } P \le I_a)$$

$$P_e = \frac{(P - I_a)^2}{P - I_a + S} \quad (\text{if } P > I_a) \quad \left[\text{mm}\right]$$

### 2.6 Total Runoff Volume ($V$) & Peak Discharge ($Q_p$):

$$V = P_e \times \text{Catchment Area (ha)} \times 10 \quad \left[\text{m}^3\right]$$

Time of concentration ($t_c$) via Kirpich formula:
$$t_c = \frac{0.0195 \times L^{0.77} \times S_{\text{slope}}^{-0.385}}{60} \quad \left[\text{hours}\right]$$

Time to peak ($t_p$):
$$t_p = 0.6 \, t_c + 0.25 \quad \left[\text{hours}\right]$$

Peak Discharge via SCS Triangular Unit Hydrograph:
$$Q_p = \frac{0.208 \times A_{\text{km}^2} \times P_e}{t_p} \quad \left[\text{m}^3/\text{s}\right]$$

---

## 3. 🛰️ ISRO / IMD INSAT-3D/3DR Satellite Remote Sensing Engine

### 3.1 Geostationary Spacecraft Orbital Positions:
* **INSAT-3D**: Positioned at $82.0^\circ\text{E}$ over the Bay of Bengal / Indian subcontinent.
* **INSAT-3DR**: Positioned at $74.0^\circ\text{E}$ over the Arabian Sea / Western India.
* Provides **Rapid Scan sector imagery every 4 minutes** during cyclones and monsoonal depressions.

### 3.2 Inversion of Planck's Blackbody Law:
Given spectral radiance $L_\lambda$ ($\text{mW} / (\text{m}^2 \cdot \text{sr} \cdot \text{cm}^{-1})$):

$$T_B = \frac{c_2 \cdot \nu}{\ln\left(\frac{c_1 \cdot \nu^3}{L_\lambda} + 1\right)} \quad \left[\text{Kelvin}\right]$$

Where:
* $c_1 = 1.191042 \times 10^{-5}\text{ mW} / (\text{m}^2 \cdot \text{sr} \cdot \text{cm}^{-4})$
* $c_2 = 1.438775\text{ cm} \cdot \text{K}$
* $\nu = 925.9\text{ cm}^{-1}$ for TIR-1 ($10.8\text{ }\mu\text{m}$)

### 3.3 Rapid Convective Cooling & Over-Shooting Top (OST) Detection:
Tracks rate of cloud-top cooling between consecutive satellite frames ($t_1, t_2$):

$$\text{Cooling Rate} = \frac{T_{B, t_1} - T_{B, t_2}}{\Delta t} \quad \left[^\circ\text{C/hr}\right]$$

* **Explosive Updraft Alert**: Triggered when $\text{Cooling Rate} \ge 16.0^\circ\text{C/hr}$ and $T_B \le -35^\circ\text{C}$.
* **Over-Shooting Top (OST)**: Triggered when $T_B \le T_{\text{tropopause}}$ (typically $\le -70^\circ\text{C}$ to $-75^\circ\text{C}$ in India), confirming an updraft core bursting into the lower stratosphere.

### 3.4 IMSRA (IMD Multispectral Satellite Rainfall Algorithm):

$$R = 0 \quad (\text{if } T_B > -20.0^\circ\text{C})$$

$$R = 1.15 \times \exp\left(0.054 \times (-20.0 - T_B)\right) \times \mu_{\text{moisture}} \quad \left[\text{mm/hr}\right]$$

---

## 4. 🎯 Multi-Model Ensemble Spread & Probability of Precipitation (PoP)

Numerical Weather Prediction ensembles model atmospheric chaotic bifurcation:

### 4.1 Ensemble Mean ($\mu$) & Spread ($\sigma$):

$$\mu(y, x) = \frac{1}{M} \sum_{m=1}^M X_m(y, x)$$

$$\sigma(y, x) = \sqrt{\frac{1}{M-1} \sum_{m=1}^M \left(X_m(y, x) - \mu(y, x)\right)^2}$$

### 4.2 Probability of Exceedance / PoP:

$$\text{PoP}(\text{threshold}) = \frac{1}{M} \sum_{m=1}^M \mathbb{I}\left(X_m \ge \text{threshold}\right) \times 100\%$$

### 4.3 Official IMD Rainfall Alert Thresholds:
* **Light Rain**: $\ge 2.5\text{ mm}$
* **Moderate Rain**: $\ge 15.6\text{ mm}$
* **Heavy Rain (Yellow Alert)**: $\ge 64.5\text{ mm}$
* **Very Heavy Rain (Orange Alert)**: $\ge 115.6\text{ mm}$
* **Extremely Heavy Rain (Red Alert)**: $\ge 204.5\text{ mm}$

---

## 5. 🔄 Direct GRIB2-to-`.mmesh` Transcoder Pipeline

```
┌─────────────────────────────────┐
│     Raw GRIB2 File (~500 MB)    │
└────────────────┬────────────────┘
                 │
                 ▼
     [ MausamMeshGribDataset ]
     - O(1) Memory-Mapped seek
     - Multi-template unpacking
                 │
                 ▼
       [ crop_grid_to_bbox ]
       - India Bounding Box Crop
       (6.0N-38.0N, 68.0E-98.0E)
                 │
                 ▼
     [ AtmosphericQuantizer ]
     - WMO Uniform Affine Uint16
                 │
                 ▼
     [ MausamMeshWriter (zlib) ]
                 │
                 ▼
┌─────────────────────────────────┐
│  Quantized .mmesh File (~12 MB) │ (80% - 95% Payload Reduction)
└─────────────────────────────────┘
```

---

## 6. 💻 Production Python Code Sample

```python
import mausam_mesh as mm

# 1. Agricultural Watershed Runoff via SCS-CN Method
runoff_report = mm.calculate_scs_curve_number_runoff(
    rainfall_depth_mm=95.0,
    catchment_area_ha=250.0,
    hydrologic_soil_group="C",
    land_use="mixed_agricultural",
    antecedent_rainfall_5day_mm=38.0, # Saturated soil (AMC-III)
    slope_pct=2.5,
    flow_length_m=1200.0,
    initial_abstraction_ratio=0.05
)

print(f"Direct Runoff Depth: {runoff_report.direct_runoff_depth_pe_mm} mm")
print(f"Total Runoff Volume: {runoff_report.total_runoff_volume_m3} m³")
print(f"Peak Discharge (Qp): {runoff_report.peak_discharge_qp_m3s} m³/s")
print(f"Flood Risk Category: {runoff_report.flood_risk_category}")
print(f"Advisory: {runoff_report.advisory}")

# 2. INSAT Satellite Convective Updraft Detection
sat_diag = mm.diagnose_satellite_convection(
    tb_t1_c=-30.0,
    tb_t2_c=-74.0, # Cloud top cooled by 44°C in 15 mins!
    time_delta_min=15.0
)

print(f"Cooling Rate: {sat_diag.cooling_rate_c_per_hr} °C/hr")
print(f"Overshooting Top: {sat_diag.is_overshooting_top}")
print(f"Explosive Updraft: {sat_diag.is_explosive_updraft}")
print(f"IMSRA Rain Rate: {sat_diag.estimated_imsra_rain_rate_mm_hr} mm/hr")
print(f"Directive: {sat_diag.safety_directive}")

# 3. Multi-Model Ensemble Spread & PoP Assessment
# 11-member ensemble forecast for a village
member_forecasts = [12.0, 25.0, 75.0, 80.0, 110.0, 15.0, 68.0, 95.0, 30.0, 5.0, 125.0]
ens = mm.evaluate_ensemble_risk(member_forecasts, variable_name="APCP")

print(f"Ensemble Mean: {ens.mean_val} mm | Spread: ±{ens.spread_std} mm")
print(f"PoP Heavy Rain (>= 64.5mm): {ens.pop_heavy_pct}%")
print(f"IMD Alert Verdict: {ens.imd_alert_level}")
print(f"Directive: {ens.risk_directive}")

# 4. Transcode GRIB2 to .mmesh
result = mm.convert_grib2_to_mmesh(
    grib_filepath="input_sample.grib2",
    output_mmesh_path="output_quantized.mmesh",
    variables=["TMP", "UGRD", "VGRD", "CAPE"]
)
print(f"Payload Reduction: {result['payload_reduction_pct']}%")
```
