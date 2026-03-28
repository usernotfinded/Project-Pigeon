# PRELIMINARY INDUSTRIAL DATASHEET
## LMFP-162P-EV
### High-Durability Prismatic LMFP Cell for 800V Fast-Charge Packs

**Revision**: 1.2 — March 2026  
**Status**: Preliminary (simulation-validated, pre-prototype)  
**Changelog v1.2**: Replaced static DCIR with dynamic DCIR(SOC, T) model; replaced linear CC-CV factor with exponential taper integration; added DCIR operating conditions table. Prior fixes (v1.1): Arrhenius sign, pack derating, 5C removal, plating risk.

---

## 1. Product overview

| Item | Specification |
|---|---|
| Model | LMFP-162P-EV |
| Chemistry | LiMn₀.₅₉Fe₀.₃₉Mg₀.₀₁Nb₀.₀₁PO₄/C + LFP coating // Graphite-HC |
| Cell format | Aluminum prismatic |
| Design objective | Maximum cycle life at practical fast-charge rates |
| Recommended use | BEV fleets, LCV, industrial traction, high-power ESS |
| Pack compatibility | 400V / 800V architectures |

---

## 2. Electrical characteristics

| Parameter | Value | Condition |
|---|---|---|
| Nominal capacity | 162 Ah | 0.33C, 25°C |
| Nominal voltage | 3.78 V | BOL |
| Cell energy | 612.4 Wh | Calculated |
| Recommended charge voltage | 4.20 V | CC-CV |
| Absolute max charge voltage | 4.25 V | BMS hard limit |
| Discharge cut-off voltage | 2.50 V | Standard |
| Standard charge current | 162 A (1C) | 25°C |
| Recommended fast charge | 486 A (3C) | Active cooling |
| Maximum fast charge | 648 A (4C) | 28–38°C, active cooling |
| Continuous discharge | 486 A (3C) | Active cooling |
| Peak discharge (10–30 s) | 648 A (4C) | — |

**Hard cap at 4C charge.** No peak charge rate above 4C is specified or recommended. This is a deliberate design constraint to protect the electrode-electrolyte interface and preserve the cycle life advantage that defines this cell.

---

## 3. Fast-charge envelope

| Parameter | Value |
|---|---|
| Recommended fast-charge window | 10–80% SOC |
| 3C charge, 10→80% SOC (CC-CV) | ~20–21 min |
| 4C charge, 10→80% SOC (CC-CV) | ~16–18 min |
| Fast-charge temperature window | 28–38°C |
| BMS must derate current if | T < 20°C or T > 40°C or SOC > 80% |

**Note on charge time methodology**: Times are computed using a CC phase (constant current until voltage hits 4.20V) followed by a CV phase modeled as exponential current decay: I(t) = I_cc × exp(−t/τ), with τ_macro = 150 s (solid-state diffusion time constant for prismatic LMFP) and cutoff at C/20. The CC→CV transition SOC depends on C-rate: at 3C, ~72% of the charge window is delivered in CC mode before IR drop forces the voltage limit. This replaces the v1.0 linear empirical factor.

---

## 4. Internal resistance

| Parameter | Value | Condition |
|---|---|---|
| DCIR (reference) | 0.14–0.19 mΩ | 50% SOC, 25°C, 10 s pulse |
| AC impedance (1 kHz) | 0.10–0.15 mΩ | 50% SOC, 25°C |

**DCIR varies with SOC and temperature.** The reference value is measured at optimal conditions (50% SOC, 25°C). In real operating conditions, DCIR deviates significantly:

| Condition | DCIR | Multiplier vs ref | Heat at 3C |
|---|---|---|---|
| SOC 50%, 25°C (reference) | 0.160 mΩ | 1.00× | 37.8 W |
| SOC 10%, 25°C (low SOC) | 0.208 mΩ | 1.30× | 49.1 W |
| SOC 90%, 25°C (high SOC) | 0.192 mΩ | 1.20× | 45.3 W |
| SOC 10%, 5°C (cold + low SOC) | 0.321 mΩ | 2.01× | 75.9 W |
| SOC 10%, 0°C (worst case) | 0.362 mΩ | 2.26× | 85.4 W |
| SOC 50%, 45°C (hot) | 0.109 mΩ | 0.68× | 25.8 W |

The thermal simulation model uses this dynamic DCIR, updating every second based on evolving SOC and cell temperature. BMS current derating must account for the elevated heat generation at low SOC / low temperature.

---

## 5. Physical characteristics

| Parameter | Value |
|---|---|
| Dimensions | 174 × 204 × 45 mm |
| Volume | 1.597 L |
| Cell mass | 3.05–3.20 kg |
| Specific energy | 191–201 Wh/kg |
| Volumetric energy density | 383 Wh/L |
| Terminal type | Prismatic stud |
| Enclosure | Aluminum case with safety vent |

---

## 6. Operating temperature

| Parameter | Value |
|---|---|
| Charge temperature | 0°C to 50°C |
| Recommended fast-charge | 20°C to 40°C |
| Optimal fast-charge | 28°C to 38°C |
| Discharge temperature | −20°C to 60°C |
| Storage (recommended) | 15°C to 30°C |

---

## 7. Cycle life and calendar life

All values to 80% SOH. Two columns: cell-level (single cell, controlled lab temperature) and pack worst-case (hottest cell in a 210-cell pack with liquid cooling, accounting for 3–6°C thermal gradient depending on C-rate).

| Condition | Cell-level | Pack worst-case |
|---|---|---|
| 1C/1C, 100% DOD, 25°C | 4,500–5,500 | 4,100–5,000 |
| 1C/1C, 80% DOD, 25°C | 5,500–7,000 | 5,000–6,400 |
| 3C charge / 1C discharge, 70% DOD | 2,500–3,200 | 2,100–2,700 |
| 4C charge / 1C discharge, 70% DOD | 2,000–2,500 | 1,600–2,100 |
| Calendar life | 15–18 years | — |
| Self-discharge | ≤2.5%/month (25°C) | — |

**Pack derating model**: The hottest cell in a multi-cell pack operates at T_avg + ΔT, where ΔT = 2.0 + 1.2 × C_rate (°C). At 3C, ΔT ≈ 5.6°C; at 4C, ΔT ≈ 6.8°C. Arrhenius-based degradation acceleration gives 8–17% fewer cycles for the worst-case cell, which dictates pack end-of-life.

---

## 8. Lithium plating risk assessment

Plating risk score (0–100 scale) at selected operating points. Risk ≥ 70 is considered unacceptable for sustained operation.

| C-rate | SOC | 10°C | 25°C | 35°C |
|---|---|---|---|---|
| 1C | 20% | 16 | 11 | 11 |
| 2C | 40% | 39 | 22 | 22 |
| 3C | 20% | 59 | 33 | 33 |
| 3C | 80% | 78 | 44 | 44 |
| 4C | 40% | 79 | 44 | 44 |
| 4C | 80% | 100 | 58 | 58 |

**Key finding**: At 10°C, 4C charging above 40% SOC is unsafe (risk ≥ 79). BMS must derate to ≤ 2C below 15°C. The hard carbon component provides ~15% risk reduction vs. pure graphite (already included in scores above).

---

## 9. Safety and materials

| Parameter | Value |
|---|---|
| Cathode active material | LiMn₀.₅₉Fe₀.₃₉Mg₀.₀₁Nb₀.₀₁PO₄/C |
| Cathode surface treatment | LiFePO₄ coating (~0.5 μm) |
| Anode | Artificial graphite (90%) + spherical hard carbon (10%) |
| Electrolyte salt | 0.95M LiFSI / 0.05M LiPF₆ |
| Electrolyte solvent | EC/EMC 3:7 |
| Electrolyte additives | 2% FEC + 1% LiDFOB + 1% VC |
| Separator | 12 μm Al₂O₃ ceramic-coated PE/PP/PE trilayer |
| N/P ratio | 1.14–1.17 |
| Safety vent | Yes |
| Certification target | UN 38.3 / IEC 62619 / UL 2580 design-compatible |

---

## 10. Integration guidelines

| Parameter | Recommendation |
|---|---|
| Cooling | Liquid cooling mandatory above 2C charge |
| BMS features | Anti-plating control, impedance tracking, thermal derating |
| BMS must enforce | Current derating below 15°C and above 40°C |
| BMS must enforce | Current derating above 80% SOC |
| Best longevity SOC window | 10–90% |
| Best fast-charge window | 10–80% |
| Storage SOC | 30–50% |
| Maximum continuous storage temp | 35°C at SOC ≤ 60% |

---

*Revision 1.1 — All specifications are simulation-based and require experimental validation through prototype cell testing. Pack worst-case values use a conservative thermal gradient model calibrated against published multi-cell pack data.*
