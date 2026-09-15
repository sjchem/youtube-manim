"""Command-line entry point for *Why Electrons Don't Orbit the Nucleus* (Part 2).

Examples:
    python main.py list
    python main.py preview 09
    python main.py scene 09
    python main.py render
    python main.py review 09
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg  # noqa: E402

CLASS_NAMES = (
    "Scene01WhereIsIt",
    "Scene02WhatSurvives",
    "Scene03BohrNumbers",
    "Scene04MatterWaves",
    "Scene05OneAtATime",
    "Scene06WavesThatFit",
    "Scene07Uncertainty",
    "Scene08AllowedStates",
    "Scene09BornProbability",
    "Scene10OrbitToOrbital",
    "Scene11OrbitalShapes",
    "Scene12QuantumAddress",
    "Scene13EnergyLandscape",
    "Scene14BuildingAtoms",
    "Scene15FillingP",
    "Scene16Chemistry",
    "Scene17Potassium",
    "Scene18Answer",
    "Scene19Subscribe",
)

SCENE_MAP: dict[str, tuple[str, str, str]] = {
    key: (f"manim_scenes.scene_{key}_{slug}", class_name, title)
    for (key, slug, title, _), class_name in zip(cfg.SCENES, CLASS_NAMES)
}


def list_scenes() -> None:
    print(f"\n{cfg.PROJECT_TITLE} — {cfg.PROJECT_PART}")
    print("─" * 92)
    elapsed = 0
    for key, _, title, seconds in cfg.SCENES:
        _, class_name, _ = SCENE_MAP[key]
        dimension = "3D" if key in cfg.THREE_D_SCENES else "  "
        start = f"{elapsed // 60}:{elapsed % 60:02d}"
        elapsed += seconds
        print(f"{key}  {class_name:<24} {dimension}  {start:>6}  {seconds:>4}s  {title}")
    print("─" * 92)
    minutes, seconds = divmod(elapsed, 60)
    print(f"{'FullVideo':<28}          {elapsed:>10}s  ({minutes}:{seconds:02d})\n")


def _run_manim(module: str, class_name: str, command: str) -> int:
    low = command in {"preview", "review"}
    quality = cfg.RENDER["preview_quality"] if low else cfg.RENDER["youtube_quality"]
    fps = cfg.RENDER["preview_fps"] if low else cfg.RENDER["fps"]

    environment = os.environ.copy()
    if command == "review":
        # Review mode compresses every narration window. It is for inspecting
        # motion, never for synchronising against a recorded voice.
        environment["ATOM_REVIEW_SPEED"] = "16"
        fps = 8

    argv = [sys.executable, "-m", "manim", f"-q{quality}", "--fps", str(fps), "--progress_bar", "none"]
    if not low:
        argv += ["-r", str(cfg.RENDER["resolution"])]
    if command == "review":
        argv += ["--media_dir", "media/review"]
    argv += [f"{module.replace('.', '/')}.py", class_name]

    print("▶", " ".join(argv))
    return subprocess.run(argv, cwd=PROJECT_ROOT, env=environment, check=False).returncode


def main() -> int:
    args = sys.argv[1:]
    command = args[0] if args else "list"
    if command == "list":
        list_scenes()
        return 0
    if command not in {"preview", "scene", "render", "review"}:
        print("Usage: python main.py list | preview NN | scene NN | render | review [NN]")
        return 2

    key = args[1].zfill(2) if len(args) > 1 else None
    if key is not None and key not in SCENE_MAP:
        print(f"Unknown scene: {args[1]}")
        list_scenes()
        return 2
    if key is None:
        module, class_name = "manim_scenes.full_video", "FullVideo"
    else:
        module, class_name, _ = SCENE_MAP[key]
    return _run_manim(module, class_name, command)


if __name__ == "__main__":
    raise SystemExit(main())
