# Periodic Trends — revision review

Reviewed all 20 chapters against the attached continuation brief. The planned
length remains **23:40** and the film retains Part 3's Oceanic palette and Lato
letterforms.

## Presentation

- Shorter captions and three-word idea labels carry the screen; explanations
  remain in the continuous narration.
- Clean chapter headings replace the fuzzy glow. Direction arrows use bright
  magenta so they remain distinct from coloured data tiles.
- Block labels sit in the open space above the table, clear of element symbols.
- Replacing text fades out before new text fades in, including changing nucleus
  charges, radius readouts, chapter headings and heat-map tabs. This removes
  brief overlaps that were invisible in end-state stills.
- Atomic/ionic measurement labels share one bottom row. The 3D density surface
  and heat-map table leave room for captions. The salt crystal moves right
  before its explanation appears. The final atom reveal clears the table first;
  decorative atoms stay clear of the subscribe title.

## Scientific corrections

- The F/Cl close-up counts **five p electrons**, rather than confusing them with
  the seven total valence electrons. Its beads indicate occupancy, not paths.
- Neon does not end the attachment illustration with a stable bound Ne⁻ ion.
- Effective nuclear charge is described as charge after shielding.
- Probability dots are samples, not separate particles. The contour is a display
  guide; the scaled schematic does not compute each element's orbitals.
- Electronegativity difference indicates ionic character without a universal
  numerical cutoff. The density landscape is explicitly illustrative.
- Salt formation includes a complete energy balance, including atomization.
  The gas-phase transfer ledger now carries kJ/mol.
- The anion badge highlights a halogen rather than suggesting favourable
  attachment to nitrogen. Uncertain element classifications stay muted.
- Each finale tab displays its own property definition/units. Covalent-radius
  wording no longer persists over ionization or electronegativity data.

Primary references and data conventions are linked in
[concept_summary.md](concept_summary.md).

## Narration and rendering

Continuous chapter paragraphs have been regenerated in
[assets/narration](assets/narration), together with the full narration, master
script and separate cue sheets. The script contains **3,050 words**; every beat
passes the 2.75 words/second pacing limit. Existing chapter lengths are retained.

[README.md](README.md) now includes a complete command block for each chapter
at **480p / 15 fps** and **2K / QHD 1440p / 30 fps**, as well as 1080p and whole-film
commands. Each command also works individually.

## Validation

- All Python sources parse.
- Full scene review used Manim CE 0.19.2. Additional motion checks on the
  repository's CE 0.22.0 pass for chapters 01, 02, 15, 18 and 20, covering the
  new replacement animation, table labels, 3D HUD and closing card. The
  requirements range includes the installed version.
- The data audit checks 27 spoken values; maths, electron-configuration and
  probability-sampling checks pass.
- All 20 chapters pass the text layout check at animation endpoints and at
  quarter, half and three-quarter progress, after targeted spacing corrections.
- All chapter timing checks pass at 30 fps. FullVideo was constructed end to
  end: **1,420.13 seconds**, no stray objects, camera reset. Final local spacing
  and reveal changes were checked again per chapter.
- All chapters have been inspected as 854×480 storyboard stills; the revised
  landscapes and crystal have additional close-up reviews.
- Chapter 13 was rendered as a full **854×480 / 15 fps** video (66 seconds).
  A short rendered hook clip verifies the changing-label animation.

Text audits sample motion; they do not inspect every frame or every graphical
intersection. Visual review complements them. The entire final 2K movie has
not been rendered, and voice recordings have not been supplied. Record one
continuous chapter at a time and compare it with narration_cues.md before the
final audio render.

## Local previews

Generated previews are ignored by Git and can be recreated:

- [20-scene overview](output/review/overview.png)
- [Chapter 13: fluorine/chlorine, 480p](output/review/scene_13_480p.mp4)
- [Hook label transitions, 480p](output/review/hook_transitions_480p.mp4)
- [Validation summary](output/review/validation.txt)
