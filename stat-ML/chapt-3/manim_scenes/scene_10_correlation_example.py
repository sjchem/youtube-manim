"""Scene 10 - worked covariance and correlation example."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, equation_box, label_pill, narration_wait, paced_play, scene_title


class Scene10CorrelationExample(Scene):
    """Compute covariance terms from paired x and y values."""

    def construct(self) -> None:
        play_scene(self)


def _mini_table() -> VGroup:
    rows = [
        ("x", "1", "2", "3", "4"),
        ("y", "2", "3", "5", "6"),
        (r"x-\bar{x}", "-1.5", "-0.5", "0.5", "1.5"),
        (r"y-\bar{y}", "-2", "-1", "1", "2"),
        ("product", "3", "0.5", "0.5", "3"),
    ]
    table = VGroup()
    for row_index, row in enumerate(rows):
        for col_index, item in enumerate(row):
            color = cfg.GOLD if row_index == 4 else cfg.WHITE
            if col_index == 0:
                color = cfg.CYAN if row_index < 2 else cfg.GREEN if row_index < 4 else cfg.GOLD
            cell = MathTex(item, font_size=30, color=color)
            box = Rectangle(width=1.18, height=0.48, stroke_color=cfg.COLORS["line"], stroke_width=1.2, fill_color=cfg.COLORS["panel"], fill_opacity=0.55)
            mob = VGroup(box, cell).move_to([col_index * 1.18, -row_index * 0.48, 0])
            table.add(mob)
    table.move_to(ORIGIN)
    return table


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "10")
    scene.add(cinematic_background())

    title = scene_title("Correlation Is Standardized Co-Movement", "multiply paired deviations, then divide by scale").to_edge(UP, buff=0.42)
    title.scale(0.68).to_edge(UP, buff=0.2)
    table = _mini_table().scale(0.68).move_to(LEFT * 4.85 + UP * 0.05)

    axes = Axes(
        x_range=[0, 5, 1],
        y_range=[0, 7, 1],
        x_length=3.0,
        y_length=2.25,
        tips=False,
        axis_config={"stroke_color": cfg.MUTED, "stroke_width": 2},
    ).move_to(RIGHT * 4.45 + DOWN * 0.62)
    points = [(1, 2), (2, 3), (3, 5), (4, 6)]
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.07, color=cfg.CYAN) for x, y in points])
    trend = Line(axes.c2p(0.8, 1.7), axes.c2p(4.2, 6.2), color=cfg.GOLD, stroke_width=5)
    graph_label = label_pill("up together", cfg.GOLD, font_size=20).next_to(axes, DOWN, buff=0.12)

    paced_play(scene, FadeIn(title), run_time=0.7)
    paced_play(scene, FadeIn(table, shift=RIGHT * 0.15), Create(axes), LaggedStart(*[FadeIn(dot, scale=0.35) for dot in dots], lag_ratio=0.12), run_time=1.35)
    paced_play(scene, Create(trend), FadeIn(graph_label), run_time=0.75)

    mean_note = VGroup(
        equation_box(r"\bar{x}=2.5", cfg.CYAN, font_size=28),
        equation_box(r"\bar{y}=4", cfg.CYAN, font_size=28),
    ).arrange(RIGHT, buff=0.18).move_to(LEFT * 4.85 + UP * 1.54)
    cov = equation_box(r"\mathrm{cov}(x,y)={3+0.5+0.5+3\over4}=1.75", cfg.GOLD, font_size=24).move_to(RIGHT * 0.2 + UP * 0.9)
    corr = equation_box(r"r={1.75\over \sigma_x\sigma_y}\approx 0.98", cfg.GREEN, font_size=29).move_to(RIGHT * 0.2 + DOWN * 0.32)

    paced_play(scene, FadeIn(mean_note, shift=DOWN * 0.1), run_time=0.75)
    paced_play(scene, Indicate(table[-5:], color=cfg.GOLD), FadeIn(cov, shift=DOWN * 0.12), run_time=0.9)
    paced_play(scene, FadeIn(corr, shift=UP * 0.12), Indicate(trend, color=cfg.WHITE), run_time=0.9)

    caption = VGroup(
        Text("Positive products mean the pair moves", font_size=27, color=cfg.WHITE, weight=BOLD),
        Text("in the same direction from its centers.", font_size=27, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.08)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.38)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    narration_wait(scene, 0.55)
    end_scene(scene, scene_start)
