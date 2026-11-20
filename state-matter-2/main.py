"""Command-line entry point for "Beyond Ideal Gases"..

Examples:
    python main.py list                 # scene list with timestamps
    python main.py chapters             # the eleven YouTube chapter markers
    python main.py preview 13           # fast 480p15 preview of one scene
    python main.py scene 13             # one scene at full quality (1080p30)
    python main.py preview all          # every scene as separate previews
    python main.py preview full         # the whole film at preview quality
    python main.py render               # the whole film at 1080p30
    python main.py check                # model + spoken numbers + narration + timing + layout audits
    python main.py export               # narration scripts, ElevenLabs text and cue sheets
    python main.py audio-check          # recorded narration clips vs scene lengths
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
    "scene_01": ("manim_scenes.scene_01_hook", "Scene01Hook", "PV = nRT returns; squeezed CO₂ condenses in a 3D cylinder; title"),
    "scene_02": ("manim_scenes.scene_02_roadmap", "Scene02Roadmap", "Five-stop journey: speeds, assumptions, repairs, critical point, liquids"),
    "scene_03": ("manim_scenes.scene_03_collisions", "Scene03Collisions", "Two equal-speed molecules collide elastically: one faster, one slower"),
    "scene_04": ("manim_scenes.scene_04_one_speed", "Scene04OneSpeed", "2D hard disks from one speed: the spike relaxes to a steady distribution"),
    "scene_05": ("manim_scenes.scene_05_velocity_space", "Scene05VelocitySpace", "3D velocity cloud; a growing shell: 4πu² × fading cloud = Maxwell–Boltzmann"),
    "scene_06": ("manim_scenes.scene_06_three_speeds", "Scene06ThreeSpeeds", "N₂ at 300 K: u_mp 420, u_av 480, u_rms 520 m/s; 1 : 1.128 : 1.225"),
    "scene_07": ("manim_scenes.scene_07_hotter_lighter", "Scene07HotterLighter", "300 → 600 K: ×√2; N₂ vs Cl₂: u ∝ 1/√M"),
    "scene_08": ("manim_scenes.scene_08_kmt_rules", "Scene08KmtRules", "Six postulates of kinetic molecular theory, each shown on a 3D gas"),
    "scene_09": ("manim_scenes.scene_09_two_cracks", "Scene09TwoCracks", "Negligible volume and no attraction fail at high P and low T"),
    "scene_10": ("manim_scenes.scene_10_attraction", "Scene10Attraction", "Neighbours tug a wall-bound molecule back: P_real < P_ideal"),
    "scene_11": ("manim_scenes.scene_11_size", "Scene11Size", "Point gas vs hard spheres, squeezed: more wall hits, P_real > P_ideal"),
    "scene_12": ("manim_scenes.scene_12_tug_of_war", "Scene12TugOfWar", "Tug-of-war rope: attraction vs size across P and T; CH₄, 600 K, He; concept check"),
    "scene_13": ("manim_scenes.scene_13_pressure_correction", "Scene13PressureCorrection", "Nearby pairs ×4 when density doubles: an²/V²; a for He, CO₂, NH₃"),
    "scene_14": ("manim_scenes.scene_14_excluded_volume", "Scene14ExcludedVolume", "Hard spheres: forbidden sphere of radius d = 8 volumes, 4 per molecule: V − nb"),
    "scene_15": ("manim_scenes.scene_15_vdw_equation", "Scene15VdwEquation", "(P + an²/V²)(V − nb) = nRT; CO₂ flask 24.9 → 26.1 → 22.4 bar; dilute limit"),
    "scene_16": ("manim_scenes.scene_16_compressibility", "Scene16Compressibility", "Z = PV/nRT; Z–P curves at 300 K; Z = V_real / V_ideal; 0.8 and 1.2"),
    "scene_17": ("manim_scenes.scene_17_boyle_temperature", "Scene17BoyleTemperature", "3D Z surface over P and T; the Boyle temperature; Z ≈ 1 by cancellation"),
    "scene_18": ("manim_scenes.scene_18_andrews", "Scene18Andrews", "Andrews' 21.5 °C isotherm: gas, gas + liquid plateau, liquid, in a 3D cylinder"),
    "scene_19": ("manim_scenes.scene_19_critical_point", "Scene19CriticalPoint", "Isotherm family, the dome, T_c 304.1 K, P_c 73.8 bar; sealed-tube meniscus vanishes"),
    "scene_20": ("manim_scenes.scene_20_vdw_loops", "Scene20VdwLoops", "Van der Waals loops, unstable branch, Maxwell's equal areas, T_c = 8a/27Rb"),
    "scene_21": ("manim_scenes.scene_21_continuity", "Scene21Continuity", "3D P–V–T surface and the endpoint of coexistence; two routes from gas to liquid"),
    "scene_22": ("manim_scenes.scene_22_cooling", "Scene22Cooling", "Critical temperatures vs room temperature: CO₂, N₂, NH₃; attraction sets T_c"),
    "scene_23": ("manim_scenes.scene_23_vapour_pressure", "Scene23VapourPressure", "Sealed 3D vessel: evaporation and condensation rates meet; vapour pressure"),
    "scene_24": ("manim_scenes.scene_24_boiling", "Scene24Boiling", "Vapour-pressure curves; boiling when P_vap = P_ext; Everest ~70 °C, cooker ~120 °C"),
    "scene_25": ("manim_scenes.scene_25_surface_energy", "Scene25SurfaceEnergy", "3D liquid slab: bulk vs surface neighbours; dW = γ dA; γ = F/L; water 73 mN/m"),
    "scene_26": ("manim_scenes.scene_26_drops_tubes", "Scene26DropsTubes", "Cube → sphere (−19 % area); capillary rise and depression; γ(T) → 0 at T_c"),
    "scene_27": ("manim_scenes.scene_27_viscosity", "Scene27Viscosity", "3D laminar layers between plates; du/dz; F/A = η du/dz"),
    "scene_28": ("manim_scenes.scene_28_honey_glass", "Scene28HoneyGlass", "Balls in water and honey; η(T) of water; glass is an amorphous solid"),
    "scene_29": ("manim_scenes.scene_29_synthesis", "Scene29Synthesis", "Speeds, size, attraction: one story from ideal gas to real liquids"),
    "scene_30": ("manim_scenes.scene_30_subscribe", "Scene30Subscribe", "Subscribe card"),
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


def _stamp(seconds: float) -> str:
    minutes, rest = divmod(int(seconds), 60)
    return f"{minutes:02d}:{rest:02d}"


def scene_starts() -> dict[str, float]:
    starts, elapsed = {}, 0.0
    for key, duration in cfg.SCENE_DURATIONS.items():
        starts[key] = elapsed
        elapsed += duration
    return starts


def list_scenes() -> None:
    print(f"\n{cfg.PROJECT_TITLE} — {cfg.PROJECT_PART}")
    print("─" * 110)
    starts = scene_starts()
    for key, (_, class_name, title) in SCENE_MAP.items():
        number = key[-2:]
        print(f"{key:<10} {_stamp(starts[number]):>6}  {class_name:<24} {cfg.SCENE_DURATIONS[number]:>5.0f}s  {title}")
    total = sum(cfg.SCENE_DURATIONS.values())
    print("─" * 110)
    print(f"{'FullVideo':<10} {'':>6}  {'FullVideo':<26} {total:>5.0f}s  ({_stamp(total)})\n")


def list_chapters() -> None:
    starts = scene_starts()
    for first, title in cfg.YOUTUBE_CHAPTERS:
        print(f"{_stamp(starts[first])} {title}")


def run_checks() -> int:
    steps = [
        ["-m", "utils.math_utils"],
        ["-m", "utils.physics_models"],
        ["-m", "utils.visual_contract_audit"],
        ["-m", "utils.spoken_numbers"],
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
    if command == "chapters":
        list_chapters()
        return 0
    if command == "check":
        return run_checks()
    if command == "export":
        return subprocess.run([sys.executable, "-m", "utils.narration_export", *args[1:]], cwd=PROJECT_ROOT,
                              check=False).returncode
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
