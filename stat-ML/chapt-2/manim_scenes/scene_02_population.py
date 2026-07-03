from manim import *
import numpy as np

import config as cfg
from manim_scenes.common import (
    PALETTE,
    cinematic_background,
    dot_cloud,
    icon_tile,
    info_card,
    narration_wait,
    paced_play,
    scene_title,
    scene_transition,
)


def _domain(label: str, symbol: str, color: str, offset: np.ndarray, seed: int) -> VGroup:
    tile = icon_tile(label, symbol, color)
    dots = dot_cloud(26, width=1.15, height=0.8, center=DOWN * 0.62, colors=[color, cfg.MUTED], seed=seed, radius=0.027)
    group = VGroup(tile, dots).move_to(offset)
    return group


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("Population", "the full world we care about").to_edge(UP)
    population = Circle(radius=4.35, stroke_color=cfg.BLUE, stroke_width=4, fill_color=cfg.COLORS["panel"], fill_opacity=0.26)
    population.move_to(DOWN * 0.55)
    label = Text("Population", font_size=36, color=cfg.TEXT, weight=BOLD).move_to(population.get_top() + DOWN * 2.05)
    edge_hint = Text("continues beyond what we can observe", font_size=20, color=cfg.MUTED).to_edge(DOWN)
    boundary_notes = VGroup(
        info_card("Hard to observe", ["rare cases", "future cases", "costly labels"], 2.5, cfg.WARNING, 18, 14).move_to([-4.95, -2.55, 0]),
        info_card("Still in scope", ["unseen users", "new roads", "new patients"], 2.45, cfg.GREEN, 18, 14).move_to([4.95, -2.55, 0]),
    )

    domains = VGroup(
        _domain("customers", "$", cfg.GREEN, np.array([-3.0, 0.7, 0]), 2),
        _domain("patients", "+", cfg.RED, np.array([-1.0, -0.55, 0]), 3),
        _domain("roads", "car", cfg.YELLOW, np.array([1.15, 0.7, 0]), 4),
        _domain("transactions", "#", cfg.PURPLE, np.array([3.15, -0.55, 0]), 5),
        _domain("factories", "gear", cfg.ORANGE, np.array([0.3, -2.05, 0]), 6),
    )
    message = Text("Population = all cases we want to understand", font_size=31, color=cfg.TEXT, weight=BOLD).to_edge(DOWN, buff=0.55)

    paced_play(scene, FadeIn(title), Create(population), FadeIn(label), run_time=0.9)
    for domain in domains:
        paced_play(scene, FadeIn(domain, shift=UP * 0.15), run_time=0.42)
    paced_play(scene, FadeIn(boundary_notes, shift=UP * 0.12), run_time=0.65)
    paced_play(scene, Transform(edge_hint, message), run_time=0.8)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene02Population(Scene):
    def construct(self) -> None:
        play_scene(self)
