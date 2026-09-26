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
from utils.timing_audit import camera_class_for, normalize


@dataclass(frozen=True)
class TextBox:
    label: str
    left: float
    right: float
    bottom: float
    top: float
    # Identity of the mobject this glyph sits directly inside. Two lines that
    # share one parent were arranged together on purpose, so tight leading
    # between them is a typographic choice rather than a collision.
    parent: int = 0

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


def _invisible(mobject) -> bool:  # noqa: ANN001
    """Faded-out glyphs still sit in scene.mobjects; they cannot collide visually."""
    # Text/MathTex containers can have zero opacity while their glyphs are
    # visible. Inspect rendered descendants rather than skipping the container.
    for glyph in mobject.family_members_with_points():
        if float(glyph.get_fill_opacity()) >= 0.05 or (
            float(glyph.get_stroke_opacity()) >= 0.05
            and float(glyph.get_stroke_width()) > 0
        ):
            return False
    return True



def _text_boxes(scene: Scene) -> list[TextBox]:
    boxes: list[TextBox] = []
    seen: set[int] = set()
    for top_level in scene.mobjects:
        if getattr(top_level, "_is_project_background", False):
            continue
        for parent, member in _walk(top_level, id(top_level)):
            if id(member) in seen or not isinstance(member, (Text, MathTex)):
                continue
            if getattr(member, "_is_decorative", False):
                continue
            seen.add(id(member))
            if member.width < 0.02 or member.height < 0.02:
                continue
            if _invisible(member):
                continue
            # Audit the actual camera projection, including fixed HUD text in 3D.
            points = member.get_all_points()
            if not len(points):
                continue
            if hasattr(scene.camera, "reset_rotation_matrix"):
                scene.camera.reset_rotation_matrix()
            projected = scene.camera.transform_points_pre_display(member, points)
            boxes.append(
                TextBox(
                    _label(member),
                    float(projected[:, 0].min()),
                    float(projected[:, 0].max()),
                    float(projected[:, 1].min()),
                    float(projected[:, 1].max()),
                    parent,
                )
            )
    return boxes


def _walk(mobject, parent: int):  # noqa: ANN001, ANN201
    """Yield (immediate parent id, mobject) for a mobject and its descendants."""
    yield parent, mobject
    for child in mobject.submobjects:
        yield from _walk(child, id(mobject))


# Two captions that merely touch read as one crowded block on a phone, so the
# audit enforces a gap as well as an absence of overlap. And for text, any
# visible overlap at all is a defect — a clipped corner is as unreadable as a
# fully covered word, so the ratio limit is deliberately near zero.
BREATHING_ROOM = 0.16
OVERLAP_LIMIT = 0.03


def _overlap_ratio(first: TextBox, second: TextBox) -> float:
    width = min(first.right, second.right) - max(first.left, second.left)
    height = min(first.top, second.top) - max(first.bottom, second.bottom)
    if width <= 0 or height <= 0:
        return 0.0
    return width * height / max(min(first.area, second.area), 1e-9)


def _too_close(first: TextBox, second: TextBox) -> bool:
    """True when two text blocks share a column (or a row) and nearly touch."""
    x_gap = max(first.left, second.left) - min(first.right, second.right)
    y_gap = max(first.bottom, second.bottom) - min(first.top, second.top)
    if x_gap < 0 and 0 <= y_gap < BREATHING_ROOM:
        return True
    return y_gap < 0 and 0 <= x_gap < BREATHING_ROOM


class LayoutRenderer(CairoRenderer):
    """Advance animations to their final state, auditing each distinct layout."""

    def __init__(self, scene_key: str, camera_class=None, sample_motion=False) -> None:  # noqa: ANN001
        super().__init__(camera_class=camera_class)
        self.scene_key = scene_key
        self.issues: set[str] = set()
        self.sample_motion = sample_motion

    def play(self, scene, *args, **kwargs) -> None:  # noqa: ANN001
        scene.compile_animation_data(*args, **kwargs)
        scene.begin_animations()
        duration = scene.get_run_time(scene.animations)
        frame_step = 1 / self.camera.frame_rate
        self.time += len(np.arange(0, duration, frame_step)) * frame_step
        if self.sample_motion:
            for alpha in (.25, .5, .75):
                for animation in scene.animations:
                    animation.interpolate(alpha)
                self._audit(scene)
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
            for second in boxes[index + 1:]:
                labels = sorted((first.label, second.label))
                if _overlap_ratio(first, second) >= OVERLAP_LIMIT:
                    self.issues.add(
                        f"{self.scene_key} play {self.num_plays}: text overlap: {labels[0]!r} / {labels[1]!r}"
                    )
                elif first.parent != second.parent and _too_close(first, second):
                    self.issues.add(
                        f"{self.scene_key} play {self.num_plays}: text crowding: {labels[0]!r} / {labels[1]!r}"
                    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes", nargs="*", help="Scene keys or numbers; default is every scene")
    parser.add_argument("--fps", type=int, default=5)
    parser.add_argument("--motion", action="store_true", help="Also inspect quarter, half, and three-quarter animation states")
    args = parser.parse_args()

    manim_config.frame_rate = args.fps
    manim_config.progress_bar = "none"
    selected = [normalize(name) for name in args.scenes] if args.scenes else list(SCENE_MAP)

    issues: list[str] = []
    for scene_name in selected:
        module_name, class_name, _ = SCENE_MAP[scene_name]
        module = importlib.import_module(module_name)
        original_end = module.end_scene
        module.end_scene = lambda *unused_args, **unused_kwargs: None
        scene_class = getattr(module, class_name)
        renderer = LayoutRenderer(scene_name, camera_class=camera_class_for(scene_class), sample_motion=args.motion)
        scene = scene_class(renderer=renderer)
        try:
            scene.construct()
        finally:
            module.end_scene = original_end
        issues.extend(sorted(renderer.issues))
        print(f"{scene_name}: {len(renderer.issues)} issue(s)", flush=True)
        for issue in sorted(renderer.issues):
            print(issue, flush=True)

    if issues:
        print("\n".join(issues))
        return 1
    print("All readable text stays inside the frame and free of text-on-text collisions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
