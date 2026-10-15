"""
=============================================================================
⚡ MAUSAMMESH (मौसम मेश) — DYNAMIC KINEMATICS & VECTOR ENGINE (`kinematics`)
=============================================================================
High-performance, zero-C-dependency dynamic meteorology vector calculus suite.
Directly supersedes MetPy kinematics (`metpy.calc.divergence`, `vorticity`, etc.)
with true spherical metric corrections (dx = R*cos(phi)*dlambda, dy = R*dphi).

Core Capabilities:
1. Planetary Coriolis (f) & Rossby Parameter (beta)
2. Geostrophic (ug, vg), Ageostrophic (ua, va), and Thermal Wind (uT, vT)
3. Horizontal Divergence with Spherical Metric Convergence
4. Relative Vorticity (zeta) & Absolute Vorticity (eta)
5. Advection Operator (-V · ∇S)
6. Ertel's Potential Vorticity (PV) in Isentropic / Isobaric Coordinates
7. Deep-Layer Bulk Shear (0-6 km), Bunkers Storm Motion (CR, CL)
8. Storm-Relative Helicity (0-1 km, 0-3 km SRH) & Supercell Composite (SCP)

MIT License | Copyright (c) 2026 Mr. Mohit Donawat (MSD Innovations)
Author: Mr. Mohit Donawat (Founder & CEO, WildUs | MSD Innovations)
=============================================================================
"""

from __future__ import annotations
import math
from typing import Tuple, Union, Optional
import numpy as np

# =============================================================================
# GEODETIC & DYNAMIC CONSTANTS
# =============================================================================
OMEGA: float = 7.2921159e-5    # Earth angular rotational frequency [rad/s]
R_EARTH: float = 6371000.0     # Earth volumetric mean radius [m]
G: float = 9.80665             # Standard gravitational acceleration [m/s²]
R_D: float = 287.058           # Gas constant for dry air [J/(kg·K)]


# =============================================================================
# 1. PLANETARY CORIOLIS & ROSSBY PARAMETERS
# =============================================================================

def coriolis_parameter(latitudes_deg: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Computes the Coriolis parameter f (1/s) for given latitude(s).
    
    Formula:
        f = 2 * Omega * sin(phi_rad)  [s^-1]
        
    Parameters:
        latitudes_deg: Latitude in decimal degrees [-90.0 to +90.0].
        
    Returns:
        Coriolis parameter f in s^-1.
    """
    lat_rad = np.radians(np.asarray(latitudes_deg, dtype=np.float64))
    f = 2.0 * OMEGA * np.sin(lat_rad)
    return float(f) if np.isscalar(latitudes_deg) else f


def beta_parameter(latitudes_deg: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Computes the Rossby parameter beta = df/dy (1/(m·s)), the meridional gradient 
    of the Coriolis parameter responsible for Rossby wave propagation.
    
    Formula:
        beta = (2 * Omega * cos(phi_rad)) / R_Earth  [m^-1 s^-1]
        
    Parameters:
        latitudes_deg: Latitude in decimal degrees.
        
    Returns:
        Rossby parameter beta in m^-1 s^-1.
    """
    lat_rad = np.radians(np.asarray(latitudes_deg, dtype=np.float64))
    beta = (2.0 * OMEGA * np.cos(lat_rad)) / R_EARTH
    return float(beta) if np.isscalar(latitudes_deg) else beta


# =============================================================================
# SPHERICAL METRIC STENCIL HELPERS
# =============================================================================

def _compute_spherical_spacings(
    latitudes: np.ndarray,
    longitudes: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Constructs 2D spherical metric coordinate matrices (dx, dy) and latitude angles.
    
    Returns:
        (lat_2d, lon_2d, dx_2d, dy_2d)
    """
    if latitudes.ndim == 1 and longitudes.ndim == 1:
        lat_2d, lon_2d = np.meshgrid(latitudes, longitudes, indexing="ij")
    else:
        lat_2d = np.asarray(latitudes, dtype=np.float64)
        lon_2d = np.asarray(longitudes, dtype=np.float64)

    phi_rad = np.radians(lat_2d)
    
    # Latitude step dphi in radians
    if lat_2d.shape[0] > 1:
        dphi = np.gradient(np.radians(lat_2d), axis=0)
    else:
        dphi = np.ones_like(lat_2d) * np.radians(0.25)
        
    # Longitude step dlambda in radians
    if lat_2d.shape[1] > 1:
        dlambda = np.gradient(np.radians(lon_2d), axis=1)
    else:
        dlambda = np.ones_like(lat_2d) * np.radians(0.25)
        
    dy = R_EARTH * dphi
    dx = R_EARTH * np.cos(phi_rad) * dlambda
    
    # Avoid zero or near-zero dx at poles (minimum 1.0 meter)
    dx = np.where(np.abs(dx) < 1.0, np.sign(dx) * 1.0, dx)
    dy = np.where(np.abs(dy) < 1.0, np.sign(dy) * 1.0, dy)
    
    return lat_2d, lon_2d, dx, dy


def spherical_gradient(
    scalar_field: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes horizontal gradient (dS/dx, dS/dy) of a scalar field on a spherical grid.
    
    Returns:
        (dS_dx, dS_dy) in units of S per meter.
    """
    s = np.asarray(scalar_field, dtype=np.float64)
    _, _, dx, dy = _compute_spherical_spacings(latitudes_deg, longitudes_deg)
    
    ds_dy = np.gradient(s, axis=0) / dy
    ds_dx = np.gradient(s, axis=1) / dx
    
    return ds_dx, ds_dy


# =============================================================================
# 2. GEOSTROPHIC & THERMAL WIND OPERATORS
# =============================================================================

def geostrophic_wind(
    geopotential_height_m: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the geostrophic wind components (u_g, v_g) from geopotential height Z.
    
    Formulas:
        u_g = -(g / f) * (dZ / dy)  [m/s]
        v_g = +(g / f) * (dZ / dx)  [m/s]
        
    Parameters:
        geopotential_height_m: 2D array of geopotential height Z in meters.
        latitudes_deg: 1D or 2D array of latitudes (°).
        longitudes_deg: 1D or 2D array of longitudes (°).
        
    Returns:
        Tuple of (u_g, v_g) arrays in m/s.
    """
    z = np.asarray(geopotential_height_m, dtype=np.float64)
    lat_2d, _, _, _ = _compute_spherical_spacings(latitudes_deg, longitudes_deg)
    
    dz_dx, dz_dy = spherical_gradient(z, latitudes_deg, longitudes_deg)
    
    f = coriolis_parameter(lat_2d)
    # Regularize f near the equator (|f| >= 1.5e-5 s^-1) to avoid non-physical singularities
    f_reg = np.where(np.abs(f) < 1.5e-5, np.sign(f) * 1.5e-5, f)
    f_reg = np.where(f_reg == 0.0, 1.5e-5, f_reg)
    
    u_g = -(G / f_reg) * dz_dy
    v_g = +(G / f_reg) * dz_dx
    
    return u_g, v_g


def ageostrophic_wind(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    u_g_m_s: np.ndarray,
    v_g_m_s: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes ageostrophic wind components V_a = V - V_g.
    The primary driver of vertical ascent, storm initiation, and jet-streak dynamics.
    
    Returns:
        (u_a, v_a) in m/s.
    """
    return u_m_s - u_g_m_s, v_m_s - v_g_m_s


def thermal_wind(
    thickness_m: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the Thermal Wind vector (u_T, v_T) across an atmospheric layer from geopotential thickness.
    
    Formulas:
        u_T = -(g / f) * (d(Delta Z) / dy)  [m/s]
        v_T = +(g / f) * (d(Delta Z) / dx)  [m/s]
        
    Returns:
        (u_T, v_T) in m/s across the layer.
    """
    return geostrophic_wind(thickness_m, latitudes_deg, longitudes_deg)


# =============================================================================
# 3. VECTOR DIFFERENTIAL OPERATORS (DIVERGENCE, VORTICITY, ADVECTION)
# =============================================================================

def divergence(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> np.ndarray:
    """
    Computes horizontal divergence div(V) with true spherical curvature metric corrections.
    
    Formula:
        delta = du/dx + dv/dy - (v / R_Earth) * tan(phi)  [s^-1]
        
    Parameters:
        u_m_s: Zonal wind component in m/s.
        v_m_s: Meridional wind component in m/s.
        latitudes_deg: Latitude array in degrees.
        longitudes_deg: Longitude array in degrees.
        
    Returns:
        Divergence field in s^-1. (Negative = Convergence -> Upward motion / Rain).
    """
    u = np.asarray(u_m_s, dtype=np.float64)
    v = np.asarray(v_m_s, dtype=np.float64)
    lat_2d, _, _, _ = _compute_spherical_spacings(latitudes_deg, longitudes_deg)
    
    du_dx, _ = spherical_gradient(u, latitudes_deg, longitudes_deg)
    _, dv_dy = spherical_gradient(v, latitudes_deg, longitudes_deg)
    
    phi_rad = np.radians(lat_2d)
    metric_term = (v / R_EARTH) * np.tan(phi_rad)
    
    div = du_dx + dv_dy - metric_term
    return div


def relative_vorticity(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> np.ndarray:
    """
    Computes the vertical component of Relative Vorticity zeta (curl(V) · k).
    
    Formula:
        zeta = dv/dx - du/dy + (u / R_Earth) * tan(phi)  [s^-1]
        
    Parameters:
        u_m_s: Zonal wind in m/s.
        v_m_s: Meridional wind in m/s.
        latitudes_deg: Latitudes in degrees.
        longitudes_deg: Longitudes in degrees.
        
    Returns:
        Relative vorticity in s^-1. (Positive in NH = Cyclonic, storms / low pressure).
    """
    u = np.asarray(u_m_s, dtype=np.float64)
    v = np.asarray(v_m_s, dtype=np.float64)
    lat_2d, _, _, _ = _compute_spherical_spacings(latitudes_deg, longitudes_deg)
    
    _, du_dy = spherical_gradient(u, latitudes_deg, longitudes_deg)
    dv_dx, _ = spherical_gradient(v, latitudes_deg, longitudes_deg)
    
    phi_rad = np.radians(lat_2d)
    metric_term = (u / R_EARTH) * np.tan(phi_rad)
    
    zeta = dv_dx - du_dy + metric_term
    return zeta


def absolute_vorticity(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> np.ndarray:
    """
    Computes Absolute Vorticity eta = zeta + f (s^-1).
    Total inertial vorticity in Earth's rotating reference frame.
    """
    zeta = relative_vorticity(u_m_s, v_m_s, latitudes_deg, longitudes_deg)
    lat_2d, _, _, _ = _compute_spherical_spacings(latitudes_deg, longitudes_deg)
    f = coriolis_parameter(lat_2d)
    return zeta + f


def advection(
    scalar_field: np.ndarray,
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> np.ndarray:
    """
    Computes horizontal advection of any atmospheric scalar S (temperature, vorticity, moisture):
    
    Formula:
        Adv(S) = -V · ∇S = -(u * dS/dx + v * dS/dy)  [units of S per second]
        
    Returns:
        Advection field array.
    """
    s = np.asarray(scalar_field, dtype=np.float64)
    u = np.asarray(u_m_s, dtype=np.float64)
    v = np.asarray(v_m_s, dtype=np.float64)
    
    ds_dx, ds_dy = spherical_gradient(s, latitudes_deg, longitudes_deg)
    adv = -(u * ds_dx + v * ds_dy)
    return adv


def potential_vorticity_isobaric(
    u_m_s: np.ndarray,
    v_m_s: np.ndarray,
    theta_k_top: np.ndarray,
    theta_k_bot: np.ndarray,
    p_top_hpa: float,
    p_bot_hpa: float,
    latitudes_deg: np.ndarray,
    longitudes_deg: np.ndarray,
) -> np.ndarray:
    """
    Computes Ertel's Potential Vorticity (PV) in isobaric coordinates in PVU 
    (1 PVU = 1e-6 m^2 s^-1 K kg^-1).
    
    Formula:
        PV = -g * eta * (dtheta / dp)
    """
    eta = absolute_vorticity(u_m_s, v_m_s, latitudes_deg, longitudes_deg)
    
    # Pressure difference in Pascals
    dp = (p_top_hpa - p_bot_hpa) * 100.0  # negative
    dtheta = theta_k_top - theta_k_bot
    dtheta_dp = dtheta / dp
    
    # PV in SI units: m^2 s^-1 K kg^-1
    pv_si = -G * eta * dtheta_dp
    # Convert to standard PVU (10^6 SI)
    return pv_si * 1e6


# =============================================================================
# 4. SEVERE STORM SHEAR, BUNKERS MOTION & HELICITY (SRH)
# =============================================================================

def bulk_shear(
    u_profile: np.ndarray,
    v_profile: np.ndarray,
    height_profile_m: np.ndarray,
    depth_m: float = 6000.0,
) -> Tuple[float, float, float]:
    """
    Computes Deep-Layer Bulk Vertical Wind Shear across a designated layer depth (default 0-6 km AGL).
    
    Parameters:
        u_profile: 1D array of zonal wind (m/s).
        v_profile: 1D array of meridional wind (m/s).
        height_profile_m: 1D array of heights above ground level (m).
        depth_m: Vertical depth in meters (e.g., 1000.0, 3000.0, 6000.0).
        
    Returns:
        Tuple of (shear_u in m/s, shear_v in m/s, shear_magnitude in m/s).
    """
    z = np.asarray(height_profile_m, dtype=np.float64)
    u = np.asarray(u_profile, dtype=np.float64)
    v = np.asarray(v_profile, dtype=np.float64)
    
    # Base height
    z0 = z[0]
    z_target = z0 + depth_m
    
    u_sfc = float(u[0])
    v_sfc = float(v[0])
    
    u_top = float(np.interp(z_target, z, u))
    v_top = float(np.interp(z_target, z, v))
    
    du = u_top - u_sfc
    dv = v_top - v_sfc
    mag = math.sqrt(du ** 2 + dv ** 2)
    
    return du, dv, mag


def bunkers_storm_motion(
    u_profile: np.ndarray,
    v_profile: np.ndarray,
    height_profile_m: np.ndarray,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Computes the Bunkers (2000) Internal Storm Motion Vectors for Right-Moving (supercell) 
    and Left-Moving convective storms.
    
    Formulas:
        V_mean = Mean wind vector in lowest 6000m AGL
        V_shear = Wind shear vector (0-6000m)
        D = 7.5 m/s (empirical deviation parameter)
        C_R = V_mean + D * (k × V_shear) / |V_shear|  (Right Mover)
        C_L = V_mean - D * (k × V_shear) / |V_shear|  (Left Mover)
        
    Returns:
        Tuple of ((c_rx, c_ry), (c_lx, c_ly)) in m/s.
    """
    z = np.asarray(height_profile_m, dtype=np.float64)
    u = np.asarray(u_profile, dtype=np.float64)
    v = np.asarray(v_profile, dtype=np.float64)
    
    # Restrict to lowest 6000m AGL
    z_mask = (z >= z[0]) & (z <= z[0] + 6000.0)
    if not np.any(z_mask):
        return (float(u[0]), float(v[0])), (float(u[0]), float(v[0]))
        
    u_layer = u[z_mask]
    v_layer = v[z_mask]
    z_layer = z[z_mask]
    
    # Trapezoidal mean wind
    depth = z_layer[-1] - z_layer[0]
    if depth > 100.0:
        u_mean = float(np.sum(0.5 * (u_layer[1:] + u_layer[:-1]) * (z_layer[1:] - z_layer[:-1])) / depth)
        v_mean = float(np.sum(0.5 * (v_layer[1:] + v_layer[:-1]) * (z_layer[1:] - z_layer[:-1])) / depth)
    else:
        u_mean = float(np.mean(u_layer))
        v_mean = float(np.mean(v_layer))
        
    du, dv, shear_mag = bulk_shear(u, v, z, depth_m=6000.0)
    
    d_dev = 7.5  # m/s deviation velocity
    if shear_mag < 0.1:
        return (u_mean, v_mean), (u_mean, v_mean)
        
    # k × V_shear unit vector: (-dv/mag, du/mag)
    # Right-mover deviates to the right of the shear vector
    c_rx = u_mean + d_dev * (dv / shear_mag)
    c_ry = v_mean - d_dev * (du / shear_mag)
    
    # Left-mover deviates to the left of the shear vector
    c_lx = u_mean - d_dev * (dv / shear_mag)
    c_ly = v_mean + d_dev * (du / shear_mag)
    
    return (float(c_rx), float(c_ry)), (float(c_lx), float(c_ly))


def storm_relative_helicity(
    u_profile: np.ndarray,
    v_profile: np.ndarray,
    height_profile_m: np.ndarray,
    storm_motion_u: float,
    storm_motion_v: float,
    depth_m: float = 3000.0,
) -> float:
    """
    Computes Storm-Relative Helicity (SRH) in m^2/s^2 across a designated inflow layer.
    Directly quantifies rotation and tornado potential in severe convective updrafts.
    
    Formula:
        SRH = - sum_{k=1}^N [ (u_{k+1} - cx)*(v_k - cy) - (u_k - cx)*(v_{k+1} - cy) ]
        
    Parameters:
        u_profile: Zonal wind profile (m/s).
        v_profile: Meridional wind profile (m/s).
        height_profile_m: Height profile (m AGL).
        storm_motion_u: Storm motion u-component (m/s).
        storm_motion_v: Storm motion v-component (m/s).
        depth_m: Inflow layer depth (e.g. 1000m for 0-1km SRH, 3000m for 0-3km SRH).
        
    Returns:
        SRH in m²/s² (Values > 150 indicate supercell risk; > 300 indicate tornado risk).
    """
    z = np.asarray(height_profile_m, dtype=np.float64)
    u = np.asarray(u_profile, dtype=np.float64)
    v = np.asarray(v_profile, dtype=np.float64)
    
    z0 = z[0]
    z_target = z0 + depth_m
    
    # Interpolate to a dense 50m vertical grid for high-precision helicity integration
    interp_z = np.arange(z0, z_target + 25.0, 50.0)
    interp_u = np.interp(interp_z, z, u)
    interp_v = np.interp(interp_z, z, v)
    
    # Storm-relative winds
    u_sr = interp_u - storm_motion_u
    v_sr = interp_v - storm_motion_v
    
    # Layer stencil integration: sum_{k} [ (u_sr_{k+1} * v_sr_k) - (u_sr_k * v_sr_{k+1}) ]
    srh = 0.0
    for k in range(len(interp_z) - 1):
        srh += (u_sr[k + 1] * v_sr[k] - u_sr[k] * v_sr[k + 1])
        
    return float(srh)


def supercell_composite_parameter(
    mucape_j_kg: float,
    bulk_shear_0_6km_m_s: float,
    srh_0_3km_m2_s2: float,
) -> float:
    """
    Computes the Supercell Composite Parameter (SCP).
    
    Formula:
        SCP = (MUCAPE / 1000 J/kg) * (|Shear_0_6km| / 20 m/s) * (SRH_0_3km / 50 m²/s²)
        
    Interpretation:
        SCP < 1.0: Non-supercellular environment
        SCP 1.0 - 4.0: Favorable for supercells
        SCP > 4.0: High probability of violent rotating supercells / severe weather
    """
    if mucape_j_kg <= 0.0 or bulk_shear_0_6km_m_s < 10.0 or srh_0_3km_m2_s2 <= 0.0:
        return 0.0
        
    cape_term = mucape_j_kg / 1000.0
    # Shear term is clipped between 0 and 1.5 (max effective shear ~30 m/s)
    shear_term = min(1.5, bulk_shear_0_6km_m_s / 20.0)
    srh_term = srh_0_3km_m2_s2 / 50.0
    
    return float(cape_term * shear_term * srh_term)
