"""Scene 07: change the rule, and watch the shape obey."""

from __future__ import annotations

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
    glow_dot,
    narration_wait,
    paced_play,
    swap_caption,
)
from utils.math_utils import parabola_window, transformed_parabola

X_MIN, X_MAX = -4.2, 4.2
Y_MIN, Y_MAX = -4.6, 6.2


class Scene07Transformations(Scene):
    """Four edits to one rule, each one visible before it is written down."""

    def construct(self) -> None:
        play_scene(self)


def _transformation_card(formula_tex: str, motion: str, color: str, transform, x_range) -> VGroup:
    """A compact before/after graph instead of a title-only recap."""
    card = RoundedRectangle(
        width=6.0,
        height=2.25,
        corner_radius=0.15,
        stroke_color=color,
        stroke_width=2,
        stroke_opacity=0.65,
        fill_color=cfg.BG,
        fill_opacity=0.55,
    )
    formula = MathTex(formula_tex, font_size=31, color=color).move_to([-1.65, 0.28, 0])
    movement = Text(
        motion,
        font="DejaVu Sans",
        font_size=20,
        color=cfg.WHITE,
        weight=BOLD,
    ).move_to([-1.65, -0.48, 0])
    mini_axes = Axes(
        x_range=[-3, 5, 1],
        y_range=[-4, 6, 2],
        x_length=2.25,
        y_length=1.5,
        tips=False,
        axis_config={"include_ticks": False, "stroke_color": cfg.MUTED, "stroke_width": 1.2},
    ).move_to([1.45, 0.02, 0])
    original = mini_axes.plot(lambda x: x * x, x_range=[-2.0, 2.0], color=cfg.GRAY,
                              stroke_width=2, stroke_opacity=0.55)
    transformed = mini_axes.plot(transform, x_range=x_range, color=color, stroke_width=3)
    return VGroup(card, formula, movement, mini_axes, original, transformed)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "07")
    add_cinematic_background(scene)

    def checkpoint(name: str) -> None:
        callback = getattr(scene, "_scene07_review", None)
        if callback:
            callback(scene, name, float(scene.time) - started)

    axes = fn_axes(x_range=(X_MIN, X_MAX, 1), y_range=(Y_MIN, Y_MAX, 2), x_length=8.6, y_length=6.4)
    axes.move_to([1.1, -0.2, 0])
    labels = axis_labels(axes, "x", "y")

    a = ValueTracker(1.0)
    h = ValueTracker(0.0)
    k = ValueTracker(0.0)

    def current_curve() -> VMobject:
        a_v, h_v, k_v = a.get_value(), h.get_value(), k.get_value()
        window = parabola_window(a_v, h_v, k_v, y_min=Y_MIN, y_max=Y_MAX, x_min=X_MIN, x_max=X_MAX)
        curve = axes.plot(transformed_parabola(a_v, h_v, k_v), x_range=list(window), color=cfg.WHITE, stroke_width=7)
        halo = curve.copy().set_stroke(cfg.CYAN, width=20, opacity=0.11)
        return VGroup(halo, curve)

    curve = always_redraw(current_curve)
    vertex = always_redraw(lambda: glow_dot(axes.c2p(h.get_value(), k.get_value()), cfg.GOLD, radius=0.11))
    ghost_window = parabola_window(1.0, 0.0, 0.0, y_min=Y_MIN, y_max=Y_MAX, x_min=X_MIN, x_max=X_MAX)
    ghost = axes.plot(
        transformed_parabola(1.0, 0.0, 0.0),
        x_range=list(ghost_window),
        color=cfg.GRAY,
        stroke_width=4,
        stroke_opacity=0.55,
    )

    formula = eq("f(x)=x^2", cfg.WHITE, cfg.FONT["title"]).move_to([-4.7, 2.9, 0])
    caption = bottom_caption("Start with one clean shape.", cfg.CYAN)

    paced_play(scene, Create(axes), FadeIn(labels), run_time=1.1)
    scene.add(curve, vertex)
    paced_play(scene, FadeIn(formula), FadeIn(caption), run_time=1.0)
    narration_wait(scene, 6.0)

    # --- 1. Add two to every output.
    caption = swap_caption(scene, caption, "Add two to every output.", cfg.GOLD)
    paced_play(scene, Create(ghost), run_time=0.8)
    narration_wait(scene, 2.0)
    up_formula = eq("f(x)+2=x^2+2", cfg.GREEN, cfg.FONT["title"]).move_to([-4.7, 2.9, 0])
    if up_formula.width > 5.4:
        up_formula.scale_to_fit_width(5.4)
    up_formula.move_to([-4.7, 2.9, 0])
    paced_play(scene, ReplacementTransform(formula, up_formula), run_time=0.8)
    paced_play(scene, k.animate.set_value(2.0), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 6.5)
    paced_play(scene, k.animate.set_value(0.0), run_time=2.0)
    narration_wait(scene, 3.0)

    # --- 2. The counter-intuitive one: subtract inside.
    caption = swap_caption(scene, caption, "Now subtract two inside the rule.", cfg.GOLD)
    right_formula = eq("f(x-2)=(x-2)^2", cfg.PURPLE, cfg.FONT["title"])
    if right_formula.width > 5.4:
        right_formula.scale_to_fit_width(5.4)
    right_formula.move_to([-4.7, 2.9, 0])
    paced_play(scene, ReplacementTransform(up_formula, right_formula), run_time=0.8)
    narration_wait(scene, 5.0)

    guess = eq(r"\text{left?}", cfg.GOLD, cfg.FONT["section"]).move_to([-4.7, 1.6, 0])
    paced_play(scene, FadeIn(guess, shift=DOWN * 0.2), run_time=0.6)
    checkpoint("01_bright_left")
    narration_wait(scene, 4.5)
    paced_play(scene, h.animate.set_value(2.0), run_time=3.2, rate_func=rate_functions.ease_in_out_sine)
    paced_play(scene, FadeOut(guess, scale=0.7), run_time=0.5)
    narration_wait(scene, 4.0)

    # The landmark argument, spelled out on the vertex itself.
    caption = swap_caption(scene, caption, "Follow the lowest point.", cfg.GOLD)
    # Three short lines instead of one long one: each stays at full size, which
    # is what keeps them readable on a phone.
    reasoning = VGroup(
        eq(r"\text{lowest when}", cfg.WHITE, cfg.FONT["section"]),
        eq("x-2=0", cfg.WHITE, cfg.FONT["section"]),
        eq(r"\Rightarrow x=2", cfg.GOLD, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    if reasoning.width > 5.4:
        reasoning.scale_to_fit_width(5.4)
    reasoning.move_to([-4.6, 1.05, 0])
    marker = DashedLine(axes.c2p(2, 0), axes.c2p(2, 3.4), color=cfg.GOLD, stroke_width=3.5, dash_length=0.14)
    tick_label = eq("2", cfg.GOLD, cfg.FONT["body"]).next_to(axes.c2p(2, 0), DOWN, buff=0.28)
    for line in reasoning:
        paced_play(scene, FadeIn(line, shift=RIGHT * 0.2), run_time=0.6)
        narration_wait(scene, 2.2)
    paced_play(scene, Create(marker), FadeIn(tick_label), run_time=0.9)
    narration_wait(scene, 6.0)
    paced_play(scene, FadeOut(VGroup(reasoning, marker, tick_label)), h.animate.set_value(0.0), run_time=1.6)

    # --- 3. Stretch: every output doubles.
    caption = swap_caption(scene, caption, "Double every output.", cfg.GOLD)
    stretch_formula = eq("2f(x)=2x^2", cfg.ORANGE, cfg.FONT["title"]).move_to([-4.7, 2.9, 0])
    paced_play(scene, ReplacementTransform(right_formula, stretch_formula), run_time=0.8)

    sample_dot = glow_dot(axes.c2p(1, 1), cfg.CYAN, radius=0.1)
    sample_label = MathTex("1", r"\rightarrow", "1", font_size=cfg.FONT["section"])
    sample_label[0].set_color(cfg.GOLD)
    sample_label[1].set_color(cfg.WHITE)
    sample_label[2].set_color(cfg.GREEN)
    sample_label.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    sample_label.move_to([-4.7, 1.35, 0])
    paced_play(scene, FadeIn(sample_dot, scale=1.5), FadeIn(sample_label), run_time=0.8)
    checkpoint("02_bright_landmark")
    narration_wait(scene, 4.5)

    lifted_dot = glow_dot(axes.c2p(1, 2), cfg.GREEN, radius=0.1)
    lift_arrow = Arrow(axes.c2p(1, 1.05), axes.c2p(1, 1.95), color=cfg.GREEN, stroke_width=6, buff=0.0, max_tip_length_to_length_ratio=0.3)
    new_label = MathTex("1", r"\rightarrow", "2", font_size=cfg.FONT["section"])
    new_label[0].set_color(cfg.GOLD)
    new_label[1].set_color(cfg.WHITE)
    new_label[2].set_color(cfg.GREEN)
    new_label.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    new_label.move_to([-4.7, 1.35, 0])
    paced_play(scene, GrowArrow(lift_arrow), FadeIn(lifted_dot, scale=1.5), ReplacementTransform(sample_label, new_label), run_time=1.0)
    narration_wait(scene, 4.0)
    paced_play(scene, a.animate.set_value(2.0), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 5.5)
    paced_play(
        scene,
        FadeOut(VGroup(sample_dot, lifted_dot, lift_arrow, new_label)),
        a.animate.set_value(1.0),
        run_time=1.6,
    )

    # --- 4. Reflect: every output changes sign.
    caption = swap_caption(scene, caption, "Flip the sign of every output.", cfg.GOLD)
    flip_formula = eq("-f(x)=-x^2", cfg.RED, cfg.FONT["title"]).move_to([-4.7, 2.9, 0])
    paced_play(scene, ReplacementTransform(stretch_formula, flip_formula), run_time=0.8)
    narration_wait(scene, 3.5)
    paced_play(scene, a.animate.set_value(-1.0), run_time=3.2, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 6.0)

    # --- Replay all four edits back to back, against the original shape.
    caption = swap_caption(scene, caption, "Four edits. Four motions.", cfg.GOLD)
    recap_formula = eq("f(x)=x^2", cfg.WHITE, cfg.FONT["title"]).move_to([-4.7, 2.9, 0])
    paced_play(scene, ReplacementTransform(flip_formula, recap_formula), a.animate.set_value(1.0), run_time=1.2)
    recap = [
        ("x^2+2", cfg.GREEN, k, 2.0),
        ("(x-2)^2", cfg.PURPLE, h, 2.0),
        ("2x^2", cfg.ORANGE, a, 2.0),
        ("-x^2", cfg.RED, a, -1.0),
    ]
    for latex, color, tracker, value in recap:
        chip = eq(latex, color, cfg.FONT["section"]).move_to([-4.7, 1.5, 0])
        rest = 1.0 if tracker is a else 0.0
        paced_play(scene, FadeIn(chip, shift=UP * 0.15), run_time=0.45)
        paced_play(scene, tracker.animate.set_value(value), run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        narration_wait(scene, 1.1)
        paced_play(scene, tracker.animate.set_value(rest), FadeOut(chip, scale=0.7), run_time=1.1)

    # --- Four small before/after graphs make the recap usable as a reference.
    curve.clear_updaters()
    vertex.clear_updaters()
    summary_title = Text(
        "The rule tells the graph how to move.",
        font="DejaVu Sans",
        font_size=34,
        color=cfg.WHITE,
        weight=MEDIUM,
    ).move_to([0, 3.35, 0])
    cards = VGroup(
        _transformation_card(r"f(x)+2", "UP", cfg.GREEN, lambda x: x*x+2, [-1.9, 1.9]),
        _transformation_card(r"f(x-2)", "RIGHT", cfg.PURPLE, lambda x: (x-2)**2, [0.0, 4.0]),
        _transformation_card(r"2f(x)", "STRETCH", cfg.ORANGE, lambda x: 2*x*x, [-1.65, 1.65]),
        _transformation_card(r"-f(x)", "REFLECT", cfg.RED, lambda x: -x*x, [-2.0, 2.0]),
    ).arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.28)).move_to([0, 0.05, 0])
    next_step = Text(
        "Next: connect two rules.",
        font="DejaVu Sans",
        font_size=25,
        color=cfg.CYAN,
        weight=MEDIUM,
    ).move_to([0, -3.35, 0])
    paced_play(
        scene,
        FadeOut(VGroup(axes, labels, curve, vertex, ghost, recap_formula), scale=0.9),
        FadeOut(caption),
        run_time=1.0,
    )
    paced_play(
        scene,
        FadeIn(summary_title),
        LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.12),
        FadeIn(next_step),
        run_time=1.0,
    )
    checkpoint("03_visual_summary")
    narration_wait(scene, 3.5)

    end_scene(scene, started, cfg.SCENE_DURATIONS["07"])
