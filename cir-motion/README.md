# Circular Motion — Why Changing Direction Means Acceleration

**How can an object accelerate continuously when its speed never changes?**
Episode 02 of *Visualized Physics — From Motion to the Quantum World*, and the
sequel to Episode 01 (`../motion1-vector`): a Manim film of **37:40** built as
26 scenes in the brief's **7 YouTube chapters**.

The film opens on one picture: a car at a steady 20 m/s, first on a straight
road (its gold velocity arrow never changes, a = 0), then on a circular track
(same speedometer, but the arrow never stops turning). Everything after it
explains that arrow: why the change in velocity points to the centre, why its
size is v²/r, how we measure turning (radians, ω, T, f, α), which real forces
do the inward job, and what changes when the speed changes too.

One particle carries the mathematics throughout (`physics_models.REFERENCE`,
the brief's own): **2 kg on a 2 m circle at 4 m/s** — 2 rad/s, a period of
π s ≈ 3.14 s, 0.318 Hz, 8 m/s², 16 N.

- [`review_notes.md`](review_notes.md) — scene-by-scene visual review and validation
- [`concept_summary.md`](concept_summary.md) — the science, worked numbers, assumptions, sources
- [`animation_plan.md`](animation_plan.md) — every scene's visuals (generated from the scene docstrings)
- [`assets/references/brief_review.md`](assets/references/brief_review.md) — what was clarified or corrected in the brief
- [`narration_script.md`](narration_script.md) — full timestamped script; ElevenLabs-tagged version in [`narration_script_tagged.md`](narration_script_tagged.md); per-beat timing in [`narration_cues.md`](narration_cues.md)
- [`youtube_package.md`](youtube_package.md) — titles, description, chapters, tags, thumbnail idea

## Why Manim CE (and not ManimGL)

The brief prefers ManimGL for its 3D, and ManimGL 1.7.2 is installed in the
`youtube` env. This film is still built on **Manim Community Edition 0.22**, on
purpose, exactly as Episode 01 was:

* the channel's shared Oceanic Next theme (`../themes/oceanic_next.py`) is
  written against CE through `manim_themes`, so a ManimGL scene could not use
  the house look that ties the episodes together;
* the one-scene full-film render (`FullVideo`) needs a single engine;
* an Episode 02 must speak Episode 01's visual language — the same arrows,
  colours and 3D stage.

The 3D comes from the projection engine shared with Episode 01
([`manim_scenes/stage3d.py`](manim_scenes/stage3d.py)): bodies keep real 3D
coordinates, the stage turns and projects them every frame with perspective
and depth sorting, and captions stay ordinary 2D text (so none of CE's
`ThreeDScene` HUD bugs apply). For this film it gained a lit **`Block`** (cars
built from shaded boxes that hide their back faces), a **`Band`** (roads and
running tracks, with a real hole in the middle) and a **`globe`** (an Earth
whose meridian grid hides behind it as it turns). On top of it,
`common.Circuit` puts a ball or a car on a circle driven by one clock that the
body and its velocity and acceleration arrows all read.

3D chapters: 01 (straight road and circular track), 04 (the tangent), 05 (the
circle stretched into a **space-time helix** whose wall shadows are a cosine
and a sine), 06 (one lap of a running track), 10 (two circuits on one clock),
13 (a turntable: one ω, two speeds), 17 (a ball on a string on a table; the
string snaps), 18 (a flat curve: one car holds it, one drifts wide), 19
(**Newton's cannon** round a turning Earth; the real 400 km orbit to scale),
22 (a car speeding up and slowing down), 25 (the closing track).

Scene headings hold for 3 seconds, then fade over 0.7 seconds without shifting
narration cues. Chapter openers show only the title, without numbered badges. Explanations are spoken; on-screen text is limited to short
labels, symbols, equations and worked values.

## Everything on screen is computed

* **One model** (`utils/physics_models.py`): `Circular` (position, velocity,
  acceleration, ω, T, f, a_c, F_c), `SpeedingUp` (constant α), the 5î/5ĵ
  velocities, the small-angle ratio 2 sin(x/2)/x, the doubled speed and radius,
  Newton's coast-and-nudge polygon (vertices stay on the circle; the nudge rate
  tends to v²/r), the turntable, the flat curve (v_max = √(μ_s g r); the
  skidding car's tightest bend v²/(μ_s g)), and orbits (v = √(GM/r),
  T = 2π√(r³/GM), RK4 cannon shots under inverse-square gravity). Scenes ask
  the model; they don't type results.
* **Spoken numbers** (`utils/circle_data.py`): `python -m utils.circle_data`
  recomputes all 47 numbers the narrator says, converts each to words
  ("seven point zero seven") and checks the phrase is still in `narration.py`,
  plus 10 qualitative claims (double v → 4a; 15 m/s holds the 50 m curve and
  20 m/s does not; gravity 400 km up is still most of its surface value; …).
* **Pictures are the physics** (`utils/visual_contract_audit.py`): drawn velocity
  arrows are the numerical derivative of the drawn position (tangent, ⊥ r) at
  true length; acceleration arrows point at the centre at length v²/r, in 2D
  and on the 3D stage; comparisons share one physical clock; the centrifugal
  passenger coasts in a straight line until the door reaches it.
* **Colour is meaning**, everywhere: position teal, velocity gold, acceleration
  toward the centre and every Δv orange, tangential acceleration purple, their
  total white, net force green, angles and angular quantities cyan, x and y
  components blue and rose, traps red.

## Setup

From this folder, in the repository's `youtube` pyenv environment:

```bash
~/.pyenv/versions/youtube/bin/pip install -r requirements.txt
```

You also need FFmpeg/ffprobe, LaTeX with dvisvgm, Cairo/Pango and the Lato font
(see `requirements.txt`), plus the shared `themes/` folder one level up. (The
env prints a harmless "SoX could not be found" warning on import.)

## Preview and render

```bash
python main.py list                # scene names, start times and durations
python main.py chapters            # the 7 YouTube chapter markers
python main.py preview 19          # one scene at 854×480, 15 fps
python main.py preview all         # separate previews of all 26 scenes
python main.py preview full        # the full film at preview quality
python main.py scene 19            # one scene at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
python main.py check               # model, spoken numbers, contracts, narration, timing and layout audits
python main.py audio-check         # recorded narration clips vs scene lengths
```

Final 1080p film, directly with Manim:

```bash
python -m manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo
```

Output: `media/videos/full_video/1080p30/FullVideo.mp4`.

### 480p previews — every scene

```bash
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_acceleration.py Scene02Acceleration
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_speed_velocity.py Scene03SpeedVelocity
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_tangent.py Scene04Tangent
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_components.py Scene05Components
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_one_lap.py Scene06OneLap
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_delta_v.py Scene07DeltaV
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_velocity_triangle.py Scene08VelocityTriangle
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_derivation.py Scene09Derivation
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_speed_radius.py Scene10SpeedRadius
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_falling_around.py Scene11FallingAround
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_radians.py Scene12Radians
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_angular_velocity.py Scene13AngularVelocity
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_period.py Scene14Period
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_angular_accel.py Scene15AngularAccel
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_centripetal_force.py Scene16CentripetalForce
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_string.py Scene17String
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_car_friction.py Scene18CarFriction
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_satellite.py Scene19Satellite
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_centrifugal.py Scene20Centrifugal
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_uniform.py Scene21Uniform
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_22_nonuniform.py Scene22Nonuniform
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_23_table.py Scene23Table
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_24_challenges.py Scene24Challenges
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_25_synthesis.py Scene25Synthesis
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_26_subscribe.py Scene26Subscribe
```

### 2K / 1440p renders — every scene

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_acceleration.py Scene02Acceleration
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_speed_velocity.py Scene03SpeedVelocity
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_tangent.py Scene04Tangent
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_components.py Scene05Components
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_one_lap.py Scene06OneLap
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_delta_v.py Scene07DeltaV
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_velocity_triangle.py Scene08VelocityTriangle
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_derivation.py Scene09Derivation
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_speed_radius.py Scene10SpeedRadius
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_falling_around.py Scene11FallingAround
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_radians.py Scene12Radians
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_angular_velocity.py Scene13AngularVelocity
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_period.py Scene14Period
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_angular_accel.py Scene15AngularAccel
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_centripetal_force.py Scene16CentripetalForce
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_string.py Scene17String
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_car_friction.py Scene18CarFriction
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_satellite.py Scene19Satellite
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_centrifugal.py Scene20Centrifugal
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_uniform.py Scene21Uniform
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_22_nonuniform.py Scene22Nonuniform
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_23_table.py Scene23Table
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_24_challenges.py Scene24Challenges
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_25_synthesis.py Scene25Synthesis
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_26_subscribe.py Scene26Subscribe
```

Output: `media/videos/<scene_module>/<quality>/<SceneClass>.mp4`.

## Narration and voice

`narration.py` is the timing source: each scene's beats are `(start second,
spoken line)` and the scene code waits for each with `beat(scene, t, i)`, so a
picture can never drift from its sentence. After editing a line:

```bash
python -m utils.narration_audit            # every beat speakable in its window (≤ 2.85 words/s)
python -m utils.circle_data                # spoken numbers still match the model
python -m utils.narration_export --beats   # regenerate scripts, cue sheets, per-beat text files
```

Recordings go in `assets/audio/` as either one clip per scene
(`scene_07.wav`) or one per beat (`scene_07/beat_001.wav` …); `start()`
attaches them automatically and refuses clips longer than their window.

## Checks

`python main.py check` runs, in order: `utils.math_utils`,
`utils.physics_models`, `utils.circle_data`, `utils.visual_contract_audit`,
`utils.narration_audit`, `utils.timing_audit` at 15 and 30 fps (every scene
lands on its `config.SCENE_DURATIONS` second; no cue overruns; no idle tail
over 4 s), `utils.timing_audit --full` (FullVideo constructs end to end with 0
stray mobjects) and `utils.layout_audit --motion` (no text outside the frame
or on top of other text, sampled mid-animation too; expired titles stay
invisible; essential balls, cars and arrows stay inside the frame). The last run is
in `output/validation.txt`.

Stills without rendering video:

```bash
python -m utils.storyboard 19 --every 3
python -m utils.contact_sheet scene_19 --cols 4
```

## Project layout

```
config.py              palette, type scale, scene durations, YouTube chapters
narration.py           the script, as timed beats
narration_delivery.py  sparse ElevenLabs delivery cues
main.py                CLI (list / preview / render / check)
manim_scenes/
  common.py            the visual grammar: lifecycle, type, VecArrow, CircleView, Circuit,
                       ground/tracks/cars/globe, props (Car, Speedometer)
  stage3d.py           projected 3D engine: Stage, Ball, Rod, Grid, Curve, Disc, Block, Band, Vector, Tag
  scene_01 … scene_26  one file per scene, each a play_scene(scene) function
  full_video.py        all 26 scenes in one Scene
utils/
  physics_models.py    circular motion, forces, orbits, Newton's polygon, cannon shots
  circle_data.py       spoken-number check
  visual_contract_audit.py, timing_audit.py, layout_audit.py, narration_audit.py,
  storyboard.py, contact_sheet.py, narration_export.py, voiceover.py, math_utils.py, render_helpers.py
```
