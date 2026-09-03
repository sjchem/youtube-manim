"""Scene 12: five different quantities, one identical instruction."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    end_scene,
    eq,
    fitted_eq,
    narration_wait,
    outlined_text,
    paced_play,
)

ROWS = (
    (r"dA=f(x)\,dx", "area", cfg.CYAN),
    (r"dV=\pi r^{2}\,dx", "volume", cfg.BLUE),
    (r"ds=v(t)\,dt", "distance", cfg.GOLD),
    (r"dm=\rho(x)\,dx", "mass", cfg.ORANGE),
    (r"dP=p(x)\,dx", "probability", cfg.PURPLE),
)

# One hold per row, so the chapter's pacing is tunable in a single place.
ROW_HOLDS = (4.9, 4.9, 4.9, 4.9, 5.5)


def _icon(kind: str, colour: str) -> VGroup:
    """A 0.7-unit glyph standing for each quantity, drawn from primitives."""
    if kind == "area":
        return VGroup(Polygon([-0.34, -0.30, 0], [0.34, -0.30, 0], [0.34, 0.18, 0], [-0.34, 0.34, 0], color=colour, fill_color=colour, fill_opacity=0.45, stroke_width=3))
    if kind == "volume":
        return VGroup(
            Ellipse(width=0.68, height=0.24, color=colour, fill_color=colour, fill_opacity=0.45, stroke_width=3).shift(UP * 0.24),
            Rectangle(width=0.68, height=0.48, color=colour, fill_color=colour, fill_opacity=0.30, stroke_width=3),
            Ellipse(width=0.68, height=0.24, color=colour, fill_color=colour, fill_opacity=0.60, stroke_width=3).shift(DOWN * 0.24),
        )
    if kind == "distance":
        return VGroup(
            Line([-0.36, -0.20, 0], [0.36, -0.20, 0], color=colour, stroke_width=4),
            Arrow([-0.30, 0.16, 0], [0.34, 0.16, 0], color=colour, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.3),
        )
    if kind == "mass":
        return VGroup(
            *(
                Dot([-0.26 + 0.26 * (index % 3), -0.18 + 0.26 * (index // 3), 0], radius=0.075, color=colour)
                for index in range(6)
            )
        )
    bell = ParametricFunction(
        lambda s: np.array([s, 0.42 * np.exp(-6.0 * s * s) - 0.22, 0.0]),
        t_range=[-0.36, 0.36],
        color=colour,
        stroke_width=4,
    )
    return VGroup(bell, Line([-0.38, -0.22, 0], [0.38, -0.22, 0], color=colour, stroke_width=3).set_stroke(opacity=0.6))


class Scene12OneIdea(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "12")
    add_cinematic_background(scene)

    heading = outlined_text("the notation changes", cfg.FONT["body"], cfg.MUTED).to_edge(UP, buff=0.42)
    paced_play(scene, FadeIn(heading), run_time=0.8)

    entries = VGroup()
    for latex, kind, colour in ROWS:
        icon = _icon(kind, colour)
        formula = eq(latex, colour, cfg.FONT["section"])
        name = outlined_text(kind, cfg.FONT["small"], cfg.MUTED)
        row = VGroup(icon, formula, name).arrange(RIGHT, buff=0.55)
        entries.add(row)
    entries.arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to([0, -0.45, 0])
    if entries.height > 5.4:
        entries.scale_to_fit_height(5.4)

    for index, row in enumerate(entries):
        paced_play(scene, FadeIn(row, shift=RIGHT * 0.22), run_time=0.9)
        narration_wait(scene, ROW_HOLDS[index])

    # -- The common shape, made visible ---------------------------------------
    boxes = VGroup(*(SurroundingRectangle(row[1], color=cfg.GOLD, buff=0.16, corner_radius=0.10, stroke_width=3) for row in entries))
    paced_play(scene, LaggedStart(*(Create(box) for box in boxes), lag_ratio=0.18), run_time=1.8)
    same = outlined_text("the idea does not", cfg.FONT["body"], cfg.GOLD).move_to(heading)
    paced_play(scene, ReplacementTransform(heading, same), run_time=1.0)
    narration_wait(scene, 5.5)

    paced_play(scene, FadeOut(VGroup(entries, boxes, same)), run_time=0.8)

    statement = fitted_eq(
        r"\int \big(\text{tiny piece}\big) \;=\; \text{the whole thing}",
        cfg.WHITE,
        cfg.FONT["section"],
        width=11.6,
    ).move_to([0, 0.75, 0])
    plate = SurroundingRectangle(statement, color=cfg.CYAN, buff=0.34, corner_radius=0.18, stroke_width=3.5)
    paced_play(scene, Write(statement), Create(plate), run_time=1.8)
    narration_wait(scene, 5.1)

    verdict = bottom_caption("Break it apart, understand one piece, add everything back.", cfg.GOLD)
    paced_play(scene, FadeIn(verdict), run_time=0.9)
    narration_wait(scene, 5.1)

    end_scene(scene, started, cfg.SCENE_DURATIONS["12"])
