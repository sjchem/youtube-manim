from manim import *

import config as cfg
from manim_scenes.common import arrow_between, cinematic_background, info_card, labeled_box, narration_wait, paced_play, scene_title, scene_transition, simple_model, warning_label


def _split_box(title: str, percent: str, width: float, color: str) -> VGroup:
    box = RoundedRectangle(
        corner_radius=cfg.VISUAL["corner_radius"],
        width=width,
        height=0.95,
        fill_color=cfg.COLORS["panel"],
        fill_opacity=0.85,
        stroke_color=color,
        stroke_width=2.5,
    )
    title_text = Text(title, font_size=22, color=cfg.TEXT, weight=BOLD)
    percent_text = Text(percent, font_size=22, color=cfg.TEXT, weight=BOLD)
    content = VGroup(title_text, percent_text).arrange(DOWN, buff=0.01)
    if content.width > width - 0.3:
        content.scale_to_fit_width(width - 0.3)
    content.move_to(box)
    return VGroup(box, content)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("Training, validation, and test sets").to_edge(UP)
    title.scale_to_fit_width(12.6).to_edge(UP, buff=0.12)
    dataset = RoundedRectangle(corner_radius=0.16, width=6.8, height=0.88, fill_color=cfg.COLORS["panel_alt"], fill_opacity=0.92, stroke_color=cfg.BLUE, stroke_width=3)
    dataset_label = Text("Dataset", font_size=31, color=cfg.TEXT, weight=BOLD).move_to(dataset)
    dataset_group = VGroup(dataset, dataset_label).move_to(UP * 1.65)

    train = _split_box("Training Set", "70%", 2.5, cfg.GREEN).move_to([-3.65, 0.62, 0])
    valid = _split_box("Validation Set", "15%", 2.55, cfg.YELLOW).move_to([0, 0.62, 0])
    test = _split_box("Test Set", "15%", 2.25, cfg.PURPLE).move_to([3.65, 0.62, 0])
    splits = VGroup(train, valid, test)

    model = simple_model("Model").scale(0.88).move_to([-3.65, -2.02, 0])
    settings = labeled_box("settings", 1.7, 0.76, cfg.YELLOW, 20).move_to([0, -2.02, 0])
    score = labeled_box("final\nperformance", 2.0, 0.9, cfg.PURPLE, 20).move_to([3.65, -2.02, 0])
    warning = warning_label().scale(0.9).move_to([0, 2.62, 0])
    role_cards = VGroup(
        info_card("Training", ["fits parameters"], 2.25, cfg.GREEN, 20, 15).move_to([-3.65, -0.78, 0]),
        info_card("Validation", ["chooses settings"], 2.35, cfg.YELLOW, 20, 15).move_to([0, -0.78, 0]),
        info_card("Test", ["final estimate"], 2.15, cfg.PURPLE, 20, 15).move_to([3.65, -0.78, 0]),
    )
    flows = VGroup(
        arrow_between(role_cards[0].get_bottom(), model.get_top(), cfg.GREEN),
        arrow_between(role_cards[1].get_bottom(), settings.get_top(), cfg.YELLOW),
        arrow_between(role_cards[2].get_bottom(), score.get_top(), cfg.PURPLE),
    )
    slice_warning = info_card("Clean split is not enough", ["wrong original data -> wrong slices"], 4.2, cfg.WARNING, 21, 16).move_to([0, -3.3, 0])

    paced_play(scene, FadeIn(title), FadeIn(dataset_group), run_time=0.75)
    paced_play(scene, ReplacementTransform(dataset_group.copy(), splits), run_time=1.0)
    paced_play(scene, FadeIn(role_cards, lag_ratio=0.08), FadeIn(warning, shift=DOWN * 0.12), run_time=0.65)
    paced_play(scene, FadeIn(VGroup(model, settings, score)), FadeIn(flows, lag_ratio=0.12), run_time=1.1)
    paced_play(scene, FadeIn(slice_warning, shift=UP * 0.12), run_time=0.55)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene07TrainValidationTest(Scene):
    def construct(self) -> None:
        play_scene(self)
