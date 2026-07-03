from manim import *

import config as cfg
from manim_scenes.common import bell_curve, cinematic_background, dot_cloud, info_card, narration_wait, paced_play, scene_title, scene_transition


def _cloud_panel(label: str, x: float, seed: int) -> VGroup:
    box = RoundedRectangle(corner_radius=0.12, width=2.05, height=1.25, fill_color=cfg.COLORS["panel"], fill_opacity=0.82, stroke_color=cfg.BLUE)
    dots = dot_cloud(45, width=1.6, height=0.72, center=box.get_center() + UP * 0.05, colors=[cfg.BLUE, cfg.GREEN, cfg.YELLOW], seed=seed, radius=0.025)
    text = Text(label, font_size=19, color=cfg.TEXT, weight=BOLD).next_to(box, DOWN, buff=0.08)
    return VGroup(box, dots, text).move_to([x, 1.25, 0])


def _video_tiles() -> VGroup:
    tiles = VGroup()
    for index in range(4):
        tile = RoundedRectangle(corner_radius=0.07, width=0.95, height=0.62, fill_color=cfg.COLORS["panel_alt"], fill_opacity=0.9, stroke_color=cfg.WARNING)
        tile.move_to([(index - 1.5) * 1.05, 0, 0])
        car = Rectangle(width=0.28, height=0.12, fill_color=cfg.YELLOW, fill_opacity=1, stroke_width=0).move_to(tile.get_center() + RIGHT * index * 0.03)
        tiles.add(VGroup(tile, car))
    arrows = VGroup(*[Arrow(tiles[i].get_right(), tiles[i + 1].get_left(), buff=0.05, color=cfg.WARNING, stroke_width=3) for i in range(3)])
    label = MathTex(r"x_t\approx x_{t+1}", font_size=30, color=cfg.WARNING).next_to(tiles, DOWN, buff=0.22)
    return VGroup(tiles, arrows, label)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("IID").to_edge(UP, buff=0.12)
    subtitle = Text("the ideal assumption", font_size=25, color=cfg.MUTED).move_to([0, 2.35, 0])
    panels = VGroup(
        _cloud_panel("training", -4.35, 8),
        _cloud_panel("validation", -1.45, 9),
        _cloud_panel("test", 1.45, 10),
        _cloud_panel("future", 4.35, 11),
    )
    iid = Text("IID", font_size=58, color=cfg.YELLOW, weight=BOLD).move_to([0, -0.3, 0])
    independent = Text("Independent", font_size=34, color=cfg.GREEN, weight=BOLD).move_to([-3.35, -1.15, 0])
    identical = Text("Identically Distributed", font_size=34, color=cfg.BLUE, weight=BOLD).move_to([2.65, -1.15, 0])
    random_dots = dot_cloud(30, width=2.25, height=0.72, center=[-3.35, -2.12, 0], colors=[cfg.GREEN, cfg.MUTED], seed=12, radius=0.03)
    no_links = Text("no direct links", font_size=17, color=cfg.MUTED).next_to(random_dots, DOWN, buff=0.1)
    video_tiles = _video_tiles().scale(0.74).move_to([-3.35, -2.38, 0])
    curves = VGroup(
        bell_curve(cfg.BLUE).scale(0.66).move_to([1.65, -2.35, 0]),
        bell_curve(cfg.GREEN).scale(0.66).move_to([3.55, -2.35, 0]),
    )
    distorted = bell_curve(cfg.WARNING, shift_x=0.9, stretch=0.72, skew=0.25).scale(0.66).move_to([3.55, -2.35, 0])
    independent_card = info_card("Independence breaks when", ["examples are near-duplicates", "users influence each other"], 3.85, cfg.WARNING, 21, 16).move_to([-3.35, -3.28, 0])
    identical_card = info_card("Same distribution means", ["evaluation resembles future use"], 3.65, cfg.BLUE, 21, 16).move_to([2.65, -3.28, 0])

    paced_play(scene, FadeIn(title), FadeIn(subtitle), FadeIn(panels, lag_ratio=0.08), run_time=1.0)
    paced_play(scene, FadeIn(iid, scale=0.92), run_time=0.55)
    paced_play(scene, iid.animate.scale(0.62).move_to([-6.1, -0.58, 0]), FadeIn(independent), FadeIn(identical), run_time=0.75)
    paced_play(scene, FadeIn(random_dots), FadeIn(no_links), FadeIn(curves), FadeIn(identical_card, shift=UP * 0.1), run_time=0.9)
    paced_play(scene, ReplacementTransform(VGroup(random_dots, no_links), video_tiles), run_time=0.9)
    paced_play(scene, FadeIn(independent_card, shift=UP * 0.1), ReplacementTransform(curves[1], distorted), run_time=0.8)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene08IID(Scene):
    def construct(self) -> None:
        play_scene(self)
