from manim_scenes.common import *


class FinalSummaryScene(RedClayScene):
    def construct(self):
        scene_start = self.time
        self.add_cinematic_background()
        words = VGroup(
            Text("AIR", font_size=54, color=MAGNUS_COLOR, weight=BOLD),
            Text("SPIN", font_size=54, color=SPIN_COLOR, weight=BOLD),
            Text("FRICTION", font_size=54, color=FRICTION_COLOR, weight=BOLD),
            Text("CLAY", font_size=54, color=CLAY_LIGHT, weight=BOLD),
        ).arrange(RIGHT, buff=0.55)
        self.play(LaggedStart(*[FadeIn(w, scale=1.08) for w in words], lag_ratio=0.15), run_time=1.8)
        self.wait(0.9)

        chain = science_panel(
            "complete physics chain",
            [
                "racket sets v and omega",
                "air changes trajectory",
                "court impulse changes bounce",
                "surface condition changes strategy",
            ],
            width=6.1,
            font_size=20,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(chain, shift=UP * 0.15), run_time=1.2)
        self.wait(1.0)

        line1 = Text("Air shapes the flight.", font_size=35, color=OFF_WHITE)
        line2 = Text("Clay rewrites the bounce.", font_size=35, color=GOLD)
        takeaway = VGroup(line1, line2).arrange(DOWN, buff=0.25).move_to(DOWN * 0.9)
        self.play(FadeOut(chain), words.animate.to_edge(UP), FadeIn(takeaway), run_time=1.4)
        synthesis = science_panel(
            "one shot, two transformations",
            [
                "air: force balance changes flight",
                "contact: impulse changes bounce",
                "strategy: time and height change choices",
            ],
            width=6.0,
            font_size=20,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(synthesis, shift=UP * 0.15), run_time=1.1)
        self.wait(1.2)

        final = create_title_card("The Hidden Science", "of Red Clay Tennis").move_to(ORIGIN)
        self.play(FadeOut(takeaway), FadeOut(synthesis), FadeTransform(words, final), run_time=1.6)
        cta = Text("What surface should we explain next?", font_size=28, color=OFF_WHITE).to_edge(DOWN)
        self.play(FadeIn(cta), run_time=1.0)
        subscribe_tab = VGroup(
            RoundedRectangle(
                corner_radius=0.12,
                width=3.2,
                height=0.62,
                fill_color="#E62117",
                fill_opacity=1,
                stroke_color=OFF_WHITE,
                stroke_opacity=0.35,
            ),
            Text("SUBSCRIBE", font_size=25, color=OFF_WHITE, weight=BOLD),
            Text("✓", font_size=28, color=OFF_WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.12)
        subscribe_tab[1:].move_to(subscribe_tab[0].get_center())
        subscribe_tab[2].next_to(subscribe_tab[1], RIGHT, buff=0.16)
        subscribe_tab.move_to(RIGHT * 4.7 + DOWN * 3.45)
        self.play(FadeIn(subscribe_tab, shift=UP * 0.15), run_time=0.8)
        self.wait(1.4)
        self.pad_scene_to(scene_start, 24)
