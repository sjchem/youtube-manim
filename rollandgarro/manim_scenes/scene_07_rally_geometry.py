from manim_scenes.common import *


class RallyGeometryScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        title = Text("On clay, time becomes tactics", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        court = Rectangle(width=10, height=5.2, color=OFF_WHITE, stroke_width=3, fill_color=CLAY_DARK, fill_opacity=0.75)
        center = Line(UP * 2.6, DOWN * 2.6, color=OFF_WHITE, stroke_width=2)
        service1 = Line(LEFT * 5 + UP * 1.15, RIGHT * 5 + UP * 1.15, color=OFF_WHITE, stroke_width=2)
        service2 = Line(LEFT * 5 + DOWN * 1.15, RIGHT * 5 + DOWN * 1.15, color=OFF_WHITE, stroke_width=2)
        net = Line(LEFT * 5, RIGHT * 5, color=OFF_WHITE, stroke_width=4)
        geometry = VGroup(court, center, service1, service2, net).shift(DOWN * 0.1)
        self.play(Create(geometry), run_time=1.6)

        speed_panel = science_panel(
            "rally physics on clay",
            [
                "post-bounce speed is lower",
                "reaction window increases",
                "high bounce pushes court position back",
                "controlled sliding manages momentum",
            ],
            width=5.5,
            font_size=18,
        ).to_corner(UL, buff=0.3).shift(DOWN * 0.55)
        decay_bars = VGroup(
            coefficient_bar("hard v_after", 0.82, 1.0, HARD_COURT, width=1.8),
            coefficient_bar("clay v_after", 0.58, 1.0, CLAY_LIGHT, width=1.8),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(speed_panel, DOWN, buff=0.15)
        self.play(FadeIn(speed_panel), FadeIn(decay_bars), run_time=1.2)

        p1 = Dot(LEFT * 3.6 + DOWN * 2.0, radius=0.13, color=BALL)
        p2 = Dot(RIGHT * 3.6 + UP * 1.8, radius=0.13, color=MAGNUS_COLOR)
        slide = Line(RIGHT * 4.5 + UP * 1.8, RIGHT * 3.6 + UP * 1.8, color=FRICTION_COLOR, stroke_width=7)
        shoe_tread = VGroup(*[
            Line(RIGHT * 4.25 + UP * (1.58 + 0.08 * i), RIGHT * 4.42 + UP * (1.68 + 0.08 * i), color=OFF_WHITE, stroke_width=2)
            for i in range(5)
        ])
        slide_label = Text("kinetic friction slide", font_size=20, color=FRICTION_COLOR).next_to(slide, UP, buff=0.12)
        self.play(FadeIn(p1), FadeIn(p2), Create(slide), Create(shoe_tread), FadeIn(slide_label), run_time=1.1)

        rally_paths = VGroup(
            CurvedArrow(LEFT * 3.6 + DOWN * 2.0, RIGHT * 3.5 + UP * 2.1, angle=-TAU / 5, color=BALL),
            CurvedArrow(RIGHT * 3.5 + UP * 2.1, LEFT * 4.1 + UP * 1.8, angle=-TAU / 5, color=MAGNUS_COLOR),
            CurvedArrow(LEFT * 4.1 + UP * 1.8, RIGHT * 2.7 + DOWN * 2.1, angle=TAU / 6, color=BALL),
            CurvedArrow(RIGHT * 2.7 + DOWN * 2.1, LEFT * 0.7 + DOWN * 0.35, angle=TAU / 7, color=GOLD),
        )
        labels = VGroup(
            Text("heavy topspin", font_size=23, color=BALL).move_to(LEFT * 1.4 + UP * 2.75),
            Text("wide angle", font_size=23, color=MAGNUS_COLOR).move_to(LEFT * 3.7 + UP * 2.25),
            Text("drop shot", font_size=23, color=GOLD).move_to(RIGHT * 1.6 + DOWN * 0.65),
        )
        self.play(LaggedStart(*[Create(a) for a in rally_paths], lag_ratio=0.35), run_time=3.4)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.16), run_time=1.2)

        tactic_words = VGroup(
            Text("+ time", font_size=30, color=GOLD, weight=BOLD),
            Text("+ endurance", font_size=30, color=OFF_WHITE, weight=BOLD),
            Text("+ patience", font_size=30, color=OFF_WHITE, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.45).shift(UP * 1.25)
        self.play(LaggedStart(*[FadeIn(word, shift=LEFT * 0.12) for word in tactic_words], lag_ratio=0.12), run_time=1.4)

        tactical_equation = science_panel(
            "point construction",
            [
                "spin creates height",
                "height creates depth",
                "depth creates space",
                "space creates the next shot",
            ],
            width=4.7,
            font_size=18,
        ).to_corner(DR, buff=0.3).shift(UP * 0.25)
        self.play(FadeIn(tactical_equation, shift=LEFT * 0.15), run_time=1.1)
        recovery = science_panel(
            "strategy from physics",
            [
                "slower ball increases reachability",
                "higher ball moves contact point upward",
                "sliding changes recovery timing",
            ],
            width=4.9,
            font_size=18,
        ).to_edge(LEFT, buff=0.35).shift(DOWN * 2.35)
        self.play(FadeIn(recovery, shift=RIGHT * 0.15), run_time=1.1)
        self.wait(1.4)
        self.pad_scene_to(scene_start, 28)
