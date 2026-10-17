# ⚡ Module 07: Kisan Agromet, Dual-Polarimetric Radar & Voice Distiller (`kisan_agro`, `radar`, `voice_distiller`)
**Architecture Specification & Engineering Treatise**  
**Author:** Mr. Mohit Donawat (Founder, CEO & Lead Systems Architect — WildUs & MSD Innovations)  
**Package:** `mausam-mesh` | **Version:** `1.1.0` | **License:** MIT

---

## 1. 🎯 Executive Purpose: Grassroots Agricultural Resilience

While standard meteorological libraries serve academic researchers, `MausamMesh` was engineered to deliver direct life-saving and livelihood-protecting value to India's **140 million agricultural families**:
1. **Precision Tubewell Irrigation Optimization**: Prevents over-pumping, groundwater depletion, and power wastage by calculating exact crop evapotranspiration ($ET_0$) adjusted for antecedent rainfall.
2. **Stoichiometric Fertilizer Balancing**: Eliminates expensive fertilizer overdosing by computing commercial 50kg bag equivalents (DAP, Urea, MOP, SSP) based on soil deficiencies.
3. **Dual-Polarimetric Doppler Radar (DWR) Hydrometeor Classification**: Decodes reflectivity ($Z_H$), differential reflectivity ($Z_{DR}$), and cross-correlation coefficient ($\rho_{HV}$) into physical particles (Giant Hail, Heavy Rain, Wet Snow, Insects).
4. **Offline Multilingual Spoken Voice Distillation**: Generates natural spoken advisories in 6 Indian regional languages (Hindi, Telugu, Tamil, Marathi, Punjabi, Bengali) without external cloud TTS API costs.

---

## 2. 🌾 Kisan Agromet: FAO-56 Evapotranspiration & Tubewell Pump Math

### 2.1 Hargreaves Evapotranspiration ($ET_0$):
When solar radiation sensors are unavailable on rural farms, the **Hargreaves-Samani (1985)** equation estimates reference evapotranspiration from daily extreme temperatures and latitude:

$$ET_0 = 0.0023 \times R_a \times \sqrt{T_{\max} - T_{\min}} \times (T_{\text{mean}} + 17.8) \quad \left[\text{mm/day}\right]$$

Where:
* $R_a$ is extraterrestrial solar radiation ($\text{mm/day}$) derived from orbital solar declination $\delta$ and sunset hour angle $\omega_s$:
  $$\delta = 0.409 \sin\left(\frac{2\pi}{365} J - 1.39\right)$$
  $$\omega_s = \arccos(-\tan(\phi) \tan(\delta))$$
  $$R_a = \frac{24 \times 60}{\pi} G_{\text{sc}} d_r \left[\omega_s \sin(\phi) \sin(\delta) + \cos(\phi) \cos(\delta) \sin(\omega_s)\right]$$

### 2.2 Crop Water Requirement ($ET_c$) & FAO-56 Crop Coefficients ($K_c$):
$$ET_c = ET_0 \times K_c \quad \left[\text{mm/day}\right]$$

| Crop | Initial Stage $K_{c,\text{ini}}$ | Mid-Season $K_{c,\text{mid}}$ | Late Season $K_{c,\text{late}}$ |
| :--- | :---: | :---: | :---: |
| **Wheat (गेहूं)** | 0.40 | 1.15 | 0.35 |
| **Paddy / Rice (धान)** | 1.05 | 1.20 | 0.90 |
| **Mustard (सरसों)** | 0.35 | 1.05 | 0.35 |
| **Cotton (कपास)** | 0.45 | 1.20 | 0.50 |
| **Sugarcane (गन्ना)**| 0.40 | 1.25 | 0.75 |

### 2.3 Tubewell Pump Runtime Solver:
Given water deficit $D = \max(0.0, ET_c - P_{\text{rain}})$:
$$\text{Water Volume Needed} = D \times \text{Acres} \times 4046.86 \times 10^{-3} \quad \left[\text{m}^3\right]$$

Given tubewell pump horsepower (HP), the water discharge rate $Q_{\text{pump}}$ is calculated:
$$Q_{\text{pump}} = \text{HP} \times 2.8 \quad \left[\text{Liters/second}\right] = \text{HP} \times 0.0028 \times 3600 \quad \left[\text{m}^3/\text{hour}\right]$$

$$\text{Pump Runtime (Hours)} = \frac{\text{Water Volume Needed}}{Q_{\text{pump}}}$$

---

## 3. 🧪 Stoichiometric Fertilizer Optimization (DAP vs. SSP)

Indian farmers often waste money buying expensive DAP (Di-Ammonium Phosphate) when SSP (Single Super Phosphate) is superior and supplies essential Sulfur.

### 3.1 Nutrient Stoichiometry:
* **Urea**: $46\%\text{ Nitrogen (N)}$ (45kg bag)
* **DAP (18-46-0)**: $18\%\text{ Nitrogen (N)}$, $46\%\text{ Phosphate (P}_2\text{O}_5\text{)}$ (50kg bag)
* **MOP (0-0-60)**: $60\%\text{ Potash (K}_2\text{O)}$ (50kg bag)
* **SSP (0-16-0 + 11% S)**: $16\%\text{ Phosphate (P}_2\text{O}_5\text{)}$, $11\%\text{ Sulfur (S)}$ (50kg bag)

### 3.2 Dual-Source Solver:
When DAP is used, it also supplies secondary Nitrogen:
$$N_{\text{from\_DAP}} = \text{DAP Bags} \times 50 \times 0.18$$
$$\text{Net Urea Needed} = \frac{\max(0.0, N_{\text{target}} - N_{\text{from\_DAP}})}{45 \times 0.46}$$
This eliminates Nitrogen burning of crops!

---

## 4. 📡 Dual-Polarimetric Doppler Radar Engine (`radar`)

Modern Indian Doppler Weather Radars (IMD S-band and C-band DWRs) transmit both horizontally and vertically polarized microwave pulses.

### 4.1 Polarimetric Observables:
1. **$Z_H$ (Horizontal Reflectivity, dBZ)**: Total hydrometeor backscattered power.
2. **$Z_{DR}$ (Differential Reflectivity, dB)**: Shape ratio ($Z_H / Z_V$). Oblate raindrops have $Z_{DR} > 0$; tumbling hail pellets have $Z_{DR} \approx 0$.
3. **$\rho_{HV}$ (Cross-Correlation Coefficient)**: Uniformity of hydrometeors. Rain/snow has $\rho_{HV} > 0.96$; mixed-phase hail or non-meteorological clutter drops to $\rho_{HV} < 0.90$.
4. **$K_{DP}$ (Specific Differential Phase, deg/km)**: Liquid water content along radar ray.

### 4.2 Hydrometeor Classification Decision Matrix:
| Hydrometeor Class | $Z_H$ (dBZ) | $Z_{DR}$ (dB) | $\rho_{HV}$ | Temperature (°C) |
| :--- | :--- | :--- | :--- | :--- |
| **GIANT HAIL** | $\ge 58.0$ | $-0.5\text{ to }+0.8$ | $< 0.92$ | Any |
| **HAIL / RAIN MIX** | $50.0 - 58.0$ | $0.5 - 2.0$ | $0.88 - 0.95$ | $< 10.0$ |
| **TORRENTIAL RAIN** | $\ge 45.0$ | $> 2.2$ | $> 0.97$ | $> 0.0$ |
| **MODERATE RAIN** | $30.0 - 45.0$ | $0.8 - 2.2$ | $> 0.97$ | $> 0.0$ |
| **WET SNOW / GRAUPEL** | $25.0 - 40.0$ | $0.2 - 1.2$ | $0.90 - 0.96$ | $-5.0\text{ to }+2.0$ |
| **DRY AGGREGATES** | $15.0 - 30.0$ | $0.0 - 0.6$ | $> 0.98$ | $< -2.0$ |
| **BIOLOGICAL CLUTTER**| $< 20.0$ | $> 3.5$ | $< 0.80$ | Any |

---

## 5. 🗣️ Multilingual Voice Distiller (`voice_distiller`)

Converts complex meteorological telemetry into natural spoken agricultural advisories in 6 major Indian languages:
* **Hindi (हिन्दी)**
* **Telugu (తెలుగు)**
* **Tamil (தமிழ்)**
* **Marathi (मराठी)**
* **Punjabi (ਪੰਜਾਬੀ)**
* **Bengali (বাংলা)**

Directly formatted for village loudspeaker announcements, community radio, and smartphone voice push notifications.

---

## 6. 💻 Production Python Code Sample

```python
import mausam_mesh as mm

# 1. Calculate Tubewell Irrigation Runtime for 3 Acres of Wheat
pump = mm.calculate_pump_runtime(
    crop="wheat",
    acres=3.0,
    pump_hp=5.0,
    temp_max_c=36.0,
    temp_min_c=22.0,
    lat_deg=22.7,
    rainfall_forecast_mm=0.0
)

print(f"ET0 Reference: {pump['et0_mm_day']:.2f} mm/day")
print(f"Crop Water Demand: {pump['crop_water_demand_mm_day']:.2f} mm/day")
print(f"Recommended Tubewell Runtime: {pump['formatted_runtime']}")
print(f"Advice: {pump['advisory_hi']}")

# 2. Dual-Pol Doppler Radar Hail Detection
echo = mm.classify_hydrometeor(
    zh_dbz=62.0,
    zdr_db=0.3,
    rho_hv=0.89,
    kdp_deg_km=0.8,
    temp_c=12.0
)

print(f"Radar Classification: {echo.classification}")
print(f"Hail Hazard Detected: {echo.is_hail}")
print(f"Instantaneous Rain Rate: {echo.rain_rate_mm_hr} mm/hr")

# 3. Multilingual Voice Advisory
voice = mm.to_kisan_voice(None, language="hi")
print(f"Spoken Text: {voice['spoken_text']}")
```
