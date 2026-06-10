# Why Motivation Fades: The Physics Behind Discipline

A complete Manim Community Edition project for a cinematic 7-8 minute scientific YouTube animation about motivation, discipline, habits, procrastination, and self-control through physics-inspired metaphors.

## Project Overview

Core model:

```text
Action = Motivation - Friction + Momentum
```

This is a visual metaphor, not a clinical or strict psychological law. The animation uses exponential decay, inertia, friction, potential wells, activation-energy barriers, momentum, and feedback loops to explain why motivation fades and why discipline works as a repeatable system.

## Folder Tree

```text
motivation/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── narration_script.md
├── manim_scenes/
│   ├── __init__.py
│   ├── common.py
│   ├── full_video.py
│   ├── scene_01_hook.py
│   ├── scene_02_motivation_decay.py
│   ├── scene_03_inertia.py
│   ├── scene_04_friction.py
│   ├── scene_05_energy_barrier.py
│   ├── scene_06_momentum.py
│   ├── scene_07_feedback_loop.py
│   └── scene_08_final_synthesis.py
├── utils/
│   ├── __init__.py
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

Manim also needs system dependencies such as Cairo, Pango, FFmpeg, and a LaTeX installation for `MathTex`.

This workspace includes a small local `manim_data_structures` compatibility shim. The installed `manim-data-structures==0.1.4` package can fail during Manim 0.20.x plugin discovery on Python 3.12, and this project does not use that plugin. Remove the shim if your upstream plugin is updated and imports cleanly.

## Quick Preview

Preview the hook scene:

```bash
python main.py --scene 01 --quality pql
```

Preview the complete video at lower quality:

```bash
python main.py --scene full --quality pql
```

## Individual Scene Commands

```bash
manim -pql manim_scenes/scene_01_hook.py Scene01Hook
manim -pql manim_scenes/scene_02_motivation_decay.py Scene02MotivationDecay
manim -pql manim_scenes/scene_03_inertia.py Scene03Inertia
manim -pql manim_scenes/scene_04_friction.py Scene04Friction
manim -pql manim_scenes/scene_05_energy_barrier.py Scene05EnergyBarrier
manim -pql manim_scenes/scene_06_momentum.py Scene06Momentum
manim -pql manim_scenes/scene_07_feedback_loop.py Scene07FeedbackLoop
manim -pql manim_scenes/scene_08_final_synthesis.py Scene08FinalSynthesis
```

## Final Render

Target final render:

```bash
manim -pqh manim_scenes/full_video.py FullVideo
```

1080p final render:

```bash
manim -p --quality h manim_scenes/full_video.py FullVideo
```

## Files

`config.py` defines the palette, 16:9 frame, and reusable visual constants.

`manim_scenes/common.py` contains reusable Manim primitives: glowing text, force arrows, rolling balls, graph axes, glowing curves, particles, title cards, labels, and loop arrows.

`utils/math_utils.py` contains motivation decay, logistic habit momentum, feedback updates, normalized curves, and potential-energy barrier functions.

`utils/physics_models.py` contains small force, friction, impulse, rolling, and energy-barrier helper models.

`narration_script.md` contains the scientific concept summary, full timestamped narration, scene plan, and YouTube upload package.
