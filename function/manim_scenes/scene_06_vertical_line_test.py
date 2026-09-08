"""Scene 06: the vertical line test, discovered before it is named."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    axis_labels,
    begin_scene,
    bottom_caption,
    end_scene,
    eq,
    fn_axes,
    glow_curve,
    glow_dot,
    narration_wait,
    paced_play,
    swap_caption,
    verdict_badge,
)
from utils.math_utils import square

AXES_CENTER = [0, -0.15, 0]


class Scene06VerticalLineTest(Scene):
    """One vertical line, one crossing - or the rule is broken."""

    def construct(self) -> None:
        play_scene(self)


def _scanner(axes: Axes, tracker: ValueTracker, y_low: float, y_high: float) -> VGroup:
    def build() -> VGroup:
        x = tracker.get_value()
        line = Line(axes.c2p(x, y_low), axes.c2p(x, y_high), color=cfg.GOLD, stroke_width=5)
        halo = line.copy().set_stroke(cfg.GOLD, width=22, opacity=0.14)
        return VGroup(halo, line)

    return always_redraw(build)


def _comparison_panel(kind: str) -> VGroup:
    """A small visual summary of one crossing versus two crossings."""
    ok = kind == "one"
    color = cfg.GREEN if ok else cfg.RED
    card = RoundedRectangle(
        width=5.25,
        height=4.15,
        corner_radius=0.16,
        stroke_color=color,
        stroke_width=2,
        stroke_opacity=0.72,
        fill_color=cfg.BG,
        fill_opacity=0.5,
    )
    mini_axes = Axes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-2.2, 4.4, 1],
        x_length=3.35,
        y_length=2.45,
        tips=False,
        axis_config={"include_ticks": False, "stroke_color": cfg.MUTED, "stroke_width": 1.5},
    ).shift(UP * 0.35)
    if ok:
        curve = mini_axes.plot(lambda x: x * x, x_range=[-1.9, 1.9], color=cfg.CYAN, stroke_width=3)
        x_value = 0.8
        scan = Line(mini_axes.c2p(x_value, -1.8), mini_axes.c2p(x_value, 4.0), color=cfg.GOLD, stroke_width=3)
        hits = VGroup(glow_dot(mini_axes.c2p(x_value, x_value**2), cfg.GREEN, radius=0.075))
        words = "ONE CROSSING"
        symbol = r"\checkmark"
    else:
        curve = ParametricFunction(
            lambda t: mini_axes.c2p(1.55 * np.cos(t), 1.55 * np.sin(t)),
            t_range=[0, TAU],
            color=cfg.PURPLE,
            stroke_width=3,
        )
        x_value = 0.45
        y_value = float(np.sqrt(1.55**2 - x_value**2))
        scan = Line(mini_axes.c2p(x_value, -2.0), mini_axes.c2p(x_value, 2.0), color=cfg.GOLD, stroke_width=3)
        hits = VGroup(
            glow_dot(mini_axes.c2p(x_value, y_value), cfg.GREEN, radius=0.075),
            glow_dot(mini_axes.c2p(x_value, -y_value), cfg.PURPLE, radius=0.075),
        )
        words = "TWO CROSSINGS"
        symbol = r"\times"
    label = VGroup(
        MathTex(symbol, font_size=34, color=color),
        Text(words, font="DejaVu Sans", font_size=22, color=color, weight=BOLD),
    ).arrange(RIGHT, buff=0.18).move_to([0, -1.55, 0])
    return VGroup(card, mini_axes, curve, scan, hits, label)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "06")
    add_cinematic_background(scene)

    def checkpoint(name: str) -> None:
        callback = getattr(scene, "_scene06_review", None)
        if callback:
            callback(scene, name, float(scene.time) - started)

    axes = fn_axes(x_range=(-4, 4, 1), y_range=(-2.5, 5, 1), x_length=6.0, y_length=5.625)
    axes.move_to(AXES_CENTER)
    labels = axis_labels(axes, "x", "y")
    curve = axes.plot(square, x_range=[-2.2, 2.2], color=cfg.WHITE, stroke_width=7)
    glow = glow_curve(curve, cfg.CYAN)
    tag = eq("y=x^2", cfg.WHITE, cfg.FONT["section"]).move_to([-4.9, 2.5, 0])

    caption = bottom_caption("Slide a line across and count the crossings.", cfg.CYAN)
    paced_play(scene, Create(axes), FadeIn(labels), run_time=1.1)
    paced_play(scene, Create(glow), FadeIn(tag), FadeIn(caption), run_time=1.3)
    narration_wait(scene, 5.0)

    tracker = ValueTracker(-2.2)
    scanner = _scanner(axes, tracker, -2.4, 4.9)
    hit = always_redraw(
        lambda: glow_dot(axes.c2p(tracker.get_value(), square(tracker.get_value())), cfg.GREEN, radius=0.11)
    )
    scene.add(scanner, hit)
    paced_play(scene, tracker.animate.set_value(2.2), run_time=6.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 3.5)

    good = verdict_badge("ONE CROSSING", True, scale=1.0).move_to([4.3, 2.7, 0])
    paced_play(scene, FadeIn(good, scale=1.15), run_time=0.8)
    narration_wait(scene, 6.0)

    # --- Now a shape that is not the graph of a function of x.
    caption = swap_caption(scene, caption, "Same test. Different shape.", cfg.RED)
    scene.remove(scanner, hit)
    circle_tag = eq("x^2+y^2=4", cfg.WHITE, cfg.FONT["section"]).move_to([-4.9, 2.5, 0])
    ring = ParametricFunction(
        lambda t: axes.c2p(2 * np.cos(t), 2 * np.sin(t)),
        t_range=[0, TAU],
        color=cfg.WHITE,
        stroke_width=7,
    )
    ring_glow = glow_curve(ring, cfg.PURPLE)
    paced_play(
        scene,
        FadeOut(good, scale=0.85),
        ReplacementTransform(glow, ring_glow),
        ReplacementTransform(tag, circle_tag),
        run_time=1.3,
    )
    narration_wait(scene, 4.5)

    tracker.set_value(-1.95)
    scanner = _scanner(axes, tracker, -2.4, 4.9)
    upper = always_redraw(
        lambda: glow_dot(
            axes.c2p(tracker.get_value(), float(np.sqrt(max(4 - tracker.get_value() ** 2, 0.0)))),
            cfg.GREEN,
            radius=0.11,
        )
    )
    lower = always_redraw(
        lambda: glow_dot(
            axes.c2p(tracker.get_value(), -float(np.sqrt(max(4 - tracker.get_value() ** 2, 0.0)))),
            cfg.PURPLE,
            radius=0.11,
        )
    )
    scene.add(scanner, upper, lower)
    paced_play(scene, tracker.animate.set_value(1.95), run_time=6.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.0)
    paced_play(scene, tracker.animate.set_value(0.0), run_time=2.0)

    conflict = MathTex(
        r"x=0", r"\Rightarrow", r"y=2", r"\quad\text{and}\quad", r"y=-2",
        font_size=cfg.FONT["body"],
    )
    conflict[0].set_color(cfg.GOLD)
    conflict[1].set_color(cfg.WHITE)
    conflict[2].set_color(cfg.GREEN)
    conflict[3].set_color(cfg.WHITE)
    conflict[4].set_color(cfg.PURPLE)
    conflict.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    conflict.move_to([0, -3.15, 0])
    paced_play(scene, FadeOut(caption), FadeIn(conflict, shift=UP * 0.2), run_time=0.8)
    checkpoint("01_bright_coordinates")
    narration_wait(scene, 6.0)
    bad = verdict_badge("TWO ANSWERS", False, scale=1.0).move_to([4.3, 2.7, 0])
    paced_play(scene, FadeIn(bad, scale=1.15), run_time=0.8)
    narration_wait(scene, 5.5)

    scene.remove(scanner, upper, lower)
    summary_title = Text(
        "Scan vertically. Count the intersections.",
        font="DejaVu Sans",
        font_size=34,
        color=cfg.WHITE,
        weight=MEDIUM,
    ).move_to([0, 3.25, 0])
    one = _comparison_panel("one").move_to([-3.05, 0.2, 0])
    two = _comparison_panel("two").move_to([3.05, 0.2, 0])
    rule = Text(
        "A function passes every vertical line.",
        font="DejaVu Sans",
        font_size=27,
        color=cfg.CYAN,
        weight=MEDIUM,
    ).move_to([0, -3.15, 0])
    paced_play(
        scene,
        FadeOut(VGroup(ring_glow, circle_tag, bad, conflict, axes, labels), scale=0.9),
        run_time=0.9,
    )
    paced_play(
        scene,
        FadeIn(summary_title),
        FadeIn(one, shift=RIGHT * 0.2),
        FadeIn(two, shift=LEFT * 0.2),
        FadeIn(rule),
        run_time=0.9,
    )
    checkpoint("02_visual_summary")
    narration_wait(scene, 8.5)

    end_scene(scene, started, cfg.SCENE_DURATIONS["06"])
