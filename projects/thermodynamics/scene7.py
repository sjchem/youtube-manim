from manim import *


class ThirdLaw(Scene):
    """3rd Law: lim(T→0) S = 0  — short ~12 sec scene."""

    def construct(self):
        # ── Title ─────────────────────────────────────────────────────────────
        title = Text("3rd Law of Thermodynamics", font_size=42, color=YELLOW)
        subtitle = Text(
            "At absolute zero, entropy reaches its minimum.",
            font_size=28, color=WHITE,
        ).next_to(title, DOWN, buff=0.5)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.5)

        # ── Equation ──────────────────────────────────────────────────────────
        eq = MathTex(
            r"\lim_{T \to 0}", r"S", r"=", r"0",
            font_size=110,
        )
        eq.set_color_by_tex(r"\lim", TEAL)
        eq.set_color_by_tex("S", YELLOW)
        eq.set_color_by_tex("0", GREEN)
        eq.move_to(ORIGIN + UP * 0.5)

        self.play(Write(eq), run_time=1.2)
        self.wait(0.4)

        # ── Labels ────────────────────────────────────────────────────────────
        lbl_lim = Text("Temperature\napproaches zero", font_size=22, color=TEAL)
        lbl_s   = Text("Entropy", font_size=22, color=YELLOW)
        lbl_0   = Text("Reaches\nminimum", font_size=22, color=GREEN)

        lbl_lim.next_to(eq[0], DOWN, buff=0.9)
        lbl_s.next_to(eq[1], DOWN, buff=0.9)
        lbl_0.next_to(eq[3], DOWN, buff=0.9)

        arr_lim = Arrow(lbl_lim.get_top(), eq[0].get_bottom(), buff=0.08, color=TEAL)
        arr_s   = Arrow(lbl_s.get_top(),   eq[1].get_bottom(), buff=0.08, color=YELLOW)
        arr_0   = Arrow(lbl_0.get_top(),   eq[3].get_bottom(), buff=0.08, color=GREEN)

        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arr_lim), FadeIn(lbl_lim, shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arr_s),   FadeIn(lbl_s,   shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arr_0),   FadeIn(lbl_0,   shift=DOWN * 0.2)),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(0.5)

        # ── Closing note ──────────────────────────────────────────────────────
        note = Text(
            "Perfect order is only possible at absolute zero.",
            font_size=24, color=GRAY_A,
        ).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.5)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


class ArrowOfTime(Scene):
    """Entropy explains time — ordered → disordered, ~7 sec."""

    def construct(self):
        # ── Header ────────────────────────────────────────────────────────────
        header = Text("Entropy explains time itself.", font_size=36, color=YELLOW)
        header.to_edge(UP, buff=0.45)
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=0.5)

        # ── Time arrow ────────────────────────────────────────────────────────
        time_arrow = Arrow(
            start=LEFT * 5.5, end=RIGHT * 5.5,
            color=WHITE, stroke_width=5, buff=0,
        ).move_to(ORIGIN)
        time_label = Text("Time", font_size=28, color=WHITE).next_to(
            time_arrow, UP, buff=0.2
        ).shift(RIGHT * 4.8)

        self.play(GrowArrow(time_arrow), FadeIn(time_label), run_time=0.7)

        # ── Ordered side (left) ───────────────────────────────────────────────
        ordered_dots = VGroup(
            *[
                Dot(radius=0.16, color=BLUE_B).move_to(
                    LEFT * 4.0 + RIGHT * (i % 3) * 0.45 + DOWN * (1.0 + (i // 3) * 0.45)
                )
                for i in range(9)
            ]
        )
        ordered_lbl = Text("Ordered", font_size=22, color=BLUE_B).next_to(
            ordered_dots, DOWN, buff=0.2
        )

        # ── Disordered side (right) ───────────────────────────────────────────
        import random
        random.seed(7)
        disordered_dots = VGroup(
            *[
                Dot(radius=0.16, color=RED_B).move_to(
                    RIGHT * 2.5
                    + RIGHT * random.uniform(-1.2, 1.2)
                    + DOWN * (1.5 + random.uniform(-0.6, 0.6))
                )
                for _ in range(9)
            ]
        )
        disordered_lbl = Text("Disordered", font_size=22, color=RED_B).next_to(
            disordered_dots, DOWN, buff=0.2
        )

        self.play(
            LaggedStartMap(GrowFromCenter, ordered_dots, lag_ratio=0.06),
            FadeIn(ordered_lbl),
            run_time=0.6,
        )
        self.wait(0.2)

        # Animate dots flying from ordered → disordered positions
        self.play(
            LaggedStart(
                *[
                    ordered_dots[i].animate.move_to(disordered_dots[i].get_center()).set_color(RED_B)
                    for i in range(9)
                ],
                lag_ratio=0.07,
            ),
            FadeIn(disordered_lbl),
            run_time=1.2,
        )
        self.wait(0.3)

        # ── Closing line ──────────────────────────────────────────────────────
        closing = Text(
            "The universe moves forward because entropy grows.",
            font_size=23, color=GRAY_A,
        ).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(closing, shift=UP * 0.15), run_time=0.5)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
