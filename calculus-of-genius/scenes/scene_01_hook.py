from __future__ import annotations

from manim import *

from utils.equations import probability_success_equation
from utils.helpers import jagged_path
from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, MUTED_TEXT, PURPLE_GLOW, RED_GLOW, TEXT_COLOR, glow_text, set_scene_style, soft_panel


class HookScene(MovingCameraScene):
    """Creativity shifts from mythic lightning to statistical machinery."""

    def construct(self) -> None:
        set_scene_style(self)

        lightning = jagged_path(UP * 3.4 + LEFT * 3, DOWN * 1.3 + RIGHT * 0.4, segments=15, seed=21)
        halo = lightning.copy().set_stroke(GOLD_GLOW, width=16, opacity=0.18)
        self.play(Create(halo), Create(lightning), run_time=0.9)
        self.play(Flash(lightning.get_end(), color=GOLD_GLOW, flash_radius=1.3), run_time=0.8)

        symbols = VGroup(
            MathTex(r"P(\mathrm{success})", font_size=34, color=BLUE_GLOW),
            MathTex(r"n\ \mathrm{attempts}", font_size=34, color=GREEN_GLOW),
            MathTex(r"{n\choose k}", font_size=34, color=PURPLE_GLOW),
            MathTex(r"H", font_size=40, color=GOLD_GLOW),
        ).arrange(RIGHT, buff=0.55).move_to(UP * 1.6)
        self.play(Transform(VGroup(halo, lightning), symbols), run_time=1.2)

        left_panel = soft_panel(5.6, 2.5, RED_GLOW).move_to(LEFT * 3.2 + DOWN * 0.7)
        right_panel = soft_panel(5.6, 2.5, GREEN_GLOW).move_to(RIGHT * 3.2 + DOWN * 0.7)
        myth = VGroup(
            Text("Myth", font_size=30, color=RED_GLOW, weight=BOLD),
            Text("Genius is random", font_size=28, color=TEXT_COLOR),
            Text("a rare accident", font_size=20, color=MUTED_TEXT),
        ).arrange(DOWN, buff=0.18).move_to(left_panel.get_center())
        reality = VGroup(
            Text("Reality", font_size=30, color=GREEN_GLOW, weight=BOLD),
            Text("Genius is statistical", font_size=28, color=TEXT_COLOR),
            Text("rare, but not unmeasurable", font_size=20, color=MUTED_TEXT),
        ).arrange(DOWN, buff=0.18).move_to(right_panel.get_center())
        self.play(FadeIn(left_panel), FadeIn(right_panel), FadeIn(myth), FadeIn(reality), run_time=1.2)

        equation = probability_success_equation(46).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(glow_text(equation, BLUE_GLOW, opacity=0.17), shift=UP * 0.2), run_time=1.2)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.72).move_to(equation), run_time=1.6)
        self.wait(21.0)
        self.play(Restore(self.camera.frame), run_time=1.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
