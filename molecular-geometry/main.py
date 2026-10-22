"""Command-line entry point for 'Molecular Geometry, Explained Visually'.

Examples:
    python main.py list                 # chapter list with timestamps
    python main.py preview 07           # fast 480p15 preview of one chapter
    python main.py scene 07             # one chapter at full quality (1080p30)
    python main.py preview all          # every chapter as separate previews
    python main.py preview full         # the whole film at preview quality
    python main.py render               # the whole film at 1080p30
    python main.py check                # models + data + narration + timing + layout audits
    python main.py audio-check          # recorded narration clips vs chapter lengths
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
    "scene_01": ("manim_scenes.scene_01_shape_mystery", "Scene01ShapeMystery", "CO2 vs H2O: flat Lewis to 3D (3D)"),
    "scene_02": ("manim_scenes.scene_02_lewis_is_flat", "Scene02LewisIsFlat", "Methane: flat cross to tetrahedron (3D)"),
    "scene_03": ("manim_scenes.scene_03_regions_repel", "Scene03RegionsRepel", "Repulsion finds 2, 3, 4 arrangements (3D)"),
    "scene_04": ("manim_scenes.scene_04_counting_regions", "Scene04CountingRegions", "Counting rules, AXmEn, steric number"),
    "scene_05": ("manim_scenes.scene_05_linear_planar", "Scene05LinearPlanar", "CO2 linear, BF3 trigonal planar (3D)"),
    "scene_06": ("manim_scenes.scene_06_tetrahedron", "Scene06Tetrahedron", "Square to tetrahedron; the cube (3D)"),
    "scene_07": ("manim_scenes.scene_07_ammonia", "Scene07Ammonia", "One lone pair: NH3, two geometries (3D)"),
    "scene_08": ("manim_scenes.scene_08_water", "Scene08Water", "Two lone pairs: H2O; the trend (3D)"),
    "scene_09": ("manim_scenes.scene_09_five_regions", "Scene09FiveRegions", "Trigonal bipyramid, PCl5 (3D)"),
    "scene_10": ("manim_scenes.scene_10_tbp_family", "Scene10TbpFamily", "PCl5 > SF4 > ClF3 > XeF2 (3D)"),
    "scene_11": ("manim_scenes.scene_11_six_regions", "Scene11SixRegions", "Octahedron, SF6 (3D)"),
    "scene_12": ("manim_scenes.scene_12_flat_from_six", "Scene12FlatFromSix", "SF6 > BrF5 > XeF4 (3D)"),
    "scene_13": ("manim_scenes.scene_13_mixing_orbitals", "Scene13MixingOrbitals", "s and p; the s-p dial; sp (3D)"),
    "scene_14": ("manim_scenes.scene_14_sp2_sp3", "Scene14Sp2Sp3", "sp2, sp3, cos = -1/n (3D)"),
    "scene_15": ("manim_scenes.scene_15_methane_ethene", "Scene15MethaneEthene", "CH4 sigma overlaps; ethene sigma + pi (3D)"),
    "scene_16": ("manim_scenes.scene_16_two_models", "Scene16TwoModels", "VSEPR vs hybridization; sp3d labels"),
    "scene_17": ("manim_scenes.scene_17_bond_dipoles", "Scene17BondDipoles", "HCl, CO2 cancels, H2O does not (3D)"),
    "scene_18": ("manim_scenes.scene_18_symmetry_polarity", "Scene18SymmetryPolarity", "3D vector sums: BF3, CH4, NH3 (3D)"),
    "scene_19": ("manim_scenes.scene_19_predict", "Scene19Predict", "Challenges: SO2, PF3, BrF3 (3D)"),
    "scene_20": ("manim_scenes.scene_20_big_picture", "Scene20BigPicture", "Synthesis: molecules live in 3D (3D)"),
    "scene_21": ("manim_scenes.scene_21_oxygen_magnet", "Scene21OxygenMagnet", "Teaser: why is O2 magnetic?"),
    "scene_22": ("manim_scenes.scene_22_subscribe", "Scene22Subscribe", "Subscribe card"),
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
        sys.executable, "-m", "manim", f"-q{quality}",
        "--fps", str(cfg.RENDER["preview_fps"] if preview else cfg.RENDER["fps"]),
        "-r", str(cfg.RENDER["preview_resolution"] if preview else cfg.RENDER["resolution"]),
        f"{module.replace('.', '/')}.py", class_name,
    ]
    print("▶", " ".join(cmd))
    return subprocess.run(cmd, cwd=PROJECT_ROOT, check=False).returncode


def list_scenes() -> None:
    print(f"\n{cfg.PROJECT_TITLE} — {cfg.PROJECT_PART}")
    print("─" * 100)
    elapsed = 0
    for key, (_, class_name, title) in SCENE_MAP.items():
        duration = cfg.SCENE_DURATIONS[key[-2:]]
        start = f"{elapsed // 60:02d}:{elapsed % 60:02d}"
        print(f"{key:<10} {start:>6}  {class_name:<26} {duration:>5.0f}s  {title}")
        elapsed += int(duration)
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 100)
    minutes, seconds = divmod(int(total), 60)
    print(f"{'FullVideo':<10} {'':>6}  {'FullVideo':<26} {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


def run_checks() -> int:
    steps = [
        ["-m", "utils.math_utils"],
        ["-m", "utils.physics_models"],
        ["-m", "utils.orbital_models"],
        ["-m", "utils.molecule_library"],
        ["-m", "utils.geometry_data"],
        ["-m", "utils.narration_audit"],
        ["-m", "utils.timing_audit"],
        ["-m", "utils.timing_audit", "--fps", "30"],
        ["-m", "utils.timing_audit", "--full"],
        ["-m", "utils.layout_audit", "--motion"],
    ]
    for step in steps:
        print("▶ python", " ".join(step), flush=True)
        code = subprocess.run([sys.executable, *step], cwd=PROJECT_ROOT, check=False).returncode
        if code:
            return code
    return 0


def main() -> int:
    args = sys.argv[1:]
    command = args[0] if args else "list"
    if command in {"list", "ls"}:
        list_scenes()
        return 0
    if command == "check":
        return run_checks()
    if command == "audio-check":
        from utils.voiceover import main as audit_audio

        return audit_audio()
    if command == "render":
        return _run_manim("manim_scenes.full_video", "FullVideo", str(cfg.RENDER["youtube_quality"]))
    if command in {"preview", "scene"}:
        if len(args) < 2:
            print(f"Usage: python main.py {command} <scene number or name | all | full>")
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
