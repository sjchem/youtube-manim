"""Command-line entry point for Visual Calculus Part 3: From Integrals to Differential Equations.

Examples:
    python main.py list
    python main.py preview scene_04
    python main.py scene scene_11
    python main.py render
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent
for _path in (str(PROJECT_ROOT), str(REPO_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import config as cfg  # noqa: E402

SCENE_MAP: dict[str, tuple[str, str, str]] = {
    "scene_01": ("manim_scenes.scene_01_reverse_problem", "Scene01ReverseProblem", "The reverse problem"),
    "scene_02": ("manim_scenes.scene_02_missing_constant", "Scene02MissingConstant", "The information a derivative throws away"),
    "scene_03": ("manim_scenes.scene_03_equation_of_change", "Scene03EquationOfChange", "An equation about change itself"),
    "scene_04": ("manim_scenes.scene_04_slope_field", "Scene04SlopeField", "The slope field, and curves that flow"),
    "scene_05": ("manim_scenes.scene_05_exponential_growth", "Scene05ExponentialGrowth", "Growth proportional to size"),
    "scene_06": ("manim_scenes.scene_06_exponential_decay", "Scene06ExponentialDecay", "One sign flip, an opposite world"),
    "scene_07": ("manim_scenes.scene_07_newton_cooling", "Scene07NewtonCooling", "Newton's law of cooling"),
    "scene_08": ("manim_scenes.scene_08_separation_of_variables", "Scene08SeparationOfVariables", "Separating the variables"),
    "scene_09": ("manim_scenes.scene_09_initial_conditions", "Scene09InitialConditions", "Which universe are we in?"),
    "scene_10": ("manim_scenes.scene_10_spring_oscillation", "Scene10SpringOscillation", "F = ma, and a spring that oscillates"),
    "scene_11": ("manim_scenes.scene_11_area_to_volume", "Scene11AreaToVolume", "From area to volume, in 3D"),
    "scene_12": ("manim_scenes.scene_12_one_idea", "Scene12OneIdea", "Area, volume, mass, probability — one idea"),
    "scene_13": ("manim_scenes.scene_13_equation_to_future", "Scene13EquationToFuture", "From an equation to a future"),
    "scene_14": ("manim_scenes.scene_14_modern_science", "Scene14ModernScience", "The language of modern science and AI"),
    "scene_15": ("manim_scenes.scene_15_synthesis", "Scene15Synthesis", "The final revelation"),
    "scene_16": ("manim_scenes.scene_16_subscribe", "Scene16Subscribe", "Subscribe card"),
}


def _resolve_scene(value: str) -> tuple[str, str, str] | None:
    normalized = value if value.startswith("scene_") else f"scene_{int(value):02d}" if value.isdigit() else value
    for key, details in SCENE_MAP.items():
        if normalized == key or value.startswith(key):
            return details
    return None


def _run_manim(module: str, class_name: str, quality: str) -> int:
    cmd = [
        sys.executable,
        "-m",
        "manim",
        f"-q{quality}",
        "--fps",
        str(cfg.RENDER["fps"]),
        f"{module.replace('.', '/')}.py",
        class_name,
    ]
    print("▶", " ".join(cmd))
    return subprocess.run(cmd, cwd=PROJECT_ROOT, check=False).returncode


def list_scenes() -> None:
    print(f"\n{cfg.PROJECT_TITLE} — {cfg.PROJECT_PART}")
    print("─" * 82)
    for key, (_, class_name, title) in SCENE_MAP.items():
        number = key[-2:]
        duration = cfg.SCENE_DURATIONS[number]
        dimension = "3D" if number in cfg.THREE_D_SCENES else "  "
        print(f"{key:<10} {class_name:<28} {dimension}  {duration:>5.0f}s  {title}")
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 82)
    minutes, seconds = divmod(int(total), 60)
    print(f"{'FullVideo':<10} {'':<28}      {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


def main() -> int:
    args = sys.argv[1:]
    command = args[0] if args else "list"
    if command == "list":
        list_scenes()
        return 0
    if command == "render":
        return _run_manim("manim_scenes.full_video", "FullVideo", str(cfg.RENDER["youtube_quality"]))
    if command in {"preview", "scene"}:
        if len(args) < 2:
            print(f"Usage: python main.py {command} <scene number or name>")
            return 2
        scene = _resolve_scene(args[1])
        if scene is None:
            print(f"Unknown scene: {args[1]}")
            list_scenes()
            return 2
        module, class_name, _ = scene
        quality = cfg.RENDER["preview_quality"] if command == "preview" else cfg.RENDER["youtube_quality"]
        return _run_manim(module, class_name, str(quality))
    print(f"Unknown command: {command}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
