from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SUCCESS_COLOR, TEXT_COLOR, WARNING_COLOR
from manim_scenes.common import curved_loop_arrow, loop_node, set_scene_style, soft_background


def _feedback_loop(labels, center, radius, color):
    nodes = VGroup()
    arrows = VGroup()
    positions = []
    for i, label in enumerate(labels):
        angle = PI / 2 - i * TAU / len(labels)
        pos = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
        positions.append(pos)
        nodes.add(loop_node(label, color=color).move_to(pos))
    for i in range(len(positions)):
        arrows.add(curved_loop_arrow(positions[i], positions[(i + 1) % len(positions)], color=color, angle=-TAU / 10))
    return VGroup(arrows, nodes), positions


def play_scene(scene: Scene):
    set_scene_style(scene)
    scene.add(soft_background())

    title = Text("Discipline is a feedback system", font_size=34, color=TEXT_COLOR).to_edge(UP, buff=0.6)
    scene.play(Write(title), run_time=1.4)

    positive, pos_points = _feedback_loop(
        ["Action", "Progress", "Confidence", "Lower\nFriction", "More\nAction"],
        center=LEFT * 3.35 + DOWN * 0.1,
        radius=1.62,
        color=SUCCESS_COLOR,
    )
    negative, neg_points = _feedback_loop(
        ["Avoidance", "Guilt", "More\nFriction", "More\nAvoidance"],
        center=RIGHT * 3.3 + DOWN * 0.1,
        radius=1.5,
        color=WARNING_COLOR,
    )
    pos_label = Text("positive loop", font_size=23, color=SUCCESS_COLOR).move_to(LEFT * 3.35 + UP * 2.55)
    neg_label = Text("negative loop", font_size=23, color=WARNING_COLOR).move_to(RIGHT * 3.3 + UP * 2.55)

    scene.play(FadeIn(pos_label), Create(positive), run_time=2.2)
    scene.play(FadeIn(neg_label), Create(negative), run_time=2.0)

    pos_particles = VGroup(*[Dot(radius=0.045, color=SUCCESS_COLOR).move_to(pos_points[0]) for _ in range(5)])
    neg_particles = VGroup(*[Dot(radius=0.04, color=WARNING_COLOR).move_to(neg_points[0]) for _ in range(4)])
    scene.add(pos_particles, neg_particles)

    for i in range(5):
        scene.play(
            pos_particles[i].animate.move_to(pos_points[(i + 1) % len(pos_points)]),
            run_time=0.45,
        )
    for i in range(4):
        scene.play(
            neg_particles[i].animate.move_to(neg_points[(i + 1) % len(neg_points)]),
            run_time=0.38,
        )

    scene.play(
        positive.animate.set_opacity(1.0).scale(1.04),
        negative.animate.set_opacity(0.62).scale(0.94),
        run_time=1.4,
    )

    model = MathTex(
        r"M_{tomorrow}",
        "=",
        r"M_{today}",
        "+",
        r"\text{small action}",
        "-",
        r"\text{drag}",
        color=TEXT_COLOR,
    ).scale(0.72)
    model.to_edge(DOWN, buff=0.72)
    model[4].set_color(SUCCESS_COLOR)
    model[6].set_color(DIM_TEXT_COLOR)
    scene.play(Write(model), run_time=1.8)

    compassionate = Text("Progress creates evidence. Evidence changes the next push.", font_size=24, color=DIM_TEXT_COLOR)
    compassionate.next_to(model, UP, buff=0.35)
    scene.play(FadeIn(compassionate), run_time=1.3)
    scene.wait(4.0)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)


class Scene07FeedbackLoop(Scene):
    def construct(self):
        play_scene(self)
