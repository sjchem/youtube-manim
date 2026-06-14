"""Command helpers for local rendering."""

from __future__ import annotations

SCENE_CLASSES = [
    "Scene01Hook",
    "Scene02ReverseMultiplication",
    "Scene03ZeroCollapse",
    "Scene04NoSolution",
    "Scene05LimitsNotInfinity",
    "Scene06ZeroOverZero",
    "Scene07Computers",
    "Scene08FinalSummary",
]


def preview_command(scene_name: str = "Scene01Hook") -> str:
    return f"manim -pql manim_scenes/scene_01.py {scene_name}"


def scene_command(module: str, scene_name: str, quality: str = "-pqh") -> str:
    return f"manim {quality} manim_scenes/{module}.py {scene_name}"


def full_video_command(quality: str = "-pqh") -> str:
    return f"manim {quality} manim_scenes/full_video.py FullVideo"
