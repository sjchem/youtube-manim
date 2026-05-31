from manim_scenes.common import *


class LivingClayCourtScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        title = Text("The court is a living variable", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=1.0)

        panels = VGroup()
        for name, color, x in [
            ("wet / compact", "#8F3926", -4.6),
            ("ideal / grippy", CLAY, 0.0),
            ("dry / loose", "#D66A37", 4.6),
        ]:
            panel = RoundedRectangle(corner_radius=0.08, width=4.0, height=4.6, fill_color=color, fill_opacity=0.95, stroke_color=OFF_WHITE, stroke_opacity=0.25)
            label = Text(name, font_size=27, color=OFF_WHITE, weight=BOLD).next_to(panel, UP, buff=0.22)
            rng = random.Random(int((x + 6) * 100))
            specks = VGroup(*[
                Dot(panel.get_center() + RIGHT * rng.uniform(-1.75, 1.75) + UP * rng.uniform(-1.9, 1.9), radius=rng.uniform(0.006, 0.022), color=CLAY_LIGHT, fill_opacity=rng.uniform(0.25, 0.8))
                for _ in range(70)
            ])
            panels.add(VGroup(panel, label, specks).shift(RIGHT * x + DOWN * 0.25))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in panels], lag_ratio=0.15), run_time=1.8)

        property_rows = VGroup(
            VGroup(
                Text("dense", font_size=17, color=OFF_WHITE),
                Text("can skid if too wet", font_size=17, color=MAGNUS_COLOR),
            ).arrange(DOWN, buff=0.08).move_to(LEFT * 4.6 + DOWN * 2.15),
            VGroup(
                Text("grip + slide balance", font_size=17, color=GOLD),
                Text("most consistent bounce", font_size=17, color=OFF_WHITE),
            ).arrange(DOWN, buff=0.08).move_to(DOWN * 2.15),
            VGroup(
                Text("dusty / loose", font_size=17, color=CLAY_LIGHT),
                Text("higher bounce, less traction", font_size=17, color=OFF_WHITE),
            ).arrange(DOWN, buff=0.08).move_to(RIGHT * 4.6 + DOWN * 2.15),
        )
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.08) for row in property_rows], lag_ratio=0.12), run_time=1.2)

        notes = VGroup(
            Text("moisture changes density", font_size=25, color=GOLD),
            Text("rolling changes smoothness", font_size=25, color=OFF_WHITE),
            Text("wear creates loose particles", font_size=25, color=CLAY_LIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in notes], lag_ratio=0.18), run_time=1.5)

        mini_ball = create_tennis_ball(0.14).move_to(panels[0][0].get_center() + UP * 1.4)
        paths = [
            path_mobject([panels[i][0].get_center() + UP * 1.4, panels[i][0].get_center() + DOWN * 1.2], color=VELOCITY_COLOR, stroke_width=4)
            for i in range(3)
        ]
        self.play(FadeIn(mini_ball), run_time=0.5)
        for path in paths:
            ball_copy = mini_ball.copy().move_to(path.get_start())
            self.add(ball_copy)
            self.play(Create(path), MoveAlongPath(ball_copy, path), run_time=1.0)
            self.remove(ball_copy)

        maintenance = VGroup(
            Text("water", font_size=22, color=MAGNUS_COLOR),
            Arrow(LEFT * 0.25, RIGHT * 0.25, color=OFF_WHITE, buff=0),
            Text("roll", font_size=22, color=GOLD),
            Arrow(LEFT * 0.25, RIGHT * 0.25, color=OFF_WHITE, buff=0),
            Text("brush", font_size=22, color=CLAY_LIGHT),
        ).arrange(RIGHT, buff=0.16).to_edge(RIGHT, buff=0.55).shift(DOWN * 3.35)
        self.play(FadeIn(maintenance, shift=LEFT * 0.15), run_time=1.1)
        self.wait(1.5)
        self.pad_scene_to(scene_start, 28)
