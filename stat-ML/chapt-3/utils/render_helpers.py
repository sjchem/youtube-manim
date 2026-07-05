"""Command helpers for rendering the Chapter 3 Manim scenes."""

from __future__ import annotations

from pathlib import Path


SCENES: dict[str, tuple[str, str]] = {
    "01": ("manim_scenes/scene_01_data_first_look.py", "Scene01DataFirstLook"),
    "02": ("manim_scenes/scene_02_center.py", "Scene02Center"),
    "03": ("manim_scenes/scene_03_outliers.py", "Scene03Outliers"),
    "04": ("manim_scenes/scene_04_spread.py", "Scene04Spread"),
    "05": ("manim_scenes/scene_05_percentiles.py", "Scene05Percentiles"),
    "06": ("manim_scenes/scene_06_scaling.py", "Scene06Scaling"),
    "07": ("manim_scenes/scene_07_covariance_correlation.py", "Scene07CovarianceCorrelation"),
    "08": ("manim_scenes/scene_08_worked_mean_variance.py", "Scene08WorkedMeanVariance"),
    "09": ("manim_scenes/scene_09_distribution_shape.py", "Scene09DistributionShape"),
    "10": ("manim_scenes/scene_10_correlation_example.py", "Scene10CorrelationExample"),
    "11": ("manim_scenes/scene_11_ml_checklist.py", "Scene11MLChecklist"),
    "12": ("manim_scenes/scene_12_subscribe.py", "Scene12Subscribe"),
    "full": ("manim_scenes/full_video.py", "FullVideo"),
}

QUALITY_PRESETS: dict[str, str] = {
    "preview": "-pql",
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
    "4k": "-qk",
}
QUALITY_FPS: dict[str, str] = {
    "preview": "15",
    "low": "15",
    "medium": "30",
    "high": "30",
    "4k": "30",
}


def list_scenes() -> list[tuple[str, str, str]]:
    """Return renderable scene metadata in display order."""
    return [(key, *SCENES[key]) for key in SCENES]


def resolve_scene(scene_key: str) -> tuple[str, str]:
    """Resolve aliases such as '1' into the scene file and class."""
    normalized = scene_key.lower().strip()
    if normalized.isdigit():
        normalized = normalized.zfill(2)
    if normalized not in SCENES:
        valid = ", ".join(SCENES)
        raise KeyError(f"Unknown scene '{scene_key}'. Valid scenes: {valid}")
    return SCENES[normalized]


def render_command(scene_key: str, quality: str = "preview", preview: bool = False) -> list[str]:
    """Build a Manim CLI command for one scene."""
    scene_file, scene_class = resolve_scene(scene_key)
    flag = QUALITY_PRESETS[quality]
    if preview and "p" not in flag:
        flag = "-p" + flag.lstrip("-")
    return ["manim", flag, str(Path(scene_file)), scene_class, "--fps", QUALITY_FPS[quality]]
