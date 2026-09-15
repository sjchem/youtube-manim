# Why Electrons Don't Orbit the Nucleus — Part 2

A nineteen-chapter Manim Community Edition sequel. Planned runtime **35:20**, spoken narration **4,855 words**.
One question carries the film:

> If electrons do not move in classical orbits, how does quantum mechanics describe where they can exist?

**Orbit → matter wave → uncertainty → wave function → probability → orbital → quantum numbers → electron filling → chemistry.**

Quantum numbers are introduced only after the distinctions they name are already visible on screen. Aufbau, Pauli
and Hund arrive through the act of building atoms rather than as rules to memorise, and the comparison of neon with
sodium connects the diagrams to chemistry.

Chapter 3 is the hinge. It banks four of Bohr's numbers — a radius, an energy, a speed and the 2n² capacity — while
the model still looks convincing, and every later chapter spends one of them. The first-shell speed becomes a de
Broglie wavelength in chapter 4; that wavelength turns out to be *exactly* the first orbit's circumference in
chapter 6, so `2πr = nλ` reproduces the postulate Bohr could only assume; the radius and speed are the pair
uncertainty forbids in chapter 7; the radius returns as the peak of the radial distribution in chapter 11; and
`2, 8, 18` is re-derived from `1 + 3 + 5 = n²` orbitals in chapter 12. `utils/audit.py` pins all of them.

## Start here

- **Motion preview** — `python -m manim -ql --fps 12 --media_dir output/review utils/visual_preview.py VisualPreview` renders a short unsynchronised pass over the whole visual spine. Rendered output is gitignored, so it is produced locally.
- [Narration](narration_script.md) — the full spoken screenplay and its contiguous chapter windows.
- [Voice-ready text](assets/narration/full_narration.txt) and [individual chapters](assets/narration/).
- [Animation plan](animation_plan.md) — the anchor each chapter receives, what it does with it, and what it hands on.
- [Architecture](architecture.md) — file structure, continuity, the numerical pipeline, and why the shading works the way it does.
- [Science notes](concept_summary.md) — sources, and the limits of each illustration.
- [Recording guide](voiceover_guide.md) — pronunciation and alignment points.
- [Verification](verification.md) — what has been checked, and what has not.

## Run

Use Python 3.12 and the `youtube` pyenv, as in Part 1.

```bash
python -m pip install -r requirements.txt
python main.py list
python main.py preview 07      # the uncertainty chapter
python main.py preview 11      # the orbital shapes
python main.py preview 12      # the quantum-number address
python main.py preview 17      # potassium and Madelung's rule
python main.py preview 19      # separate subscribe card
```

FFmpeg, LaTeX and dvisvgm are needed for video and equations. This project uses **Manim CE**, not ManimGL. It is
self-contained: it does not import Part 1 or the repository's `themes` package. `scikit-image` extracts the
isodensity surfaces and SciPy supplies the radial and angular functions.

Individual previews render at **854 × 480, 15 FPS** over the full narration duration. For a **2560 × 1440, 30 FPS**
chapter or the whole film:

```bash
python main.py scene 11
python main.py render
```

### Direct Manim commands

Run these from `atomic-structure-2`. Copy one block to render all 19 scenes at that resolution.
The `-p` flag opens each finished video in your default player; omit it when rendering without a desktop player.

#### 480p previews — 854 × 480, 15 FPS

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_where_is_it.py Scene01WhereIsIt
python -m manim -pql --fps 15 manim_scenes/scene_02_what_survives.py Scene02WhatSurvives
python -m manim -pql --fps 15 manim_scenes/scene_03_bohr_numbers.py Scene03BohrNumbers
python -m manim -pql --fps 15 manim_scenes/scene_04_matter_waves.py Scene04MatterWaves
python -m manim -pql --fps 15 manim_scenes/scene_05_one_at_a_time.py Scene05OneAtATime
python -m manim -pql --fps 15 manim_scenes/scene_06_waves_that_fit.py Scene06WavesThatFit
python -m manim -pql --fps 15 manim_scenes/scene_07_uncertainty.py Scene07Uncertainty
python -m manim -pql --fps 15 manim_scenes/scene_08_allowed_states.py Scene08AllowedStates
python -m manim -pql --fps 15 manim_scenes/scene_09_born_probability.py Scene09BornProbability
python -m manim -pql --fps 15 manim_scenes/scene_10_orbit_to_orbital.py Scene10OrbitToOrbital
python -m manim -pql --fps 15 manim_scenes/scene_11_orbital_shapes.py Scene11OrbitalShapes
python -m manim -pql --fps 15 manim_scenes/scene_12_quantum_address.py Scene12QuantumAddress
python -m manim -pql --fps 15 manim_scenes/scene_13_energy_landscape.py Scene13EnergyLandscape
python -m manim -pql --fps 15 manim_scenes/scene_14_building_atoms.py Scene14BuildingAtoms
python -m manim -pql --fps 15 manim_scenes/scene_15_filling_p.py Scene15FillingP
python -m manim -pql --fps 15 manim_scenes/scene_16_chemistry.py Scene16Chemistry
python -m manim -pql --fps 15 manim_scenes/scene_17_potassium.py Scene17Potassium
python -m manim -pql --fps 15 manim_scenes/scene_18_answer.py Scene18Answer
python -m manim -pql --fps 15 manim_scenes/scene_19_subscribe.py Scene19Subscribe

# Alternatively, render the continuous full film instead of separate scenes:
# python -m manim -pql --fps 15 manim_scenes/full_video.py FullVideo
```

#### 2K renders — 2560 × 1440, 30 FPS

```bash
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_01_where_is_it.py Scene01WhereIsIt
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_02_what_survives.py Scene02WhatSurvives
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_03_bohr_numbers.py Scene03BohrNumbers
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_04_matter_waves.py Scene04MatterWaves
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_05_one_at_a_time.py Scene05OneAtATime
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_06_waves_that_fit.py Scene06WavesThatFit
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_07_uncertainty.py Scene07Uncertainty
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_08_allowed_states.py Scene08AllowedStates
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_09_born_probability.py Scene09BornProbability
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_10_orbit_to_orbital.py Scene10OrbitToOrbital
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_11_orbital_shapes.py Scene11OrbitalShapes
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_12_quantum_address.py Scene12QuantumAddress
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_13_energy_landscape.py Scene13EnergyLandscape
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_14_building_atoms.py Scene14BuildingAtoms
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_15_filling_p.py Scene15FillingP
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_16_chemistry.py Scene16Chemistry
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_17_potassium.py Scene17Potassium
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_18_answer.py Scene18Answer
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_19_subscribe.py Scene19Subscribe

# Alternatively, render the continuous full film instead of separate scenes:
# python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/full_video.py FullVideo
```

`FullVideo` keeps its anchor between chapters, so the joins are transformations. Rendering chapters separately is
convenient for revision, but concatenating those files is not equivalent to the continuous render.

The 3D chapters are the expensive ones: each orbital is a few thousand individually depth-sorted and individually
lit triangles. Budget accordingly, and prefer `preview` while iterating.

## Equations and scientist portraits

Chapters 4, 7 and 8 connect de Broglie, Heisenberg and Schrödinger through calculated examples, with brief historical portrait introductions:

- Electron speed doubles: wavelength falls from approximately 0.727 to 0.364 nm.
- Position spread halves from 100 to 50 pm: the minimum momentum spread doubles.
- The Schrödinger operator gives hydrogen's 1s and 2p wave functions together with -13.6 and -3.40 eV.

[Science notes](concept_summary.md) explain the approximations; [portrait credits](assets/images/README.md) record sources and reuse statements.
A continuous, silent review of chapters 04–08 runs at three times production pace:

```bash
ATOM_REVIEW_SPEED=3 python -m manim -ql --fps 12 --media_dir output/equation_motion utils/equation_preview.py EquationPreview
```

## Revised ending preview

The final six chapters (14–19) run continuously in a dedicated preview, with their actual **6:35** narration window:

```bash
python -m manim -ql --fps 12 --media_dir output/ending_motion utils/ending_preview.py EndingPreview
```

The current cut has 19 chapters and runs **35:20**. The recap is chapter 18; the separate subscribe card is chapter 19. The detailed
Cr/Cu chapter is preserved under `assets/references/next_video/` for the periodic-table sequel.

## Compressed visual review

```bash
python main.py review 09
python main.py review
```

Review mode compresses every narration window and writes under `media/review/`. It is for inspecting motion, never
for synchronising against a recorded voice. Frame rounding can stretch short transitions past the nominal factor.

The dedicated [visual preview](utils/visual_preview.py) runs the principal transformations at a readable pace:

```bash
python -m manim -ql --fps 15 utils/visual_preview.py VisualPreview
```

## Expanded chemistry explanation

The audience is senior secondary / introductory university chemistry. The existing 19-chapter sequence is retained.
[Teaching and reference notes](assets/references/expanded_explanation.md) describe the scientific distinctions and worked examples.

- Chapter 5 builds individual detections into interference, then starts a fresh run with path information.
  Both patterns use the same diffraction envelope; the detector removes the interference term.
- Chapter 11 links the 1s density slice to a radial curve and a moving spherical boundary:
  32.3% inside one Bohr radius, 90% inside approximately 2.66 Bohr radii.
- Chapter 12 connects shape and magnetic labels to angular momentum and spin projections.
  Shell capacities follow from state counting and Pauli exclusion.
- Narration distinguishes the ring analogy, a classical statistical analogy, and approximate many-electron energies.

Focused motion review of the radial example:

~~~bash
python -m manim -ql --fps 15 --media_dir output/depth_motion utils/depth_preview.py RadialProbabilityReview
~~~

## Checks

```bash
python utils/narration_export.py            # regenerate the voice-ready text
python utils/narration_export.py --check    # fail if the exports are stale
python utils/audit.py --science-only
python utils/audit.py                       # every chapter, standalone
python utils/audit.py --full --fps 30       # the continuous film
python utils/audit.py --storyboard          # also write rendered endpoint frames
python -m compileall -q config.py main.py manim_scenes utils
```

The audit runs the real animations and inspects them at their endpoints, without rasterizing every frame. It checks
radial normalization, the 2s node, the p nodal plane, the Gaussian uncertainty product, sampling statistics,
enclosed surface probability and every H–Ar occupancy constraint; then narration order, windows and speaking rates;
then each chapter's duration, its text bounds and text collisions, and that no chapter ends with anything visible
outside its anchor. Watching video is still the only way to judge the transformations in between.

## What these pictures are and are not

Surfaces and density maps are numerically calculated visualizations. Mesh resolution and finite grids limit their
precision, and a surface is a chosen isodensity threshold, not the edge of an atom. Nucleus sizes, chart energies
and many-electron density views are schematic. Read the science notes before reusing a frame out of context.

Narration ships as editable text and speech-only exports; no recorded or cloned speech is included. Align measured
narration in the editor, or update the chapter's `at()` marks, before producing a voiced master. Rendered output is
excluded from Git by design.
