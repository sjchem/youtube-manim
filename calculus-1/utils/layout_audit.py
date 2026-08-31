"""Fast text-overlap and frame-boundary audit without rendering video frames."""

from __future__ import annotations

import argparse
import importlib
from dataclasses import dataclass

import numpy as np
from manim import MathTex, Scene, Text, config as manim_config
from manim.renderer.cairo_renderer import CairoRenderer

import config as cfg
from main import SCENE_MAP


@dataclass(frozen=True)
class TextBox:
    label: str
    left: float
    right: float
    bottom: float
    top: float

    @property
    def area(self) -> float:
        return max(self.right - self.left, 0) * max(self.top - self.bottom, 0)


def _label(mobject) -> str:  # noqa: ANN001
    if isinstance(mobject, Text):
        return mobject.text
    try:
        return mobject.get_tex_string()
    except AttributeError:
        return type(mobject).__name__


def _text_boxes(scene: Scene) -> list[TextBox]:
    boxes: list[TextBox] = []
    seen: set[int] = set()
    for top_level in scene.mobjects:
        if getattr(top_level, "_is_project_background", False):
            continue
        for member in top_level.get_family():
            if id(member) in seen or not isinstance(member, (Text, MathTex)):
                continue
            seen.add(id(member))
            if member.width < 0.02 or member.height < 0.02:
                continue
            boxes.append(
                TextBox(
                    _label(member),
                    float(member.get_left()[0]),
                    float(member.get_right()[0]),
                    float(member.get_bottom()[1]),
                    float(member.get_top()[1]),
                )
            )
    return boxes


def _overlap_ratio(first: TextBox, second: TextBox) -> float:
    width = min(first.right, second.right) - max(first.left, second.left)
    height = min(first.top, second.top) - max(first.bottom, second.bottom)
    if width <= 0 or height <= 0:
        return 0.0
    return width * height / max(min(first.area, second.area), 1e-9)


class LayoutRenderer(CairoRenderer):
    """Advance animations to their final state, auditing each distinct layout."""

    def __init__(self, scene_key: str) -> None:
        super().__init__()
        self.scene_key = scene_key
        self.issues: set[str] = set()

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
        self._audit(scene)

    def _audit(self, scene: Scene) -> None:
        boxes = _text_boxes(scene)
        frame_left = -cfg.FRAME_WIDTH / 2 + 0.08
        frame_right = cfg.FRAME_WIDTH / 2 - 0.08
        frame_bottom = -cfg.FRAME_HEIGHT / 2 + 0.08
        frame_top = cfg.FRAME_HEIGHT / 2 - 0.08
        for box in boxes:
            if box.left < frame_left or box.right > frame_right or box.bottom < frame_bottom or box.top > frame_top:
                self.issues.add(f"{self.scene_key} play {self.num_plays}: outside frame: {box.label!r}")

        for index, first in enumerate(boxes):
            for second in boxes[index + 1 :]:
                if _overlap_ratio(first, second) >= 0.18:
                    labels = sorted((first.label, second.label))
                    self.issues.add(
                        f"{self.scene_key} play {self.num_plays}: text overlap: {labels[0]!r} / {labels[1]!r}"
                    )


def _normalize(name: str) -> str:
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
    parser.add_argument("scenes", nargs="*", help="Scene keys or numbers; default is every scene")
    parser.add_argument("--fps", type=int, default=5)
    args = parser.parse_args()

    manim_config.frame_rate = args.fps
    manim_config.progress_bar = "none"
    selected = [_normalize(name) for name in args.scenes] if args.scenes else list(SCENE_MAP)

    issues: list[str] = []
    for scene_name in selected:
        module_name, class_name, _ = SCENE_MAP[scene_name]
        module = importlib.import_module(module_name)
        module.end_scene = lambda *unused_args, **unused_kwargs: None
        renderer = LayoutRenderer(scene_name)
        scene = getattr(module, class_name)(renderer=renderer)
        scene.construct()
        issues.extend(sorted(renderer.issues))
        print(f"{scene_name}: {len(renderer.issues)} issue(s)")

    if issues:
        print("\n".join(issues))
        return 1
    print("All readable text stays inside the frame and free of text-on-text collisions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
