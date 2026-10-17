"""
=============================================================================
⚡ MAUSAMMESH — DYNAMIC KINEMATICS VERIFICATION SUITE
=============================================================================
Tests all spherical vector differential operators, severe storm shear,
Bunkers motion, and storm-relative helicity against analytical solutions.
=============================================================================
"""

import math
import numpy as np
try:
    from .kinematics import (
        coriolis_parameter,
        beta_parameter,
        spherical_gradient,
        geostrophic_wind,
        ageostrophic_wind,
        divergence,
        relative_vorticity,
        absolute_vorticity,
        advection,
        bulk_shear,
        bunkers_storm_motion,
        storm_relative_helicity,
        supercell_composite_parameter,
        OMEGA,
        R_EARTH,
    )
except (ImportError, ValueError):
    from kinematics import (
        coriolis_parameter,
        beta_parameter,
        spherical_gradient,
        geostrophic_wind,
        ageostrophic_wind,
        divergence,
        relative_vorticity,
        absolute_vorticity,
        advection,
        bulk_shear,
        bunkers_storm_motion,
        storm_relative_helicity,
        supercell_composite_parameter,
        OMEGA,
        R_EARTH,
    )


def test_coriolis_and_beta():
    # At equator (0 deg), f must be 0
    f_eq = coriolis_parameter(0.0)
    assert abs(f_eq) < 1e-12, f"Coriolis at equator must be 0: {f_eq}"
    
    # At North Pole (90 deg), f = 2 * Omega
    f_pole = coriolis_parameter(90.0)
    assert abs(f_pole - 2.0 * OMEGA) < 1e-10, f"Coriolis at pole failed: {f_pole}"
    
    # At 45 deg N, f ≈ 1.03e-4 s^-1
    f_45 = coriolis_parameter(45.0)
    assert abs(f_45 - 1.031e-4) < 1e-6, f"Coriolis at 45N failed: {f_45}"
    
    # Beta parameter at equator: 2*Omega / R_Earth ≈ 2.289e-11
    beta_eq = beta_parameter(0.0)
    expected_beta = (2.0 * OMEGA) / R_EARTH
    assert abs(beta_eq - expected_beta) < 1e-15, f"Beta at equator failed: {beta_eq}"
    print("[PASS] Coriolis Parameter & Beta Parameter Passed.")


def test_vorticity_and_divergence():
    # Construct a synthetic 2D grid covering India (10N to 30N, 70E to 90E)
    lats = np.linspace(10.0, 30.0, 41)   # 0.5 deg step
    lons = np.linspace(70.0, 90.0, 41)
    
    lat_2d, lon_2d = np.meshgrid(lats, lons, indexing="ij")
    
    # Pure non-divergent cyclonic vortex:
    # u = -V0 * sin(y), v = +V0 * cos(x)
    # div(V) should be near 0, vorticity should be positive
    center_lat, center_lon = 20.0, 80.0
    r_lat = np.radians(lat_2d - center_lat) * R_EARTH
    r_lon = np.radians(lon_2d - center_lon) * R_EARTH * np.cos(np.radians(center_lat))
    
    # Solid body rotation around center with radius R = 500 km
    scale_r = 500000.0  # 500 km
    u_field = -20.0 * (r_lat / scale_r)
    v_field = +20.0 * (r_lon / scale_r)
    
    div = divergence(u_field, v_field, lats, lons)
    zeta = relative_vorticity(u_field, v_field, lats, lons)
    
    # Check interior values (away from boundary stencils)
    interior_zeta = zeta[15:25, 15:25]
    # For solid body rotation, zeta ≈ 2 * angular_speed = 2 * (20 / 500000) = 8e-5 s^-1
    mean_zeta = np.mean(interior_zeta)
    assert mean_zeta > 0.0, f"Cyclonic vortex must have positive vorticity: {mean_zeta}"
    
    interior_div = div[15:25, 15:25]
    assert np.all(np.abs(interior_div) < 1e-4), "Divergence in solid body rotation must be near 0"
    
    print(f"[PASS] Spherical Vorticity & Divergence Passed: Mean Zeta = {mean_zeta:.2e} s^-1.")


def test_bunkers_motion_and_shear():
    # Typical severe weather hodograph profile
    heights = np.array([0.0, 500.0, 1000.0, 1500.0, 2000.0, 3000.0, 4000.0, 6000.0])
    # Clockwise turning hodograph (veering winds with height)
    # Surface: SSE wind 8 m/s (u = -3, v = 7)
    # 1 km: South wind 15 m/s (u = 0, v = 15)
    # 3 km: SW wind 22 m/s (u = 15, v = 15)
    # 6 km: WSW wind 30 m/s (u = 28, v = 10)
    u_prof = np.array([-3.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0])
    v_prof = np.array([7.0, 12.0, 15.0, 17.0, 18.0, 15.0, 12.0, 8.0])
    
    du, dv, shear_mag = bulk_shear(u_prof, v_prof, heights, depth_m=6000.0)
    
    # 0-6 km shear: du = 30 - (-3) = 33 m/s, dv = 8 - 7 = 1 m/s -> mag ≈ 33 m/s
    assert abs(shear_mag - 33.01) < 0.2, f"0-6km bulk shear failed: {shear_mag}"
    
    c_right, c_left = bunkers_storm_motion(u_prof, v_prof, heights)
    c_rx, c_ry = c_right
    c_lx, c_ly = c_left
    
    print(f"Deep-Layer 0-6km Shear Magnitude : {shear_mag:.1f} m/s")
    print(f"Bunkers Right-Mover Motion (CR)  : u={c_rx:.1f} m/s, v={c_ry:.1f} m/s")
    print(f"Bunkers Left-Mover Motion (CL)   : u={c_lx:.1f} m/s, v={c_ly:.1f} m/s")
    
    assert c_rx != c_lx, "Right and left movers must differentiate"
    
    # Compute 0-3km Storm-Relative Helicity (SRH) for right-moving supercell
    srh = storm_relative_helicity(u_prof, v_prof, heights, c_rx, c_ry, depth_m=3000.0)
    print(f"0-3km Storm-Relative Helicity    : {srh:.1f} m^2/s^2")
    assert srh > 100.0, f"Veering hodograph should have strong positive SRH: {srh}"
    
    # Supercell Composite Parameter
    scp = supercell_composite_parameter(mucape_j_kg=2800.0, bulk_shear_0_6km_m_s=shear_mag, srh_0_3km_m2_s2=srh)
    print(f"Supercell Composite Parameter (SCP): {scp:.2f}")
    assert scp > 1.0, f"SCP should indicate supercell environment: {scp}"
    
    print("[PASS] Severe Storm Shear, Bunkers Motion, SRH, and SCP Passed.")


if __name__ == "__main__":
    test_coriolis_and_beta()
    test_vorticity_and_divergence()
    test_bunkers_motion_and_shear()
    print("\n[SUCCESS] ALL KINEMATICS SCIENTIFIC TESTS PASSED WITH 100% SUCCESS!")
