from manim_scenes.common import *


class EquationBuildScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        title = Text("A visual model of flight", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        ball = create_tennis_ball(0.28).move_to(LEFT * 4.85 + UP * 0.95)
        equation = create_equation_box(
            [
                "m dv/dt = F_g + F_d + F_M",
                "F_g = m g",
                "F_d = -1/2 rho C_d A |v| v",
                "F_M ~= S (omega x v)",
            ],
            title="Flight forces",
            width=7.1,
        ).scale(0.92).move_to(RIGHT * 2.75 + UP * 0.95)
        self.play(FadeIn(ball), FadeIn(equation), run_time=1.5)

        constants = science_panel(
            "tennis ball inputs",
            [
                "mass m = 57 g",
                "radius R = 3.35 cm",
                "air density rho ~= 1.225 kg/m3",
                "C_d is approximate, not fixed",
            ],
            width=5.1,
            font_size=20,
        ).to_corner(DL, buff=0.35).shift(UP * 0.35)
        self.play(FadeIn(constants, shift=RIGHT * 0.2), run_time=1.1)

        arrows = VGroup(
            create_force_arrow(ball.get_center(), DOWN * 1.35, GRAVITY_COLOR, "F_g"),
            create_force_arrow(ball.get_center(), LEFT * 1.35, DRAG_COLOR, "F_d"),
            create_force_arrow(ball.get_center(), DOWN * 0.85 + RIGHT * 0.85, MAGNUS_COLOR, "F_M"),
        )
        arrows[0][1].next_to(arrows[0][0].get_end(), DOWN, buff=0.16)
        arrows[1][1].next_to(arrows[1][0].get_end(), LEFT, buff=0.16)
        arrows[2][1].next_to(arrows[2][0].get_end(), RIGHT, buff=0.16)
        self.play(LaggedStart(*[GrowArrow(a[0]) for a in arrows], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(a[1]) for a in arrows], lag_ratio=0.15), run_time=0.9)

        terms = VGroup(
            Text("mass resists change", font_size=28, color=OFF_WHITE),
            Text("drag steals speed", font_size=28, color=DRAG_COLOR),
            Text("spin bends the path", font_size=28, color=MAGNUS_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(LEFT * 3.25 + DOWN * 1.0)
        self.play(FadeOut(constants), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in terms], lag_ratio=0.2), run_time=1.6)

        curve = path_mobject(trajectory_with_spin(-210, origin=LEFT * 1.4 + DOWN * 2.35, x_scale=0.15, y_scale=0.36), color=BALL)
        self.play(Create(curve), run_time=2.0)

        numerical_note = science_panel(
            "numerical integration",
            [
                "update velocity from net force",
                "update position from velocity",
                "repeat every small dt",
                "visual model, not CFD",
            ],
            width=5.1,
            font_size=19,
        ).to_corner(DR, buff=0.25).shift(UP * 0.35)
        self.play(FadeIn(numerical_note, shift=LEFT * 0.2), run_time=1.2)
        limitations = science_panel(
            "model limits",
            [
                "real flow is turbulent",
                "C_d and lift change with speed",
                "enough to explain direction",
            ],
            width=4.35,
            font_size=18,
        ).move_to(LEFT * 1.1 + DOWN * 2.05)
        self.play(FadeIn(limitations, shift=UP * 0.12), run_time=1.1)
        self.wait(1.5)
        self.pad_scene_to(scene_start, 30)
