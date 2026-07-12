"""Command helpers for rendering the Chapter 4 Manim scenes."""

from __future__ import annotations

from pathlib import Path


SCENES: dict[str, tuple[str, str]] = {
    "01": ("manim_scenes/scene_01_uncertainty.py", "Scene01Uncertainty"),
    "02": ("manim_scenes/scene_02_probability_scale.py", "Scene02ProbabilityScale"),
    "03": ("manim_scenes/scene_03_random_variables.py", "Scene03RandomVariables"),
    "04": ("manim_scenes/scene_04_conditional_probability.py", "Scene04ConditionalProbability"),
    "05": ("manim_scenes/scene_05_independence.py", "Scene05Independence"),
    "06": ("manim_scenes/scene_06_joint_marginal.py", "Scene06JointMarginal"),
    "07": ("manim_scenes/scene_07_bayes_theorem.py", "Scene07BayesTheorem"),
    "08": ("manim_scenes/scene_08_ml_connections.py", "Scene08MLConnections"),
    "09": ("manim_scenes/scene_09_synthesis.py", "Scene09Synthesis"),
    "10": ("manim_scenes/scene_10_subscribe.py", "Scene10Subscribe"),
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
