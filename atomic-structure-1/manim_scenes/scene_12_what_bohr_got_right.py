"""Scene 12: the same four questions, put to both models."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    check_mark,
    cross_mark,
    end_scene,
    eq,
    equation_card,
    fit_width,
    narration_wait,
    outlined_text,
    paced_play,
    top_caption,
)
from utils.physics_models import HydrogenAtom

HYDROGEN = HydrogenAtom()
QUESTIONS = ("a tiny nucleus", "mostly empty space", "an atom that lasts", "hydrogen's lines")
RUTHERFORD_ANSWERS = (True, True, False, False)
BOHR_ANSWERS = (True, True, True, True)

PANEL_WIDTH = 6.55
ROW_YS = (1.55, 0.55, -0.45, -1.45)


def _panel(title: str, color: str, center_x: float) -> VGroup:
    plate = RoundedRectangle(
        width=PANEL_WIDTH, height=4.55, corner_radius=0.22,
        color=color, stroke_width=3, stroke_opacity=0.65,
        fill_color=cfg.PANEL, fill_opacity=0.82,
    ).move_to([center_x, 0.30, 0])
    heading = outlined_text(title, cfg.FONT["body"], color, BOLD).move_to([center_x, 2.10, 0])
    return VGroup(plate, heading)


def _row(question: str, passed: bool, center_x: float, y: float) -> tuple[VGroup, VMobject]:
    mark = check_mark(0.20, cfg.GREEN) if passed else cross_mark(0.18, cfg.RED)
    mark.move_to([center_x - PANEL_WIDTH / 2 + 0.62, y, 0])
    label = fit_width(outlined_text(question, 30, "#EBD9B4" if passed else "#BCC9D5", BOLD),
                      PANEL_WIDTH - 1.65)
    # Left-aligned against a shared margin, so four rows of different lengths
    # read as a list rather than as four separately centred phrases.
    label.move_to([center_x - PANEL_WIDTH / 2 + 1.20 + label.width / 2, y, 0])
    return VGroup(mark, label), mark


class Scene12WhatBohrGotRight(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "12")
    add_cinematic_background(scene)

    heading = top_caption("SAME FOUR QUESTIONS", cfg.GOLD)
    paced_play(scene, FadeIn(heading), run_time=0.7)

    left_x, right_x = -3.72, 3.72
    left_panel = _panel("RUTHERFORD", cfg.CYAN, left_x)
    right_panel = _panel("BOHR", cfg.GREEN, right_x)
    paced_play(scene, FadeIn(left_panel, shift=RIGHT * 0.2), run_time=1.0)
    narration_wait(scene, 3.4)

    # -- Beat 1: Rutherford's report card --------------------------------------
    left_rows = []
    left_marks = []
    for question, passed, y in zip(QUESTIONS, RUTHERFORD_ANSWERS, ROW_YS):
        row, mark = _row(question, passed, left_x, y)
        left_rows.append(row)
        left_marks.append(mark)
        paced_play(scene, FadeIn(row, shift=RIGHT * 0.15), run_time=0.8)
        narration_wait(scene, 3.8)

    paced_play(
        scene,
        LaggedStart(*[Indicate(mark, color=cfg.RED, scale_factor=1.4) for mark in left_marks[2:]], lag_ratio=0.3),
        run_time=1.4,
    )
    narration_wait(scene, 5.6)

    # -- Beat 2: the same questions, asked of Bohr -----------------------------
    paced_play(scene, FadeIn(right_panel, shift=LEFT * 0.2), run_time=1.0)
    right_rows = []
    for question, passed, y in zip(QUESTIONS, BOHR_ANSWERS, ROW_YS):
        row, _mark = _row(question, passed, right_x, y)
        right_rows.append(row)

    for index, row in enumerate(right_rows):
        paced_play(scene, FadeIn(row, shift=LEFT * 0.15), run_time=0.8)
        if index >= 2:
            paced_play(scene, Indicate(row[0], color=cfg.WHITE, scale_factor=1.5), run_time=0.7)
            narration_wait(scene, 4.6)
        else:
            narration_wait(scene, 2.6)

    narration_wait(scene, 4.6)

    # -- Beat 3: where those energies come from --------------------------------
    everything = VGroup(left_panel, right_panel, *left_rows, *right_rows)
    paced_play(scene, everything.animate.scale(0.70).to_edge(UP, buff=0.60), FadeOut(heading), run_time=1.1)

    formula = equation_card(r"E_n \propto -\frac{1}{n^{2}}", cfg.WHITE, cfg.FONT["title"])
    formula.move_to([-3.15, -2.45, 0])
    paced_play(scene, FadeIn(formula, scale=1.1), run_time=1.1)

    values = VGroup(
        eq(rf"E_1 = {HYDROGEN.energy_ev(1):.1f}\ \text{{eV}}", cfg.CYAN, cfg.FONT["small"]),
        eq(rf"E_2 = {HYDROGEN.energy_ev(2):.2f}\ \text{{eV}}", cfg.CYAN, cfg.FONT["small"]),
        eq(rf"E_3 = {HYDROGEN.energy_ev(3):.2f}\ \text{{eV}}", cfg.CYAN, cfg.FONT["small"]),
    ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([3.55, -2.45, 0])
    paced_play(scene, LaggedStart(*[FadeIn(line, shift=LEFT * 0.15) for line in values], lag_ratio=0.35), run_time=2.0)
    narration_wait(scene, 14.5)

    # -- Beat 4: the idea worth keeping ----------------------------------------
    paced_play(scene, FadeOut(everything, formula, values), run_time=0.8)
    idea = outlined_text("ENERGY COMES IN STEPS", cfg.FONT["hero"], cfg.PURPLE)
    fit_width(idea)
    idea.move_to([0, 0.65, 0])
    gloss = outlined_text("that one idea rebuilt the atom", cfg.FONT["body"], cfg.WHITE).move_to([0, -1.15, 0])
    paced_play(scene, FadeIn(idea, scale=1.1), run_time=1.1)
    paced_play(scene, FadeIn(gloss, shift=UP * 0.15), run_time=0.8)
    narration_wait(scene, 6.4)

    end_scene(scene, started, cfg.SCENE_DURATIONS["12"])
