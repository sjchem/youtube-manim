"""Scene 13: back to the first machine, carrying everything the film built."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    boxed_statement,
    connect,
    end_scene,
    fn_axes,
    machine,
    narration_wait,
    outlined_text,
    paced_play,
    token,
)
from utils.math_utils import square
from utils.render_helpers import fit_width

ROW_Y = 0.85


class Scene13Finale(Scene):
    """One sentence, earned."""

    def construct(self) -> None:
        play_scene(self)


def _thumbnail(builder, label: str, color: str) -> VGroup:
    art = builder()
    # Fit on whichever dimension binds first, so a wide pipeline sketch and a
    # tall graph sketch both sit inside the same card.
    art.scale(min(1.3 / max(art.height, 1e-6), 2.35 / max(art.width, 1e-6)))
    frame = RoundedRectangle(
        width=2.9,
        height=2.2,
        corner_radius=0.16,
        stroke_color=color,
        stroke_width=3,
        stroke_opacity=0.7,
        fill_color=cfg.PANEL,
        fill_opacity=0.85,
    )
    art.move_to(frame.get_center() + UP * 0.24)
    tag = outlined_text(label, cfg.FONT["tiny"], color)
    fit_width(tag, 2.5)
    tag.move_to(frame.get_bottom() + UP * 0.35)
    return VGroup(frame, art, tag)


def _graph_art() -> VGroup:
    axes = fn_axes(x_range=(-2, 2, 1), y_range=(0, 4, 1), x_length=2.0, y_length=1.5)
    curve = axes.plot(square, x_range=[-1.9, 1.9], color=cfg.WHITE, stroke_width=4)
    return VGroup(axes, curve)


def _pipeline_art() -> VGroup:
    boxes = VGroup(
        *[
            RoundedRectangle(width=0.7, height=0.7, corner_radius=0.1, stroke_color=cfg.PURPLE, stroke_width=3, fill_color=cfg.PANEL_2, fill_opacity=0.9)
            for _ in range(3)
        ]
    ).arrange(RIGHT, buff=0.34)
    links = VGroup(
        *[Line(boxes[i].get_right(), boxes[i + 1].get_left(), color=cfg.PURPLE, stroke_width=3) for i in range(2)]
    )
    return VGroup(boxes, links)


def _mirror_art() -> VGroup:
    axes = fn_axes(x_range=(-2, 2, 1), y_range=(-2, 2, 1), x_length=1.8, y_length=1.8)
    line_a = axes.plot(lambda x: 1.8 * x, x_range=[-1.05, 1.05], color=cfg.CYAN, stroke_width=4)
    line_b = axes.plot(lambda x: x / 1.8, x_range=[-1.9, 1.9], color=cfg.GREEN, stroke_width=4)
    mirror = DashedLine(axes.c2p(-1.8, -1.8), axes.c2p(1.8, 1.8), color=cfg.GRAY, stroke_width=2.5, dash_length=0.1)
    return VGroup(axes, mirror, line_a, line_b)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "13")
    add_cinematic_background(scene)

    # --- 1. The very first diagram, in plain words.
    words_in = token(r"\text{input}", cfg.INPUT_COLOR, font_size=cfg.FONT["body"]).move_to([-4.9, ROW_Y, 0])
    words_box = machine("RULE", cfg.RULE_COLOR, width=3.1, height=1.9, font_size=cfg.FONT["body"]).move_to([0, ROW_Y, 0])
    words_out = token(r"\text{output}", cfg.OUTPUT_COLOR, font_size=cfg.FONT["body"]).move_to([4.9, ROW_Y, 0])
    links = VGroup(connect(words_in, words_box, cfg.INPUT_COLOR), connect(words_box, words_out, cfg.OUTPUT_COLOR))
    paced_play(scene, FadeIn(words_box, scale=0.9), run_time=0.8)
    paced_play(scene, FadeIn(words_in), FadeIn(words_out), *[GrowFromEdge(link, LEFT) for link in links], run_time=1.0)
    narration_wait(scene, 5.5)

    # --- 2. The same diagram, in symbols.
    sym_in = token("x", cfg.INPUT_COLOR).move_to([-4.9, ROW_Y, 0])
    sym_box = machine("f", cfg.RULE_COLOR, width=3.1, height=1.9, tex=True, font_size=cfg.FONT["hero"]).move_to([0, ROW_Y, 0])
    sym_out = token("f(x)", cfg.OUTPUT_COLOR).move_to([4.9, ROW_Y, 0])
    paced_play(
        scene,
        ReplacementTransform(words_in, sym_in),
        ReplacementTransform(words_box, sym_box),
        ReplacementTransform(words_out, sym_out),
        run_time=1.3,
    )
    narration_wait(scene, 5.5)

    # --- 3. Everything the film built, in one row.
    thumbs = VGroup(
        _thumbnail(_graph_art, "GRAPH", cfg.CYAN),
        _thumbnail(_pipeline_art, "COMPOSITION", cfg.PURPLE),
        _thumbnail(_mirror_art, "INVERSE", cfg.GREEN),
    ).arrange(RIGHT, buff=0.65).move_to([0, -1.85, 0])
    for thumb in thumbs:
        paced_play(scene, FadeIn(thumb, shift=UP * 0.25), run_time=0.7)
        narration_wait(scene, 2.6)
    narration_wait(scene, 4.5)

    # --- 4. The closing line.
    paced_play(
        scene,
        FadeOut(VGroup(thumbs, links, sym_in, sym_out), scale=0.85),
        sym_box.animate.scale(0.001).set_opacity(0),
        run_time=1.1,
    )
    scene.remove(sym_box)

    final = boxed_statement(r"\text{input} \rightarrow \text{rule} \rightarrow \text{output}", cfg.GOLD, cfg.FONT["title"], tex=True)
    final.move_to([0, 0.55, 0])
    tagline = outlined_text("That is a function.", cfg.FONT["section"], cfg.WHITE)
    tagline.next_to(final, DOWN, buff=0.75)
    paced_play(scene, FadeIn(final, scale=0.92), run_time=1.2)
    narration_wait(scene, 4.5)
    paced_play(scene, FadeIn(tagline, shift=UP * 0.2), run_time=0.9)
    narration_wait(scene, 7.0)
    paced_play(scene, Indicate(final, color=cfg.WHITE, scale_factor=1.03), run_time=1.0)
    narration_wait(scene, 3.5)

    end_scene(scene, started, cfg.SCENE_DURATIONS["13"])
