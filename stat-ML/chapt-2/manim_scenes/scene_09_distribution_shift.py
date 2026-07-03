from manim import *

import config as cfg
from manim_scenes.common import bell_curve, cinematic_background, icon_tile, info_card, narration_wait, paced_play, scene_title, scene_transition, simple_model


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("Distribution shift").to_edge(UP, buff=0.12)
    subtitle = Text("the model stays fixed while the world moves", font_size=25, color=cfg.MUTED).move_to([0, 2.72, 0])
    timeline = NumberLine(x_range=[2023, 2026, 1], length=7.7, include_numbers=True, font_size=18, color=cfg.MUTED).move_to([0, 1.38, 0])
    train_curve = bell_curve(cfg.BLUE, shift_x=-0.8, stretch=0.75).scale(0.95).move_to([-3.25, -0.05, 0])
    real_curve = bell_curve(cfg.GREEN, shift_x=-0.8, stretch=0.75).scale(0.95).move_to([3.25, -0.05, 0])
    shifted_curve = bell_curve(cfg.WARNING, shift_x=0.9, stretch=0.95, skew=0.35).scale(0.95).move_to([3.25, -0.05, 0])
    train_label = MathTex(r"P_{\mathrm{train}}(X)", font_size=31, color=cfg.BLUE).next_to(train_curve, DOWN, buff=0.12)
    real_label = MathTex(r"P_{\mathrm{real\ world}}(X)", font_size=31, color=cfg.GREEN).next_to(real_curve, DOWN, buff=0.12)
    equation = MathTex(r"P_{\mathrm{train}}(X)\neq P_{\mathrm{real\ world}}(X)", font_size=33, color=cfg.TEXT).to_edge(DOWN, buff=0.28)
    model = simple_model("Fixed model").scale(0.74).move_to([0, -1.05, 0])

    examples = VGroup(
        icon_tile("fraud", "$", cfg.RED, 1.25),
        icon_tile("customers", "#", cfg.GREEN, 1.45),
        icon_tile("sensors", "S", cfg.YELLOW, 1.25),
        icon_tile("weather", "*", cfg.BLUE, 1.3),
    ).arrange(RIGHT, buff=0.25).scale(0.82).move_to([0, 2.08, 0])
    fixed_card = info_card("Fixed model", ["same weights", "new world"], 2.55, cfg.PURPLE, 20, 15).move_to([0, -2.45, 0])
    monitoring = info_card("After deployment", ["monitor inputs", "compare to training", "retrain when needed"], 3.35, cfg.GREEN, 21, 16).move_to([4.75, -2.45, 0])
    shift_causes = info_card("Why it shifts", ["new behavior", "new devices", "policy changes"], 3.05, cfg.WARNING, 21, 16).move_to([-4.75, -2.45, 0])

    paced_play(scene, FadeIn(title), FadeIn(subtitle), Create(timeline), FadeIn(examples, lag_ratio=0.08), run_time=0.9)
    paced_play(scene, FadeIn(train_curve), FadeIn(real_curve), FadeIn(train_label), FadeIn(real_label), FadeIn(model), FadeIn(fixed_card), run_time=0.9)
    paced_play(scene, ReplacementTransform(real_curve, shifted_curve), real_label.animate.set_color(cfg.WARNING), examples.animate.shift(RIGHT * 0.12), FadeIn(shift_causes, shift=RIGHT * 0.12), run_time=1.25)
    paced_play(scene, FadeIn(monitoring, shift=LEFT * 0.12), Write(equation), run_time=0.75)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene09DistributionShift(Scene):
    def construct(self) -> None:
        play_scene(self)
