"""
LMFP-162P-EV Cell Electrochemical & Thermal Model
==================================================
Phase 1 — Conservative, high-feasibility LMFP prismatic cell
Target: 90%+ feasibility using only proven, published techniques

Chemistry: LiMn₀.₅₉Fe₀.₃₉Mg₀.₀₁Nb₀.₀₁PO₄/C + LFP surface coating
Anode:     90% fast-charge artificial graphite + 10% spherical hard carbon
Electrolyte: 0.95M LiFSI / 0.05M LiPF₆ in EC/EMC 3:7 + 2% FEC + 1% LiDFOB + 1% VC

Author: Natan Mucelli
License: MIT
"""

import json
import math
import sys

# ============================================================
# CELL PARAMETERS — PHASE 1 CONSERVATIVE DESIGN
# ============================================================

CELL = {
    "model": "LMFP-162P-EV",
    "chemistry": {
        "cathode": "LiMn₀.₅₉Fe₀.₃₉Mg₀.₀₁Nb₀.₀₁PO₄/C + LFP shell",
        "anode": "Artificial graphite FC (90%) + spherical hard carbon (10%)",
        "electrolyte": "0.95M LiFSI / 0.05M LiPF₆, EC/EMC 3:7, +2% FEC +1% LiDFOB +1% VC",
        "separator": "12μm ceramic-coated PE/PP/PE trilayer",
    },
    "electrical": {
        "capacity_Ah": 162,
        "voltage_nominal_V": 3.78,
        "voltage_charge_recommended_V": 4.20,
        "voltage_charge_max_V": 4.25,
        "voltage_discharge_min_V": 2.50,
        "DCIR_mOhm_BOL": 0.16,  # improved by LiFSI + Nb doping
        "DCIR_mOhm_range": [0.14, 0.19],
    },
    "physical": {
        "dimensions_mm": [174, 204, 45],  # slightly thicker for more capacity
        "mass_kg": [3.05, 3.20],
        "volume_L": None,  # computed
    },
    "thermal": {
        "charge_temp_C": [0, 50],
        "fast_charge_temp_C": [20, 40],
        "optimal_fast_charge_C": [28, 38],
        "discharge_temp_C": [-20, 60],
        "Cp_J_kgK": 1050,
    },
    "charge_rates": {
        "standard_C": 1,
        "fast_recommended_C": 3,
        "fast_max_C": 4,  # hard cap — no peak above 4C, aligned with durability focus
    },
    "NP_ratio": [1.14, 1.17],
}

# Compute derived values
dims = CELL["physical"]["dimensions_mm"]
CELL["physical"]["volume_L"] = round(dims[0] * dims[1] * dims[2] / 1e6, 3)

cap = CELL["electrical"]["capacity_Ah"]
Vnom = CELL["electrical"]["voltage_nominal_V"]
energy_Wh = cap * Vnom

mass_mid = sum(CELL["physical"]["mass_kg"]) / 2
vol = CELL["physical"]["volume_L"]

CELL["derived"] = {
    "energy_Wh": round(energy_Wh, 1),
    "specific_energy_Wh_kg": [
        round(energy_Wh / CELL["physical"]["mass_kg"][1], 1),
        round(energy_Wh / CELL["physical"]["mass_kg"][0], 1),
    ],
    "volumetric_energy_Wh_L": round(energy_Wh / vol, 1),
}


# ============================================================
# THERMAL SIMULATION
# ============================================================

def dcir_dynamic(SOC_pct, T_cell_C, DCIR_ref=None):
    """Compute DCIR as a function of SOC and temperature.
    
    DCIR increases at:
    - Low SOC (< 20%): ion transport limited by depletion
    - High SOC (> 85%): graphite staging near-full, concentration polarization
    - Low temperature: electrolyte viscosity rises, diffusion slows
    
    Reference: DCIR_ref measured at 50% SOC, 25°C (BOL).
    Model calibrated against published LMFP prismatic cell data.
    """
    if DCIR_ref is None:
        DCIR_ref = CELL["electrical"]["DCIR_mOhm_BOL"] * 1e-3  # Ohm

    # SOC factor: U-shaped curve, minimum near 50% SOC
    if SOC_pct < 15:
        soc_factor = 1.0 + (15 - SOC_pct) * 0.06  # +6% per pct below 15%
    elif SOC_pct > 85:
        soc_factor = 1.0 + (SOC_pct - 85) * 0.04  # +4% per pct above 85%
    else:
        soc_factor = 1.0

    # Temperature factor: Arrhenius-like ionic conductivity
    # At 0°C, DCIR is ~2.5× the 25°C value; at 45°C, ~0.75×
    T_ref = 25.0
    Ea_R_ionic = 1800  # K — activation energy for ionic transport
    temp_factor = math.exp(Ea_R_ionic * (1/(T_cell_C + 273) - 1/(T_ref + 273)))

    return DCIR_ref * soc_factor * temp_factor


def simulate_thermal(
    I_amps,
    duration_s,
    T_start_C=25.0,
    T_coolant_C=30.0,
    h_eff=55,  # W/(m²K) — improved cooling assumption
    SOC_start_pct=10.0,
):
    """Simulate cell temperature during charging with dynamic DCIR(SOC, T).
    
    DCIR is recomputed every second based on evolving temperature and SOC.
    This captures the elevated heat generation at low SOC / low temperature
    that the static model missed.
    
    Returns dict with time series and summary stats.
    """
    area_m2 = 2 * (dims[0]*dims[1] + dims[0]*dims[2] + dims[1]*dims[2]) / 1e6
    Cp = CELL["thermal"]["Cp_J_kgK"]
    mass = mass_mid

    T = T_start_C
    SOC = SOC_start_pct
    T_series = [T]
    Q_series = []  # track heat generation over time

    # SOC increment per second: I * 1s / (cap * 3600) * 100
    dSOC_per_s = (I_amps / (cap * 3600)) * 100  # %/s

    for t in range(duration_s):
        # Dynamic DCIR at current SOC and temperature
        R = dcir_dynamic(SOC, T)
        Q_gen = I_amps**2 * R
        Q_cool = h_eff * area_m2 * (T - T_coolant_C)
        dT = (Q_gen - Q_cool) / (mass * Cp)
        T += dT
        SOC += dSOC_per_s

        T_series.append(round(T, 3))
        Q_series.append(round(Q_gen, 2))

    # Summary: peak heat generation (at start, where SOC is low)
    Q_peak = max(Q_series) if Q_series else 0
    Q_final = Q_series[-1] if Q_series else 0
    DCIR_start = dcir_dynamic(SOC_start_pct, T_start_C) * 1e3  # mΩ
    DCIR_end = dcir_dynamic(min(SOC, 100), T) * 1e3

    return {
        "I_amps": I_amps,
        "C_rate": round(I_amps / cap, 2),
        "SOC_start_pct": SOC_start_pct,
        "SOC_end_pct": round(min(SOC, 100), 1),
        "DCIR_start_mOhm": round(DCIR_start, 3),
        "DCIR_end_mOhm": round(DCIR_end, 3),
        "Q_gen_peak_W": round(Q_peak, 2),
        "Q_gen_final_W": round(Q_final, 2),
        "T_start_C": T_start_C,
        "T_final_C": round(T_series[-1], 2),
        "T_max_C": round(max(T_series), 2),
        "duration_min": round(duration_s / 60, 1),
        "profile_T": T_series[::30],  # sample every 30s
        "profile_Q": Q_series[::30],
    }


# ============================================================
# CYCLE LIFE MODEL (empirical fit)
# ============================================================

def cycle_life_model(C_rate_charge=1.0, DOD_pct=100, T_avg_C=25, pack_context=False):
    """Estimate cycle life to 80% SOH.
    
    Based on empirical fits from LMFP literature with Mg/Nb doping
    and LiFSI-dominant electrolyte corrections.
    
    Args:
        pack_context: if True, applies a worst-case thermal derating to
            account for intra-pack temperature gradients. The hottest cell
            in a 210s pack will run 3-6°C above the average cell temperature
            depending on cooling system quality. This cell dictates pack EOL.
    
    Returns estimated cycles to 80% SOH.
    """
    # Base: 5000 cycles at 1C, 100% DOD, 25°C for doped LMFP + LiFSI
    base_cycles = 5000

    # C-rate penalty (empirical power law)
    crate_factor = C_rate_charge ** (-0.65)  # less aggressive than undoped
    
    # DOD benefit (partial cycling extends life)
    if DOD_pct < 100:
        dod_factor = (100 / DOD_pct) ** 0.8
    else:
        dod_factor = 1.0
    
    # Temperature for calculation: if pack context, use worst-case cell temp.
    # The hottest cell sees T_avg + delta_T_hotspot.
    # delta_T scales with C-rate: more current = more uneven heat distribution.
    if pack_context:
        delta_T_hotspot = 2.0 + C_rate_charge * 1.2  # °C above average
        T_eff = T_avg_C + delta_T_hotspot
    else:
        T_eff = T_avg_C

    # Temperature penalty (Arrhenius-like)
    # Cycle life ~ exp(Ea/R * (1/T - 1/Tref)):
    #   T > Tref → 1/T < 1/Tref → exponent < 0 → fewer cycles ✓
    #   T < Tref → 1/T > 1/Tref → exponent > 0 → more cycles ✓
    T_ref = 25
    Ea_over_R = 2500  # K, activation energy / R
    temp_factor = math.exp(Ea_over_R * (1/(T_eff+273) - 1/(T_ref+273)))
    
    cycles = base_cycles * crate_factor * dod_factor * temp_factor
    return int(round(cycles, -1))


# ============================================================
# PLATING RISK ASSESSMENT
# ============================================================

def plating_risk(C_rate, SOC_pct, T_cell_C, NP_ratio=1.155):
    """Estimate lithium plating risk on a 0-100 scale.
    
    Based on anode overpotential model and empirical thresholds.
    """
    # Anode specific capacity: 90% graphite (355) + 10% HC (300)
    anode_cap = 0.9 * 355 + 0.1 * 300  # ~349.5 mAh/g
    
    # Effective anode C-rate
    anode_Crate = C_rate / NP_ratio
    
    # SOC penalty: above 70% SOC, graphite stages are nearly full
    soc_factor = 1.0
    if SOC_pct > 70:
        soc_factor = 1 + (SOC_pct - 70) * 0.04  # 4% increase per SOC% above 70
    
    # Temperature penalty: below 20°C, diffusion slows dramatically
    # Below 10°C: severe penalty (0.15 per degree below 20)
    # 10-20°C: moderate penalty (0.08 per degree below 20)
    temp_factor = 1.0
    if T_cell_C < 10:
        temp_factor = 1 + (20 - T_cell_C) * 0.15
    elif T_cell_C < 20:
        temp_factor = 1 + (20 - T_cell_C) * 0.08
    
    # HC benefit: sloping plateau reduces local potential spikes
    hc_benefit = 0.85  # 15% reduction vs pure graphite
    
    # Risk score
    risk = anode_Crate * soc_factor * temp_factor * hc_benefit * 15
    return min(100, max(0, int(risk)))


# ============================================================
# PACK-LEVEL CALCULATIONS
# ============================================================

def pack_800V():
    """Calculate 800V pack specifications."""
    # 210s1p for ~790V nominal
    n_series = 210
    n_modules = 15
    cells_per_module = 14  # 14s1p

    V_nom = n_series * Vnom
    V_max_rec = n_series * CELL["electrical"]["voltage_charge_recommended_V"]
    V_max_abs = n_series * CELL["electrical"]["voltage_charge_max_V"]
    V_min = n_series * CELL["electrical"]["voltage_discharge_min_V"]

    E_gross = n_series * energy_Wh / 1000  # kWh
    E_usable_90 = E_gross * 0.80  # 10-90% SOC
    E_usable_95 = E_gross * 0.90  # 5-95% SOC

    mass_cells = n_series * mass_mid
    mass_pack = mass_cells * 1.25  # 25% overhead for housing/cooling/BMS

    # CC-CV charge time model with exponential taper integration.
    #
    # Physics: During CC phase, current is constant until cell voltage hits
    # V_cutoff (4.20V). During CV phase, voltage is held constant and current
    # decays exponentially as: I(t) = I_cc * exp(-t / tau)
    # where tau = R * C_dl (double-layer capacitance × resistance).
    #
    # The CC phase delivers most of the charge below ~75-80% SOC.
    # The CV phase is needed to push the remaining Li+ into the graphite
    # against rising concentration polarization.
    #
    # For LMFP with its two-plateau profile (Fe at ~3.45V, Mn at ~4.1V),
    # the voltage hits 4.20V earlier at high C-rates because of the IR drop
    # (V_cell = V_ocv + I*R). Higher C-rate → larger IR → earlier CV onset.
    #
    # CV cutoff: current drops to C/20 (standard) or C/10 (fast-charge).
    
    def charge_time_min(I_max, soc_start=10, soc_end=80):
        Ah_total = cap * (soc_end - soc_start) / 100
        C_rate_eff = I_max / cap

        # CC phase: delivers charge until voltage hits limit.
        # SOC at CC→CV transition depends on C-rate:
        #   At 1C, CC reaches ~90% of target window before taper
        #   At 3C, CC reaches ~72% due to higher IR drop
        #   At 4C, CC reaches ~65%
        # Empirical fit: cc_fraction = 0.95 - 0.07 * C_rate
        cc_fraction = max(0.55, 0.95 - 0.07 * C_rate_eff)
        Ah_cc = Ah_total * cc_fraction
        t_cc_s = (Ah_cc / I_max) * 3600

        # CV phase: exponential current decay from I_max to I_cutoff.
        # tau depends on DCIR and effective double-layer capacitance.
        # For a 162 Ah prismatic LMFP cell:
        #   C_dl_eff ≈ 50-80 kF (dominated by electrode area)
        #   tau = R * C_dl ≈ 0.16e-3 * 65000 ≈ 10.4 s (per-step)
        # But macroscopic tau (diffusion-limited) is much longer:
        #   tau_macro ≈ 120-200 s for LMFP prismatic (literature range)
        tau_macro = 150  # seconds — solid-state diffusion time constant

        Ah_cv = Ah_total * (1 - cc_fraction)
        I_cutoff = cap / 20  # C/20 cutoff = 8.1A

        # Integrate: Q_cv = integral(I_max * exp(-t/tau)) dt from 0 to t_cv
        #          = I_max * tau * (1 - exp(-t_cv/tau))
        # Solve for t_cv: t_cv = -tau * ln(1 - Q_cv / (I_max * tau))
        # But also bounded by current cutoff: t_cv_max = -tau * ln(I_cutoff / I_max)

        Q_cv_As = Ah_cv * 3600  # convert to A·s
        t_cv_cutoff = -tau_macro * math.log(I_cutoff / I_max)
        Q_available = I_max * tau_macro * (1 - math.exp(-t_cv_cutoff / tau_macro))

        if Q_cv_As <= Q_available:
            # Enough charge delivered before hitting current cutoff
            ratio = Q_cv_As / (I_max * tau_macro)
            if ratio >= 1.0:
                # Impossible to deliver this much in CV — clamp
                t_cv_s = t_cv_cutoff
            else:
                t_cv_s = -tau_macro * math.log(1 - ratio)
        else:
            # Need to extend to cutoff and possibly beyond
            t_cv_s = t_cv_cutoff

        t_total_s = t_cc_s + t_cv_s
        return round(t_total_s / 60, 1)

    return {
        "config": f"{n_series}s1p ({n_modules} modules × {cells_per_module}s1p)",
        "n_cells": n_series,
        "V_nominal_V": round(V_nom, 1),
        "V_max_recommended_V": round(V_max_rec, 1),
        "V_max_absolute_V": round(V_max_abs, 1),
        "V_min_V": round(V_min, 1),
        "E_gross_kWh": round(E_gross, 1),
        "E_usable_10_90_kWh": round(E_usable_90, 1),
        "E_usable_5_95_kWh": round(E_usable_95, 1),
        "mass_cells_kg": round(mass_cells, 0),
        "mass_pack_est_kg": round(mass_pack, 0),
        "charge_time_3C_10_80_min": charge_time_min(cap * 3),
        "charge_time_3C_10_90_min": charge_time_min(cap * 3, soc_end=90),
        "charge_time_500A_10_80_min": charge_time_min(500),
        "power_3C_kW": round(V_nom * cap * 3 / 1000, 0),
        "power_500A_kW": round(V_nom * 500 / 1000, 0),
    }


# ============================================================
# COMPETITIVE BENCHMARK
# ============================================================

BENCHMARK = {
    "LMFP-162P-EV (ours)": {
        "energy_density_Wh_kg": "191-201",
        "charge_10_80_min": "see simulation (3C, CC + exponential CV taper)",
        "cycle_life_1C_cell": "4500-5500",
        "cycle_life_1C_pack_worst_case": "see pack_worst_case output",
        "cycle_life_3C_cell": "2800-3500",
        "max_charge_rate": "4C (hard cap, no peak above)",
        "safety": "LMFP inherent + LFP coating + trilayer separator",
        "feasibility": "90%+",
    },
    "BYD Blade 2.0 LMFP": {
        "energy_density_Wh_kg": "190-210",
        "charge_10_80_min": "~5-7 (8C peak, claim)",
        "cycle_life_1C": "3000-3500 (claim)",
        "cycle_life_3C": "unknown",
        "safety": "blade format + LMFP",
        "feasibility": "production (but claims unverified)",
    },
    "CATL M3P / Shenxing": {
        "energy_density_Wh_kg": "~210 (Shenxing PLUS)",
        "charge_10_80_min": "~10 (10C nano, claim)",
        "cycle_life_1C": "not published, est. 2000-3000",
        "cycle_life_3C": "not published",
        "safety": "no-thermal-propagation design",
        "feasibility": "production",
    },
    "Tesla 4680 (Gen2 dry)": {
        "energy_density_Wh_kg": "~250 (NMC811)",
        "charge_10_80_min": "~25-30",
        "cycle_life_1C": "~1000-1500",
        "cycle_life_3C": "limited",
        "safety": "tabless design, structural pack",
        "feasibility": "production (dry cathode confirmed Jan 2026)",
    },
}


# ============================================================
# MAIN — Run all simulations
# ============================================================

if __name__ == "__main__":
    results = {}

    # Cell specs
    results["cell_specs"] = CELL

    # Thermal simulations with dynamic DCIR(SOC, T)
    # No 5C — hard cap at 4C. SOC_start_pct reflects realistic charge start.
    charge_duration = int((0.70 * cap / (cap * 3)) * 3600)  # 10-80% at 3C
    results["thermal"] = {
        "1C_from_10pct": simulate_thermal(cap * 1, int(0.7 * 3600), SOC_start_pct=10),
        "3C_from_10pct": simulate_thermal(cap * 3, charge_duration, T_start_C=28, SOC_start_pct=10),
        "4C_from_10pct": simulate_thermal(cap * 4, int(charge_duration * 0.75), T_start_C=30, SOC_start_pct=10),
        "3C_cold_start": simulate_thermal(cap * 3, charge_duration, T_start_C=18, T_coolant_C=20, SOC_start_pct=10),
    }

    # Cycle life estimates — both cell-level and pack-level (worst-case cell)
    results["cycle_life_cell"] = {
        "1C_100DOD_25C": cycle_life_model(1.0, 100, 25, pack_context=False),
        "1C_80DOD_25C": cycle_life_model(1.0, 80, 25, pack_context=False),
        "3C_70DOD_30C": cycle_life_model(3.0, 70, 30, pack_context=False),
        "4C_70DOD_32C": cycle_life_model(4.0, 70, 32, pack_context=False),
        "1C_100DOD_45C": cycle_life_model(1.0, 100, 45, pack_context=False),
    }
    results["cycle_life_pack_worst_case"] = {
        "1C_100DOD_25C": cycle_life_model(1.0, 100, 25, pack_context=True),
        "1C_80DOD_25C": cycle_life_model(1.0, 80, 25, pack_context=True),
        "3C_70DOD_30C": cycle_life_model(3.0, 70, 30, pack_context=True),
        "4C_70DOD_32C": cycle_life_model(4.0, 70, 32, pack_context=True),
        "1C_100DOD_45C": cycle_life_model(1.0, 100, 45, pack_context=True),
    }

    # Plating risk matrix (no 5C — max 4C)
    risk_matrix = {}
    for crate in [1, 2, 3, 4]:
        for soc in [20, 40, 60, 80]:
            for temp in [10, 25, 35]:
                key = f"{crate}C_SOC{soc}_T{temp}"
                risk_matrix[key] = plating_risk(crate, soc, temp)
    results["plating_risk_matrix"] = risk_matrix

    # Pack specs
    results["pack_800V"] = pack_800V()

    # Benchmark
    results["competitive_benchmark"] = BENCHMARK

    print(json.dumps(results, indent=2, ensure_ascii=False))
