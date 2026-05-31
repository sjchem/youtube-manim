from manim_scenes.common import *


class BouncePhysicsScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        title = Text("Journey Two: the collision", font_size=40, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        hard = create_court_surface(width=6.7, height=1.4, surface_type="hard", label=False).shift(LEFT * 4 + DOWN * 2.7)
        clay = create_court_surface(width=6.7, height=1.4, surface_type="clay", label=False).shift(RIGHT * 4 + DOWN * 2.7)
        labels = VGroup(
            Text("Hard court: skids forward", font_size=25, color=OFF_WHITE).next_to(hard, UP, buff=0.2),
            Text("Clay: grips, slows, kicks", font_size=25, color=GOLD).next_to(clay, UP, buff=0.2),
        )
        self.play(FadeIn(hard), FadeIn(clay), FadeIn(labels), run_time=1.3)

        comparison = VGroup(
            coefficient_bar("hard speed retained alpha", 0.82, 1.0, HARD_COURT, width=2.25),
            coefficient_bar("clay speed retained alpha", 0.58, 1.0, CLAY_LIGHT, width=2.25),
            coefficient_bar("clay friction mu", 0.78, 1.0, FRICTION_COLOR, width=2.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).scale(0.88).to_corner(UL, buff=0.35).shift(DOWN * 0.85)
        self.play(FadeIn(comparison, shift=DOWN * 0.1), run_time=1.2)
        self.wait(0.8)

        incoming_left = path_mobject([LEFT * 6.6 + UP * 2.0, LEFT * 5.4 + UP * 0.5, LEFT * 4.4 + DOWN * 2.0], VELOCITY_COLOR)
        outgoing_left = path_mobject([LEFT * 4.4 + DOWN * 2.0, LEFT * 3.0 + DOWN * 1.35, LEFT * 1.3 + DOWN * 1.15], HARD_COURT)
        incoming_right = path_mobject([RIGHT * 1.4 + UP * 2.0, RIGHT * 2.6 + UP * 0.5, RIGHT * 3.6 + DOWN * 2.0], VELOCITY_COLOR)
        outgoing_right = path_mobject([RIGHT * 3.6 + DOWN * 2.0, RIGHT * 4.4 + DOWN * 0.6, RIGHT * 5.2 + UP * 0.75], BALL)
        self.play(Create(incoming_left), Create(incoming_right), run_time=1.5)

        dust = create_dust_particles(RIGHT * 3.6 + DOWN * 2.0, count=48, radius=1.1, seed=18)
        self.play(Create(outgoing_left), Create(outgoing_right), FadeIn(dust), LaggedStart(*[MoveToTarget(p) for p in dust], lag_ratio=0.015), run_time=2.1)

        normal_arrow = create_force_arrow(RIGHT * 3.6 + DOWN * 2.05, UP * 0.85, GRAVITY_COLOR, "normal rebound", scale=0.9)
        tangent_arrow = create_force_arrow(RIGHT * 3.6 + DOWN * 1.95, LEFT * 1.05, FRICTION_COLOR, "tangential impulse", scale=0.9)
        normal_arrow[1].next_to(normal_arrow[0].get_end(), RIGHT, buff=0.16)
        tangent_arrow[1].next_to(tangent_arrow[0].get_end(), UP, buff=0.16)
        self.play(FadeOut(labels), GrowArrow(normal_arrow[0]), FadeIn(normal_arrow[1]), GrowArrow(tangent_arrow[0]), FadeIn(tangent_arrow[1]), run_time=1.4)

        eq = create_equation_box(
            [
                "e = v_after_normal / v_before_normal",
                "v_x_after = alpha v_x_before",
                "omega_after = beta omega + gamma v_x",
            ],
            title="Bounce model",
            width=6.5,
        ).scale(0.88).to_edge(LEFT).shift(UP * 0.25)
        self.play(FadeOut(normal_arrow), FadeOut(tangent_arrow), FadeIn(eq, shift=RIGHT * 0.2), run_time=1.2)

        impulse = science_panel(
            "contact physics",
            [
                "normal: restitution returns vertical speed",
                "tangent: friction removes forward speed",
                "spin transfer changes omega",
                "energy -> heat, sound, clay motion",
            ],
            width=5.3,
            font_size=18,
        ).to_edge(RIGHT, buff=0.25).shift(UP * 0.15)
        self.play(FadeIn(impulse, shift=LEFT * 0.2), run_time=1.2)
        energy = science_panel(
            "energy bookkeeping",
            [
                "ball deformation stores and returns energy",
                "loose clay converts energy into particle motion",
                "friction couples translation and rotation",
            ],
            width=5.2,
            font_size=18,
        ).move_to(DOWN * 1.25)
        self.play(FadeIn(energy, shift=UP * 0.15), run_time=1.1)
        self.wait(1.5)
        self.pad_scene_to(scene_start, 30)
