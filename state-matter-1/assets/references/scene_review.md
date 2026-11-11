# Complete scene review — The Molecular Dance

Reviewed against the supplied Class 11 lesson framework. The final script has
4,808 words and an estimated runtime of **39:52**. Speech and pauses are planned;
recorded narration still needs the existing `audio-check` workflow.

The explanatory detail belongs in the narration. On screen, the film retains
brief opening titles, molecular diagrams, compact labels, controlled conditions
and equations introduced after their physical meaning. Scene titles hold for
three seconds and fade over 0.7 seconds; there are no numbered chapter cards.

| Scene | Review and correction |
|---|---|
| 01 — Hook | Checked the balloon-to-molecular zoom and frame boundaries. Clarified opposing atmospheric forces and the net force from a pressure difference. |
| 02 — Collective behavior | Shortened the four question cards and the tracked-molecule label. Avoided presenting microscopic trajectories as fundamentally unknowable. |
| 03 — Inside / between | Distinguished intramolecular O–H bonds from interactions between waters. Qualified the bond-strength comparison to water; corrected the shared molecular geometry. |
| 04 — Dispersion | The factor of 64 is explicitly an interaction-energy change. Raised and shortened the noble-gas chart to clear lower labels. |
| 05 — Permanent dipoles | Checked attractive/repulsive orientations, 3D rotation, fixed-orientation 1/r³ energy and thermal averaging to 1/r⁶. |
| 06 — Hydrogen bonds | Replaced the “almost bare” hydrogen caption with partial-charge language. All waters now have 104.5° bond angles; network coordination remains approximate. |
| 07 — Repulsion | Checked the potential well, short-range repulsion, separation axis and cloud approach. The potential is an illustrative model. |
| 08 — Thermal motion | Distinguished average translational energy from sample energy and RT. Reduced velocity arrows and removed them before the distribution becomes the focus. |
| 09 — States and idealization | Removed the dim particle box behind the energy bars. Playback now advances forward. Transition now uses an actual independent-particle ideal model. |
| 10 — One wall | Labelled the example's normal velocity vₓ consistently; raised the opening question. Checked the reversal of only the perpendicular momentum. |
| 11 — Impulses to force | Raised the force graph. All six displayed impulses become complete equal-area rectangles, including the final interval. |
| 12 — Many impacts | Labelled the force curves F/⟨F⟩ and explained the normalization. Clarified pressure as momentum transferred per unit area per unit time. |
| 13 — The factor 1/3 | Raised and reduced the sample chart. Narration distinguishes finite-sample fluctuations from exact ensemble isotropy. The derivation remains three-dimensional. |
| 14 — Temperature to PV=nRT | Checked algebra and the N-to-n conversion. Raised the lower comparison captions. |
| 15 — Boyle | Checked fixed amount, constant temperature and the moving piston. Rescaled the impact-rate rail so both states do not saturate it; smoothed counters by elapsed time. |
| 16 — Boyle calculation | Checked 4 L at 1 bar to 2 L at 2 bar, reciprocal-volume graph and isotherms. |
| 17 — Density and rapid compression | Raised low captions and moved the control-condition prompt above the graph, clear of the thermometer. Checked that the rapid-compression trajectory lies above the isothermal curve. |
| 18 — Charles | Replaced “same pressure, always” with fixed external pressure. Equilibrium states follow V/T; transient overpressure drives the piston. Removed the Charles formula from the open hot-air-balloon application. |
| 19 — Absolute zero | Raised and reduced the graph to make room for both Celsius and Kelvin labels. Kept the ideal extrapolation and phase-change caveat. |
| 20 — Kelvin | Raised the chart baselines and shortened the bars, leaving space for the closing caption. Corrected the distinction between a Celsius number and absolute temperature. |
| 21 — Gay-Lussac | Raised the numerical answer; replaced the tiny verbal equation chain with a compact proportionality. Changed the application to sealed gas and made counter smoothing depend on time. |
| 22 — Compare heating | Moved “free piston” and “rigid walls” above the apparatus. Checked the different final responses and the tyre example's qualitative gauge reading. |
| 23 — Avogadro | Fixed the external-pressure label, raised the V–n graph and clarified equilibrium. Chest expansion now precedes the incoming-air animation. |
| 24 — Equal volumes | Raised the three boxes and gauges. Corrected the molar-volume unit to L mol⁻¹; retained the 1 bar versus 1 atm distinction. |
| 25 — One surface | Removed the dim miniature table before the equation. The previous slice disappears while the next law is explained; all slices return for the final overview. Kept the T label by the near part of its axis, clear of the projected surface. |
| 26 — Use the ideal equation | Checked R units, the combined law and the 3.33 L balloon result. Added the absolute-pressure requirement to narration. |
| 27 — Density / molar mass | Checked density units and both calculations. Made the nitrogen-to-helium density comparison explicit, raised the assumption cards and moved the balloon clear of the lower subtitle area. |
| 28 — Dalton | Checked independent contributions, mole fractions, the 2 + 1 bar example and oxygen partial pressures. Counter smoothing is independent of frame rate. |
| 29 — Collected over water | Matched inner and outer water levels before identifying total pressure with atmospheric pressure. Water and evaporation originate at the corrected level. Narration states saturation. |
| 30 — Model limits | Cleared the introductory chain before the detailed illustrations. Attraction arrows follow their particle and disappear after use; the dim comparison arrow is removed. A labelled finite-size packing schematic preserves separation and wall clearance. Explicitly stated that a speed distribution already exists in an ideal gas. |
| 31 — Closing card | Checked centering, spacing, final fade and the short narration. |

## Narration and render files

The corrected source is `narration.py`, with delivery cues in
`narration_delivery.py`. Clean and tagged scripts, all 31 per-scene texts,
per-beat texts and the JSON cue sheet are regenerated together using:

```bash
python main.py export --beats
```

The [README](../../README.md) contains separate complete command blocks for
480p previews and 2560 × 1440 final scene renders. Generated timing and chapter
markers are synchronized with the corrected script.

## Verification artifacts

- [All-scene overview](../../output/review/overview.png)
- [Storyboard contact sheets](../../output/review/storyboard/)
- [Final validation log](../../output/review/validation.log)
- [Validation scope and results](../../output/review/validation.json)

The scientific clarifications and primary teaching references are recorded in
[brief_review.md](brief_review.md). A full-resolution final film is a separate
rendering step; sampled storyboards and motion excerpts cannot guarantee every
frame of a 40-minute master.

Final verification completed on 2026-11-09: all 31 scenes pass sampled motion
and layout checks with zero final issues, and all scene timings pass at both
15 and 30 fps. The complete sequence constructs in 2392.47 seconds and leaves
zero stray graphics. Model checks, 64 spoken numbers, 19 scientific claims,
narration pacing and delivery anchors pass. Four short 480p motion excerpts
were rendered and inspected; the full master and recorded voiceover remain
separate production steps.

Motion excerpts: [ideal-model transition](../../output/review/motion/scene_09_ideal_transition.mp4),
[Boyle piston impacts](../../output/review/motion/scene_15_impacts.mp4),
[heated free piston](../../output/review/motion/scene_18_piston.mp4), and
[water levels](../../output/review/motion/scene_29_water_levels.mp4).
