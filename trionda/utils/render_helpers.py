"""Render command helpers for this Manim project."""

from __future__ import annotations

SCENE_REGISTRY = {
    "01": ("manim_scenes/scene_01_cutaway.py", "Scene01CutawayHook"),
    "02": ("manim_scenes/scene_02_material_layers.py", "Scene02MaterialLayers"),
    "03": ("manim_scenes/scene_03_thermal_bonding.py", "Scene03ThermalBonding"),
    "04": ("manim_scenes/scene_04_panel_geometry.py", "Scene04PanelGeometry"),
    "05": ("manim_scenes/scene_05_boundary_layer.py", "Scene05BoundaryLayer"),
    "06": ("manim_scenes/scene_06_drag_crisis.py", "Scene06DragCrisis"),
    "07": ("manim_scenes/scene_07_sensor_inside.py", "Scene07SensorInside"),
    "08": ("manim_scenes/scene_08_ai_var.py", "Scene08AIVAR"),
    "09": ("manim_scenes/scene_09_subscribe.py", "Scene09Subscribe"),
    "full": ("manim_scenes/full_video.py", "FullVideo"),
}

SCENE_CLASSES = [value[1] for key, value in SCENE_REGISTRY.items() if key != "full"]

QUALITY_PRESETS = {
    "preview": "-ql",
    "medium": "-qm",
    "high": "-qh",
    "production": "-qh",
}


def render_command(scene_key: str, quality: str = "preview", preview: bool = False) -> list[str]:
    """Build a Manim CLI command."""

    if scene_key not in SCENE_REGISTRY:
        raise KeyError(f"Unknown scene key: {scene_key}")
    scene_file, scene_class = SCENE_REGISTRY[scene_key]
    quality_flag = QUALITY_PRESETS.get(quality, quality if quality.startswith("-") else f"-{quality}")
    cmd = ["manim", quality_flag, scene_file, scene_class]
    if preview:
        cmd.insert(1, "-p")
    return cmd


def list_scenes() -> list[tuple[str, str, str]]:
    """Return scene registry rows."""

    return [(key, value[0], value[1]) for key, value in SCENE_REGISTRY.items()]


def full_video_command(quality: str = "preview") -> list[str]:
    """Return the full-video Manim command."""

    return render_command("full", quality=quality)
