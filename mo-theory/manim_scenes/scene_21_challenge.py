"""Chapter 21 — a challenge: an unlabelled, filled diagram. Magnetic? Bond order?

The diagram is ``mo_models.fill("C2")``, drawn with its atoms hidden; the
answers are read from the same filling.
"""

from manim_scenes.common import *
from manim_scenes.scene_14_fill_nitrogen import PANEL_X, valence_diagram

SECRET = "C2"
THINK_SECONDS = 7


class Scene21Challenge(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "21", "Read the diagram")
    f = mo.fill(SECRET)

    # --- 1. No molecule named, just a filled diagram ---------------------------------------------------------------------------
    diagram = valence_diagram(f.diagram.kind, "?")
    arrows = diagram.electrons_for(f)
    dismiss_opening_title(scene, t, head, at=1.0)
    scene.play(FadeIn(diagram), LaggedStart(*[FadeIn(a, shift=DOWN * 0.15) for a in arrows], lag_ratio=0.1), run_time=2.0)
    mystery = txt("?", 150, cfg.GOLD).move_to([PANEL_X, 1.6, 0])
    scene.play(FadeIn(mystery, scale=0.6), run_time=0.8)

    # --- 2. Magnetic? Bond order? ------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    questions = VGroup(txt("Magnetic?", cfg.FONT["section"], cfg.GOLD), txt("Bond order?", cfg.FONT["section"], cfg.GREEN))
    questions.arrange(DOWN, buff=0.9).move_to([PANEL_X, -0.55, 0])
    scene.play(LaggedStart(*[FadeIn(q, shift=LEFT * 0.2) for q in questions], lag_ratio=0.4), run_time=1.4)

    # --- 3. Take a few seconds: a countdown ring ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    clock = ValueTracker(1.0)
    ring_base = Circle(radius=0.55, stroke_color=cfg.MUTED, stroke_width=6, stroke_opacity=0.4).move_to([PANEL_X, -2.55, 0])
    ring = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=TAU * max(clock.get_value(), 1e-3),
                                     stroke_color=cfg.GOLD, stroke_width=8).move_arc_center_to(ring_base.get_center()))
    scene.play(Create(ring_base), FadeIn(ring), run_time=0.6)
    scene.play(clock.animate.set_value(0.0), run_time=THINK_SECONDS, rate_func=linear)
    ring.clear_updaters()
    scene.play(FadeOut(ring), FadeOut(ring_base), run_time=0.4)

    # --- 4. No lone arrows: diamagnetic ------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    frames = VGroup(*[diagram.highlight(key, cfg.CYAN, buff=0.1) for key, counts in f.occupancy().items() if sum(counts)])
    scene.play(LaggedStart(*[Create(fr) for fr in frames], lag_ratio=0.2), run_time=1.4)
    answer_mag = result_label(f.magnetism, cfg.DIAMAGNETIC if not f.unpaired else cfg.PARAMAGNETIC, cfg.FONT["body"])
    answer_mag.move_to(questions[0])
    scene.play(FadeOut(frames), Transform(questions[0], answer_mag), run_time=1.0)

    # --- 5. Bonding six, antibonding two: bond order two --------------------------------------------------------------------------------------
    beat(scene, t, 4)
    numbers = bond_order_numbers(f.bonding, f.antibonding, cfg.FONT["section"]).move_to(questions[1])
    fit_width(numbers, 4.3)
    scene.play(Transform(questions[1], numbers), run_time=1.4)

    # --- 6. It's C2: flames and comets -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    reveal = formula(SECRET, cfg.FONT["hero"], cfg.WHITE).move_to(mystery)
    atoms = VGroup(txt("C", cfg.FONT["body"]).move_to(diagram.atom_names[0]), txt("C", cfg.FONT["body"]).move_to(diagram.atom_names[1]))
    scene.play(Transform(mystery, reveal), Transform(diagram.atom_names, atoms), run_time=1.2)
    flames = caption("C₂ glows blue-green in flames and in comets", cfg.CYAN)
    scene.play(FadeIn(flames), run_time=0.8)
    scene.play(Indicate(mystery, color=cfg.CYAN, scale_factor=1.1), run_time=1.6)
    scene.play(*[Indicate(a, color=cfg.WHITE, scale_factor=1.2) for a in arrows], run_time=2.0)
    scene.play(mystery.animate.scale(1.08), run_time=3.4, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["21"])
