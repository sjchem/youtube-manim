from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, create_number_line, create_particle, narration_wait, paced_play, scene_transition
from utils.physics_models import particle_motion_1d


def _jump(scene: Scene, particle: Mobject, line: NumberLine, start: float, end: float, color: str) -> None:
    path = ArcBetweenPoints(line.n2p(start), line.n2p(end), angle=-TAU / 8 if end > start else TAU / 8)
    path.set_stroke(color=color, opacity=0.55, width=4)
    paced_play(scene, Create(path), MoveAlongPath(particle, path), run_time=0.55)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = Text("Multiplication as motion", font_size=42, color=cfg.ZERO).to_edge(UP)
    line = create_number_line(-15, 15, unit_size=0.34).move_to(DOWN * 0.45)
    paced_play(scene, FadeIn(title, shift=DOWN * 0.2), Create(line), run_time=1.1)

    labels = VGroup(
        Text("right = positive", font_size=24, color=cfg.POSITIVE),
        Text("left = negative", font_size=24, color=cfg.NEGATIVE),
    ).arrange(RIGHT, buff=0.8).next_to(line, DOWN, buff=0.55)
    paced_play(scene, FadeIn(labels), run_time=0.45)

    eq = MathTex(r"3\times4=12", font_size=48, color=cfg.POSITIVE).next_to(title, DOWN, buff=0.4)
    particle = create_particle(cfg.GOLD).move_to(line.n2p(0))
    paced_play(scene, FadeIn(eq), FadeIn(particle), run_time=0.6)
    for step in particle_motion_1d(0, 4, 3):
        _jump(scene, particle, line, step.start, step.end, cfg.POSITIVE)
    paced_play(scene, Flash(particle, color=cfg.GOLD), run_time=0.45)
    narration_wait(scene, 0.25)

    eq2 = MathTex(r"3\times(-4)=-12", font_size=48)
    eq2.set_color_by_tex("-", cfg.NEGATIVE)
    eq2.next_to(title, DOWN, buff=0.4)
    paced_play(scene, ReplacementTransform(eq, eq2), particle.animate.move_to(line.n2p(0)), run_time=0.75)
    for step in particle_motion_1d(0, -4, 3):
        _jump(scene, particle, line, step.start, step.end, cfg.NEGATIVE)
    paced_play(scene, Flash(particle, color=cfg.NEGATIVE), run_time=0.45)
    narration_wait(scene, 0.75)
    scene_transition(scene)


class Scene02MultiplicationAsMotion(Scene):
    def construct(self) -> None:
        play_scene(self)
