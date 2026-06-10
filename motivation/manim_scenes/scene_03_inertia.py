from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SECONDARY_GLOW, SUCCESS_COLOR, TEXT_COLOR, WARNING_COLOR
from manim_scenes.common import (
    force_arrow,
    friction_arrow,
    label_badge,
    motion_trail,
    rolling_ball,
    set_scene_style,
    soft_background,
    surface_line,
)


def _desk_metaphor():
    desk = Line(LEFT * 2.5, RIGHT * 2.5, color="#384052", stroke_width=5)
    legs = VGroup(
        Line(LEFT * 2.2, LEFT * 2.2 + DOWN * 0.8, color="#384052", stroke_width=4),
        Line(RIGHT * 2.2, RIGHT * 2.2 + DOWN * 0.8, color="#384052", stroke_width=4),
    )
    notebook = Rectangle(width=1.0, height=0.6, color=PRIMARY_GLOW).set_fill(PRIMARY_GLOW, 0.08)
    notebook.move_to(LEFT * 0.75 + UP * 0.38)
    phone = RoundedRectangle(corner_radius=0.08, width=0.42, height=0.75, color=WARNING_COLOR)
    phone.set_fill(WARNING_COLOR, 0.12).move_to(RIGHT * 0.8 + UP * 0.45)
    hill = ArcBetweenPoints(RIGHT * 1.35 + DOWN * 0.02, RIGHT * 2.45 + UP * 0.45, angle=-PI / 5, color=SECONDARY_GLOW)
    label = Text("task", font_size=18, color=SECONDARY_GLOW).next_to(hill, UP, buff=0.1)
    return VGroup(desk, legs, notebook, phone, hill, label)


def play_scene(scene: Scene):
    set_scene_style(scene)
    scene.add(soft_background())

    title = Text("Starting is the hardest part", font_size=34, color=TEXT_COLOR).to_edge(UP, buff=0.6)
    surface = surface_line(width=7.5, y=-1.65)
    ball = rolling_ball(radius=0.27, color=PRIMARY_GLOW).move_to(surface.get_left() + RIGHT * 1.05 + UP * 0.3)
    rest = Text("Rest resists change.", font_size=34, color=DIM_TEXT_COLOR).next_to(surface, UP, buff=1.05)

    scene.play(Write(title), Create(surface), FadeIn(ball), run_time=2.0)
    scene.play(FadeIn(rest), run_time=1.1)
    scene.wait(1.5)

    weak = force_arrow(
        ball.get_right() + RIGHT * 0.08,
        ball.get_right() + RIGHT * 1.2,
        color=SECONDARY_GLOW,
        label="weak push",
        label_font_size=26,
    )
    weak[-1].shift(UP * 0.12)
    scene.play(FadeIn(weak), run_time=0.8)
    scene.play(ball.animate.shift(RIGHT * 0.22), run_time=0.7)
    scene.play(ball.animate.shift(LEFT * 0.14), FadeOut(weak), run_time=0.8)

    strong = force_arrow(
        ball.get_right() + RIGHT * 0.1,
        ball.get_right() + RIGHT * 2.05,
        color=PRIMARY_GLOW,
        label="motivation",
        label_font_size=26,
    )
    strong[-1].shift(UP * 0.12)
    trail = motion_trail([ball.get_center(), ball.get_center() + RIGHT * 0.65, ball.get_center() + RIGHT * 1.45], color=PRIMARY_GLOW)
    scene.play(FadeIn(strong), run_time=0.8)
    scene.play(ball.animate.shift(RIGHT * 1.75), FadeIn(trail), run_time=1.4)
    scene.play(FadeOut(strong), run_time=0.5)

    drag = friction_arrow(
        ball.get_left() + LEFT * 0.08,
        ball.get_left() + LEFT * 1.35,
        label="resistance",
        label_font_size=26,
    )
    drag[-1].shift(LEFT * 0.12 + UP * 0.14)
    scene.play(FadeIn(drag), run_time=0.8)
    scene.play(ball.animate.shift(RIGHT * 0.45), drag.animate.shift(RIGHT * 0.45), run_time=1.3)
    scene.play(FadeOut(drag), run_time=0.6)

    law = MathTex(r"\text{object at rest}", r"\rightarrow", r"\text{stays at rest}", color=TEXT_COLOR).scale(0.72)
    law.to_edge(DOWN, buff=0.55)
    scene.play(Write(law), run_time=1.6)
    scene.wait(2.0)

    desk = _desk_metaphor().scale(1.05).move_to(DOWN * 0.15)
    badge = label_badge("same physics-inspired pattern", color=SUCCESS_COLOR).to_edge(DOWN, buff=0.7)
    scene.play(FadeOut(VGroup(surface, ball, trail, rest, law)), FadeIn(desk, shift=UP * 0.2), FadeIn(badge), run_time=2.0)
    scene.wait(4.0)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)


class Scene03Inertia(Scene):
    def construct(self):
        play_scene(self)
