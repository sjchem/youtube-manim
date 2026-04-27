from manim import *
import random


class SecondLawIntro(Scene):
    """Title card: entropy always increases."""

    def construct(self):
        title = Text("2nd Law of Thermodynamics", font_size=48, color=YELLOW)
        subtitle = Text(
            "The total entropy of an isolated system\nalways increases over time.",
            font_size=30,
            color=WHITE,
            line_spacing=1.4,
        ).next_to(title, DOWN, buff=0.6)

        self.play(Write(title))
        self.wait(0.4)
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.wait(2.5)
        self.play(FadeOut(title), FadeOut(subtitle))


class EntropyScene(Scene):
    """Ordered dots → disordered dots to visualise entropy increase."""

    NUM_DOTS = 18
    SEED = 42

    def construct(self):
        random.seed(self.SEED)

        # ── Header ────────────────────────────────────────────────────────────
        header = Text("Order → Disorder", font_size=36, color=YELLOW).to_edge(UP, buff=0.35)
        self.play(Write(header))

        # ── Left panel: ordered grid ──────────────────────────────────────────
        ordered_label = Text("Low Entropy\n(Ordered)", font_size=26, color=GREEN).move_to(
            LEFT * 4.5 + UP * 1.2
        )
        ordered_box = Rectangle(width=3.2, height=3.2, color=GREEN, fill_opacity=0.1).move_to(
            LEFT * 4.5 + DOWN * 0.4
        )

        cols, rows = 6, 3
        ordered_dots = VGroup(
            *[
                Dot(radius=0.18, color=BLUE_B).move_to(
                    ordered_box.get_center()
                    + RIGHT * ((i % cols - 2.5) * 0.46)
                    + UP * ((1 - i // cols) * 0.75)
                )
                for i in range(self.NUM_DOTS)
            ]
        )

        self.play(
            DrawBorderThenFill(ordered_box),
            Write(ordered_label),
        )
        self.play(LaggedStartMap(GrowFromCenter, ordered_dots, lag_ratio=0.07))
        self.wait(0.5)

        # ── Right panel: disordered scatter ───────────────────────────────────
        disordered_label = Text("High Entropy\n(Disordered)", font_size=26, color=RED_B).move_to(
            RIGHT * 4.5 + UP * 1.2
        )
        disordered_box = Rectangle(width=3.2, height=3.2, color=RED_D, fill_opacity=0.1).move_to(
            RIGHT * 4.5 + DOWN * 0.4
        )

        scatter_positions = [
            disordered_box.get_center()
            + RIGHT * random.uniform(-1.2, 1.2)
            + UP * random.uniform(-1.2, 1.2)
            for _ in range(self.NUM_DOTS)
        ]

        disordered_dots = VGroup(
            *[
                Dot(radius=0.18, color=ORANGE).move_to(scatter_positions[i])
                for i in range(self.NUM_DOTS)
            ]
        )

        self.play(
            DrawBorderThenFill(disordered_box),
            Write(disordered_label),
        )

        # ── Arrow with "time passes" ───────────────────────────────────────────
        arrow = Arrow(
            start=ordered_box.get_right(),
            end=disordered_box.get_left(),
            color=YELLOW,
            buff=0.15,
        )
        time_label = Text("time passes", font_size=22, color=YELLOW).next_to(arrow, UP, buff=0.15)
        self.play(GrowArrow(arrow), FadeIn(time_label))

        # Animate ordered dots moving to scattered positions
        self.play(
            LaggedStart(
                *[
                    ordered_dots[i].animate.move_to(scatter_positions[i])
                    for i in range(self.NUM_DOTS)
                ],
                lag_ratio=0.06,
            ),
            run_time=2.0,
        )
        # Swap colour to orange to show they've become "disordered"
        self.play(
            LaggedStart(
                *[ordered_dots[i].animate.set_color(ORANGE) for i in range(self.NUM_DOTS)],
                lag_ratio=0.04,
            ),
            run_time=0.8,
        )
        self.wait(0.5)

        # ── Reversible note ───────────────────────────────────────────────────
        note = Text(
            "In ideal reversible processes, entropy stays constant.",
            font_size=22,
            color=GRAY_B,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class SecondLawEquation(Scene):
    """ΔS ≥ 0 with annotations."""

    def construct(self):
        # ── Main equation (large) ─────────────────────────────────────────────
        equation = MathTex(
            r"\Delta S", r"\geq", r"0",
            font_size=120,
        )
        equation.set_color_by_tex(r"\Delta S", YELLOW)
        equation.set_color_by_tex(r"\geq", WHITE)
        equation.set_color_by_tex("0", GREEN)
        equation.move_to(ORIGIN + UP * 0.6)

        self.play(Write(equation), run_time=1.5)
        self.wait(0.5)

        # ── Term labels ────────────────────────────────────────────────────────
        ds_label = Text("Change in\nentropy", font_size=26, color=YELLOW)
        zero_label = Text("Never\ndecreases", font_size=26, color=GREEN)

        ds_label.next_to(equation[0], DOWN, buff=1.1)
        zero_label.next_to(equation[2], DOWN, buff=1.1)

        arrow_ds = Arrow(ds_label.get_top(), equation[0].get_bottom(), buff=0.1, color=YELLOW)
        arrow_zero = Arrow(zero_label.get_top(), equation[2].get_bottom(), buff=0.1, color=GREEN)

        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arrow_ds), FadeIn(ds_label, shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arrow_zero), FadeIn(zero_label, shift=DOWN * 0.2)),
                lag_ratio=0.4,
            )
        )
        self.wait(0.8)

        # ── Two sub-cases ──────────────────────────────────────────────────────
        case_irreversible = MathTex(r"\Delta S > 0", font_size=36, color=RED_B).shift(
            LEFT * 3 + DOWN * 2.6
        )
        case_reversible = MathTex(r"\Delta S = 0", font_size=36, color=BLUE_B).shift(
            RIGHT * 3 + DOWN * 2.6
        )
        irrev_note = Text("Irreversible\n(real processes)", font_size=20, color=RED_B).next_to(
            case_irreversible, DOWN, buff=0.2
        )
        rev_note = Text("Reversible\n(ideal only)", font_size=20, color=BLUE_B).next_to(
            case_reversible, DOWN, buff=0.2
        )

        self.play(
            LaggedStart(
                AnimationGroup(Write(case_irreversible), FadeIn(irrev_note)),
                AnimationGroup(Write(case_reversible), FadeIn(rev_note)),
                lag_ratio=0.4,
            )
        )
        self.wait(1.0)

        # ── Closing statement ──────────────────────────────────────────────────
        closing = Text(
            "Disorder always wins — that's the universe.", font_size=28, color=WHITE
        ).to_edge(UP, buff=0.4)
        self.play(Write(closing))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


class BoltzmannEquation(Scene):
    """S = k log W — Boltzmann's deep entropy formula."""

    def construct(self):
        # ── Title ─────────────────────────────────────────────────────────────
        title = Text("Boltzmann's Entropy Formula", font_size=38, color=YELLOW).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # ── Main equation ─────────────────────────────────────────────────────
        equation = MathTex(
            r"S", r"=", r"k_B", r"\log", r"W",
            font_size=110,
        )
        equation.set_color_by_tex("S", YELLOW)
        equation.set_color_by_tex(r"k_B", TEAL)
        equation.set_color_by_tex(r"\log", WHITE)
        equation.set_color_by_tex("W", ORANGE)
        equation.move_to(ORIGIN + UP * 0.3)
        self.play(Write(equation), run_time=1.4)
        self.wait(0.4)

        # ── Labels ────────────────────────────────────────────────────────────
        s_label = Text("Entropy", font_size=24, color=YELLOW)
        k_label = Text("Boltzmann\nconstant", font_size=24, color=TEAL)
        w_label = Text("Number of\nmicrostates (W)", font_size=24, color=ORANGE)

        s_label.next_to(equation[0], DOWN, buff=1.0)
        k_label.next_to(equation[2], DOWN, buff=1.0)
        w_label.next_to(equation[4], DOWN, buff=1.0)

        arrow_s = Arrow(s_label.get_top(), equation[0].get_bottom(), buff=0.1, color=YELLOW)
        arrow_k = Arrow(k_label.get_top(), equation[2].get_bottom(), buff=0.1, color=TEAL)
        arrow_w = Arrow(w_label.get_top(), equation[4].get_bottom(), buff=0.1, color=ORANGE)

        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arrow_s), FadeIn(s_label, shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arrow_k), FadeIn(k_label, shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arrow_w), FadeIn(w_label, shift=DOWN * 0.2)),
                lag_ratio=0.35,
            )
        )
        self.wait(0.6)

        # ── Insight note ──────────────────────────────────────────────────────
        note = Text(
            "More ways to arrange things  →  higher entropy",
            font_size=24,
            color=GRAY_A,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class EntropyGraphScene(Scene):
    """Bar chart: configurations vs probability — clean≈0, messy=spike."""

    def construct(self):
        title = Text("Configurations vs Probability", font_size=34, color=YELLOW).to_edge(
            UP, buff=0.35
        )
        self.play(Write(title))

        # ── Axes ──────────────────────────────────────────────────────────────
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.15, 0.25],
            x_length=7.5,
            y_length=3.6,
            axis_config={"color": WHITE, "include_ticks": False},
            tips=True,
        ).shift(UP * 0.1)

        x_label = Text("Configurations  (W)", font_size=22, color=WHITE).next_to(
            axes.x_axis, DOWN, buff=0.35
        )
        y_label = (
            Text("Probability", font_size=22, color=WHITE)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=0.35)
        )
        self.play(Create(axes), Write(x_label), Write(y_label))

        # ── Bar data: heights represent probability of each "configuration bucket"
        # Bucket 0-1: clean/ordered  → near zero
        # Bucket 8-9: messy/disordered → huge spike
        bar_heights = [0.04, 0.03, 0.06, 0.05, 0.07, 0.09, 0.12, 0.18, 0.95, 1.0]
        bar_colors  = [GREEN if i < 2 else (YELLOW if i < 7 else RED_B) for i in range(len(bar_heights))]

        bars = VGroup()
        bar_width = 0.72
        for i, (h, col) in enumerate(zip(bar_heights, bar_colors)):
            bar = Rectangle(
                width=bar_width,
                height=h * axes.y_length,
                color=col,
                fill_color=col,
                fill_opacity=0.85,
                stroke_width=1,
            )
            bar.move_to(
                axes.c2p(i + 0.5, 0) + UP * (h * axes.y_length / 2)
            )
            bars.add(bar)

        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.08), run_time=1.8)
        self.wait(0.3)

        # ── Annotation: Clean ─────────────────────────────────────────────────
        clean_arrow = Arrow(
            start=axes.c2p(0.5, 0.35),
            end=axes.c2p(0.5, 0.06),
            color=GREEN,
            buff=0.05,
        )
        clean_label = Text("Clean\n(ordered)", font_size=20, color=GREEN).next_to(
            clean_arrow, UP, buff=0.1
        )
        self.play(GrowArrow(clean_arrow), FadeIn(clean_label))

        # ── Annotation: Messy spike ───────────────────────────────────────────
        messy_arrow = Arrow(
            start=axes.c2p(9.0, 0.85) + UP * 0.5,
            end=axes.c2p(9.0, 0.78),
            color=RED_B,
            buff=0.05,
        )
        messy_label = Text("Messy\n(disordered)", font_size=20, color=RED_B).next_to(
            messy_arrow, UP, buff=0.1
        )
        self.play(GrowArrow(messy_arrow), FadeIn(messy_label))
        self.wait(0.5)

        # ── Flash the spike ───────────────────────────────────────────────────
        self.play(
            bars[-1].animate.set_color(YELLOW).set_fill(YELLOW),
            bars[-2].animate.set_color(YELLOW).set_fill(YELLOW),
            run_time=0.4,
        )
        self.play(
            bars[-1].animate.set_color(RED_B).set_fill(RED_B),
            bars[-2].animate.set_color(RED_B).set_fill(RED_B),
            run_time=0.4,
        )

        caption = Text(
            "Nature overwhelmingly prefers disorder.", font_size=24, color=GRAY_A
        ).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(caption, shift=UP * 0.2))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class SecondLawDeepConcept(Scene):
    """Boltzmann equation + probability graph combined."""

    def construct(self):
        BoltzmannEquation.construct(self)
        EntropyGraphScene.construct(self)


class TotalEntropyEquation(Scene):
    """ΔS_total = ΔS_room + ΔS_you > 0"""

    def construct(self):
        title = Text("Total Entropy Always Increases", font_size=36, color=YELLOW).to_edge(
            UP, buff=0.4
        )
        self.play(Write(title))

        # ── Main equation ─────────────────────────────────────────────────────
        eq = MathTex(
            r"\Delta S_{\text{total}}",
            r"=",
            r"\Delta S_{\text{room}}",
            r"+",
            r"\Delta S_{\text{you}}",
            r">",
            r"0",
            font_size=72,
        )
        eq.set_color_by_tex(r"\Delta S_{\text{total}}", YELLOW)
        eq.set_color_by_tex(r"\Delta S_{\text{room}}", ORANGE)
        eq.set_color_by_tex(r"\Delta S_{\text{you}}", TEAL)
        eq.set_color_by_tex(r">", WHITE)
        eq.set_color_by_tex(r"0", GREEN)
        eq.move_to(ORIGIN + UP * 0.4)

        self.play(Write(eq), run_time=1.6)
        self.wait(0.4)

        # ── Labels ────────────────────────────────────────────────────────────
        lbl_total = Text("Total entropy\nof system", font_size=22, color=YELLOW)
        lbl_room  = Text("Room's\nentropy", font_size=22, color=ORANGE)
        lbl_you   = Text("Your body's\nentropy", font_size=22, color=TEAL)

        lbl_total.next_to(eq[0], DOWN, buff=1.0)
        lbl_room.next_to(eq[2], DOWN, buff=1.0)
        lbl_you.next_to(eq[4], DOWN, buff=1.0)

        arr_total = Arrow(lbl_total.get_top(), eq[0].get_bottom(), buff=0.08, color=YELLOW)
        arr_room  = Arrow(lbl_room.get_top(),  eq[2].get_bottom(), buff=0.08, color=ORANGE)
        arr_you   = Arrow(lbl_you.get_top(),   eq[4].get_bottom(), buff=0.08, color=TEAL)

        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arr_total), FadeIn(lbl_total, shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arr_room),  FadeIn(lbl_room,  shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arr_you),   FadeIn(lbl_you,   shift=DOWN * 0.2)),
                lag_ratio=0.35,
            )
        )
        self.wait(0.5)

        note = Text(
            "Even when you tidy your room, your body creates more disorder.",
            font_size=22, color=GRAY_A,
        ).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class EnergyFlowScene(Scene):
    """Arrow flow: Food → Energy → Work → Heat"""

    def construct(self):
        title = Text("Energy Flow in Your Body", font_size=36, color=YELLOW).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # ── Nodes ─────────────────────────────────────────────────────────────
        labels   = ["Food", "Energy", "Work", "Heat"]
        colors   = [GREEN,  YELLOW,   BLUE_B, RED_B]
        positions = [LEFT * 4.5, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4.5]

        boxes = VGroup()
        texts = VGroup()
        for lbl, col, pos in zip(labels, colors, positions):
            box = RoundedRectangle(
                width=2.2, height=1.0, corner_radius=0.2,
                color=col, fill_color=col, fill_opacity=0.2, stroke_width=2,
            ).move_to(pos)
            txt = Text(lbl, font_size=28, color=col).move_to(pos)
            boxes.add(box)
            texts.add(txt)

        self.play(
            LaggedStart(
                *[AnimationGroup(DrawBorderThenFill(b), Write(t)) for b, t in zip(boxes, texts)],
                lag_ratio=0.2,
            )
        )
        self.wait(0.3)

        # ── Arrows between nodes ──────────────────────────────────────────────
        arrow_colors = [YELLOW, BLUE_B, RED_B]
        for i in range(len(boxes) - 1):
            arr = Arrow(
                start=boxes[i].get_right(),
                end=boxes[i + 1].get_left(),
                color=arrow_colors[i],
                buff=0.1,
                stroke_width=4,
            )
            self.play(GrowArrow(arr), run_time=0.45)

        self.wait(0.4)

        # ── Heat loss note ────────────────────────────────────────────────────
        note = Text(
            "Heat is wasted energy — entropy increases.",
            font_size=22, color=GRAY_A,
        ).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class SecondLawFull(Scene):
    """Runs all segments as a single combined scene."""

    def construct(self):
        SecondLawIntro.construct(self)
        EntropyScene.construct(self)
        SecondLawEquation.construct(self)
        BoltzmannEquation.construct(self)
        EntropyGraphScene.construct(self)
        TotalEntropyEquation.construct(self)
        EnergyFlowScene.construct(self)
