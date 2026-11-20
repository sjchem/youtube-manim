# Review of the brief — Beyond Ideal Gases (States of Matter, Part 2)

The brief's eleven chapters, driving questions, teaching emphases and
checkpoints are kept. Every number below is recomputed by
`python -m utils.physics_models`, every spoken one is checked by
`python -m utils.spoken_numbers`, and the picture-to-model contracts by
`python -m utils.visual_contract_audit`.

## Engine choice

The brief prefers ManimGL for 3D. ManimGL 1.7 is installed, but the shared
Oceanic Next theme (`../themes`, via `manim_themes`) and the brief's own code
blocks are Manim Community Edition, and one `FullVideo` render cannot mix
engines. As in Part 1, the 3D comes from the projected-3D stage engine
(`manim_scenes/stage3d.py`): real rotating geometry with perspective, depth
sorting and lit spheres inside ordinary CE scenes. Part 2 extends it with
translucent spheres that split into back and front halves (so molecules sit
*inside* a forbidden zone or a velocity-space shell), a liquid pool with its
vapour (`TwoPhaseBox`), and live hard-sphere gases.

## Corrections and clarifications made in the film

| Brief | Film |
|---|---|
| §2A "a large collection prepared with the same speed" | Demonstrated, not asserted: a real 2D simulation of 240 elastic disks, all starting at one speed, relaxes to the 2D equilibrium (Rayleigh) distribution; energy is conserved to 10⁻³ and the distribution stops changing (`pm.verify`). Labelled "2D model" on screen, with the brief's 2D-vs-3D caution spoken. |
| §2B the u² factor | Derived visually in 3D: the velocity tips form a round cloud densest at the centre; counting tips in a thin shell (area 4πu²) times a fading cloud gives f(u). The full formula is shown as optional, not derived. |
| §2C numbers | N₂ at 300 K: u_mp 422, u_av 476, u_rms 517 m/s, said "about 420, 480, 520". M in kg mol⁻¹ (grams give speeds wrong by √1000 ≈ 32). |
| §2 "billions of collisions" | Checked: N₂ at 1 bar, 300 K collides ≈ 6.8 × 10⁹ times per second (kinetic diameter 0.364 nm). |
| §3 "molecular volume negligible" | Quantified for air: molecules (from b/4N_A) fill ≈ 0.04 % of the volume — "less than a thousandth". |
| §4B positive deviation | Demonstrated with a live hard-sphere gas beside a point-particle gas at equal count and speed: the hard spheres strike the walls measurably more often (`pm.verify` asserts > 1.25×). |
| §4A attraction | The single-tug picture is called a simplification of a mean-field average; the film never claims fewer molecules hit the wall. |
| §5A n² scaling | Counted: a seeded configuration where doubling the density takes nearby pairs from 33 to 141 (≈ 4×; the dense set contains the dilute one). |
| §5B b ≠ molecular volume | Shown geometrically: the forbidden sphere around a hard sphere has radius d (8 molecular volumes), shared by a pair → 4 per molecule. |
| §5 no worked example | Added: 1 mol CO₂ in 1 L at 300 K — ideal 24.94 bar, size correction alone 26.06 bar, attraction −3.64 bar, van der Waals 22.42 bar (10 % below ideal, Z ≈ 0.90); in 100 L the difference is 0.1 %. |
| §6 Z curves | NCERT's familiar figure draws CO₂ at 273 K as a continuous curve, but CO₂ condenses at about 35 bar at that temperature. The film draws Z at 300 K for CH₄, N₂, H₂ and He from the van der Waals model and says "model". |
| §6 Boyle temperature | Measured values quoted (N₂ 327.2 K, He 22.64 K; Atkins). The 3D Z surface is a reduced van der Waals fluid (its Boyle temperature is 27/8 T_c), so model and data are kept apart. |
| §7 Andrews | Isotherm temperatures are Andrews' (13.1, 21.5, 31.1, 35.5, 48.1 °C). Curves come from the van der Waals model with Maxwell's construction scaled to CO₂'s critical point, so their shape is qualitative; P_c and T_c are measured values. |
| §7 critical point and continuity | The van der Waals equation's own loops and Maxwell's equal areas show why a single fluid splits. T_c = 8a/27Rb is given with the honest note that tabulated a and b are often fitted to measured critical constants (CO₂'s give 304 K by construction). |
| §7F critical temperatures | Compared with room temperature: CO₂ (31 °C) can be liquefied by pressure alone at room temperature, as in the hook; N₂ (126 K ≈ −147 °C) must be cooled first; NH₃ 405.5 K. |
| §8 boiling | Antoine-equation vapour pressures: ether 34.6 °C, ethanol 78.3 °C, water 100.0 °C at 1 atm; Everest (0.337 bar) ≈ 72 °C, said "about seventy"; pressure cooker (2 bar absolute) ≈ 120 °C. |
| §8 sealed vessel | Revised the closed-vessel example: pressure is not fixed by the atmosphere and sealing alone does not forbid boiling; with a suitable fill the meniscus survives until the critical temperature, where it vanishes — tying chapter 8 back to chapter 7. |
| §9 surface tension | Energy first, "not an elastic skin"; γ(T) for water from the IAPWS correlation falls to exactly zero at T_c = 647.1 K (≈ 374 °C). Sphere vs cube of equal volume: 19.4 % less area ("about a fifth"). |
| §10 viscosity | Water 1.00 mPa s at 20 °C, 0.28 at 100 °C (CRC) — "less than a third"; honey 2–20 Pa s ("thousands of times"). Glass is an amorphous solid (the brief's correction of the older NCERT text). |

## Length and pace

The narration is updated during review; see `narration_cues.md` for the final word count and duration. Scene lengths are derived from the words
(2.6 words per second) plus stated visual holds, so the film's length follows
the script (see `python main.py list`). The brief targets 140–150 spoken words
per minute but asks for fewer on 3D structures and calculations; almost every
scene here is one, so the film averages about 120 words per finished minute,
matching Part 1. Per-beat speech and pause estimates are in `narration_cues.md`.

## Primary references

NCERT Chemistry Part I (Class 11), Unit 5; CRC Handbook of Chemistry and
Physics; Atkins' Physical Chemistry; T. Andrews, Phil. Trans. R. Soc. 159, 575
(1869); IAPWS Revised Release on the Surface Tension of Ordinary Water Substance
(2014); NIST Chemistry WebBook; [OpenStax Chemistry 2e, §9.5–9.6](https://openstax.org/books/chemistry-2e/pages/9-6-non-ideal-gas-behavior)
and [§10.2–10.3](https://openstax.org/books/chemistry-2e/pages/10-2-properties-of-liquids).


## Detailed revision, 16 November 2026

See [scene_review.md](scene_review.md) for the complete visual and scientific
review. The pressure reference, the limits of the Boyle-temperature tangent,
critical and supercritical conditions, finite-liquid requirement for saturated
vapour pressure, two-sided soap-film force, and honey/polymer distinction have
been corrected in both narration exports and the matching pictures.
Water saturation pressure now follows [IAPWS SR1-86(1992)](https://iapws.org/relguide/Supp-sat.html),
including its critical endpoint.
