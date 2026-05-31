from manim_scenes.common import *


class SpinTrajectoryScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        title = Text("Topspin dips. Backspin floats.", font_size=38, color=OFF_WHITE, weight=BOLD).to_edge(UP).shift(LEFT * 2.3)
        self.play(FadeIn(title), run_time=1.1)

        model = science_panel(
            "spin changes the force field",
            [
                "topspin: omega x v points downward",
                "slice: omega x v points upward",
                "higher RPM -> stronger curve",
            ],
            width=5.8,
            font_size=19,
        ).to_corner(UR, buff=0.28).shift(DOWN * 0.65)
        self.play(FadeIn(model, shift=LEFT * 0.15), run_time=1.0)

        base = Line(LEFT * 6.7 + DOWN * 2.55, RIGHT * 6.7 + DOWN * 2.55, color=OFF_WHITE, stroke_opacity=0.35)
        net = VGroup(
            Line(DOWN * 2.55, DOWN * 1.15, color=OFF_WHITE, stroke_width=4),
            DashedLine(DOWN * 2.50, DOWN * 1.20, color=OFF_WHITE, dash_length=0.12),
        )
        self.play(Create(base), Create(net), run_time=1.1)

        topspin_pts = trajectory_with_spin(omega_z=-230, v0=(29, 9), duration=1.25)
        flat_pts = trajectory_with_spin(omega_z=0, v0=(29, 9), duration=1.25)
        slice_pts = trajectory_with_spin(omega_z=150, v0=(29, 9), duration=1.25)
        top_path = path_mobject(topspin_pts, color=BALL, stroke_width=6)
        flat_path = path_mobject(flat_pts, color=OFF_WHITE, stroke_width=3).set_opacity(0.55)
        slice_path = path_mobject(slice_pts, color=MAGNUS_COLOR, stroke_width=5)

        top_label = Text("topspin", font_size=30, color=BALL).move_to(LEFT * 4.5 + DOWN * 1.15)
        slice_label = Text("backspin / slice", font_size=30, color=MAGNUS_COLOR).move_to(LEFT * 3.9 + UP * 2.55)
        flat_label = Text("same launch speed", font_size=28, color=OFF_WHITE).move_to(RIGHT * 3.7 + UP * 0.35)
        rpm_labels = VGroup(
            Text("omega < 0: dip into clay", font_size=24, color=BALL),
            Text("omega = 0: reference path", font_size=24, color=OFF_WHITE),
            Text("omega > 0: slice lift", font_size=24, color=MAGNUS_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(LEFT, buff=0.45).shift(UP * 0.45)
        ball = create_tennis_ball(0.18).move_to(topspin_pts[0])

        self.play(Create(flat_path), FadeIn(flat_label), run_time=1.4)
        self.play(Create(slice_path), FadeIn(slice_label), run_time=2.0)
        self.play(Create(top_path), MoveAlongPath(ball, top_path), Rotate(ball, -TAU * 2.2), FadeIn(top_label), run_time=2.7)
        self.play(LaggedStart(*[FadeIn(label, shift=UP * 0.1) for label in rpm_labels], lag_ratio=0.13), run_time=1.2)

        force_sample = VGroup(
            create_force_arrow(LEFT * 1.6 + UP * 0.55, DOWN * 1.0, MAGNUS_COLOR, "Magnus down", scale=0.95),
            create_force_arrow(RIGHT * 0.8 + UP * 1.55, UP * 0.8, MAGNUS_COLOR, "Magnus up", scale=0.95),
        )
        force_sample[0][1].next_to(force_sample[0][0].get_end(), DOWN, buff=0.16)
        force_sample[1][1].move_to(RIGHT * 0.65 + UP * 2.45)
        self.play(GrowArrow(force_sample[0][0]), FadeIn(force_sample[0][1]), GrowArrow(force_sample[1][0]), FadeIn(force_sample[1][1]), run_time=1.3)
        rpm_note = science_panel(
            "spin rate intuition",
            [
                "tour topspin can exceed 2500 rpm",
                "larger omega strengthens Magnus force",
                "the same launch can land shorter or float longer",
            ],
            width=5.9,
            font_size=19,
        ).to_corner(DL, buff=0.28).shift(UP * 0.55)
        self.play(FadeIn(rpm_note, shift=RIGHT * 0.15), run_time=1.1)
        self.wait(1.3)

        insight = Text("The shot is already changing before it touches the court.", font_size=31, color=GOLD).to_edge(DOWN)
        self.play(FadeOut(rpm_note), FadeIn(insight, shift=UP * 0.2), run_time=1.1)
        self.wait(1.4)
        self.pad_scene_to(scene_start, 30)
