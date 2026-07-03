from manim import *

import config as cfg
from manim_scenes.common import (
    PALETTE,
    arrow_between,
    cinematic_background,
    dataset_table,
    info_card,
    labeled_box,
    narration_wait,
    paced_play,
    scene_title,
    scene_transition,
)


def _machine() -> VGroup:
    body = RoundedRectangle(corner_radius=0.22, width=3.2, height=2.1, fill_color=cfg.COLORS["panel_alt"], fill_opacity=0.9, stroke_color=cfg.BLUE, stroke_width=3)
    title = Text("real-world\nprocess", font_size=25, color=cfg.TEXT, weight=BOLD, line_spacing=0.8).shift(UP * 0.24)
    gears = VGroup(
        Circle(radius=0.24, color=cfg.YELLOW).shift(LEFT * 0.75 + DOWN * 0.72),
        Circle(radius=0.17, color=cfg.GREEN).shift(LEFT * 0.25 + DOWN * 0.72),
        Circle(radius=0.14, color=cfg.PURPLE).shift(RIGHT * 0.18 + DOWN * 0.72),
    )
    return VGroup(body, title, gears)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("The hidden data-generating process").to_edge(UP)
    machine = _machine().move_to(ORIGIN)

    input_labels = ["Environment", "Human behavior", "Time", "Sensors", "Randomness"]
    inputs = VGroup()
    for index, label in enumerate(input_labels):
        y = 2.15 - index * 0.78
        source = Text(label, font_size=20, color=cfg.MUTED).move_to([-5.35, y, 0])
        arrow = arrow_between(source.get_right() + RIGHT * 0.1, machine.get_left() + UP * (y * 0.28), cfg.BLUE)
        inputs.add(VGroup(source, arrow))

    output_labels = ["images", "transactions", "medical records", "sensor signals"]
    outputs = VGroup()
    for index, label in enumerate(output_labels):
        y = 1.45 - index * 0.82
        box = labeled_box(label, 1.9, 0.52, PALETTE[index], 16).move_to([4.55, y, 0])
        arrow = arrow_between(machine.get_right() + UP * (y * 0.18), box.get_left() + LEFT * 0.1, PALETTE[index])
        outputs.add(VGroup(arrow, box))

    dataset = dataset_table(3, 5, colors=[cfg.BLUE, cfg.GREEN, cfg.YELLOW]).scale(0.8).move_to([4.7, -2.1, 0])
    dataset_box = labeled_box("Dataset", 2.1, 0.78, cfg.YELLOW).move_to([4.7, -3.0, 0])
    few_arrow = arrow_between(outputs[1].get_center() + DOWN * 0.4, dataset.get_top(), cfg.YELLOW)
    few_label = Text("a few outputs", font_size=16, color=cfg.YELLOW, weight=BOLD).move_to([3.35, -1.55, 0])
    few_outputs = VGroup(few_arrow, few_label)
    message = equation_box = MathTex(r"\mathrm{Reality}\to\mathrm{Data}\to\mathrm{Dataset}", font_size=34, color=cfg.TEXT).to_edge(DOWN, buff=0.32)
    process_card = info_card("Data can be shaped by", ["lighting", "business rules", "missing labels", "sensor drift"], 3.35, cfg.WARNING, 20, 16).move_to([-4.4, -2.2, 0])
    loss_card = info_card("Not all reality is stored", ["dropped events", "delayed records", "unmeasured causes"], 3.45, cfg.YELLOW, 20, 16).move_to([-0.25, -2.2, 0])

    paced_play(scene, FadeIn(title), FadeIn(machine), run_time=0.8)
    paced_play(scene, FadeIn(inputs, lag_ratio=0.08), run_time=1.0)
    paced_play(scene, FadeIn(process_card, shift=RIGHT * 0.12), run_time=0.55)
    paced_play(scene, FadeIn(outputs, lag_ratio=0.09), run_time=1.05)
    paced_play(scene, FadeIn(few_outputs), FadeIn(dataset), FadeIn(dataset_box), FadeIn(loss_card, shift=UP * 0.12), run_time=0.9)
    paced_play(scene, Write(message), run_time=0.75)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene04DataProcess(Scene):
    def construct(self) -> None:
        play_scene(self)
