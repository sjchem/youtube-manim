"""Scene 05: a graph is nothing more than a picture of every input-output pair."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    axis_labels,
    begin_scene,
    bottom_caption,
    boxed_statement,
    connect,
    end_scene,
    eq,
    feed_machine,
    fn_axes,
    glow_curve,
    glow_dot,
    machine,
    narration_wait,
    paced_play,
    swap_caption,
    token,
    value_table,
)
from utils.math_utils import format_number, pair_tex, square

SAMPLES = (-2.0, -1.0, 0.0, 1.0, 2.0)
MACHINE_CENTER = [-3.4, 0.9, 0]


class Scene05MachineToGraph(Scene):
    """The single most important transition in the film."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "05")
    add_cinematic_background(scene)

    # --- 1. A new rule, the same picture.
    box = machine("f(x)=x^2", cfg.RULE_COLOR, width=3.2, height=2.3, tex=True, font_size=cfg.FONT["section"])
    box.move_to(MACHINE_CENTER)
    caption = bottom_caption("Feed it every number you like.", cfg.CYAN)
    paced_play(scene, FadeIn(box, scale=0.9), FadeIn(caption, shift=UP * 0.2), run_time=1.1)
    narration_wait(scene, 5.5)

    table = value_table([(format_number(x), format_number(square(x))) for x in SAMPLES], row_buff=0.3)
    table.move_to([4.9, 0.25, 0])
    paced_play(scene, FadeIn(table.header), Create(table.rule), Create(table[3]), run_time=0.9)

    out_x = MACHINE_CENTER[0] + 3.8
    for index, value in enumerate(SAMPLES):
        in_tok = token(format_number(value), cfg.INPUT_COLOR).move_to([MACHINE_CENTER[0] - 3.6, MACHINE_CENTER[1], 0])
        out_tok = token(format_number(square(value)), cfg.OUTPUT_COLOR).move_to([out_x, MACHINE_CENTER[1], 0])
        if index == 0:
            arrow_in = connect(in_tok, box, cfg.INPUT_COLOR)
            arrow_out = connect(box, out_tok, cfg.OUTPUT_COLOR)
            paced_play(scene, FadeIn(in_tok, shift=RIGHT * 0.3), GrowFromEdge(arrow_in, LEFT), run_time=0.7)
            scene.add(arrow_out)
        else:
            paced_play(scene, FadeIn(in_tok, shift=RIGHT * 0.3), run_time=0.45)
        feed_machine(scene, box, in_tok, out_tok, run_time=1.3)
        paced_play(scene, TransformFromCopy(out_tok, table.rows[index], path_arc=-0.45), run_time=0.9)
        paced_play(scene, FadeOut(out_tok, scale=0.7), run_time=0.3)
        narration_wait(scene, 1.5)

    caption = swap_caption(scene, caption, "Five inputs. Five answers. Nothing mysterious yet.", cfg.GOLD)
    narration_wait(scene, 6.0)

    # --- 2. Each row is secretly a pair of coordinates.
    caption = swap_caption(scene, caption, "Write each row as a pair.", cfg.GOLD)
    pairs = VGroup(
        *[eq(pair_tex(x, square(x)), cfg.WHITE, cfg.FONT["section"]) for x in SAMPLES]
    ).arrange(DOWN, buff=0.44)
    pairs.move_to(table.rows.get_center())
    paced_play(
        scene,
        FadeOut(box, scale=0.85),
        FadeOut(VGroup(arrow_in, arrow_out)),
        FadeOut(table.header),
        FadeOut(table.rule),
        FadeOut(table[3]),
        run_time=0.8,
    )
    paced_play(
        scene,
        LaggedStart(*[ReplacementTransform(row, pair) for row, pair in zip(table.rows, pairs)], lag_ratio=0.18),
        run_time=2.2,
    )
    narration_wait(scene, 6.5)

    # --- 3. Give the pairs somewhere to live.
    caption = swap_caption(scene, caption, "Now give every pair an address.", cfg.GOLD)
    axes = fn_axes(x_range=(-3, 3, 1), y_range=(-0.5, 5, 1), x_length=7.6, y_length=6.0)
    axes.move_to([2.5, -0.3, 0])
    axes.add_coordinates([-2, -1, 0, 1, 2], [1, 2, 3, 4], font_size=26)
    labels = axis_labels(axes, "x", "f(x)")
    paced_play(
        scene,
        pairs.animate.move_to([-5.15, 0.15, 0]),
        run_time=1.0,
    )
    paced_play(scene, Create(axes), FadeIn(labels), run_time=1.4)
    narration_wait(scene, 4.5)

    dots = VGroup()
    for pair, x in zip(pairs, SAMPLES):
        target = axes.c2p(x, square(x))
        dot = glow_dot(target, cfg.GOLD, radius=0.1)
        flying = pair.copy()
        guides = VGroup()
        if x != 0:
            guides.add(DashedLine(axes.c2p(0, 0), axes.c2p(x, 0), color=cfg.INPUT_COLOR))
            guides.add(DashedLine(axes.c2p(x, 0), target, color=cfg.OUTPUT_COLOR))
        scene.play(flying.animate.scale(0.7).move_to(target + UP * 0.55),
                   Create(guides), run_time=0.75, path_arc=-0.5)
        paced_play(scene, FadeIn(dot, scale=1.6), FadeOut(flying, scale=0.6), run_time=0.4)
        paced_play(scene, pair.animate.set_color(cfg.MUTED).set_opacity(0.5), FadeOut(guides), run_time=0.25)
        dots.add(dot)
        narration_wait(scene, 1.5)

    narration_wait(scene, 4.0)

    # --- 4. Fill in everything between them.
    caption = swap_caption(scene, caption, "Do it for every input in between.", cfg.GOLD)
    fine_inputs = np.linspace(-2.2, 2.2, 33)
    fine_dots = VGroup(
        *[Dot(axes.c2p(float(x), square(float(x))), radius=0.055, color=cfg.CYAN) for x in fine_inputs]
    )
    paced_play(scene, FadeOut(pairs, shift=LEFT * 0.5), run_time=0.6)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(dot, scale=1.8) for dot in fine_dots], lag_ratio=0.05),
        run_time=2.6,
    )
    narration_wait(scene, 4.0)

    curve = axes.plot(square, x_range=[-2.2, 2.2], color=cfg.WHITE, stroke_width=7)
    glow = glow_curve(curve, cfg.CYAN)
    paced_play(scene, FadeOut(fine_dots), Create(glow), run_time=2.4)
    narration_wait(scene, 5.5)

    # --- 5. Say what a graph actually is.
    statement = boxed_statement(r"\text{graph}=\text{every pair }(x,\,f(x))", cfg.GOLD, cfg.FONT["section"], tex=True)
    if statement.width > 6.3:
        statement.scale_to_fit_width(6.3)
    statement.move_to([-4.1, 2.5, 0])
    paced_play(scene, FadeOut(caption), FadeIn(statement, scale=0.9), run_time=1.0)
    narration_wait(scene, 5.0)

    tracer = ValueTracker(-2.2)
    moving_dot = always_redraw(
        lambda: glow_dot(axes.c2p(tracer.get_value(), square(tracer.get_value())), cfg.GOLD, radius=0.11)
    )
    x_value = DecimalNumber(-2.2, num_decimal_places=1, font_size=cfg.FONT["body"], color=cfg.GOLD)
    y_value = DecimalNumber(square(-2.2), num_decimal_places=1, font_size=cfg.FONT["body"], color=cfg.GOLD)
    readout = VGroup(eq("(", cfg.GOLD, cfg.FONT["body"]), x_value,
                    eq(",", cfg.GOLD, cfg.FONT["body"]), y_value,
                    eq(")", cfg.GOLD, cfg.FONT["body"]))
    def update_readout(mob):
        x_value.set_value(tracer.get_value())
        y_value.set_value(square(tracer.get_value()))
        mob.arrange(RIGHT, buff=0.08).move_to([-4.1, 0.2, 0])
    readout.add_updater(update_readout)
    scene.add(moving_dot, readout)
    paced_play(scene, tracer.animate.set_value(2.2), run_time=5.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 3.0)
    # Freeze the tracked mobjects so the closing fade is not fought by updaters.
    moving_dot.clear_updaters()
    readout.clear_updaters()

    end_scene(scene, started, cfg.SCENE_DURATIONS["05"])
