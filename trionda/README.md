# The Secret Material Inside the 2026 World Cup Ball

A complete Manim Community Edition project about the science of the FIFA World Cup 26 TRIONDA ball: engineered surface layers, thermally bonded seams, controlled aerodynamic roughness, drag crisis behavior, and connected-ball sensor data.

## Setup

```bash
cd /home/santanu/code/sjchem/youtube-manim/trionda
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The project imports the local Oceanic theme from `../themes`, so render commands should be run from this folder.

## List Scenes

```bash
python main.py --list
```

## Preview One Scene

```bash
python main.py --scene 01 --quality preview
python main.py --scene Scene06DragCrisis --quality preview
```

Add `--preview` to open the rendered preview automatically:

```bash
python main.py --scene 05 --quality preview --preview
```

## Render Individual Scenes

```bash
manim -ql manim_scenes/scene_01_cutaway.py Scene01CutawayHook
manim -ql manim_scenes/scene_02_material_layers.py Scene02MaterialLayers
manim -ql manim_scenes/scene_03_thermal_bonding.py Scene03ThermalBonding
manim -ql manim_scenes/scene_04_panel_geometry.py Scene04PanelGeometry
manim -ql manim_scenes/scene_05_boundary_layer.py Scene05BoundaryLayer
manim -ql manim_scenes/scene_06_drag_crisis.py Scene06DragCrisis
manim -ql manim_scenes/scene_07_sensor_inside.py Scene07SensorInside
manim -ql manim_scenes/scene_08_ai_var.py Scene08AIVAR
manim -ql manim_scenes/scene_09_subscribe.py Scene09Subscribe
```

## Render Full Video

Preview:

```bash
python main.py --full --quality preview
```

Final 1080p render:

```bash
python main.py --full --quality high
```

Equivalent direct command:

```bash
manim -qh manim_scenes/full_video.py FullVideo
```

## Project Files

- `concept_summary.md`: scientific summary and guardrails.
- `animation_plan.md`: scene-by-scene visual plan.
- `narration_script.md`: timestamped narration.
- `youtube_package.md`: titles, description, tags, thumbnail ideas, pinned comment, and social post.
- `manim_scenes/`: complete scene code and combined full video.
- `utils/`: math, physics, and render helper utilities.

## References

- Scientific American, "The Surprising Math and Physics behind the 2026 World Cup Soccer Ball"
- FIFA, official TRIONDA launch release
- adidas, official TRIONDA technology release
- FIFA, Connected Ball Technology
- Goff et al. 2026, "Trionda: Enhanced Surface Roughness Relative to Previous FIFA World Cup Match Balls"
