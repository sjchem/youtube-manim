# Review — Chemical Bonding, Explained Visually

Reviewed against the supplied production brief and the preceding periodic-trends film.
The 18 scenes and planned 28:10 running time remain intact. The spoken script
contains 3,470 words, exported as one continuous paragraph per scene for ElevenLabs.

## Presentation and animation

- Kept the shared Oceanic Next palette and bold Lato type. Warm nuclei, cyan
  electron density, teal stabilisation, red repulsion and gold energy retain
  consistent meanings across the film.
- Shortened captions throughout. Labels name the visual idea; the narration
  explains the reasoning. Opening headings clear after the first few seconds.
- Replaced simultaneous overlapping caption changes with separate fade phases,
  particularly in the sigma/pi demonstrations and polarity continuum.
- Initialised hydrogen labels before their first fade, moved the sodium-energy
  callout into the empty part of the table, and separated the 74 pm label from
  graph ticks.
- Rebuilt the bond-order summary so moving H/O/N labels do not cross. Removed
  the small, shrunk reaction ledger from the final energy summary, which now
  retains a large equation and result.
- Kept the ionic energy ledger separate from the subsequent neighbour diagram;
  labelled the lattice balance's gaseous-atom starting state.
- Separated the electron-sea caption, simplified the bond-map legend, and fixed
  graph-label transitions in the bond-strength comparison.
- Corrected the common Cairo rendering path for rebuilt orbital surfaces.
  The normal flattened moving-object list retained detached old mesh faces
  during morphs, producing visible ghost orbitals. Surface animations now draw
  the current scene roots each frame. Other animations retain the static cache.
  The rendered control region went from 7,500 stale blue pixels to zero.
- Put whole-ion charge labels outside the electron cloud, so chloride's minus
  sign cannot be read as a negative nucleus.
- Removed the extra enlargement of water's O–H distances in the 3D teaser:
  CO₂ and H₂O now use the same length scale.

## Scientific corrections

- The misconception being crossed out is **breaking bonds releases energy**.
  The film no longer crosses out the broader statement that bonds store energy.
- The Morse well is identified as a schematic model from its first appearance.
  Its enthalpy-calibrated scale is distinguished from the true electronic well
  depth, zero-point dissociation energy and room-temperature bond enthalpy in
  the science notes. Bond formation must also dispose of excess energy.
- The H₂/Cl₂ reaction ledger is explicitly bookkeeping, rather than a claim
  that the reaction proceeds by breaking every bond before making new ones.
- Opposite spins are described in relation to a shared orbital/spin singlet,
  rather than a rule that same-spin electrons cannot occupy overlapping space.
  Spin arrows and moving position samples are identified as symbolic pictures.
- Orbital surfaces illustrate density and symmetry; they are not presented as
  an exact valence-bond or molecular wavefunction. The pi node belongs to that
  contribution, rather than to the total molecular density. The sigma/pi rule
  is scoped to the ordinary single, double and triple bonds being introduced.
- Differences between average carbon-bond enthalpies are no longer labelled
  as measured individual pi-bond energies. Large numerical comparisons show
  that the averages are not simple integer multiples.
- The lattice result starts from gaseous atoms; it is not NaCl's standard
  formation enthalpy from elemental sodium and chlorine. The Madelung factor
  describes an electrostatic contribution, not a complete lattice potential.
- Electronegativity difference is a qualitative guide to bonding character,
  rather than a quantitative ionic-percentage ruler.
- Copper is described through delocalised states, not a literal sequential
  donation of one free electron per atom. Electron drift is distinguished from
  conventional current.
- SF₆'s Lewis count is distinguished from its actual octahedral geometry and
  from a literal twelve-electron sulfur shell. The oxygen/magnet example keeps
  the limitation of the paired-electron Lewis picture explicit.

Direct supporting references and model boundaries are in
[concept_summary.md](concept_summary.md).

## Files for recording and rendering

- [Continuous narration](narration_script.md) and
  [individual plain-text scene files](assets/narration/) are regenerated from
  `narration.py`; timings remain separate in `narration_cues.md` and the JSON cue sheet.
- [README.md](README.md) has individual 480p, 1080p and 2K/QHD commands,
  plus full-film commands. `python main.py check` now includes both frame rates
  and intermediate-animation text checks.
- [youtube_package.md](youtube_package.md) recommends the series title
  **Chemical Bonding, Explained Visually** and groups the 18 rendered scenes
  into 10 YouTube upload chapters.

## Review artifacts and verification scope

- [All-scene visual overview](output/review/overview.png).
- [Rendered 3D sigma-overlap clip](output/review/sigma_overlap_480p.mp4):
  854×480, 15 fps, 10.8 seconds, including the corrected live mesh transition.
- [Detailed storyboard frames](output/review/storyboard/).
- [Validation results](output/review/validation.txt).

The checks cover model arithmetic, data consistency, narration pacing, sampled
text bounds/collisions, scene durations at preview and production frame rates,
and full-film scene/camera cleanup. They do not constitute a pixel render of
every frame of the entire 28-minute film. The full 2K export and synchronization
against the final recorded voice remain production steps.
