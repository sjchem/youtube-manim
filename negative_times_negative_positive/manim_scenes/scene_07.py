from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, narration_wait, paced_play, scene_transition


def _cracks() -> VGroup:
    segments = [
        ([0, 1.8, 0], [0.28, 0.9, 0]),
        ([0.28, 0.9, 0], [-0.25, 0.15, 0]),
        ([-0.25, 0.15, 0], [0.15, -0.8, 0]),
        ([0.28, 0.9, 0], [0.95, 0.32, 0]),
        ([-0.25, 0.15, 0], [-1.0, -0.55, 0]),
    ]
    return VGroup(*[Line(a, b, color=cfg.COLORS["warning"], stroke_width=5, stroke_opacity=0.85) for a, b in segments])


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = Text("What if it were negative?", font_size=42, color=cfg.COLORS["warning"]).to_edge(UP)
    paced_play(scene, FadeIn(title))

    suppose = MathTex(r"\text{Suppose}\quad(-3)(-5)=-15", font_size=46)
    suppose.set_color_by_tex("-", cfg.NEGATIVE)
    suppose.move_to(UP * 1.8)
    paced_play(scene, Write(suppose), run_time=0.9)

    sub = MathTex(r"-15+(-3)(-5)=-15+(-15)", font_size=42)
    sub.set_color_by_tex("-", cfg.NEGATIVE)
    sub.next_to(suppose, DOWN, buff=0.55)
    bad = MathTex(r"-15+(-15)=-30", font_size=48)
    bad.set_color_by_tex("-", cfg.NEGATIVE)
    bad.next_to(sub, DOWN, buff=0.35)
    paced_play(scene, FadeIn(sub, shift=DOWN * 0.15), run_time=0.75)
    paced_play(scene, TransformMatchingTex(sub.copy(), bad), run_time=0.8)

    original = MathTex(r"-3(5+(-5))=0", font_size=48)
    original.set_color_by_tex("-", cfg.NEGATIVE)
    original.set_color_by_tex("0", cfg.ZERO)
    contradiction = MathTex(r"0\neq -30", font_size=68, color=cfg.COLORS["warning"]).to_edge(DOWN, buff=0.7)
    paced_play(scene, Write(original.next_to(bad, DOWN, buff=0.5)), run_time=0.7)
    paced_play(scene, Write(contradiction), run_time=0.6)

    cracks = _cracks()
    warnings = VGroup(
        Text("Pattern breaks", font_size=24, color=cfg.COLORS["warning"]),
        Text("Distributive law breaks", font_size=24, color=cfg.COLORS["warning"]),
        Text("Arithmetic collapses", font_size=24, color=cfg.COLORS["warning"]),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.8)
    paced_play(scene, Create(cracks), LaggedStart(*[FadeIn(w, shift=LEFT * 0.15) for w in warnings], lag_ratio=0.14), run_time=1.0)
    paced_play(scene, Wiggle(bad), Flash(contradiction, color=cfg.COLORS["warning"]), run_time=0.9)
    narration_wait(scene, 0.7)
    scene_transition(scene)


class Scene07BrokenUniverse(Scene):
    def construct(self) -> None:
        play_scene(self)
