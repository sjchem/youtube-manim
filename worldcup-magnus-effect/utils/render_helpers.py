"""Render command helpers for the World Cup Magnus effect project."""

from __future__ import annotations

SCENE_REGISTRY = {
    "01": ("manim_scenes/scene_01_hook.py", "Scene01Hook"),
    "02": ("manim_scenes/scene_02_off_center_kick.py", "Scene02OffCenterKick"),
    "03": ("manim_scenes/scene_03_airflow_spin.py", "Scene03AirflowSpin"),
    "04": ("manim_scenes/scene_04_magnus_force.py", "Scene04MagnusForce"),
    "05": ("manim_scenes/scene_05_curve_simulation.py", "Scene05CurveSimulation"),
    "06": ("manim_scenes/scene_06_surface_matters.py", "Scene06SurfaceMatters"),
    "07": ("manim_scenes/scene_07_trionda_design.py", "Scene07TriondaDesign"),
    "08": ("manim_scenes/scene_08_final_synthesis.py", "Scene08FinalSynthesis"),
    "09": ("manim_scenes/scene_09_subscribe.py", "Scene09Subscribe"),
    "full": ("manim_scenes/full_video.py", "FullVideo"),
}

QUALITY_PRESETS = {
    "preview": "-ql",
    "medium": "-qm",
    "high": "-qh",
    "production": "-qk",
}


def render_command(scene_key: str, quality: str = "preview", preview: bool = False) -> list[str]:
    """Build a Manim CLI command as a list for subprocess."""
    if scene_key not in SCENE_REGISTRY:
        raise KeyError(f"Unknown scene key: {scene_key}")
    scene_file, scene_class = SCENE_REGISTRY[scene_key]
    cmd = ["manim", QUALITY_PRESETS[quality], scene_file, scene_class]
    if preview:
        cmd.insert(1, "-p")
    return cmd


def list_scenes() -> list[tuple[str, str, str]]:
    """Return scene registry rows as key, file, class."""
    return [(key, value[0], value[1]) for key, value in SCENE_REGISTRY.items()]
