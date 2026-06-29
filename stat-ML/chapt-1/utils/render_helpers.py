"""Render and export helpers."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def available_scenes(scene_map: dict[str, tuple[str, str]]) -> list[str]:
    return list(scene_map.keys())


def render_scene(
    project_root: Path,
    module: str,
    class_name: str,
    quality: str = "qh",
    fps: int = 30,
) -> int:
    py_path = project_root / (module.replace(".", "/") + ".py")
    cmd = [
        sys.executable, "-m", "manim",
        f"-q{quality}",
        "--fps", str(fps),
        str(py_path),
        class_name,
    ]
    result = subprocess.run(cmd, cwd=str(project_root))
    return result.returncode


def stitch_scenes(
    project_root: Path,
    scene_video_paths: list[Path],
    output_path: Path,
) -> int:
    """Concatenate rendered scene videos using ffmpeg."""
    list_file = project_root / "output" / "_concat_list.txt"
    list_file.parent.mkdir(parents=True, exist_ok=True)
    with open(list_file, "w") as f:
        for p in scene_video_paths:
            f.write(f"file '{p.resolve()}'\n")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(output_path),
    ]
    result = subprocess.run(cmd)
    return result.returncode
