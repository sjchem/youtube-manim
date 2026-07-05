"""Scene 08 - worked mean, variance, and standard deviation example."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, equation_box, label_pill, narration_wait, number_line_with_dots, paced_play, scene_title, vertical_marker


class Scene08WorkedMeanVariance(Scene):
    """Compute mean, variance, and standard deviation on a small dataset."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "08")
    scene.add(cinematic_background())

    title = scene_title("A Small Dataset, Fully Measured", "mean, squared deviations, variance, standard deviation").to_edge(UP, buff=0.42)
    title.scale(0.9).to_edge(UP, buff=0.25)
    values = [2, 4, 4, 4, 5, 5, 7, 9]
    line, dots = number_line_with_dots(values, x_min=0, x_max=10, length=8.8)
    VGroup(line, dots).move_to(DOWN * 1.75)
    dataset = label_pill("2, 4, 4, 4, 5, 5, 7, 9", cfg.CYAN, font_size=24).move_to(UP * 1.45)

    paced_play(scene, FadeIn(title), run_time=0.7)
    paced_play(scene, FadeIn(dataset, shift=DOWN * 0.12), Create(line), LaggedStart(*[FadeIn(dot, scale=0.3) for dot in dots], lag_ratio=0.04), run_time=1.25)

    mean_marker = vertical_marker(line, 5, r"\bar{x}=5", cfg.CYAN)
    mean_marker[1].next_to(mean_marker[0], DOWN, buff=0.12)
    mean_eq = equation_box(r"\bar{x}={2+4+4+4+5+5+7+9\over 8}=5", cfg.CYAN, font_size=36).move_to(UP * 0.55)
    paced_play(scene, FadeIn(mean_marker), FadeIn(mean_eq, shift=DOWN * 0.12), run_time=0.9)

    deviations = VGroup()
    labels = VGroup()
    for index, value in enumerate(values):
        y_offset = UP * (0.42 + 0.08 * (index % 2))
        start = line.n2p(value) + y_offset
        end = line.n2p(5) + y_offset
        color = cfg.GOLD if value != 5 else cfg.GREEN
        deviations.add(Arrow(start, end, color=color, stroke_width=3.2, buff=0.03, max_tip_length_to_length_ratio=0.18))
        if index in (0, 1, 6, 7):
            lab = MathTex(f"{value}-5", font_size=26, color=color).next_to(deviations[-1], UP, buff=0.05)
            labels.add(lab)

    paced_play(scene, LaggedStart(*[GrowArrow(arrow) for arrow in deviations], lag_ratio=0.04), FadeIn(labels), run_time=1.15)

    square_eq = equation_box(r"(2-5)^2+(4-5)^2+\cdots+(9-5)^2=32", cfg.GOLD, font_size=32).move_to(UP * 0.78)
    var_eq = equation_box(r"\sigma^2={32\over 8}=4\qquad \sigma=\sqrt{4}=2", cfg.GREEN, font_size=34).next_to(square_eq, DOWN, buff=0.16)
    paced_play(scene, Transform(mean_eq, square_eq), run_time=0.75)
    paced_play(scene, FadeOut(deviations, shift=DOWN * 0.08), FadeOut(labels, shift=DOWN * 0.08), FadeIn(var_eq, shift=UP * 0.12), run_time=0.75)

    brackets = VGroup(
        BraceBetweenPoints(line.n2p(3), line.n2p(7), color=cfg.GREEN),
        Text("about one standard deviation", font_size=22, color=cfg.GREEN, weight=BOLD),
    )
    brackets[1].set_stroke("#02111D", width=4, opacity=0.85, background=True)
    brackets[1].next_to(brackets[0], UP, buff=0.12)
    paced_play(scene, FadeOut(mean_marker, shift=DOWN * 0.08), GrowFromCenter(brackets[0]), FadeIn(brackets[1]), Indicate(var_eq, color=cfg.WHITE), run_time=0.9)

    caption = VGroup(
        Text("A formula becomes useful", font_size=28, color=cfg.WHITE, weight=BOLD),
        Text("when you can see what each term measures.", font_size=28, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.08)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.38)
    paced_play(scene, FadeIn(caption, shift=UP * 0.12), run_time=0.7)
    narration_wait(scene, 0.5)
    end_scene(scene, scene_start)
