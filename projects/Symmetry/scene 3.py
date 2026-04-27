from manim import *


class Transformations(Scene):
    def construct(self):

        # ── Utility: ghost copy (faded original) ──────────────────────
        def ghost_of(mob):
            g = mob.copy()
            g.set_fill(opacity=0.18)
            g.set_stroke(opacity=0.35)
            return g

        # ── Shape: right triangle — asymmetric so changes are obvious ──
        def make_shape():
            t = Polygon(
                LEFT * 0.8 + DOWN * 0.7,
                RIGHT * 0.8 + DOWN * 0.7,
                LEFT * 0.8 + UP * 0.7,
                color=BLUE, fill_color=BLUE_D, fill_opacity=0.85,
            )
            return t

        # ── Title ──────────────────────────────────────────────────────
        title = Text("Geometric Transformations", font_size=42).to_edge(UP)
        self.play(Write(title), run_time=1)
        self.wait(0.3)

        shape = make_shape()
        self.play(DrawBorderThenFill(shape), run_time=0.5)
        self.wait(0.2)

        # ══ 1. TRANSLATION ════════════════════════════════════════════
        lbl = Text("Translation", font_size=36, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(lbl), run_time=0.4)

        ghost = ghost_of(shape)
        self.add(ghost)
        arrow = Arrow(shape.get_center(), shape.get_center() + RIGHT * 2.8,
                      color=YELLOW, buff=0.1)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(shape.animate.shift(RIGHT * 2.8), run_time=1.5)
        self.play(FadeOut(lbl), FadeOut(ghost), FadeOut(arrow), run_time=0.35)
        self.play(shape.animate.move_to(ORIGIN), run_time=0.45)

        # ══ 2. ROTATION ═══════════════════════════════════════════════
        lbl2 = Text("Rotation  (90°)", font_size=36, color=GREEN).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(lbl2), run_time=0.4)

        ghost2 = ghost_of(shape)
        self.add(ghost2)
        arc = Arc(radius=0.55, start_angle=0, angle=PI / 2,
                  color=GREEN).move_to(shape.get_center())
        self.play(Create(arc), run_time=0.4)
        self.play(Rotate(shape, PI / 2, about_point=shape.get_center()), run_time=1.5)
        self.play(FadeOut(lbl2), FadeOut(ghost2), FadeOut(arc), run_time=0.35)
        self.play(shape.animate.move_to(ORIGIN), run_time=0.45)

        # ══ 3. REFLECTION ═════════════════════════════════════════════
        lbl3 = Text("Reflection", font_size=36, color=PINK).next_to(title, DOWN, buff=0.15)
        axis = DashedLine(UP * 2.2, DOWN * 2.2, color=GRAY, dash_length=0.15)
        self.play(FadeIn(lbl3), Create(axis), run_time=0.5)

        ghost3 = ghost_of(shape)
        self.add(ghost3)
        self.play(shape.animate.flip(RIGHT), run_time=1.5)
        self.play(FadeOut(lbl3), FadeOut(ghost3), FadeOut(axis), run_time=0.35)
        self.play(shape.animate.move_to(ORIGIN), run_time=0.45)

        # ══ 4. SCALING (DILATION) ═════════════════════════════════════
        lbl4 = Text("Scaling  (Dilation)", font_size=36, color=ORANGE).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(lbl4), run_time=0.4)

        ghost4 = ghost_of(shape)
        self.add(ghost4)
        self.play(shape.animate.scale(1.9), run_time=1.5)
        self.play(FadeOut(lbl4), FadeOut(ghost4), run_time=0.35)

        # ── Outro ──────────────────────────────────────────────────────
        self.wait(0.6)
        self.play(FadeOut(shape), FadeOut(title), run_time=0.5)v
