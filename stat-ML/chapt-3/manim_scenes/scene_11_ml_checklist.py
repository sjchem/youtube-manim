"""Scene 11 - descriptive statistics as an ML checklist."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, label_pill, narration_wait, paced_play, scene_title, stat_card, tiny_model


class Scene11MLChecklist(Scene):
    """Synthesize descriptive statistics into ML data checks."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "11")
    scene.add(cinematic_background())

    title = scene_title("A Small Statistical Checklist", "what to understand before fitting").to_edge(UP, buff=0.42)
    checks = VGroup(
        stat_card("center", "mean / median", cfg.CYAN, width=3.0),
        stat_card("spread", "variance / std", cfg.GOLD, width=3.0),
        stat_card("rank", "percentiles", cfg.GREEN, width=3.0),
        stat_card("pairs", "correlation", cfg.PURPLE, width=3.0),
    ).arrange(DOWN, buff=0.18).scale(0.92).move_to(LEFT * 4.5 + DOWN * 0.12)

    issues = VGroup(
        label_pill("outliers", cfg.ORANGE),
        label_pill("scale mismatch", cfg.GOLD),
        label_pill("feature leakage?", cfg.RED),
        label_pill("redundant inputs", cfg.PURPLE),
    ).arrange(DOWN, buff=0.24).move_to(ORIGIN + DOWN * 0.25)

    model = tiny_model("trained model").scale(1.25).move_to(RIGHT * 4.45 + DOWN * 0.2)
    arrows = VGroup(
        Arrow(checks.get_right(), issues.get_left(), color=cfg.CYAN, stroke_width=6, buff=0.22),
        Arrow(issues.get_right(), model.get_left(), color=cfg.GREEN, stroke_width=6, buff=0.22),
    )

    paced_play(scene, FadeIn(title), run_time=0.7)
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=RIGHT * 0.15) for card in checks], lag_ratio=0.14), run_time=1.1)
    paced_play(scene, GrowArrow(arrows[0]), LaggedStart(*[FadeIn(issue, scale=0.94) for issue in issues], lag_ratio=0.12), run_time=1.0)
    paced_play(scene, GrowArrow(arrows[1]), FadeIn(model, shift=LEFT * 0.25), run_time=0.85)

    shield = Circle(radius=0.62, color=cfg.GREEN, stroke_width=5).move_to(model.get_center() + UP * 1.22)
    check = Text("OK", font_size=32, color=cfg.GREEN, weight=BOLD).move_to(shield)
    paced_play(scene, Create(shield), FadeIn(check), Indicate(model, color=cfg.WHITE), run_time=0.9)

    caption = VGroup(
        Text("Descriptive statistics do not replace modeling.", font_size=27, color=cfg.WHITE, weight=BOLD),
        Text("They make modeling less blind.", font_size=27, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.08)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.34)
    paced_play(scene, FadeIn(caption), run_time=0.75)

    next_card = VGroup(
        Text("NEXT CHAPTER", font_size=22, color=cfg.GOLD, weight=BOLD),
        Text("Probability Basics", font_size=34, color=cfg.WHITE, weight=BOLD),
        Text("Every ML Learner Must Know", font_size=24, color=cfg.CYAN, weight=BOLD),
    ).arrange(DOWN, buff=0.04)
    next_card.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    next_frame = RoundedRectangle(
        corner_radius=0.12,
        width=next_card.width + 0.55,
        height=next_card.height + 0.38,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.88,
        stroke_color=cfg.GOLD,
        stroke_width=2.5,
    )
    next_bridge = VGroup(next_frame, next_card).move_to(RIGHT * 2.55 + DOWN * 2.72)
    next_arrow = Arrow(model.get_bottom() + DOWN * 0.18, next_bridge.get_top(), color=cfg.GOLD, stroke_width=5, buff=0.12)

    paced_play(scene, FadeOut(caption, shift=DOWN * 0.08), GrowArrow(next_arrow), FadeIn(next_bridge, shift=UP * 0.12), run_time=0.95)
    narration_wait(scene, 0.6)
    end_scene(scene, scene_start)
