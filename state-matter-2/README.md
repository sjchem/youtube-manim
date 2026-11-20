# Beyond Ideal Gases — How Molecules Become Liquids

*States of Matter, Part 2* · an approximately 40-minute visual lesson for Class 11 Chemistry
(NCERT Unit 5, §5.7–5.11), in the channel's Oceanic Next style.

If the ideal gas equation explains gases so elegantly, why do real gases
violate it — and how can the same molecules turn from a freely moving gas into
a liquid? The film connects to Part 1 and follows one chain of
reasoning in 30 scenes grouped into the brief's 11 YouTube chapters: a spread
of molecular speeds (Maxwell–Boltzmann) → the assumptions of kinetic theory →
attraction and size as the two causes of deviation → the van der Waals
equation → the compressibility factor → Andrews' isotherms, the critical point
and gas–liquid continuity → vapour pressure and boiling → surface tension →
viscosity → one synthesis: the same molecules, under different conditions.

| File | What it is |
|---|---|
| [concept_summary.md](concept_summary.md) | The science in one page, with the models and simplifications named |
| [animation_plan.md](animation_plan.md) | Scene-by-scene visual plan with film timestamps (generated) |
| [narration_script.md](narration_script.md) | Full timestamped narration, clean prose (generated) |
| [narration_script_tagged.md](narration_script_tagged.md) | The same with sparse ElevenLabs v3/v4 delivery tags (generated) |
| [narration_cues.md](narration_cues.md) | Per-scene timing plan: words, estimated speech, visual pauses per beat (generated) |
| [youtube_package.md](youtube_package.md) | Titles, description with chapters, tags, thumbnail, pinned comment |
| [assets/references/brief_review.md](assets/references/brief_review.md) | Corrections and choices made against the brief, with sources |

## Why Manim Community Edition, not ManimGL

The brief prefers ManimGL for 3D. ManimGL is installed (in the `youtube` pyenv
env), but the shared `../themes/oceanic_next.py` that gives every video on the
channel its look is written against Manim CE (`manim_themes`), the brief's code
blocks use CE imports, and a single `FullVideo` render cannot mix engines. So
the film is built on **Manim CE 0.22**, and its 3D comes from the projected 3D
engine in `manim_scenes/stage3d.py` (shared with Part 1): real rotating
geometry with perspective, depth sorting and lit spheres, drawn as smooth 2D
shapes inside an ordinary `Scene`, so captions stay crisp and spheres stay
smooth. Part 2 adds translucent spheres split into back and front halves
(forbidden zones, velocity-space shells), a liquid pool with its vapour
(`TwoPhaseBox`) and live hard-sphere gases.

No Manim plugin is used: `manim-physics` and `manim-chemistry` would not
improve the gases, pools, surfaces or plots, and the models in
`utils/physics_models.py` are small, seeded and self-checking.

## Setup

```bash
# from the repository root (one level up)
pyenv activate youtube            # or any Python 3.10+ env with Manim CE 0.19–0.22
pip install -r state-matter-2/requirements.txt
cd state-matter-2
```

System requirements (ffmpeg, LaTeX + dvisvgm, cairo/pango, the Lato font) are
listed at the top of [requirements.txt](requirements.txt). `config.py` adds the
repository root to `sys.path`, so `themes/` imports work from this sub-folder.
Run every command from this folder (the repo's `.python-version` selects the
`youtube` environment).

## Commands

```bash
python main.py list                 # all 30 scenes with film timestamps and lengths
python main.py chapters             # the 11 YouTube chapter markers
python main.py preview 18           # fast 480p15 preview of one scene
python main.py scene 18             # one scene at 1080p30
python main.py preview all          # every scene as separate previews
python main.py preview full         # the whole film at preview quality
python main.py render               # the whole film at 1080p30 (FullVideo)
python main.py check                # every audit (see Validation)
python main.py export               # regenerate scripts, ElevenLabs text, cue sheets, animation plan
python main.py audio-check          # recorded narration vs scene lengths
```

Direct Manim commands work too, from this folder:

```bash
manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_andrews.py Scene18Andrews
manim -qh manim_scenes/full_video.py FullVideo        # final 1080p30 render
```

Render output goes to `media/` (ignored by git; `output/` holds storyboards and
the simulation cache). A full final-quality render of the whole film is long (hours on a laptop CPU, not minutes); preview scenes at 480p first.

## How the project is organised

```
state-matter-2/
├── main.py                # CLI: list, chapters, preview, scene, render, check, export, audio-check
├── config.py              # palette (colour = meaning), fonts, render settings; durations come from narration.py
├── narration.py           # the script: (spoken text, visual hold) beats → beat times and scene lengths
├── narration_delivery.py  # sparse ElevenLabs delivery tags (anchors must match the script)
├── manim_scenes/
│   ├── common.py          # the visual grammar: GasBox, TwoPhaseBox + VapourExchange, gauges, plots,
│   │                      #   Maxwell–Boltzmann curves, DiskView, glass spheres, surfaces, cards
│   ├── stage3d.py         # projected 3D engine: Stage, Ball, Rod, Face, Curve, Dots, SphereHalf, GasCloud, Flashes
│   ├── kit_*.py           # helpers shared by a few neighbouring scenes
│   ├── scene_01_hook.py … scene_30_subscribe.py
│   └── full_video.py      # FullVideo: all 30 scenes in order, one deterministic render
├── utils/
│   ├── physics_models.py  # constants, data, worked examples, MB speeds, 2D disks, hard spheres,
│   │                      #   van der Waals + Maxwell construction, Antoine, IAPWS, viscosity; verify()
│   ├── spoken_numbers.py  # every spoken number recomputed, turned into words, found in the script
│   ├── visual_contract_audit.py  # what the picture implies is true of the model
│   ├── math_utils.py      # vectors, rotations, projection, colour
│   ├── render_helpers.py  # safe-frame fitting
│   ├── timing_audit.py    # every scene lands on its exact length (no frames rendered)
│   ├── layout_audit.py    # text collisions, frame edges, title expiry, sampled mid-animation
│   ├── narration_audit.py # every beat is speakable in its window
│   └── narration_export.py, voiceover.py, storyboard.py, contact_sheet.py
└── assets/ (audio, images, narration, references, sounds, textures), media/, output/
```

### Rules that keep picture, voice and model in agreement

1. **No number is typed in a scene.** `utils/physics_models.py` holds every
   constant, data table and worked example; scenes format them with `fx()`,
   and `python -m utils.spoken_numbers` checks every spoken number and claim in
   the narration against the same model.
2. **Every gas is a model.** A `GasBox` runs a seeded `IdealGas` (exact
   wall reflections) or a live `HardSphereGas` (real sphere collisions); a
   `TwoPhaseBox` adds a liquid pool whose vapour condenses and evaporates
   molecule by molecule. Isotherms, the coexistence dome and the P–V–T surface
   come from the van der Waals model with Maxwell's construction.
3. **Narration drives timing.** Each beat's window is its words at 2.6 words/s
   plus a stated visual hold; scenes wait on `beat(scene, t, i)` and end with
   `finish()`, which keeps something moving to the last frame.
4. **Live objects are never `.animate`d.** Stages, gas clouds, pools and disk
   playbacks change through `Param` tweens, never Transform copies.

## Recording the narration (ElevenLabs v4, cloned voice)

1. `python main.py export` writes `assets/narration/elevenlabs/scene_XX.txt`
   (tagged) and `assets/narration/scene_XX.txt` (clean), plus
   `narration_cues.md` and `assets/narration/cue_sheet.json`.
2. Generate one clip per scene and save it as `assets/audio/scene_XX.wav`
   (or `.mp3`), or record beats separately (`python main.py export --beats`,
   then `assets/audio/scene_XX/beat_001.wav`, …) for cue-exact placement.
3. `python main.py audio-check` compares each clip with its scene; a clip
   longer than its window is refused rather than stretched. To retime, edit the
   holds in `narration.py`; scene lengths and cue sheets follow automatically.

### Pacing

The reviewed script has **4,876 words over 40:12** of film: about
**121 words per minute** overall. That is below the
140–150 words-per-minute target on purpose. The brief asks for about 40 minutes,
and the scenes are dense with 3D motion, derivations and live simulations, so the
extra time is held as visual pauses. Each beat's window is its words at 2.6 words/s
plus a stated hold, listed per beat in [narration_cues.md](narration_cues.md).
The speech estimate is separate from the animation cues. Measure the generated or recorded audio with `python main.py audio-check` before the final render. To move closer to ~145 words per minute, add narration, or
shorten holds in `narration.py`, then re-run `python main.py check`: a beat whose
animation no longer fits its shorter window is reported by name.

## Validation

```bash
python -m compileall .              # syntax
python main.py check                # model, spoken numbers, visual contracts, narration pace,
                                    # timing (15 and 30 fps), FullVideo end to end, layout with mid-animation sampling
python -m utils.storyboard 18 --every 3 && python -m utils.contact_sheet scene_18
```

## Scientific notes

Sources are listed in `utils/physics_models.py`; corrections and choices made
against the brief are in [assets/references/brief_review.md](assets/references/brief_review.md).
Models and schematics (the 2D disk simulation, the velocity-space shell, the
mean-field tug at the wall, the van der Waals isotherms and surface, the liquid
snapshot, the falling balls) are identified as models on screen where the distinction matters, and documented in
[concept_summary.md](concept_summary.md).

## Review and render commands

The scene-by-scene findings and scientific corrections are in
[assets/references/scene_review.md](assets/references/scene_review.md).
Scene titles hold for three seconds and fade over 0.7 seconds. Captions are
introduced with the relevant action; long final camera drifts are capped.

Run the following blocks from `state-matter-2`. Each block renders every scene
separately, in story order. 2K here means the YouTube 1440p format, 2560 × 1440.
The videos do not include a generated voice track unless you supply the audio.

### 480p previews · 854 × 480 · 15 fps

```bash
manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_hook.py Scene01Hook
manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_roadmap.py Scene02Roadmap
manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_collisions.py Scene03Collisions
manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_one_speed.py Scene04OneSpeed
manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_velocity_space.py Scene05VelocitySpace
manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_three_speeds.py Scene06ThreeSpeeds
manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_hotter_lighter.py Scene07HotterLighter
manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_kmt_rules.py Scene08KmtRules
manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_two_cracks.py Scene09TwoCracks
manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_attraction.py Scene10Attraction
manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_size.py Scene11Size
manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_tug_of_war.py Scene12TugOfWar
manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_pressure_correction.py Scene13PressureCorrection
manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_excluded_volume.py Scene14ExcludedVolume
manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_vdw_equation.py Scene15VdwEquation
manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_compressibility.py Scene16Compressibility
manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_boyle_temperature.py Scene17BoyleTemperature
manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_andrews.py Scene18Andrews
manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_critical_point.py Scene19CriticalPoint
manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_vdw_loops.py Scene20VdwLoops
manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_continuity.py Scene21Continuity
manim -ql --fps 15 -r 854,480 manim_scenes/scene_22_cooling.py Scene22Cooling
manim -ql --fps 15 -r 854,480 manim_scenes/scene_23_vapour_pressure.py Scene23VapourPressure
manim -ql --fps 15 -r 854,480 manim_scenes/scene_24_boiling.py Scene24Boiling
manim -ql --fps 15 -r 854,480 manim_scenes/scene_25_surface_energy.py Scene25SurfaceEnergy
manim -ql --fps 15 -r 854,480 manim_scenes/scene_26_drops_tubes.py Scene26DropsTubes
manim -ql --fps 15 -r 854,480 manim_scenes/scene_27_viscosity.py Scene27Viscosity
manim -ql --fps 15 -r 854,480 manim_scenes/scene_28_honey_glass.py Scene28HoneyGlass
manim -ql --fps 15 -r 854,480 manim_scenes/scene_29_synthesis.py Scene29Synthesis
manim -ql --fps 15 -r 854,480 manim_scenes/scene_30_subscribe.py Scene30Subscribe
```

### 2K final scenes · 2560 × 1440 · 30 fps

```bash
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_hook.py Scene01Hook
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_roadmap.py Scene02Roadmap
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_collisions.py Scene03Collisions
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_one_speed.py Scene04OneSpeed
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_velocity_space.py Scene05VelocitySpace
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_three_speeds.py Scene06ThreeSpeeds
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_hotter_lighter.py Scene07HotterLighter
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_kmt_rules.py Scene08KmtRules
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_two_cracks.py Scene09TwoCracks
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_attraction.py Scene10Attraction
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_size.py Scene11Size
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_tug_of_war.py Scene12TugOfWar
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_pressure_correction.py Scene13PressureCorrection
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_excluded_volume.py Scene14ExcludedVolume
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_vdw_equation.py Scene15VdwEquation
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_compressibility.py Scene16Compressibility
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_boyle_temperature.py Scene17BoyleTemperature
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_andrews.py Scene18Andrews
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_critical_point.py Scene19CriticalPoint
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_vdw_loops.py Scene20VdwLoops
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_continuity.py Scene21Continuity
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_22_cooling.py Scene22Cooling
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_23_vapour_pressure.py Scene23VapourPressure
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_24_boiling.py Scene24Boiling
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_25_surface_energy.py Scene25SurfaceEnergy
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_26_drops_tubes.py Scene26DropsTubes
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_27_viscosity.py Scene27Viscosity
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_28_honey_glass.py Scene28HoneyGlass
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_29_synthesis.py Scene29Synthesis
manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_30_subscribe.py Scene30Subscribe
```

### Whole episode

```bash
# 480p
manim -ql --fps 15 -r 854,480 manim_scenes/full_video.py FullVideo

# 2K / 1440p
manim -qh --fps 30 -r 2560,1440 manim_scenes/full_video.py FullVideo
```
