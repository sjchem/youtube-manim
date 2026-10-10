# Periodic Trends, Explained Visually

**Why do atoms get smaller across the periodic table but larger down it — and
how does that change their chemistry?** A 20-chapter Manim film (planned
running time **23:40**), *Atomic Structure · Part 4*, the direct sequel to
[`../periodic-table`](../periodic-table) ("Why Does the Periodic Table Have This
Shape?"). Part 3 explained the table's shape; this film shows why that shape is
useful: the arrangement of electrons predicts how atoms behave.

Every trend is built from three questions about the outer electrons — *how far
are they, how strongly does the nucleus pull, how are they arranged* — before
any summary arrow appears. See [`concept_summary.md`](concept_summary.md) for
the science and sources, and [`animation_plan.md`](animation_plan.md) for the
chapter-by-chapter visuals. The latest presentation and science review is in
[`revision_review.md`](revision_review.md).

## Why Manim Community Edition, not ManimGL

The brief asked to prefer ManimGL. In this environment ManimGL is only
installed in the separate `youtube` pyenv environment, and the channel's shared
theme (`../themes/oceanic_next.py`, built on `manim-themes`) only works with
Manim CE. A ManimGL scene could not use the house Oceanic theme, and mixing
engines would stop `full_video.py` from rendering the film as one scene. So the
whole film uses Manim CE. Real 3D comes from `ThreeDScene` in chapters 06 (shell
spheres), 10 (the ionization mountain range), 15 (the electron-density
landscape) and 18 (the heat-map skyline); every atom elsewhere is a turning,
seeded 3D point cloud.

## Setup

From this folder:

```bash
pip install -r requirements.txt
```

The full review used Manim CE 0.19.2; changing-label and 3D checks also pass
with the repository's CE 0.22.0 interpreter. The dependency range includes both.

You also need FFmpeg/ffprobe, LaTeX with dvisvgm, Cairo/Pango and the Lato font
(see `requirements.txt`), plus the repository's shared `themes/` folder one
level up. `config.py` adds the repository root to `sys.path`, so the theme
imports from inside this sub-folder.

## Preview and render

```bash
python main.py list                # chapter names, start times and durations
python main.py preview 05          # one chapter at 854×480, 15 fps
python main.py preview all         # separate previews of all 20 chapters
python main.py preview full        # the full film at preview quality
python main.py scene 05            # one chapter at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
```

### Render each chapter at 480p previews (854×480, 15 fps)

Paste this block to render all 20 chapters as separate videos. Each line also
works on its own. Remove `-p` to skip opening previews.

```bash
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_02_from_shape.py Scene02FromShape
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_03_nuclear_pull.py Scene03NuclearPull
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_04_shielding.py Scene04Shielding
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_05_radius_across.py Scene05RadiusAcross
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_06_radius_down.py Scene06RadiusDown
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_07_ions.py Scene07Ions
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_08_isoelectronic.py Scene08Isoelectronic
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_09_ionization.py Scene09Ionization
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_10_ionization_landscape.py Scene10IonizationLandscape
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_11_exceptions.py Scene11Exceptions
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_12_electron_gain.py Scene12ElectronGain
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_13_fluorine_chlorine.py Scene13FluorineChlorine
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_14_electronegativity.py Scene14Electronegativity
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_15_bond_landscape.py Scene15BondLandscape
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_16_sodium_chloride.py Scene16SodiumChloride
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_17_behaviour_map.py Scene17BehaviourMap
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_18_heat_maps.py Scene18HeatMaps
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_19_ending.py Scene19Ending
python -m manim -pql -r 854,480 --fps 15 manim_scenes/scene_20_subscribe.py Scene20Subscribe
```

### Render each chapter at 2K / QHD renders (2560×1440, 30 fps)

Paste this block to render all 20 chapters as separate videos. Each line also
works on its own. Remove `-p` to skip opening previews.

```bash
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_02_from_shape.py Scene02FromShape
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_03_nuclear_pull.py Scene03NuclearPull
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_04_shielding.py Scene04Shielding
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_05_radius_across.py Scene05RadiusAcross
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_06_radius_down.py Scene06RadiusDown
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_07_ions.py Scene07Ions
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_08_isoelectronic.py Scene08Isoelectronic
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_09_ionization.py Scene09Ionization
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_10_ionization_landscape.py Scene10IonizationLandscape
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_11_exceptions.py Scene11Exceptions
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_12_electron_gain.py Scene12ElectronGain
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_13_fluorine_chlorine.py Scene13FluorineChlorine
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_14_electronegativity.py Scene14Electronegativity
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_15_bond_landscape.py Scene15BondLandscape
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_16_sodium_chloride.py Scene16SodiumChloride
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_17_behaviour_map.py Scene17BehaviourMap
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_18_heat_maps.py Scene18HeatMaps
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_19_ending.py Scene19Ending
python -m manim -pqh -r 2560,1440 --fps 30 manim_scenes/scene_20_subscribe.py Scene20Subscribe
```

### Render each chapter at 1080p (1920×1080, 30 fps)

Run from `periodic-trend/`; one line per chapter, or paste the block to render
all 20 as separate videos (add `-p` to open each result).

```bash
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_02_from_shape.py Scene02FromShape
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_03_nuclear_pull.py Scene03NuclearPull
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_04_shielding.py Scene04Shielding
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_05_radius_across.py Scene05RadiusAcross
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_06_radius_down.py Scene06RadiusDown
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_07_ions.py Scene07Ions
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_08_isoelectronic.py Scene08Isoelectronic
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_09_ionization.py Scene09Ionization
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_10_ionization_landscape.py Scene10IonizationLandscape
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_11_exceptions.py Scene11Exceptions
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_12_electron_gain.py Scene12ElectronGain
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_13_fluorine_chlorine.py Scene13FluorineChlorine
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_14_electronegativity.py Scene14Electronegativity
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_15_bond_landscape.py Scene15BondLandscape
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_16_sodium_chloride.py Scene16SodiumChloride
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_17_behaviour_map.py Scene17BehaviourMap
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_18_heat_maps.py Scene18HeatMaps
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_19_ending.py Scene19Ending
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/scene_20_subscribe.py Scene20Subscribe
```

### The whole film as one video

```bash
# Final: complete film at 1920×1080, 30 fps (same as python main.py render)
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/full_video.py FullVideo

# 2K / QHD variant
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/full_video.py FullVideo

# Quick full-length preview
python -m manim -ql -r 854,480 --fps 15 manim_scenes/full_video.py FullVideo
```

Video goes to `media/`. Expect the final render to take hours, not minutes:
every frame redraws the turning electron clouds, and Cairo shades 3D faces in
Python. At 480p15, chapter 01 (62 s) renders in under 3 minutes on the
development machine.

## Narration and your voice

`narration.py` is the single source of the spoken script and its beat times;
scenes hold on each beat with `beat(scene, t, i)`.

- `narration_script.md` — the readable master script, chapter by chapter, with timestamps.
- `assets/narration/scene_01.txt` … `scene_20.txt` — continuous prose to paste into a TTS tool or read aloud.
- `narration_cues.md`, `assets/narration/cue_sheet.json` — beat-by-beat timing targets.

Save recordings as `assets/audio/scene_01.wav` (or `.mp3`/`.m4a`), one per
chapter. Renders attach them automatically; a clip longer than its chapter
stops the render rather than spilling into the next chapter.

```bash
python main.py audio-check            # missing / too-long clips
python -m utils.narration_export      # regenerate the script files after editing narration.py
```

## Checks (no video rendering needed)

```bash
python main.py check                  # everything below, in order (~10 minutes)
python -m utils.math_utils            # colour scale, rotations, density illustration
python -m utils.element_data          # every trend, ratio and exception the narration states; all 27 spoken numbers
python -m utils.physics_models        # the computed table (as in Part 3), Slater Z_eff, radial probability samples, Coulomb ratios
python -m utils.narration_audit       # no beat faster than 2.75 words/s
python -m utils.timing_audit          # every chapter lands on its planned second (15 fps)
python -m utils.timing_audit --fps 30 # the same at production frame rate
python -m utils.timing_audit --full   # FullVideo end to end: chapters chain, nothing left behind
python -m utils.layout_audit          # no text off-frame, overlapping or crowding (--motion: mid-animation too)
python -m utils.storyboard 05 --every 4   # PNG stills of key layouts to output/storyboard/
python -m utils.contact_sheet scene_05    # tile those stills into one review sheet
```

## Design rules

- **Scientific values have one source.** Radii, ionization and electron-gain values,
  electronegativities and ionic radii live in `utils/element_data.py`, with
  sources; tile positions come from Part 3's filling model in
  `utils/physics_models.py`. `python -m utils.element_data` fails if a spoken
  number or a stated trend disagrees with the data.
- **Colour is meaning.** Cyan outer electrons, gray-blue inner electrons, red
  nucleus, gold pull, purple Z_eff, green released / orange required energy,
  magenta direction arrows, one cool→warm heat scale, Part 3's block colours.
  See `config.py`.
- **Clouds, not orbits.** Every electron cloud is a seeded sample of a
  hydrogen-like radial density, projected and scaled to illustrate size. Dots
  are probability samples, not individual electrons; the contour is a display
  guide, not a measured atomic boundary. The planetary orbit appears once,
  to be crossed out.
- **Honest pictures.** Schematic sizes, energy spacings and balance bars are
  labelled as schematic on screen; the NaCl transfer is called a simplified
  model and its uphill energy (+147 kJ/mol) is shown; noble-gas radii are never
  mixed into covalent data.
- **Mobile-first type.** A true 16×9 logical frame; captions, labels and
  equations are 30 pt Lato or larger (TeX is scaled 1.35× to match), short, and
  clear of the action. In 3D chapters, captions are pinned to the screen and
  only fade in or out; the camera tilts and orbits but never moves its
  `frame_center` (content is moved instead).

## Notes for maintainers

Manim CE behaviours this film works around (all in `manim_scenes/common.py`):

- `AnimationGroup` adds a second copy of its members to the scene, drawn on top
  — it would hide a nucleus under its own cloud. `start()` teaches each scene to
  look through animation groups (`flatten_animation_groups`).
- Transform-type animations keep running the updaters of their hidden start
  and target copies. Clouds and crystals change their point layout every frame,
  so copies are born frozen (`_LiveMixin`), and atoms move with `Glide`, never
  `.animate`.
- `FadeOut` restores a mobject after removing it, so a part of a group that
  stays on screen (a nucleus label) is hidden with `.animate.set_opacity(0)`.

## Files

```
periodic-trend/
├── main.py                  CLI: list / preview / scene / render / check / audio-check
├── config.py                palette, fonts, frame, durations, theme setup, seed
├── narration.py             spoken script + beat times (timing source)
├── manim_scenes/
│   ├── common.py            visual grammar: clouds, atoms, bonds, meters, tiles, heat maps, crystal
│   ├── full_video.py        FullVideo: all 20 chapters in order
│   └── scene_01_… scene_20_ one chapter per file, each with play_scene(scene)
├── utils/
│   ├── element_data.py      measured values + sources + narration cross-check
│   ├── physics_models.py    the computed table, Slater Z_eff, cloud sampling, Coulomb
│   ├── math_utils.py        colour scales, 3D rotation/projection, bond density
│   ├── render_helpers.py    safe-frame fitting and layout grids
│   ├── timing_audit.py      layout_audit.py  storyboard.py  contact_sheet.py
│   └── narration_audit.py   narration_export.py  voiceover.py
├── concept_summary.md       the science, accuracy notes, references
├── animation_plan.md        chapter-by-chapter visual plan
├── narration_script.md      generated master script (+ narration_cues.md)
├── youtube_package.md       titles, description, chapters, tags
└── assets/ media/ output/   inputs and (git-ignored) render output
```

No Manim plugin is used. `manim-chemistry` offers periodic tables and Bohr
diagrams, but this film needs Part 3's computed layout and probability clouds
rather than planetary Bohr shells, so core Manim is both more accurate and more
consistent with the series.
