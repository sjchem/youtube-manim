"""Scene 08: separating the variables is a rearrangement you can watch happen."""

from __future__ import annotations

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

CENTER_Y = 0.55


class Scene08SeparationOfVariables(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "08")
    add_cinematic_background(scene)

    # -- Beat 1: the equation we already met, one step more general ----------
    start = fitted_eq(r"\frac{dy}{dx}=ky", cfg.WHITE, cfg.FONT["hero"], width=6.2).move_to([0, CENTER_Y, 0])
    paced_play(scene, Write(start), run_time=1.3)
    restriction = outlined_text("first protect  y = 0", cfg.FONT["small"], cfg.PURPLE).next_to(start, DOWN, buff=0.48)
    paced_play(scene, FadeIn(restriction, shift=UP * 0.10), run_time=0.8)
    narration_wait(scene, 6.2)

    # -- Beat 2: send each variable to its own side ---------------------------
    separated = fitted_eq(r"\frac{1}{y}\,dy=k\,dx", cfg.WHITE, cfg.FONT["hero"], width=7.6).move_to([0, CENTER_Y, 0])
    paced_play(scene, TransformMatchingShapes(start, separated), FadeOut(restriction), run_time=1.8)
    narration_wait(scene, 6.8)

    divider = Line([0, CENTER_Y + 2.55, 0], [0, CENTER_Y - 2.75, 0], color=cfg.MUTED, stroke_width=3)
    divider.set_stroke(opacity=0.55)
    left_title = outlined_text("everything about y", cfg.FONT["body"], cfg.CYAN).move_to([-3.7, CENTER_Y + 2.15, 0])
    right_title = outlined_text("everything about x", cfg.FONT["body"], cfg.GOLD).move_to([3.7, CENTER_Y + 2.15, 0])

    left_side = fitted_eq(r"\frac{1}{y}\,dy", cfg.CYAN, cfg.FONT["hero"], width=3.6).move_to([-3.7, CENTER_Y, 0])
    equals = eq("=", cfg.WHITE, cfg.FONT["hero"]).move_to([0, CENTER_Y, 0])
    right_side = fitted_eq(r"k\,dx", cfg.GOLD, cfg.FONT["hero"], width=3.0).move_to([3.7, CENTER_Y, 0])

    paced_play(scene, Create(divider), run_time=0.7)
    paced_play(
        scene,
        FadeOut(separated),
        FadeIn(left_side),
        FadeIn(equals),
        FadeIn(right_side),
        run_time=1.3,
    )
    paced_play(scene, FadeIn(left_title, shift=DOWN * 0.12), FadeIn(right_title, shift=DOWN * 0.12), run_time=0.9)
    narration_wait(scene, 8.0)

    # -- Beat 3: integrate both halves ----------------------------------------
    left_integral = fitted_eq(r"\int\frac{1}{y}\,dy", cfg.CYAN, cfg.FONT["hero"], width=4.4).move_to([-3.7, CENTER_Y, 0])
    right_integral = fitted_eq(r"\int k\,dx", cfg.GOLD, cfg.FONT["hero"], width=3.8).move_to([3.7, CENTER_Y, 0])
    paced_play(
        scene,
        ReplacementTransform(left_side, left_integral),
        ReplacementTransform(right_side, right_integral),
        run_time=1.5,
    )
    narration_wait(scene, 7.2)

    # -- Beat 4: what each side integrates to ----------------------------------
    left_result = fitted_eq(r"\ln|y|", cfg.CYAN, cfg.FONT["hero"], width=3.2).move_to([-3.7, CENTER_Y - 1.75, 0])
    right_result = fitted_eq(r"kx+C", cfg.GOLD, cfg.FONT["hero"], width=3.6).move_to([3.7, CENTER_Y - 1.75, 0])
    down_left = Arrow(left_integral.get_bottom(), left_result.get_top(), color=cfg.MUTED, buff=0.20, stroke_width=4, max_tip_length_to_length_ratio=0.28)
    down_right = Arrow(right_integral.get_bottom(), right_result.get_top(), color=cfg.MUTED, buff=0.20, stroke_width=4, max_tip_length_to_length_ratio=0.28)
    paced_play(scene, GrowArrow(down_left), GrowArrow(down_right), run_time=0.9)
    paced_play(scene, FadeIn(left_result, shift=UP * 0.12), FadeIn(right_result, shift=UP * 0.12), run_time=1.1)
    narration_wait(scene, 6.6)

    # -- Beat 5: undo the logarithm --------------------------------------------
    paced_play(
        scene,
        FadeOut(VGroup(divider, left_title, right_title, left_integral, right_integral, down_left, down_right, equals)),
        run_time=0.8,
    )
    line = fitted_eq(r"\ln|y|=kx+C", cfg.WHITE, cfg.FONT["hero"], width=8.2).move_to([0, CENTER_Y + 0.48, 0])
    paced_play(scene, ReplacementTransform(VGroup(left_result, right_result), line), run_time=1.3)
    narration_wait(scene, 6.6)

    final = fitted_eq(r"y=Ce^{kx}", cfg.GREEN, cfg.FONT["hero"], width=6.4).move_to([0, CENTER_Y - 1.15, 0])
    plate = SurroundingRectangle(final, color=cfg.GREEN, buff=0.34, corner_radius=0.18, stroke_width=3.5)
    paced_play(scene, TransformFromCopy(line, final), Create(plate), run_time=1.6)
    paced_play(scene, Indicate(final, color=cfg.WHITE, scale_factor=1.05), run_time=0.8)
    narration_wait(scene, 6.8)

    equilibrium = fitted_eq(r"C=0\quad\Longrightarrow\quad y=0", cfg.PURPLE, cfg.FONT["section"], width=5.8)
    equilibrium.next_to(plate, DOWN, buff=0.48)
    paced_play(scene, FadeIn(equilibrium, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 3.0)

    verdict = bottom_caption("The divided-out equilibrium returns when C = 0.", cfg.GOLD)
    paced_play(scene, FadeIn(verdict), run_time=0.9)
    narration_wait(scene, 5.6)

    end_scene(scene, started, cfg.SCENE_DURATIONS["08"])
