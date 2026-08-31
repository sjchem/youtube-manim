# Visual Calculus: From Limits to Derivatives — Part 1

A Manim Community Edition project for a connected, roughly 18-minute visual calculus film. It opens with a car easing away from a red light and a question no average velocity can answer, follows that question into the idea of a limit, a removable hole, the three faces of continuity, a geometric proof of `lim(x→0) sin(x)/x = 1`, a hand-built derivative of `x²`, and closes on the deepest idea in the film: zoom into any smooth curve far enough and it becomes indistinguishable from a straight line — its derivative.

The complete render behaves as one film rather than nine separate clips. It begins directly with the moving-car mystery; the title emerges inside Scene 1 only after the need for calculus has been established. Later scenes open on their next idea or visual, without numbered chapter labels or repeated title cards.

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
| 01 | `scene_01` | Motion hides a question | 0:00–2:20 | 2:20 |
| 02 | `scene_02` | Getting infinitely close | 2:20–4:15 | 1:55 |
| 03 | `scene_03` | A hole in the graph | 4:15–6:25 | 2:10 |
| 04 | `scene_04` | When the limit meets the function | 6:25–8:20 | 1:55 |
| 05 | `scene_05` | A beautiful trigonometric limit | 8:20–10:50 | 2:30 |
| 06 | `scene_06` | From secant to tangent | 10:50–12:58 | 2:08 |
| 07 | `scene_07` | The most powerful visual: local linearity | 12:58–14:48 | 1:50 |
| 08 | `scene_08` | Derivative as instantaneous change | 14:48–17:33 | 2:45 |
| 09 | `scene_09` | Subscribe | 17:33–17:48 | 0:15 |
|  |  | **Complete Part 1** | **0:00–17:48** | **17:48** |

List the same render map from the command line:

```bash
python main.py list
```

## Validation without rendering

Byte-compile everything, then check pacing with the timing-only audit, which advances Manim's animation clock and mobject state without drawing frames:

```bash
python -m compileall .
python main.py list
python utils/timing_audit.py --fps 15
python utils/layout_audit.py --fps 5
```

The timing audit reports how closely each chapter lands on its narration target. The layout audit advances every animation to its authored final state and flags readable text that leaves the frame or collides with other text.

## Fast preview rendering — `-pql`, 15 FPS

Use these commands for layout and timing checks. Remove `-p` on a headless machine. Add `--disable_caching` after changing animation timing.

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_moving_car.py Scene01MovingCar
python -m manim -pql --fps 15 manim_scenes/scene_02_limits.py Scene02Limits
python -m manim -pql --fps 15 manim_scenes/scene_03_hole_in_graph.py Scene03HoleInGraph
python -m manim -pql --fps 15 manim_scenes/scene_04_continuity.py Scene04Continuity
python -m manim -pql --fps 15 manim_scenes/scene_05_trig_limit.py Scene05TrigLimit
python -m manim -pql --fps 15 manim_scenes/scene_06_secant_to_tangent.py Scene06SecantToTangent
python -m manim -pql --fps 15 manim_scenes/scene_07_local_linearity.py Scene07LocalLinearity
python -m manim -pql --fps 15 manim_scenes/scene_08_derivative_meaning.py Scene08DerivativeMeaning
python -m manim -pql --fps 15 manim_scenes/scene_09_subscribe.py Scene09Subscribe
```

Or use the CLI wrapper, which resolves a scene by number or name:

```bash
python main.py preview scene_01
python main.py preview 6
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
python main.py scene scene_05
```

## 2K / 1440p renders — individual scenes

For YouTube-style 2K output (`2560×1440`) at 30 FPS, render every scene separately with:

```bash
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_01_moving_car.py Scene01MovingCar
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_02_limits.py Scene02Limits
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_03_hole_in_graph.py Scene03HoleInGraph
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_04_continuity.py Scene04Continuity
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_05_trig_limit.py Scene05TrigLimit
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_06_secant_to_tangent.py Scene06SecantToTangent
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_07_local_linearity.py Scene07LocalLinearity
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_08_derivative_meaning.py Scene08DerivativeMeaning
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_09_subscribe.py Scene09Subscribe
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
3. Target an accessible average delivery near 105 words per minute.
4. Place each clip at the exact timeline boundaries in the course table above.
5. If a generated clip differs materially in length, adjust that chapter's entry in `SCENE_DURATIONS` (`config.py`) and rebalance `narration_wait` calls in the matching scene file, then re-run `utils/timing_audit.py` to confirm it lands `OK`.

## Project structure

```text
calculus-1/
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
│   └── scene_01_*.py ... scene_09_*.py
├── utils/
│   ├── math_utils.py
│   ├── physics_models.py
│   ├── render_helpers.py
│   └── timing_audit.py
└── assets/
```

## Theme

This project uses the repository's local Oceanic Next theme (`themes/oceanic_next.py`), applied via `config.apply_project_theme` and the shared `manim_scenes/common.py::begin_scene` helper. `config.py` inserts the repo root onto `sys.path` so `from themes.oceanic_next import ...` resolves regardless of the current working directory.

## Part 2

Part 1 ends at the formal definition of the derivative and its meaning as instantaneous change. The final bridge announces Part 2: **From Derivatives to Integrals**, where instantaneous change leads into accumulation, area, antiderivatives, and the Fundamental Theorem of Calculus.
