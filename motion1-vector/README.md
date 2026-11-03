# Vectors & Projectile Motion — The Geometry of 2D Motion

**Can we use vectors and the laws of motion to predict an object's position,
velocity and trajectory in two dimensions?** Episode 01 of *Visualized Physics —
From Motion to the Quantum World*: a Manim film (planned running time
**41:42**) built as 29 scenes that map onto the brief's **9 YouTube chapters**.

One throw drives the whole film: **20 m/s at 45°**. Every chapter of vector
mathematics (addition, subtraction, scalar multiplication, unit vectors,
components) is a tool that the final third uses to predict that throw:
14.14 m/s each way, 2.89 s in the air, 10.20 m high, 40.82 m long. The central
picture is the one in the first minute — the ball's **floor shadow glides
steadily while its wall shadow only rises and falls** — and the film spends
40 minutes earning it.

- [`concept_summary.md`](concept_summary.md) — the science, worked numbers, the model's limits, sources
- [`animation_plan.md`](animation_plan.md) — scene-by-scene visuals and where the 3D is
- [`narration_script.md`](narration_script.md) — full timestamped script; ElevenLabs-tagged version in [`narration_script_tagged.md`](narration_script_tagged.md); per-beat timing plan in [`narration_cues.md`](narration_cues.md)
- [`youtube_package.md`](youtube_package.md) — titles, description, chapters, tags, thumbnail idea

## Why Manim CE (and not ManimGL)

The brief prefers ManimGL for 3D, and ManimGL 1.7.2 is installed in the
`youtube` env. This film is still built on **Manim Community Edition 0.22**, on
purpose:

* the channel's shared Oceanic Next theme (`../themes/oceanic_next.py`) is
  written against CE through `manim_themes`, so a ManimGL scene could not use
  the house look that ties the videos together;
* the one-scene full-film render (`FullVideo`) needs a single engine.

The 3D comes from the projection engine shared with the previous films
([`manim_scenes/stage3d.py`](manim_scenes/stage3d.py)): bodies keep real 3D
coordinates, the stage turns and projects them every frame with perspective
and depth sorting, and captions stay ordinary 2D text (so none of CE's
`ThreeDScene` HUD bugs apply). For this film it gained a ruled **`Grid`**
(ground and shadow wall), a glowing **`Curve`** (trails, the running track,
the space-time curve) and a flat **`Disc`** (shadows, drone rotors, strobe
marks). On top of it, `common.Flight` is a projectile driven by one clock that
the ball, trail, both shadows, all velocity arrows and the strobe ghosts read
every frame.

Scene headings hold for 3 seconds, then fade over 0.7 seconds without shifting narration cues. Explanations are spoken; on-screen text is limited to short labels, symbols, equations and worked values. The reviewed attachment is in `assets/references/episode_outline_reviewed.txt`.

3D chapters: 01 (the hook throw and its two shadows), 05 (3-4-5 walk and a
400 m lap), 07 (delivery drone), 11 (parallel-light component projections and tip-to-tail reconstruction), 18, 20, 21, 22 (the throw: gravity arrow,
floor strobe, wall shadow with live v_y graph, the frozen apex), 23 (the
flight as a **space-time curve** read from above, from the side and down the
time axis), 25 (range ruler), 26 (a fan of five throws), 28 (the closing throw).

## Everything on screen is computed

* **One model** (`utils/physics_models.py`): every worked example of the brief
  is data there — the 3-4-5 walk, the 6-8-10 drone, (5, 3) − (2, 1),
  3i + 4j, 10 at 30°, (−3, 4) for the atan2 trap, (4, 3) + (−2, 5) — and
  `Projectile` computes v_x, v_y(t), x(t), y(t), T, t_H, H, R and y(x).
  Scenes ask the model; they don't type results.
* **Beyond the ideal model**, only to show where it stops: a foam ball with
  quadratic drag, integrated with RK4 (range 25.0 m instead of 40.8; best
  angle 41°), and a launch from a 10 m ledge (best angle 39.3°, closed form
  checked against a numerical scan).
* **Spoken numbers** (`utils/motion_data.py`): `python -m utils.motion_data`
  recomputes all 45 numbers the narrator says, converts each to words
  ("fourteen point one four") and checks the phrase is still in
  `narration.py`, plus 10 qualitative claims (30° and 60° land together; the
  top is the slowest point; drag lowers the best angle; …).
* **Colour is meaning**, everywhere: horizontal blue, vertical rose, velocity
  gold, acceleration/gravity orange, position teal, resultant green, the
  second vector (and time) purple, traps red.

## Setup

From this folder, in the repository's `youtube` pyenv environment:

```bash
~/.pyenv/versions/youtube/bin/pip install -r requirements.txt
```

You also need FFmpeg/ffprobe, LaTeX with dvisvgm, Cairo/Pango and the Lato font
(see `requirements.txt`), plus the shared `themes/` folder one level up.
`config.py` adds the repository root to `sys.path`, so the theme imports from
inside this sub-folder. (The env prints a harmless "SoX could not be found"
warning on import; it comes from an installed plugin, not this project.)

## Preview and render

```bash
python main.py list                # scene names, start times and durations
python main.py chapters            # the 9 YouTube chapter markers
python main.py preview 21          # one scene at 854×480, 15 fps
python main.py preview all         # separate previews of all 29 scenes
python main.py preview full        # the full film at preview quality
python main.py scene 21            # one scene at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
python main.py check               # model, spoken numbers, narration, timing and layout audits
python main.py audio-check         # recorded narration clips vs scene lengths
```

Final 1080p film, directly with Manim:

```bash
python -m manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo
```

Output: `media/videos/full_video/1080p30/FullVideo.mp4`.

## Commands for every scene at 480p and 2K

Run these commands from this project folder with the `youtube` Python environment
active. Each block contains scenes 01–29 in order and produces a separate MP4
for each scene; copy the whole block to render them all, or run individual lines.
Here **2K** means **2560×1440 (1440p/QHD)**, preserving the film's 16:9 frame.

### 480p previews — all 29 scenes

```bash
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_predict_flight.py Scene01PredictFlight
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_three_questions.py Scene02ThreeQuestions
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_scalars.py Scene03Scalars
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_vectors.py Scene04Vectors
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_displacement.py Scene05Displacement
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_why_add.py Scene06WhyAdd
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_drone.py Scene07Drone
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_subtraction.py Scene08Subtraction
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_scalar_multiple.py Scene09ScalarMultiple
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_unit_vectors.py Scene10UnitVectors
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_resolve.py Scene11Resolve
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_sin_cos.py Scene12SinCos
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_component_sum.py Scene13ComponentSum
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_position.py Scene14Position
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_velocity.py Scene15Velocity
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_acceleration.py Scene16Acceleration
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_equations.py Scene17Equations
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_projectile.py Scene18Projectile
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_launch.py Scene19Launch
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_horizontal.py Scene20Horizontal
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_vertical.py Scene21Vertical
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_22_top.py Scene22Top
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_23_parabola.py Scene23Parabola
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_24_time_height.py Scene24TimeHeight
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_25_range.py Scene25Range
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_26_best_angle.py Scene26BestAngle
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_27_challenges.py Scene27Challenges
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_28_synthesis.py Scene28Synthesis
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_29_subscribe.py Scene29Subscribe
```

Output: `media/videos/<scene_module>/480p15/<SceneClass>.mp4`.

### 2K / 1440p renders — all 29 scenes

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_predict_flight.py Scene01PredictFlight
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_three_questions.py Scene02ThreeQuestions
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_scalars.py Scene03Scalars
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_vectors.py Scene04Vectors
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_displacement.py Scene05Displacement
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_why_add.py Scene06WhyAdd
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_drone.py Scene07Drone
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_subtraction.py Scene08Subtraction
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_scalar_multiple.py Scene09ScalarMultiple
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_unit_vectors.py Scene10UnitVectors
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_resolve.py Scene11Resolve
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_sin_cos.py Scene12SinCos
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_component_sum.py Scene13ComponentSum
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_position.py Scene14Position
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_velocity.py Scene15Velocity
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_acceleration.py Scene16Acceleration
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_equations.py Scene17Equations
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_projectile.py Scene18Projectile
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_launch.py Scene19Launch
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_horizontal.py Scene20Horizontal
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_vertical.py Scene21Vertical
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_22_top.py Scene22Top
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_23_parabola.py Scene23Parabola
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_24_time_height.py Scene24TimeHeight
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_25_range.py Scene25Range
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_26_best_angle.py Scene26BestAngle
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_27_challenges.py Scene27Challenges
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_28_synthesis.py Scene28Synthesis
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_29_subscribe.py Scene29Subscribe
```

Output: `media/videos/<scene_module>/1440p30/<SceneClass>.mp4`.

## Narration and voice

`narration.py` is the timing source: each scene's beats are `(start second,
spoken line)` and the scene code waits for each with `beat(scene, t, i)`, so a
picture can never drift from its sentence. After editing a line:

```bash
python -m utils.narration_audit      # every beat speakable in its window (≤ 2.85 words/s)
python -m utils.motion_data          # spoken numbers still match the model
python -m utils.narration_export --beats   # regenerate scripts, cue sheets, per-beat text files
```

Recordings go in `assets/audio/` as either one clip per scene
(`scene_07.wav`) or one per beat (`scene_07/beat_001.wav` …); `start()`
attaches them automatically and refuses clips longer than their window.

## Checks

`python main.py check` runs, in order: `utils.math_utils`,
`utils.physics_models`, `utils.motion_data`, `utils.visual_contract_audit`, `utils.narration_audit`,
`utils.timing_audit` at 15 and 30 fps (every scene lands on its
`config.SCENE_DURATIONS` second; no cue overruns; no idle tail over 4 s),
`utils.timing_audit --full` (FullVideo constructs end to end with 0 stray
mobjects) and `utils.layout_audit --motion` (no text outside the frame or on
top of other text, sampled mid-animation too; expired titles stay invisible
and essential flight balls and arrows stay inside the frame).

Stills without rendering video:

```bash
python -m utils.storyboard 23 --every 3
python -m utils.contact_sheet scene_23 --cols 4
```

## Project layout

```
config.py              palette, type scale, scene durations, YouTube chapters
narration.py           the script, as timed beats
narration_delivery.py  sparse ElevenLabs delivery cues
main.py                CLI (list / preview / render / check)
manim_scenes/
  common.py            the visual grammar: lifecycle, type, VecArrow, plane,
                       SideFlight, Flight, field_stage, props (car, drone, gauges)
  stage3d.py           projected 3D engine: Stage, Ball, Rod, Grid, Curve, Disc, Vector, Tag
  scene_01 … scene_29  one file per scene, each a play_scene(scene) function
  full_video.py        all 29 scenes in one Scene
utils/
  physics_models.py    vectors, the projectile, drag, the ledge
  motion_data.py       spoken-number check
  timing_audit.py, layout_audit.py, narration_audit.py, storyboard.py,
  contact_sheet.py, narration_export.py, voiceover.py, math_utils.py, render_helpers.py
```
