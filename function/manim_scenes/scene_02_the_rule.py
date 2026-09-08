"""Scene 02: the machine gets a rule, and the rule gets a notation."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    connect,
    cross_mark,
    end_scene,
    eq,
    feed_machine,
    machine,
    narration_wait,
    outlined_text,
    paced_play,
    swap_caption,
    token,
    value_table,
)
from utils.math_utils import double, format_number
from utils.render_helpers import fit_width

MACHINE_CENTER = [-3.4, 0.7, 0]
IN_X = -7.0
OUT_X = 0.3
SAMPLES = (1.0, 3.0, 5.0)


class Scene02TheRule(Scene):
    """One rule, many numbers, and finally a name for the rule."""

    def construct(self) -> None:
        play_scene(self)


def _beveled_pointer(start, end, color) -> VGroup:
    """A compact annotation arrow with shaded faces and a shallow extrusion."""
    start, end = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
    # Keep the tip anchored to its symbol while shortening the label end.
    start = start + .18 * (end - start)
    direction = (end - start) / np.linalg.norm(end - start)
    normal = np.array([-direction[1], direction[0], 0.0])
    neck = end - .23 * direction
    shaft_half, head_half = .029, .115
    outline = [start + shaft_half * normal, neck + shaft_half * normal,
               neck + head_half * normal, end, neck - head_half * normal,
               neck - shaft_half * normal, start - shaft_half * normal]
    depth = np.array([.035, -.035, 0.0])
    dark = interpolate_color(ManimColor(color), ManimColor(cfg.BG), .60)
    light = interpolate_color(ManimColor(color), WHITE, .48)
    sides = VGroup(*[
        Polygon(a, b, b + depth, a + depth, fill_color=dark,
                fill_opacity=1, stroke_width=0)
        for a, b in zip(outline, outline[1:] + outline[:1])
    ])
    face = Polygon(*outline, fill_color=color, fill_opacity=1, stroke_width=0)
    bevel = Polygon(neck, neck + head_half * normal, end,
                    fill_color=light, fill_opacity=1, stroke_width=0)
    highlight = Line(start + shaft_half * normal, neck + shaft_half * normal,
                     color=light, stroke_width=1.2, stroke_opacity=.9)
    pointer = VGroup(sides, face, bevel, highlight)
    pointer.tail = start
    return pointer


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "02")
    add_cinematic_background(scene)

    # --- 1. A machine with an actual rule inside it.
    box = machine(r"\times 2", cfg.RULE_COLOR, width=3.4, height=2.3, tex=True, font_size=cfg.FONT["title"])
    box.move_to(MACHINE_CENTER)
    caption = bottom_caption("This machine doubles whatever enters.", cfg.CYAN)
    paced_play(scene, FadeIn(box, scale=0.9), FadeIn(caption, shift=UP * 0.2), run_time=1.1)
    narration_wait(scene, 6.0)

    # --- 2. Numbers flow through, and a record of what happened builds up.
    table = value_table([(format_number(x), format_number(double(x))) for x in SAMPLES],
                        head_left=r"\text{Input}", head_right=r"\text{Output}", col_buff=0.65)
    table.move_to([4.4, 0.35, 0])
    paced_play(scene, FadeIn(table.header), Create(table.rule), Create(table[3]), run_time=1.0)

    for index, value in enumerate(SAMPLES):
        in_tok = token(format_number(value), cfg.INPUT_COLOR).move_to([IN_X, MACHINE_CENTER[1], 0])
        out_tok = token(format_number(double(value)), cfg.OUTPUT_COLOR).move_to([OUT_X, MACHINE_CENTER[1], 0])
        if index == 0:
            arrow_in = connect(in_tok, box, cfg.INPUT_COLOR)
            arrow_out = connect(box, out_tok, cfg.OUTPUT_COLOR)
            paced_play(scene, FadeIn(in_tok, shift=RIGHT * 0.35), GrowFromEdge(arrow_in, LEFT), run_time=0.8)
            scene.add(arrow_out.set_opacity(0))
            paced_play(scene, arrow_out.animate.set_opacity(1), run_time=0.4)
        else:
            paced_play(scene, FadeIn(in_tok, shift=RIGHT * 0.35), run_time=0.55)
        feed_machine(scene, box, in_tok, out_tok, run_time=1.7)
        row = table.rows[index]
        paced_play(scene, TransformFromCopy(out_tok, row, path_arc=-0.5), run_time=1.1)
        narration_wait(scene, 4.0 if index < 2 else 6.0)
        if index < len(SAMPLES) - 1:
            paced_play(scene, FadeOut(out_tok, scale=0.7), run_time=0.4)
        else:
            paced_play(scene, FadeOut(out_tok, scale=0.7), FadeOut(arrow_in), FadeOut(arrow_out), run_time=0.5)

    caption = swap_caption(scene, caption, "A rule this useful deserves a name.", cfg.GOLD)
    narration_wait(scene, 4.5)

    # --- 3. The rule becomes notation.
    named = eq("f(x)=2x", cfg.WHITE, cfg.FONT["title"])
    named.scale_to_fit_width(min(named.width, box.body.width - 0.5))
    named.move_to(box.body.get_center())
    # Lift the label out of the machine group first: ReplacementTransform can
    # only swap mobjects that sit at the top level of the scene.
    old_label = box.label.copy()
    scene.add(old_label)
    box.label.set_opacity(0)
    paced_play(
        scene,
        FadeOut(table, shift=RIGHT * 0.6),
        ReplacementTransform(old_label, named),
        run_time=1.2,
    )
    narration_wait(scene, 5.0)

    # --- 4. Anatomy of the notation, one coloured piece at a time.
    parts = MathTex("f", "(", "x", ")", "=", "2", "x", font_size=110)
    parts.set_stroke(cfg.BG, width=4, opacity=0.92, background=True)
    parts[0].set_color(cfg.RULE_COLOR)
    parts[2].set_color(cfg.INPUT_COLOR)
    parts[5].set_color(cfg.OUTPUT_COLOR)
    parts[6].set_color(cfg.OUTPUT_COLOR)
    parts.move_to([0, 1.55, 0])
    paced_play(
        scene,
        FadeOut(box, scale=0.85),
        ReplacementTransform(named, parts),
        run_time=1.2,
    )
    caption = swap_caption(scene, caption, "The rule, the input, and its output.", cfg.GOLD)

    callouts = [
        (parts[0], "the RULE", cfg.RULE_COLOR, -4.1),
        (parts[2], "the INPUT", cfg.INPUT_COLOR, 0.0),
        (VGroup(parts[5], parts[6]), "the OUTPUT", cfg.OUTPUT_COLOR, 4.1),
    ]
    labels = VGroup()
    pointers = VGroup()
    for target, text, color, x_slot in callouts:
        label = outlined_text(text, cfg.FONT["label"], color)
        fit_width(label, 3.9)
        label.move_to([x_slot, -1.35, 0])
        pointer = _beveled_pointer(
            label.get_top() + UP * 0.12,
            target.get_bottom() + DOWN * 0.16,
            color,
        )
        labels.add(label)
        pointers.add(pointer)
    for label, pointer in zip(labels, pointers):
        paced_play(scene, GrowFromPoint(pointer, pointer.tail), FadeIn(label, shift=UP * 0.18), run_time=0.85)
        narration_wait(scene, 3.8)

    # --- 5. The most common misreading, killed on sight.
    caption = swap_caption(scene, caption, "It is not multiplication.", cfg.RED)
    warning = eq(r"f(x) \neq f \times x", cfg.RED, cfg.FONT["title"])
    warning.move_to([0, -1.35, 0])
    paced_play(
        scene,
        FadeOut(labels, scale=0.85),
        FadeOut(pointers, scale=0.85),
        run_time=0.6,
    )
    paced_play(scene, Write(warning), run_time=1.1)
    narration_wait(scene, 1.0)
    narration_wait(scene, 5.5)

    meaning = outlined_text("f(x) = what f gives back when you hand it x", cfg.FONT["body"], cfg.WHITE)
    fit_width(meaning, cfg.SAFE_WIDTH - 1.0)
    meaning.move_to([0, -1.35, 0])
    paced_play(scene, ReplacementTransform(warning, meaning), run_time=1.0)
    narration_wait(scene, 6.0)

    # --- 6. Plug a number in and watch the notation do exactly what the box did.
    caption = swap_caption(scene, caption, "So hand it a 3.", cfg.GOLD)
    steps = VGroup(
        eq("f(3)", cfg.INPUT_COLOR, cfg.FONT["title"]),
        eq("=2(3)", cfg.WHITE, cfg.FONT["title"]),
        eq("=6", cfg.OUTPUT_COLOR, cfg.FONT["title"]),
    ).arrange(RIGHT, buff=0.28)
    steps.move_to([0, -1.35, 0])
    paced_play(scene, FadeOut(meaning, shift=DOWN * 0.3), run_time=0.5)
    for step in steps:
        paced_play(scene, FadeIn(step, shift=RIGHT * 0.25), run_time=0.7)
        narration_wait(scene, 2.4)
    narration_wait(scene, 5.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["02"])
