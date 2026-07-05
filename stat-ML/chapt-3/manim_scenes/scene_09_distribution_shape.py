"""Scene 09 - histogram shape, skew, and IQR."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, equation_box, label_pill, narration_wait, paced_play, scene_title


class Scene09DistributionShape(Scene):
    """Compare histograms with similar center but different shape."""

    def construct(self) -> None:
        play_scene(self)


def _histogram(counts: list[int], color: str, label: str) -> VGroup:
    bars = VGroup()
    max_count = max(counts)
    for index, count in enumerate(counts):
        height = 2.25 * count / max_count
        bar = Rectangle(
            width=0.38,
            height=height,
            fill_color=color,
            fill_opacity=0.72,
            stroke_color=cfg.WHITE,
            stroke_opacity=0.38,
            stroke_width=1,
        )
        bar.move_to([index * 0.46, height / 2, 0])
        bars.add(bar)
    bars.move_to(ORIGIN)
    axis = Line(LEFT * 0.35, RIGHT * (0.46 * (len(counts) - 1) + 0.35), color=cfg.MUTED, stroke_width=3).next_to(bars, DOWN, buff=0.02)
    text = Text(label, font_size=25, color=color, weight=BOLD).next_to(axis, DOWN, buff=0.12)
    return VGroup(bars, axis, text)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "09")
    scene.add(cinematic_background())

    title = scene_title("Shape Matters After Center", "histograms show what one number hides").to_edge(UP, buff=0.42)
    title.scale(0.9).to_edge(UP, buff=0.24)
    compact = _histogram([1, 3, 6, 8, 6, 3, 1], cfg.CYAN, "compact").move_to(LEFT * 3.85 + DOWN * 0.78)
    wide = _histogram([2, 4, 5, 5, 5, 4, 2], cfg.GOLD, "wide").move_to(ORIGIN + DOWN * 0.78)
    skewed = _histogram([7, 6, 4, 3, 2, 1, 1], cfg.ORANGE, "right tail").move_to(RIGHT * 3.85 + DOWN * 0.78)

    paced_play(scene, FadeIn(title), run_time=0.7)
    paced_play(scene, LaggedStart(FadeIn(compact, shift=UP * 0.12), FadeIn(wide, shift=UP * 0.12), FadeIn(skewed, shift=UP * 0.12), lag_ratio=0.18), run_time=1.25)

    mean_labels = VGroup(
        label_pill(r"mean near 5", cfg.CYAN, font_size=19).next_to(compact, UP, buff=0.07),
        label_pill(r"mean near 5", cfg.GOLD, font_size=19).next_to(wide, UP, buff=0.07),
        label_pill(r"mean near 5", cfg.ORANGE, font_size=19).next_to(skewed, UP, buff=0.07),
    )
    paced_play(scene, FadeIn(mean_labels), run_time=0.75)

    iqr_eq = equation_box(r"\mathrm{IQR}=Q_3-Q_1", cfg.GREEN, font_size=36).move_to(UP * 1.58)
    compact_iqr = BraceBetweenPoints(compact.get_center() + LEFT * 0.7 + DOWN * 1.16, compact.get_center() + RIGHT * 0.7 + DOWN * 1.16, color=cfg.GREEN)
    wide_iqr = BraceBetweenPoints(wide.get_center() + LEFT * 1.18 + DOWN * 1.16, wide.get_center() + RIGHT * 1.18 + DOWN * 1.16, color=cfg.GREEN)
    tail_arrow = Arrow(skewed.get_center() + RIGHT * 0.55 + UP * 0.15, skewed.get_center() + RIGHT * 1.55 + UP * 0.15, color=cfg.ORANGE, stroke_width=6)
    tail_note = label_pill("skew changes interpretation", cfg.ORANGE, font_size=18).next_to(tail_arrow, UP, buff=0.12)

    paced_play(scene, FadeIn(iqr_eq, shift=DOWN * 0.12), GrowFromCenter(compact_iqr), GrowFromCenter(wide_iqr), run_time=0.9)
    paced_play(scene, GrowArrow(tail_arrow), FadeIn(tail_note), Indicate(skewed, color=cfg.WHITE), run_time=0.9)

    caption = VGroup(
        Text("Same center can mean different risk,", font_size=27, color=cfg.WHITE, weight=BOLD),
        Text("different tails, different preprocessing.", font_size=27, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.08)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.32)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    narration_wait(scene, 0.55)
    end_scene(scene, scene_start)
