"""Scene 07 - covariance and correlation."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, equation_box, label_pill, narration_wait, paced_play, scatter_points, scene_title


class Scene07CovarianceCorrelation(Scene):
    """Show how two variables move together."""

    def construct(self) -> None:
        play_scene(self)


def _trend_line(axes: Axes, slope: float, color: str) -> Line:
    return Line(axes.c2p(-2.7, slope * -2.7), axes.c2p(2.7, slope * 2.7), color=color, stroke_width=5)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "07")
    scene.add(cinematic_background())

    title = scene_title("Relationships Live Between Columns", "covariance sees direction; correlation standardizes it").to_edge(UP, buff=0.42)
    axes_pos, dots_pos = scatter_points(slope=0.78, noise=0.48, color=cfg.CYAN)
    axes_neg, dots_neg = scatter_points(slope=-0.72, noise=0.5, seed=7, color=cfg.ORANGE)
    axes_zero, dots_zero = scatter_points(slope=0.02, noise=1.1, seed=9, color=cfg.GRAY)
    panels = VGroup(
        VGroup(axes_pos, dots_pos, _trend_line(axes_pos, 0.78, cfg.CYAN), label_pill("positive", cfg.CYAN).next_to(axes_pos, DOWN, buff=0.1)),
        VGroup(axes_neg, dots_neg, _trend_line(axes_neg, -0.72, cfg.ORANGE), label_pill("negative", cfg.ORANGE).next_to(axes_neg, DOWN, buff=0.1)),
        VGroup(axes_zero, dots_zero, _trend_line(axes_zero, 0.02, cfg.GRAY), label_pill("near zero", cfg.GRAY).next_to(axes_zero, DOWN, buff=0.1)),
    ).arrange(RIGHT, buff=0.35).scale(0.72).move_to(RIGHT * 1.65 + DOWN * 0.25)

    paced_play(scene, FadeIn(title), run_time=0.7)
    paced_play(scene, LaggedStart(*[FadeIn(panel, shift=UP * 0.15) for panel in panels], lag_ratio=0.2), run_time=1.35)
    paced_play(scene, Indicate(panels[0][2], color=cfg.WHITE), Indicate(panels[1][2], color=cfg.WHITE), Indicate(panels[2][2], color=cfg.WHITE), run_time=1.0)

    cov = equation_box(r"\mathrm{cov}(x,y)={1\over n}\sum (x_i-\mu_x)(y_i-\mu_y)", cfg.GOLD, font_size=29).move_to(LEFT * 4.45 + UP * 1.0)
    corr = equation_box(r"r={\mathrm{cov}(x,y)\over\sigma_x\sigma_y}", cfg.GREEN, font_size=36).next_to(cov, DOWN, buff=0.22)
    arrow = Arrow(cov.get_bottom(), corr.get_top(), color=cfg.GREEN, stroke_width=5, buff=0.05)
    note = label_pill("bounded from -1 to 1", cfg.GREEN, font_size=20).next_to(corr, DOWN, buff=0.14)

    paced_play(scene, panels.animate.shift(RIGHT * 0.28 + DOWN * 0.35), FadeIn(cov, shift=DOWN * 0.12), run_time=0.85)
    paced_play(scene, GrowArrow(arrow), FadeIn(corr, shift=DOWN * 0.12), FadeIn(note), run_time=0.85)
    paced_play(scene, Indicate(corr, color=cfg.WHITE), run_time=0.7)

    caption = Text("Correlation is covariance after both axes agree on scale.", font_size=31, color=cfg.WHITE, weight=BOLD)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.38)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    narration_wait(scene, 0.5)
    end_scene(scene, scene_start)
