"""Scene 15: the closing revelation — a rule for change becomes a future."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    chip,
    end_scene,
    fitted_eq,
    narration_wait,
    outlined_text,
    paced_play,
    title_card,
)

CHAIN = (
    ("tiny change", cfg.CYAN),
    ("accumulation", cfg.BLUE),
    ("equation of change", cfg.GOLD),
    ("future evolution", cfg.GREEN),
)
CLOSING = (
    ("Derivatives say how the world is changing now.", cfg.CYAN),
    ("Integrals add those changes up.", cfg.BLUE),
    ("Differential equations turn both into what happens next.", cfg.GREEN),
)


class Scene15Synthesis(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "15")
    add_cinematic_background(scene)

    # -- Beat 1: the question we opened with -----------------------------------
    question_1 = outlined_text("If we only know how something changes,", cfg.FONT["title"], cfg.WHITE)
    question_2 = outlined_text("can we recover the thing itself?", cfg.FONT["title"], cfg.GOLD)
    question = VGroup(question_1, question_2).arrange(DOWN, buff=0.34).move_to([0, 0.55, 0])
    if question.width > cfg.SAFE_WIDTH:
        question.scale_to_fit_width(cfg.SAFE_WIDTH)
    paced_play(scene, FadeIn(question_1, shift=UP * 0.12), run_time=1.1)
    paced_play(scene, FadeIn(question_2, shift=UP * 0.12), run_time=1.1)
    narration_wait(scene, 6.4)

    yes = outlined_text("yes", cfg.FONT["hero"], cfg.GREEN).next_to(question, DOWN, buff=0.75)
    paced_play(scene, FadeIn(yes, scale=1.25), run_time=1.0)
    narration_wait(scene, 5.6)
    paced_play(scene, FadeOut(VGroup(question, yes)), run_time=0.7)

    # -- Beat 2: local rule + initial state = accumulated future ---------------
    rule_card = VGroup(
        fitted_eq(r"\frac{dy}{dt}=f(y,t)", cfg.CYAN, cfg.FONT["title"], width=5.2),
        outlined_text("the local rule", cfg.FONT["small"], cfg.MUTED),
    ).arrange(DOWN, buff=0.34).move_to([-3.6, 2.15, 0])
    state_card = VGroup(
        fitted_eq(r"y(t_0)=y_0", cfg.GOLD, cfg.FONT["title"], width=4.5),
        outlined_text("the starting state", cfg.FONT["small"], cfg.MUTED),
    ).arrange(DOWN, buff=0.34).move_to([3.6, 2.15, 0])
    paced_play(scene, FadeIn(rule_card, shift=UP * 0.12), run_time=1.0)
    narration_wait(scene, 5.7)
    paced_play(scene, FadeIn(state_card, shift=UP * 0.12), run_time=1.0)
    narration_wait(scene, 5.7)

    unified = fitted_eq(
        r"y(t)=y_0+\int_{t_0}^{t}f\!\left(y(\tau),\tau\right)\,d\tau",
        cfg.GREEN,
        cfg.FONT["title"],
        width=11.8,
    ).move_to([0, -0.65, 0])
    unified_plate = SurroundingRectangle(unified, color=cfg.GREEN, buff=0.36, corner_radius=0.18, stroke_width=3.5)
    unified_note = outlined_text("starting state + accumulated change", cfg.FONT["body"], cfg.GREEN)
    unified_note.next_to(unified_plate, DOWN, buff=0.48)
    arrows_to_future = VGroup(
        Arrow(rule_card.get_bottom(), unified_plate.get_top() + LEFT * 2.1, color=cfg.CYAN, buff=0.20, stroke_width=4),
        Arrow(state_card.get_bottom(), unified_plate.get_top() + RIGHT * 2.1, color=cfg.GOLD, buff=0.20, stroke_width=4),
    )
    paced_play(scene, GrowArrow(arrows_to_future[0]), GrowArrow(arrows_to_future[1]), Write(unified), Create(unified_plate), run_time=2.2)
    paced_play(scene, FadeIn(unified_note, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 13.0)
    paced_play(scene, FadeOut(VGroup(rule_card, state_card, arrows_to_future, unified, unified_plate, unified_note)), run_time=0.7)

    # -- Beat 3: the arc of the whole episode ------------------------------------
    chips = VGroup(*(chip(word, colour, cfg.FONT["small"]) for word, colour in CHAIN))
    chips.arrange(RIGHT, buff=0.72)
    if chips.width > cfg.SAFE_WIDTH:
        chips.scale_to_fit_width(cfg.SAFE_WIDTH)
    arrows = VGroup(
        *(
            Arrow(chips[i].get_right(), chips[i + 1].get_left(), color=cfg.GOLD, buff=0.12, stroke_width=5, max_tip_length_to_length_ratio=0.34)
            for i in range(len(chips) - 1)
        )
    )
    chain = VGroup(chips, arrows).move_to([0, 1.35, 0])
    paced_play(
        scene,
        LaggedStart(
            FadeIn(chips[0]), GrowArrow(arrows[0]), FadeIn(chips[1]), GrowArrow(arrows[1]),
            FadeIn(chips[2]), GrowArrow(arrows[2]), FadeIn(chips[3]),
            lag_ratio=0.38,
        ),
        run_time=4.4,
    )
    narration_wait(scene, 9.8)

    # -- Beat 4: three sentences to leave with ------------------------------------
    lines = VGroup(*(outlined_text(text, cfg.FONT["body"], colour) for text, colour in CLOSING))
    lines.arrange(DOWN, buff=0.36).move_to([0, -1.55, 0])
    if lines.width > cfg.SAFE_WIDTH:
        lines.scale_to_fit_width(cfg.SAFE_WIDTH)
    for line in lines:
        paced_play(scene, FadeIn(line, shift=UP * 0.1), run_time=0.9)
        narration_wait(scene, 5.2)

    paced_play(scene, FadeOut(VGroup(chain, lines)), run_time=0.8)

    # -- Beat 5: the sentence worth remembering -------------------------------------
    punch_1 = outlined_text("A differential equation does not tell you where a system is.", cfg.FONT["body"], cfg.MUTED)
    punch_2 = outlined_text("It tells you how it must move —", cfg.FONT["body"], cfg.WHITE)
    punch_3 = outlined_text("and calculus turns that rule into its future.", cfg.FONT["body"], cfg.GOLD)
    punch = VGroup(punch_1, punch_2, punch_3).arrange(DOWN, buff=0.32).move_to([0, 0.35, 0])
    if punch.width > cfg.SAFE_WIDTH:
        punch.scale_to_fit_width(cfg.SAFE_WIDTH)
    paced_play(scene, FadeIn(punch_1), run_time=0.9)
    paced_play(scene, FadeIn(punch_2, shift=UP * 0.1), run_time=0.9)
    paced_play(scene, FadeIn(punch_3, shift=UP * 0.1), run_time=1.0)
    paced_play(scene, Indicate(punch_3, color=cfg.WHITE, scale_factor=1.04), run_time=0.9)
    narration_wait(scene, 10.3)

    paced_play(scene, FadeOut(punch), run_time=0.7)
    sign_off = title_card("VISUAL CALCULUS", "From Integrals to Differential Equations", cfg.GOLD)
    paced_play(scene, FadeIn(sign_off, shift=UP * 0.12), run_time=1.3)
    narration_wait(scene, 5.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["15"])
