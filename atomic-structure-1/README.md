# How We Discovered What an Atom Looks Like — Part 1

A fifteen-scene Manim Community Edition film for students, teachers and curious
viewers. Planned runtime: **22:05**, with **2,772 spoken words**. The opening follows
**Mystery → Promise → Bigger mystery → Story begins**.

“We're not going to memorize the models of the atom. We're going to discover why
each one had to exist.”

The scenes follow experimental evidence from electrons to the nucleus and
hydrogen's allowed energies, then set up the quantum description in the next video.

## Start here

- [Narration script](narration_script.md): spoken paragraphs with planning windows.
- [ElevenLabs full text](assets/narration/full_narration.txt): paste-ready speech only.
- [Individual voice files](assets/narration/): `scene_01.txt` through `scene_15.txt`.
- [Animation plan](animation_plan.md): merge map, visual beats and transitions.
- [Recording guide](voiceover_guide.md): pronunciation, pacing and final audio sync.
- [Science notes](concept_summary.md): analogy limits and source links.

## Environment and rendering

The active pyenv is `youtube` (Python 3.12.9), inherited from the parent directory's
`.python-version`. This film uses **Manim CE 0.21.0** (`import manim`). ManimGL
1.7.2 (`import manimlib`) is installed separately in that environment.

```bash
pyenv version
python -m pip install -r requirements.txt
python main.py list
python main.py preview 01
python main.py preview 07
python main.py preview 09
python main.py scene 07
python main.py render
```

`preview` writes a low-resolution video; `scene` and `render` use high quality.
Output appears under `media/videos/`. Rendering requires FFmpeg, LaTeX and
dvisvgm. The parent repository's `themes/oceanic_next.py` supplies the theme, so
keep this project inside its current repository layout.

Six scenes use 3D camera moves: 01, 03, 04, 05, 06 and 14. The camera returns to its
flat orientation before explanatory diagrams. Reading holds keep labels still;
3D camera sweeps use eased motion. The default final frame rate is 30 FPS in
`config.py`.

## Fast preview rendering — `-pql`, 15 FPS

Run these commands from this project directory. Each command renders one scene
at **854 × 480 (480p), 15 FPS**, then opens the finished video. Pass the specific
Python file and scene class, as shown below.

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_impossible_atom.py Scene01ImpossibleAtom
python -m manim -pql --fps 15 manim_scenes/scene_02_seeing_the_invisible.py Scene02SeeingTheInvisible
python -m manim -pql --fps 15 manim_scenes/scene_03_dalton_sphere.py Scene03DaltonSphere
python -m manim -pql --fps 15 manim_scenes/scene_04_cathode_rays.py Scene04CathodeRays
python -m manim -pql --fps 15 manim_scenes/scene_05_thomson_prediction.py Scene05ThomsonPrediction
python -m manim -pql --fps 15 manim_scenes/scene_06_gold_foil.py Scene06GoldFoil
python -m manim -pql --fps 15 manim_scenes/scene_07_empty_space.py Scene07EmptySpace
python -m manim -pql --fps 15 manim_scenes/scene_08_unstable_atom.py Scene08UnstableAtom
python -m manim -pql --fps 15 manim_scenes/scene_09_light_barcode.py Scene09LightBarcode
python -m manim -pql --fps 15 manim_scenes/scene_10_energy_floors.py Scene10EnergyFloors
python -m manim -pql --fps 15 manim_scenes/scene_11_photon_ladder.py Scene11PhotonLadder
python -m manim -pql --fps 15 manim_scenes/scene_12_what_bohr_got_right.py Scene12WhatBohrGotRight
python -m manim -pql --fps 15 manim_scenes/scene_13_not_an_orbit.py Scene13NotAnOrbit
python -m manim -pql --fps 15 manim_scenes/scene_14_part_two.py Scene14PartTwo
python -m manim -pql --fps 15 manim_scenes/scene_15_subscribe.py Scene_15_Subscribe
```

Preview the complete film, including the separate subscribe card:

```bash
python -m manim -pql --fps 15 manim_scenes/full_video.py FullVideo
```

## 2K / QHD rendering — 2560 × 1440, 30 FPS

Here, “2K” means **2560 × 1440 (1440p/QHD)**. The explicit `-r 2560,1440`
sets this resolution; `-qh` alone selects 1080p. These commands also open the
finished video with `-p`.

```bash
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_01_impossible_atom.py Scene01ImpossibleAtom
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_02_seeing_the_invisible.py Scene02SeeingTheInvisible
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_03_dalton_sphere.py Scene03DaltonSphere
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_04_cathode_rays.py Scene04CathodeRays
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_05_thomson_prediction.py Scene05ThomsonPrediction
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_06_gold_foil.py Scene06GoldFoil
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_07_empty_space.py Scene07EmptySpace
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_08_unstable_atom.py Scene08UnstableAtom
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_09_light_barcode.py Scene09LightBarcode
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_10_energy_floors.py Scene10EnergyFloors
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_11_photon_ladder.py Scene11PhotonLadder
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_12_what_bohr_got_right.py Scene12WhatBohrGotRight
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_13_not_an_orbit.py Scene13NotAnOrbit
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_14_part_two.py Scene14PartTwo
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/scene_15_subscribe.py Scene_15_Subscribe
```

Render the complete film at the same resolution:

```bash
python -m manim -pqh --fps 30 -r 2560,1440 manim_scenes/full_video.py FullVideo
```

For smoother 60 FPS output, change `--fps 30` to `--fps 60` in any 2K command.
For example:

```bash
python -m manim -pqh --fps 60 -r 2560,1440 manim_scenes/full_video.py FullVideo
```

Remove `p` from `-pql` or `-pqh` to render without opening a video player.
Files are written under `media/videos/`, with separate resolution/FPS folders.
These commands set quality explicitly; the `main.py` shortcuts retain their
settings from `config.py`.

## ManimGL environment check

Manim CE and ManimGL are separate engines. The film source imports CE. To check
the installed GL renderer independently:

```bash
python utils/manimgl_smoke.py --headless
```

This writes `media/manimgl/ManimGLSmoke.mp4`, a four-second rotating atom. The
`--headless` flag uses EGL and project-local caches; omit it for an X display.
ManimGL's older dependency on `pkg_resources` requires the existing
`setuptools<81` pin. `requirements-manimgl.txt` records that optional installation.

## Checks

```bash
python utils/narration_export.py
python utils/narration_export.py --check
python utils/narration_audit.py
python utils/timing_audit.py --fps 30
python utils/layout_audit.py --fps 5
python utils/storyboard.py
python -m compileall -q main.py config.py manim_scenes utils
```

The narration audit checks every scene's order, contiguous time window and word
rate. The timing audit executes animations without drawing frames. The layout
audit checks authored text positions at animation endpoints; rendered previews
are still needed to assess intermediate motion and 3D depth.

The current render contains visuals only. Cloned narration has not been supplied
or generated. Measure the exported audio and align its paragraph beats in your
editor before producing the final voiced film. The planned time windows do not
guarantee word-level synchronization.

## Revision

The original project contained 17 teaching scenes plus a closing card. Three
merges now produce fifteen scene modules, fifteen CLI entries and fifteen
narration exports. Scene 14 retains the next video explanation; scene 15 is the
separate subscribe card. Scene numbers have changed; use `python main.py list` for the
current names. Existing videos under `media/` may use the earlier numbering.

The scientific changes include qualifying hydrogen's four displayed lines,
separating charge-to-mass evidence from the modern electron mass, explaining that
scattering is electric repulsion, and treating “empty space” as a useful size
comparison. The cricket-ball example is approximately five kilometres in radius;
it is not a universal size or a sharp physical edge.
