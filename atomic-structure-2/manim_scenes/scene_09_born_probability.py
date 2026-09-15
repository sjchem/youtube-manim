"""Chapter 9: what psi means, and where the cloud actually comes from.

The two colours are signs of a real amplitude, and the chapter says on screen
that they are not charges. Squaring removes the sign; integrating over a region
gives a probability; and the cloud is then built the honest way, one detection
at a time, from many independently prepared trials.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    cloud,
    cross_mark,
    density_slice,
    halo,
    nucleus,
    outlined_text,
)

FIRST_DETECTIONS = 8


def _framed_slice(n: int, l: int, m: int, *, phase: bool = False,
                  center=ORIGIN, start_size: float = 4.7,
                  end_size: float = 4.95, duration: float = 32.0) -> ImageMobject:
    """A gentle push-in on an unchanged calculated image, never a breathing density.

    Only the viewing scale changes. The pixel values, relative lobe intensities,
    sign colours and nodal plane remain exactly those of the original state.
    """
    picture = density_slice(n, l, m, phase=phase, size=start_size).move_to(center)
    picture.framing_elapsed = 0.0
    picture.framing_start_size = start_size

    def push_in(mob: ImageMobject, dt: float) -> None:
        mob.framing_elapsed += dt * cfg.SPEED
        fraction = np.clip(mob.framing_elapsed / duration, 0.0, 1.0)
        eased = 0.5 - 0.5 * np.cos(PI * fraction)
        mob.set_height(start_size + (end_size - start_size) * eased)

    picture.add_updater(push_in)
    return picture


def _region_highlight(picture: ImageMobject) -> VGroup:
    """Move the selected region across the fixed density, following its framing."""
    region = Square(side_length=1.05, color=cfg.GOLD, stroke_width=3.2)
    highlight = VGroup(region.copy().set_stroke(width=13, opacity=0.13), region)
    highlight.scan_elapsed = 0.0

    def scan(mob: VGroup, dt: float) -> None:
        mob.scan_elapsed += dt * cfg.SPEED
        scale = picture.height / picture.framing_start_size
        # The volume is unchanged in plot coordinates; the viewing scale and
        # its selected location move, not the state or its probability density.
        offset = np.array([0.45 * np.sin(0.35 * mob.scan_elapsed), 1.0, 0.0])
        mob.set_width(1.05 * scale)
        mob.move_to(picture.get_center() + offset * scale)

    highlight.add_updater(scan)
    highlight.update(0)
    return highlight


def _sign_legend() -> VGroup:
    """Two swatches, and the sentence that stops the commonest misreading."""
    entries = VGroup()
    for label, colour in (("positive amplitude", cfg.PHASE_POS), ("negative amplitude", cfg.PHASE_NEG)):
        swatch = Square(side_length=0.34, fill_color=colour, fill_opacity=0.95, stroke_width=0)
        entries.add(VGroup(swatch, outlined_text(label, cfg.FONT["tiny"], colour)).arrange(RIGHT, buff=0.24))
    entries.arrange(RIGHT, buff=1.1)
    return entries


def _city_block() -> VGroup:
    """A street plan seen from above, with one warm doorway.

    The analogy chapter needs a familiar space in which one thing is somewhere
    and we only ever learn where by looking. Nothing here is an atom; the map
    is drawn in the film's scaffolding grey so it cannot be mistaken for one.
    """
    rng = np.random.default_rng(cfg.SEED + 9)
    plan = VGroup()
    for x in (-3.9, -1.3, 1.3, 3.9):
        for y in (-1.5, 1.5):
            block = RoundedRectangle(
                width=1.85, height=1.65, corner_radius=0.08,
                color=cfg.GRAY, stroke_width=1.8,
                fill_color=cfg.PANEL, fill_opacity=0.55,
            ).move_to([x + float(rng.uniform(-0.06, 0.06)), y, 0])
            plan.add(block)
    for y in (0.0,):
        plan.add(Line([-5.4, y, 0], [5.4, y, 0], color=cfg.GRAY, stroke_width=2, stroke_opacity=0.35))
    for x in (-2.6, 0.0, 2.6):
        plan.add(Line([x, -2.6, 0], [x, 2.6, 0], color=cfg.GRAY, stroke_width=2, stroke_opacity=0.35))

    doorway = VGroup(
        halo(0.34, cfg.GOLD, layers=4, peak_opacity=0.28),
        Dot(ORIGIN, radius=0.12, color=cfg.GOLD),
    ).move_to(DOORWAY)
    # A gentle change in the doorway's light keeps the analogy alive without
    # moving or adding any of the recorded sightings.
    doorway[0].glow_elapsed = 0.0

    def warm_light(mob: VGroup, dt: float) -> None:
        mob.glow_elapsed += dt * cfg.SPEED
        strength = 0.85 + 0.15 * np.sin(1.2 * mob.glow_elapsed)
        for index, ring in enumerate(mob):
            ring.set_fill(opacity=0.28 * strength * (1 - (index + 1) / len(mob)) ** 2)

    doorway[0].add_updater(warm_light)
    plan.add(doorway)
    plan.doorway = doorway
    return plan


DOORWAY = np.array([-1.30, 0.95, 0.0])


class Scene09BornProbability(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("09")

    # -- Beat 1: the sign of a real wave function -----------------------------
    phase_picture = _framed_slice(2, 1, 0, phase=True, center=[0, -0.25, 0])
    scene.dissolve(phase_picture, seconds=1.8)
    symbol = scene.formula(r"\psi", position=UP * 3.6, size=74)
    legend = scene.pin(_sign_legend().move_to([0, -3.45, 0]))
    scene.playq(FadeIn(legend), seconds=0.7)
    scene.at(17)

    not_charge = VGroup(
        cross_mark(0.22, cfg.RED),
        outlined_text("not positive and negative charge", cfg.FONT["small"], cfg.RED),
    ).arrange(RIGHT, buff=0.34)
    scene.pin(not_charge.move_to([0, 2.65, 0]))
    scene.playq(FadeIn(not_charge, shift=DOWN * 0.12), seconds=0.7)
    scene.hold(2.4)
    scene.at(27)
    scene.drop(not_charge, legend, symbol, seconds=0.7)

    # -- Beat 2: square it, and every sign becomes a nonnegative density ------
    law = scene.formula(r"\psi \;\longrightarrow\; |\psi|^2", position=UP * 3.35, size=70)
    phase_picture.clear_updaters()
    probability_picture = _framed_slice(
        2, 1, 0, center=[-1.35, -0.10, 0], start_size=4.65,
        end_size=4.9, duration=40.0,
    )
    scene.dissolve(probability_picture, seconds=3.0)
    slice_tag = scene.pin(outlined_text("calculated x–z slice", cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.55, 0]))
    scene.playq(FadeIn(slice_tag), seconds=0.6)
    scene.at(50)

    # -- Beat 3: a density is not yet a probability ---------------------------
    region = _region_highlight(probability_picture)
    scene.show(region, seconds=0.8)
    integral = scene.formula(r"P(V)=\int_V |\psi|^2\,dV", position=[4.35, 0.15, 0], size=48, color=cfg.GOLD)
    scene.drop(slice_tag, seconds=0.5)
    scene.at(65)
    region.clear_updaters()
    probability_picture.clear_updaters()
    scene.clear_local()

    # -- Beat 3b: the same logic, in a place the viewer already understands ---
    # An analogy, labelled as one. It carries exactly one idea across: a single
    # observation is a point, and only the accumulation is the distribution.
    scene.dissolve(_city_block(), seconds=1.8)
    premise = scene.pin(outlined_text("one cat, photographed at random times",
                                      cfg.FONT["small"], cfg.MUTED).move_to([0, 3.35, 0]))
    scene.playq(FadeIn(premise), seconds=0.6)

    rng = np.random.default_rng(cfg.SEED + 19)
    sightings = VGroup()
    for _ in range(150):
        if rng.random() < 0.55:
            point = DOORWAY + np.array([*rng.normal(0, 0.55, 2), 0.0])
        else:
            point = np.array([float(rng.uniform(-5.2, 5.2)), float(rng.uniform(-2.5, 2.5)), 0.0])
        sightings.add(Dot(point, radius=0.045, color=cfg.GOLD, fill_opacity=0.85))

    first, rest = VGroup(*sightings[:4]), VGroup(*sightings[4:])
    scene.playq(LaggedStart(*(FadeIn(dot, scale=3.0) for dot in first), lag_ratio=0.6), seconds=2.8)
    scene.playq(LaggedStart(*(FadeIn(dot) for dot in rest), lag_ratio=0.012), seconds=4.6)
    scene.adopt(*sightings)
    scene.drop(premise, seconds=0.5)

    lesson = scene.pin(outlined_text("many observations reveal a distribution",
                                     cfg.FONT["small"], cfg.GOLD, limit=11.5).move_to([0, 3.35, 0]))
    scene.playq(FadeIn(lesson), Indicate(scene.anchor.doorway, color=cfg.WHITE, scale_factor=1.25), seconds=1.6)
    scene.hold(1.6)
    mapping = scene.pin(VGroup(
        outlined_text("one photograph  =  one detection", cfg.FONT["tiny"], cfg.CYAN),
        outlined_text("the pile  =  the density map", cfg.FONT["tiny"], cfg.CYAN),
    ).arrange(DOWN, buff=0.26).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(mapping), seconds=0.8)
    scene.at(88)
    scene.drop(lesson, mapping, seconds=0.7)
    scene.cue("an analogy · a cat is somewhere between photographs", cfg.MUTED,
              hold=1.8, position=UP * 3.35)

    # -- Beat 4: prepare the same state again, and again ----------------------
    scene.anchor.clear_updaters()
    scene.dissolve(VGroup(nucleus(0.20)), seconds=1.8)
    detections = cloud(count=950, scale=1.15)
    # Keep every sampled record, with a common display scale about the nucleus.
    # Rare outer detections must not enter the caption band.
    detections.scale(5.3 / detections.height, about_point=ORIGIN)
    opening, remainder = VGroup(*detections[:FIRST_DETECTIONS]), VGroup(*detections[FIRST_DETECTIONS:])

    counter = scene.pin(outlined_text("1 preparation · 1 detection", cfg.FONT["small"], cfg.GOLD).move_to([0, 3.35, 0]))
    scene.playq(FadeIn(counter), seconds=0.6)
    scene.playq(LaggedStart(*(FadeIn(dot, scale=3.0) for dot in opening), lag_ratio=0.4), seconds=6.4)
    scene.adopt(*opening)
    scene.drop(counter, seconds=0.5)

    many = scene.pin(outlined_text("many independently prepared trials", cfg.FONT["small"], cfg.CYAN).move_to([0, 3.35, 0]))
    scene.playq(FadeIn(many), seconds=0.6)
    scene.playq(LaggedStart(*(FadeIn(dot) for dot in remainder), lag_ratio=0.008), seconds=22.0)
    scene.adopt(*remainder)
    scene.at(125)
    scene.drop(many, seconds=0.6)

    # -- Beat 5: the records fade into the map they were sampled from ---------
    prediction_map = _framed_slice(
        1, 0, 0, center=[0, -0.10, 0], start_size=4.7,
        end_size=5.05, duration=60.0,
    )
    scene.dissolve(prediction_map, seconds=4.5)
    density = scene.formula(r"|\psi|^2", position=UP * 3.35, size=78)
    scene.at(147)

    honest = scene.pin(outlined_text("a prediction map, not a photograph of a fuzzy object",
                                     cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(honest), seconds=0.7)
    scene.hold(2.6)
    scene.at(167)
    scene.drop(density, honest, seconds=0.7)

    scene.finish()
    prediction_map.clear_updaters()
