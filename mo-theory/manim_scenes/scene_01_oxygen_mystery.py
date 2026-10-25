"""Chapter 01 — the hook: a Lewis structure with every electron paired, and a
liquid that hangs between the poles of a magnet.

The pour is a precomputed simulation (``physics_models.pour``, seeded by
``config.SEED``): droplets fall under gravity and, being paramagnetic, are
pulled toward the strong field in the gap and captured there. The freeze
frame hands over to the title.
"""

from manim_scenes.common import *
from manim_scenes.cryogenic_lab import CryogenicPour

MAGNET_AT = np.array([3.9, 0.7, 0])
LEWIS_AT = np.array([-4.3, 0.6, 0])


class Scene01OxygenMystery(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")   # a cold open: the title card arrives at the end

    # --- 1. This is oxygen ---------------------------------------------------------------------------------------
    stage = Stage([0, 0.4, 0], zoom=2.3, yaw=0.3, pitch=0.2, spin=0.3)
    diatomic_model(stage, "O", 2, length=2.3)
    show(scene, stage, 1.4)
    name = formula("O2", cfg.FONT["hero"]).move_to([0, -2.3, 0])
    scene.play(Write(name), run_time=1.0)

    # --- 2. A double bond; every electron paired -----------------------------------------------------------------
    beat(scene, t, 1)
    lewis = LewisDiatomic("O", 2, 2, at=[0, 0.3, 0])
    scene.play(stage.fade(stage, 0.0), FadeOut(name), run_time=0.9)
    scene.remove(stage)
    scene.play(Write(lewis), run_time=1.6)
    rings = VGroup(*[glow_frame(pair, cfg.WHITE, buff=0.08, width=3) for pair in lewis.lone])
    paired = result_label("every electron paired", cfg.WHITE, cfg.FONT["body"]).move_to([0, -2.3, 0])
    scene.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), FadeIn(paired), run_time=1.6)
    scene.play(Indicate(lewis.bonds, color=cfg.CYAN, scale_factor=1.1), run_time=1.0)

    # --- 3. Pour liquid oxygen between the poles --------------------------------------------------------------------
    beat(scene, t, 2)
    magnet = Electromagnet(MAGNET_AT, scale=1.2)
    pour = CryogenicPour(magnet, drops=90, seed=cfg.SEED + 1, duration=8.0)
    scene.play(FadeOut(rings), FadeOut(paired), lewis.animate.scale(0.8).move_to(LEWIS_AT), run_time=1.2)
    scene.play(FadeIn(magnet, shift=LEFT * 0.3), FadeIn(pour.flask), run_time=1.2)
    scene.add(pour)
    label = txt("liquid oxygen", cfg.FONT["small"], cfg.LIQUID_O2).next_to(pour.flask, LEFT, buff=0.3)
    scene.play(FadeIn(label), magnet.field_on(), run_time=0.8)
    pour.run()

    # --- 4. It sticks, bridging the gap --------------------------------------------------------------------------------
    beat(scene, t, 3)
    sticks = caption("It doesn't fall through. It hangs in the gap.", cfg.LIQUID_O2)
    scene.play(FadeIn(sticks), run_time=0.8)
    gap_ring = glow_frame(Rectangle(width=1.8, height=1.2).move_to(magnet.gap_center), cfg.GOLD, buff=0.1)
    narration_wait(scene, 2.4)
    scene.play(Create(gap_ring), run_time=1.0)

    # --- 5. The signature of unpaired electrons -------------------------------------------------------------------------
    beat(scene, t, 4)
    clue = VGroup(spin_arrow(1, cfg.UNPAIRED), spin_arrow(1, cfg.UNPAIRED)).arrange(RIGHT, buff=0.3)
    clue.scale(1.3).move_to(magnet.gap_center + UP * 1.75 + LEFT * 2.1)
    unpaired = caption("Attraction like this means unpaired electrons", cfg.UNPAIRED)
    scene.play(FadeOut(gap_ring), fade_through(sticks, unpaired), FadeIn(clue, shift=DOWN * 0.2), run_time=1.0)
    scene.remove(sticks)
    scene.play(Indicate(clue, color=cfg.WHITE, scale_factor=1.15), run_time=1.2)

    # --- 6. But the Lewis structure has none --------------------------------------------------------------------------------
    beat(scene, t, 5)
    no_lone = cross_mark(0.45).move_to(LEWIS_AT + DOWN * 1.75)
    none = caption("But this structure has none. Where are they hiding?", cfg.WHITE)
    scene.play(fade_through(unpaired, none), Indicate(lewis.lone, color=cfg.RED, scale_factor=1.3), run_time=1.2)
    scene.remove(unpaired)
    scene.play(Create(no_lone), run_time=0.6)
    question = txt("?", 150, cfg.GOLD).move_to([-0.3, 0.55, 0])
    glow = question.copy().set_stroke(cfg.GOLD, width=22, opacity=0.18).set_fill(opacity=0)
    decorative(glow)
    scene.play(FadeIn(question, scale=0.6), FadeIn(glow, scale=0.6), run_time=1.0)

    # --- 7. Freeze: we need a different picture -----------------------------------------------------------------------
    beat(scene, t, 6)
    pour.run(False)
    veil = Rectangle(width=16.5, height=9.5, stroke_width=0, fill_color=cfg.BG, fill_opacity=0.0)
    different = caption("We need a completely different picture of a bond", cfg.CYAN)
    scene.add(veil)
    scene.play(veil.animate.set_fill(opacity=0.55), fade_through(none, different), FadeOut(question), FadeOut(glow),
               FadeOut(no_lone), FadeOut(label), FadeOut(clue), run_time=1.4)
    scene.remove(none)
    narration_wait(scene, 2.0)

    # --- 8. The title ---------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    card = title_card("MOLECULAR ORBITAL THEORY", "Explained Visually")
    card.scale(0.92).move_to([0, 0.3, 0])
    scene.play(FadeOut(different), FadeOut(lewis), FadeOut(magnet), FadeOut(pour), veil.animate.set_fill(opacity=0.0),
               run_time=0.8)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=1.4)
    part = txt(cfg.PROJECT_PART, cfg.FONT["small"], cfg.MUTED).next_to(card, DOWN, buff=0.45)
    scene.play(FadeIn(part), run_time=0.7)
    scene.play(Indicate(card.title[0], color=cfg.WHITE, scale_factor=1.03), run_time=1.5)
    scene.play(card.animate.scale(1.04), run_time=4.0, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
