"""Command-line entry point for 'What Does a Function Actually Do?'.

Examples:
    python main.py list
    python main.py preview scene_05
    python main.py scene 7
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
    "scene_01": ("manim_scenes.scene_01_everyday_machines", "Scene01EverydayMachines", "The universal translator (3D)"),
    "scene_02": ("manim_scenes.scene_02_the_rule", "Scene02TheRule", "Input, rule, output"),
    "scene_03": ("manim_scenes.scene_03_one_output", "Scene03OneOutput", "Why one input gives one output"),
    "scene_04": ("manim_scenes.scene_04_domain_range", "Scene04DomainRange", "Domain and range"),
    "scene_05": ("manim_scenes.scene_05_machine_to_graph", "Scene05MachineToGraph", "How a function becomes a graph"),
    "scene_06": ("manim_scenes.scene_06_vertical_line_test", "Scene06VerticalLineTest", "The vertical line test"),
    "scene_07": ("manim_scenes.scene_07_transformations", "Scene07Transformations", "Change the rule, change the shape"),
    "scene_08": ("manim_scenes.scene_08_composition", "Scene08Composition", "Machines in a pipeline"),
    "scene_09": ("manim_scenes.scene_09_inverse", "Scene09Inverse", "Running the machine backward"),
    "scene_10": ("manim_scenes.scene_10_no_inverse", "Scene10NoInverse", "When there is no way back"),
    "scene_11": ("manim_scenes.scene_11_higher_dimensions", "Scene11HigherDimensions", "Two inputs, one output (3D)"),
    "scene_12": ("manim_scenes.scene_12_why_it_matters", "Scene12WhyItMatters", "Why functions matter"),
    "scene_13": ("manim_scenes.scene_13_finale", "Scene13Finale", "Input, rule, output"),
    "scene_14": ("manim_scenes.scene_14_subscribe", "Scene14Subscribe", "Subscribe card"),
}


def _resolve_scene(value: str) -> tuple[str, str, str] | None:
    if value.isdigit():
        value = f"scene_{int(value):02d}"
    normalized = value if value.startswith("scene_") else f"scene_{value[:2]}"
    for key, details in SCENE_MAP.items():
        if normalized == key or value.startswith(key):
            return details
    return None


def _run_manim(module: str, class_name: str, quality: str, *, preview: bool = False) -> int:
    cmd = [
        sys.executable,
        "-m",
        "manim",
        f"-q{quality}",
        "--fps",
        str(cfg.RENDER["preview_fps"] if preview else cfg.RENDER["fps"]),
        "-r",
        str(cfg.RENDER["preview_resolution"] if preview else cfg.RENDER["resolution"]),
        f"{module.replace('.', '/')}.py",
        class_name,
    ]
    print("▶", " ".join(cmd))
    return subprocess.run(cmd, cwd=PROJECT_ROOT, check=False).returncode


def list_scenes() -> None:
    print(f"\n{cfg.PROJECT_TITLE} — {cfg.SERIES_LABEL}")
    print("─" * 78)
    for key, (_, class_name, title) in SCENE_MAP.items():
        duration = cfg.SCENE_DURATIONS[key[-2:]]
        print(f"{key:<10} {class_name:<28} {duration:>5.0f}s  {title}")
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 78)
    minutes, seconds = divmod(int(total), 60)
    print(f"{'FullVideo':<10} {'FullVideo':<28} {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


def main() -> int:
    args = sys.argv[1:]
    command = args[0] if args else "list"
    if command in {"list", "ls"}:
        list_scenes()
        return 0
    if command == "render":
        return _run_manim("manim_scenes.full_video", "FullVideo", str(cfg.RENDER["youtube_quality"]))
    if command in {"preview", "scene"}:
        if len(args) < 2:
            print(f"Usage: python main.py {command} <scene number or name>")
            return 2
        preview = command == "preview"
        quality = str(cfg.RENDER["preview_quality"] if preview else cfg.RENDER["youtube_quality"])
        if args[1] == "all":
            for module, class_name, _ in SCENE_MAP.values():
                result = _run_manim(module, class_name, quality, preview=preview)
                if result:
                    return result
            return 0
        if args[1] == "full":
            return _run_manim("manim_scenes.full_video", "FullVideo", quality, preview=preview)
        scene = _resolve_scene(args[1])
        if scene is None:
            print(f"Unknown scene: {args[1]}")
            list_scenes()
            return 2
        module, class_name, _ = scene
        return _run_manim(module, class_name, quality, preview=preview)
    print(f"Unknown command: {command}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
