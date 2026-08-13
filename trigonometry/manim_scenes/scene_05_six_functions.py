"""Scene 05: SOH-CAH-TOA expands naturally into all six trig functions."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    color_formula_parts,
    end_scene,
    eq,
    equation_card,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)


class Scene05SixFunctions(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "05")
    add_cinematic_background(scene)
    tag = section_tag("05", "Three ratios — and their mirrors")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    origin = np.array([-5.2, -2.2, 0.0])
    adjacent = Line(origin, origin + RIGHT * 4.2, color=cfg.GREEN, stroke_width=8)
    opposite = Line(origin + RIGHT * 4.2, origin + RIGHT * 4.2 + UP * 3.15, color=cfg.CYAN, stroke_width=8)
    hypotenuse = Line(origin, origin + RIGHT * 4.2 + UP * 3.15, color=cfg.WHITE, stroke_width=8)
    hypotenuse_angle = np.arctan2(3.15, 4.2)
    triangle = VGroup(adjacent, opposite, hypotenuse)
    angle = Angle(adjacent, hypotenuse, radius=0.72, color=cfg.GOLD, stroke_width=5)
    theta = eq(r"\theta", cfg.GOLD, cfg.FONT["section"]).move_to(origin + [0.9, 0.35, 0])
    labels = VGroup(
        outlined_text("ADJACENT", cfg.FONT["small"], cfg.GREEN, BOLD).next_to(adjacent, DOWN, buff=0.18),
        outlined_text("OPPOSITE", cfg.FONT["small"], cfg.CYAN, BOLD).next_to(opposite, RIGHT, buff=0.18),
        outlined_text("HYPOTENUSE", cfg.FONT["small"], cfg.WHITE, BOLD)
        .rotate(hypotenuse_angle)
        .move_to(hypotenuse.get_center() + np.array([-0.34, 0.46, 0])),
    )
    paced_play(scene, FadeOut(tag), Create(triangle), Create(angle), FadeIn(theta), run_time=1.7)
    paced_play(scene, LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.22), run_time=1.2)

    mnemonic = VGroup(
        outlined_text("SOH", cfg.FONT["hero"], cfg.CYAN, BOLD),
        outlined_text("CAH", cfg.FONT["hero"], cfg.GREEN, BOLD),
        outlined_text("TOA", cfg.FONT["hero"], cfg.ORANGE, BOLD),
    ).arrange(DOWN, buff=0.45).move_to([4.4, 0.15, 0])
    expansions = VGroup(
        outlined_text("Sine = Opposite / Hypotenuse", cfg.FONT["small"], cfg.CYAN, BOLD),
        outlined_text("Cosine = Adjacent / Hypotenuse", cfg.FONT["small"], cfg.GREEN, BOLD),
        outlined_text("Tangent = Opposite / Adjacent", cfg.FONT["small"], cfg.ORANGE, BOLD),
    ).arrange(DOWN, buff=0.48).move_to([2.95, -0.05, 0])
    paced_play(scene, LaggedStart(*[FadeIn(word, shift=LEFT * 0.2) for word in mnemonic], lag_ratio=0.25), run_time=1.6)
    for word, expansion in zip(mnemonic, expansions, strict=True):
        paced_play(scene, ReplacementTransform(word, expansion), run_time=1.1)
        narration_wait(scene, 0.65)
    narration_wait(scene, 1.0)

    paced_play(scene, FadeOut(VGroup(triangle, angle, theta, labels, expansions)), run_time=0.9)
    primary = VGroup(
        equation_card(r"\sin\theta=\frac{O}{H}", cfg.CYAN, cfg.FONT["section"]),
        equation_card(r"\cos\theta=\frac{A}{H}", cfg.GREEN, cfg.FONT["section"]),
        equation_card(r"\tan\theta=\frac{O}{A}", cfg.ORANGE, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.32).move_to([-3.2, 0, 0])
    reciprocal = VGroup(
        equation_card(r"\csc\theta=\frac{H}{O}", cfg.CYAN, cfg.FONT["section"]),
        equation_card(r"\sec\theta=\frac{H}{A}", cfg.GREEN, cfg.FONT["section"]),
        equation_card(r"\cot\theta=\frac{A}{O}", cfg.ORANGE, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.32).move_to([3.2, 0, 0])
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=RIGHT * 0.15) for card in primary], lag_ratio=0.25), run_time=1.8)
    flip_arrows = VGroup(*[
        DoubleArrow(primary[i].get_right(), reciprocal[i].get_left(), color=cfg.GOLD, stroke_width=4, buff=0.18)
        for i in range(3)
    ])
    paced_play(scene, LaggedStart(*[GrowArrow(arrow) for arrow in flip_arrows], lag_ratio=0.22), run_time=1.3)
    for source, target in zip(primary, reciprocal, strict=True):
        paced_play(scene, TransformFromCopy(source, target), run_time=1.2)
        narration_wait(scene, 0.65)
    reciprocal_caption = VGroup(
        outlined_text("Cosecant, secant, and cotangent", cfg.FONT["label"], cfg.WHITE, BOLD),
        outlined_text("simply flip the first three ratios.", cfg.FONT["label"], cfg.WHITE, BOLD),
    ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.22)
    # Add the complete thought at once.  Animating a long Text object directly
    # can expose only its first glyphs in intermediate video frames.
    scene.add(reciprocal_caption)
    paced_play(scene, Indicate(reciprocal_caption, color=cfg.GOLD, scale_factor=1.015), run_time=0.7)
    narration_wait(scene, 1.8)

    paced_play(scene, FadeOut(VGroup(primary, reciprocal, flip_arrows, reciprocal_caption)), run_time=0.9)
    web = VGroup()
    center = color_formula_parts(eq(r"\sin\theta,\ \cos\theta", cfg.WHITE, cfg.FONT["hero"]))
    center.move_to(UP * 1.6)
    relations = VGroup(
        color_formula_parts(eq(r"\tan\theta=\frac{\sin\theta}{\cos\theta}", cfg.WHITE, cfg.FONT["section"])),
        color_formula_parts(eq(r"\csc\theta=\frac1{\sin\theta}", cfg.WHITE, cfg.FONT["section"])),
        color_formula_parts(eq(r"\sec\theta=\frac1{\cos\theta}", cfg.WHITE, cfg.FONT["section"])),
        color_formula_parts(eq(r"\cot\theta=\frac{\cos\theta}{\sin\theta}", cfg.WHITE, cfg.FONT["section"])),
    ).arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.7)).move_to(DOWN * 0.5)
    web.add(center, relations)
    paced_play(scene, FadeIn(center, scale=1.15), run_time=0.9)
    paced_play(scene, LaggedStart(*[TransformFromCopy(center, relation) for relation in relations], lag_ratio=0.25), run_time=2.2)
    takeaway = VGroup(
        outlined_text("Learn sine and cosine deeply.", cfg.FONT["label"], cfg.GOLD, BOLD),
        outlined_text("The other four are built from them.", cfg.FONT["label"], cfg.WHITE, BOLD),
    ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.22)
    scene.add(takeaway)
    paced_play(scene, LaggedStart(*[Indicate(item, color=cfg.WHITE) for item in relations], lag_ratio=0.18), run_time=1.8)
    narration_wait(scene, 2.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["05"])
