"""Render command helpers for Manim."""

from __future__ import annotations

SCENE_REGISTRY = {
    "01": ("manim_scenes/scene_01.py", "Scene01ColdOpen"),
    "02": ("manim_scenes/scene_02.py", "Scene02MultiplicationAsMotion"),
    "03": ("manim_scenes/scene_03.py", "Scene03NegativeAsReversal"),
    "04": ("manim_scenes/scene_04.py", "Scene04MirrorRoom"),
    "05": ("manim_scenes/scene_05.py", "Scene05PatternThroughZero"),
    "06": ("manim_scenes/scene_06.py", "Scene06DistributiveLawMachine"),
    "07": ("manim_scenes/scene_07.py", "Scene07BrokenUniverse"),
    "08": ("manim_scenes/scene_08.py", "Scene08FinalSynthesis"),
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


def output_name(scene_key: str, ext: str = "mp4") -> str:
    """Return a stable output filename."""
    _, scene_class = SCENE_REGISTRY[scene_key]
    return f"{scene_class}.{ext}"


def list_scenes() -> list[tuple[str, str, str]]:
    """Return scene registry rows as key, file, class."""
    return [(key, value[0], value[1]) for key, value in SCENE_REGISTRY.items()]
