"""Convenience entry point for rendering the motivation physics project."""

from __future__ import annotations

import argparse
import subprocess


SCENES = {
    "01": ("scene_01_hook.py", "Scene01Hook"),
    "02": ("scene_02_motivation_decay.py", "Scene02MotivationDecay"),
    "03": ("scene_03_inertia.py", "Scene03Inertia"),
    "04": ("scene_04_friction.py", "Scene04Friction"),
    "05": ("scene_05_energy_barrier.py", "Scene05EnergyBarrier"),
    "06": ("scene_06_momentum.py", "Scene06Momentum"),
    "07": ("scene_07_feedback_loop.py", "Scene07FeedbackLoop"),
    "08": ("scene_08_final_synthesis.py", "Scene08FinalSynthesis"),
}


def run(command):
    print(" ".join(command))
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description="Render Manim scenes for Why Motivation Fades.")
    parser.add_argument("--scene", choices=[*SCENES.keys(), "full"], default="01")
    parser.add_argument("--quality", default="pql", help="Manim quality flag without leading dash, e.g. pql, pqh, p, quality h")
    parser.add_argument("--no-preview", action="store_true", help="Do not open the rendered video.")
    args = parser.parse_args()

    quality_flag = f"-{args.quality}"
    if args.no_preview and "p" in args.quality:
        quality_flag = "-" + args.quality.replace("p", "", 1)

    if args.scene == "full":
        run(["manim", quality_flag, "manim_scenes/full_video.py", "FullVideo"])
        return

    file_name, scene_name = SCENES[args.scene]
    run(["manim", quality_flag, f"manim_scenes/{file_name}", scene_name])


if __name__ == "__main__":
    main()

