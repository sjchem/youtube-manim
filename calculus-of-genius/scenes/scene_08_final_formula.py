from __future__ import annotations

import numpy as np
from manim import *

from utils.equations import final_creativity_formula, genius_formula
from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, MUTED_TEXT, PURPLE_GLOW, TEXT_COLOR, glow_text, set_scene_style


class FinalFormulaScene(MovingCameraScene):
    """Synthesis and practical takeaway."""

    def construct(self) -> None:
        set_scene_style(self)
        self.camera.frame.save_state()

        icons = VGroup()
        labels = [
            (r"\cdot", "attempts", BLUE_GLOW),
            (r"r^{-s}", "power law", GOLD_GLOW),
            (r"{n\choose k}", "remix", PURPLE_GLOW),
            (r"(1+r)^t", "time", GREEN_GLOW),
            (r"H", "balance", GOLD_GLOW),
        ]
        for i, (symbol, label, color) in enumerate(labels):
            angle = TAU * i / len(labels)
            pos = np.array([np.cos(angle), np.sin(angle), 0]) * 2.35
            token = VGroup(
                Circle(radius=0.42, color=color, fill_color=color, fill_opacity=0.08),
                MathTex(symbol, font_size=32, color=color),
                Text(label, font_size=16, color=MUTED_TEXT).shift(DOWN * 0.68),
            )
            token[0].move_to(pos)
            token[1].move_to(pos)
            token[2].move_to(pos + DOWN * 0.62)
            icons.add(token)

        formula = final_creativity_formula(34)
        formula.move_to(ORIGIN)
        halo = Circle(radius=2.9, color=BLUE_GLOW, stroke_opacity=0.28, stroke_width=3)
        self.play(LaggedStart(*[FadeIn(icon, scale=0.7) for icon in icons], lag_ratio=0.12), Create(halo), run_time=1.8)
        self.play(Rotate(icons, angle=TAU / 8, about_point=ORIGIN), run_time=2.2)
        self.play(FadeIn(glow_text(formula, BLUE_GLOW, opacity=0.16), shift=UP * 0.08), run_time=1.3)
        self.wait(1.0)

        genius = genius_formula(32).move_to(ORIGIN)
        self.play(TransformMatchingTex(formula.copy(), genius), FadeOut(formula), run_time=1.4)
        self.play(icons.animate.scale(0.75).set_opacity(0.55), halo.animate.scale(0.82), run_time=0.9)

        takeaway = Text("Make more. Mix wider. Stay longer. Tune the chaos.", font_size=31, color=TEXT_COLOR)
        takeaway.next_to(genius, DOWN, buff=0.6)
        outro = Text("Subscribe for visual stories about mathematics, AI, and science.", font_size=22, color=MUTED_TEXT)
        outro.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(takeaway, shift=UP * 0.12), run_time=1.0)
        self.play(FadeIn(outro), run_time=0.9)
        self.wait(28.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.1)
