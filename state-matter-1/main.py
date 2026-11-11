"""Command-line entry point for 'The Molecular Dance'.

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
    "scene_01": ("manim_scenes.scene_01_hook", "Scene01Hook", "Balloon → inside the air: a 3D crowd of molecules; 10 t per m²; title"),
    "scene_02": ("manim_scenes.scene_02_puzzle", "Scene02Puzzle", "One molecule's zigzag vs steady gauges; four questions"),
    "scene_03": ("manim_scenes.scene_03_inside_between", "Scene03InsideBetween", "3D water: bonds inside vs attractions between (≈460 vs ≈20 kJ/mol)"),
    "scene_04": ("manim_scenes.scene_04_dispersion", "Scene04Dispersion", "Flickering clouds, induced dipoles, −1/r⁶, noble-gas boiling points"),
    "scene_05": ("manim_scenes.scene_05_dipoles", "Scene05Dipoles", "3D HCl poses; tumbling dipoles: Keesom average measured"),
    "scene_06": ("manim_scenes.scene_06_hydrogen_bonds", "Scene06HydrogenBonds", "Dipole–induced dipole; 3D water network; NH₃; H₂O vs H₂S"),
    "scene_07": ("manim_scenes.scene_07_repulsion", "Scene07Repulsion", "Clouds overlap; the Lennard-Jones curve: wall, well, tail"),
    "scene_08": ("manim_scenes.scene_08_thermal_motion", "Scene08ThermalMotion", "⟨K⟩ = 3/2 k_B T; live speed histogram shifts on heating"),
    "scene_09": ("manim_scenes.scene_09_tug_of_war", "Scene09TugOfWar", "2D Lennard-Jones MD: crystal → liquid → gas; ideal-gas model"),
    "scene_10": ("manim_scenes.scene_10_one_wall", "Scene10OneWall", "One molecule in a 3D cube; elastic bounce: Δp = 2m vₓ"),
    "scene_11": ("manim_scenes.scene_11_hits_to_force", "Scene11HitsToForce", "Spikes every 2L/vₓ spread into F = m vₓ²/L"),
    "scene_12": ("manim_scenes.scene_12_crowd", "Scene12Crowd", "1, 5, 50, 5000 molecules: force smooths; P = N m⟨vₓ²⟩/V"),
    "scene_13": ("manim_scenes.scene_13_one_third", "Scene13OneThird", "3D velocity ball; ⟨vₓ²⟩ = ⟨v²⟩/3; PV = ⅓ N m⟨v²⟩"),
    "scene_14": ("manim_scenes.scene_14_temperature", "Scene14Temperature", "PV = ⅔ N⟨K⟩ → N k_B T → n R T"),
    "scene_15": ("manim_scenes.scene_15_boyle", "Scene15Boyle", "J-tube; isothermal piston: more hits, P ∝ 1/V, equal PV rectangles"),
    "scene_16": ("manim_scenes.scene_16_boyle_numbers", "Scene16BoyleNumbers", "4 L, 1 bar → 2 L: 2 bar; P vs 1/V; isotherms"),
    "scene_17": ("manim_scenes.scene_17_thinner_air", "Scene17ThinnerAir", "Density ∝ P; Everest; rapid compression warms"),
    "scene_18": ("manim_scenes.scene_18_charles", "Scene18Charles", "Weighted piston + heater: V ∝ T; hot-air balloon"),
    "scene_19": ("manim_scenes.scene_19_absolute_zero", "Scene19AbsoluteZero", "V–θ lines meet at −273.15 °C; Kelvin scale"),
    "scene_20": ("manim_scenes.scene_20_kelvin", "Scene20Kelvin", "300 → 450 K: 3 L; the Celsius trap (≈3 %)"),
    "scene_21": ("manim_scenes.scene_21_gay_lussac", "Scene21GayLussac", "Rigid box heated: P ∝ T; 1.00 → 1.20 bar; sealed gas cylinder"),
    "scene_22": ("manim_scenes.scene_22_side_by_side", "Scene22SideBySide", "Charles vs Gay-Lussac side by side; tyres"),
    "scene_23": ("manim_scenes.scene_23_avogadro", "Scene23Avogadro", "Pump in molecules at constant P, T: V ∝ n"),
    "scene_24": ("manim_scenes.scene_24_equal_volumes", "Scene24EqualVolumes", "He, N₂, CO₂ boxes: equal N; 22.71 L vs 22.4 L"),
    "scene_25": ("manim_scenes.scene_25_ideal_surface", "Scene25IdealSurface", "Four laws → PV = nRT; the 3D P–V–T surface and its slices"),
    "scene_26": ("manim_scenes.scene_26_using_ideal", "Scene26UsingIdeal", "R = 8.314; one mole fills 25 L; weather balloon 3.33 L"),
    "scene_27": ("manim_scenes.scene_27_density", "Scene27Density", "ρ = PM/RT: N₂ 1.12 g/L, He 0.16 g/L; M from ρ"),
    "scene_28": ("manim_scenes.scene_28_dalton", "Scene28Dalton", "Two gases, separate hits; P = P_A + P_B; 2 + 1 bar; Everest O₂"),
    "scene_29": ("manim_scenes.scene_29_over_water", "Scene29OverWater", "Gas over water: 1.000 − 0.0317 = 0.968 bar"),
    "scene_30": ("manim_scenes.scene_30_limits", "Scene30Limits", "Attractions, size, speed spread; Maxwell–Boltzmann; Part 2"),
    "scene_31": ("manim_scenes.scene_31_subscribe", "Scene31Subscribe", "Subscribe card"),
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
        ["-m", "utils.gas_data"],
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
