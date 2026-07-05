"""Scene 01 - why descriptive statistics comes before ML."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, dot_cloud, end_scene, label_pill, narration_wait, paced_play, safe_caption, scene_title, stat_card, tiny_model


class Scene01DataFirstLook(Scene):
    """Open with raw data becoming readable summaries."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "01")
    scene.add(cinematic_background())

    title = scene_title("Statistics Before Learning", "The first map of a dataset").to_edge(UP, buff=0.34)
    cloud = dot_cloud(count=120, width=7.1, height=3.5, center=LEFT * 2.1 + DOWN * 0.05)
    raw = label_pill("raw records", cfg.CYAN).next_to(cloud, DOWN, buff=0.25)
    model = tiny_model().scale(1.15).move_to(RIGHT * 4.2 + DOWN * 0.1)
    arrow = Arrow(LEFT * 0.1, RIGHT * 2.7, color=cfg.MUTED, stroke_width=6, max_tip_length_to_length_ratio=0.12)
    question = safe_caption("Before a model learns, we ask: what shape is the data?", cfg.WHITE, 31).to_edge(DOWN, buff=0.46)

    paced_play(scene, FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(dot, scale=0.4) for dot in cloud], lag_ratio=0.015), FadeIn(raw), run_time=1.4)
    paced_play(scene, GrowArrow(arrow), FadeIn(model, shift=LEFT * 0.25), run_time=0.9)
    paced_play(scene, FadeIn(question, shift=UP * 0.15), run_time=0.75)
    narration_wait(scene, 0.5)

    summaries = VGroup(
        stat_card("center", "mean", cfg.CYAN),
        stat_card("spread", "std", cfg.GOLD),
        stat_card("rank", "p90", cfg.GREEN),
        stat_card("relation", "corr", cfg.PURPLE),
    ).arrange(DOWN, buff=0.16).scale(0.92).move_to(RIGHT * 1.0 + DOWN * 0.72)
    brace = Brace(summaries, LEFT, color=cfg.GOLD)
    insight = Text("summary signals", font_size=28, color=cfg.GOLD, weight=BOLD).next_to(brace, LEFT, buff=0.18)
    subtitle = title[2] if len(title) > 2 else None

    transition_anims = [
        cloud.animate.scale(0.82).shift(LEFT * 0.55),
        model.animate.shift(RIGHT * 0.35).set_opacity(0.55),
        FadeOut(arrow),
    ]
    if subtitle is not None:
        transition_anims.append(FadeOut(subtitle, shift=UP * 0.1))
    paced_play(scene, *transition_anims, run_time=0.8)
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=RIGHT * 0.18) for card in summaries], lag_ratio=0.18), GrowFromCenter(brace), FadeIn(insight), run_time=1.35)
    paced_play(scene, Indicate(summaries[0], color=cfg.WHITE), Indicate(summaries[1], color=cfg.WHITE), run_time=0.75)
    end_scene(scene, scene_start)
