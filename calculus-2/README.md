# Visual Calculus: From Derivatives to Integrals — Part 2

A Manim Community Edition project for a connected, roughly 17.5-minute visual calculus film. A derivative measures how fast something changes; an integral measures how much has accumulated. This film builds the bridge between them: a car's changing velocity leads into Riemann sums, the literal meaning of `dx`, a synchronized reveal of the Fundamental Theorem of Calculus (`A'(x) = f(x)`), a derivative shown as an entire new function, maxima and minima, a real fenced-garden optimization, the mystery of the integration constant `+C`, substitution and integration by parts derived geometrically, the area between two curves, and a closing synthesis tying position, velocity, and accumulated displacement into one picture.

The complete render behaves as one film rather than fourteen separate clips. It opens directly with the "how far did it go?" question; the title emerges inside Scene 1 only after that question is posed. Later scenes open on their next idea or visual, without numbered chapter labels or repeated title cards.

## Requirements

- Python 3.12 or another version supported by Manim Community Edition
- Manim Community Edition 0.19–0.20
- A working LaTeX installation for `MathTex` (`latex`, `dvisvgm`)
- FFmpeg for video output

Install from this directory:

```bash
python -m pip install -r requirements.txt
```

## Course timeline

| Chapter | Source scene | Topic | Timeline | Duration |
|---:|---|---|---|---:|
| 01 | `scene_01` | Velocity becomes distance | 0:00–1:29 | 1:29 |
| 02 | `scene_02` | Rectangles become the integral | 1:29–2:53 | 1:24 |
| 03 | `scene_03` | What dx really means | 2:53–3:49 | 0:56 |
| 04 | `scene_04` | The Fundamental Theorem, revealed | 3:49–5:41 | 1:52 |
| 05 | `scene_05` | f(x) = x, and a loop that closes | 5:41–6:46 | 1:05 |
| 06 | `scene_06` | A derivative is a new function | 6:46–7:57 | 1:11 |
| 07 | `scene_07` | Maxima and minima | 7:57–8:53 | 0:56 |
| 08 | `scene_08` | The fenced-garden optimization | 8:53–10:29 | 1:36 |
| 09 | `scene_09` | Reversing the derivative, and +C | 10:29–11:43 | 1:14 |
| 10 | `scene_10` | Substitution as new coordinates | 11:43–12:53 | 1:10 |
| 11 | `scene_11` | Integration by parts, geometrically | 12:53–14:08 | 1:15 |
| 12 | `scene_12` | Area between curves | 14:08–15:09 | 1:01 |
| 13 | `scene_13` | The deep connection and final revelation | 15:09–17:19 | 2:10 |
| 14 | `scene_14` | Subscribe | 17:19–17:34 | 0:15 |
|  |  | **Complete Part 2** | **0:00–17:34** | **17:34** |

List the same render map from the command line:

```bash
python main.py list
```

## Validation without rendering

Byte-compile everything, then check pacing with the timing-only audit, which advances Manim's animation clock and mobject state without drawing frames:

```bash
python -m compileall .
python main.py list
python utils/narration_audit.py
python utils/timing_audit.py --fps 15
python utils/layout_audit.py --fps 5
```

The timing audit reports how closely each chapter lands on its narration target. The layout audit advances every animation to its authored final state and flags readable text that leaves the frame or collides with other text.

## Fast preview rendering — `-pql`, 15 FPS

Use these commands for layout and timing checks. Remove `-p` on a headless machine. Add `--disable_caching` after changing animation timing.

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_velocity_to_distance.py Scene01VelocityToDistance
python -m manim -pql --fps 15 manim_scenes/scene_02_riemann_sums.py Scene02RiemannSums
python -m manim -pql --fps 15 manim_scenes/scene_03_what_is_dx.py Scene03WhatIsDx
python -m manim -pql --fps 15 manim_scenes/scene_04_fundamental_theorem.py Scene04FundamentalTheorem
python -m manim -pql --fps 15 manim_scenes/scene_05_beautiful_example.py Scene05BeautifulExample
python -m manim -pql --fps 15 manim_scenes/scene_06_derivative_new_function.py Scene06DerivativeNewFunction
python -m manim -pql --fps 15 manim_scenes/scene_07_maxima_minima.py Scene07MaximaMinima
python -m manim -pql --fps 15 manim_scenes/scene_08_optimization_garden.py Scene08OptimizationGarden
python -m manim -pql --fps 15 manim_scenes/scene_09_reverse_problem.py Scene09ReverseProblem
python -m manim -pql --fps 15 manim_scenes/scene_10_substitution.py Scene10Substitution
python -m manim -pql --fps 15 manim_scenes/scene_11_integration_by_parts.py Scene11IntegrationByParts
python -m manim -pql --fps 15 manim_scenes/scene_12_area_between_curves.py Scene12AreaBetweenCurves
python -m manim -pql --fps 15 manim_scenes/scene_13_synthesis.py Scene13Synthesis
python -m manim -pql --fps 15 manim_scenes/scene_14_subscribe.py Scene14Subscribe
```

Or use the CLI wrapper, which resolves a scene by number or name:

```bash
python main.py preview scene_01
python main.py preview 8
```

Render the connected film at preview quality:

```bash
python -m manim -pql --fps 15 --disable_caching manim_scenes/full_video.py FullVideo
```

## Final 1080p render

```bash
python -m manim -p --resolution 1920,1080 --fps 30 --disable_caching manim_scenes/full_video.py FullVideo
```

or, using the CLI wrapper's configured render settings (`config.py: RENDER`):

```bash
python main.py render
```

Render an individual chapter at the same settings:

```bash
python main.py scene scene_08
```

## 2K / 1440p renders — individual scenes

For YouTube-style 2K output (`2560×1440`) at 30 FPS, render every scene separately with:

```bash
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_01_velocity_to_distance.py Scene01VelocityToDistance
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_02_riemann_sums.py Scene02RiemannSums
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_03_what_is_dx.py Scene03WhatIsDx
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_04_fundamental_theorem.py Scene04FundamentalTheorem
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_05_beautiful_example.py Scene05BeautifulExample
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_06_derivative_new_function.py Scene06DerivativeNewFunction
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_07_maxima_minima.py Scene07MaximaMinima
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_08_optimization_garden.py Scene08OptimizationGarden
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_09_reverse_problem.py Scene09ReverseProblem
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_10_substitution.py Scene10Substitution
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_11_integration_by_parts.py Scene11IntegrationByParts
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_12_area_between_curves.py Scene12AreaBetweenCurves
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_13_synthesis.py Scene13Synthesis
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_14_subscribe.py Scene14Subscribe
```

Render the complete connected film at the same resolution:

```bash
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/full_video.py FullVideo
```

Remove `-p` when rendering on a headless machine or when you do not want Manim to open the completed video automatically.

Rendered files are written below `media/videos/`, grouped by source file and resolution.

## Narration workflow

1. Open `narration_script.md` and generate one audio file per chapter block.
2. Do not synthesize the Markdown headings.
3. Target an accessible 95–105 words per minute, slowing slightly for the Fundamental Theorem and other equation-heavy reveals.
4. Place each clip at the exact timeline boundaries in the course table above.
5. If a generated clip differs materially in length, adjust that chapter's entry in `SCENE_DURATIONS` (`config.py`) and rebalance `narration_wait` calls in the matching scene file, then re-run `utils/timing_audit.py` to confirm it lands `OK`.

## Project structure

```text
calculus-2/
├── main.py
├── config.py
├── README.md
├── concept_summary.md
├── animation_plan.md
├── narration_script.md
├── youtube_package.md
├── manim_scenes/
│   ├── common.py
│   ├── full_video.py
│   └── scene_01_*.py ... scene_14_*.py
├── utils/
│   ├── math_utils.py
│   ├── physics_models.py
│   ├── render_helpers.py
│   ├── timing_audit.py
│   └── layout_audit.py
└── assets/
```

## Theme

This project uses the repository's local Oceanic Next theme (`themes/oceanic_next.py`), applied via `config.apply_project_theme` and the shared `manim_scenes/common.py::begin_scene` helper. `config.py` inserts the repo root onto `sys.path` so `from themes.oceanic_next import ...` resolves regardless of the current working directory.

## Part 1

Part 2 assumes the material covered in Part 1, **From Limits to Derivatives**: limits, continuity, and the formal definition of the derivative as a limit of secant slopes. Scene 06 of this film briefly revisits the derivative's meaning before moving into new territory: accumulation, the Fundamental Theorem of Calculus, optimization, and the core integration techniques.
