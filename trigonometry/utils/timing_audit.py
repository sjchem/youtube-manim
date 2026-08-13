"""Audit narration pacing at a chosen frame rate without drawing video frames."""

from __future__ import annotations

import argparse
import importlib
from dataclasses import dataclass

import numpy as np
from manim import config as manim_config
from manim.renderer.cairo_renderer import CairoRenderer

import config as cfg
from main import SCENE_MAP


@dataclass
class TimingResult:
    key: str
    elapsed: float
    remaining: float


class TimingRenderer(CairoRenderer):
    """Advance Manim's clock and mobject state without rasterizing frames."""

    def play(self, scene, *args, **kwargs) -> None:  # noqa: ANN001
        scene.compile_animation_data(*args, **kwargs)
        scene.begin_animations()
        duration = scene.get_run_time(scene.animations)
        frame_step = 1 / self.camera.frame_rate
        self.time += len(np.arange(0, duration, frame_step)) * frame_step
        for animation in scene.animations:
            animation.update_mobjects(duration)
            animation.interpolate(1.0)
            animation.finish()
            animation.clean_up_from_scene(scene)
        scene.update_mobjects(duration)
        self.static_image = None
        self.num_plays += 1


def audit_scene(scene_name: str, fps: int) -> TimingResult:
    module_name, class_name, _ = SCENE_MAP[scene_name]
    module = importlib.import_module(module_name)
    key = scene_name[-2:]
    captured: dict[str, float] = {}

    def capture_end(scene, started_at: float, target_seconds: float, **kwargs) -> None:  # noqa: ANN001, ARG001
        elapsed = float(scene.time) - started_at
        captured["elapsed"] = elapsed
        captured["remaining"] = target_seconds - elapsed - cfg.TIMING["transition"]

    module.end_scene = capture_end
    renderer = TimingRenderer()
    scene = getattr(module, class_name)(renderer=renderer)
    scene.construct()
    return TimingResult(key, captured["elapsed"], captured["remaining"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes", nargs="*", help="Scene keys such as scene_03 or scene_03_coordinates")
    parser.add_argument("--fps", type=int, default=15)
    args = parser.parse_args()

    manim_config.frame_rate = args.fps
    manim_config.progress_bar = "none"
    selected = args.scenes or list(SCENE_MAP)

    def normalize(name: str) -> str:
        if name in SCENE_MAP:
            return name
        if name.isdigit():
            candidate = f"scene_{int(name):02d}"
            if candidate in SCENE_MAP:
                return candidate
        for key in SCENE_MAP:
            if name.startswith(key):
                return key
        raise ValueError(f"Unknown scene: {name}")

    normalized = [normalize(name) for name in selected]

    print(f"Timing-only audit at {args.fps} FPS")
    print("scene     elapsed   pre-fade remainder   status")
    failed = False
    for name in normalized:
        result = audit_scene(name, args.fps)
        if result.remaining < -0.1:
            status = f"OVERRUN {-result.remaining:.2f}s"
            failed = True
        elif result.remaining > 1.0:
            status = f"PADDING {result.remaining:.2f}s"
            failed = True
        else:
            status = "OK"
        print(f"scene_{result.key}   {result.elapsed:8.2f}s   {result.remaining:8.2f}s          {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
