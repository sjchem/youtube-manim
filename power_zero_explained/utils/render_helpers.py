"""Command helpers for rendering the project with Manim."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCENE_REGISTRY: dict[str, tuple[str, str]] = {
    "hook": ("manim_scenes/scene_01_hook.py", "HookStrangeRule"),
    "scene_01": ("manim_scenes/scene_01_hook.py", "HookStrangeRule"),
    "ladder": ("manim_scenes/scene_02_power_ladder.py", "PowerLadderScene"),
    "scene_02": ("manim_scenes/scene_02_power_ladder.py", "PowerLadderScene"),
    "law": ("manim_scenes/scene_03_exponent_law.py", "ExponentLawScene"),
    "scene_03": ("manim_scenes/scene_03_exponent_law.py", "ExponentLawScene"),
    "empty": ("manim_scenes/scene_04_empty_product.py", "EmptyProductScene"),
    "scene_04": ("manim_scenes/scene_04_empty_product.py", "EmptyProductScene"),
    "graph": ("manim_scenes/scene_05_graph_view.py", "GraphViewScene"),
    "scene_05": ("manim_scenes/scene_05_graph_view.py", "GraphViewScene"),
    "summary": ("manim_scenes/scene_06_final_summary.py", "FinalSummaryScene"),
    "scene_06": ("manim_scenes/scene_06_final_summary.py", "FinalSummaryScene"),
    "full": ("manim_scenes/full_video.py", "FullVideo"),
}

QUALITY_FLAGS = {
    "l": "-ql",
    "m": "-qm",
    "h": "-qh",
    "p": "-qp",
    "k": "-qk",
}


def scene_choices() -> list[str]:
    """Return stable scene aliases for the CLI."""

    return sorted(SCENE_REGISTRY)


def get_scene_entry(scene_name: str) -> tuple[Path, str]:
    """Resolve a scene alias into a Manim file path and class name."""

    key = scene_name.strip().lower()
    if key not in SCENE_REGISTRY:
        choices = ", ".join(scene_choices())
        raise KeyError(f"Unknown scene '{scene_name}'. Choices: {choices}")

    relative_path, class_name = SCENE_REGISTRY[key]
    return PROJECT_ROOT / relative_path, class_name


def build_manim_command(
    scene_name: str,
    quality: str = "l",
    preview: bool = False,
    fps: int | None = None,
    output_file: str | None = None,
) -> list[str]:
    """Build a subprocess-safe command for Manim."""

    scene_path, class_name = get_scene_entry(scene_name)
    quality_flag = QUALITY_FLAGS.get(quality, "-ql")
    command = ["python", "-m", "manim", quality_flag, str(scene_path), class_name]

    if preview:
        command.append("-p")
    if fps is not None:
        command.extend(["--fps", str(fps)])
    if output_file:
        command.extend(["-o", output_file])

    return command
