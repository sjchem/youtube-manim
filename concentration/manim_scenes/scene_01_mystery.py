"""Scene 01 — the hook: glucose dissolves in a turning glass, the camera
dives among the molecules, and four different, correct concentrations
appear around the same liquid.

The swarm is drawn at the true 1 : 100 glucose-to-water molecule ratio
(6 gold beads among 600 blue dots); sizes are not to scale. The four numbers
are the reference solution's, from ``utils.physics_models``.
"""

from manim_scenes.common import *

BASE = np.array([0.0, -2.75, 0.0])


class Scene01Mystery(Scene):
    def construct(self) -> None:
        play_scene(self)


def _value_card(value_tex: str, name: str, color: str) -> VGroup:
    number = eq(value_tex, cfg.FONT["hero"], color)
    label = txt(name, cfg.FONT["small"], cfg.MUTED)
    group = VGroup(number, label).arrange(DOWN, buff=0.22)
    group.number, group.label = number, label
    return group


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")   # a cold open: the title arrives at the end

    # --- 1. A glass of water --------------------------------------------------------------------------------
    stage, glass, swarm = solution_stage(BASE, zoom=1.2, solvent=600, solute=6, seed=1,
                                         solvent_radius=0.027, solute_radius=0.13, style="polished")
    glass.reflection_alpha = 0.0
    swarm.mix, swarm.solute_alpha = 0.0, 0.0
    swarm.drop_from = glass.top_point() + np.array([0.0, 1.1, 0.0])
    show(scene, stage, 2.0)
    water = txt("water", cfg.FONT["body"], cfg.SOLVENT).move_to([-4.6, 0.2, 0])
    scene.play(FadeIn(water, shift=RIGHT * 0.2), run_time=0.8)
    glucose = txt("glucose", cfg.FONT["body"], cfg.SOLUTE).move_to([3.9, 2.6, 0])
    scene.play(set_attr(stage, swarm, "solute_alpha", 1.0), set_attr(stage, swarm, "solute_glow", 0.8),
               FadeIn(glucose, shift=LEFT * 0.2), run_time=1.2)

    # --- 2. It falls, dissolves, spreads ----------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(set_attr(stage, swarm, "mix", 1.0), FadeOut(glucose), FadeOut(water), run_time=6.5,
               rate_func=linear)
    same = caption("uniform: every part of the glass looks the same", cfg.CYAN)
    scene.play(FadeIn(same), run_time=0.7)
    # Dive in among the molecules.
    scene.play(stage.zoom_to(3.6), stage.glide([0.0, -4.5, 0.0]),
               set_attr(stage, swarm, "solute_glow", 0.2), FadeOut(same), run_time=2.4)

    # --- 3. How concentrated is it? ---------------------------------------------------------------------------
    beat(scene, t, 2)
    question = result_label("How concentrated is it?", cfg.WHITE, cfg.FONT["title"]).move_to([0, 2.9, 0])
    scene.play(FadeIn(question, shift=DOWN * 0.2), run_time=1.0)
    scene.play(stage.zoom_to(1.15), stage.glide([0.0, -2.8, 0.0]), run_time=2.6)

    # --- 4-6. Four chemists, four numbers ------------------------------------------------------------------------
    beat(scene, t, 3)
    cards = [
        _value_card(rf"{M_TEXT}\ \mathrm{{M}}", "molarity", cfg.WHITE).move_to([-5.2, 1.85, 0]),
        _value_card(rf"{m_TEXT}\ \mathrm{{m}}", "molality", cfg.WHITE).move_to([5.2, 1.85, 0]),
        _value_card(X_TEXT, "mole fraction", cfg.WHITE).move_to([-5.2, -1.55, 0]),
        _value_card(rf"{W_TEXT}\%", "percent by mass", cfg.WHITE).move_to([5.2, -1.55, 0]),
    ]
    liquid = np.array([0.0, -1.1, 0.0])
    threads = [glow_arrow(liquid + np.array([np.sign(c.get_x()) * 1.65, 0.3 * np.sign(c.get_y()), 0]),
                         c.get_edge_center(RIGHT if c.get_x() < 0 else LEFT) + (RIGHT if c.get_x() < 0 else LEFT) * 0.2,
                         cfg.CYAN, width=2.4, tip=0.18) for c in cards]
    scene.play(FadeOut(question), run_time=0.4)
    scene.play(Create(threads[0]), FadeIn(cards[0], shift=RIGHT * 0.2), run_time=1.0)
    beat(scene, t, 4)
    scene.play(Create(threads[1]), FadeIn(cards[1], shift=LEFT * 0.2), run_time=1.2)
    beat(scene, t, 5)
    scene.play(Create(threads[2]), FadeIn(cards[2], shift=RIGHT * 0.2), run_time=1.2)
    narration_wait(scene, 3.2)
    scene.play(Create(threads[3]), FadeIn(cards[3], shift=LEFT * 0.2), run_time=1.2)

    # --- 7. One solution, four correct answers ---------------------------------------------------------------------
    beat(scene, t, 6)
    banner = result_label("ONE SOLUTION. FOUR CORRECT ANSWERS.", cfg.GOLD, cfg.FONT["body"]).move_to([0, 3.55, 0])
    scene.play(FadeIn(banner, shift=DOWN * 0.15), *[Indicate(c.number, color=cfg.GOLD, scale_factor=1.06) for c in cards],
               run_time=1.4)

    # --- 8. Which one is right? All of them --------------------------------------------------------------------------
    beat(scene, t, 7)
    checks = [check_mark(0.26).next_to(c.number, RIGHT, buff=0.25) for c in cards]
    scene.play(LaggedStart(*[Create(c) for c in checks], lag_ratio=0.25), run_time=1.6)
    scene.play(*[c.number.animate.set_color(cfg.RESULT) for c in cards], run_time=0.8)

    # --- 9. It's about what we compare the glucose with ---------------------------------------------------------------
    beat(scene, t, 8)
    hues = [cfg.VOLUME, cfg.SOLVENT_MASS, cfg.AMOUNT, cfg.SOLUTION_MASS]
    teasers = []
    for card, hue in zip(cards, hues):
        frac = eq([r"\frac{", r"\text{glucose}", "}{", "?", "}"], cfg.FONT["section"])
        frac[1].set_color(cfg.SOLUTE)
        frac[3].set_color(hue)
        teasers.append(frac.next_to(card.number, DOWN, buff=0.2))
    scene.play(*[FadeOut(c) for c in checks], *[fade_through(c.label, tz) for c, tz in zip(cards, teasers)],
               *[c.number.animate.set_color(cfg.WHITE) for c in cards], run_time=1.2)
    for card, tz in zip(cards, teasers):
        card.remove(card.label)
        scene.remove(card.label)
    scene.play(*[Indicate(tz[3], color=hue, scale_factor=1.5) for tz, hue in zip(teasers, hues)], run_time=1.4)

    # --- 10. Change the comparison, the number changes -----------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(glass.set_glow(1.0), Indicate(cards[0].number, color=cfg.VOLUME, scale_factor=1.06), run_time=1.3)
    scene.play(glass.set_glow(0.0), set_attr(stage, swarm, "solvent_glow", 1.0),
               Indicate(cards[1].number, color=cfg.SOLVENT_MASS, scale_factor=1.06), run_time=1.3)
    scene.play(set_attr(stage, swarm, "solvent_glow", 0.0), Indicate(cards[2].number, color=cfg.AMOUNT, scale_factor=1.06),
               run_time=1.3)
    unchanged = caption("Nothing in the glass changes.", cfg.CYAN, y=-3.65)
    scene.play(FadeIn(unchanged), Indicate(cards[3].number, color=cfg.SOLUTION_MASS, scale_factor=1.06), run_time=1.3)

    # --- 11. Not things to memorise: things to picture -------------------------------------------------------------------
    beat(scene, t, 10)
    memorise = txt("memorise", cfg.FONT["title"], cfg.MUTED).move_to([-3.2, 3.4, 0])
    picture = txt("picture", cfg.FONT["title"], cfg.CYAN).move_to([3.2, 3.4, 0])
    arrow = glow_arrow([-1.2, 3.4, 0], [1.6, 3.4, 0], cfg.CYAN)
    scene.play(FadeOut(banner), FadeOut(unchanged), run_time=0.4)
    scene.play(FadeIn(memorise), run_time=0.5)
    scene.play(Create(strike(memorise)), run_time=0.6)
    scene.play(GrowFromEdge(arrow, LEFT), FadeIn(picture, shift=LEFT * 0.2), run_time=1.0)

    # --- 12. Look inside the solution: the title ---------------------------------------------------------------------------
    beat(scene, t, 11)
    leftovers = [m for m in scene.mobjects if m not in (stage,) and not getattr(m, "_is_project_background", False)]
    scene.play(*[FadeOut(m) for m in leftovers], stage.zoom_to(0.9), stage.fade(stage, 0.0), run_time=2.4)
    stage.clear_updaters()
    scene.remove(stage)
    card = title_card("CONCENTRATION", "Explained Visually").move_to([0, 0.5, 0])
    subtitle = txt(cfg.VIDEO_SUBTITLE, cfg.FONT["small"], cfg.MUTED).next_to(card, DOWN, buff=0.45)
    fit_width(subtitle, 13.0)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=1.6)
    scene.play(FadeIn(subtitle), run_time=0.8)
    scene.play(Indicate(card.title[0], color=cfg.WHITE, scale_factor=1.03), run_time=1.4)
    scene.play(card.animate.scale(1.04), run_time=10.5, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
