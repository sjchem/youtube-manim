"""Command-line entry point for 'Molecular Orbital Theory, Explained Visually'.

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
    "scene_01": ("manim_scenes.scene_01_oxygen_mystery", "Scene01OxygenMystery", "Hook: Lewis O=O vs liquid O2 on a magnet"),
    "scene_02": ("manim_scenes.scene_02_two_pictures", "Scene02TwoPictures", "Valence bond vs molecular orbital (3D)"),
    "scene_03": ("manim_scenes.scene_03_waves", "Scene03Waves", "Interference; 1s profiles add or cancel"),
    "scene_04": ("manim_scenes.scene_04_lcao", "Scene04Lcao", "LCAO, psi^2, phase maps, N in -> N out"),
    "scene_05": ("manim_scenes.scene_05_bonding_antibonding", "Scene05BondingAntibonding", "sigma 1s and sigma* 1s surfaces (3D)"),
    "scene_06": ("manim_scenes.scene_06_two_energies", "Scene06TwoEnergies", "Level splitting; LCAO H2+ energy curves"),
    "scene_07": ("manim_scenes.scene_07_h2_plus", "Scene07H2Plus", "H2+: one electron, bond order 1/2"),
    "scene_08": ("manim_scenes.scene_08_hydrogen", "Scene08Hydrogen", "H2: Pauli pair, bond order 1"),
    "scene_09": ("manim_scenes.scene_09_helium", "Scene09Helium", "He2 bond order 0; He2+; line-up"),
    "scene_10": ("manim_scenes.scene_10_sigma_p", "Scene10SigmaP", "Head-on p: sigma 2p, sigma* 2p (3D)"),
    "scene_11": ("manim_scenes.scene_11_pi", "Scene11Pi", "Sideways p: degenerate pi and pi* (3D)"),
    "scene_12": ("manim_scenes.scene_12_build_diagram", "Scene12BuildDiagram", "Valence diagram; Aufbau, Pauli, Hund"),
    "scene_13": ("manim_scenes.scene_13_orderings", "Scene13Orderings", "Two orderings; s-p mixing crossing"),
    "scene_14": ("manim_scenes.scene_14_fill_nitrogen", "Scene14FillNitrogen", "N2: ten electrons, bond order 3"),
    "scene_15": ("manim_scenes.scene_15_nitrogen_bond", "Scene15NitrogenBond", "N2 sigma + 2 pi (3D); falls past magnet"),
    "scene_16": ("manim_scenes.scene_16_oxygen_reveal", "Scene16OxygenReveal", "Lewis dots fly into O2 MOs; pi* (3D)"),
    "scene_17": ("manim_scenes.scene_17_mystery_solved", "Scene17MysterySolved", "O2 bond order 2; O2 vs N2 pours"),
    "scene_18": ("manim_scenes.scene_18_remove_electron", "Scene18RemoveElectron", "O2+: bond order 2.5"),
    "scene_19": ("manim_scenes.scene_19_add_electrons", "Scene19AddElectrons", "O2-, O2 2-: bond lengths, magnetism"),
    "scene_20": ("manim_scenes.scene_20_boron_fluorine", "Scene20BoronFluorine", "B2 and F2; four-molecule line-up"),
    "scene_21": ("manim_scenes.scene_21_challenge", "Scene21Challenge", "Unlabelled diagram challenge: C2"),
    "scene_22": ("manim_scenes.scene_22_final", "Scene22Final", "Synthesis: from waves to chemistry (3D)"),
    "scene_23": ("manim_scenes.scene_23_subscribe", "Scene23Subscribe", "Subscribe card"),
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
        print(f"{key:<10} {start:>6}  {class_name:<28} {duration:>5.0f}s  {title}")
        elapsed += int(duration)
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 100)
    minutes, seconds = divmod(int(total), 60)
    print(f"{'FullVideo':<10} {'':>6}  {'FullVideo':<28} {total:>5.0f}s  ({minutes}:{seconds:02d})\n")


def run_checks() -> int:
    steps = [
        ["-m", "utils.math_utils"],
        ["-m", "utils.physics_models"],
        ["-m", "utils.orbital_models"],
        ["-m", "utils.mo_models"],
        ["-m", "utils.mo_data"],
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
