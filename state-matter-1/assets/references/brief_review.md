# Review of the brief — The Molecular Dance (States of Matter, Part 1)

The brief's eleven chapters, driving questions, teaching priorities and worked
examples are kept. Every number below is recomputed by
`python -m utils.physics_models`, and every spoken one is checked by
`python -m utils.gas_data`.

## Corrections and clarifications made in the film

| Brief | Film |
|---|---|
| "billions of molecules" | A litre of air at 1 bar and 300 K holds ≈ 2.4 × 10²² molecules, so the narration says "countless" or "an enormous crowd", and gives the real number in scene 24. |
| Hook: air "can support loads" | Made quantitative: 1 bar presses on each square metre with the weight of ≈ 10.2 t (1 bar / g), said as "about ten tonnes". |
| §2: no energy scale for "weak" intermolecular forces | O–H bond in water ≈ 463 kJ/mol against a typical hydrogen bond ≈ 20 kJ/mol (literature range ≈ 10–40). Both are said with "about". |
| §2B: thermal averaging of dipole–dipole energy | Shown, not just stated. The two HCl molecules tumble through a seeded Metropolis walk, and the running mean of their energy settles below zero. The −1/r⁶ law is checked by exact quadrature: −2/3 μ⁴/(kT r⁶) to leading order. The walk's temperature (kT = 0.25 in reduced units) was chosen so the bias is visible. |
| §3: "the physical state depends on the balance…" | Demonstrated with a real 2D Lennard-Jones molecular-dynamics run of 61 atoms (velocity Verlet, velocity-rescaling thermostat). Target temperatures are 0.10, 0.47 and 1.6 ε/k_B, chosen against the 2D triple (~0.41) and critical (~0.53) points. `physics_models.verify` checks that the liquid flows, the solid only vibrates and the gas fills the box. On screen it is called a two-dimensional simulation. |
| §4: 2D model must not stand in for the 3D derivation | The 2D close-up explains only the bounce and the round-trip time. The factor 1/3 comes from a 3D velocity ball, with ⟨v_x²⟩, ⟨v_y²⟩, ⟨v_z²⟩ computed from the sample (0.34, 0.35, 0.31 of ⟨v²⟩ for 600 molecules, so the scatter shows honestly). |
| §4: "a measurable average force" | Force traces for 1, 5, 50 and 5000 molecules are computed from exact hit times. Fluctuations shrink like 1/√(hits). Real air: ≈ 2.9 × 10²³ hits per cm² per second (P / √(2πmkT) for N₂ at 300 K). |
| §5: rapid compression warms the gas | Quantified for air (γ = 7/5). Halving the volume quickly raises T by 2^0.4 (300 → 396 K) and P to 2^1.4 ≈ 2.64 bar, above Boyle's 2 bar. The 3D box does exactly this, so its gauge and thermometer read the model. |
| §6: "50 % in kelvin vs 50 % in Celsius" | Made concrete. 300 → 450 K takes 2 L to 3 L (+50 %). 20 → 30 °C (also +50 % "in Celsius") is 293.15 → 303.15 K: +3.4 % in volume. |
| §6: extrapolation to −273.15 °C | Three samples with different slopes meet at zero volume. Red dots mark where real gases would condense first, and the screen says "ideal-gas extrapolation". |
| §7: no worked number | Added: a sealed container from 300 K to 360 K takes 1.00 bar to 1.20 bar. |
| §7: tyre example | No number is claimed. Tyre gauges read gauge pressure, not absolute pressure, and tyres stretch, so the scene shows only the needle rising, labelled "an estimate". |
| §8: 22.4 L vs 22.71 L | Kept: 22.71 L at 273.15 K and 1 bar; 22.41 L at 1 atm (1.013 bar). |
| §9: ρ = PM/RT | Worked both ways: N₂ 1.12 g/L and He 0.160 g/L at 1 bar and 300 K (ratio 7); and 1.12 g/L → 28 g/mol. |
| §10: Dalton | The worked example is kept. Each species' hits are *measured* in the mixed box (N₂ ≈ 2.1 × O₂, from 2:1 molecules and √(32/28) slower O₂). |

## Additions beyond the brief (all within NCERT Unit 5)

- Boyle's J-tube (1662): an extra 760 mm of mercury doubles the pressure and halves the trapped air.
- Density ∝ pressure at constant T; Everest's summit ≈ 0.337 bar (West, *J. Appl. Physiol.* 1999), "about a third" of sea level. Its O₂ partial pressure (≈ 0.07 bar vs 0.21) returns in Dalton's chapter.
- Isotherms at three temperatures; a hot-air balloon (Charles); a sealed, rigid gas cylinder (Gay-Lussac); breathing (Avogadro).
- One mole at 300 K and 1 bar fills 24.94 L, a cube about 29 cm on a side; R in L bar units (0.08314).
- The P–V–T surface of one mole, with the three laws as slices.

## Visual-model simplifications (named in concept_summary.md)

- The film's gas is the ideal model: point molecules that collide only with walls.
- On-screen speeds are scaled to be watchable. Ratios are exact: √(T/T_ref) on heating, √(M_ref/M) between gases.
- Force-time spikes are drawn wide enough to see; their areas are exact.
- The commuter crowd (scene 02) and mountain air column (scene 17) are qualitative schematics; neither encodes quantitative atmospheric dynamics.

## Length and pace

The derived film is 39:52 (planned 40:00). Chapter boundaries shift by up to
two minutes from the brief's table, because each chapter now runs exactly as
long as its narration and visual holds. It carries 4,808 words (≈ 120 per
finished minute). The brief targets 140–150 but asks for fewer on 3D and
calculation scenes; per-beat speech and pause estimates are in
`narration_cues.md`.

## Further scientific corrections from the complete scene review

- Dispersion: the 1/r⁶ expression and the factor of 64 apply to **interaction energy**; force has a different distance dependence.
- Hydrogen bonding: electron-poor hydrogen has a **partial positive charge**, not a bare proton. The water models now preserve a 104.5° H–O–H angle for all five molecules, while using approximate tetrahedral network coordination.
- Thermal energy: average translational energy is distinguished from the total sample energy and the molar scale RT. Kelvin is the SI absolute temperature scale.
- Momentum: the numerical collision illustration identifies its chosen speed as the perpendicular component vₓ. The plotted impulse areas are preserved through all six complete averaging intervals.
- Force traces are divided by each trace's own mean. Their axis is F/⟨F⟩: these compare relative fluctuations rather than absolute forces for different molecule counts. The plot identifies peaks clipped above 4; its mean refers to the complete, unclipped trace.
- The ideal-model transition now switches from the interacting Lennard-Jones simulation to the independent-particle GasBox model. The molecular-dynamics playback time advances monotonically.
- A loaded piston holds **external** pressure fixed. Internal pressure can temporarily exceed it while the piston accelerates. Charles and Avogadro compare balanced equilibrium states.
- Hot-air balloons release air and change the amount inside. Breathing starts with chest expansion, followed by a small pressure drop and incoming air.
- The constant-volume example uses a sealed gas cylinder; liquid propellants make aerosol cans a poor direct illustration of fixed-n ideal-gas P/T.
- Molar volume carries L mol⁻¹. Gas-law equations use absolute pressure, distinct from tyre gauge pressure.
- The gas-over-water diagram now has equal internal/external water levels, so the total pressure can be identified with atmospheric pressure without ignoring a hydrostatic head. The vapour pressure assumes saturation at the measured temperature.
- Maxwell–Boltzmann speed distributions occur **within** the classical ideal-gas model. A speed spread is not a failure of ideal-gas behavior.

Primary teaching references checked for these clarifications:
[OpenStax kinetic molecular theory](https://openstax.org/books/chemistry-2e/pages/9-5-the-kinetic-molecular-theory),
[OpenStax gas mixtures and collection over water](https://openstax.org/books/chemistry-2e/pages/9-3-stoichiometry-of-gaseous-substances-mixtures-and-reactions),
[OpenStax intermolecular forces](https://openstax.org/books/chemistry-atoms-first-2e/pages/10-1-intermolecular-forces), and
[IUPAC hydrogen-bond definition](https://publications.iupac.org/pac/pdf/2011/pdf/8308x1637.pdf).
