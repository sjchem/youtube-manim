# The Molecular Dance — From Invisible Forces to the Gas Laws

*States of Matter, Part 1* · an approximately 40-minute visual lesson for Class 11 Chemistry
(NCERT Unit 5, §5.1–5.6), in the channel's Oceanic Next style.

How can billions of invisible molecules, moving randomly and colliding
continuously, produce the predictable gas laws? The film follows one chain of
reasoning, in 31 scenes grouped into the brief's 11 YouTube chapters:
intermolecular forces → thermal energy vs attraction → pressure as momentum
delivered to walls → Boyle, Charles, Gay-Lussac and Avogadro as slices of one
equation, PV = nRT → Dalton's law → where the ideal gas model ends.

| File | What it is |
|---|---|
| [concept_summary.md](concept_summary.md) | The science in one page, with the metaphors and simplifications named |
| [animation_plan.md](animation_plan.md) | Scene-by-scene visual plan with film timestamps (generated) |
| [narration_script.md](narration_script.md) | Full timestamped narration, clean prose (generated) |
| [narration_script_tagged.md](narration_script_tagged.md) | The same with sparse ElevenLabs v3/v4 delivery tags (generated) |
| [narration_cues.md](narration_cues.md) | Per-scene timing plan: words, estimated speech, visual pauses per beat (generated) |
| [youtube_package.md](youtube_package.md) | Titles, description with chapters, tags, thumbnail, pinned comment |

## Why Manim Community Edition, not ManimGL

The brief prefers ManimGL for 3D. ManimGL is installed (in the `youtube` pyenv
env), but the shared `../themes/oceanic_next.py` that gives every video on the
channel its look is written against Manim CE (`manim_themes`), and a single
`FullVideo` render cannot mix engines. So the film is built on **Manim CE
0.22**, and its 3D comes from a projected 3D engine
(`manim_scenes/stage3d.py`): real rotating geometry with depth sorting,
perspective and lit spheres, drawn as smooth 2D shapes inside an ordinary
`Scene`. This avoids CE's `ThreeDScene` pitfalls (faceted spheres,
fixed-in-frame text glitches) and keeps every caption crisp.

## Setup

```bash
# from the repository root (one level up)
pyenv activate youtube            # or any Python 3.10+ env
pip install -r state-matter-1/requirements.txt
cd state-matter-1
```

System requirements (ffmpeg, LaTeX + dvisvgm, cairo/pango, the Lato font) are
listed at the top of [requirements.txt](requirements.txt). The project adds the
repository root to `sys.path` in `config.py`, so `themes/` imports work from
this sub-folder.

## Commands

```bash
python main.py list                 # all 31 scenes with film timestamps and lengths
python main.py chapters             # the 11 YouTube chapter markers
python main.py preview 13           # fast 480p15 preview of one scene
python main.py scene 13             # one scene at 1080p30
python main.py preview all          # every scene as separate previews
python main.py preview full         # the whole film at preview quality
python main.py render               # the whole film at 1080p30 (FullVideo)
python main.py check                # every audit (see Validation)
python main.py export               # regenerate scripts, ElevenLabs text, cue sheets, animation plan
python main.py audio-check          # recorded narration vs scene lengths
```

Direct Manim commands work too, from this folder:

```bash
manim -ql --fps 15 -r 854,480 manim_scenes/scene_25_ideal_surface.py Scene25IdealSurface
manim -qh manim_scenes/full_video.py FullVideo        # final 1080p30 render
```

Render output goes to `media/` (ignored by git; `output/` holds storyboards).
A full 1080p render takes hours on a laptop; preview single scenes first.

## How the project is organised

```
state-matter-1/
├── main.py                # CLI: list, preview, render, check, export
├── config.py              # palette (colour = meaning), fonts, render settings; durations come from narration.py
├── narration.py           # the script: (spoken text, visual hold) beats → beat times and scene lengths
├── narration_delivery.py  # sparse ElevenLabs delivery tags (anchors must match the script)
├── manim_scenes/
│   ├── common.py          # the visual grammar: GasBox, Gauge, Thermo, plots, atoms, molecules, MD view, cards
│   ├── stage3d.py         # projected 3D engine: Stage, Ball, Rod, Face, Curve, Chamber, GasCloud, Flashes, Dots
│   ├── scene_01_hook.py … scene_31_subscribe.py
│   └── full_video.py      # FullVideo: all 31 scenes in order, one deterministic render
├── utils/
│   ├── physics_models.py  # constants, worked examples, the ideal gas, dipoles, 2D Lennard-Jones MD
│   ├── gas_data.py        # every spoken number recomputed, turned into words, found in the script
│   ├── math_utils.py      # vectors, rotations, projection, colour
│   ├── render_helpers.py  # safe-frame fitting
│   ├── timing_audit.py    # every scene lands on its exact length (no frames rendered)
│   ├── layout_audit.py    # text collisions, frame edges, title expiry, sampled mid-animation
│   ├── narration_audit.py # every beat is speakable in its window
│   ├── narration_export.py, voiceover.py, storyboard.py, contact_sheet.py
└── assets/ (audio, images, narration, references, sounds, textures), media/, output/
```

### Rules that keep picture, voice and model in agreement

1. **No number is typed in a scene.** `utils/physics_models.py` holds every
   constant and worked example; scenes format them with `fx()`/`sci()`, and
   `python -m utils.gas_data` checks 64 spoken numbers and 19 claims in the
   narration against the same model.
2. **Every gas is one model.** A `GasBox` runs a seeded `IdealGas`:
   Maxwell–Boltzmann velocities and exact elastic wall reflections (positions
   fold analytically, so every wall hit is detected and sparks where it
   happens). Gauges read the model's pressure; hit counters measure actual hits
   (the piston's hits per second really double when the volume halves).
3. **Narration drives timing.** Each beat's window is its words at 2.6 words/s
   plus a stated visual hold; scenes wait on `beat(scene, t, i)` and end with
   `finish()`, which keeps something moving to the last frame.
4. **Live objects are never `.animate`d.** Stages, gas clouds, atoms and MD
   views change through `Param` tweens (`stage.fade`, `box.heat_to`,
   `box.volume_to`, `atom.glide`), never Transform copies.

## Recording the narration (ElevenLabs v4, cloned voice)

1. `python main.py export` writes `assets/narration/elevenlabs/scene_XX.txt`
   (tagged) and `assets/narration/scene_XX.txt` (clean), plus
   `narration_cues.md` and `assets/narration/cue_sheet.json`.
2. Generate one clip per scene and save it as `assets/audio/scene_XX.wav`
   (or `.mp3`), or record beats separately (`python -m utils.narration_export
   --beats`, then `assets/audio/scene_XX/beat_001.wav`, …) for cue-exact placement.
3. `python main.py audio-check` compares each clip with its scene; a clip
   longer than its window is refused rather than stretched. To retime, edit the
   holds in `narration.py`; scene lengths and cue sheets follow automatically.

Pacing: 4,808 words over 39:52 (≈ 121 words per finished minute). The brief
asks for 140–150 but fewer on 3D and calculation scenes, and nearly every scene
here is one; the cue sheets show each beat's estimated speech and visual pause.

## Validation

```bash
python -m compileall .              # syntax
python main.py check                # model, spoken numbers, narration pace, timing (15 and 30 fps),
                                    # FullVideo end to end, layout with mid-animation sampling
python -m utils.storyboard 25 --every 3 && python -m utils.contact_sheet scene_25
```

## Scientific notes

Sources are listed in `utils/physics_models.py`; corrections and choices made
against the brief are in [assets/references/brief_review.md](assets/references/brief_review.md).
Metaphors (the commuter crowd, the mountain air column) are labelled as such on
screen and in [concept_summary.md](concept_summary.md).

## Scene review and render commands

The detailed scientific and visual review is in
[assets/references/scene_review.md](assets/references/scene_review.md).
All 31 scenes have opening titles that fade after a few seconds; the diagrams
use short labels, with explanations in the narration. The current estimated
runtime is 39:52. Narration timing is an estimate until voice clips are recorded.

Run these from `state-matter-1` with the project's Python environment active.
Each block renders all scenes separately, in order. Output is written to `media/`.

### 480p previews — 854 × 480, 15 fps

```bash
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_puzzle.py Scene02Puzzle
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_inside_between.py Scene03InsideBetween
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_dispersion.py Scene04Dispersion
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_dipoles.py Scene05Dipoles
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_hydrogen_bonds.py Scene06HydrogenBonds
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_repulsion.py Scene07Repulsion
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_thermal_motion.py Scene08ThermalMotion
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_tug_of_war.py Scene09TugOfWar
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_one_wall.py Scene10OneWall
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_hits_to_force.py Scene11HitsToForce
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_crowd.py Scene12Crowd
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_one_third.py Scene13OneThird
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_temperature.py Scene14Temperature
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_boyle.py Scene15Boyle
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_boyle_numbers.py Scene16BoyleNumbers
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_thinner_air.py Scene17ThinnerAir
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_charles.py Scene18Charles
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_absolute_zero.py Scene19AbsoluteZero
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_kelvin.py Scene20Kelvin
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_gay_lussac.py Scene21GayLussac
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_22_side_by_side.py Scene22SideBySide
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_23_avogadro.py Scene23Avogadro
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_24_equal_volumes.py Scene24EqualVolumes
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_25_ideal_surface.py Scene25IdealSurface
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_26_using_ideal.py Scene26UsingIdeal
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_27_density.py Scene27Density
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_28_dalton.py Scene28Dalton
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_29_over_water.py Scene29OverWater
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_30_limits.py Scene30Limits
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_31_subscribe.py Scene31Subscribe
```

### 2K / 1440p — 2560 × 1440, 30 fps

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_puzzle.py Scene02Puzzle
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_inside_between.py Scene03InsideBetween
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_dispersion.py Scene04Dispersion
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_dipoles.py Scene05Dipoles
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_hydrogen_bonds.py Scene06HydrogenBonds
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_repulsion.py Scene07Repulsion
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_thermal_motion.py Scene08ThermalMotion
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_tug_of_war.py Scene09TugOfWar
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_one_wall.py Scene10OneWall
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_hits_to_force.py Scene11HitsToForce
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_crowd.py Scene12Crowd
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_one_third.py Scene13OneThird
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_temperature.py Scene14Temperature
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_boyle.py Scene15Boyle
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_boyle_numbers.py Scene16BoyleNumbers
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_thinner_air.py Scene17ThinnerAir
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_charles.py Scene18Charles
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_absolute_zero.py Scene19AbsoluteZero
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_kelvin.py Scene20Kelvin
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_gay_lussac.py Scene21GayLussac
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_22_side_by_side.py Scene22SideBySide
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_23_avogadro.py Scene23Avogadro
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_24_equal_volumes.py Scene24EqualVolumes
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_25_ideal_surface.py Scene25IdealSurface
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_26_using_ideal.py Scene26UsingIdeal
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_27_density.py Scene27Density
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_28_dalton.py Scene28Dalton
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_29_over_water.py Scene29OverWater
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_30_limits.py Scene30Limits
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_31_subscribe.py Scene31Subscribe
```
