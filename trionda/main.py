"""Convenience CLI for listing, previewing, and rendering scenes."""

from __future__ import annotations

import argparse
import subprocess

from utils.render_helpers import SCENE_CLASSES, SCENE_REGISTRY, full_video_command, list_scenes, render_command


def run_command(command: list[str]) -> int:
    print(" ".join(command))
    return subprocess.call(command)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render helpers for the Trionda Manim project.")
    parser.add_argument("--list", action="store_true", help="List available scenes.")
    parser.add_argument("--scene", default="01", help="Scene key or class name to render.")
    parser.add_argument("--quality", default="preview", help="preview, medium, high, production, or a Manim flag.")
    parser.add_argument("--full", action="store_true", help="Render the full combined video.")
    parser.add_argument("--preview", action="store_true", help="Open Manim preview after rendering.")
    parser.add_argument("--dry-run", action="store_true", help="Print the command without running it.")
    args = parser.parse_args()

    if args.list:
        for key, path, cls in list_scenes():
            print(f"{key:>4}  {cls:<26}  {path}")
        return 0

    if args.full:
        command = full_video_command(args.quality)
    else:
        scene_key = args.scene
        if scene_key not in SCENE_REGISTRY:
            matches = [key for key, value in SCENE_REGISTRY.items() if value[1] == scene_key]
            if not matches:
                valid = ", ".join([*SCENE_REGISTRY.keys(), *SCENE_CLASSES])
                raise SystemExit(f"Unknown scene '{scene_key}'. Valid options: {valid}")
            scene_key = matches[0]
        command = render_command(scene_key, quality=args.quality, preview=args.preview)

    if args.dry_run:
        print(" ".join(command))
        return 0
    return run_command(command)


if __name__ == "__main__":
    raise SystemExit(main())
