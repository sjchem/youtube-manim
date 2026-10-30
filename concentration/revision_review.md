# Concentration film review — 28 October 2026

Reviewed the attached brief, all 21 scenes, the shared 3D renderer, numerical
models, and the complete narration. The film retains its **35:00 structure**,
21 scenes and 12 chapter divisions. The reference solution remains 18.0 g
glucose plus 180.0 g water with an illustrative measured final volume of
191.0 mL.

[Visual overview](output/review/2026-10-28/overview.jpg) ·
[Machine-readable results](output/review/2026-10-28/review_summary.json)

![Selected reviewed scenes](output/review/2026-10-28/overview.jpg)

## Corrections that affect the explanation

- **Density conversion:** keep guard digits through the one-litre calculation.
  It now shows **1036.6 − 94.2 ≈ 942.4 g** of solvent, then divides by
  **0.9424 kg**. The conversion formula now includes an explicit unit key
  (c in mol/L, density in kg/L, molar mass in kg/mol), and its denominator
  labels specify masses per litre. The earlier display rounded the first two masses too soon
  and showed an inconsistent subtraction. The underlying exact model still
  gives 0.556 mol/kg.
- **Normality:** use **N = M × z**, where z means equivalents per mole for the
  stated reaction. This avoids confusing that multiplier with IUPAC's
  reciprocal equivalence-factor convention. One mole of proton equivalents
  is one equivalent in this acid–base example. The 0.500 M label explicitly
  describes the **original acid stock before adding base**. The structural
  cartoon tracks proton equivalents; aqueous sulfuric acid contains ions.
- **Temperature and phases:** unchanged molality and mole fraction require
  unchanged liquid composition. Ice formation or solvent loss can change the
  composition of the remaining liquid. The heating demonstration retains its
  closed sample with expansion headspace and explicitly uses a water-like
  expansion model.
- **Mole-fraction sampling:** random picks are independent and with
  replacement. A glucose pick takes 101 picks **on average**, not as a
  guaranteed outcome. The displayed sampling population is still one glucose
  to 100 water molecules.
- **Preparing solutions:** dissolve fully and return to the flask's calibration
  temperature before making up to final volume. A litre at the reference
  molarity is imagined from a larger batch of the same composition.
- **General wording:** percent can express tiny amounts; ppm is more convenient
  for them. Adding solute does not universally increase volume. The packing
  metaphor illustrates contraction without treating molecules as rigid balls
  filling fixed holes. Normality adds a reaction condition to the usual
  concentration comparison.

## Visual work and scene coverage

The existing projected 3D molecules, glasses and cubes remain the structural
foundation. Shared improvements add glass reflections, double rims, base
highlights, liquid shading, and depth-shaded particle highlights. Their
projected geometry follows the existing rotation and liquid-volume model.
Balance hardware has metal facets; the percent bottle has curved highlights
and a ribbed cap. Vapour reservoirs now read as cylindrical liquid cutaways.
The close-up ppm particle uses a shaded sphere with a specular highlight,
while retaining the exact million-dot population at the wide view.

| Scene | Review outcome |
|---|---|
| 01 — Mystery | Retained the four-answer reveal; improved glass and particle depth; changed “different units” to “different comparisons.” |
| 02 — Counting moles | Verified masses, molar masses and counts; improved balance shading. |
| 03 — Volumes do not add | Clarified the contraction metaphor and the scope of concentration definitions. |
| 04 — Molarity | Corrected the imagined litre to come from a larger batch; clearer shared glass rendering. |
| 05 — Volumetric flask | Clarified cooling before final adjustment; improved neck, rim, liquid and reflection cues. |
| 06 — Molality | Verified solvent-mass denominator and the 0.556 mol/kg comparison. |
| 07 — Colligative properties | Verified dilute non-electrolyte calculations; clarified the phase/composition condition. |
| 08 — Heating | Checked live volume and concentration readouts; clarified the closed sample and headspace. |
| 09 — Both measures | Checked dilute-limit comparison and the labelled model's assumptions. |
| 10 — Normality | Corrected amount/equivalent wording and z notation; added an aqueous-ionisation caption that fades before the concluding arrows. |
| 11 — Two reactions | Clarified proton-equivalent bookkeeping and original-stock labels; checked molecular transfer animation. |
| 12 — Mole fraction | Corrected sampling conditions, expectation wording and fixed-composition caption. |
| 13 — Fractions sum to one | Verified sums and ideal Raoult-law ratio; improved liquid cutaways and surface depth. |
| 14 — Mass percent | Verified solution-mass denominator; improved bottle and balance materials. |
| 15 — Volume percent | Verified ethanol is made up to final solution volume; improved shared flask rendering. |
| 16 — ppm/ppb | Clarified percent wording; improved sphere shading; retained exact populations and stated measurement bases. |
| 17 — Density bridge | Fixed displayed rounding/subtraction, solvent denominator and unit key; corrected the representative swarm to a 1:100 ratio. |
| 18 — Dilution | Verified final-volume calculation and conservation of all 20 representative solute beads. |
| 19 — Traps | Corrected the universal-expansion claim and reaction-multiplier notation. |
| 20 — Map | Normality now says “eq/L for a stated reaction”; checked node spacing. |
| 21 — Ending | Retained the clear, uncrowded end card and timing. |

The charts, formulas and labels remain flat for legibility. Extra orbital-like
surfaces or moving captions would make these ratio comparisons harder to read.

## Narration and recording

The revised clean narration contains **3,936 words in 230 timed beats**, within
the brief's 3,500–4,000-word budget. The fastest beat is about **2.57 words/s**,
below the estimated natural voice pace of 100 words in 35 seconds.

At that voice pace, speech occupies approximately **23 minutes**, with about
**12 minutes distributed across demonstrations, calculations, predictions,
transitions and visual holds**. These are estimates, not measured audio.
The film is not meant to be 35 minutes of uninterrupted TTS.

Regenerated the clean and tagged scene scripts, individual beat scripts,
Markdown scripts, and JSON/Markdown cue sheets. Every export matches the
source narration and all delivery anchors resolve. Prefer the **per-beat
recordings** for alignment. A continuous scene recording needs the cue-sheet
holds inserted internally; pause tags do not guarantee exact timing.

No voice recordings were present, so pronunciation, expression and actual
recorded duration still need checking when the clips are generated.

## Validation and previews

- Mathematical, physical and spoken-number checks passed.
- All 21 scenes constructed; sampled text overlap/safe-frame checks, including
  samples during movement, report **zero issues**. Individual timings are
  within one 30 fps frame of their targets.
- FullVideo constructed end to end at **2100.00 seconds**, with **zero stray
  scene objects** after the final transition.
- Source syntax and all scene/beat narration exports passed verification.
- Reviewed scene contact sheets and rendered four native motion excerpts:
  [dissolving glass](output/review/2026-10-28/scene_01_dissolving_glass.mp4),
  [thermal expansion](output/review/2026-10-28/scene_08_thermal_expansion.mp4),
  [proton transfer](output/review/2026-10-28/scene_11_proton_transfer.mp4), and
  [dilution fill](output/review/2026-10-28/scene_18_dilution.mp4).

The review folder contains all 21 contact sheets and check reports. Motion
excerpts use 15 fps at preview resolution (opening glass: 1280×720; other
excerpts: 854×480). A complete final-resolution video has **not** been rendered.
The [README](README.md) includes a single batch command for all 21 scenes at
2560×1440, 30 fps, as well as a joined-film command.

## References used for the chemistry review

- IUPAC Gold Book: [amount concentration](https://goldbook.iupac.org/terms/view/A00295/plain),
  [molality](https://goldbook.iupac.org/terms/view/M03970), and
  [amount fraction](https://goldbook.iupac.org/terms/view/A00296).
- [IUPAC Orange Book: the equivalence concept and normality](https://publications.iupac.org/analytical_compendium/Cha06sec3.pdf).
- [OpenStax Chemistry 2e: colligative properties](https://openstax.org/books/chemistry-2e/pages/11-4-colligative-properties),
  including ideal-solution assumptions and the effect of solvent phase changes.
- [NOAA Global Monitoring Laboratory: global CO₂](https://gml.noaa.gov/ccgg/trends/gl_trend.html?simple=True),
  supporting the film's broad “above 400 ppm” example.

Existing density and thermal-property tables remain documented in
`utils/concentration_data.py` and `concept_summary.md`; the supplied 191.0 mL
reference volume remains an explicit illustrative input.
