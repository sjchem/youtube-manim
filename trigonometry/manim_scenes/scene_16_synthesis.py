"""Scene 16: assemble the complete course into one connected idea."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    end_scene,
    narration_wait,
    outlined_text,
    paced_play,
)


class Scene16Synthesis(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "16")
    add_cinematic_background(scene)

    def course_card(word: str, color: str, width: float = 2.48) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=0.95,
            corner_radius=0.14,
            color=color,
            fill_color=cfg.PANEL,
            fill_opacity=0.9,
        )
        label = outlined_text(word, cfg.FONT["tiny"], color, BOLD)
        if label.width > box.width - 0.24:
            label.scale_to_fit_width(box.width - 0.24)
        return VGroup(box, label.move_to(box))

    # A serpentine map follows the narration in reading order without packing
    # long diagonal arrows through the middle of the frame.
    row_one = VGroup(*[
        course_card(word, color)
        for word, color in (
            ("TURN", cfg.GOLD),
            ("COORDINATES", cfg.GREEN),
            ("PYTHAGORAS", cfg.WHITE),
            ("TRIG RATIOS", cfg.CYAN),
            ("SPECIAL ANGLES", cfg.ORANGE),
        )
    ]).arrange(RIGHT, buff=0.25).move_to(UP * 2.55)
    row_two = VGroup(*[
        course_card(word, color)
        for word, color in (
            ("ANY TRIANGLE", cfg.GOLD),
            ("IDENTITIES", cfg.PURPLE),
            ("INVERSE", cfg.ORANGE),
            ("GRAPHS", cfg.CYAN),
            ("UNIT CIRCLE", cfg.GREEN),
        )
    ]).arrange(RIGHT, buff=0.25).move_to(UP * 0.55)
    row_three = VGroup(*[
        course_card(word, color, 3.55)
        for word, color in (("SOUND", cfg.CYAN), ("FOURIER", cfg.PURPLE), ("EULER", cfg.GOLD))
    ]).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.55)

    row_one_arrows = VGroup(*[
        Arrow(row_one[i].get_right(), row_one[i + 1].get_left(), color=cfg.MUTED, stroke_width=3.5, buff=0.06)
        for i in range(4)
    ])
    turn_down = Arrow(row_one[-1].get_bottom(), row_two[-1].get_top(), color=cfg.ORANGE, stroke_width=4, buff=0.08)
    row_two_arrows = VGroup(*[
        Arrow(row_two[i].get_left(), row_two[i - 1].get_right(), color=cfg.MUTED, stroke_width=3.5, buff=0.06)
        for i in range(4, 0, -1)
    ])
    sound_bridge = Arrow(row_two[0].get_bottom(), row_three[0].get_top(), color=cfg.CYAN, stroke_width=4, buff=0.08)
    row_three_arrows = VGroup(*[
        Arrow(row_three[i].get_right(), row_three[i + 1].get_left(), color=cfg.GOLD, stroke_width=4, buff=0.08)
        for i in range(2)
    ])

    paced_play(scene, LaggedStart(*[FadeIn(card, shift=RIGHT * 0.12) for card in row_one], lag_ratio=0.16), run_time=1.6)
    paced_play(scene, LaggedStart(*[GrowArrow(arrow) for arrow in row_one_arrows], lag_ratio=0.18), run_time=1.0)
    paced_play(scene, LaggedStart(*[Indicate(card, color=cfg.WHITE, scale_factor=1.02) for card in row_one], lag_ratio=0.18), run_time=1.2)
    paced_play(scene, GrowArrow(turn_down), LaggedStart(*[FadeIn(card, shift=LEFT * 0.12) for card in reversed(row_two)], lag_ratio=0.16), run_time=1.8)
    paced_play(scene, LaggedStart(*[GrowArrow(arrow) for arrow in row_two_arrows], lag_ratio=0.18), run_time=1.2)
    paced_play(scene, LaggedStart(*[Indicate(card, color=cfg.WHITE, scale_factor=1.02) for card in reversed(row_two)], lag_ratio=0.18), run_time=1.6)
    paced_play(scene, GrowArrow(sound_bridge), LaggedStart(*[FadeIn(card, shift=RIGHT * 0.14) for card in row_three], lag_ratio=0.22), run_time=1.4)
    paced_play(scene, LaggedStart(*[GrowArrow(arrow) for arrow in row_three_arrows], lag_ratio=0.25), run_time=1.2)
    paced_play(scene, LaggedStart(*[Indicate(card, color=cfg.WHITE, scale_factor=1.03) for card in row_three], lag_ratio=0.25), run_time=1.5)
    narration_wait(scene, 1.2)

    paced_play(
        scene,
        FadeOut(VGroup(row_one, row_two, row_three, row_one_arrows, turn_down, row_two_arrows, sound_bridge, row_three_arrows)),
        run_time=0.9,
    )
    thesis = VGroup(
        outlined_text("Trigonometry is the language of rotation", cfg.FONT["section"], cfg.WHITE, BOLD),
        outlined_text("seen through triangles, coordinates, and waves.", cfg.FONT["section"], cfg.CYAN, BOLD),
        outlined_text("MANY FORMULAS · ONE MOVING IDEA", cfg.FONT["body"], cfg.GOLD, BOLD),
    )
    for line in thesis:
        if line.width > cfg.SAFE_WIDTH - 0.5:
            line.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    thesis.arrange(DOWN, buff=0.22)
    paced_play(scene, FadeIn(thesis[0], shift=DOWN * 0.12), run_time=1.0)
    paced_play(scene, Write(thesis[1]), run_time=1.1)
    paced_play(scene, FadeIn(thesis[2], shift=UP * 0.14), run_time=0.9)
    paced_play(scene, Indicate(thesis, color=cfg.WHITE, scale_factor=1.025), run_time=1.3)
    narration_wait(scene, 2.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["16"])
