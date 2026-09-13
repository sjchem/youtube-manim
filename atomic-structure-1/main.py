"""Command-line entry point for *How We Discovered What an Atom Looks Like* (Part 1).

Examples:
    python main.py list
    python main.py preview scene_08
    python main.py scene 08
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
    "scene_01": ("manim_scenes.scene_01_impossible_atom", "Scene01ImpossibleAtom", 'The impossible atom: mystery and promise'),
    "scene_02": ("manim_scenes.scene_02_seeing_the_invisible", "Scene02SeeingTheInvisible", 'Seeing the invisible'),
    "scene_03": ("manim_scenes.scene_03_dalton_sphere", "Scene03DaltonSphere", 'Dalton: a useful starting point'),
    "scene_04": ("manim_scenes.scene_04_cathode_rays", "Scene04CathodeRays", 'The electron: something smaller'),
    "scene_05": ("manim_scenes.scene_05_thomson_prediction", "Scene05ThomsonPrediction", 'Thomson: model and prediction'),
    "scene_06": ("manim_scenes.scene_06_gold_foil", "Scene06GoldFoil", 'Gold foil: the one that came back'),
    "scene_07": ("manim_scenes.scene_07_empty_space", "Scene07EmptySpace", 'A cricket ball and five kilometres'),
    "scene_08": ("manim_scenes.scene_08_unstable_atom", "Scene08UnstableAtom", 'Why the classical atom collapses'),
    "scene_09": ("manim_scenes.scene_09_light_barcode", "Scene09LightBarcode", "Light: hydrogen's barcode"),
    "scene_10": ("manim_scenes.scene_10_energy_floors", "Scene10EnergyFloors", 'Bohr: energy has floors'),
    "scene_11": ("manim_scenes.scene_11_photon_ladder", "Scene11PhotonLadder", 'A jump becomes a colour'),
    "scene_12": ("manim_scenes.scene_12_what_bohr_got_right", "Scene12WhatBohrGotRight", 'What Bohr got right'),
    "scene_13": ("manim_scenes.scene_13_not_an_orbit", "Scene13NotAnOrbit", 'Why an orbit is not enough'),
    "scene_14": ("manim_scenes.scene_14_part_two", "Scene14PartTwo", 'Next video: beyond the orbit'),
    "scene_15": ("manim_scenes.scene_15_subscribe", "Scene_15_Subscribe", 'Subscribe: stay curious'),
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
    print("─" * 90)
    elapsed = 0.0
    for key, (_, class_name, title) in SCENE_MAP.items():
        number = key[-2:]
        duration = cfg.SCENE_DURATIONS[number]
        dimension = "3D" if number in cfg.THREE_D_SCENES else "  "
        start = f"{int(elapsed) // 60}:{int(elapsed) % 60:02d}"
        elapsed += duration
        print(f"{key:<10} {class_name:<26} {dimension}  {start:>6}  {duration:>5.0f}s  {title}")
    print("─" * 90)
    minutes, seconds = divmod(int(elapsed), 60)
    print(f"{'FullVideo':<10} {'':<26}          {elapsed:>5.0f}s  ({minutes}:{seconds:02d})\n")


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
