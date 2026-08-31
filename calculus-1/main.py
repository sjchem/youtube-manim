"""Command-line entry point for Visual Calculus Part 1: From Limits to Derivatives.

Examples:
    python main.py list
    python main.py preview scene_01
    python main.py scene scene_06
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
    "scene_01": ("manim_scenes.scene_01_moving_car", "Scene01MovingCar", "Motion hides a question"),
    "scene_02": ("manim_scenes.scene_02_limits", "Scene02Limits", "Getting infinitely close"),
    "scene_03": ("manim_scenes.scene_03_hole_in_graph", "Scene03HoleInGraph", "A hole in the graph"),
    "scene_04": ("manim_scenes.scene_04_continuity", "Scene04Continuity", "When the limit meets the function"),
    "scene_05": ("manim_scenes.scene_05_trig_limit", "Scene05TrigLimit", "A beautiful trigonometric limit"),
    "scene_06": ("manim_scenes.scene_06_secant_to_tangent", "Scene06SecantToTangent", "From secant to tangent"),
    "scene_07": ("manim_scenes.scene_07_local_linearity", "Scene07LocalLinearity", "The most powerful visual"),
    "scene_08": ("manim_scenes.scene_08_derivative_meaning", "Scene08DerivativeMeaning", "Derivative as instantaneous change"),
    "scene_09": ("manim_scenes.scene_09_subscribe", "Scene09Subscribe", "Subscribe card"),
}


def _resolve_scene(value: str) -> tuple[str, str, str] | None:
    normalized = value if value.startswith("scene_") else f"scene_{value[:2]}"
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
    print("─" * 72)
    for key, (_, class_name, title) in SCENE_MAP.items():
        duration = cfg.SCENE_DURATIONS[key[-2:]]
        print(f"{key:<12} {class_name:<26} {duration:>5.0f}s  {title}")
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 72)
    minutes, seconds = divmod(int(total), 60)
    print(f"FullVideo{'':<31} {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


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
