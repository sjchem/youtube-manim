"""Scene 02 — The Uncertain World.

The real world does not hand us clean data. Every measurement carries
noise. Statistics is the discipline that lets us reason under that
uncertainty rather than pretending it does not exist.

Narration cue: ~65 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    narration_wait, paced_play, label,
)
from utils.math_utils import noisy_sine_data


class Scene02UncertainWorld(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=True))

    # ── Phase 1: A hidden "truth" — the true relationship ───────────────────
    caption_truth = bottom_caption("Somewhere out there is the truth.", color=cfg.CYAN)

    true_curve = ParametricFunction(
        lambda t: np.array([t, 1.6 * np.sin(0.6 * t), 0]),
        t_range=[-6.5, 6.5],
        color=cfg.GREEN,
        stroke_width=5.5,
        stroke_opacity=0.0,
    )
    glow_bg = true_curve.copy().set_stroke(cfg.GREEN, width=22, opacity=0.0)
    scene.add(glow_bg, true_curve)

    paced_play(
        scene,
        true_curve.animate.set_stroke(opacity=0.90),
        glow_bg.animate.set_stroke(opacity=0.12),
        FadeIn(caption_truth, shift=UP * 0.1),
        run_time=1.5,
    )
    narration_wait(scene, 0.8)

    example_cards = VGroup()
    for title, subtitle, pos, col in (
        ("blood pressure", "age -> risk", LEFT * 3.0 + UP * 1.35, cfg.GREEN),
        ("chip temperature", "heat -> failure", RIGHT * 3.0 + UP * 1.35, cfg.GOLD),
    ):
        box = RoundedRectangle(
            corner_radius=0.12, width=2.85, height=0.82,
            fill_color=cfg.COLORS["panel"], fill_opacity=0.86,
            stroke_color=col, stroke_width=2.0,
        )
        text = VGroup(
            Text(title, font_size=21, color=col, weight=BOLD),
            Text(subtitle, font_size=17, color=cfg.WHITE),
        ).arrange(DOWN, buff=0.02)
        for mob in text:
            mob.set_stroke(cfg.BG, width=2, background=True)
        text.move_to(box.get_center())
        example_cards.add(VGroup(box, text).move_to(pos))

    paced_play(
        scene,
        LaggedStart(*[FadeIn(card, shift=DOWN * 0.10) for card in example_cards], lag_ratio=0.18),
        run_time=0.9,
    )
    narration_wait(scene, 0.5)

    # ── Phase 2: Real-world observations — noisy and incomplete ─────────────
    xs, ys_noisy, ys_true = noisy_sine_data(n=55, noise_std=0.55, seed=13)

    obs_dots = VGroup(*[
        Dot(point=[x, y, 0], radius=0.07, color=cfg.ORANGE, fill_opacity=0.82)
        for x, y in zip(xs, ys_noisy)
    ])

    caption_noise = bottom_caption("We do not observe truth directly. We observe measurements.", color=cfg.ORANGE)

    paced_play(
        scene,
        FadeOut(example_cards),
        LaggedStart(*[FadeIn(d, scale=0.4) for d in obs_dots], lag_ratio=0.04),
        run_time=2.0,
    )
    paced_play(
        scene,
        FadeOut(caption_truth),
        FadeIn(caption_noise, shift=UP * 0.1),
        run_time=0.6,
    )
    narration_wait(scene, 0.6)

    # ── Phase 3: Measurement uncertainty bars on a few points ───────────────
    n_bars = 8
    rng = np.random.default_rng(77)
    bar_indices = rng.choice(len(xs), size=n_bars, replace=False)

    error_bars = VGroup()
    for idx in bar_indices:
        x_pos = xs[idx]
        y_pos = ys_noisy[idx]
        half  = rng.uniform(0.25, 0.55)
        bar   = Line(
            [x_pos, y_pos - half, 0], [x_pos, y_pos + half, 0],
            color=cfg.GOLD, stroke_width=3.5, stroke_opacity=0.78,
        )
        cap_b = Line([x_pos - 0.12, y_pos - half, 0], [x_pos + 0.12, y_pos - half, 0],
                     color=cfg.GOLD, stroke_width=2.5, stroke_opacity=0.78)
        cap_t = Line([x_pos - 0.12, y_pos + half, 0], [x_pos + 0.12, y_pos + half, 0],
                     color=cfg.GOLD, stroke_width=2.5, stroke_opacity=0.78)
        error_bars.add(VGroup(bar, cap_b, cap_t))

    paced_play(
        scene,
        LaggedStart(*[GrowFromCenter(eb) for eb in error_bars], lag_ratio=0.10),
        run_time=1.5,
    )

    missing_marks = VGroup()
    for idx in sorted(rng.choice(len(xs), size=5, replace=False)):
        mark = Cross(obs_dots[idx], stroke_color=cfg.PURPLE, stroke_width=4)
        mark.scale(0.8)
        missing_marks.add(mark)

    uncertainty_tags = VGroup(
        label("imprecise sensors", font_size=cfg.FONT["tiny"], color=cfg.GOLD),
        label("missing values", font_size=cfg.FONT["tiny"], color=cfg.PURPLE),
        label("wrong labels", font_size=cfg.FONT["tiny"], color=cfg.ORANGE),
    ).arrange(RIGHT, buff=0.42)
    uncertainty_tags.to_edge(UP, buff=0.48)
    paced_play(
        scene,
        LaggedStart(*[Create(m) for m in missing_marks], lag_ratio=0.10),
        LaggedStart(*[FadeIn(t, shift=DOWN * 0.08) for t in uncertainty_tags], lag_ratio=0.18),
        run_time=0.9,
    )
    narration_wait(scene, 0.5)

    def process_box(text: str, color: str) -> VGroup:
        box = RoundedRectangle(
            corner_radius=0.12, width=2.35, height=0.75,
            fill_color=cfg.COLORS["panel"], fill_opacity=0.88,
            stroke_color=color, stroke_width=2.2,
        )
        txt = Text(text, font_size=cfg.FONT["tiny"], color=color, weight=BOLD)
        txt.set_stroke(cfg.BG, width=2, background=True)
        if txt.width > 2.0:
            txt.scale_to_fit_width(2.0)
        txt.move_to(box.get_center())
        return VGroup(box, txt)

    world_box = process_box("Real world", cfg.GREEN)
    measure_box = process_box("Measurement", cfg.GOLD)
    dataset_box = process_box("Dataset", cfg.ORANGE)
    dgp_boxes = VGroup(world_box, measure_box, dataset_box).arrange(RIGHT, buff=0.7)
    dgp_arrows = VGroup(
        Arrow(world_box.get_right(), measure_box.get_left(), buff=0.12,
              color=cfg.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.25),
        Arrow(measure_box.get_right(), dataset_box.get_left(), buff=0.12,
              color=cfg.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.25),
    )
    dgp_title = Text("Data-generating process", font_size=cfg.FONT["small"],
                     color=cfg.WHITE, weight=BOLD)
    dgp_title.set_stroke(cfg.BG, width=4, background=True)
    dgp_group = VGroup(dgp_boxes, dgp_arrows).move_to(UP * 2.25)
    dgp_title.next_to(dgp_group, UP, buff=0.18)

    random_card = process_box("Random variation", cfg.PURPLE).scale(0.88)
    systematic_card = process_box("Systematic error", cfg.RED).scale(0.88)
    error_types = VGroup(random_card, systematic_card).arrange(RIGHT, buff=0.5)
    error_types.next_to(dgp_group, DOWN, buff=0.28)
    dgp_visual = VGroup(dgp_title, dgp_group, error_types)

    paced_play(
        scene,
        FadeOut(uncertainty_tags),
        obs_dots.animate.set_fill(opacity=0.42),
        missing_marks.animate.set_stroke(opacity=0.25),
        true_curve.animate.set_stroke(opacity=0.42),
        FadeIn(dgp_title, shift=DOWN * 0.08),
        LaggedStart(*[FadeIn(m, scale=0.92) for m in dgp_boxes], lag_ratio=0.18),
        LaggedStart(*[GrowArrow(a) for a in dgp_arrows], lag_ratio=0.20),
        run_time=1.3,
    )
    paced_play(
        scene,
        LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in error_types], lag_ratio=0.22),
        run_time=0.9,
    )
    narration_wait(scene, 1.3)

    random_noise = VGroup(*[
        Line(
            [xs[i], ys_true[i], 0], [xs[i], ys_noisy[i], 0],
            color=cfg.PURPLE, stroke_width=2.2, stroke_opacity=0.45,
        )
        for i in rng.choice(len(xs), size=12, replace=False)
    ])
    biased_sensor = VGroup(*[
        Dot(point=[x, y + 0.42, 0], radius=0.052, color=cfg.RED, fill_opacity=0.78)
        for x, y in zip(xs[::4], ys_noisy[::4])
    ])
    bias_arrow = Arrow(
        LEFT * 4.8 + DOWN * 2.75, LEFT * 4.8 + DOWN * 2.15,
        color=cfg.RED, stroke_width=4,
        max_tip_length_to_length_ratio=0.30,
    )
    bias_label = label("biased sensor shifts everything", font_size=cfg.FONT["tiny"], color=cfg.RED)
    bias_label.next_to(bias_arrow, RIGHT, buff=0.18)

    paced_play(
        scene,
        random_card.animate.scale(1.08),
        LaggedStart(*[Create(line) for line in random_noise], lag_ratio=0.04),
        run_time=0.9,
    )
    paced_play(
        scene,
        random_card.animate.scale(1 / 1.08),
        systematic_card.animate.scale(1.08),
        LaggedStart(*[FadeIn(d, scale=0.45) for d in biased_sensor], lag_ratio=0.05),
        GrowArrow(bias_arrow),
        FadeIn(bias_label, shift=LEFT * 0.08),
        run_time=1.0,
    )
    narration_wait(scene, 0.7)

    # ── Phase 4: Question mark — can we find the true pattern? ──────────────
    paced_play(
        scene,
        true_curve.animate.set_stroke(opacity=0.20),
        glow_bg.animate.set_stroke(opacity=0.04),
        obs_dots.animate.set_fill(opacity=0.82),
        FadeOut(dgp_visual),
        FadeOut(random_noise),
        FadeOut(biased_sensor),
        FadeOut(bias_arrow),
        FadeOut(bias_label),
        FadeOut(missing_marks),
        run_time=0.75,
    )

    question_mark = Text("?", font_size=180, color=cfg.PURPLE, weight=BOLD)
    question_mark.set_stroke(cfg.BG, width=10, background=True)
    question_mark.set_fill(opacity=0.0)
    scene.add(question_mark)

    caption_q = bottom_caption("Can we recover the true signal from all this noise?", color=cfg.PURPLE)

    paced_play(
        scene,
        question_mark.animate.set_fill(opacity=0.55),
        FadeOut(caption_noise),
        FadeIn(caption_q, shift=UP * 0.1),
        run_time=1.0,
    )
    narration_wait(scene, 0.5)

    # ── Phase 5: Statistics label ────────────────────────────────────────────
    stat_label = Text("Statistics is built for this.", font_size=cfg.FONT["body"],
                      color=cfg.CYAN, weight=BOLD)
    stat_label.set_stroke(cfg.BG, width=5, background=True)
    stat_label.to_edge(UP, buff=0.42)

    paced_play(
        scene,
        question_mark.animate.set_fill(opacity=0.20),
        true_curve.animate.set_stroke(opacity=0.65),
        glow_bg.animate.set_stroke(opacity=0.10),
        FadeIn(stat_label, shift=DOWN * 0.12),
        FadeOut(caption_q),
        run_time=1.1,
    )
    narration_wait(scene, 1.2)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["02"])
