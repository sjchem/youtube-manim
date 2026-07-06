"""Command helpers for rendering this Manim project."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCENE_REGISTRY: dict[str, tuple[str, str]] = {
    "hook": ("manim_scenes/scene_01_hook.py", "Scene01Hook"),
    "scene_01": ("manim_scenes/scene_01_hook.py", "Scene01Hook"),
    "perfect": ("manim_scenes/scene_02_perfect_six.py", "Scene02PerfectSix"),
    "scene_02": ("manim_scenes/scene_02_perfect_six.py", "Scene02PerfectSix"),
    "hexagon": ("manim_scenes/scene_03_hexagon_order.py", "Scene03HexagonOrder"),
    "scene_03": ("manim_scenes/scene_03_hexagon_order.py", "Scene03HexagonOrder"),
    "prime": ("manim_scenes/scene_04_prime_outsider.py", "Scene04PrimeOutsider"),
    "scene_04": ("manim_scenes/scene_04_prime_outsider.py", "Scene04PrimeOutsider"),
    "heptagon": ("manim_scenes/scene_05_heptagon_impossibility.py", "Scene05HeptagonImpossibility"),
    "scene_05": ("manim_scenes/scene_05_heptagon_impossibility.py", "Scene05HeptagonImpossibility"),
    "decimal": ("manim_scenes/scene_06_decimal_cycle.py", "Scene06DecimalCycle"),
    "scene_06": ("manim_scenes/scene_06_decimal_cycle.py", "Scene06DecimalCycle"),
    "cyclic": ("manim_scenes/scene_07_cyclic_number.py", "Scene07CyclicNumber"),
    "scene_07": ("manim_scenes/scene_07_cyclic_number.py", "Scene07CyclicNumber"),
    "synthesis": ("manim_scenes/scene_08_synthesis.py", "Scene08Synthesis"),
    "scene_08": ("manim_scenes/scene_08_synthesis.py", "Scene08Synthesis"),
    "subscribe": ("manim_scenes/scene_09_subscribe.py", "Scene09Subscribe"),
    "scene_09": ("manim_scenes/scene_09_subscribe.py", "Scene09Subscribe"),
    "full": ("manim_scenes/full_video.py", "FullVideo"),
}

QUALITY_FLAGS = {"l": "-ql", "m": "-qm", "h": "-qh", "p": "-qp", "k": "-qk"}


def scene_choices() -> list[str]:
    """Return available scene aliases."""

    return sorted(SCENE_REGISTRY)


def get_scene_entry(scene_name: str) -> tuple[Path, str]:
    """Resolve a scene alias into a file path and class name."""

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
    """Build a subprocess-safe Manim command."""

    scene_path, class_name = get_scene_entry(scene_name)
    command = ["python", "-m", "manim", QUALITY_FLAGS.get(quality, "-ql"), str(scene_path), class_name]
    if preview:
        command.append("-p")
    if fps is not None:
        command.extend(["--fps", str(fps)])
    if output_file:
        command.extend(["-o", output_file])
    return command
