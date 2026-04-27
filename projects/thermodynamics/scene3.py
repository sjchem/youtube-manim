from manim import *


class FirstLawIntro(Scene):
    """Title card: Energy cannot be created or destroyed."""

    def construct(self):
        title = Text("1st Law of Thermodynamics", font_size=48, color=YELLOW)
        subtitle = Text(
            "Energy cannot be created or destroyed—\nonly transformed.",
            font_size=32,
            color=WHITE,
            line_spacing=1.4,
        ).next_to(title, DOWN, buff=0.6)

        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.wait(2.5)
        self.play(FadeOut(title), FadeOut(subtitle))


class MessyRoomScene(Scene):
    """Closet → Floor demo: items move but total count stays constant."""

    NUM_ITEMS = 6

    def construct(self):
        # ── Closet box ──────────────────────────────────────────────────────
        closet_box = Rectangle(width=3.5, height=2.5, color=BLUE_D, fill_opacity=0.25)
        closet_box.move_to(LEFT * 3.5)
        closet_label = Text("Closet", font_size=30, color=BLUE_B).next_to(
            closet_box, UP, buff=0.2
        )

        # ── Floor box ───────────────────────────────────────────────────────
        floor_box = Rectangle(width=3.5, height=2.5, color=RED_D, fill_opacity=0.25)
        floor_box.move_to(RIGHT * 3.5)
        floor_label = Text("Floor", font_size=30, color=RED_B).next_to(
            floor_box, UP, buff=0.2
        )

        # ── Arrow between boxes ─────────────────────────────────────────────
        arrow = Arrow(
            start=closet_box.get_right(),
            end=floor_box.get_left(),
            color=YELLOW,
            buff=0.1,
        )
        arrow_label = Text("items move", font_size=22, color=YELLOW).next_to(
            arrow, UP, buff=0.15
        )

        self.play(
            DrawBorderThenFill(closet_box),
            Write(closet_label),
            DrawBorderThenFill(floor_box),
            Write(floor_label),
        )
        self.play(GrowArrow(arrow), FadeIn(arrow_label))

        # ── Item dots inside closet ──────────────────────────────────────────
        item_colors = [GREEN, ORANGE, PINK, TEAL, MAROON, PURPLE]
        items = VGroup(
            *[
                Circle(radius=0.18, color=item_colors[i], fill_opacity=0.9).move_to(
                    closet_box.get_center()
                    + RIGHT * (((i % 3) - 1) * 0.85)
                    + UP * ((1 - i // 3) * 0.75)
                )
                for i in range(self.NUM_ITEMS)
            ]
        )
        self.play(LaggedStartMap(FadeIn, items, lag_ratio=0.15))
        self.wait(0.4)

        # ── Counter ─────────────────────────────────────────────────────────
        counter_label = Text("Total items: ", font_size=28, color=WHITE).to_edge(DOWN, buff=0.7)
        counter_num = Integer(self.NUM_ITEMS, font_size=28, color=YELLOW).next_to(
            counter_label, RIGHT, buff=0.1
        )
        counter_note = Text("(constant)", font_size=22, color=GRAY_B).next_to(
            counter_num, RIGHT, buff=0.2
        )
        self.play(Write(counter_label), Write(counter_num), FadeIn(counter_note))
        self.wait(0.5)

        # ── Animate items moving from closet → floor one by one ──────────────
        floor_positions = [
            floor_box.get_center()
            + RIGHT * (((i % 3) - 1) * 0.85)
            + UP * ((1 - i // 3) * 0.75)
            for i in range(self.NUM_ITEMS)
        ]

        for i, item in enumerate(items):
            self.play(item.animate.move_to(floor_positions[i]), run_time=0.55)

        self.wait(0.4)

        # Counter keeps the same value — flash to emphasise unchanged total
        self.play(
            counter_num.animate.set_color(GREEN),
            counter_note.animate.set_color(GREEN),
            run_time=0.5,
        )
        unchanged = Text(
            "Total unchanged — energy conserved!", font_size=26, color=GREEN
        ).next_to(counter_label, UP, buff=0.4)
        self.play(Write(unchanged))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class FirstLawEquation(Scene):
    """ΔE = Q − W with labels."""

    def construct(self):
        # ── Main equation (large) ────────────────────────────────────────────
        equation = MathTex(
            r"\Delta E", r"=", r"Q", r"-", r"W",
            font_size=96,
        )
        equation.set_color_by_tex(r"\Delta E", YELLOW)
        equation.set_color_by_tex("Q", RED_B)
        equation.set_color_by_tex("W", BLUE_B)
        equation.move_to(ORIGIN + UP * 0.5)

        self.play(Write(equation), run_time=1.5)
        self.wait(0.5)

        # ── Term labels ──────────────────────────────────────────────────────
        delta_e_label = Text("Change in\ninternal energy", font_size=24, color=YELLOW)
        q_label = Text("Heat added\nto system", font_size=24, color=RED_B)
        w_label = Text("Work done\nby system", font_size=24, color=BLUE_B)

        delta_e_label.next_to(equation[0], DOWN, buff=1.1).shift(LEFT * 0.3)
        q_label.next_to(equation[2], DOWN, buff=1.1)
        w_label.next_to(equation[4], DOWN, buff=1.1)

        arrow_de = Arrow(
            delta_e_label.get_top(), equation[0].get_bottom(), buff=0.1, color=YELLOW
        )
        arrow_q = Arrow(q_label.get_top(), equation[2].get_bottom(), buff=0.1, color=RED_B)
        arrow_w = Arrow(w_label.get_top(), equation[4].get_bottom(), buff=0.1, color=BLUE_B)

        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arrow_de), FadeIn(delta_e_label, shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arrow_q), FadeIn(q_label, shift=DOWN * 0.2)),
                AnimationGroup(GrowArrow(arrow_w), FadeIn(w_label, shift=DOWN * 0.2)),
                lag_ratio=0.35,
            )
        )
        self.wait(1.0)

        # ── Reminder line ────────────────────────────────────────────────────
        reminder = Text(
            "Energy is conserved — always.", font_size=30, color=WHITE
        ).to_edge(UP, buff=0.4)
        self.play(Write(reminder))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


class FirstLawFull(Scene):
    """Runs all three segments as a single combined scene."""

    def construct(self):
        FirstLawIntro.construct(self)
        MessyRoomScene.construct(self)
        FirstLawEquation.construct(self)
