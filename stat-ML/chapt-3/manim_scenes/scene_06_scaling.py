"""Scene 06 - statistics explain feature scaling."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, equation_box, label_pill, narration_wait, paced_play, scene_title


class Scene06Scaling(Scene):
    """Show why mean and standard deviation matter for preprocessing."""

    def construct(self) -> None:
        play_scene(self)


def _feature_axis(label: str, span: str, color: str) -> VGroup:
    axis = NumberLine(x_range=[0, 10, 2], length=4.4, include_numbers=False, color=cfg.MUTED)
    dots = VGroup(*[Dot(axis.n2p(x), radius=0.07, color=color) for x in [1.0, 2.2, 2.7, 4.0, 6.4, 7.1, 8.5]])
    name = Text(label, font_size=26, color=color, weight=BOLD).next_to(axis, UP, buff=0.14)
    scale = Text(span, font_size=21, color=cfg.MUTED).next_to(axis, DOWN, buff=0.12)
    return VGroup(axis, dots, name, scale)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "06")
    scene.add(cinematic_background())

    title = scene_title("Scaling Makes Features Comparable", "same data, fairer geometry").to_edge(UP, buff=0.42)
    price = _feature_axis("house price", "$80k to $900k", cfg.GOLD).move_to(LEFT * 3.1 + UP * 0.35)
    rooms = _feature_axis("bedrooms", "1 to 6", cfg.CYAN).move_to(RIGHT * 3.1 + UP * 0.35)
    model_space = Rectangle(width=8.4, height=1.3, stroke_color=cfg.PURPLE, fill_color=cfg.COLORS["panel"], fill_opacity=0.5).move_to(DOWN * 1.72)
    model_label = Text("distance-based ML sees geometry", font_size=28, color=cfg.PURPLE, weight=BOLD).move_to(model_space)

    paced_play(scene, FadeIn(title), run_time=0.7)
    paced_play(scene, FadeIn(price, shift=RIGHT * 0.2), FadeIn(rooms, shift=LEFT * 0.2), run_time=0.95)
    paced_play(scene, FadeIn(model_space), FadeIn(model_label), run_time=0.75)

    unbalanced = Arrow(price.get_bottom(), model_space.get_left() + RIGHT * 1.1, color=cfg.ORANGE, stroke_width=8, buff=0.18)
    small = Arrow(rooms.get_bottom(), model_space.get_right() + LEFT * 1.1, color=cfg.CYAN, stroke_width=3, buff=0.18)
    warning = label_pill("large scale dominates", cfg.ORANGE).next_to(unbalanced, LEFT, buff=0.15)
    paced_play(scene, GrowArrow(unbalanced), GrowArrow(small), FadeIn(warning), run_time=0.95)

    zscore = equation_box(r"z={x-\mu\over\sigma}", cfg.GREEN, font_size=52).move_to(UP * 1.34)
    standardized = VGroup(
        _feature_axis("price z-score", "-2 to 2", cfg.GREEN),
        _feature_axis("rooms z-score", "-2 to 2", cfg.GREEN),
    ).arrange(RIGHT, buff=1.25).move_to(DOWN * 0.28)
    equal_arrows = VGroup(
        Arrow(standardized[0].get_bottom(), model_space.get_left() + RIGHT * 2.0, color=cfg.GREEN, stroke_width=5, buff=0.18),
        Arrow(standardized[1].get_bottom(), model_space.get_right() + LEFT * 2.0, color=cfg.GREEN, stroke_width=5, buff=0.18),
    )

    paced_play(scene, FadeIn(zscore, scale=0.95), run_time=0.75)
    paced_play(scene, FadeOut(price), FadeOut(rooms), FadeOut(unbalanced), FadeOut(small), FadeOut(warning), FadeIn(standardized), run_time=1.0)
    paced_play(scene, GrowArrow(equal_arrows[0]), GrowArrow(equal_arrows[1]), Indicate(model_label, color=cfg.WHITE), run_time=0.9)

    caption = Text("Mean recenters. Standard deviation rescales.", font_size=32, color=cfg.WHITE, weight=BOLD)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.42)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    narration_wait(scene, 0.5)
    end_scene(scene, scene_start)
