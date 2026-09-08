"""Scene 12: the same three boxes, wearing every disguise mathematics has."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    connect,
    end_scene,
    eq,
    flow_arrow,
    machine,
    narration_wait,
    outlined_text,
    paced_play,
    swap_caption,
    token,
)
from utils.render_helpers import fit_width

ROW_Y = 1.15


class Scene12WhyItMatters(Scene):
    """Physics, statistics and machine learning are the same diagram relabelled."""

    def construct(self) -> None:
        play_scene(self)


def _trio(in_tex: str, rule_tex: str, out_tex: str, colors=(cfg.INPUT_COLOR, cfg.RULE_COLOR, cfg.OUTPUT_COLOR)) -> tuple:
    in_tok = token(in_tex, colors[0]).move_to([-4.7, ROW_Y, 0])
    box = machine(rule_tex, colors[1], width=3.2, height=1.9, tex=True, font_size=cfg.FONT["body"])
    box.move_to([0, ROW_Y, 0])
    out_tok = token(out_tex, colors[2]).move_to([4.7, ROW_Y, 0])
    arrows = VGroup(connect(in_tok, box, colors[0]), connect(box, out_tok, colors[2]))
    return in_tok, box, out_tok, arrows


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "12")
    add_cinematic_background(scene)

    caption = bottom_caption("Now change nothing but the labels.", cfg.CYAN)
    in_tok, box, out_tok, arrows = _trio("x", "f", "f(x)")
    heading = outlined_text("THE SAME DIAGRAM", cfg.FONT["body"], cfg.GOLD).move_to([0, 3.15, 0])
    paced_play(scene, FadeIn(box, scale=0.9), FadeIn(caption), FadeIn(heading, shift=DOWN * 0.2), run_time=1.1)
    paced_play(scene, FadeIn(in_tok), FadeIn(out_tok), *[GrowFromEdge(a, LEFT) for a in arrows], run_time=1.0)
    narration_wait(scene, 5.0)

    disguises = [
        ("PHYSICS", "t", "x", "x(t)", cfg.GREEN, "Time in. Position out."),
        ("CALCULUS", "x(t)", r"\dfrac{d}{dt}", r"\dfrac{dx}{dt}", cfg.CYAN, "A function in. Its rate of change out."),
        ("STATISTICS", "x", "p", r"P(Y=1\mid x)", cfg.BLUE, "Data in. A probability out."),
        ("MACHINE LEARNING", r"\mathbf{x}", r"f_\theta", r"\hat{y}", cfg.PURPLE, "Features in. A prediction out."),
    ]

    # The field changes; gold inputs, cyan rules and green outputs stay stable.
    current = (in_tok, box, out_tok, arrows)
    current_heading = heading
    for name, in_tex, rule_tex, out_tex, color, line in disguises:
        new_heading = outlined_text(name, cfg.FONT["body"], color).move_to([0, 3.15, 0])
        new_in, new_box, new_out, new_arrows = _trio(in_tex, rule_tex, out_tex)
        paced_play(
            scene,
            ReplacementTransform(current[0], new_in),
            ReplacementTransform(current[1], new_box),
            ReplacementTransform(current[2], new_out),
            ReplacementTransform(current[3], new_arrows),
            ReplacementTransform(current_heading, new_heading),
            run_time=1.2,
        )
        caption = swap_caption(scene, caption, line, color)
        narration_wait(scene, 6.3)
        current = (new_in, new_box, new_out, new_arrows)
        current_heading = new_heading

    # --- A neural network is the pipeline chapter, repeated.
    caption = swap_caption(scene, caption, "A neural network is that, in a row.", cfg.PURPLE)
    net_heading = outlined_text("NEURAL NETWORK", cfg.FONT["body"], cfg.PURPLE).move_to([0, 3.15, 0])
    paced_play(
        scene,
        FadeOut(VGroup(*current), scale=0.85),
        ReplacementTransform(current_heading, net_heading),
        run_time=0.9,
    )

    boxes = VGroup(
        *[
            machine(f"f_{index}", cfg.PURPLE, width=1.9, height=1.5, tex=True, font_size=cfg.FONT["body"])
            for index in (1, 2, 3)
        ]
    ).arrange(RIGHT, buff=1.35).move_to([0.35, ROW_Y - 0.2, 0])
    x_in = token(r"\mathbf{x}", cfg.INPUT_COLOR).move_to([-5.6, ROW_Y - 0.2, 0])
    y_out = token(r"\hat{y}", cfg.OUTPUT_COLOR).move_to([5.6, ROW_Y - 0.2, 0])
    links = VGroup(
        connect(x_in, boxes[0], cfg.INPUT_COLOR, width=5),
        connect(boxes[0], boxes[1], cfg.PURPLE, width=5),
        connect(boxes[1], boxes[2], cfg.PURPLE, width=5),
        connect(boxes[2], y_out, cfg.OUTPUT_COLOR, width=5),
    )
    paced_play(scene, FadeIn(x_in), LaggedStart(*[FadeIn(b, scale=0.9) for b in boxes], lag_ratio=0.25), FadeIn(y_out), run_time=1.6)
    paced_play(scene, LaggedStart(*[GrowFromEdge(link, LEFT) for link in links], lag_ratio=0.2), run_time=1.6)

    pulse = Dot(x_in.get_center(), radius=0.13, color=cfg.GOLD)
    scene.add(pulse)
    for stop in [boxes[0], boxes[1], boxes[2], y_out]:
        paced_play(scene, pulse.animate.move_to(stop.get_center()), run_time=0.8, rate_func=rate_functions.ease_in_out_sine)
    paced_play(scene, FadeOut(pulse, scale=0.5), run_time=0.4)
    narration_wait(scene, 7.0)

    composition_note = eq(r"\hat{y}=f_3\big(f_2(f_1(\mathbf{x}))\big)", cfg.WHITE, cfg.FONT["section"])
    fit_width(composition_note, cfg.SAFE_WIDTH - 2.0)
    composition_note.move_to([0, -1.5, 0])
    paced_play(scene, FadeIn(composition_note, shift=UP * 0.2), run_time=1.0)
    narration_wait(scene, 6.0)

    # Return to the opening hub: these are applications, not a prerequisite chain.
    caption = swap_caption(scene, caption, "Different questions about functions.", cfg.GOLD)
    paced_play(scene, FadeOut(VGroup(boxes, x_in, y_out, links, composition_note, net_heading)), run_time=0.9)
    hub = machine("FUNCTION", cfg.RULE_COLOR, width=3.7, height=1.6, font_size=cfg.FONT["body"])
    hub.move_to([-4, 0.3, 0])
    paced_play(scene, FadeIn(hub), run_time=0.8)
    for index, label in enumerate(["CALCULUS", "PHYSICS", "STATISTICS", "MACHINE LEARNING", "AI"]):
        chip = outlined_text(label, cfg.FONT["small"], cfg.WHITE)
        chip.move_to([3.2, 2.6 - index * 1.25, 0]).align_to([1, 0, 0], LEFT)
        arrow = flow_arrow(hub.get_right() + RIGHT * 0.15, chip.get_left() + LEFT * 0.2, cfg.CYAN, 4)
        paced_play(scene, GrowFromEdge(arrow, LEFT), FadeIn(chip), run_time=0.8)
        narration_wait(scene, 2.2)
    narration_wait(scene, 6.2)
    end_scene(scene, started, cfg.SCENE_DURATIONS["12"])
