"""Guided motion for orbital filling: fixed states, animated reading cues."""
from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import QuantumScene, boxes


class ReadingTrace(VGroup):
    """A travelling border highlights a box or equation without moving it.

    The trace is a reading aid. Occupancy and the directions of the spin
    arrows remain fixed throughout the explanation.
    """

    def __init__(self) -> None:
        super().__init__()
        self.elapsed = 0.0
        self.paths = []
        self.colour = cfg.GOLD
        self.add_updater(self._advance)

    def focus(self, targets, colour: str = cfg.GOLD) -> None:
        self.submobjects.clear()
        self.paths = []
        self.elapsed = 0.0
        self.colour = colour
        for target in targets:
            path = SurroundingRectangle(target, buff=0.10, corner_radius=0.12,
                                        stroke_width=2, color=colour, fill_opacity=0)
            self.paths.append(path)
            halo = path.copy().set_stroke(width=8, opacity=0.10)
            edge = path.copy().set_stroke(width=2, opacity=0.18)
            first = VMobject().set_stroke(colour, width=3.5)
            second = first.copy()
            self.add(VGroup(halo, edge, first, second))
        self._advance(self, 0)

    def _advance(self, _mob, dt: float) -> None:
        self.elapsed += dt * cfg.SPEED
        for index, (path, (halo, edge, first, second)) in enumerate(zip(self.paths, self)):
            # Two equation rows take turns; a single orbital stays in focus.
            emphasis = (1.0 if len(self.paths) == 1 else
                        0.5 + 0.5*np.cos(TAU*(self.elapsed/5.6-index/len(self.paths))))
            head = (self.elapsed/3.8) % 1.0
            tail = head-0.20
            first.pointwise_become_partial(path, max(0.0, tail), head)
            second.pointwise_become_partial(path, 1.0+tail if tail < 0 else 1.0, 1.0)
            first.set_stroke(self.colour, width=3.5, opacity=0.95*emphasis)
            second.set_stroke(self.colour, width=3.5, opacity=0.95*emphasis)
            halo.set_stroke(opacity=0.10+0.07*emphasis)
            edge.set_stroke(opacity=0.18+0.20*emphasis)


def fill_electrons(scene: QuantumScene, electron_count: int,
                   seconds: float = 1.8, center=RIGHT * 2.4) -> None:
    """Draw just the newly occupied spin states, preserving existing arrows.

    The H/He/Li beats add one arrow. Completing neon adds the last two arrows
    in sequence within the original transition window, without an extra atom.
    """
    target = boxes(electron_count, center=center)
    old_keys = set(scene.anchor.arrows)
    new_keys = sorted(set(target.arrows)-old_keys)
    if not new_keys or not old_keys.issubset(target.arrows):
        raise ValueError("This beat must add electrons without removing a state.")
    arrows = [target.arrows[key] for key in new_keys]
    slots = [scene.anchor.slots[key[:2]] for key in new_keys]
    grow = [GrowArrow(arrow) for arrow in arrows]
    emphasis = [Indicate(slot, color=cfg.GOLD, scale_factor=1.04) for slot in slots]
    if len(arrows) == 1:
        scene.playq(*grow, *emphasis, seconds=seconds)
    else:
        scene.playq(LaggedStart(*grow, lag_ratio=0.4),
                    LaggedStart(*emphasis, lag_ratio=0.4), seconds=seconds)
    scene.adopt(*arrows)
    scene.anchor.arrows.update({key: target.arrows[key] for key in new_keys})


def portrait_push_in(portrait: ImageMobject) -> None:
    """Inspect the same fixed density image with a small, slow close-up."""
    start = portrait.height
    centre = portrait.get_center().copy()
    elapsed = 0.0

    def advance(mob: ImageMobject, dt: float) -> None:
        nonlocal elapsed
        elapsed += dt*cfg.SPEED
        fraction = min(1.0, elapsed/22.0)
        mob.scale_to_fit_height(start+0.12*smooth(fraction)).move_to(centre)

    portrait.add_updater(advance)
