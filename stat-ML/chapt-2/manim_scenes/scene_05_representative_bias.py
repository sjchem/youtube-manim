from manim import *

import config as cfg
from manim_scenes.common import PALETTE, cinematic_background, dot_cloud, info_card, narration_wait, paced_play, scene_title, scene_transition


def _panel(title: str, biased: bool, x: float) -> VGroup:
    heading = Text(title, font_size=28, color=cfg.TEXT, weight=BOLD).move_to([x, 2.46, 0])
    pop_label = Text("population", font_size=18, color=cfg.MUTED).move_to([x - 1.4, 1.92, 0])
    sample_label = Text("sample", font_size=18, color=cfg.MUTED).move_to([x + 1.25, 1.92, 0])
    colors = PALETTE[:4]
    pop = dot_cloud(95, width=2.25, height=1.55, center=[x - 1.42, 1.1, 0], colors=colors, seed=51 if not biased else 52, radius=0.032)
    sample_colors = [cfg.BLUE, cfg.BLUE, cfg.BLUE, cfg.GREEN] if biased else colors
    sample = dot_cloud(48, width=1.45, height=1.05, center=[x + 1.25, 1.1, 0], colors=sample_colors, seed=61 if not biased else 62, radius=0.038)

    axes = Axes(
        x_range=[-2, 2, 1],
        y_range=[-1.2, 1.2, 1],
        x_length=3.1,
        y_length=1.65,
        tips=False,
        axis_config={"stroke_color": cfg.MUTED, "stroke_opacity": 0.45, "stroke_width": 2},
    ).move_to([x, -0.48, 0])
    boundary_color = cfg.GREEN if not biased else cfg.WARNING
    boundary = Line(axes.c2p(-1.5, -0.65), axes.c2p(1.55, 0.62), color=boundary_color, stroke_width=4)
    if biased:
        boundary.rotate(0.42, about_point=axes.get_center())
    model_label = Text("balanced boundary" if not biased else "distorted boundary", font_size=18, color=boundary_color).next_to(axes, DOWN, buff=0.04)
    divider = Line([x + 3.38, -3.25, 0], [x + 3.38, 2.72, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.65)
    group = VGroup(heading, pop_label, sample_label, pop, sample, axes, boundary, model_label)
    if x < 0:
        group.add(divider)
    return group


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("Representative sample vs biased sample").to_edge(UP)
    title.scale_to_fit_width(12.8).to_edge(UP, buff=0.14)
    left = _panel("Representative Sample", False, -3.35)
    right = _panel("Biased Sample", True, 3.35)
    message = MathTex(r"\mathrm{Large\ dataset}\neq\mathrm{Good\ dataset}", font_size=34, color=cfg.TEXT).to_edge(DOWN, buff=0.12)
    message.set_color_by_tex("Large", cfg.YELLOW)
    message.set_color_by_tex("Good", cfg.GREEN)
    left_card = info_card("Fairer view", ["similar proportions", "rare groups visible", "boundary has context"], 3.35, cfg.GREEN, 22, 17).move_to([-3.35, -2.58, 0])
    right_card = info_card("Common bias sources", ["one city", "one device", "one time period"], 3.35, cfg.WARNING, 22, 17).move_to([3.35, -2.58, 0])

    paced_play(scene, FadeIn(title), run_time=0.55)
    paced_play(scene, FadeIn(left, lag_ratio=0.05), run_time=1.1)
    paced_play(scene, FadeIn(left_card, shift=UP * 0.1), run_time=0.45)
    paced_play(scene, FadeIn(right, lag_ratio=0.05), run_time=1.1)
    paced_play(scene, FadeIn(right_card, shift=UP * 0.1), Write(message), run_time=0.75)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene05RepresentativeBias(Scene):
    def construct(self) -> None:
        play_scene(self)
