"""Convenience entry point for previewing and rendering the project."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from utils.render_helpers import SCENE_CLASSES, full_video_command

SCENE_MODULES = {
    "Scene01Hook": "scene_01",
    "Scene02ReverseMultiplication": "scene_02",
    "Scene03ZeroCollapse": "scene_03",
    "Scene04NoSolution": "scene_04",
    "Scene05LimitsNotInfinity": "scene_05",
    "Scene06ZeroOverZero": "scene_06",
    "Scene07Computers": "scene_07",
    "Scene08FinalSummary": "scene_08",
}


def run_command(command: list[str]) -> int:
    print(" ".join(command))
    return subprocess.call(command)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render helpers for the division-by-zero Manim project.")
    parser.add_argument("--list", action="store_true", help="List available scenes.")
    parser.add_argument("--scene", default="Scene01Hook", choices=SCENE_CLASSES, help="Scene to render.")
    parser.add_argument("--quality", default="pql", help="Manim quality flag, for example pql or pqh.")
    parser.add_argument("--full", action="store_true", help="Render FullVideo instead of an individual scene.")
    parser.add_argument("--dry-run", action="store_true", help="Print the command without running it.")
    args = parser.parse_args()

    if args.list:
        print("\n".join(SCENE_CLASSES))
        quality = args.quality if args.quality.startswith("-") else f"-{args.quality}"
        print(f"\nFull video: {full_video_command(quality)}")
        return 0

    quality = args.quality if args.quality.startswith("-") else f"-{args.quality}"
    if args.full:
        command = ["manim", quality, "manim_scenes/full_video.py", "FullVideo"]
    else:
        module = SCENE_MODULES[args.scene]
        path = Path("manim_scenes") / f"{module}.py"
        command = ["manim", quality, str(path), args.scene]

    if args.dry_run:
        print(" ".join(command))
        return 0
    return run_command(command)


if __name__ == "__main__":
    raise SystemExit(main())
