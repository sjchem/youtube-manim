"""Scene 04: domain and range, discovered from a physical question."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    cross_mark,
    end_scene,
    eq,
    glow_dot,
    machine,
    narration_wait,
    outlined_text,
    paced_play,
    swap_caption,
    token,
)
from utils.math_utils import circle_area, format_number
from utils.render_helpers import fit_width

# Sized so that even the largest radius in the sweep (r = 3) stops well
# short of the input number line that starts at x = -1.1.
CIRCLE_CENTER = np.array([-4.6, 0.35, 0.0])
UNIT = 0.8


class Scene04DomainRange(Scene):
    """A circle grows, and the allowed inputs draw their own boundary."""

    def construct(self) -> None:
        play_scene(self)


def _number_line(label_tex: str, color: str, y: float, x_min: float, x_max: float, step: float = 1) -> VGroup:
    line = NumberLine(
        x_range=[x_min, x_max, step],
        length=7.4,
        color=cfg.MUTED,
        stroke_width=3,
        include_numbers=False,
        include_ticks=True,
    )
    line.move_to([2.6, y, 0])
    label = eq(label_tex, color, cfg.FONT["body"]).next_to(line, LEFT, buff=0.35)
    group = VGroup(line, label)
    group.line = line
    group.label = label
    return group


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "04")
    add_cinematic_background(scene)

    def checkpoint(name: str) -> None:
        callback = getattr(scene, "_scene04_review", None)
        if callback:
            callback(scene, name, float(scene.time) - started)

    radius = ValueTracker(1.2)

    disc = always_redraw(
        lambda: Circle(
            radius=radius.get_value() * UNIT,
            color=cfg.CYAN,
            stroke_width=5,
            fill_color=cfg.BLUE,
            fill_opacity=0.22,
        ).move_to(CIRCLE_CENTER)
    )
    spoke = always_redraw(
        lambda: Line(
            CIRCLE_CENTER,
            CIRCLE_CENTER + RIGHT * radius.get_value() * UNIT,
            color=cfg.GOLD,
            stroke_width=5,
        )
    )
    radius_value = DecimalNumber(radius.get_value(), num_decimal_places=2, font_size=cfg.FONT["body"], color=cfg.GOLD)
    spoke_label = VGroup(eq("r=", cfg.GOLD, cfg.FONT["body"]), radius_value).arrange(RIGHT, buff=0.08)
    def update_radius(mob):
        radius_value.set_value(radius.get_value())
        # Follow the outside edge of the changing circle. Keeping the readout
        # below the circumference prevents the text from touching the arc at
        # small radii and keeps it clear while the circle grows.
        label_y = CIRCLE_CENTER[1] - radius.get_value() * UNIT - 0.34
        mob.arrange(RIGHT, buff=0.08).move_to([CIRCLE_CENTER[0], label_y, 0])
    spoke_label.add_updater(update_radius)
    area_value = DecimalNumber(circle_area(radius.get_value()), num_decimal_places=2, font_size=cfg.FONT["body"], color=cfg.GREEN)
    area_label = VGroup(eq("A=", cfg.GREEN, cfg.FONT["body"]), area_value).arrange(RIGHT, buff=0.08)
    def update_area(mob):
        area_value.set_value(circle_area(radius.get_value()))
        mob.arrange(RIGHT, buff=0.08).move_to(CIRCLE_CENTER + UP * 3.0)
    area_label.add_updater(update_area)
    rule = eq(r"A(r)=\pi r^2", cfg.WHITE, cfg.FONT["title"]).move_to([3.3, 2.7, 0])

    caption = bottom_caption("Radius in. Area out.", cfg.CYAN)
    paced_play(scene, Create(disc), Create(spoke), run_time=1.2)
    paced_play(scene, FadeIn(spoke_label), FadeIn(area_label), Write(rule), FadeIn(caption), run_time=1.1)
    checkpoint("01_radius_label")
    narration_wait(scene, 6.5)

    # --- Two number lines: what goes in, what comes out.
    input_line = _number_line("r", cfg.INPUT_COLOR, 0.35, -3, 4)
    output_line = _number_line("A", cfg.OUTPUT_COLOR, -1.9, -30, 40, 10)
    input_dot = always_redraw(lambda: glow_dot(input_line.line.n2p(radius.get_value()), cfg.INPUT_COLOR))
    output_dot = always_redraw(
        lambda: glow_dot(output_line.line.n2p(circle_area(radius.get_value())), cfg.OUTPUT_COLOR)
    )
    paced_play(
        scene,
        Create(input_line.line),
        Create(output_line.line),
        FadeIn(input_line.label),
        FadeIn(output_line.label),
        run_time=1.2,
    )
    scale_labels = VGroup()
    for line, values in ((input_line.line, (0, 2, 4)), (output_line.line, (0, 20, 40))):
        for value in values:
            scale_labels.add(eq(str(value), cfg.MUTED, cfg.FONT["tiny"]).next_to(line.n2p(value), DOWN, buff=0.15))
    scene.add(input_dot, output_dot, scale_labels)
    paced_play(scene, radius.animate.set_value(3.0), run_time=3.4, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.5)
    paced_play(scene, radius.animate.set_value(0.5), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.5)
    paced_play(scene, radius.animate.set_value(2.0), run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 5.0)

    # --- The physical question that defines the domain.
    caption = swap_caption(scene, caption, "Can the radius be minus three metres?", cfg.RED)
    # Centre the rejected value in the open region below the formula, leaving
    # a clear gap above the input number line.
    bad_token = token("r=-3", cfg.RED).move_to([3.3, 1.35, 0])
    paced_play(scene, FadeIn(bad_token, shift=DOWN * 0.3), run_time=0.8)
    checkpoint("02_negative_radius")
    narration_wait(scene, 5.5)
    reject = cross_mark(cfg.RED, scale=1.5).move_to(bad_token.get_center())
    paced_play(scene, FadeIn(reject, scale=1.7), Flash(bad_token, color=cfg.RED, line_length=0.4), run_time=0.8)
    narration_wait(scene, 5.5)
    paced_play(scene, FadeOut(VGroup(bad_token, reject), scale=0.75), run_time=0.6)

    # --- Paint the allowed inputs, then the outputs they can reach.
    caption = swap_caption(scene, caption, "The allowed inputs: the domain.", cfg.GOLD)
    domain_band = Line(
        input_line.line.n2p(0),
        input_line.line.n2p(4),
        color=cfg.GREEN,
        stroke_width=13,
        stroke_opacity=0.55,
    )
    domain_tex = eq(r"r \ge 0", cfg.GREEN, cfg.FONT["body"]).next_to(input_line.line, UP, buff=0.3).shift(RIGHT * 1.2)
    paced_play(scene, Create(domain_band), run_time=1.0)
    paced_play(scene, FadeIn(domain_tex, shift=UP * 0.2), run_time=0.7)
    narration_wait(scene, 6.5)

    caption = swap_caption(scene, caption, "The outputs it can reach: the range.", cfg.GOLD)
    range_band = Line(
        output_line.line.n2p(0),
        output_line.line.n2p(40),
        color=cfg.GREEN,
        stroke_width=13,
        stroke_opacity=0.55,
    )
    range_tex = eq(r"A \ge 0", cfg.GREEN, cfg.FONT["body"]).next_to(output_line.line, UP, buff=0.3).shift(RIGHT * 1.2)
    paced_play(scene, Create(range_band), run_time=1.0)
    paced_play(scene, FadeIn(range_tex, shift=DOWN * 0.2), run_time=0.7)
    narration_wait(scene, 6.5)

    # --- Say it once, plainly, as one diagram.
    scene.remove(input_dot, output_dot, disc, spoke, spoke_label, area_label)
    stale = VGroup(scale_labels, input_line, output_line, domain_band, range_band, domain_tex, range_tex, rule)
    caption = swap_caption(scene, caption, "Every function carries both.", cfg.GOLD)

    domain_box = machine("DOMAIN", cfg.INPUT_COLOR, width=3.6, height=1.6, font_size=cfg.FONT["body"])
    rule_box = machine("f", cfg.RULE_COLOR, width=2.4, height=1.6, tex=True, font_size=cfg.FONT["title"])
    range_box = machine("RANGE", cfg.OUTPUT_COLOR, width=3.6, height=1.6, font_size=cfg.FONT["body"])
    chain = VGroup(domain_box, rule_box, range_box).arrange(RIGHT, buff=1.05).move_to([0, 1.1, 0])
    links = VGroup(
        Arrow(domain_box.get_right(), rule_box.get_left(), color=cfg.CYAN, stroke_width=6, buff=0.14, max_tip_length_to_length_ratio=0.3),
        Arrow(rule_box.get_right(), range_box.get_left(), color=cfg.CYAN, stroke_width=6, buff=0.14, max_tip_length_to_length_ratio=0.3),
    )
    paced_play(scene, FadeOut(stale, scale=0.85), run_time=0.8)
    paced_play(scene, FadeIn(chain, scale=0.92), *[GrowArrow(link) for link in links], run_time=1.2)

    definitions = VGroup(
        outlined_text("DOMAIN  =  the inputs you are allowed to use", cfg.FONT["label"], cfg.INPUT_COLOR),
        outlined_text("RANGE  =  the outputs that actually come out", cfg.FONT["label"], cfg.OUTPUT_COLOR),
    ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    for line in definitions:
        fit_width(line, cfg.SAFE_WIDTH - 1.4)
    definitions.move_to([0, -1.5, 0])
    for line in definitions:
        paced_play(scene, FadeIn(line, shift=RIGHT * 0.25), run_time=0.8)
        narration_wait(scene, 5.0)

    everyday = VGroup(
        eq(r"\text{time}\rightarrow\text{position}", cfg.CYAN, cfg.FONT["small"]),
        eq(r"\text{Celsius}\rightarrow\text{Fahrenheit}", cfg.CYAN, cfg.FONT["small"]),
        eq(r"\text{radius}\rightarrow\text{area}", cfg.CYAN, cfg.FONT["small"]),
    ).arrange(RIGHT, buff=0.9).move_to([0, -3.05, 0])
    fit_width(everyday, cfg.SAFE_WIDTH - 0.8)
    paced_play(scene, FadeOut(caption), LaggedStart(*[FadeIn(item, shift=UP * 0.2) for item in everyday], lag_ratio=0.3), run_time=1.6)
    narration_wait(scene, 4.8)

    end_scene(scene, started, cfg.SCENE_DURATIONS["04"])
