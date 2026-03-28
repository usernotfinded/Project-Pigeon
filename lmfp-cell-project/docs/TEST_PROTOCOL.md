# PROTOTYPE VALIDATION PROTOCOL
## LMFP-162P-EV — TRL 4 → TRL 5
### Transition from Simulation to Physical Measurement

**Revision**: 1.0 — March 2026  
**Objective**: Validate or falsify the three core simulation assumptions before committing to full-format prototype cells.

---

## 0. Philosophy

This protocol is designed around one principle: **measure the assumptions, not the cell**.

The v1.2 simulation model rests on three pillars that cannot be validated by further computation:

1. **DCIR(SOC, T)** — the dynamic resistance model with SOC-dependent U-curve and Arrhenius temperature scaling
2. **τ_macro** — the 150 s macroscopic diffusion time constant that governs CV taper duration
3. **ΔT_core-surface** — the internal thermal gradient that the 0D lumped model ignores

If any of these is wrong by more than 20%, the cycle life projections, charge times, and thermal limits must be recalculated. The goal of Phase 1 testing is to produce calibration data for these three parameters, not to build a finished product.

---

## 1. Test vehicle: single-layer pouch cells

Full-format 162 Ah prismatic cells are expensive and slow to iterate. The validation protocol uses **single-layer pouch cells** (SLPCs) with identical chemistry:

| Parameter | SLPC spec |
|---|---|
| Cathode | LiMn₀.₅₉Fe₀.₃₉Mg₀.₀₁Nb₀.₀₁PO₄/C + LFP coating |
| Anode | Artificial graphite FC (90%) + spherical hard carbon (10%) |
| Electrolyte | 0.95M LiFSI / 0.05M LiPF₆ in EC/EMC 3:7 + 2% FEC + 1% LiDFOB + 1% VC |
| Separator | 12 μm Al₂O₃ ceramic PE/PP/PE trilayer |
| N/P ratio | 1.15 (target midpoint) |
| Format | Single-layer pouch, ~50 × 80 mm electrode area |
| Capacity | ~200–400 mAh (depending on electrode loading) |
| Electrode loading | Match full-cell: ~20 mg/cm² cathode (single-sided) |
| Tabs | Al (cathode), Ni/Cu (anode), ultrasonic welded |

**Why SLPCs**: They isolate electrochemistry from cell engineering. No jelly-roll winding artifacts, no tab resistance distribution, no through-thickness thermal gradients. If the chemistry doesn't work in an SLPC, it won't work in a prismatic cell. If it does work, the gap to full-format is cell engineering, not chemistry — a much more tractable problem.

**Quantity**: Minimum 117 SLPCs (see test matrix for per-test allocation) plus 10% spares for cell failures during formation. Total: ~130 SLPCs across 3 synthesis batches (~45 per batch). Additionally, 6 multi-layer pouch cells for T9.

---

## 2. Test matrix overview

| Test ID | What it measures | Simulation assumption | Cells needed | Duration |
|---|---|---|---|---|
| T1 | DCIR vs SOC at fixed T | DCIR U-curve shape | 6 | 2 days |
| T2 | DCIR vs T at fixed SOC | Arrhenius Ea/R = 1800 K | 6 | 3 days |
| T3 | DCIR at worst case (SOC 10%, 0°C) | 0.362 mΩ (scaled) | 3 | 1 day |
| T4 | CV taper current decay | τ_macro = 150 s | 6 | 2 days |
| T5a | Mn dissolution rate vs cycle number | LiFSI 95/5 benefit (kinetics) | 30 | 8 weeks |
| T5b | Mn dissolution vs SOC (static hold) | SOC-dependent dissolution | 12 | 8 weeks |
| T6 | Plating detection at 4C/10°C | Risk score calibration | 12 | 4 weeks |
| T7 | Cycle life at 1C, 25°C | 5000 cycles prediction | 18 | 6–12 months |
| T8 | Cycle life at 3C, 30°C | 2840 cycles prediction | 18 | 4–8 months |
| T9 | Thermal gradient (multi-layer) | ΔT_core-surface | 6 | 1 week |
| T10 | Electrolyte compatibility | LiFSI + Al + LMFP | 6 | 4 weeks |

---

## 3. Test T1 — DCIR vs SOC mapping

**Objective**: Measure the SOC-dependent resistance curve and compare against the model's U-shape (soc_factor in `dcir_dynamic`).

**Setup**:
- Thermal chamber at 25.0 ± 0.5°C
- Potentiostat/galvanostat with EIS capability
- 6 SLPCs (3 from batch A, 3 from batch B)

**Procedure**:
1. Form cells: 3 cycles at C/10 between 2.50–4.20 V at 25°C
2. Charge to 100% SOC at C/10, rest 2 h
3. For each SOC point [100, 90, 80, 70, 60, 50, 40, 30, 20, 15, 10, 5]:
   a. Discharge to target SOC at C/10
   b. Rest 1 h (open circuit voltage stabilization)
   c. Apply 10 s discharge pulse at 1C equivalent
   d. Record voltage drop at t = 0.1 s (ohmic), t = 1 s, t = 10 s
   e. Calculate DCIR_10s = ΔV_10s / I_pulse
   f. Apply 10 s charge pulse at 1C equivalent
   g. Record voltage response identically
   h. Perform EIS sweep: 100 kHz → 10 mHz, 10 mV amplitude
   i. Rest 30 min before next SOC step

**Deliverables**:
- DCIR_10s(SOC) plot — compare vs model prediction
- Nyquist plots at each SOC — extract R_ohmic, R_ct, R_diffusion
- Validate or recalibrate: `soc_factor` coefficients (0.06/pct below 15%, 0.04/pct above 85%)

**Pass criterion**: Measured DCIR U-curve within ±15% of model at all SOC points. If failed, recalibrate coefficients and re-run cycle life simulation.

---

## 4. Test T2 — DCIR vs temperature (Arrhenius calibration)

**Objective**: Measure DCIR at multiple temperatures to extract the true Ea/R for ionic transport. The model assumes Ea/R = 1800 K.

**Setup**:
- Thermal chamber programmable from −10°C to 60°C (±0.5°C)
- 6 SLPCs, pre-formed

**Procedure**:
1. Set SOC to 50% at 25°C (C/10 discharge from full)
2. Rest 2 h
3. For each temperature [−10, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]:
   a. Soak cell at target temperature for 3 h (thermal equilibration)
   b. Verify OCV stability (< 1 mV drift over 10 min)
   c. Apply 10 s discharge pulse at 1C equivalent
   d. Calculate DCIR_10s
   e. Apply 10 s charge pulse at 1C equivalent
   f. Perform EIS sweep
   g. Rest 30 min

**Analysis**:
- Plot ln(DCIR) vs 1/T — should be linear if Arrhenius holds
- Linear regression: slope = Ea/R, extract measured Ea/R
- Compare to assumed 1800 K

**Pass criterion**: Measured Ea/R within 1500–2200 K. If outside this range, recalibrate `dcir_dynamic` and recompute all thermal simulations.

**Critical data point**: The DCIR at 0°C, 50% SOC. Model predicts 0.362 mΩ equivalent (2.26× ref for the full cell). The SLPC measurement, normalized to electrode area, must produce a consistent ratio.

---

## 5. Test T3 — Worst-case DCIR (SOC 10%, 0°C)

**Objective**: Direct measurement of the single most critical operating point — the one the static model missed entirely.

**Setup**: Same as T2, but cells set to 10% SOC at 25°C first, then cooled to 0°C.

**Procedure**:
1. Discharge to 10% SOC at C/10, 25°C
2. Rest 1 h
3. Cool to 0°C, soak 4 h (long soak — full thermal equilibration through jelly roll)
4. 10 s discharge pulse at 1C equivalent → DCIR_10s
5. 10 s charge pulse at 1C equivalent → DCIR_10s (charge)
6. EIS sweep
7. Repeat at 3C equivalent pulse (10 s) → verify linearity of I-V response
8. Repeat at SOC 15% and 20% for gradient

**Deliverable**: Single number — DCIR at SOC 10%, 0°C, normalized to full-cell equivalent. This is the number that determines whether 3C charging in winter is thermally safe.

**Pass criterion**: Measured DCIR ratio (vs 50%/25°C) within 2.0–2.8×. If > 2.8×, the BMS derating threshold must be raised from 15°C to 20°C.

---

## 6. Test T4 — CV taper time constant (τ_macro)

**Objective**: Directly measure the macroscopic diffusion time constant that governs how quickly current decays during CV phase. The model assumes τ_macro = 150 s.

**Setup**:
- Potentiostat in CC-CV mode with high-resolution current logging (≥ 10 Hz sampling)
- 6 SLPCs at 25°C

**Procedure**:
1. Discharge to 10% SOC at C/10
2. Rest 1 h
3. Charge at 3C equivalent in CC mode until V_cell = 4.20 V
4. Switch to CV at 4.20 V
5. Log current I(t) at 10 Hz until I drops below C/50
6. Repeat at 1C and 4C equivalent
7. Repeat entire sequence at 10°C and 40°C

**Analysis**:
- Plot ln(I(t)) vs t during CV phase — should be linear for simple exponential
- Slope = −1/τ → extract τ_macro
- If not linear (multi-exponential), fit I(t) = A₁·exp(−t/τ₁) + A₂·exp(−t/τ₂)
  and report both time constants with their amplitudes
- Compare τ_macro at different C-rates: if τ varies with C-rate, the model
  needs a C-rate-dependent τ (expected for solid-state diffusion)

**Expected outcome**: τ_macro likely between 100–250 s. If multi-exponential, the fast component (τ₁ ~ 30–60 s) represents interfacial charge transfer, the slow component (τ₂ ~ 150–300 s) represents solid-state Li⁺ diffusion in the cathode particles.

**Pass criterion**: Dominant τ within 100–250 s. If < 100 s (faster than expected), charge times will be shorter — positive surprise. If > 250 s, charge times will be longer and must be updated.

**Impact if failed**: A τ_macro of 300 s instead of 150 s would add ~2–3 min to the 3C 10→80% charge time (from 20.6 to ~23 min). Not catastrophic, but the datasheet must reflect it.

---

## 7. Test T5 — Mn dissolution kinetics

**Objective**: Quantify not only *how much* manganese dissolves, but *when* and *through which mechanism* — cycling-induced vs. potential-driven. This data directly informs BMS optimization: if dissolution is dominated by high-SOC hold, a software voltage limit at elevated temperatures could extend pack life more than any material modification.

The test is split into two sub-protocols: T5a (cycling with sacrificial cell matrix) and T5b (static calendar holds at controlled SOC).

**T5c (single-cycle dissolution profiling) has been removed from TRL 5.** The diffusion delay of Mn²⁺ ions through the electrode porosity and separator (~mm-scale transport through tortuous paths) makes intra-cycle electrolyte sampling unreliable — the Mn detected at any given SOC reflects dissolution that occurred minutes to hours earlier at a different SOC. The macroscopic kinetics from T5a + T5b are sufficient to define BMS strategy. Intra-cycle profiling belongs in TRL 6+ with specialized flow-cell or operando XAS setups.

**Total cells**: 42 SLPCs (21 target chemistry, 21 baseline)

---

### T5a — Cycling dissolution kinetics (sacrificial cell matrix)

**Objective**: Track cumulative Mn dissolution and anode Mn deposition as a function of cycle count to capture the dissolution rate curve shape (linear, concave, or convex).

**Why not electrolyte sampling via micro-septum**: A single-layer pouch cell contains ~3–5 mL of electrolyte. Even 5 μL per sample seems negligible (0.1–0.2%), but repeated septum puncture at 45°C introduces cumulative risks: micro-leaks from imperfect resealing, trace moisture ingress at each puncture, localized electrolyte composition gradients near the port, and accelerated gas generation at the seal. Over 10+ samplings during aggressive 1C cycling at 45°C, these perturbations would produce a convex degradation curve that looks exactly like the Mn-induced SEI feedback loop we're trying to detect — an observer artifact indistinguishable from the signal. The only clean measurement is a sacrificial cell that has never been opened.

**Setup**:
- 30 SLPCs: 15 target chemistry, 15 baseline (undoped LiMn₀.₆₀Fe₀.₄₀PO₄/C, 1M LiPF₆ in EC/EMC)
- All cells from the same electrode coating batch to minimize inter-cell variability
- Cycled at 1C/1C, 100% DOD, 45°C (accelerated aging)

**Procedure**:
1. Form all 30 cells: 3 cycles at C/10, 25°C
2. Record formation capacity and ICE for each cell. Exclude outliers (> 2σ from mean)
3. Begin cycling at 1C/1C, 100% DOD, 45°C
4. At each checkpoint, sacrifice 3 cells per chemistry group (total 6 per checkpoint):
   - **Cycle 10** — early dissolution, before SEI fully matures
   - **Cycle 50** — SEI should be stable; baseline dissolution rate established
   - **Cycle 100** — potential onset of Mn-induced SEI degradation in baseline
   - **Cycle 150** — intermediate check
   - **Cycle 200** — endpoint
5. For each sacrificed cell, in argon glovebox:
   a. Extract and weigh remaining electrolyte
   b. Electrolyte ICP-OES: Mn, Fe, Ni, Nb concentration (μg/mL)
   c. Wash anode 3× with DMC, dry under vacuum
   d. Digest anode in aqua regia → ICP-OES: total Mn, Fe on anode (μg/cm²)
   e. SEM/EDX of anode surface: spatial distribution of Mn deposits
   f. Cathode SEM: surface morphology changes, LFP coating integrity
   g. Record capacity at last cycle before sacrifice (from cycling data)

**Analysis**:
- Plot **total Mn on anode** (μg/cm²) vs cycle number — this is the definitive metric, not electrolyte Mn (which is a transient pool; the damage is done when Mn deposits on graphite)
- Plot **electrolyte Mn** (μg/mL) vs cycle number — secondary metric showing dissolution rate
- Curve shape classification:
  - **Linear**: constant dissolution rate, coating holds, no feedback loop → excellent prognosis
  - **Concave (decelerating)**: initial dissolution slows as surface passivates → best case
  - **Convex (accelerating)**: Mn deposits poison SEI → SEI regrows → consumes Li inventory → more Mn deposits → positive feedback. The onset cycle is the critical number
- Compare target vs baseline: the doping + LFP coat + LiFSI must shift the curve downward AND (if convex) delay the acceleration onset by ≥ 50 cycles
- **Mn/Fe ratio on anode**: if Fe deposition increases relative to Mn over cycling, the LFP coating itself may be dissolving — critical failure mode to detect early

**Deliverables**:
- Cumulative Mn deposition curve (μg/cm²) vs cycle number, target vs baseline
- Electrolyte Mn concentration curve vs cycle number
- Acceleration onset cycle (if convex) for target and baseline
- Mn/Fe deposition ratio evolution
- Cathode SEM: LFP coating integrity at each checkpoint
- Capacity retention curves (from cycling data, all remaining cells)

**Pass criterion**:
- Target Mn deposition at cycle 200 must be ≥ 50% lower than baseline
- No convex acceleration onset in target cells within 200 cycles (baseline may show onset at ~100–150)
- LFP coating visually intact on cathode SEM at cycle 200
- If acceleration detected in target before cycle 200: investigate coating thickness, adhesion, or Nb doping level

**Statistical note**: 3 cells per checkpoint gives a meaningful mean ± standard deviation. If inter-cell variability (CV%) exceeds 30% at any checkpoint, the synthesis process needs tightening before proceeding to full-format cells.

---

### T5b — Static calendar dissolution (SOC-decoupled)

**Objective**: Separate the two dissolution mechanisms — cycling-induced (mechanical stress from lattice expansion/contraction) vs. potential-driven (thermodynamic instability of Mn³⁺ at high voltage). This is the test that tells the BMS what to do.

**Setup**:
- 12 SLPCs (6 target, 6 baseline)
- No cycling — cells are charged to a fixed SOC and held at constant temperature

**Procedure**:
1. Form cells at 25°C
2. Charge cells to three SOC levels (1 cell per chemistry per SOC level, ×2 for duplicates):
   - **50% SOC** (mid-plateau, ~3.65V — low Mn³⁺ concentration)
   - **80% SOC** (~3.95V — Mn²⁺/Mn³⁺ transition region)
   - **100% SOC** (4.20V — maximum Mn³⁺, maximum dissolution driving force)
3. Store all cells at 45°C for 8 weeks
4. OCV measurement weekly (voltage decay indicates side reactions)
5. At week 8: full disassembly in argon glovebox
   a. Extract and measure electrolyte → ICP-OES for Mn, Fe
   b. Anode digestion → ICP-OES for deposited Mn, Fe
   c. Cathode SEM for surface morphology
   d. Compare against T5a cycle-50 data (same total time at temperature, different stress mode)

**Note on electrolyte sampling**: Unlike T5a cycling cells, static hold cells experience no mechanical cycling stress and minimal gas generation. A single endpoint disassembly at week 8 avoids the micro-septum perturbation entirely. If intermediate data points are needed (week 2, 4, 6), dedicate additional sacrificial cells rather than sampling from the same cell.

**Analysis**:
- Plot Mn deposition on anode (μg/cm²) at each SOC level
- Calculate dissolution rate (μg/cm²/week) at each SOC
- Key deliverable: **SOC threshold above which dissolution accelerates**
  - If dissolution at 100% SOC >> dissolution at 80% SOC → the BMS should reduce charge voltage limit at temperatures > 35°C (e.g., from 4.20V to 4.15V)
  - If dissolution at 80% SOC ≈ dissolution at 100% SOC → the voltage is not the primary driver; mechanical cycling stress is → BMS voltage limit won't help, focus on DOD reduction instead
- Cross-reference with T5a: compare Mn on anode from T5b 100% SOC / 8 weeks vs T5a cycle 50 (also ~50 days at 45°C but with cycling). The difference isolates the mechanical contribution.

**Pass criterion**:
- At 50% SOC: Mn on anode < 0.5 μg/cm² after 8 weeks (target chemistry)
- At 100% SOC: target must show ≥ 40% less Mn than baseline
- Clear SOC-dependent gradient (higher SOC → more dissolution) — this validates the thermodynamic model

**Impact on BMS design**: If T5b shows that dissolution at 100% SOC is ≥ 3× higher than at 80% SOC at 45°C, the BMS should implement: *if T_cell > 35°C, limit charge to 4.15V (≈90% SOC)*. This software-only intervention could extend pack life by 20–30% in hot climates at zero hardware cost.

---

### T5 combined deliverables

| Deliverable | Source | BMS action |
|---|---|---|
| Dissolution rate curve shape | T5a | If convex: set cycle-count trigger for health check / current derating |
| Acceleration onset cycle | T5a | Fleet maintenance scheduling: health check before onset |
| Dissolution rate vs SOC (static) | T5b | If SOC-dependent: implement V_max derating at high T |
| Cycling vs calendar contribution | T5a vs T5b | If calendar dominates: SOC limit matters more than DOD |
| Target vs baseline comparison | T5a + T5b | Validate the triple-defense strategy quantitatively |
| Mn/Fe ratio evolution | T5a | If Fe grows relative to Mn: LFP coating dissolving — investigate |
| LFP coating integrity | T5a cathode SEM | If cracking/delamination: increase coating thickness or change method |

---

## 8. Test T6 — Lithium plating detection at 4C / 10°C

**Objective**: Validate the plating risk model prediction that 4C at 10°C / SOC > 40% is unsafe (risk score ≥ 79).

**Setup**:
- 12 SLPCs at 10°C
- Reference electrode (Li metal micro-reference in 3-electrode cell) or voltage relaxation method

**Procedure — Method A (reference electrode)**:
1. Insert Li micro-reference electrode during cell assembly (3 SLPCs)
2. Charge at 4C equivalent from 10% SOC at 10°C
3. Monitor anode potential vs Li/Li⁺ in real time
4. If anode potential drops below 0 mV vs Li/Li⁺ → plating onset detected
5. Record SOC at plating onset

**Procedure — Method B (voltage relaxation, non-invasive)**:
1. Charge at 4C from 10% SOC at 10°C, stop at target SOC [30, 40, 50, 60, 70, 80]
2. Immediately switch to OCV rest
3. Log voltage at 0.1 Hz for 2 h
4. If voltage relaxation shows characteristic "hump" (voltage dip followed by recovery
   within 5–30 min), lithium stripping is occurring → plating was present
5. Repeat at 3C and 2C for comparison

**Procedure — Method C (post-mortem)**:
1. After Method B, disassemble cells in glovebox
2. Photograph anode surface: Li plating appears as metallic gray/silver patches
3. SEM/EDX of anode surface for metallic Li deposits

**Deliverables**:
- SOC threshold at which plating initiates for each C-rate at 10°C
- Comparison with model prediction: model says risk ≥ 70 at 4C/SOC40/10°C
- If plating detected at SOC < 40%, the model underestimates risk → increase BMS derating

**Pass criterion**: No plating detected at ≤ 3C up to 80% SOC at 10°C. Plating confirmed at 4C above SOC 30–50% at 10°C (consistent with risk score 79 at SOC 40%).

---

## 9. Test T7/T8 — Cycle life validation

**Objective**: Long-duration cycling to validate cycle life predictions.

**T7 — Standard cycling (1C/1C, 25°C)**:
- 18 SLPCs (6 per synthesis batch)
- Cycle at 1C charge / 1C discharge, 100% DOD, 25°C
- Target: 5000 cycles to 80% SOH
- Every 100 cycles: perform reference capacity check at C/10 + EIS + DCIR pulse
- Expected duration: 6–12 months

**T8 — Fast-charge cycling (3C/1C, 30°C)**:
- 18 SLPCs (6 per synthesis batch)
- Charge at 3C (CC-CV, 4.20V cutoff, C/20 cutoff), discharge at 1C
- 10–80% SOC window (70% DOD)
- 30°C thermal chamber
- Target: 2840 cycles to 80% SOH
- Every 50 cycles: reference capacity + EIS + DCIR
- Expected duration: 4–8 months

**Early termination triggers**:
- If capacity < 85% SOH at cycle 500 (T7) or cycle 300 (T8) → chemistry problem, stop and investigate
- If DCIR growth > 50% from BOL at any checkpoint → impedance anomaly, investigate

**Deliverables**:
- Capacity retention vs cycle number curves
- DCIR evolution vs cycle number
- EIS evolution (Nyquist plots) at checkpoints
- Coulombic efficiency tracking (target: > 99.9% after formation)
- Post-mortem of cells at 80% SOH: SEM, XRD, ICP-OES

---

## 10. Test T9 — Internal thermal gradient (multi-layer cell)

**Objective**: Measure the temperature difference between cell core and surface to quantify the error of the lumped-capacitance thermal model.

**This test requires a different cell format**: a 5–10 layer stacked pouch cell (~2–4 Ah) with embedded thermocouples.

**Setup**:
- 6 multi-layer pouch cells with same chemistry
- 3 type-K thermocouples per cell:
  - TC1: center layer (between layers 5 and 6 in a 10-layer cell)
  - TC2: outer layer (between layer 1 and pouch wall)
  - TC3: pouch surface
- Thermocouple wires exit through the pouch seal (sealed with epoxy)
- Thermal chamber at 30°C
- No active cooling (natural convection only — worst case)

**Procedure**:
1. Charge at 1C → record TC1, TC2, TC3 over time
2. Charge at 3C → record
3. Charge at 4C → record
4. For each: compute ΔT_core-surface = TC1 − TC3

**Analysis**:
- At 4C, model predicts Q_gen_peak = 79 W for a 162 Ah cell. Scale to the multi-layer cell:
  Q_scaled = 79 × (cell_capacity / 162)
- The core-to-surface ΔT depends on:
  - Through-thickness thermal conductivity: k_z ≈ 0.5–1.5 W/(m·K) for electrode stack
  - In-plane thermal conductivity: k_xy ≈ 20–40 W/(m·K) (along foils)
  - Cell half-thickness: L = 22.5 mm for the full-format cell
  - ΔT_core-surface ≈ Q_gen × L / (k_z × A_cooling)

**Expected result**: For 45 mm thickness and k_z ~ 1 W/(m·K):
- At 4C (79 W scaled): ΔT ≈ 79 × 0.0225 / (1.0 × 0.0355) ≈ 50°C
  This is physically unrealistic for steady-state because it ignores heat removal.
  In transient (10 min charge), the actual ΔT will be 5–15°C depending on cooling.
- The measurement will provide the real number.

**Deliverables**:
- ΔT_core-surface at 1C, 3C, 4C as a function of time
- Effective through-thickness thermal conductivity k_z (extracted from transient data)
- Recommendation: if ΔT_core > 8°C at 4C, the cycle life model must apply
  an additional derating factor for core degradation

**Impact**: This is the measurement that determines whether the lumped 0D model is "good enough" or needs to be replaced with a 1D through-thickness model for the full-format prismatic cell.

---

## 11. Test T10 — Electrolyte compatibility

**Objective**: Verify that LiFSI 95/5 does not corrode the aluminum current collector at the operating voltage of the Mn²⁺/Mn³⁺ redox couple (~4.1V).

**Setup**:
- 6 SLPCs with aluminum cathode current collector
- Linear sweep voltammetry (LSV) setup with Al foil working electrode

**Procedure — LSV**:
1. Prepare 3-electrode cell: Al foil WE, Li metal CE + RE
2. Fill with target electrolyte (0.95M LiFSI / 0.05M LiPF₆ + additives)
3. LSV scan from OCV to 5.0 V vs Li/Li⁺ at 0.5 mV/s
4. Measure oxidation current — onset of Al dissolution appears as
   sharp current increase
5. Repeat with baseline (1M LiPF₆)
6. Post-LSV: SEM of Al surface — check for pitting

**Procedure — Long-term float**:
1. 3 SLPCs: charge to 4.20V, hold at 4.20V float for 28 days at 45°C
2. Monitor leakage current daily
3. After 28 days: disassemble, SEM/EDX of Al current collector
4. Look for Al dissolution, pitting, fluoride deposits

**Pass criterion**: 
- LSV: no oxidation current > 10 μA/cm² below 4.5V
- Float: leakage current < 0.5 mA at day 28
- SEM: no visible pitting on Al surface

**If failed**: The 5% LiPF₆ is insufficient for Al passivation. Options:
a. Increase LiPF₆ to 10% (reduces Mn dissolution benefit)
b. Add 2% LiDFOB (already present at 1%, increase)
c. Pre-passivate Al foil with AlF₃ coating before electrode fabrication

---

## 12. Equipment requirements

| Equipment | Purpose | Estimated cost |
|---|---|---|
| Potentiostat/galvanostat (multi-channel) | Cycling, EIS, DCIR pulses | €15,000–30,000 |
| Thermal chamber (−20°C to 80°C) | Temperature control for all tests | €8,000–15,000 |
| Argon glovebox | Cell assembly and post-mortem | €25,000–50,000 |
| ICP-OES | Mn/Fe dissolution quantification (T5) | €50,000–80,000 (or outsource) |
| SEM/EDX | Post-mortem surface analysis | outsource (~€200/sample) |
| Electrode coating line (lab-scale) | Electrode fabrication | €20,000–40,000 |
| Pouch cell sealer | Cell assembly | €3,000–5,000 |
| Type-K thermocouples + DAQ | Thermal gradient measurement | €2,000–5,000 |
| Chemicals and materials | Cathode powder, LiFSI, separator | €5,000–10,000 per batch |

**Total estimated budget**: €130,000–240,000 for complete protocol. Outsourcing ICP-OES and SEM reduces this to ~€80,000–160,000.

**ICP-OES sample count for T5**: T5a produces 2 analyses/cell (electrolyte + anode digest) × 30 cells = 60 samples. T5b produces 2 analyses/cell × 12 cells = 24 samples. Plus 30 SEM sessions for cathode coating integrity checks. Total: ~84 ICP-OES analyses + ~30 SEM sessions. At ~€30–50/sample (ICP-OES) and ~€200/session (SEM): €4,500–10,000 for T5 analytics — significantly less than the v1.0 micro-septum approach, and the data is cleaner.

**Alternative**: Partner with a university battery lab (e.g., Politecnico di Milano, University of Bologna) that already has glovebox + potentiostat + thermal chamber + ICP-OES. Reduces capital cost to materials and consumables: ~€20,000–40,000.

---

## 13. Timeline

| Month | Activity |
|---|---|
| 1–2 | Synthesize cathode material (3 batches), procure LiFSI electrolyte, separator |
| 2–3 | Fabricate electrodes, assemble ~130 SLPCs + 6 multi-layer cells |
| 3 | Formation cycling, T1 (DCIR vs SOC), T2 (DCIR vs T), T3 (worst-case DCIR) |
| 3–4 | T4 (τ_macro measurement), T10 (electrolyte compatibility) |
| 4 | **Decision gate 1**: Are DCIR model and τ_macro within spec? |
| 4–6 | T9 (thermal gradient), T6 (plating detection) |
| 4–12 | T5a (cycling dissolution kinetics, 200 cycles at 45°C, sacrificial cells at 5 checkpoints) |
| 4–12 | T5b (static calendar holds at 50/80/100% SOC, 45°C, 8 weeks, endpoint disassembly) |
| 4–16 | T7 (cycle life 1C), T8 (cycle life 3C) |
| 8 | **Decision gate 2**: Cycle life trending? Mn dissolution kinetics? Cross-reference T5a vs T5b? |
| 12–16 | T7 completion, post-mortem analysis |
| 16–18 | Data analysis, model recalibration, v2.0 simulation, full-format cell design freeze |

**Critical path**: Decision gate 1 (month 4) determines whether the chemistry works at all. If T1–T4 pass, commit to the long-duration cycling. If they fail, iterate on chemistry before burning 12 months of cycle testing.

---

## 14. Decision gates and go/no-go criteria

### Gate 1 (Month 4) — Chemistry validation

| Test | Pass | Conditional pass | Fail |
|---|---|---|---|
| T1 DCIR(SOC) | Within ±15% of model | Within ±25%, recalibrate | > ±25%, investigate |
| T2 Ea/R | 1500–2200 K | 1200–2500 K, recalibrate | < 1200 or > 2500 K |
| T3 DCIR worst-case | 2.0–2.8× ref | 1.5–3.5× ref, update BMS | > 3.5× ref |
| T4 τ_macro | 100–250 s | 80–350 s, update datasheet | < 80 or > 350 s |
| T10 Al corrosion | No pitting, low leakage | Minor pitting, increase LiPF₆ | Severe pitting |

**All 5 must pass or conditional-pass to proceed.**

### Gate 2 (Month 8) — Durability validation

| Test | Pass | Fail |
|---|---|---|
| T5a Mn dissolution rate | ≥ 50% reduction vs baseline, no acceleration within 200 cycles | < 50% reduction OR acceleration onset < cycle 150 |
| T5a Mn/Fe ratio | Fe/Mn ratio stable (LFP coating intact) | Fe/Mn ratio increasing (LFP coating dissolving) |
| T5b SOC-dependent dissolution | Clear SOC gradient, < 0.5 μg/cm² at 50% SOC/8 weeks | No SOC gradient (dissolution not potential-driven) |
| T6 Plating at 4C/10°C | No plating at ≤ 3C/80% SOC | Plating at ≤ 3C/60% SOC |
| T7 trending | > 90% SOH at cycle 1000 | < 88% SOH at cycle 1000 |
| T8 trending | > 90% SOH at cycle 500 | < 88% SOH at cycle 500 |
| T9 ΔT_core | < 12°C at 4C | > 15°C at 4C |

**T5 combined pass**: T5a AND T5b must pass. Cross-reference between T5a (cycle 50 data, ~50 days at 45°C) and T5b (8 weeks at 45°C, static) isolates the mechanical cycling contribution to dissolution.

---

## 15. What happens after validation

**If all gates pass**: Proceed to full-format 162 Ah prismatic cell prototyping. The simulation model parameters are updated with measured values, and the datasheet v2.0 is issued with experimentally validated numbers.

**If Gate 1 fails**: The chemistry needs iteration. Most likely failure modes:
- DCIR too high at low T → HC fraction may need to increase to 15–20%
- τ_macro too long → cathode particle size reduction required
- Al corrosion → LiPF₆ fraction needs to increase to 10%

**If Gate 2 fails**: The chemistry works in short-term but degrades too fast. Most likely:
- Mn dissolution too high → LFP coating thickness or Nb doping level insufficient
- Plating at lower SOC than expected → N/P ratio needs to increase to 1.18–1.20
- Core temperature too high → prismatic cell thickness may need to reduce from 45 to 40 mm

Each failure mode has a defined corrective action. No failure requires abandoning the project — only iterating.

---

*This protocol was designed for worst-case validation. Every test is structured to find the point of failure, not to confirm success.*
