"""Scene 07: zoom into a curve until it becomes indistinguishable from a line."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    dashed_ring,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    tangent_line,
)
from utils.math_utils import cubic_wiggle, d_cubic_wiggle


class Scene07LocalLinearity(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "07")
    add_cinematic_background(scene)

    f_label = eq("f(x)=x^3-x", cfg.WHITE, cfg.FONT["section"]).to_corner(UL, buff=0.5)
    paced_play(scene, Write(f_label), run_time=1.1)

    # Shift the wide graph left so the chosen point, rather than the axes'
    # origin, becomes the center of the later zoom.
    axes = calc_axes(x_range=(-2, 2, 1), y_range=(-2, 2, 1), x_length=8.0, y_length=6.0).move_to([-2.3, -0.4, 0])
    axis_label_size = cfg.FONT["section"] + 4
    x_axis_label = eq("x", cfg.WHITE, axis_label_size).next_to(axes.x_axis.get_right(), UP, buff=0.14)
    y_axis_label = eq("f(x)", cfg.WHITE, axis_label_size).next_to(axes.y_axis.get_top(), RIGHT, buff=0.14)
    axis_labels = VGroup(x_axis_label, y_axis_label)
    curve = axes.plot(cubic_wiggle, x_range=[-1.9, 1.9], color=cfg.WHITE, stroke_width=5)

    x1 = 1.15
    anchor = axes.c2p(x1, cubic_wiggle(x1))
    tangent = tangent_line(axes, cubic_wiggle, d_cubic_wiggle, x1, cfg.GREEN, half_length=1.6)
    tangent.set_stroke(opacity=0)

    # Axis labels establish orientation at the wide view, then disappear
    # before the coordinate system itself is magnified far beyond the frame.
    world = VGroup(axes, curve, tangent)
    paced_play(scene, Create(axes), FadeIn(axis_labels), run_time=1.6)
    paced_play(scene, Create(curve), run_time=3.4, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 3.51)

    reticle = dashed_ring(anchor, 0.14, cfg.GOLD, num_dashes=12)
    anchor_dot = glow_dot(anchor, cfg.GOLD, 0.11)
    reticle.set_z_index(19, family=True)
    anchor_dot.set_z_index(20, family=True)
    pick_caption = bottom_caption("Pick one point, and zoom in.", cfg.GOLD)
    paced_play(scene, Create(reticle), FadeIn(anchor_dot), FadeIn(pick_caption), FadeOut(axis_labels), run_time=0.9)
    narration_wait(scene, 10.34)

    zoom_label = outlined_text("ZOOM  1x", cfg.FONT["body"], cfg.GOLD, BOLD).to_corner(UR, buff=0.5)
    scene.add(zoom_label)

    cumulative = 1.0
    for level in (5, 20, 100, 1000):
        relative_factor = level / cumulative
        cumulative = level
        new_zoom_label = outlined_text(f"ZOOM  {level}x", cfg.FONT["body"], cfg.GOLD, BOLD).to_corner(UR, buff=0.5)
        paced_play(
            scene,
            world.animate.scale(relative_factor, about_point=anchor),
            ReplacementTransform(zoom_label, new_zoom_label),
            run_time=5.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        zoom_label = new_zoom_label
        narration_wait(scene, 1.29)

    flat_caption = bottom_caption("The curve straightens into its tangent.", cfg.GREEN)
    paced_play(scene, ReplacementTransform(pick_caption, flat_caption), FadeOut(reticle), tangent.animate.set_stroke(opacity=1), run_time=1.3)
    narration_wait(scene, 15.51)

    message = bottom_caption("A derivative is the line that best fits a curve, up close.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(flat_caption, message), run_time=0.8)
    narration_wait(scene, 10.34)

    approx = eq(r"f(x+\Delta x)\approx f(x)+f'(x)\,\Delta x", cfg.GOLD, cfg.FONT["body"])
    approx.to_corner(UL, buff=0.5)
    if approx.width > cfg.SAFE_WIDTH:
        approx.scale_to_fit_width(cfg.SAFE_WIDTH)
    paced_play(scene, ReplacementTransform(f_label, approx), FadeOut(zoom_label), run_time=1.3)
    narration_wait(scene, 15.51)

    closing = bottom_caption("Every curve looks straight, once you zoom in far enough.", cfg.GOLD)
    paced_play(scene, ReplacementTransform(message, closing), run_time=0.8)
    narration_wait(scene, 15.51)

    end_scene(scene, started, cfg.SCENE_DURATIONS["07"])
