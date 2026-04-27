from manim import *
import numpy as np


class Disentangle(Scene):
    def construct(self):
        np.random.seed(7)

        signal_colors = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE]
        N = 7

        # ── Title  (~2 s) ──────────────────────────────────────────────
        title = Text("Disentanglement", font_size=38, weight=BOLD)
        subtitle = Text("signals become clean & organized", font_size=22, color=GRAY_B)
        title.to_edge(UP, buff=0.25)
        subtitle.next_to(title, DOWN, buff=0.1)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)

        # ── Brain at centre  (~1.5 s) ──────────────────────────────────
        brain = Ellipse(width=2.6, height=2.0, color=BLUE_D, stroke_width=2.5)
        brain.set_fill(BLUE_D, opacity=0.1)
        brain_glow = Ellipse(width=3.2, height=2.6, color=BLUE_E, stroke_width=1)
        brain_glow.set_fill(BLUE_E, opacity=0.0)
        brain_lbl = Text("Deep\nBrain", font_size=20, color=BLUE_C)

        self.play(Create(brain_glow), Create(brain), Write(brain_lbl), run_time=1.5)

        # ── Tangled signals on left  (~3.8 s) ─────────────────────────
        messy = VGroup()
        for i in range(N):
            y_base = -1.5 + i * 0.5
            pts = []
            x = -6.5
            while x < -1.4:
                pts.append([x, y_base + np.random.uniform(-0.55, 0.55), 0])
                x += np.random.uniform(0.25, 0.65)
            pts[-1] = [-1.4, y_base, 0]
            line = VMobject(color=signal_colors[i], stroke_width=2.8)
            line.set_points_as_corners(pts)
            line.make_smooth()
            messy.add(line)

        tangled_tag = Text("Tangled Signals", font_size=22, color=RED_C)
        tangled_tag.move_to([-4.5, -2.5, 0])

        self.play(
            LaggedStart(*[Create(l) for l in messy], lag_ratio=0.1),
            run_time=2.5,
        )
        self.play(FadeIn(tangled_tag), run_time=0.5)
        self.wait(0.8)

        # ── Signals absorbed into brain  (~2 s) ────────────────────────
        self.play(
            LaggedStart(
                *[l.animate.move_to(ORIGIN).scale(0.05) for l in messy],
                lag_ratio=0.08,
            ),
            FadeOut(tangled_tag),
            run_time=2.0,
        )

        # ── Brain "processes" — pulse  (~1.5 s) ───────────────────────
        self.play(
            brain.animate.set_fill(BLUE_D, opacity=0.55),
            brain_glow.animate.set_fill(BLUE_E, opacity=0.28).scale(1.08),
            run_time=0.7,
        )
        self.play(
            brain.animate.set_fill(BLUE_D, opacity=0.12),
            brain_glow.animate.set_fill(BLUE_E, opacity=0.0).scale(1 / 1.08),
            run_time=0.8,
        )

        # ── Internal neural activity — nodes + connections  (~3.5 s) ──
        node_positions = []
        nodes = VGroup()
        rng = np.random.default_rng(42)
        while len(node_positions) < 14:
            x = rng.uniform(-1.1, 1.1)
            y = rng.uniform(-0.8, 0.8)
            if (x / 1.3) ** 2 + (y / 1.0) ** 2 < 0.88:   # inside ellipse
                node_positions.append(np.array([x, y, 0]))
                nodes.add(Dot([x, y, 0], radius=0.06, color=TEAL_B))

        connections = VGroup()
        for i in range(len(node_positions)):
            for j in range(i + 1, len(node_positions)):
                dist = np.linalg.norm(node_positions[i] - node_positions[j])
                if dist < 0.85:
                    connections.add(
                        Line(
                            node_positions[i], node_positions[j],
                            color=TEAL_E, stroke_width=1.2, stroke_opacity=0.55,
                        )
                    )

        process_lbl = Text("Processing…", font_size=18, color=TEAL_C)
        process_lbl.next_to(brain, DOWN, buff=0.2)

        self.play(
            LaggedStart(*[FadeIn(n, scale=0.5) for n in nodes], lag_ratio=0.07),
            FadeIn(process_lbl),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[Create(c) for c in connections], lag_ratio=0.04),
            run_time=1.2,
        )
        self.wait(0.8)
        self.play(
            FadeOut(nodes), FadeOut(connections), FadeOut(process_lbl),
            run_time=0.5,
        )

        # ── Clean signals emerge from right  (~3 s) ───────────────────
        clean = VGroup()
        for i in range(N):
            y_pos = -1.5 + i * 0.5
            line = Line(
                [1.4, y_pos, 0], [6.5, y_pos, 0],
                color=signal_colors[i], stroke_width=2.8,
            )
            clean.add(line)

        clean_tag = Text("Organized Signals", font_size=22, color=GREEN_C)
        clean_tag.move_to([4.5, -2.5, 0])

        self.play(
            LaggedStart(*[Create(l) for l in clean], lag_ratio=0.1),
            run_time=2.5,
        )
        self.play(FadeIn(clean_tag), run_time=0.5)
        self.wait(0.5)

        # ── Final message  (~3.5 s) ────────────────────────────────────
        final = Text("Clarity Emerges from Chaos", font_size=24, color=GREEN_B, weight=BOLD)
        final.to_edge(DOWN, buff=0.5)
        self.play(Write(final), run_time=1.5)
        self.wait(3.0)
        # Total ≈ 22.3 s
