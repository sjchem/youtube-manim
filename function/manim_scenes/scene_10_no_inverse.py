"""Scene 10: some machines cannot be run backward - until you narrow the door."""

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
    glow_dot,
    machine,
    narration_wait,
    outlined_text,
    paced_play,
    swap_caption,
    token,
)
from utils.math_utils import identity_reflection_matrix, square
from utils.render_helpers import fit_width


class Scene10NoInverse(Scene):
    """One output, two possible histories - and the repair."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "10")
    add_cinematic_background(scene)

    # --- 1. Two different inputs land on the same answer.
    box = machine("x^2", cfg.RULE_COLOR, width=2.8, height=2.0, tex=True, font_size=cfg.FONT["title"])
    box.move_to([0, 1.35, 0])
    top_in = token("2", cfg.INPUT_COLOR).move_to([-4.6, 2.35, 0])
    bottom_in = token("-2", cfg.INPUT_COLOR).move_to([-4.6, 0.35, 0])
    out_tok = token("4", cfg.OUTPUT_COLOR).move_to([4.6, 1.35, 0])
    arrows = VGroup(
        flow_arrow(top_in.get_right() + RIGHT * 0.2, box.get_left() + LEFT * 0.15 + UP * 0.45, cfg.INPUT_COLOR, 5),
        flow_arrow(bottom_in.get_right() + RIGHT * 0.2, box.get_left() + LEFT * 0.15 + DOWN * 0.45, cfg.INPUT_COLOR, 5),
        flow_arrow(box.get_right() + RIGHT * 0.2, out_tok.get_left() + LEFT * 0.2, cfg.OUTPUT_COLOR, 5),
    )
    caption = bottom_caption("Two doors. One answer.", cfg.CYAN)
    paced_play(scene, FadeIn(box, scale=0.9), FadeIn(caption), run_time=1.0)
    paced_play(
        scene,
        FadeIn(top_in, shift=RIGHT * 0.3),
        FadeIn(bottom_in, shift=RIGHT * 0.3),
        GrowFromEdge(arrows[0], LEFT),
        GrowFromEdge(arrows[1], LEFT),
        run_time=1.1,
    )
    paced_play(scene, GrowFromEdge(arrows[2], LEFT), FadeIn(out_tok, shift=RIGHT * 0.3), run_time=0.9)
    narration_wait(scene, 6.5)

    # --- 2. Now try to run it backward.
    caption = swap_caption(scene, caption, "Now hand it a four and ask for the input.", cfg.RED)
    # Reverse each segment in place; rotating the whole fork disconnects it.
    reversed_arrows = VGroup(*[
        flow_arrow(a[-1].get_end(), a[-1].get_start(), cfg.RED, 5) for a in arrows
    ])
    paced_play(scene, ReplacementTransform(arrows, reversed_arrows), run_time=1.3)
    arrows = reversed_arrows
    guesses = VGroup(
        eq(r"2\;?", cfg.RED, cfg.FONT["title"]).move_to([-4.6, 2.35, 0]),
        eq(r"-2\;?", cfg.RED, cfg.FONT["title"]).move_to([-4.6, 0.35, 0]),
    )
    paced_play(
        scene,
        FadeOut(VGroup(top_in, bottom_in), scale=0.7),
        FadeIn(guesses, scale=1.2),
        run_time=0.9,
    )
    for _ in range(2):
        paced_play(scene, Indicate(guesses[0], color=cfg.RED, scale_factor=1.15), run_time=0.5)
        paced_play(scene, Indicate(guesses[1], color=cfg.RED, scale_factor=1.15), run_time=0.5)
    narration_wait(scene, 7.0)
    stuck = outlined_text("The machine cannot choose.", cfg.FONT["section"], cfg.RED).move_to([0, -1.7, 0])
    paced_play(scene, FadeIn(stuck, shift=UP * 0.2), run_time=0.9)
    narration_wait(scene, 5.0)

    # --- 3. See the same failure on the graph.
    caption = swap_caption(scene, caption, "The graph says it too.", cfg.GOLD)
    paced_play(
        scene,
        FadeOut(VGroup(box, guesses, out_tok, arrows, stuck), scale=0.85),
        run_time=0.9,
    )
    axes = fn_axes(x_range=(-3, 6, 1), y_range=(-1, 6, 1), x_length=7.2, y_length=5.6)
    axes.move_to([1.4, -0.35, 0])
    tags = axis_labels(axes, "x", "y")
    parabola = axes.plot(square, x_range=[-2.25, 2.25], color=cfg.WHITE, stroke_width=7)
    parabola_glow = glow_curve(parabola, cfg.CYAN)
    paced_play(scene, Create(axes), FadeIn(tags), run_time=1.0)
    paced_play(scene, Create(parabola_glow), run_time=1.2)

    level = Line(axes.c2p(-3.2, 4), axes.c2p(3.2, 4), color=cfg.RED, stroke_width=5)
    level_tag = eq("y=4", cfg.RED, cfg.FONT["small"]).next_to(axes.c2p(-3.2, 4), LEFT, buff=0.2)
    hits = VGroup(glow_dot(axes.c2p(-2, 4), cfg.RED, 0.1), glow_dot(axes.c2p(2, 4), cfg.RED, 0.1))
    paced_play(scene, Create(level), FadeIn(level_tag), run_time=1.0)
    paced_play(scene, FadeIn(hits, scale=1.5), run_time=0.7)
    narration_wait(scene, 8.0)

    # --- 4. The repair: shut one of the doors.
    caption = swap_caption(scene, caption, "So close one of the doors.", cfg.GREEN)
    restriction = eq(r"x \ge 0", cfg.GREEN, cfg.FONT["section"]).move_to([-4.6, 2.5, 0])
    left_half = axes.plot(square, x_range=[-2.25, 0], color=cfg.WHITE, stroke_width=7)
    right_half = axes.plot(square, x_range=[0, 2.25], color=cfg.GREEN, stroke_width=7)
    right_glow = glow_curve(right_half, cfg.GREEN)
    paced_play(scene, FadeIn(restriction, shift=DOWN * 0.2), run_time=0.8)
    scene.remove(parabola_glow)
    scene.add(left_half, right_glow)
    paced_play(
        scene,
        FadeOut(left_half),
        FadeOut(hits[0], scale=0.6),
        run_time=1.8,
    )
    narration_wait(scene, 6.5)
    paced_play(scene, FadeOut(VGroup(level, level_tag, hits[1]), scale=0.8), run_time=0.7)

    # --- 5. Fold it, and meet the square root.
    caption = swap_caption(scene, caption, "Fold what is left across y = x.", cfg.GOLD)
    identity = DashedLine(
        axes.c2p(-1.0, -1.0),
        axes.c2p(5.0, 5.0),
        color=cfg.GOLD,
        stroke_width=4.5,
        dash_length=0.16,
        stroke_opacity=0.92,
    )
    identity_text = eq("y=x", cfg.GOLD, 46)
    identity_plate = RoundedRectangle(
        width=identity_text.width + 0.34,
        height=identity_text.height + 0.20,
        corner_radius=0.12,
        stroke_color=cfg.GOLD,
        stroke_width=1.4,
        stroke_opacity=0.38,
        fill_color=cfg.BG,
        fill_opacity=0.9,
    )
    identity_tag = VGroup(identity_plate, identity_text).move_to([4.85, 1.20, 0])
    paced_play(scene, Create(identity), FadeIn(identity_tag), run_time=1.0)
    narration_wait(scene, 3.0)

    mirrored = right_glow.copy()
    scene.add(mirrored)
    paced_play(
        scene,
        ApplyMatrix(identity_reflection_matrix(), mirrored, about_point=axes.c2p(0, 0)),
        run_time=2.8,
        rate_func=rate_functions.ease_in_out_sine,
    )
    paced_play(scene, mirrored.animate.set_color(cfg.GOLD), run_time=0.7)

    pair = VGroup(
        eq(r"f(x)=x^2,\; x \ge 0", cfg.GREEN, cfg.FONT["body"]),
        eq(r"f^{-1}(x)=\sqrt{x}", cfg.GOLD, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.45).move_to([-4.5, 0.4, 0])
    fit_width(pair, 5.6)
    pair.move_to([-4.5, 0.4, 0])
    paced_play(scene, FadeOut(restriction, scale=0.8), FadeIn(pair[0], shift=RIGHT * 0.2), run_time=0.9)
    narration_wait(scene, 2.5)
    paced_play(scene, FadeIn(pair[1], shift=RIGHT * 0.2), run_time=0.9)
    narration_wait(scene, 7.5)

    closing = bottom_caption("Narrow the inputs, and the way back appears.", cfg.GOLD)
    paced_play(scene, FadeOut(caption), FadeIn(closing, shift=UP * 0.2), run_time=0.9)
    narration_wait(scene, 6.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["10"])
