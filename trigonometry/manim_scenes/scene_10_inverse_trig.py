"""Scene 10: inverse trigonometric functions run the projection backward."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)


class Scene10InverseTrig(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "10")
    add_cinematic_background(scene)
    tag = section_tag("10", "Run trigonometry backward")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    forward = VGroup(
        eq(r"30^\circ", cfg.GOLD, cfg.FONT["hero"]),
        Arrow(LEFT, RIGHT, color=cfg.MUTED, stroke_width=5, buff=0),
        eq(r"\sin(30^\circ)=\frac12", cfg.CYAN, cfg.FONT["hero"]),
    ).arrange(RIGHT, buff=0.55).move_to(UP * 1.2)
    paced_play(scene, FadeOut(tag), LaggedStart(*[FadeIn(item, shift=RIGHT * 0.14) for item in forward], lag_ratio=0.2), run_time=1.5)
    backward = VGroup(
        eq(r"\frac12", cfg.CYAN, cfg.FONT["hero"]),
        Arrow(RIGHT, LEFT, color=cfg.GOLD, stroke_width=5, buff=0),
        eq(r"\arcsin\left(\frac12\right)=30^\circ", cfg.GOLD, cfg.FONT["hero"]),
    ).arrange(RIGHT, buff=0.55).move_to(DOWN * 1.1)
    paced_play(scene, TransformFromCopy(forward, backward), run_time=1.8)
    narration_wait(scene, 1.6)

    warning = VGroup(
        eq(r"\sin^{-1}x", cfg.GOLD, cfg.FONT["section"]),
        outlined_text("means inverse sine", cfg.FONT["body"], cfg.WHITE, BOLD),
        eq(r"\neq\frac1{\sin x}", cfg.RED, cfg.FONT["section"]),
    ).arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.45)
    paced_play(scene, FadeIn(warning, shift=UP * 0.15), run_time=1.2)
    paced_play(scene, Indicate(warning[0], color=cfg.WHITE), Indicate(warning[2], color=cfg.RED), run_time=1.2)
    narration_wait(scene, 1.5)

    paced_play(scene, FadeOut(VGroup(forward, backward, warning)), run_time=0.8)

    # A horizontal line meets sine many times; the inverse must choose one branch.
    axes = Axes(
        x_range=[-PI, 3 * PI, PI / 2],
        y_range=[-1.3, 1.3, 1],
        x_length=12.4,
        y_length=4.2,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.5},
    ).move_to(DOWN * 0.2)
    sine = axes.plot(np.sin, x_range=[-PI, 3 * PI], color=cfg.CYAN, stroke_width=6)
    level = ValueTracker(0.5)
    horizontal = always_redraw(
        lambda: Line(axes.c2p(-PI, level.get_value()), axes.c2p(3 * PI, level.get_value()), color=cfg.GOLD, stroke_width=4)
    )
    paced_play(scene, Create(axes), Create(sine), run_time=2.0)
    scene.add(horizontal)
    intersections = VGroup(*[
        glow_dot(axes.c2p(value, 0.5), cfg.GOLD, 0.075)
        for value in (PI / 6, 5 * PI / 6, 13 * PI / 6, 17 * PI / 6)
    ])
    paced_play(scene, LaggedStart(*[FadeIn(dot, scale=1.3) for dot in intersections], lag_ratio=0.22), run_time=1.5)
    many = outlined_text("One height appears at many angles", cfg.FONT["label"], cfg.WHITE, BOLD)
    if many.width > cfg.SAFE_WIDTH - 0.8:
        many.scale_to_fit_width(cfg.SAFE_WIDTH - 0.8)
    many.to_edge(UP, buff=0.45)
    paced_play(scene, FadeIn(many), run_time=0.7)
    narration_wait(scene, 1.6)

    principal_box = SurroundingRectangle(
        axes.plot(np.sin, x_range=[-PI / 2, PI / 2], color=cfg.GREEN, stroke_width=8),
        color=cfg.GREEN,
        buff=0.18,
        corner_radius=0.1,
    )
    principal = axes.plot(np.sin, x_range=[-PI / 2, PI / 2], color=cfg.GREEN, stroke_width=8)
    range_label = eq(
        r"-\frac\pi2\leq\arcsin x\leq\frac\pi2",
        cfg.GOLD,
        cfg.FONT["section"],
    ).to_edge(UP, buff=0.38)
    range_label.set_stroke(cfg.BG, width=4.5, opacity=1.0, background=True)
    paced_play(scene, FadeOut(many), Create(principal), FadeIn(range_label), run_time=1.5)
    chosen = glow_dot(axes.c2p(PI / 6, 0.5), cfg.GREEN, 0.1)
    paced_play(scene, FadeOut(intersections), FadeIn(chosen, scale=1.3), run_time=1.0)
    narration_wait(scene, 1.8)

    paced_play(scene, FadeOut(VGroup(axes, sine, horizontal, principal, range_label, chosen)), run_time=0.9)

    # Three inverse functions answer three different measurement questions.
    cards = VGroup()
    specs = (
        (r"\arcsin(y)", "height → angle", r"[-90^\circ,90^\circ]", cfg.CYAN),
        (r"\arccos(x)", "horizontal position → angle", r"[0^\circ,180^\circ]", cfg.GREEN),
        (r"\arctan(m)", "slope → angle", r"(-90^\circ,90^\circ)", cfg.ORANGE),
    )
    for formula, meaning, principal_range, color in specs:
        box = RoundedRectangle(width=4.25, height=2.6, corner_radius=0.18, color=color, fill_color=cfg.PANEL, fill_opacity=0.88)
        content = VGroup(
            eq(formula, color, cfg.FONT["section"]),
            outlined_text(meaning, cfg.FONT["small"], cfg.WHITE, BOLD),
            eq(principal_range, cfg.GOLD, cfg.FONT["small"]),
        ).arrange(DOWN, buff=0.18).move_to(box)
        cards.add(VGroup(box, content))
    cards.arrange(RIGHT, buff=0.35)
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in cards], lag_ratio=0.25), run_time=1.8)
    examples = VGroup(
        eq(r"\arcsin(0.5)=30^\circ", cfg.CYAN, cfg.FONT["body"]),
        eq(r"\arccos(0.5)=60^\circ", cfg.GREEN, cfg.FONT["body"]),
        eq(r"\arctan(1)=45^\circ", cfg.ORANGE, cfg.FONT["body"]),
    )
    for card, example in zip(cards, examples, strict=True):
        example.next_to(card, DOWN, buff=0.3)
    paced_play(scene, LaggedStart(*[FadeIn(item) for item in examples], lag_ratio=0.25), run_time=1.5)
    paced_play(scene, LaggedStart(*[Indicate(card, color=cfg.WHITE, scale_factor=1.025) for card in cards], lag_ratio=0.22), run_time=1.6)
    takeaway = VGroup(
        outlined_text("A calculator returns one principal angle.", cfg.FONT["label"], cfg.GOLD, BOLD),
        outlined_text("For every solution: use circle symmetry, then add complete turns.", cfg.FONT["small"], cfg.WHITE, BOLD),
    ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.22)
    paced_play(scene, FadeOut(examples), FadeIn(takeaway), run_time=0.8)
    narration_wait(scene, 2.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["10"])
