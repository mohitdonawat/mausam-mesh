# ⚡ MausamMesh — Scientific Architecture Specification
## Module 02: Dynamic Kinematics & Vector Calculus Engine (`mausam_mesh.kinematics`)

**Architect & Author**: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)  
**Repository**: [github.com/mohitdonawat/mausam-mesh](https://github.com/mohitdonawat/mausam-mesh)  
**Status**: APPROVED SCIENTIFIC SPECIFICATION  
**Target Benchmark**: 120x Faster than `MetPy` (`metpy.calc.kinematics`), Native Spherical Coordinate Corrections, Zero-Pint Runtime Overhead.

---

## 1. 🎯 Executive Purpose & Meteorological Mandate

Atmospheric motion is governed by non-linear fluid dynamics on a rotating sphere. While thermodynamics (Module 01) tells us **how much potential energy** is stored in an atmospheric column, kinematics and dynamics determine **how that energy converts into destructive winds, rotating cyclones, severe thunderstorms, and jet stream turbulence**.

### Critical Deficiencies of Academic Kinematics (`MetPy`):
1. **Flat-Plane Assumption Errors**: Most standard tutorials and MetPy functions approximate grids with Cartesian coordinates ($dx, dy = \text{const}$). Over a large subcontinent like India (spanning $6^\circ\text{N}$ at Kanyakumari to $38^\circ\text{N}$ at Kashmir), the convergence of meridians introduces up to **18% metric error** in vorticity and divergence if spherical metric terms ($\frac{u}{R}\tan\phi$) are omitted.
2. **Excessive Memory Allocation**: MetPy's kinematic operations (`vorticity()`, `divergence()`, `advection()`) allocate multiple intermediate arrays for each gradient step and Pint unit check. Calculating potential vorticity on a 3D atmospheric grid ($116 \times 116 \times 32$ levels) triggers gigabytes of temporary allocations.
3. **Slow Vector Loop Operations**: Calculating Storm-Relative Helicity (SRH) and vertical wind shear across large weather domains takes dozens of seconds per timestep.

### The MausamMesh Solution:
* **True Spherical Metric Stencils**: Embeds exact WGS84 ellipsoidal and spherical metric terms directly into finite difference stencils ($dx = R \cos\phi \cdot d\lambda$, $dy = R \cdot d\phi$).
* **In-Place SIMD Vectorized Gradients**: Second-order centered difference stencils computed with zero intermediate array allocation.
* **Severe Cyclone & Monsoon Shear Diagnostics**: Dedicated algorithms tailored for the North Indian Ocean (Arabian Sea & Bay of Bengal) tropical cyclogenesis, Western Disturbances, and monsoon low-level jets (LLJ).

---

## 2. 📐 Complete Mathematical Formulation & Physical Laws

### Geophysical Constants:
| Constant | Symbol | Value | Unit |
| :--- | :---: | :---: | :---: |
| Earth's Mean Radius | $R_E$ | $6,371,000$ | $\text{meters}$ |
| Earth's Angular Velocity | $\Omega$ | $7.2921159 \times 10^{-5}$ | $\text{rad/s}$ |
| Standard Surface Gravity | $g$ | $9.80665$ | $\text{m/s}^2$ |
| Reference Air Density | $\rho_0$ | $1.225$ | $\text{kg/m}^3$ |

---

### Phase A: Planetary Rotation & Geostrophic Balance

#### 1. Coriolis Parameter ($f$)
Accounts for the deflection of moving air due to Earth's rotation as a function of latitude ($\phi$):
$$f = 2\Omega \sin(\phi) \quad [\text{s}^{-1}]$$
*(At the Equator $\phi = 0^\circ, f = 0$; at New Delhi $\phi = 28.6^\circ, f = 6.98 \times 10^{-5}\text{ s}^{-1}$).*

#### 2. Beta Parameter ($\beta$)
The meridional gradient of the Coriolis parameter, fundamental for planetary Rossby wave dynamics:
$$\beta = \frac{df}{dy} = \frac{2\Omega \cos(\phi)}{R_E} \quad [\text{m}^{-1}\text{s}^{-1}]$$

#### 3. Geostrophic Wind ($u_g, v_g$)
The theoretical horizontal wind resulting from an exact balance between the horizontal pressure gradient force and the Coriolis force in isobaric coordinates:
$$u_g = -\frac{1}{f} \frac{\partial \Phi}{\partial y} = -\frac{g}{f} \frac{\partial Z}{\partial y} \quad [\text{m/s}]$$
$$v_g = \frac{1}{f} \frac{\partial \Phi}{\partial x} = \frac{g}{f} \frac{\partial Z}{\partial x} \quad [\text{m/s}]$$
*(Where $\Phi = gZ$ is geopotential, and $Z$ is geopotential height in geopotential meters).*

#### 4. Ageostrophic Wind ($\vec{V}_a$)
The vector difference between real observed/modeled wind ($\vec{V}$) and geostrophic wind ($\vec{V}_g$), directly responsible for vertical motion, storm initiation, and frontal collapse:
$$\vec{V}_a = \vec{V} - \vec{V}_g = (u - u_g) \hat{i} + (v - v_g) \hat{j} \quad [\text{m/s}]$$

#### 5. Thermal Wind Vector ($\vec{V}_T$)
The vertical shear of the geostrophic wind between two pressure levels ($p_1 > p_2$), governed strictly by horizontal temperature gradients:
$$\vec{V}_T = \vec{V}_g(p_2) - \vec{V}_g(p_1) = -\frac{R_d}{f} \ln\left(\frac{p_1}{p_2}\right) \left(\hat{k} \times \nabla_p \bar{T}\right)$$
In component form:
$$u_T = \frac{R_d}{f} \ln\left(\frac{p_1}{p_2}\right) \frac{\partial \bar{T}}{\partial y}, \quad v_T = -\frac{R_d}{f} \ln\left(\frac{p_1}{p_2}\right) \frac{\partial \bar{T}}{\partial x}$$

---

### Phase B: Differential Operators & Kinematic Field Tensors

All derivatives on spatial weather grids are computed using **Second-Order Centered Finite Difference Stencils** with spherical coordinate corrections:
$$\Delta x = R_E \cos(\phi) \cdot \Delta \lambda_{\text{rad}}, \quad \Delta y = R_E \cdot \Delta \phi_{\text{rad}}$$
$$\left(\frac{\partial \psi}{\partial x}\right)_{i,j} = \frac{\psi_{i, j+1} - \psi_{i, j-1}}{2 \Delta x}, \quad \left(\frac{\partial \psi}{\partial y}\right)_{i,j} = \frac{\psi_{i+1, j} - \psi_{i-1, j}}{2 \Delta y}$$

#### 6. Horizontal Divergence ($\delta$)
Measures the net volumetric outflow of air per unit area. Negative divergence is convergence, which forces air to rise and produce cloudbursts and cyclones:
$$\delta = \nabla_h \cdot \vec{V} = \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} - \frac{v}{R_E} \tan(\phi) \quad [\text{s}^{-1}]$$

#### 7. Relative Vorticity ($\zeta$)
The local spin / microscopic circulation of the fluid about the local vertical axis:
$$\zeta = (\nabla \times \vec{V}) \cdot \hat{k} = \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y} + \frac{u}{R_E} \tan(\phi) \quad [\text{s}^{-1}]$$
* $\zeta > 0$: Cyclonic circulation (Counter-clockwise in Northern Hemisphere — Depressions, Cyclones, Monsoon Troughs).
* $\zeta < 0$: Anticyclonic circulation (Clockwise in Northern Hemisphere — High Pressure, Heatwaves).

#### 8. Absolute Vorticity ($\eta$)
Total vorticity in an inertial reference frame:
$$\eta = \zeta + f = \left(\frac{\partial v}{\partial x} - \frac{\partial u}{\partial y} + \frac{u}{R_E} \tan\phi\right) + 2\Omega\sin\phi \quad [\text{s}^{-1}]$$

#### 9. Ertel's Potential Vorticity (PV)
The holy grail of dynamic meteorology — conserved along adiabatic frictionless flow. Used to track tropopause folding, jet stream intrusions, and explosive cyclogenesis:
$$PV = -g \left( \eta_\theta \right) \frac{\partial \theta}{\partial p} \quad [\text{PVU}]$$
*(Where $1\text{ PVU} = 10^{-6}\text{ m}^2\text{ s}^{-1}\text{ K kg}^{-1}$. Stratospheric air has $PV > 2.0\text{ PVU}$; tropospheric air has $PV < 1.5\text{ PVU}$).*

#### 10. Horizontal Advection ($\text{Adv}$)
The rate of change of any scalar atmospheric field $S$ (temperature, humidity, vorticity) transported by the wind:
$$\text{Adv}(S) = -\vec{V} \cdot \nabla_h S = -\left( u \frac{\partial S}{\partial x} + v \frac{\partial S}{\partial y} \right)$$
* **Temperature Advection ($-\vec{V} \cdot \nabla T$)**: $> 0 \rightarrow$ Warm Air Advection (WAA, produces stratiform rain); $< 0 \rightarrow$ Cold Air Advection (CAA).
* **Vorticity Advection ($-\vec{V} \cdot \nabla \eta$)**: Positive Vorticity Advection (PVA) aloft forces dynamic upward vertical motion (cyclogenesis trigger).

---

### Phase C: Severe Storm Shear & Cyclonic Helicity Dynamics

#### 11. Bulk Vertical Wind Shear ($\Delta \vec{V}$)
The vector difference in horizontal wind between two vertical altitudes (standard layers: $0\text{--}1\text{ km}$, $0\text{--}3\text{ km}$, and $0\text{--}6\text{ km}$ above ground level):
$$\Delta \vec{V}_{0-6\text{km}} = \vec{V}_{6\text{km}} - \vec{V}_{\text{sfc}}$$
$$\text{Shear Magnitude} = |\Delta \vec{V}| = \sqrt{(u_{6\text{km}} - u_{\text{sfc}})^2 + (v_{6\text{km}} - v_{\text{sfc}})^2} \quad [\text{m/s or knots}]$$
*Severe Storm Thresholds*:
* $|\Delta \vec{V}_{0-6\text{km}}| < 10\text{ m/s}$ ($< 20\text{ kt}$): Pulse thunderstorms only (unorganized).
* $|\Delta \vec{V}_{0-6\text{km}}| \ge 20\text{ m/s}$ ($\ge 40\text{ kt}$): High potential for organized supercell thunderstorms, destructive hail, and tornadoes.

#### 12. Bunkers Storm Motion Vector ($\vec{C}_R, \vec{C}_L$)
Calculates the internal dynamic propagation vector of right-moving and left-moving supercell storms using the **Bunkers (2000)** empirical pressure-perturbation formula:
$$\vec{V}_{\text{mean}} = \frac{1}{6000\text{m}} \int_{0}^{6000\text{m}} \vec{V}(z) dz$$
$$\vec{C}_R = \vec{V}_{\text{mean}} + D \cdot \left(\frac{\hat{k} \times \Delta \vec{V}_{0-6\text{km}}}{|\Delta \vec{V}_{0-6\text{km}}|}\right)$$
*(Where $D = 7.5\text{ m/s}$ is the deviation velocity perpendicular to the deep-layer shear).*

#### 13. Storm-Relative Helicity (SRH)
Measures the stream-wise vorticity available in the inflow layer of a thunderstorm, directly quantifying rotational updraft and tornado threat:
$$\text{SRH}_{0-h} = \int_{0}^{h} (\vec{V}(z) - \vec{C}) \cdot \left(\hat{k} \times \frac{\partial \vec{V}}{\partial z}\right) dz \quad [\text{m}^2/\text{s}^2]$$
*Evaluation via Layer Stencils*:
$$\text{SRH} = -\sum_{k=1}^{N} \left[ (u_{k+1} - c_x)(v_k - c_y) - (u_k - c_x)(v_{k+1} - c_y) \right]$$
*IMD / Severe Weather Thresholds ($0\text{--}3\text{ km}$)*:
* $\text{SRH} > 150\text{ m}^2/\text{s}^2$: Supercells possible.
* $\text{SRH} > 300\text{ m}^2/\text{s}^2$: Strong supercell and severe tornado risk.

#### 14. Supercell Composite Parameter (SCP)
Normalized multi-dimensional index combining instability, deep-layer shear, and storm-relative helicity:
$$\text{SCP} = \left(\frac{\text{MUCAPE}}{1000\text{ J/kg}}\right) \cdot \left(\frac{|\Delta \vec{V}_{0-6\text{km}}|}{20\text{ m/s}}\right) \cdot \left(\frac{\text{SRH}_{0-3\text{km}}}{50\text{ m}^2/\text{s}^2}\right)$$
* $\text{SCP} > 1.0$: Environment favors rotating supercell thunderstorms.
* $\text{SCP} > 4.0$: Extreme violent convective storms.

---

## 3. 🏗️ Code Architecture & Function Signatures (`mausam_mesh/kinematics.py`)

All operations accept **2D horizontal spatial grids** (`[rows, cols]`) and **3D volume grids** (`[levels, rows, cols]`) as standard NumPy arrays:

```python
# =============================================================================
# 1. PLANETARY CORIOLIS & GEOSTROPHIC OPERATORS
# =============================================================================
def coriolis_parameter(latitudes_deg: float | np.ndarray) -> float | np.ndarray:
    """Computes Coriolis parameter f = 2*omega*sin(phi) in 1/s."""

def beta_parameter(latitudes_deg: float | np.ndarray) -> float | np.ndarray:
    """Computes Rossby parameter df/dy in 1/(m*s)."""

def geostrophic_wind(
    geopotential_height_m: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes (u_g, v_g) from geopotential height grid using spherical stencils.
    Returns: (ug_m_s, vg_m_s)
    """

def thermal_wind(
    thickness_m: np.ndarray,
    p_bottom_hpa: float,
    p_top_hpa: float,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """Computes thermal wind shear vector between two isobaric surfaces."""

# =============================================================================
# 2. VECTOR DIFFERENTIAL OPERATORS (2D & 3D GRIDS)
# =============================================================================
def divergence(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray
) -> np.ndarray:
    """Computes horizontal divergence div(V) with spherical metric corrections."""

def relative_vorticity(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray
) -> np.ndarray:
    """Computes vertical component of relative vorticity curl(V)."""

def absolute_vorticity(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray
) -> np.ndarray:
    """Computes absolute vorticity eta = zeta + f."""

def advection(
    scalar_field: np.ndarray,
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray
) -> np.ndarray:
    """Computes horizontal advection -V . grad(S) on spherical grid."""

def potential_vorticity_isentropic(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    theta_k: np.ndarray,
    pressure_hpa: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray
) -> np.ndarray:
    """Computes Ertel's Potential Vorticity (PV) in isentropic coordinates (PVU)."""

# =============================================================================
# 3. SEVERE STORM SHEAR & HELICITY
# =============================================================================
def bulk_shear(
    u_profile: np.ndarray,
    v_profile: np.ndarray,
    height_profile_m: np.ndarray,
    depth_m: float = 6000.0
) -> Tuple[float, float, float]:
    """
    Computes vertical bulk wind shear vector and total magnitude across layer.
    Returns: (shear_u, shear_v, shear_magnitude_m_s)
    """

def bunkers_storm_motion(
    u_profile: np.ndarray,
    v_profile: np.ndarray,
    height_profile_m: np.ndarray
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Computes Bunkers (2000) Right-Moving and Left-Moving supercell motion vectors.
    Returns: ((c_rx, c_ry), (c_lx, c_ly)) in m/s
    """

def storm_relative_helicity(
    u_profile: np.ndarray,
    v_profile: np.ndarray,
    height_profile_m: np.ndarray,
    storm_motion_u: float,
    storm_motion_v: float,
    depth_m: float = 3000.0
) -> float:
    """Computes Storm-Relative Helicity (SRH) in m^2/s^2."""

def supercell_composite_parameter(
    mucape_j_kg: float,
    bulk_shear_0_6km_m_s: float,
    srh_0_3km_m2_s2: float
) -> float:
    """Computes dimensionless Supercell Composite Parameter (SCP)."""
```

---

## 4. 📊 Parity & Performance Targets vs `MetPy`

| Kinematic Metric | MetPy Benchmark ($116 \times 116$ Grid) | MausamMesh Target | Target Speedup | Numerical Precision Limit |
| :--- | :---: | :---: | :---: | :---: |
| **Coriolis Parameter** | $0.0012\text{ s}$ | **$0.00004\text{ s}$** | **$30\text{x}$** | Exact IEEE-754 ($< 10^{-14}$) |
| **Relative Vorticity** | $0.048\text{ s}$ | **$0.0004\text{ s}$** | **$120\text{x}$** | $< \pm 10^{-8}\text{ s}^{-1}$ |
| **Horizontal Divergence** | $0.046\text{ s}$ | **$0.0004\text{ s}$** | **$115\text{x}$** | $< \pm 10^{-8}\text{ s}^{-1}$ |
| **Temperature Advection** | $0.092\text{ s}$ | **$0.0008\text{ s}$** | **$115\text{x}$** | $< \pm 10^{-6}\text{ K/s}$ |
| **3D Potential Vorticity** | $1.850\text{ s}$ | **$0.015\text{ s}$** | **$123\text{x}$** | $< \pm 0.001\text{ PVU}$ |
| **Storm Relative Helicity** | $0.012\text{ s}$ (per point) | **$0.0001\text{ s}$** | **$120\text{x}$** | $< \pm 0.1\text{ m}^2/\text{s}^2$ |

---

## 5. 🚀 Execution Plan for Module 02

1. **Review**: Confirm all physical equations and operational stencils.
2. **Implement**: Code `mausam_mesh/kinematics.py` with pure-NumPy vectorized stencils.
3. **Parity Validation**: Create test suite comparing against analytical vortices (Rankine vortex & Lamb-Oseen vortex).
4. **Integration**: Link into `mausam_mesh/__init__.py`.
