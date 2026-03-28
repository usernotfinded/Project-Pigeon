# LMFP-162P-EV

**High-durability prismatic LMFP cell for 800V electric vehicles and industrial energy storage**

> *Designed for operators who need batteries that last 15+ years, not headlines about 9-minute charges.*

---

## Why this exists

The EV battery market is in an arms race for charging speed. BYD claims 10→97% in 9 minutes. CATL claims 0→80% in 10 minutes. These are impressive engineering achievements — but they optimize for a metric most fleet operators don't care about.

What fleet operators, industrial traction users, and ESS integrators actually care about is **total cost of ownership (TCO)**. A battery that lasts 5,000 cycles instead of 3,000 saves hundreds of euros per year per vehicle over a 15-year service life. That's the gap this cell is designed to fill.

**LMFP-162P-EV** is a 162 Ah prismatic LMFP cell optimized for:
- **Cycle life**: 4,500–5,500 cycles at 1C (target 80% SOH)
- **Durability at fast charge**: 2,800–3,500 cycles at 3C
- **Energy density**: 191–201 Wh/kg, 383 Wh/L
- **Safety**: Inherent LMFP stability + LFP surface coating + ceramic trilayer separator
- **Practical fast charge**: 10→80% in ~20–21 min at 3C (no extreme C-rates needed)

---

## Cell specifications

| Parameter | Value |
|---|---|
| **Model** | LMFP-162P-EV |
| **Cathode** | LiMn₀.₅₉Fe₀.₃₉Mg₀.₀₁Nb₀.₀₁PO₄/C + LFP surface coating |
| **Anode** | Artificial graphite FC (90%) + spherical hard carbon (10%) |
| **Electrolyte** | 0.95M LiFSI / 0.05M LiPF₆ in EC/EMC + FEC/LiDFOB/VC |
| **Separator** | 12 μm ceramic-coated PE/PP/PE trilayer |
| **Format** | Prismatic, aluminum case |
| **Nominal capacity** | 162 Ah |
| **Nominal voltage** | 3.78 V |
| **Cell energy** | 612.4 Wh |
| **Specific energy** | 191–201 Wh/kg |
| **Volumetric energy** | 383 Wh/L |
| **Dimensions** | 174 × 204 × 45 mm |
| **Mass** | 3.05–3.20 kg |
| **DCIR (BOL, 50% SOC, 25°C)** | 0.14–0.19 mΩ |
| **Charge voltage (recommended)** | 4.20 V |
| **Charge voltage (absolute max)** | 4.25 V |
| **Discharge cut-off** | 2.50 V |

### Charge / discharge ratings

| Mode | C-rate | Current |
|---|---|---|
| Standard charge | 1C | 162 A |
| Fast charge (recommended) | 3C | 486 A |
| Fast charge (maximum, active cooling) | 4C | 648 A |
| Continuous discharge | 3C | 486 A |
| Peak discharge (10–30 s) | 4C | 648 A |

**No peak charge above 4C.** This is a deliberate design choice: transient 5–6C peaks stress the electrode-electrolyte interface disproportionately relative to the time saved, undermining the durability advantage that defines this cell.

### Cycle life

| Condition | Cell-level | Pack worst-case* |
|---|---|---|
| 1C/1C, 100% DOD, 25°C | 4,500–5,500 | 4,100–5,000 |
| 1C/1C, 80% DOD, 25°C | 5,500–7,000 | 5,000–6,400 |
| 3C charge / 1C discharge, 70% DOD | 2,500–3,200 | 2,100–2,700 |
| 4C charge / 1C discharge, 70% DOD | 2,000–2,500 | 1,600–2,100 |
| Calendar life | 15–18 years (25°C, 40% SOC) | — |

*Pack worst-case accounts for the hottest cell in a 210-cell pack, which runs 3–6°C above average depending on C-rate and cooling system quality. This cell dictates pack end-of-life. Derating is 8–17% depending on operating conditions.*

### Operating temperature

| Condition | Range |
|---|---|
| Charge | 0°C to 50°C |
| Recommended fast charge | 20°C to 40°C |
| Optimal fast charge | 28°C to 38°C |
| Discharge | −20°C to 60°C |

---

## What makes this cell different

### 1. Mg/Nb dual-doped LMFP cathode + LFP shell

The cathode uses two well-characterized dopants working in synergy:

- **Magnesium (1%)** — mitigates Jahn-Teller distortion of Mn³⁺ octahedra, the primary mechanism behind structural degradation. Mg²⁺ stabilizes Mn in the 2+ state and promotes single-phase solid-solution behavior during cycling, reducing mechanical strain. Published data shows MgNi-LMFP/C retaining 92% capacity after 2,000 cycles at 1C.

- **Niobium (1%)** — reduces antisite defects (Fe/Mn on Li sites), accelerates Li⁺ diffusion, and suppresses Mn dissolution at elevated temperatures. Nb-doped LMFP has demonstrated 95% retention over 150 cycles at 60°C in industrial-scale cells.

- **LFP surface coating (~0.5 μm)** — a thin LiFePO₄ shell on each LMFP particle reduces direct contact between the Mn-containing active material and the electrolyte. Published full-cell tests show >50% reduction in Mn and Fe dissolution and >97% capacity retention vs. uncoated LMFP.

**Why not triple or quadruple doping?** Each additional dopant increases synthesis complexity and interaction unknowns. Mg+Nb is the most extensively validated pair in peer-reviewed literature. Keeping it to two dopants is why we target 90% feasibility, not 70%.

### 2. LiFSI-dominant electrolyte (95/5)

The electrolyte uses lithium bis(fluorosulfonyl)imide (LiFSI) as the primary salt with only 5% LiPF₆ retained for aluminum current collector passivation.

The mechanism is simple and well-proven: LiPF₆ generates HF through hydrolysis, and HF is the primary driver of manganese dissolution from the cathode. LiFSI does not generate HF. Research from Dalhousie University (2025) demonstrated that LMFP/graphite cells with 95% LiFSI showed dramatically reduced Mn deposition on the anode and improved cycle life.

The 5% LiPF₆ minimum is necessary because LiFSI alone cannot passivate the aluminum current collector at the ~4.1V operating potential of the Mn²⁺/Mn³⁺ redox couple. LiDFOB provides additional Al passivation and forms a stable cathode-electrolyte interphase (CEI).

### 3. Graphite/hard carbon hybrid anode (90/10)

Adding 10% spherical hard carbon to the graphite anode provides three benefits:

- **Anti-plating voltage buffer** — hard carbon has a sloping charge plateau (vs. graphite's flat plateau), which neutralizes local potential spikes across the electrode. This reduces the probability of lithium plating during fast charge without requiring extreme N/P ratios.

- **Low-temperature performance** — published data shows 15–18% improvement in capacity retention at 0°C vs. pure graphite systems at 1C.

- **Structural support** — hard carbon particles fill voids between graphite particles, creating a more uniform pore structure with shorter ion transport paths.

The trade-off is a small drop in initial coulombic efficiency (from ~91% to ~89%) and slightly lower specific capacity (~349 vs ~355 mAh/g). Both are manageable with electrode design optimization and slightly higher N/P ratio (1.14–1.17).

### 4. Ceramic-coated trilayer separator

The PE/PP/PE trilayer provides dual thermal shutdown capability: the PE layers melt at ~130°C to close pores and stop ion transport, while the PP layer (melting at ~165°C) maintains mechanical integrity. The Al₂O₃ ceramic coating improves electrolyte wettability and dimensional stability at elevated temperatures.

At 12 μm, this is thinner than the previous design's 14–16 μm, recovering internal volume for electrode material while actually improving safety through the trilayer architecture.

---

## 800V pack design

Using the LMFP-162P-EV in a 210s1p configuration:

| Parameter | Value |
|---|---|
| Configuration | 210s1p (15 modules × 14s1p) |
| Nominal voltage | 793.8 V |
| Max voltage (recommended) | 882.0 V |
| Gross energy | 128.6 kWh |
| Usable energy (10–90% SOC) | 102.9 kWh |
| Usable energy (5–95% SOC) | 115.7 kWh |
| DC charge power at 3C | ~386 kW |
| Charge time 10→80% at 3C | ~20–21 min |
| Charge time 10→80% at 500A | ~20 min |
| Pack mass (estimated) | ~820 kg |
| Continuous discharge power | ~386 kW |
| Peak discharge power | ~514 kW |

**Module voltage safety**: Each 14s1p module stays below 60V at maximum charge (14 × 4.25V = 59.5V), meeting low-voltage safety requirements for maintenance and modular replacement.

### Range estimate

With 102.9 kWh usable (10–90% SOC) and typical EV consumption of 16–18 kWh/100km:

| Consumption | Range |
|---|---|
| 15 kWh/100km (highway, optimal) | 686 km |
| 17 kWh/100km (mixed) | 605 km |
| 19 kWh/100km (city, cold) | 542 km |
| 21 kWh/100km (worst case) | 490 km |

---

## Competitive positioning

| Metric | LMFP-162P-EV | BYD Blade 2.0 | CATL M3P/Shenxing |
|---|---|---|---|
| Energy density | 191–201 Wh/kg | 190–210 Wh/kg | ~210 Wh/kg |
| 10→80% charge | ~20–21 min | ~5–7 min (claim) | ~10 min (claim) |
| Cycle life 1C (pack) | **4,100–5,000** | 3,000–3,500 | est. 2,000–3,000 |
| Max charge C-rate | 4C (hard cap) | 8C (peak claim) | 10C (peak claim) |
| Calendar life | **15–18 years** | ~10–12 years | not published |
| Mn dissolution control | Mg/Nb doping + LFP coat + LiFSI | unknown | unknown (M3P proprietary) |
| Feasibility | 90%+ (all components peer-reviewed) | production | production |

**Our advantage**: 30–60% more cycle life than competitors *at pack level, worst-case cell*. Not at cell level under ideal conditions — the numbers above already account for thermal gradients in a real 210-cell pack.

---

## Technology roadmap

### Phase 1 — Current design (TRL 4–5)
All components use proven, peer-reviewed techniques. Wet electrode processing. Conservative C-rates. Target: prototype cells within 12–18 months.

### Phase 2 — Dry electrode process (TRL 2–3)
Tesla confirmed full dry electrode production for 4680 cells (January 2026). Adapting dry cathode processing to prismatic LMFP format could reduce manufacturing cost by 30–40% and factory footprint by ~50%. Published research on dry-processed LFP cathodes shows up to 185 Wh/kg and 470 Wh/L at the electrode level — higher than wet processing because thicker electrodes become feasible without cracking.

Timeline: begin R&D 12 months after Phase 1 validation. Target: Phase 2 prototype at 24–30 months.

### Phase 3 — Next-generation cathode (TRL 1–2)
Explore single-crystal LMFP for further cycle life gains, higher Mn content (65/35) enabled by improved dissolution control, and Si-C composite anode for energy density >220 Wh/kg.

---

## Feasibility analysis

| Component | Technology readiness | Literature support | Risk |
|---|---|---|---|
| LMFP 60/40 cathode | TRL 6–7 (commercial LMFP exists) | Extensive | Low |
| Mg doping in LMFP | TRL 5 (lab-validated, multiple groups) | Strong | Low |
| Nb doping in LMFP | TRL 5 (industrial-scale demo, ACS 2025) | Strong | Low |
| LFP surface coating | TRL 5 (full-cell validated at 60°C) | Strong | Low |
| LiFSI 95/5 electrolyte | TRL 5 (Dalhousie 2025, full-cell data) | Strong | Low-Medium |
| FEC + LiDFOB additives | TRL 7 (commercial use in other chemistries) | Extensive | Low |
| Graphite/HC 90/10 anode | TRL 5 (multiple published studies) | Strong | Low |
| Trilayer ceramic separator | TRL 7 (commercial product) | Extensive | Very low |
| Prismatic format | TRL 9 (industry standard) | N/A | Very low |

**Combined feasibility estimate: 90%**

The remaining 10% risk comes from: (a) interaction effects between Mg+Nb doping and LiFSI electrolyte that haven't been tested in combination at this specific ratio, and (b) scale-up from lab-scale doping to industrial coprecipitation/spray-drying.

---

## Repository structure

```
├── README.md                          # This file
├── LICENSE                            # MIT
├── docs/
│   ├── CELL_DATASHEET.md             # Preliminary industrial datasheet
│   ├── PACK_SPEC.md                  # 800V pack specifications
│   ├── COMPETITIVE_ANALYSIS.md       # Detailed market positioning
│   └── REFERENCES.md                 # Academic citations
├── simulations/
│   ├── cell_model.py                 # Electrochemical & thermal model
│   └── results.json                  # Simulation outputs
└── assets/
    └── (diagrams, charts)
```

---

## Key references

1. Leslie et al., "Reducing the Rate of Mn Dissolution in LiMn₀.₈Fe₀.₂PO₄/Graphite Cells with Mixed Salt Electrolytes," *J. Electrochem. Soc.* 172, 040515 (2025)
2. Gonçalves et al., "Emerging multimetal LMFP-based cathodes for lithium-ion batteries: a review," *J. Mater. Chem. A* 13, 40399 (2025)
3. Liang et al., "Boosting High-Temperature Durability of Industrial-Scale LiMn₀.₆Fe₀.₄PO₄ Cathode through Niobium Doping," *ACS Appl. Mater. Interfaces* 17, 33783 (2025)
4. Chen et al., "Enabling 6C Fast Charging of Li-Ion Batteries with Graphite/Hard Carbon Hybrid Anodes," *Adv. Energy Mater.* 11, 2003336 (2021)
5. Wei et al., "Inhibiting manganese dissolution in LiFe₀.₄Mn₀.₆PO₄ through synergistic effect of Ti-doping and LiTiOPO₄-coating," *Chem. Eng. J.* (2025)
6. Kwon et al., "Low-Resistance LiFePO₄ Thick Film Electrode Processed with Dry Electrode Technology," *Small Science* (2024)
7. Zeng et al., "LMFP materials: Design, progress, and challenges," *Energy Materials and Devices* 3(1), 9370060 (2025)
8. Qiu et al., "Modification Strategies for LMFP Cathodes," *Chemistry–Methods* (2025)

---

## Contact

**Natan Mucelli** — cell design and systems engineering

This is a preliminary design document. All specifications are simulation-based and require experimental validation. Interested in collaborating or investing? Open an issue or reach out.

---

*Last updated: March 2026*
