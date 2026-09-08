"""Scene 08: two machines in a pipeline, and why the order is not a detail."""

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
    flow_arrow,
    fn_axes,
    glow_curve,
    machine,
    narration_wait,
    paced_play,
    swap_caption,
    token,
)
from utils.math_utils import plus_two_after_square, square_after_plus_two

PIPE_Y = 0.9
SLOT_X = (-6.35, -3.75, -0.85, 2.35, 5.55)


class Scene08Composition(Scene):
    """Wire the machines together; the order changes the answer."""

    def construct(self) -> None:
        play_scene(self)


def _pipeline(first_label: str, second_label: str, colors: tuple[str, str]) -> tuple[VGroup, VGroup]:
    first = machine(first_label, colors[0], width=2.5, height=1.9, tex=True, font_size=cfg.FONT["body"])
    second = machine(second_label, colors[1], width=2.5, height=1.9, tex=True, font_size=cfg.FONT["body"])
    first.move_to([SLOT_X[1], PIPE_Y, 0])
    second.move_to([SLOT_X[3], PIPE_Y, 0])
    return first, second


def _glowing_ball(center, color: str) -> VGroup:
    """A small shaded sphere with a readable glow at preview resolution."""
    outer_glow = Circle(radius=0.33, color=color, stroke_width=18, stroke_opacity=0.10)
    inner_glow = Circle(radius=0.25, color="#FFE6A3", stroke_width=10, stroke_opacity=0.24)
    sphere = Sphere(
        center=ORIGIN,
        radius=0.19,
        resolution=(16, 24),
        checkerboard_colors=["#FFE6A3", "#D89224"],
        stroke_width=0,
        fill_opacity=1,
    ).rotate(0.32, RIGHT).rotate(-0.42, UP)
    rim = Circle(radius=0.19, color="#FFF4CB", stroke_width=1.4, stroke_opacity=0.72)
    highlight = Dot(UP * 0.067 + LEFT * 0.067 + OUT * 0.09, radius=0.042, color=WHITE)
    highlight.set_opacity(0.9)
    return VGroup(outer_glow, inner_glow, sphere, rim, highlight).move_to(center)


def _run_the_line(
    scene: Scene,
    stops: list[Mobject],
    color: str,
    run_time: float = 0.85,
    *,
    checkpoint_name: str | None = None,
    started_at: float = 0,
) -> None:
    """Send one glowing 3D ball the whole length of the pipeline."""
    pulse = _glowing_ball(stops[0].get_center(), color)
    scene.add(pulse)
    for index, stop in enumerate(stops[1:]):
        scene.play(pulse.animate.move_to(stop.get_center()), run_time=run_time, rate_func=rate_functions.ease_in_out_sine)
        if index == 0 and checkpoint_name:
            callback = getattr(scene, "_scene08_review", None)
            if callback:
                callback(scene, checkpoint_name, float(scene.time) - started_at)
    scene.play(FadeOut(pulse, scale=0.5), run_time=0.35)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "08")
    add_cinematic_background(scene)

    def checkpoint(name: str) -> None:
        callback = getattr(scene, "_scene08_review", None)
        if callback:
            callback(scene, name, float(scene.time) - started)

    caption = bottom_caption("Bolt one machine onto the next.", cfg.CYAN)
    labels = VGroup(
        eq("f(x)=x+2", cfg.CYAN, cfg.FONT["body"]).move_to([SLOT_X[1], 3.15, 0]),
        eq("g(x)=x^2", cfg.PURPLE, cfg.FONT["body"]).move_to([SLOT_X[3], 3.15, 0]),
    )
    paced_play(scene, FadeIn(labels[0]), FadeIn(labels[1]), FadeIn(caption), run_time=1.1)
    narration_wait(scene, 6.0)

    # --- Order one: add two, then square.
    first, second = _pipeline("+2", r"\text{square}", (cfg.CYAN, cfg.PURPLE))
    x_tok = token("x", cfg.INPUT_COLOR).move_to([SLOT_X[0], PIPE_Y, 0])
    mid_tok = token("x+2", cfg.WHITE).move_to([SLOT_X[2], PIPE_Y, 0])
    out_tok = token("(x+2)^2", cfg.OUTPUT_COLOR).move_to([SLOT_X[4], PIPE_Y, 0])
    arrows = VGroup(
        flow_arrow(x_tok.get_right() + RIGHT * 0.16, first.get_left() + LEFT * 0.16, cfg.INPUT_COLOR, 5),
        flow_arrow(first.get_right() + RIGHT * 0.16, mid_tok.get_left() + LEFT * 0.16, cfg.WHITE, 5),
        flow_arrow(mid_tok.get_right() + RIGHT * 0.16, second.get_left() + LEFT * 0.16, cfg.WHITE, 5),
        flow_arrow(second.get_right() + RIGHT * 0.16, out_tok.get_left() + LEFT * 0.16, cfg.OUTPUT_COLOR, 5),
    )
    paced_play(scene, FadeIn(first, scale=0.9), FadeIn(second, scale=0.9), run_time=0.9)
    paced_play(scene, FadeIn(x_tok, shift=RIGHT * 0.3), GrowFromEdge(arrows[0], LEFT), run_time=0.8)
    paced_play(scene, Indicate(first.body, color=cfg.WHITE, scale_factor=1.06), GrowFromEdge(arrows[1], LEFT), run_time=0.8)
    paced_play(scene, FadeIn(mid_tok, shift=RIGHT * 0.3), run_time=0.7)
    narration_wait(scene, 4.5)
    paced_play(scene, GrowFromEdge(arrows[2], LEFT), Indicate(second.body, color=cfg.WHITE, scale_factor=1.06), run_time=0.9)
    paced_play(scene, GrowFromEdge(arrows[3], LEFT), FadeIn(out_tok, shift=RIGHT * 0.3), run_time=0.8)
    narration_wait(scene, 3.0)
    _run_the_line(
        scene, [x_tok, first, mid_tok, second, out_tok], cfg.GOLD,
        checkpoint_name="01_first_3d_ball", started_at=started,
    )
    narration_wait(scene, 3.5)

    composed = eq("g(f(x))=(x+2)^2", cfg.OUTPUT_COLOR, cfg.FONT["section"]).move_to([0, -1.5, 0])
    paced_play(scene, FadeIn(composed, shift=UP * 0.25), run_time=0.9)
    narration_wait(scene, 6.5)

    # --- A concrete number, so nobody has to trust the algebra.
    caption = swap_caption(scene, caption, "Try it with three.", cfg.GOLD)
    numeric = VGroup(
        eq("3", cfg.INPUT_COLOR, cfg.FONT["section"]),
        eq(r"\rightarrow 5", cfg.WHITE, cfg.FONT["section"]),
        eq(r"\rightarrow 25", cfg.OUTPUT_COLOR, cfg.FONT["section"]),
    ).arrange(RIGHT, buff=0.35).move_to([0, -2.6, 0])
    for piece in numeric:
        paced_play(scene, FadeIn(piece, shift=RIGHT * 0.25), run_time=0.6)
        narration_wait(scene, 2.4)
    narration_wait(scene, 4.0)

    # --- Swap the machines.
    caption = swap_caption(scene, caption, "Now swap the two machines.", cfg.RED)
    paced_play(scene, FadeOut(VGroup(composed, numeric), scale=0.85), run_time=0.6)
    paced_play(
        scene,
        labels[0].animate.move_to([SLOT_X[3], 3.15, 0]),
        labels[1].animate.move_to([SLOT_X[1], 3.15, 0]),
        first.animate.move_to([SLOT_X[3], PIPE_Y, 0]),
        second.animate.move_to([SLOT_X[1], PIPE_Y, 0]),
        FadeOut(VGroup(mid_tok, out_tok, arrows[1], arrows[2], arrows[3]), scale=0.8),
        run_time=1.6,
        path_arc=0.9,
    )
    new_mid = token("x^2", cfg.WHITE).move_to([SLOT_X[2], PIPE_Y, 0])
    new_out = token("x^2+2", cfg.OUTPUT_COLOR).move_to([SLOT_X[4], PIPE_Y, 0])
    new_arrows = VGroup(
        flow_arrow(second.get_right() + RIGHT * 0.16, new_mid.get_left() + LEFT * 0.16, cfg.WHITE, 5),
        flow_arrow(new_mid.get_right() + RIGHT * 0.16, first.get_left() + LEFT * 0.16, cfg.WHITE, 5),
        flow_arrow(first.get_right() + RIGHT * 0.16, new_out.get_left() + LEFT * 0.16, cfg.OUTPUT_COLOR, 5),
    )
    paced_play(scene, Indicate(second.body, color=cfg.WHITE, scale_factor=1.06), GrowFromEdge(new_arrows[0], LEFT), run_time=0.9)
    paced_play(scene, FadeIn(new_mid, shift=RIGHT * 0.3), run_time=0.7)
    paced_play(scene, GrowFromEdge(new_arrows[1], LEFT), Indicate(first.body, color=cfg.WHITE, scale_factor=1.06), run_time=0.9)
    paced_play(scene, GrowFromEdge(new_arrows[2], LEFT), FadeIn(new_out, shift=RIGHT * 0.3), run_time=0.8)
    narration_wait(scene, 2.5)
    _run_the_line(
        scene, [x_tok, second, new_mid, first, new_out], cfg.GOLD,
        checkpoint_name="02_second_3d_ball", started_at=started,
    )
    narration_wait(scene, 3.0)

    swapped = eq("f(g(x))=x^2+2", cfg.OUTPUT_COLOR, cfg.FONT["section"]).move_to([0, -1.5, 0])
    numeric_2 = VGroup(
        eq("3", cfg.INPUT_COLOR, cfg.FONT["section"]),
        eq(r"\rightarrow 9", cfg.WHITE, cfg.FONT["section"]),
        eq(r"\rightarrow 11", cfg.OUTPUT_COLOR, cfg.FONT["section"]),
    ).arrange(RIGHT, buff=0.35).move_to([0, -2.6, 0])
    paced_play(scene, FadeIn(swapped, shift=UP * 0.25), run_time=0.9)
    paced_play(scene, FadeIn(numeric_2, shift=UP * 0.2), run_time=0.9)
    narration_wait(scene, 6.5)

    # --- The two answers, side by side, then their two shapes.
    caption = swap_caption(scene, caption, "Same parts. Different result.", cfg.RED)
    verdict = eq(r"25 \;\neq\; 11", cfg.RED, cfg.FONT["title"]).move_to([0, -2.6, 0])
    paced_play(scene, ReplacementTransform(numeric_2, verdict), run_time=0.9)
    narration_wait(scene, 6.0)

    paced_play(
        scene,
        FadeOut(VGroup(first, second, new_mid, new_out, x_tok, arrows[0], new_arrows, labels, swapped, verdict), scale=0.85),
        run_time=0.9,
    )
    axes = fn_axes(x_range=(-5, 3, 1), y_range=(-0.5, 9, 2), x_length=7.6, y_length=5.2)
    axes.move_to([0.6, -0.35, 0])
    axis_tags = axis_labels(axes, "x", "y")
    curve_a = axes.plot(square_after_plus_two, x_range=[-5, 0.9], color=cfg.CYAN, stroke_width=7)
    curve_b = axes.plot(plus_two_after_square, x_range=[-2.6, 2.6], color=cfg.PURPLE, stroke_width=7)
    tag_a = eq("(x+2)^2", cfg.CYAN, cfg.FONT["body"]).move_to([-5.0, 2.4, 0])
    tag_b = eq("x^2+2", cfg.PURPLE, cfg.FONT["body"]).move_to([-5.0, 1.2, 0])
    paced_play(scene, Create(axes), FadeIn(axis_tags), run_time=1.1)
    paced_play(scene, Create(glow_curve(curve_a, cfg.CYAN)), FadeIn(tag_a), run_time=1.3)
    paced_play(scene, Create(glow_curve(curve_b, cfg.PURPLE)), FadeIn(tag_b), run_time=1.3)
    narration_wait(scene, 7.0)

    identity = MathTex(
        r"(g\circ f)(x)", "=", r"g(f(x))",
        font_size=44,
    )
    identity[0].set_color(cfg.CYAN)
    identity[1].set_color(cfg.WHITE)
    identity[2].set_color(cfg.GREEN)
    identity.set_stroke(cfg.BG, width=3, opacity=0.94, background=True)
    identity_box = SurroundingRectangle(
        identity,
        color=cfg.CYAN,
        buff=0.27,
        corner_radius=0.14,
        stroke_width=2.5,
        fill_color=cfg.PANEL,
        fill_opacity=0.88,
    )
    identity_glow = identity_box.copy().set_fill(opacity=0).set_stroke(cfg.CYAN, width=13, opacity=0.09)
    rule = VGroup(identity_glow, identity_box, identity).move_to([0, 3.32, 0])
    paced_play(scene, FadeOut(caption), FadeIn(rule, scale=0.92), run_time=1.0)
    checkpoint("03_bright_identity")
    narration_wait(scene, 5.0)

    foreshadow = bottom_caption("Order can change the result. Could a machine undo it?", cfg.PURPLE)
    paced_play(scene, FadeIn(foreshadow, shift=UP * 0.2), run_time=0.8)
    narration_wait(scene, 4.5)

    end_scene(scene, started, cfg.SCENE_DURATIONS["08"])
