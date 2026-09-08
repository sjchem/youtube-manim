"""Scene 09: running the machine backward, and why that is a reflection."""

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
    feed_machine,
    flow_arrow,
    fn_axes,
    glow_curve,
    glow_dot,
    machine,
    narration_wait,
    paced_play,
    swap_caption,
    token,
)
from utils.math_utils import identity_reflection_matrix
from utils.render_helpers import fit_width

MACHINE_Y = 1.5


def _graph_tag(tex: str, color: str, position: list[float]) -> VGroup:
    """High-contrast graph label that stays readable over glowing curves."""
    label = eq(tex, color, 46)
    label.set_stroke(cfg.WHITE, width=0.7, opacity=0.28)
    plate = RoundedRectangle(
        width=label.width + 0.34,
        height=label.height + 0.20,
        corner_radius=0.12,
        stroke_width=0,
        fill_color=cfg.BG,
        fill_opacity=0.88,
    )
    return VGroup(plate, label).move_to(position)


class Scene09Inverse(Scene):
    """Undo the rule, and the graph folds across the line y = x."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "09")
    add_cinematic_background(scene)

    # --- 1. Forward: five in, ten out.
    box = machine(r"\times 2", cfg.RULE_COLOR, width=3.0, height=2.0, tex=True, font_size=cfg.FONT["title"])
    box.move_to([0, MACHINE_Y, 0])
    in_tok = token("5", cfg.INPUT_COLOR).move_to([-4.4, MACHINE_Y, 0])
    out_tok = token("10", cfg.OUTPUT_COLOR).move_to([4.4, MACHINE_Y, 0])
    arrow_in = flow_arrow(in_tok.get_right() + RIGHT * 0.2, box.get_left() + LEFT * 0.2, cfg.INPUT_COLOR)
    arrow_out = flow_arrow(box.get_right() + RIGHT * 0.2, out_tok.get_left() + LEFT * 0.2, cfg.OUTPUT_COLOR)

    caption = bottom_caption("Forward is easy.", cfg.CYAN)
    paced_play(scene, FadeIn(box, scale=0.9), FadeIn(caption), run_time=1.0)
    paced_play(scene, FadeIn(in_tok, shift=RIGHT * 0.3), GrowFromEdge(arrow_in, LEFT), run_time=0.8)
    scene.add(arrow_out)
    feed_machine(scene, box, in_tok, out_tok, run_time=1.6)
    narration_wait(scene, 6.0)

    # --- 2. What machine would undo it?
    caption = swap_caption(scene, caption, "What machine would undo it?", cfg.GOLD)
    question = eq("?", cfg.RED, 150).move_to(box.body.get_center())
    old_label = box.label.copy()
    scene.add(old_label)
    box.label.set_opacity(0)
    paced_play(scene, ReplacementTransform(old_label, question), run_time=0.8)
    paced_play(
        scene,
        Rotate(VGroup(arrow_in, arrow_out), PI, axis=UP, about_point=box.get_center()),
        run_time=1.2,
    )
    narration_wait(scene, 6.0)

    inverse_label = eq(r"\div 2", cfg.RULE_COLOR, cfg.FONT["title"]).move_to(box.body.get_center())
    paced_play(scene, ReplacementTransform(question, inverse_label), run_time=0.9)
    back_in = token("10", cfg.INPUT_COLOR).move_to([4.4, MACHINE_Y, 0])
    back_out = token("5", cfg.OUTPUT_COLOR).move_to([-4.4, MACHINE_Y, 0])
    paced_play(scene, FadeOut(out_tok, scale=0.7), FadeIn(back_in, scale=1.2), run_time=0.7)
    paced_play(
        scene,
        back_in.animate.move_to(box.body.get_center()).scale(0.4).set_opacity(0),
        run_time=0.8,
        rate_func=rate_functions.ease_in_quad,
    )
    scene.remove(back_in)
    paced_play(scene, Indicate(box.body, color=cfg.WHITE, scale_factor=1.06), run_time=0.5)
    back_out.save_state()
    back_out.move_to(box.body.get_center()).scale(0.4).set_opacity(0)
    scene.add(back_out)
    paced_play(scene, Restore(back_out), run_time=0.7)
    narration_wait(scene, 6.5)

    pair = VGroup(
        eq("f(x)=2x", cfg.CYAN, cfg.FONT["section"]),
        eq(r"f^{-1}(x)=\dfrac{x}{2}", cfg.GREEN, cfg.FONT["section"]),
    ).arrange(RIGHT, buff=1.4).move_to([0, -1.5, 0])
    fit_width(pair, cfg.SAFE_WIDTH - 1.6)
    paced_play(scene, FadeIn(pair[0], shift=UP * 0.2), run_time=0.8)
    narration_wait(scene, 3.5)
    paced_play(scene, FadeIn(pair[1], shift=UP * 0.2), run_time=0.8)
    caption = swap_caption(scene, caption, "Inverse means undo; it does not mean reciprocal.", cfg.GOLD)
    narration_wait(scene, 3.4)

    round_trip = eq(r"f^{-1}\big(f(x)\big)=x", cfg.WHITE, cfg.FONT["section"]).move_to([0, -2.9, 0])
    paced_play(scene, FadeIn(round_trip, shift=UP * 0.2), run_time=0.9)
    narration_wait(scene, 5.5)
    paced_play(scene, FadeOut(round_trip, scale=0.85), run_time=0.6)

    # --- 3. Put both on one grid.
    caption = swap_caption(scene, caption, "Both rules, one picture.", cfg.GOLD)
    pair_target = pair.copy().arrange(DOWN, buff=0.42).scale(0.88).move_to([-4.85, 2.45, 0])
    paced_play(
        scene,
        FadeOut(VGroup(box, inverse_label, arrow_in, arrow_out, back_out), scale=0.85),
        Transform(pair, pair_target),
        run_time=1.2,
    )

    axes = fn_axes(x_range=(-4, 4, 1), y_range=(-4, 4, 1), x_length=6.0, y_length=6.0)
    axes.move_to([1.9, -0.05, 0])
    tags = axis_labels(axes, "x", "y")
    origin = axes.c2p(0, 0)

    identity = DashedLine(
        axes.c2p(-3.8, -3.8),
        axes.c2p(3.8, 3.8),
        color=cfg.GOLD,
        stroke_width=4.5,
        dash_length=0.16,
        stroke_opacity=0.9,
    )
    identity_tag = _graph_tag("y=x", cfg.GOLD, [5.25, 2.42, 0])
    forward = axes.plot(lambda x: 2 * x, x_range=[-1.95, 1.95], color=cfg.CYAN, stroke_width=7)
    forward_glow = glow_curve(forward, cfg.CYAN)
    forward_tag = _graph_tag("y=2x", cfg.CYAN, [2.05, 3.23, 0])

    paced_play(scene, Create(axes), FadeIn(tags), run_time=1.1)
    paced_play(scene, Create(identity), FadeIn(identity_tag), run_time=1.0)
    paced_play(scene, Create(forward_glow), FadeIn(forward_tag), run_time=1.1)
    narration_wait(scene, 5.5)

    # --- 4. One point tells the whole story.
    caption = swap_caption(scene, caption, "Watch one point.", cfg.GOLD)
    point_a = glow_dot(axes.c2p(1, 2), cfg.GOLD, radius=0.11)
    label_a = eq("(1,2)", cfg.GOLD, cfg.FONT["body"]).next_to(axes.c2p(1, 2), LEFT, buff=1.1)
    paced_play(scene, FadeIn(point_a, scale=1.6), FadeIn(label_a), run_time=0.8)
    narration_wait(scene, 5.0)

    point_b = glow_dot(axes.c2p(2, 1), cfg.GREEN, radius=0.11)
    label_b = eq("(2,1)", cfg.GREEN, cfg.FONT["body"]).next_to(axes.c2p(2, 1), RIGHT, buff=0.24)
    bridge = DashedLine(axes.c2p(1, 2), axes.c2p(2, 1), color=cfg.WHITE, stroke_width=3, dash_length=0.12, stroke_opacity=0.7)
    paced_play(scene, Create(bridge), run_time=0.7)
    paced_play(scene, TransformFromCopy(point_a, point_b), FadeIn(label_b), run_time=1.3)
    narration_wait(scene, 6.0)

    swap_rule = eq(r"(a,b) \rightarrow (b,a)", cfg.WHITE, cfg.FONT["section"]).move_to([-4.85, 0.4, 0])
    paced_play(scene, FadeIn(swap_rule, shift=UP * 0.2), run_time=0.8)
    narration_wait(scene, 6.0)

    reason = VGroup(
        eq(r"f:\; x \rightarrow y", cfg.CYAN, cfg.FONT["body"]),
        eq(r"f^{-1}:\; y \rightarrow x", cfg.GREEN, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to([-4.85, -1.4, 0])
    for line in reason:
        paced_play(scene, FadeIn(line, shift=RIGHT * 0.2), run_time=0.7)
        narration_wait(scene, 3.8)

    # --- 5. Fold the whole line across y = x.
    caption = swap_caption(scene, caption, "Do it to every point at once.", cfg.GOLD)
    mirrored = forward_glow.copy()
    scene.add(mirrored)
    paced_play(
        scene,
        FadeOut(VGroup(bridge, label_a, label_b, point_a, point_b)),
        run_time=0.6,
    )
    paced_play(
        scene,
        ApplyMatrix(identity_reflection_matrix(), mirrored, about_point=origin),
        run_time=3.2,
        rate_func=rate_functions.ease_in_out_sine,
    )
    paced_play(scene, mirrored.animate.set_color(cfg.GREEN), run_time=0.7)
    inverse_tag = _graph_tag(r"y=\dfrac{x}{2}", cfg.GREEN, [5.45, 0.86, 0])
    paced_play(scene, FadeIn(inverse_tag), run_time=0.6)
    narration_wait(scene, 10.5)

    closing = MathTex(
        r"\text{The inverse graph mirrors the original across }",
        r"y=x",
        color=cfg.WHITE,
        font_size=cfg.FONT["section"],
    )
    closing[1].set_color(cfg.GOLD)
    closing.set_stroke(cfg.BG, width=3.5, opacity=0.96, background=True)
    fit_width(closing, cfg.SAFE_WIDTH - 1.0)
    closing.move_to([0, -3.42, 0])
    paced_play(scene, FadeOut(caption), FadeIn(closing, shift=UP * 0.2), run_time=0.9)
    narration_wait(scene, 11.5)

    end_scene(scene, started, cfg.SCENE_DURATIONS["09"])
