from manim_scenes.common import *


class AirForcesScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        self.chapter_title("Journey One", "the ball moves through air")

        ball = create_tennis_ball(0.34).move_to(LEFT * 1.2)
        spin = create_spin_indicator(0.66).move_to(ball)
        river = airflow_lines(np.linspace(-2.6, 2.6, 10))
        fuzz = VGroup()
        rng = random.Random(42)
        for _ in range(30):
            angle = rng.uniform(0, TAU)
            start = ball.get_center() + np.array([math.cos(angle), math.sin(angle), 0]) * 0.36
            end = ball.get_center() + np.array([math.cos(angle), math.sin(angle), 0]) * 0.47
            fuzz.add(Line(start, end, color=BALL, stroke_width=1.5, stroke_opacity=0.55))
        self.play(LaggedStart(*[Create(line) for line in river], lag_ratio=0.05), FadeIn(ball), run_time=1.6)
        self.play(Create(fuzz), Create(spin), Rotate(ball, -TAU * 1.2), run_time=1.8)
        self.wait(0.8)

        center = ball.get_center()
        arrows = VGroup(
            create_force_arrow(center, DOWN * 1.65, GRAVITY_COLOR, "gravity"),
            create_force_arrow(center, LEFT * 1.85, DRAG_COLOR, "drag"),
            create_force_arrow(center, DOWN * 1.15 + RIGHT * 0.7, MAGNUS_COLOR, "Magnus"),
            create_force_arrow(center, RIGHT * 1.9 + UP * 0.6, VELOCITY_COLOR, "velocity"),
        )
        arrows[0][1].next_to(arrows[0][0].get_end(), DOWN, buff=0.16)
        arrows[1][1].next_to(arrows[1][0].get_end(), LEFT, buff=0.16)
        arrows[2][1].next_to(arrows[2][0].get_end(), RIGHT, buff=0.16)
        arrows[3][1].move_to(center + RIGHT * 0.7 + UP * 0.9)
        self.play(LaggedStart(*[GrowArrow(a[0]) for a in arrows], lag_ratio=0.16), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(a[1]) for a in arrows], lag_ratio=0.12), run_time=1.0)

        aero_panel = science_panel(
            "aerodynamic model",
            [
                "drag: F_d = -1/2 rho C_d A |v|v",
                "lift: F_M ~= S(omega x v)",
                "felt fuzz changes boundary layer",
                "spin ratio sets lift direction",
            ],
            width=6.6,
            font_size=20,
        ).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.22)
        coeffs = VGroup(
            coefficient_bar("C_d drag", 0.55, 1.0, DRAG_COLOR, width=2.0),
            coefficient_bar("C_L spin", 0.32, 1.0, MAGNUS_COLOR, width=2.0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).scale(1.12).next_to(aero_panel, DOWN, buff=0.22)
        self.play(FadeIn(aero_panel, shift=LEFT * 0.2), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in coeffs], lag_ratio=0.15), run_time=1.1)
        scale_panel = science_panel(
            "why speed matters",
            [
                "drag grows with |v| squared",
                "Magnus direction comes from omega x v",
                "felt roughness keeps air attached longer",
            ],
            width=6.0,
            font_size=20,
        ).to_edge(LEFT, buff=0.35).shift(DOWN * 2.25)
        self.play(FadeIn(scale_panel, shift=UP * 0.15), run_time=1.2)
        self.wait(1.2)

        note = Text("Spin turns the air into a steering force.", font_size=34, color=GOLD).to_edge(DOWN)
        self.play(Write(note), run_time=1.2)
        self.wait(1.4)
        self.pad_scene_to(scene_start, 30)
