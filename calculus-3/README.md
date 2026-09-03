# Visual Calculus: From Integrals to Differential Equations — Part 3

A Manim Community Edition project for a connected, 19:51 visual calculus film. It starts from a single question — *if we only know how something changes, can we recover the thing itself?* — and follows it from reversing a velocity graph all the way to slope fields, exponential growth and decay, Newton's law of cooling, separation of variables, the spring equation, the volume of a sphere by slicing, and a planetary orbit integrated numerically from Newton's law of gravitation.

The complete render behaves as one film rather than sixteen separate clips. It opens directly on a car disappearing down a road with only its speedometer visible; the title card emerges inside Chapter 1 only after that question has been posed. Later chapters open on their next idea, without numbered chapter labels or repeated title cards.

Three chapters (10, 11, 13) open the 3D camera: the oscillator's phase-space helix, the sphere swept out and sliced into disks, and the orbit. Every 3D chapter returns the camera to the flat orientation before handing over, so `FullVideo` renders all sixteen chapters as one continuous `ThreeDScene`.

## Requirements

- Python 3.12 or another version supported by Manim Community Edition
- Manim Community Edition 0.19–0.20 (developed against 0.19.2)
- A working LaTeX installation for `MathTex` (`latex`, `dvisvgm`)
- FFmpeg for video output

Install from this directory:

```bash
python -m pip install -r requirements.txt
```

The Oceanic Next theme is loaded from the repository's own `themes/` package. `config.py` puts the repo root on `sys.path`, so the project works from this subfolder with no installation step and no `PYTHONPATH` juggling.

## Course timeline

| Chapter | Source scene | Topic | View | Timeline | Duration |
|---:|---|---|---|---|---:|
| 01 | `scene_01` | The reverse problem | 2D | 0:00–1:00 | 1:00 |
| 02 | `scene_02` | The information a derivative throws away | 2D | 1:00–1:45 | 0:45 |
| 03 | `scene_03` | An equation about change itself | 2D | 1:45–2:50 | 1:05 |
| 04 | `scene_04` | The slope field, and curves that flow | 2D | 2:50–4:26 | 1:36 |
| 05 | `scene_05` | Growth proportional to size | 2D | 4:26–5:55 | 1:29 |
| 06 | `scene_06` | One sign flip, an opposite world | 2D | 5:55–7:16 | 1:21 |
| 07 | `scene_07` | Newton's law of cooling | 2D | 7:16–8:42 | 1:26 |
| 08 | `scene_08` | Separating the variables | 2D | 8:42–9:58 | 1:16 |
| 09 | `scene_09` | Which universe are we in? | 2D | 9:58–10:52 | 0:54 |
| 10 | `scene_10` | F = ma, and a spring that oscillates | 3D | 10:52–12:42 | 1:50 |
| 11 | `scene_11` | From area to volume, in 3D | 3D | 12:42–14:14 | 1:32 |
| 12 | `scene_12` | Area, volume, mass, probability — one idea | 2D | 14:14–15:08 | 0:54 |
| 13 | `scene_13` | From an equation to a future | 3D | 15:08–16:50 | 1:42 |
| 14 | `scene_14` | The language of modern science and AI | 2D | 16:50–17:54 | 1:04 |
| 15 | `scene_15` | The final revelation | 2D | 17:54–19:36 | 1:42 |
| 16 | `scene_16` | Subscribe card | 2D | 19:36–19:51 | 0:15 |
|  |  | **Complete Part 3** |  | **0:00–19:51** | **19:51** |
List the same render map from the command line:

```bash
python main.py list
```

## Validation without rendering

Byte-compile everything, then run the three frame-free audits. They advance Manim's animation clock and mobject state without drawing a single frame, so a full pass over all sixteen chapters takes a couple of minutes rather than hours:

```bash
python -m compileall .
python main.py list
python utils/narration_audit.py
python utils/timing_audit.py --fps 15
python utils/layout_audit.py --fps 5
```

- **`narration_audit.py`** reads `narration_script.md`, checks each chapter's spoken density stays between 85 and 112 words per minute, and verifies every authored window agrees with `SCENE_DURATIONS` in `config.py`. The closing card is exempt from the density check.
- **`timing_audit.py`** reports how closely each chapter lands on its narration window, flagging both overruns and more than three seconds of dead padding.
- **`layout_audit.py`** advances every animation to its authored final state and flags readable text that leaves the frame or collides with other text.

Both scene audits build a `ThreeDCamera` for the chapters listed in `config.THREE_D_SCENES`, because a renderer passed into `Scene.__init__` ignores `camera_class`.

## Fast preview rendering — `-pql`, 15 FPS

Use these for layout and timing checks. Drop `-p` on a headless machine. Add `--disable_caching` after changing animation timing.

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_reverse_problem.py Scene01ReverseProblem
python -m manim -pql --fps 15 manim_scenes/scene_02_missing_constant.py Scene02MissingConstant
python -m manim -pql --fps 15 manim_scenes/scene_03_equation_of_change.py Scene03EquationOfChange
python -m manim -pql --fps 15 manim_scenes/scene_04_slope_field.py Scene04SlopeField
python -m manim -pql --fps 15 manim_scenes/scene_05_exponential_growth.py Scene05ExponentialGrowth
python -m manim -pql --fps 15 manim_scenes/scene_06_exponential_decay.py Scene06ExponentialDecay
python -m manim -pql --fps 15 manim_scenes/scene_07_newton_cooling.py Scene07NewtonCooling
python -m manim -pql --fps 15 manim_scenes/scene_08_separation_of_variables.py Scene08SeparationOfVariables
python -m manim -pql --fps 15 manim_scenes/scene_09_initial_conditions.py Scene09InitialConditions
python -m manim -pql --fps 15 manim_scenes/scene_10_spring_oscillation.py Scene10SpringOscillation
python -m manim -pql --fps 15 manim_scenes/scene_11_area_to_volume.py Scene11AreaToVolume
python -m manim -pql --fps 15 manim_scenes/scene_12_one_idea.py Scene12OneIdea
python -m manim -pql --fps 15 manim_scenes/scene_13_equation_to_future.py Scene13EquationToFuture
python -m manim -pql --fps 15 manim_scenes/scene_14_modern_science.py Scene14ModernScience
python -m manim -pql --fps 15 manim_scenes/scene_15_synthesis.py Scene15Synthesis
python -m manim -pql --fps 15 manim_scenes/scene_16_subscribe.py Scene16Subscribe
```

`main.py` wraps the same commands:

```bash
python main.py preview 4        # low quality, one chapter
python main.py preview scene_11
python main.py scene 11         # full quality, one chapter
```

## Final render — 1080p, 30 FPS

```bash
python -m manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo
```

or equivalently:

```bash
python main.py render
```

The 3D chapters are the slow part of a full render: Cairo sorts every polygon of the sphere, the disk stacks, and the helix on each frame. Expect the 3D chapters to take several times longer per second of footage than the flat ones.

## ElevenLabs narration and final merge

1. Generate one ElevenLabs audio file from each spoken block in `narration_script.md`, for a total of sixteen clips. Do not synthesize the Markdown headings.
2. Keep the delivery curious and unhurried. The chapters are written for roughly 95–105 words per minute; the exact visual window for every clip is printed in both the narration headings and the course timeline above.
3. Render the silent `FullVideo`, then place each voice clip at its listed chapter start time in the editor. Clips 01–15 should hand off directly without an artificial ending pause.
4. Add music and effects only after the voice track is aligned. Duck them under equations and conceptual reveals so the narration remains dominant.
5. If ElevenLabs produces a materially different clip length, change that chapter in `SCENE_DURATIONS` in `config.py`, rebalance the `narration_wait` calls in its scene file, and rerun the narration and timing audits before the final render.

## Project layout

```
calculus-3/
├── main.py                 list / preview / render one chapter or the whole film
├── config.py               palette, fonts, frame size, chapter durations, theme hookup
├── narration_script.md     timestamped voice-over, one block per chapter
├── concept_summary.md      the mathematics, the numbers, and the honest limits
├── animation_plan.md       beat-by-beat plan for all sixteen chapters
├── youtube_package.md      title, description, chapters, tags, thumbnail, clips
├── manim_scenes/
│   ├── common.py           shared visual language: captions, glow, slope fields, props, 3D helpers
│   ├── full_video.py       all sixteen chapters as one deterministic ThreeDScene
│   └── scene_01..16_*.py   one module per chapter, each exposing `play_scene(scene)`
└── utils/
    ├── math_utils.py       exact closed forms, slope-field sampling, RK4
    ├── physics_models.py   the car, growth/decay, cooling cup, spring, orbit, solid of revolution
    ├── render_helpers.py   safe-frame fitting, field sampling, temperature colour mapping
    ├── narration_audit.py  spoken density vs authored windows
    ├── timing_audit.py     chapter length vs authored windows
    └── layout_audit.py     text overflow and collision
```

Every chapter module defines both a `Scene` class (so it renders standalone) and a `play_scene(scene)` function (so `full_video.py` can chain it onto a shared timeline). Nothing in the project depends on generated media files.

## Scientific accuracy

Every number displayed on screen is computed by `utils/math_utils.py` or `utils/physics_models.py`, so a value in the picture and a value in the narration cannot drift apart. Where the film approximates or uses a metaphor, it says so:

- The **slope field as a "wind field"** is a metaphor, stated as one in the narration. Nothing flows; the ticks are the slopes the equation demands, and a solution is tangent to them everywhere.
- The **coffee cooling constant** `k = 0.05 min⁻¹` is a plausible one-significant-figure value for a mug in still air, chosen so the curve reads well over forty minutes. The chapter's claim is about the shape of the curve, not the number.
- The **planetary orbit** is integrated, not drawn. The two-body problem has no elementary closed form for `r(t)`, so `OrbitingBody.trajectory` solves `r'' = −μ r/|r|³` with fixed-step RK4. Energy drifts by about one part in 10¹² over the plotted arc and the path closes to within 0.3% of its radius.
- The **disk stack** is honestly an approximation: the on-screen tally at 7, 14, and 28 disks is a real midpoint sum converging on `4π/3`, not a claim that the stack equals the sphere.
- The **colony** is discrete while the model is continuous, which is why the generation ladder is shown before the smooth curve.
- The **orbit** follows the same numerical-accumulation idea shown immediately before it: repeatedly add the current rate times a tiny time step. The production solver uses RK4 rather than the displayed first-order Euler step, which is shown as the conceptual core of numerical integration.

`concept_summary.md` carries the full table of on-screen values with their sources, plus references.

## Rendering notes worth knowing

Two Cairo-specific problems shaped `manim_scenes/common.py`, and both are commented at the definition site:

- **Surfaces of revolution need clustered sampling.** `revolution_surface` samples `x` through a cosine substitution. A profile like `√(1 − x²)` has vertical tangents at both ends, so uniform sampling leaves one enormous, near-edge-on band of quads at each pole, which Cairo draws as long slivers radiating out of the solid.
- **`Cylinder` ignores `fill_color`.** It inherits `Surface`'s checkerboard colouring, so the disk stack sets `checkerboard_colors` instead; its generated end caps ignore that colouring too and are switched off.

The title card's drop shadow deliberately overlaps its own glyphs and is tagged so `layout_audit.py` does not report it as a collision.
