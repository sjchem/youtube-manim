from manim_scenes.common import *


class ClayFrictionScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        title = Text("Why topspin becomes heavier on clay", font_size=40, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        surface = create_court_surface(width=13.5, height=1.25, surface_type="clay", label=False).to_edge(DOWN, buff=0.7)
        ball = create_tennis_ball(0.26).move_to(LEFT * 5.4 + UP * 1.6)
        spin = create_spin_indicator(0.55, "topspin").move_to(ball)
        contact_model = science_panel(
            "topspin at contact",
            [
                "bottom of ball scrubs backward",
                "relative speed: v_x - R omega",
                "clay grip creates friction impulse",
                "forward speed down, rebound angle up",
            ],
            width=5.8,
            font_size=19,
        ).to_edge(RIGHT, buff=0.3).shift(UP * 0.55)
        path_in = path_mobject([LEFT * 5.4 + UP * 1.6, LEFT * 3.8 + DOWN * 0.3, LEFT * 2.5 + DOWN * 2.25], VELOCITY_COLOR)
        path_out = path_mobject([LEFT * 2.5 + DOWN * 2.25, LEFT * 1.5 + DOWN * 0.2, LEFT * 0.5 + UP * 1.8], BALL)
        self.play(FadeIn(surface), FadeIn(ball), Create(spin), FadeIn(contact_model), run_time=1.3)
        self.play(Create(path_in), MoveAlongPath(ball, path_in), Rotate(ball, -TAU * 1.8), run_time=2.0)

        contact = LEFT * 2.5 + DOWN * 2.25
        dust = create_dust_particles(contact, count=56, radius=1.3, seed=28)
        arrows = VGroup(
            create_force_arrow(contact + UP * 0.25, LEFT * 0.95, FRICTION_COLOR, "grip"),
            create_force_arrow(contact + UP * 0.15, UP * 1.1, MAGNUS_COLOR, "kick"),
        )
        self.play(FadeIn(dust), LaggedStart(*[MoveToTarget(p) for p in dust], lag_ratio=0.012), run_time=1.0)
        self.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]), GrowArrow(arrows[1][0]), FadeIn(arrows[1][1]), run_time=1.1)

        contact_patch = VGroup(
            Rectangle(width=1.0, height=0.09, fill_color=CLAY_LIGHT, fill_opacity=1, stroke_width=0).move_to(contact + DOWN * 0.02),
            Arrow(contact + RIGHT * 0.55 + UP * 0.18, contact + LEFT * 0.35 + UP * 0.18, buff=0, color=FRICTION_COLOR, stroke_width=5),
            Text("J_t = integral F_f dt", font_size=21, color=FRICTION_COLOR).move_to(contact + RIGHT * 1.35 + UP * 0.55),
        )
        self.play(FadeIn(contact_patch, shift=UP * 0.08), run_time=1.0)
        slip_note = science_panel(
            "slip-to-grip transition",
            [
                "early contact: felt slips over clay",
                "friction impulse slows the slip",
                "late contact: rotation helps launch upward",
            ],
            width=5.4,
            font_size=18,
        ).move_to(LEFT * 4.65 + DOWN * 0.45)
        self.play(FadeIn(slip_note, shift=RIGHT * 0.15), run_time=1.1)
        self.play(Create(path_out), MoveAlongPath(ball, path_out), Rotate(ball, -TAU * 2.3), run_time=2.2)

        shoulder = DashedLine(RIGHT * 0.4 + UP * 0.95, RIGHT * 6.2 + UP * 0.95, color=GOLD, stroke_opacity=0.8)
        note = Text("shoulder-height contact", font_size=25, color=GOLD).next_to(shoulder, UP, buff=0.1)
        player = VGroup(
            Line(RIGHT * 5.6 + DOWN * 2.25, RIGHT * 5.6 + UP * 0.55, color=OFF_WHITE),
            Circle(radius=0.18, color=OFF_WHITE).move_to(RIGHT * 5.6 + UP * 0.8),
        )
        self.play(FadeOut(contact_model), Create(player), Create(shoulder), FadeIn(note), run_time=1.3)
        heavy = science_panel(
            "why it feels heavy",
            [
                "not extra mass",
                "less forward speed after bounce",
                "higher strike zone",
                "less time to attack",
            ],
            width=4.6,
            font_size=19,
        ).move_to(RIGHT * 4.55 + DOWN * 0.55)
        self.play(FadeIn(heavy, shift=LEFT * 0.15), run_time=1.1)
        self.wait(1.6)
        self.pad_scene_to(scene_start, 30)
