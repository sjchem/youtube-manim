"""Save still frames of a scene's key layouts without rendering any video.

Each ``scene.play(...)`` is advanced straight to its final state and captured,
so one cheap pass produces a contact sheet of every distinct composition:

    python -m utils.storyboard scene_04 --every 4
    python -m utils.storyboard 6 --at 12 13 14 --out output/storyboard
"""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path

import numpy as np
from manim import config as manim_config
from manim.renderer.cairo_renderer import CairoRenderer

import config as cfg
from main import SCENE_MAP
from utils.timing_audit import camera_class_for, normalize


class StoryboardRenderer(CairoRenderer):
    """Advance every animation to its end state and photograph the chosen ones."""

    def __init__(self, scene_key: str, out_dir: Path, wanted, camera_class=None) -> None:  # noqa: ANN001
        super().__init__(camera_class=camera_class)
        self.scene_key = scene_key
        self.out_dir = out_dir
        self.wanted = wanted
        self.saved: list[Path] = []

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
        if self.wanted(self.num_plays):
            self._capture(scene)

    def _capture(self, scene) -> None:  # noqa: ANN001
        self.camera.init_background()
        self.camera.reset()
        self.camera.capture_mobjects(scene.mobjects)
        path = self.out_dir / f"{self.scene_key}_play{self.num_plays:03d}.png"
        self.camera.get_image().save(path)
        self.saved.append(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes", nargs="+", help="Scene keys or numbers")
    parser.add_argument("--every", type=int, default=3, help="Capture every Nth play (default 3)")
    parser.add_argument("--at", type=int, nargs="*", help="Capture only these play indices")
    parser.add_argument("--out", default="output/storyboard", help="Destination directory")
    parser.add_argument("--width", type=int, default=854)
    args = parser.parse_args()

    manim_config.frame_rate = 5
    manim_config.progress_bar = "none"
    manim_config.pixel_width = args.width
    manim_config.pixel_height = round(args.width * 9 / 16)

    out_dir = cfg.PROJECT_ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted = (lambda n: n in set(args.at)) if args.at else (lambda n: n % args.every == 0)

    for name in (normalize(value) for value in args.scenes):
        module_name, class_name, _ = SCENE_MAP[name]
        module = importlib.import_module(module_name)
        module.end_scene = lambda *unused_args, **unused_kwargs: None
        scene_class = getattr(module, class_name)
        renderer = StoryboardRenderer(name, out_dir, wanted, camera_class=camera_class_for(scene_class))
        scene = scene_class(renderer=renderer)
        scene.construct()
        for path in renderer.saved:
            print(path.relative_to(cfg.PROJECT_ROOT))
        print(f"{name}: {len(renderer.saved)} frame(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
