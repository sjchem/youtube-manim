# Molecular Geometry, Explained Visually

**Why is CO₂ straight, H₂O bent, and CH₄ a tetrahedron — and how can we
predict a molecule's shape just by looking at its electrons?** A 22-chapter
Manim film (planned running time **28:00**, 27:50 of story plus a subscribe
card), *Chemical Bonding · Part 2*, following
[`../chemical-bond`](../chemical-bond) ("Chemical Bonding, Explained
Visually"). Next in the series: *Molecular Orbital Theory, Explained
Visually*.

The story runs **2D Lewis structure → electron regions → 3D shape → orbital
hybridization → molecular polarity**, and treats VSEPR and hybridization as
two complementary explanations rather than two sets of rules.

- [`concept_summary.md`](concept_summary.md) — the science, each model's limits, sources
- [`animation_plan.md`](animation_plan.md) — chapter-by-chapter visuals
- [`narration_script.md`](narration_script.md) — full timestamped script (3,648 words); beat timings in [`narration_cues.md`](narration_cues.md); ElevenLabs-tagged version in [`narration_script_tagged.md`](narration_script_tagged.md)
- [`revision_review.md`](revision_review.md) — review changes, validation and previews
- [`youtube_package.md`](youtube_package.md) — titles, description, chapters, tags, thumbnail idea

## Why Manim CE (and not ManimGL)

The brief prefers ManimGL for 3D. This film is built on **Manim Community
Edition** on purpose:

* the channel's shared Oceanic Next theme (`../themes/oceanic_next.py`) is
  written against CE through `manim_themes`, so a ManimGL scene could not use
  the house look that ties the series together;
* the single-scene full-film render (`FullVideo`) needs one engine;
* in this environment ManimGL lives only in a separate Python env.

The 3D comes from a small projection engine instead
([`manim_scenes/stage3d.py`](manim_scenes/stage3d.py)). Every molecule,
electron region and orbital keeps true 3D coordinates; each frame a `Stage`
turns them (yaw, pitch, model rotation, gentle sway), projects them with
perspective, sorts them back to front and redraws smooth shapes:

* atoms are polished spheres (nested shading contours, no faceting) whose
  element symbols turn with them;
* electron regions are translucent ellipsoids whose projected outlines are
  computed exactly — cyan for bonds, fatter purple for lone pairs;
* orbitals are the silhouettes of computed lobe surfaces, lit toward their tips,
  blue where ψ > 0 and rose where ψ < 0;
* angle arcs, dipole arrows and labels ride on top and never shrink.

Compared with CE's `ThreeDScene`, this keeps spheres and lobes smooth in Cairo,
keeps every caption an ordinary 2D object (no fixed-in-frame pitfalls), and is
cheap enough that every model keeps slowly turning — no shot is static.

## Everything on screen is computed

* **VSEPR arrangements** come from a literal relaxation: n unit vectors on a
  sphere under a 1/d repulsion follow the gradient flow (`utils/physics_models.py`).
  Chapters 03, 09 and 11 replay those paths, and the self-check confirms they
  find the linear, trigonal planar, tetrahedral, trigonal bipyramidal and
  octahedral arrangements — from the film's starts and from random ones.
* **Lone-pair sites** are chosen by counting crowded 90° contacts;
  `best_lone_pair_sites` returns every optimal placement and each molecule's
  layout is asserted to be one of them (equatorial in the bipyramid, trans in
  the octahedron).
* **Molecules** (`utils/molecule_library.py`) derive their lone-pair count from
  valence electrons, take measured angles from `utils/geometry_data.py`, and
  name their own shape from their own coordinates.
* **Hybrids** (`utils/orbital_models.py`) are ψ = cos α ψₛ + sin α ψₚ; the
  check verifies orthonormality and cos θ = −1/n for sp, sp², sp³.
* **Spoken numbers** — 25 claims in `narration.py` — are checked against the
  data by `python -m utils.geometry_data`.

## Setup

From this folder:

```bash
pip install -r requirements.txt
```

You also need FFmpeg/ffprobe, LaTeX with dvisvgm, Cairo/Pango and the Lato font
(see `requirements.txt`), plus the repository's shared `themes/` folder one
level up. `config.py` adds the repository root to `sys.path`, so the theme
imports from inside this sub-folder. Built and checked with Manim CE 0.22.0.

## Preview and render

```bash
python main.py list                # chapter names, start times and durations
python main.py preview 07          # one chapter at 854×480, 15 fps
python main.py preview all         # separate previews of all 22 chapters
python main.py preview full        # the full film at preview quality
python main.py scene 07            # one chapter at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
python main.py check               # every model, data, narration, timing and layout audit
python main.py audio-check         # recorded narration clips vs chapter lengths
```

### 2K / 1440p: all 22 scenes in one batch

For this YouTube video, 2K means **2560×1440 at 30 fps**. From the
`molecular-geometry` folder, activate your Manim environment and paste this
whole block. It renders scenes 01–22 sequentially as separate MP4 files and
stops if a render fails.

```bash
set -e
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_shape_mystery.py Scene01ShapeMystery
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_lewis_is_flat.py Scene02LewisIsFlat
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_regions_repel.py Scene03RegionsRepel
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_counting_regions.py Scene04CountingRegions
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_linear_planar.py Scene05LinearPlanar
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_tetrahedron.py Scene06Tetrahedron
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_ammonia.py Scene07Ammonia
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_water.py Scene08Water
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_five_regions.py Scene09FiveRegions
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_tbp_family.py Scene10TbpFamily
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_six_regions.py Scene11SixRegions
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_flat_from_six.py Scene12FlatFromSix
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_mixing_orbitals.py Scene13MixingOrbitals
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_sp2_sp3.py Scene14Sp2Sp3
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_methane_ethene.py Scene15MethaneEthene
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_two_models.py Scene16TwoModels
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_bond_dipoles.py Scene17BondDipoles
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_symmetry_polarity.py Scene18SymmetryPolarity
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_predict.py Scene19Predict
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_big_picture.py Scene20BigPicture
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_oxygen_magnet.py Scene21OxygenMagnet
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_22_subscribe.py Scene22Subscribe
```

The videos are saved under
`media/videos/<scene_file>/1440p30/<SceneClass>.mp4`.
To render just one scene, copy its individual command from the block above.

For one combined 2K film:

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/full_video.py FullVideo
```

### Each chapter directly with Manim (480p preview)

```bash
manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_shape_mystery.py Scene01ShapeMystery
manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_lewis_is_flat.py Scene02LewisIsFlat
manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_regions_repel.py Scene03RegionsRepel
manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_counting_regions.py Scene04CountingRegions
manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_linear_planar.py Scene05LinearPlanar
manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_tetrahedron.py Scene06Tetrahedron
manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_ammonia.py Scene07Ammonia
manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_water.py Scene08Water
manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_five_regions.py Scene09FiveRegions
manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_tbp_family.py Scene10TbpFamily
manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_six_regions.py Scene11SixRegions
manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_flat_from_six.py Scene12FlatFromSix
manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_mixing_orbitals.py Scene13MixingOrbitals
manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_sp2_sp3.py Scene14Sp2Sp3
manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_methane_ethene.py Scene15MethaneEthene
manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_two_models.py Scene16TwoModels
manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_bond_dipoles.py Scene17BondDipoles
manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_symmetry_polarity.py Scene18SymmetryPolarity
manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_predict.py Scene19Predict
manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_big_picture.py Scene20BigPicture
manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_oxygen_magnet.py Scene21OxygenMagnet
manim -ql --fps 15 -r 854,480 manim_scenes/scene_22_subscribe.py Scene22Subscribe
```

Replace `-ql --fps 15 -r 854,480` with `-qh --fps 30 -r 1920,1080` for a
1080p chapter.

### Final 1080p film

```bash
manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo
```

(identical to `python main.py render`). Every frame is redrawn because the
models keep turning; expect a long render — preview single chapters first.

## Narration and voice

`narration.py` is the timing source: each chapter is a list of
`(start second, sentence)` beats, and scenes hold on them with
`beat(scene, t, i)`. The cloned voice reads ~100 words per 35 s (2.86 w/s);
`python -m utils.narration_audit` refuses any beat faster than 2.85 w/s, and
the film averages 2.17 w/s, leaving room to breathe.

```bash
python -m utils.narration_export   # regenerates narration_script*.md, narration_cues.md, assets/narration/
```

* `assets/narration/scene_XX.txt` — clean prose, one clip per chapter;
* `assets/narration/elevenlabs/scene_XX.txt` — with sparse ElevenLabs v3/v4
  delivery tags (`narration_delivery.py`); tags never change the words;
* **pronunciation:** add an ElevenLabs pronunciation-dictionary alias
  `VSEPR → vesper`. Hybrid labels are already written "S P three" and codes
  "A X three E" so the voice reads them as letters.

At that voice speed, the 3,648-word script contains about **21:17 of speech**
inside a **28:00 visual edit**. The remaining time is distributed between
morphs, rotating structures, viewer predictions and the closing card. A
continuous TTS paragraph will not automatically land on the visual cues.

Choose either recording workflow for each scene:

* **Edited scene recording:** save `assets/audio/scene_01.wav` (or `.mp3` /
  `.m4a`), with pauses placed against `narration_cues.md`.
* **Automatic cue placement:** run `python -m utils.narration_export --beats`.
  Clean text appears in `assets/narration/beats/scene_01/`; tagged text in
  `assets/narration/elevenlabs/beats/scene_01/`. Record each file at your
  normal pace and save the audio as `assets/audio/scene_01/beat_001.wav`,
  `beat_002.wav`, and so on. The scene places each recording at its cue and
  uses the rest of that window as a visual pause. Text and audio use the
  same beat numbers. Complete a scene's whole beat set before rendering it.

`python main.py audio-check` measures recordings with ffprobe. It rejects
missing beats in a partial set, duplicate formats, mixed recording modes,
and speech that crosses the next cue or closing fade. It never stretches
or speeds up your voice. Actual recorded durations are the final timing
check; word-count estimates cannot account for every pronunciation or tag.
Silent previews work before recordings are supplied.

## Checks and review tools

```bash
python main.py check                         # all of the below, in order
python -m utils.math_utils                   # vectors, rotations, projection, hull
python -m utils.physics_models               # repulsion relaxation, lone-pair rule, shape naming, cube
python -m utils.orbital_models               # hybrid orthonormality, cos = -1/n, lobe shapes
python -m utils.molecule_library             # 15 molecules: AXmEn, shapes, measured angles
python -m utils.geometry_data                # 25 spoken claims vs measured data
python -m utils.narration_audit              # every beat speakable in its window
python -m utils.timing_audit [--fps 30]      # every chapter lands on its second
python -m utils.timing_audit --full          # FullVideo end to end, 0 stray mobjects
python -m utils.layout_audit --motion        # no text overlaps / crowding / off-frame text
python -m utils.storyboard 07 --every 3      # PNG stills without rendering video
python -m utils.contact_sheet scene_07       # tile them into one review sheet
```

## Plugins

None are required. `manim-chemistry` was considered for molecules but draws
static structures from `.mol` files; this film needs one central model that
morphs site by site, live angle readouts and lone-pair lobes, so the
stage engine is used throughout. `manim-voiceover` was not needed: the
beat/cue system plus recorded clips keeps narration and picture in sync
without a TTS dependency at render time.

## Project structure

```
molecular-geometry/
├── main.py                  list / preview / scene / render / check / audio-check
├── config.py                palette and colour meanings, fonts, durations, theme, seed
├── narration.py             timed narration beats (the timing source)
├── narration_delivery.py    ElevenLabs delivery tags
├── narration_script.md      exported script (+ _tagged), narration_cues.md
├── concept_summary.md · animation_plan.md · youtube_package.md
├── requirements.txt
├── manim_scenes/
│   ├── stage3d.py           projected 3D engine: Stage, Ball, Rod, Lobe, Blob, arcs, vectors
│   ├── common.py            lifecycle, type, Lewis structures, MoleculeModel, RegionModel, orbitals
│   ├── full_video.py        FullVideo: all 22 chapters in one scene
│   └── scene_01_… – scene_22_…
├── utils/
│   ├── math_utils.py        vectors, rotations, projection, ellipsoids, hull, colour
│   ├── physics_models.py    VSEPR repulsion, lone-pair placement, shape naming, dipoles, cube
│   ├── orbital_models.py    hybrid wave functions, polar plots, isosurface cross-check
│   ├── molecule_library.py  every molecule from valence counts + measured data
│   ├── geometry_data.py     measured angles, lengths, electronegativities, dipoles + spoken checks
│   ├── render_helpers.py    safe-frame fitting
│   ├── timing_audit.py · layout_audit.py · narration_audit.py · narration_export.py
│   ├── storyboard.py · contact_sheet.py · voiceover.py
├── assets/{audio,images,references,sounds,textures,narration}/
├── media/                   Manim output (not committed)
└── output/                  storyboards and review sheets (not committed)
```
