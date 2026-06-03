from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, create_vector_arrow, narration_wait, paced_play, scene_transition


def _mirror(x: float) -> VGroup:
    pane = Line([x, -2.2, 0], [x, 2.2, 0], stroke_color=cfg.POSITIVE, stroke_width=5)
    glow = pane.copy().set_stroke(cfg.POSITIVE, width=16, opacity=0.12)
    shine = VGroup(*[Line([x - 0.18, y, 0], [x + 0.18, y + 0.34, 0], color=cfg.GOLD, stroke_opacity=0.45) for y in [-1.4, -0.3, 0.8]])
    return VGroup(glow, pane, shine)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = Text("The mirror room", font_size=42, color=cfg.ZERO).to_edge(UP)
    m1 = _mirror(-1.9)
    m2 = _mirror(1.9)
    paced_play(scene, FadeIn(title), FadeIn(m1), FadeIn(m2), run_time=0.9)

    arrow_a = create_vector_arrow(LEFT * 3.6 + DOWN * 0.15, LEFT * 2.25 + DOWN * 0.15, cfg.POSITIVE, "+a")
    arrow_b = create_vector_arrow(LEFT * 1.55 + DOWN * 0.15, LEFT * 0.2 + DOWN * 0.15, cfg.NEGATIVE, "-a")
    arrow_c = create_vector_arrow(RIGHT * 2.25 + DOWN * 0.15, RIGHT * 3.6 + DOWN * 0.15, cfg.POSITIVE, "+a")
    paced_play(scene, FadeIn(arrow_a, shift=RIGHT * 0.2), run_time=0.7)
    paced_play(scene, Flash(m1, color=cfg.POSITIVE), ReplacementTransform(arrow_a.copy(), arrow_b), run_time=0.9)
    paced_play(scene, Flash(m2, color=cfg.POSITIVE), ReplacementTransform(arrow_b.copy(), arrow_c), run_time=0.9)

    eq1 = MathTex(r"-(-a)=a", font_size=52)
    eq1.set_color_by_tex("-", cfg.NEGATIVE)
    eq1.set_color_by_tex("a", cfg.GOLD)
    eq1.to_edge(DOWN)
    paced_play(scene, Write(eq1), run_time=0.8)
    eq2 = MathTex(r"(-a)(-b)=ab", font_size=56)
    eq2.set_color_by_tex("-", cfg.NEGATIVE)
    eq2.set_color_by_tex("ab", cfg.GOLD)
    eq2.to_edge(DOWN)
    paced_play(scene, TransformMatchingTex(eq1, eq2), run_time=1.0)
    narration_wait(scene, 0.8)
    scene_transition(scene)


class Scene04MirrorRoom(Scene):
    def construct(self) -> None:
        play_scene(self)
