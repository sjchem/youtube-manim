"""Command helpers used by README and quick preview scripts."""

from __future__ import annotations

SCENE_NAMES = [
    "Scene01Hook",
    "Scene02MotivationDecay",
    "Scene03Inertia",
    "Scene04Friction",
    "Scene05EnergyBarrier",
    "Scene06Momentum",
    "Scene07FeedbackLoop",
    "Scene08FinalSynthesis",
]


def scene_render_command(scene_file, scene_name, quality="pql"):
    return f"manim -{quality} manim_scenes/{scene_file} {scene_name}"


def full_video_command(quality="pqh"):
    return f"manim -{quality} manim_scenes/full_video.py FullVideo"

