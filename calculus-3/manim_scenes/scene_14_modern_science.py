"""Scene 14: the equations modern science is written in — and what AI learns."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    end_scene,
    fitted_eq,
    narration_wait,
    outlined_text,
    paced_play,
)

LAWS = (
    (r"m\frac{d^{2}\vec{r}}{dt^{2}}=\vec{F}", "Newton", cfg.CYAN, (-3.75, 1.70)),
    (r"\nabla\times\vec{E}=-\frac{\partial\vec{B}}{\partial t}", "Maxwell", cfg.GOLD, (3.75, 1.70)),
    (r"i\hbar\frac{\partial\Psi}{\partial t}=\hat{H}\Psi", "Schrödinger", cfg.PURPLE, (-3.75, -1.45)),
    (
        r"\rho\left(\frac{\partial\vec{u}}{\partial t}+(\vec{u}\cdot\nabla)\vec{u}\right)=-\nabla p+\mu\nabla^{2}\vec{u}",
        "Navier–Stokes",
        cfg.BLUE,
        (3.75, -1.45),
    ),
)
# One hold per law card, so this chapter's pacing is tunable in one place.
LAW_HOLDS = (6.9, 6.9, 6.9, 7.9)
LAYER_SIZES = (3, 4, 4, 2)


def _network(colour: str = cfg.CYAN) -> VGroup:
    """A small feed-forward diagram: enough to say 'neural network', no more."""
    layers = VGroup()
    for column, size in enumerate(LAYER_SIZES):
        nodes = VGroup(
            *(
                Dot([column * 1.30, (index - (size - 1) / 2) * 0.62, 0], radius=0.115, color=colour).set_stroke(cfg.BG, width=2)
                for index in range(size)
            )
        )
        layers.add(nodes)
    edges = VGroup()
    for left, right in zip(layers[:-1], layers[1:]):
        for start in left:
            for end in right:
                edges.add(Line(start.get_center(), end.get_center(), color=colour, stroke_width=1.5).set_stroke(opacity=0.28))
    return VGroup(edges, layers).move_to([0, -0.35, 0])


class Scene14ModernScience(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "14")
    add_cinematic_background(scene)

    heading = outlined_text("the language science is written in", cfg.FONT["body"], cfg.MUTED).to_edge(UP, buff=0.35)
    paced_play(scene, FadeIn(heading), run_time=0.8)

    cards = VGroup()
    for latex, name, colour, (x, y) in LAWS:
        formula = fitted_eq(latex, colour, cfg.FONT["body"], width=6.3)
        label = outlined_text(name, cfg.FONT["small"], cfg.MUTED)
        stack = VGroup(formula, label).arrange(DOWN, buff=0.26).move_to([x, y, 0])
        frame = RoundedRectangle(
            width=max(stack.width + 0.62, 5.6),
            height=stack.height + 0.62,
            corner_radius=0.16,
            color=colour,
            stroke_width=2.6,
            fill_color=cfg.PANEL,
            fill_opacity=0.68,
        ).move_to(stack)
        cards.add(VGroup(frame, stack))

    for index, card in enumerate(cards):
        paced_play(scene, FadeIn(card, shift=UP * 0.14), run_time=0.9)
        narration_wait(scene, LAW_HOLDS[index])

    common = outlined_text("every one of them: an equation of change", cfg.FONT["body"], cfg.GOLD).move_to(heading)
    paced_play(scene, ReplacementTransform(heading, common), run_time=1.1)
    paced_play(scene, LaggedStart(*(Indicate(card, color=cfg.GOLD, scale_factor=1.03) for card in cards), lag_ratio=0.18), run_time=2.2)
    narration_wait(scene, 7.2)

    # -- And what the newest models are still doing -----------------------------
    paced_play(scene, FadeOut(VGroup(cards, common)), run_time=0.8)

    net = _network(cfg.GREEN).scale(1.15).move_to([-3.55, -0.15, 0])
    neural_ode = fitted_eq(r"\frac{d\vec{h}}{dt}=f(\vec{h},t;\theta)", cfg.GREEN, cfg.FONT["title"], width=6.4).move_to([3.45, 0.55, 0])
    net_label = outlined_text("neural ODEs", cfg.FONT["small"], cfg.MUTED).next_to(net, DOWN, buff=0.40)
    learned = outlined_text("the network learns f", cfg.FONT["small"], cfg.MUTED).next_to(neural_ode, DOWN, buff=0.46)

    paced_play(scene, FadeIn(net, shift=RIGHT * 0.15), FadeIn(net_label), run_time=1.2)
    paced_play(scene, Write(neural_ode), FadeIn(learned), run_time=1.5)
    narration_wait(scene, 8.6)

    verdict = bottom_caption("Even the newest models still speak calculus.", cfg.GOLD)
    paced_play(scene, FadeIn(verdict), run_time=0.9)
    narration_wait(scene, 6.4)

    end_scene(scene, started, cfg.SCENE_DURATIONS["14"])
