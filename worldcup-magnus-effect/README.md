# Why the World Cup Ball Curves in Mid-Air

Complete Manim project for a scientific YouTube animation about the Magnus effect, free kicks, and the 2026 Trionda World Cup ball.

The project is animation-first: top-view flight paths, spinning ball diagrams, airflow lines, wake deflection, force vectors, a light trajectory model, and a compact Trionda design segment.

## Project Structure

```text
worldcup-magnus-effect/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── narration_script.md
├── concept_summary.md
├── animation_plan.md
├── youtube_package.md
├── manim_scenes/
├── utils/
├── assets/
├── image/
├── media/
├── output/
└── themes/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If Manim is already installed in the repo environment, you can skip the virtual environment step.

## List Scenes

```bash
python main.py list
```

## Narration Timing

The full video pads each scene to match the timestamped narration windows:

| Scene | Duration |
| --- | ---: |
| 01 - The Illusion | 45s |
| 02 - Off-Center Kick | 45s |
| 03 - Airflow and Spin | 50s |
| 04 - Magnus Force | 50s |
| 05 - Curve Builder | 55s |
| 06 - Surface Matters | 50s |
| 07 - Trionda Design Lab | 55s |
| 08 - Final Synthesis | 60s |
| 09 - Subscribe | 10s |

## Preview One Scene

```bash
python main.py preview 01 --quality preview
python main.py preview 05 --quality preview
```

## Render Individual Scenes

```bash
python main.py render 01 --quality high
python main.py render 07 --quality high
```

Direct Manim preview commands for each scene:

```bash
manim -pqh manim_scenes/scene_01_hook.py Scene01Hook
manim -pqh manim_scenes/scene_02_off_center_kick.py Scene02OffCenterKick
manim -pqh manim_scenes/scene_03_airflow_spin.py Scene03AirflowSpin
manim -pqh manim_scenes/scene_04_magnus_force.py Scene04MagnusForce
manim -pqh manim_scenes/scene_05_curve_simulation.py Scene05CurveSimulation
manim -pqh manim_scenes/scene_06_surface_matters.py Scene06SurfaceMatters
manim -pqh manim_scenes/scene_07_trionda_design.py Scene07TriondaDesign
manim -pqh manim_scenes/scene_08_final_synthesis.py Scene08FinalSynthesis
manim -pqh manim_scenes/scene_09_subscribe.py Scene09Subscribe
```

## Render the Full Video

```bash
python main.py full --quality high
```

Direct Manim 1080p render:

```bash
manim -qh manim_scenes/full_video.py FullVideo
```

## Validation

```bash
python -m compileall .
python main.py list
```

## Assets

The supplied image in `image/` is used as an optional visual reference in Scene 06. The loader prefers a compatible PNG if present, then falls back to AVIF. If the local image stack cannot decode either image, the scene automatically falls back to a vector ball-history montage.

The animation does not depend on generated media files.

## Scientific Scope

The trajectory model in `utils/physics_models.py` is a lightweight educational model. It gives the correct causal structure and force directions, but it is not a CFD solver or a match-grade prediction of any specific kick.

The Trionda segment uses published reporting and wind-tunnel work as context. It does not claim that every 2026 shot will behave the same way; real flight depends on speed, spin, ball orientation, humidity, altitude, temperature, and strike technique.

## References

- FIFA history of World Cup match balls: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/ball-balls-history
- Scientific American on Trionda geometry and design: https://www.scientificamerican.com/article/the-surprising-math-and-physics-behind-the-2026-trionda-world-cup-soccer-ball/
- MIT News on soccer-ball swerve and surface roughness: https://news.mit.edu/2014/explained-how-does-soccer-ball-swerve-0617
- Goff, Hong, Liu, and Asai, 2026, Trionda wind-tunnel characterization: https://www.mdpi.com/2076-3417/16/6/2808
- WIRED overview of Trionda aerodynamics research: https://www.wired.com/story/the-world-cups-trionda-ball-challenges-traditional-aerodynamics/
