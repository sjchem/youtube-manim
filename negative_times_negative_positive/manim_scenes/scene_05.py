from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, narration_wait, paced_play, scene_transition
from utils.math_utils import format_signed_number


def _row(n: int, known: bool = True) -> MathTex:
    product = format_signed_number(n * -4) if known else "?"
    tex = MathTex(rf"{n}\times(-4)={product}", font_size=34)
    tex.set_color_by_tex("-", cfg.NEGATIVE)
    tex.set_color_by_tex("+", cfg.GOLD)
    return tex


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = Text("Pattern through zero", font_size=42, color=cfg.ZERO).to_edge(UP)
    paced_play(scene, FadeIn(title))

    rows = VGroup(_row(3), _row(2), _row(1), _row(0), _row(-1, False), _row(-2, False), _row(-3, False))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).shift(LEFT * 3.7 + DOWN * 0.2)
    paced_play(scene, LaggedStart(*[FadeIn(row, shift=RIGHT * 0.15) for row in rows], lag_ratio=0.11), run_time=1.5)

    arrows = VGroup()
    for i in range(6):
        arrow = Arrow(rows[i].get_right() + RIGHT * 0.25, rows[i + 1].get_right() + RIGHT * 0.25, buff=0.08, color=cfg.GOLD, stroke_width=3)
        label = Text("+4", font_size=18, color=cfg.GOLD).next_to(arrow, RIGHT, buff=0.08)
        arrows.add(VGroup(arrow, label))
    paced_play(scene, LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.08), run_time=0.9)

    filled = VGroup(_row(3), _row(2), _row(1), _row(0), _row(-1), _row(-2), _row(-3))
    filled.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(rows)
    paced_play(scene, TransformMatchingTex(rows, filled), run_time=1.25)
    paced_play(scene, Flash(filled[-1], color=cfg.GOLD), run_time=0.45)

    axes = Axes(
        x_range=[-3, 3, 1],
        y_range=[-12, 12, 4],
        x_length=3.6,
        y_length=2.4,
        axis_config={"color": cfg.MUTED, "stroke_width": 2},
    ).shift(RIGHT * 2.8 + DOWN * 0.15)
    graph = axes.plot(lambda x: -4 * x, x_range=[-3, 3], color=cfg.POSITIVE, stroke_width=5)
    dots = VGroup(*[Dot(axes.c2p(n, -4 * n), color=cfg.GOLD, radius=0.055) for n in range(-3, 4)])
    graph_label = Text("same line", font_size=24, color=cfg.POSITIVE).next_to(axes, UP, buff=0.25)
    paced_play(scene, Create(axes), Create(graph), FadeIn(dots), FadeIn(graph_label), run_time=1.2)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene05PatternThroughZero(Scene):
    def construct(self) -> None:
        play_scene(self)
