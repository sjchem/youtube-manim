"""Chapter 01 — the shape mystery: two flat Lewis structures lift into 3D.

Both molecules start as Lewis structures drawn in a straight line. The 3D
models are built at exactly the Lewis positions (front view, no perspective
at depth zero), so the letters can hand over to the atoms in place. Then the
camera tips, carbon dioxide stays straight, and water bends while a live
readout reports the angle actually drawn, from 180 down to the measured value.
"""

from manim_scenes.common import *

CO2_AT = np.array([-4.0, 0.7, 0])
H2O_AT = np.array([4.0, 1.0, 0])
LEWIS_BOND = 2.3


class Scene01ShapeMystery(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")   # a cold open: the heading is the title card at the end

    # --- 1. Two flat Lewis structures, three atoms each -------------------------------------------
    co2_lewis = Lewis("C", [("O", 180, 2), ("O", 0, 2)], at=CO2_AT, bond=LEWIS_BOND)
    h2o_lewis = Lewis("O", [("H", 180, 1), ("H", 0, 1)], central_lone=[90, 270], at=H2O_AT, bond=LEWIS_BOND)
    names = VGroup(formula("CO2").move_to([CO2_AT[0], -1.65, 0]), formula("H2O").move_to([H2O_AT[0], -1.65, 0]))
    counts = VGroup(chip("3 atoms", cfg.CYAN).move_to([CO2_AT[0], -2.7, 0]),
                    chip("3 atoms", cfg.CYAN).move_to([H2O_AT[0], -2.7, 0]))
    scene.play(Write(co2_lewis), Write(h2o_lewis), run_time=2.4)
    scene.play(FadeIn(names, shift=UP * 0.15), run_time=0.8)
    for lewis, count in zip((co2_lewis, h2o_lewis), counts):
        atoms = [lewis.ligand_symbols[0], lewis.center_symbol, lewis.ligand_symbols[1]]
        scene.play(LaggedStart(*[Indicate(atom, color=cfg.CYAN, scale_factor=1.25) for atom in atoms],
                               lag_ratio=0.35), FadeIn(count, shift=UP * 0.1), run_time=1.4)

    # --- 2. On paper, both are straight lines --------------------------------------------------------
    beat(scene, t, 1)
    guides = VGroup(*[DashedLine(at + LEFT * 3.3, at + RIGHT * 3.3, stroke_color=cfg.MUTED, stroke_width=3,
                                 dash_length=0.12) for at in (CO2_AT, H2O_AT)])
    paper = caption("Lewis structures: flat, on paper", cfg.MUTED)
    scene.play(Create(guides), FadeIn(paper), run_time=1.6)
    scene.play(Indicate(h2o_lewis.lone_dots, color=cfg.WHITE, scale_factor=1.4), run_time=1.2)

    # --- 3. Lift them into three dimensions ------------------------------------------------------------
    beat(scene, t, 2)
    co2_stage = Stage(CO2_AT, zoom=1.0)
    co2 = MoleculeModel(co2_stage, ml.molecule("CO2"), bond=LEWIS_BOND)
    water_spec = ml.molecule("H2O")
    turn = bisect_down(water_spec.sites[2].direction, water_spec.sites[3].direction)
    h2o_stage = Stage(H2O_AT, zoom=1.0)
    h2o = MoleculeModel(h2o_stage, water_spec, bond=LEWIS_BOND, lone_pairs=False, orient=turn)
    bent = [h2o.dirs[i].copy() for i in range(4)]
    h2o.dirs[2], h2o.dirs[3] = RIGHT.astype(float), LEFT.astype(float)   # drawn straight, as on paper
    h2o.dirs[0], h2o.dirs[1] = UP.astype(float), DOWN.astype(float)
    h2o_stage.refresh()
    for stage in (co2_stage, h2o_stage):
        stage.presence = 0.0
        scene.add(stage)
    lift = caption("Into three dimensions", cfg.CYAN)
    scene.play(FadeOut(co2_lewis), FadeOut(h2o_lewis), FadeOut(guides),
               co2_stage.fade(co2_stage, 1.0), h2o_stage.fade(h2o_stage, 1.0), run_time=1.6)
    swap(scene, paper, lift)
    co2_stage.sway = h2o_stage.sway = 0.18
    scene.play(*co2_stage.turn(yaw=0.55, pitch=0.32), *h2o_stage.turn(yaw=-0.45, pitch=0.28),
               co2_stage.zoom_to(1.05), h2o_stage.zoom_to(1.05), run_time=2.6, rate_func=smooth)

    # --- 4. Carbon dioxide stays straight --------------------------------------------------------------------
    beat(scene, t, 3)
    co2_arc = co2.arc(0, 1, radius=1.2, live=True, label_gap=0.55, size=cfg.FONT["body"])
    scene.play(co2_stage.fade(co2_arc, 1.0), FadeOut(counts[0]), run_time=1.2)
    scene.play(*co2_stage.turn(yaw=1.35, pitch=0.4), run_time=3.2, rate_func=there_and_back)

    # --- 5. Water bends ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    h2o_arc = h2o.arc(2, 3, radius=1.05, live=True, label_gap=0.5, size=cfg.FONT["body"])
    scene.play(h2o_stage.fade(h2o_arc, 1.0), FadeOut(counts[1]), FadeOut(lift), run_time=0.8)
    scene.play(h2o.aim(2, bent[2]), h2o.aim(3, bent[3]), h2o.aim(0, bent[0]), h2o.aim(1, bent[1]),
               run_time=3.4, rate_func=smooth)
    scene.play(Indicate(names[1], color=cfg.GOLD, scale_factor=1.1), run_time=1.0)

    # --- 6. Why? ---------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    question = txt("?", 170, cfg.GOLD).move_to([0, 0.6, 0])
    glow = question.copy().set_stroke(cfg.GOLD, width=22, opacity=0.18).set_fill(opacity=0)
    decorative(glow)
    why = caption("Same number of atoms. Different shapes.", cfg.WHITE)
    scene.play(FadeIn(question, scale=0.6), FadeIn(glow, scale=0.6), FadeIn(why), run_time=1.0)
    scene.play(question.animate.scale(1.08), glow.animate.scale(1.08), run_time=1.4, rate_func=there_and_back)
    scene.play(*h2o_stage.turn(yaw=0.6, pitch=0.5), run_time=2.6, rate_func=smooth)

    # --- 7. The hidden electrons, and the title -------------------------------------------------------------
    beat(scene, t, 6)
    hidden = caption("The answer: electrons we cannot see", cfg.PURPLE)
    scene.play(*h2o.show_lone_pairs(1.0), FadeOut(question), FadeOut(glow), run_time=1.6)
    swap(scene, why, hidden)
    card = title_card("MOLECULAR GEOMETRY", "Explained Visually")
    card.scale(0.9).move_to([0, -1.9, 0])
    scene.play(FadeOut(hidden), FadeOut(names), co2_stage.glide([-4.2, 1.6, 0]), h2o_stage.glide([4.2, 2.0, 0]),
               co2_stage.zoom_to(0.9), h2o_stage.zoom_to(0.9), run_time=1.5)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=1.3)
    scene.play(Indicate(card.title[0], color=cfg.WHITE, scale_factor=1.03), run_time=1.4)
    scene.play(*h2o_stage.turn(yaw=-0.3), *co2_stage.turn(yaw=0.2), run_time=2.2, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
