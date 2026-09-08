"""Audit narration pacing at a chosen frame rate without drawing video frames."""

from __future__ import annotations

import argparse
import importlib
from dataclasses import dataclass

import numpy as np
from manim import Camera, ThreeDCamera, ThreeDScene, config as manim_config
from manim.renderer.cairo_renderer import CairoRenderer

import config as cfg
from main import SCENE_MAP


@dataclass
class TimingResult:
    key: str
    elapsed: float
    remaining: float
    rendered: float


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


def camera_class_for(scene_class: type) -> type:
    """A 3D chapter still needs a 3D camera when its renderer is injected."""
    return ThreeDCamera if issubclass(scene_class, ThreeDScene) else Camera


def audit_scene(scene_name: str) -> TimingResult:
    module_name, class_name, _ = SCENE_MAP[scene_name]
    module = importlib.import_module(module_name)
    key = scene_name[-2:]
    captured: dict[str, float] = {}
    original_end = module.end_scene

    def capture_end(scene, started_at: float, target_seconds: float, **kwargs) -> None:  # noqa: ANN001, ARG001
        elapsed = float(scene.time) - started_at
        captured["elapsed"] = elapsed
        captured["remaining"] = target_seconds - elapsed - cfg.TIMING["transition"]
        original_end(scene, started_at, target_seconds, **kwargs)
        captured["rendered"] = float(scene.time) - started_at

    module.end_scene = capture_end
    scene_class = getattr(module, class_name)
    renderer = TimingRenderer(camera_class=camera_class_for(scene_class))
    scene = scene_class(renderer=renderer)
    try:
        scene.construct()
    finally:
        module.end_scene = original_end
    return TimingResult(key, captured["elapsed"], captured["remaining"], captured["rendered"])


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes", nargs="*", help="Scene keys such as scene_03 or 3")
    parser.add_argument("--fps", type=int, default=15)
    args = parser.parse_args()

    manim_config.frame_rate = args.fps
    manim_config.progress_bar = "none"
    selected = args.scenes or list(SCENE_MAP)
    normalized = [normalize(name) for name in selected]

    print(f"Timing-only audit at {args.fps} FPS")
    print("scene     elapsed   pre-fade remainder   status")
    failed = False
    total = 0.0
    for name in normalized:
        result = audit_scene(name)
        total += cfg.SCENE_DURATIONS[result.key]
        if result.remaining < -0.1:
            status = f"OVERRUN {-result.remaining:.2f}s"
            failed = True
        elif abs(result.rendered - cfg.SCENE_DURATIONS[result.key]) > 1 / args.fps + 1e-6:
            status = f"DURATION MISMATCH: {result.rendered:.2f}s"
            failed = True
        elif result.remaining > 3.0:
            status = f"PADDING {result.remaining:.2f}s"
            failed = True
        else:
            status = "OK"
        print(f"scene_{result.key}   {result.elapsed:8.2f}s   {result.remaining:8.2f}s          {status}")
    minutes, seconds = divmod(int(total), 60)
    print(f"\nProgram total (from SCENE_DURATIONS of audited scenes): {total:.0f}s ({minutes}:{seconds:02d})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
