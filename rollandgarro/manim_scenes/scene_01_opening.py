from manim_scenes.common import *


class OpeningHookScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        question = Text("Same shot. Same speed. Same spin.", font_size=44, color=OFF_WHITE, weight=BOLD)
        self.play(FadeIn(question), run_time=1.4)
        self.wait(1.0)
        self.play(question.animate.scale(0.68).move_to(UP * 2.72), run_time=1.1)

        split = create_split_screen()
        split.shift(DOWN * 0.35)
        self.play(FadeIn(split), run_time=1.4)

        launch = science_panel("same initial shot", ["v0 = 28 m/s", "omega0 = heavy topspin", "same launch angle"], width=4.45, font_size=20)
        launch.move_to(DOWN * 0.15)
        hard_specs = science_panel("hard court response", ["firmer surface", "alpha ~= 0.82", "lower tangential grip"], width=4.25, font_size=18)
        clay_specs = science_panel("red clay response", ["crushed-brick layer", "alpha ~= 0.58", "higher friction impulse"], width=4.25, font_size=18)
        hard_specs.move_to(LEFT * 4.05 + DOWN * 1.55)
        clay_specs.move_to(RIGHT * 4.05 + DOWN * 1.55)
        self.play(FadeIn(launch), FadeIn(hard_specs), FadeIn(clay_specs), run_time=1.3)
        self.wait(1.3)

        hard_ball = create_tennis_ball(0.18).move_to(LEFT * 6.7 + DOWN * 1.0)
        clay_ball = create_tennis_ball(0.18).move_to(RIGHT * 1.3 + DOWN * 1.0)
        hard_path = path_mobject([
            LEFT * 6.7 + DOWN * 1.0,
            LEFT * 5.2 + DOWN * 0.1,
            LEFT * 3.7 + DOWN * 1.15,
            LEFT * 2.2 + DOWN * 0.75,
            LEFT * 0.8 + DOWN * 0.45,
        ], color=VELOCITY_COLOR)
        clay_path = path_mobject([
            RIGHT * 1.3 + DOWN * 1.0,
            RIGHT * 2.7 + DOWN * 0.1,
            RIGHT * 4.0 + DOWN * 1.15,
            RIGHT * 4.9 + UP * 0.55,
            RIGHT * 5.7 + UP * 1.45,
        ], color=BALL)
        self.play(Create(hard_path), MoveAlongPath(hard_ball, hard_path), Rotate(hard_ball, -TAU * 1.6), run_time=3.2)
        self.play(Create(clay_path), MoveAlongPath(clay_ball, clay_path), Rotate(clay_ball, -TAU * 2.4), run_time=3.2)

        impact = RIGHT * 4.0 + DOWN * 1.15
        dust = create_dust_particles(impact, count=48, radius=1.2, seed=10)
        self.play(LaggedStart(*[MoveToTarget(p) for p in dust], lag_ratio=0.02), FadeIn(dust), run_time=1.3)

        stack = clay_layer_stack(width=3.7).scale(0.72).move_to(RIGHT * 4.1 + UP * 0.7)
        self.play(FadeIn(stack, shift=UP * 0.15), run_time=1.1)
        mechanism = science_panel(
            "what changed?",
            [
                "incoming velocity and spin are identical",
                "surface coefficients decide the rebound",
                "clay trades forward speed for height",
            ],
            width=4.2,
            font_size=14,
        ).scale(0.8).move_to(LEFT * 4.1 + UP * 0.75)
        self.play(FadeIn(mechanism, shift=RIGHT * 0.15), run_time=1.0)
        self.wait(1.4)

        title = create_title_card("The Hidden Science", "of Red Clay Tennis").move_to(ORIGIN)
        plate = Rectangle(width=16, height=9, fill_color=BACKGROUND, fill_opacity=0.72, stroke_width=0)
        self.play(FadeIn(plate), FadeIn(title, scale=1.05), run_time=1.2)
        self.wait(1.0)
        self.pad_scene_to(scene_start, 28)
