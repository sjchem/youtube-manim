# Why Dividing by Zero Breaks Mathematics?

A complete Manim Community Edition project for a cinematic 7-8 minute YouTube-style explainer about division by zero, limits, infinity, indeterminate forms, and computation.

## Concept Summary

Division is reverse multiplication. For ordinary division, `a ÷ b = c` means `c × b = a`. Multiplying by zero destroys information because every input maps to the same output: zero. That makes `6 ÷ 0` impossible because no number times zero is six, while `0 ÷ 0` is indeterminate because every number times zero is zero. Limits such as `1/x` near zero can grow without bound, but approaching zero is not the same as dividing by zero.

## Project Tree

```text
division_by_zero_breaks_math/
├── main.py
├── config.py
├── manim.cfg
├── requirements.txt
├── README.md
├── narration_script.md
├── manim_scenes/
│   ├── __init__.py
│   ├── common.py
│   ├── full_video.py
│   ├── scene_01.py
│   ├── scene_02.py
│   ├── scene_03.py
│   ├── scene_04.py
│   ├── scene_05.py
│   ├── scene_06.py
│   ├── scene_07.py
│   └── scene_08.py
├── utils/
│   ├── math_utils.py
│   ├── physics_models.py
│   └── render_helpers.py
├── assets/
│   ├── audio/
│   ├── images/
│   ├── references/
│   ├── sounds/
│   └── textures/
├── media/
└── output/
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Manim also needs system packages for rendering and LaTeX. If `MathTex` fails, install a TeX distribution such as TeX Live.

## Preview Render

```bash
python main.py --scene Scene01Hook --quality pql
```

Equivalent direct Manim command:

```bash
manim -pql manim_scenes/scene_01.py Scene01Hook
```

## Individual Scene Commands

```bash
manim -pql manim_scenes/scene_01.py Scene01Hook
manim -pql manim_scenes/scene_02.py Scene02ReverseMultiplication
manim -pql manim_scenes/scene_03.py Scene03ZeroCollapse
manim -pql manim_scenes/scene_04.py Scene04NoSolution
manim -pql manim_scenes/scene_05.py Scene05LimitsNotInfinity
manim -pql manim_scenes/scene_06.py Scene06ZeroOverZero
manim -pql manim_scenes/scene_07.py Scene07Computers
manim -pql manim_scenes/scene_08.py Scene08FinalSummary
```

## Full 1080p Render

```bash
python main.py --full --quality pqh
```

Equivalent direct Manim command:

```bash
manim -pqh manim_scenes/full_video.py FullVideo
```

## Troubleshooting

- `ModuleNotFoundError: manim`: activate the virtual environment and run `pip install -r requirements.txt`.
- `LaTeX error converting to dvi`: install TeX Live or another LaTeX distribution.
- `manim_physics` import issues: this project treats it as optional and uses custom particle effects if it is unavailable.
- Broken global Manim plugins: Manim may import installed plugin entry points before project code runs. If an unrelated plugin fails during `from manim import *`, uninstall or upgrade that plugin in the active environment, then rerun the command.
- Slow full render: preview with `-pql`, then render final with `-pqh`.
- Missing audio: no audio is required. Asset folders are placeholders for optional narration, music, or sound design.

## Scene Classes

- `Scene01Hook`
- `Scene02ReverseMultiplication`
- `Scene03ZeroCollapse`
- `Scene04NoSolution`
- `Scene05LimitsNotInfinity`
- `Scene06ZeroOverZero`
- `Scene07Computers`
- `Scene08FinalSummary`
- `FullVideo`
