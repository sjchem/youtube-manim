"""Chapter 08 — two lone pairs: water, the trend, and the opening mystery solved.

The ammonia model from chapter 07 loses one more hydrogen to a lone pair and
its nitrogen becomes oxygen. Hiding the lone pairs leaves a bent molecule,
which is turned so the H-O-H plane faces the camera; the live arc then closes
from ammonia's angle to water's measured one. The line-up uses the measured
angles from ``geometry_data``, and the closing pair repeats the opening
shot with the regions now visible.
"""

from manim_scenes.common import *

MODEL_AT = np.array([-2.2, -0.35, 0])
PANEL_X = 4.3


class Scene08Water(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "Water: two lone pairs")
    water = ml.molecule("H2O")
    new_lone = sorted(water.lone_pair_indices() - ml.molecule("NH3").lone_pair_indices())[0]

    # --- 1. From ammonia: one more hydrogen becomes a lone pair --------------------------------------------
    stage = Stage(MODEL_AT, zoom=1.12, yaw=0.0, pitch=0.25, sway=0.12)
    model = MoleculeModel(stage, ml.molecule("NH3"))
    name = formula("NH3", cfg.FONT["section"]).move_to([PANEL_X, 2.75, 0])
    show(scene, stage, 1.0, FadeIn(name))
    dismiss_opening_title(scene, t, head, at=2.6)
    new_name = formula("H2O", cfg.FONT["section"]).move_to(name)
    valence = chip(f"O: {gd.VALENCE_ELECTRONS['O']} valence electrons", cfg.WHITE, cfg.FONT["label"])
    valence.move_to([PANEL_X, 1.6, 0])
    scene.play(*model.swap_center("O"), *model.to_lone_pair(new_lone), fade_through(name, new_name),
               *stage.turn(yaw=0.5), run_time=2.0)
    scene.remove(name)
    scene.play(FadeIn(valence, shift=UP * 0.1), run_time=0.8)

    # --- 2. Two bond, four form two lone pairs -----------------------------------------------------------------
    beat(scene, t, 1)
    split = VGroup(txt("2 for bonds", cfg.FONT["body"], cfg.CYAN),
                   txt("4 = 2 lone pairs", cfg.FONT["body"], cfg.PURPLE)).arrange(DOWN, buff=0.3)
    split.move_to([PANEL_X, 0.2, 0])
    scene.play(FadeIn(split[0], shift=UP * 0.1), *model.fade("domains", 1.0), run_time=1.0)
    scene.play(FadeIn(split[1], shift=UP * 0.1), *[stage.fade(model.lobes[i], 0.5) for i in model.lone()],
               run_time=1.0)
    scene.play(*[stage.fade(model.lobes[i], 1.0) for i in model.lone()], run_time=0.8)

    # --- 3. Four regions again: AX2E2 --------------------------------------------------------------------------
    beat(scene, t, 2)
    code = axe_eq(len(water.bonds), len(water.lone_pairs), cfg.FONT["section"]).move_to([PANEL_X, 1.8, 0])
    regions = txt("4 regions", cfg.FONT["body"], cfg.CYAN).move_to([PANEL_X, 0.95, 0])
    scene.play(FadeOut(valence), FadeOut(split), run_time=0.5)
    scene.play(FadeIn(code, shift=UP * 0.1), FadeIn(regions), run_time=0.7)
    scene.play(stage.set_spin(0.35), run_time=1.2)

    # --- 4. Electron geometry: still tetrahedral ---------------------------------------------------------------
    beat(scene, t, 3)
    tetra = faces(stage, [model._site_point(i) for i in range(4)], ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)))
    egeo = shape_name(water.electron_geometry, cfg.CYAN, cfg.FONT["body"]).move_to([PANEL_X, 0.2, 0])
    e_title = txt("electron geometry", cfg.FONT["label"], cfg.MUTED).next_to(egeo, UP, buff=0.2)
    scene.play(*[stage.fade(f, 1.0) for f in tetra], FadeOut(regions), run_time=0.6)
    scene.play(FadeIn(e_title), FadeIn(egeo), run_time=0.8)

    # --- 5. Hide the lone pairs -----------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[stage.fade(f, 0.0) for f in tetra], *model.show_lone_pairs(0.0), *model.fade("domains", 0.0),
               stage.set_spin(0.0), run_time=1.6)

    # --- 6. Bent: turn the H-O-H plane to face us ------------------------------------------------------------------
    beat(scene, t, 5)
    bonds = model.bonded()
    face_on = bisect_down(model.dirs[bonds[0]], model.dirs[bonds[1]])
    scene.play(stage.align(face_on), *stage.turn(yaw=0.0, pitch=0.0), run_time=2.2, rate_func=smooth)
    mgeo = shape_name(water.shape, size=cfg.FONT["body"]).move_to([PANEL_X, -1.45, 0])
    m_title = txt("molecular geometry", cfg.FONT["label"], cfg.MUTED).next_to(mgeo, UP, buff=0.2)
    scene.play(FadeIn(m_title), FadeIn(mgeo, shift=UP * 0.1), run_time=1.0)

    # --- 7. The angle: about 104.5, smaller again ---------------------------------------------------------------------
    beat(scene, t, 6)
    arc = model.arc(bonds[0], bonds[1], radius=1.1, live=True, label_gap=0.6, size=cfg.FONT["body"])
    scene.play(stage.fade(arc, 1.0), run_time=0.8)
    scene.play(*[model.aim(i, model.orient @ water.sites[i].direction) for i in range(4)], run_time=3.0,
               rate_func=smooth)

    # --- 8. Two lone pairs crowd more ------------------------------------------------------------------------------------
    beat(scene, t, 7)
    crowd = caption("Two lone pairs crowd the bonds more", cfg.PURPLE)
    scene.play(*model.show_lone_pairs(0.75), FadeIn(crowd), run_time=1.4)
    scene.play(*stage.turn(yaw=0.7), run_time=3.0, rate_func=there_and_back)

    # --- 9-11. Side by side: CH4, NH3, H2O ---------------------------------------------------------------------------------
    beat(scene, t, 8)
    hide(scene, stage, 0.8, FadeOut(VGroup(crowd, new_name, code, e_title, egeo, m_title, mgeo)))
    lineup = []
    for k, key in enumerate(("CH4", "NH3", "H2O")):
        spec = ml.molecule(key)
        # Every model shows the same measured pair (sites 2 and 3) face-on, opening downward.
        orient = bisect_down(spec.sites[2].direction, spec.sites[3].direction)
        small = Stage([(k - 1) * 4.7, 0.9, 0], zoom=0.78, yaw=0.0, pitch=0.12, sway=0.22)
        mini = MoleculeModel(small, spec, orient=orient)
        arc_mini = mini.arc(2, 3, radius=1.1, label=degrees_label(gd.BOND_ANGLE_DEG[key], cfg.FONT["body"]),
                            label_gap=0.55)
        arc_mini.presence = 1.0
        small.presence = 0.0
        small.refresh()
        scene.add(small)
        lone = len(spec.lone_pairs)
        tag = VGroup(formula(key, cfg.FONT["body"]),
                     txt(f"{lone} lone pair" + ("" if lone == 1 else "s"), cfg.FONT["label"], cfg.PURPLE))
        tag.arrange(DOWN, buff=0.2).move_to([(k - 1) * 4.7, -2.2, 0])
        lineup.append((small, tag))
    for k, (small, tag) in enumerate(lineup):
        if k:
            beat(scene, t, 8 + k)
        scene.play(small.fade(small, 1.0), FadeIn(tag, shift=UP * 0.15), run_time=1.2)
        scene.play(Indicate(tag[1], color=cfg.WHITE, scale_factor=1.06), run_time=1.0)

    # --- 12. Same electron geometry, three shapes ------------------------------------------------------------------------------
    beat(scene, t, 11)
    same = top_caption("Same four regions · three shapes", cfg.CYAN)
    shapes = VGroup(*[shape_name(ml.molecule(k).shape, size=cfg.FONT["label"]).next_to(tag, DOWN, buff=0.2)
                      for k, (_, tag) in zip(("CH4", "NH3", "H2O"), lineup)])
    scene.play(FadeIn(same), LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in shapes], lag_ratio=0.3), run_time=1.6)

    # --- 13. VSEPR predicts the trend ---------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    for small, _ in lineup:
        small.clear_updaters()
    scene.play(*[FadeOut(small) for small, _ in lineup], *[FadeOut(tag) for _, tag in lineup], FadeOut(shapes),
               FadeOut(same), run_time=0.9)
    for small, _ in lineup:
        scene.remove(small)
    angles = [gd.BOND_ANGLE_DEG[k] for k in ("CH4", "NH3", "H2O")]
    trend = VGroup()
    for k, value in enumerate(angles):
        trend.add(VGroup(degrees_label(value, cfg.FONT["section"]),
                         txt(f"{k} lone pair" + ("" if k == 1 else "s"), cfg.FONT["label"], cfg.PURPLE))
                  .arrange(DOWN, buff=0.25))
    trend.arrange(RIGHT, buff=1.6).move_to([0, 1.3, 0])
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.25, color=cfg.MUTED, stroke_width=6)
                      for a, b in zip(trend[:-1], trend[1:])])
    qual = chip("VSEPR: a qualitative model", cfg.CYAN, cfg.FONT["body"]).move_to([0, -0.6, 0])
    scene.play(FadeIn(qual), LaggedStart(*[FadeIn(g, shift=RIGHT * 0.2) for g in trend], lag_ratio=0.3),
               run_time=1.6)
    scene.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.4), run_time=1.2)

    # --- 14. The exact numbers are measured ---------------------------------------------------------------------------------------
    beat(scene, t, 13)
    measured = chip("exact angles: measured", cfg.GOLD, cfg.FONT["body"]).move_to([0, -1.75, 0])
    depend = caption("They depend on the atoms and the full electronic structure", cfg.WHITE)
    scene.play(FadeIn(measured, shift=UP * 0.1), FadeIn(depend), run_time=1.2)

    # --- 15. No simple formula --------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    fake = eq(r"\theta = 109.5^\circ - k\times(\text{lone pairs})", cfg.FONT["body"], cfg.MUTED).move_to([0, -0.6, 0])
    strike = Line(fake.get_corner(DL) + LEFT * 0.1, fake.get_corner(UR) + RIGHT * 0.1, stroke_color=cfg.RED, stroke_width=8)
    scene.play(fade_through(qual, fake), run_time=0.9)
    scene.remove(qual)
    scene.play(Create(strike), run_time=0.7)

    # --- 16-18. Back to the opening mystery -------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    scene.play(FadeOut(VGroup(trend, arrows, measured, depend, fake, strike)), run_time=0.8)
    co2_stage = Stage([-4.0, 0.5, 0], zoom=0.95, yaw=0.5, pitch=0.3, sway=0.15)
    co2 = MoleculeModel(co2_stage, ml.molecule("CO2"), domains=True)
    h2o_stage = Stage([4.0, 0.7, 0], zoom=0.95, yaw=0.0, pitch=0.15, sway=0.15)
    h2o = MoleculeModel(h2o_stage, water, orient=bisect_down(water.bonds[0].direction, water.bonds[1].direction),
                        domains=True)
    labels = VGroup(VGroup(formula("CO2", cfg.FONT["body"]), txt("2 regions", cfg.FONT["body"], cfg.CYAN)),
                    VGroup(formula("H2O", cfg.FONT["body"]), txt("4 regions", cfg.FONT["body"], cfg.CYAN)))
    for group, x in zip(labels, (-4.0, 4.0)):
        group.arrange(DOWN, buff=0.22).move_to([x, -2.35, 0])
    show(scene, h2o_stage, 1.2, FadeIn(labels[1]))
    scene.play(Indicate(labels[1][1], color=cfg.PURPLE, scale_factor=1.08), run_time=1.2)
    beat(scene, t, 16)
    show(scene, co2_stage, 1.2, FadeIn(labels[0]))
    scene.play(Indicate(labels[0][1], color=cfg.WHITE, scale_factor=1.08), run_time=1.2)
    beat(scene, t, 17)
    verdict = top_caption("Water: 2 bonds + 2 lone pairs. CO₂: 2 bonds.", cfg.GREEN)
    scene.play(FadeIn(verdict), *h2o.fade("domains", 0.0), *co2.fade("domains", 0.0), run_time=1.2)
    scene.play(co2_stage.set_spin(0.4), *h2o_stage.turn(yaw=0.8), run_time=3.0)

    # --- 19. Bigger molecules: the same counting -------------------------------------------------------------------------------------------
    beat(scene, t, 18)
    hide(scene, co2_stage, 0.8, FadeOut(labels), FadeOut(verdict))
    hide(scene, h2o_stage, 0.4)
    five = Stage([0, -0.1, 0], zoom=0.95, yaw=0.4, pitch=0.3, spin=0.4)
    RegionModel(five, pm.ideal_directions(5))
    more = caption("More regions, same counting", cfg.CYAN)
    show(scene, five, 1.2, FadeIn(more))
    scene.play(*five.turn(pitch=0.6), run_time=2.6, rate_func=there_and_back)
    scene.play(Indicate(more, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
