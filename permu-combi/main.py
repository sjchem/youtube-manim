"""Command-line entry point for 'Permutations & Combinations Explained Visually'.

Examples:
    python main.py list
    python main.py preview scene_04
    python main.py scene 6
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
    "scene_01": ("manim_scenes.scene_01_lock_paradox", "Scene01LockParadox", "The combination-lock paradox (3D)"),
    "scene_02": ("manim_scenes.scene_02_choices_multiply", "Scene02ChoicesMultiply", "Choices multiply"),
    "scene_03": ("manim_scenes.scene_03_factorial", "Scene03Factorial", "Factorials: the shrinking pool"),
    "scene_04": ("manim_scenes.scene_04_permutations", "Scene04Permutations", "Permutations on a podium (3D)"),
    "scene_05": ("manim_scenes.scene_05_order_matters", "Scene05OrderMatters", "Why order matters here"),
    "scene_06": ("manim_scenes.scene_06_block_gap", "Scene06BlockGap", "Restricted arrangements: block and gap methods"),
    "scene_07": ("manim_scenes.scene_07_combinations", "Scene07Combinations", "Combinations: dividing order away"),
    "scene_08": ("manim_scenes.scene_08_quiz", "Scene08Quiz", "Permutation or combination?"),
    "scene_09": ("manim_scenes.scene_09_alike_geometry", "Scene09AlikeGeometry", "Alike objects and geometrical counting"),
    "scene_10": ("manim_scenes.scene_10_symmetry", "Scene10Symmetry", "Choosing is also leaving behind"),
    "scene_11": ("manim_scenes.scene_11_poker", "Scene11Poker", "2,598,960 poker hands (3D)"),
    "scene_12": ("manim_scenes.scene_12_zero_factorial", "Scene12ZeroFactorial", "Why 0! = 1"),
    "scene_13": ("manim_scenes.scene_13_finale", "Scene13Finale", "One question, two answers"),
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
    print("─" * 82)
    elapsed = 0
    for key, (_, class_name, title) in SCENE_MAP.items():
        duration = cfg.SCENE_DURATIONS[key[-2:]]
        start = f"{elapsed // 60:02d}:{elapsed % 60:02d}"
        print(f"{key:<10} {start:>6}  {class_name:<24} {duration:>5.0f}s  {title}")
        elapsed += int(duration)
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 82)
    minutes, seconds = divmod(int(total), 60)
    print(f"{'FullVideo':<10} {'':>6}  {'FullVideo':<24} {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


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
