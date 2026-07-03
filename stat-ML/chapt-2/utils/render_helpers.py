"""Render command helpers for the Chapter 2 Manim project."""

from __future__ import annotations

SCENE_REGISTRY = {
    "01": ("manim_scenes/scene_01_world_dataset.py", "Scene01WorldDataset"),
    "02": ("manim_scenes/scene_02_population.py", "Scene02Population"),
    "03": ("manim_scenes/scene_03_sample.py", "Scene03Sample"),
    "04": ("manim_scenes/scene_04_data_process.py", "Scene04DataProcess"),
    "05": ("manim_scenes/scene_05_representative_bias.py", "Scene05RepresentativeBias"),
    "06": ("manim_scenes/scene_06_self_driving_shift.py", "Scene06SelfDrivingShift"),
    "07": ("manim_scenes/scene_07_train_validation_test.py", "Scene07TrainValidationTest"),
    "08": ("manim_scenes/scene_08_iid.py", "Scene08IID"),
    "09": ("manim_scenes/scene_09_distribution_shift.py", "Scene09DistributionShift"),
    "10": ("manim_scenes/scene_10_final_question.py", "Scene10FinalQuestion"),
    "11": ("manim_scenes/scene_11_subscribe.py", "Scene11Subscribe"),
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
