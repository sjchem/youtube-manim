"""Chapter 05 — two regions make a line (CO2), three make a flat triangle (BF3).

Each molecule is read the same way: Lewis structure on the left, the count
(regions and lone pairs, from the molecule library), then the 3D model on
the right with its regions, its angles and its shape name. Boron trifluoride
is turned edge-on, where a planar molecule collapses into a line.
"""

from manim_scenes.common import *

LEWIS_AT = np.array([-4.3, 0.55, 0])
MODEL_AT = np.array([2.7, -0.15, 0])


class Scene05LinearPlanar(Scene):
    def construct(self) -> None:
        play_scene(self)


def counts(mol: ml.Molecule, at) -> VGroup:
    group = VGroup(chip(f"{mol.regions} regions", cfg.CYAN, cfg.FONT["label"]),
                   chip(f"{len(mol.lone_pairs)} lone pairs", cfg.PURPLE, cfg.FONT["label"]))
    return group.arrange(DOWN, buff=0.25).move_to(at)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Linear and trigonal planar")

    # --- 1. Carbon dioxide ------------------------------------------------------------------------------------
    co2_spec = ml.molecule("CO2")
    lewis = Lewis("C", [("O", 180, 2), ("O", 0, 2)], at=LEWIS_AT, bond=1.9, size=88, ligand_size=76)
    name = formula("CO2", cfg.FONT["section"]).move_to(LEWIS_AT + UP * 1.7)
    scene.play(Write(lewis), FadeIn(name), run_time=1.6)
    dismiss_opening_title(scene, t, head)

    # --- 2. Two regions, no lone pairs --------------------------------------------------------------------------
    beat(scene, t, 1)
    tally = counts(co2_spec, LEWIS_AT + DOWN * 1.9)
    scene.play(LaggedStart(*[Indicate(b, color=cfg.CYAN, scale_factor=1.3) for b in lewis.bond_lines], lag_ratio=0.4),
               FadeIn(tally[0], shift=UP * 0.1), run_time=1.6)
    scene.play(Indicate(lewis.center_symbol, color=cfg.PURPLE, scale_factor=1.2), FadeIn(tally[1], shift=UP * 0.1),
               run_time=1.2)

    # --- 3. Opposite sides: AX2, linear -------------------------------------------------------------------------
    beat(scene, t, 2)
    stage = Stage(MODEL_AT, zoom=1.15, yaw=0.35, pitch=0.25, sway=0.15)
    model = MoleculeModel(stage, co2_spec, domains=True)
    for i, d in enumerate(pm.RELAXATION_STARTS[2]):
        model.dirs[i] = mu.unit(d)
    stage.refresh()
    show(scene, stage, 1.0)
    scene.play(*[model.aim(i, site.direction) for i, site in enumerate(co2_spec.sites)],
               run_time=2.2, rate_func=smooth)
    arc = model.arc(0, 1, radius=1.15, live=True, label_gap=0.55, size=cfg.FONT["body"])
    code = axe_eq(2, 0, cfg.FONT["section"]).move_to(MODEL_AT + np.array([-1.0, -2.55, 0]))
    shape = shape_name(co2_spec.shape, size=cfg.FONT["section"]).next_to(code, RIGHT, buff=0.6)
    scene.play(stage.fade(arc, 1.0), FadeIn(code), FadeIn(shape, shift=UP * 0.1), run_time=1.2)

    # --- 4. Spin it: still a rod ------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(stage.set_spin(1.1), *stage.turn(pitch=0.6), run_time=2.0)
    scene.play(stage.set_spin(0.25), *stage.turn(pitch=0.25), run_time=2.4)

    # --- 5. A double bond is still one region ---------------------------------------------------------------------
    beat(scene, t, 4)
    four = VGroup(txt("4 electrons", cfg.FONT["body"], cfg.WHITE), eq(r"\rightarrow", cfg.FONT["body"], cfg.MUTED),
                  txt("1 region", cfg.FONT["body"], cfg.CYAN)).arrange(RIGHT, buff=0.3)
    four.move_to([0, -3.65, 0])
    scene.play(FadeIn(four, shift=UP * 0.1), Indicate(lewis.bond_lines[1], color=cfg.WHITE, scale_factor=1.4),
               run_time=1.4)
    scene.play(*model.fade("domains", 0.45), run_time=1.0)
    scene.play(*model.fade("domains", 1.0), run_time=1.0)
    direction = txt("Direction counts, not pairs", cfg.FONT["body"], cfg.GOLD).move_to([0, -3.65, 0])
    scene.play(fade_through(four, direction), run_time=0.9)
    scene.remove(four)

    # --- 6. Boron trifluoride --------------------------------------------------------------------------------------
    beat(scene, t, 5)
    bf3_spec = ml.molecule("BF3")
    hide(scene, stage, 0.8, FadeOut(VGroup(lewis, name, tally, code, shape, direction)))
    lewis = Lewis("B", [("F", 90, 1), ("F", 210, 1), ("F", 330, 1)], at=LEWIS_AT + DOWN * 0.55, bond=1.5, size=88,
                  ligand_size=72)
    name = formula("BF3", cfg.FONT["section"]).move_to(LEWIS_AT + np.array([0, 2.4, 0]))
    tally = counts(bf3_spec, LEWIS_AT + DOWN * 2.85)
    scene.play(Write(lewis), FadeIn(name), run_time=1.5)
    scene.play(FadeIn(tally, shift=UP * 0.1), run_time=0.9)

    # --- 7. Three regions round a circle: 120 degrees ------------------------------------------------------------------
    beat(scene, t, 6)
    stage = Stage(MODEL_AT, zoom=1.1, yaw=0.0, pitch=0.0, sway=0.12)
    model = MoleculeModel(stage, bf3_spec, domains=True)
    show(scene, stage, 1.0)
    arcs = [model.arc(i, j, radius=0.98, label=degrees_label(bf3_spec.bond_angle(0, 1), cfg.FONT["label"]),
                      label_gap=0.55) for i, j in ((0, 1), (1, 2), (2, 0))]
    scene.play(*[stage.fade(a, 1.0) for a in arcs], run_time=1.2)
    scene.play(*model.fade("domains", 0.0), run_time=1.0)

    # --- 8. Edge-on: one plane ---------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    edge = caption("Edge on: all four atoms in one plane", cfg.WHITE)
    scene.play(*[stage.fade(a, 0.0) for a in arcs], FadeIn(edge), run_time=0.7)
    scene.play(*stage.turn(pitch=np.pi / 2 - 0.03), run_time=2.4, rate_func=smooth)
    scene.play(*stage.turn(yaw=0.6), run_time=1.6, rate_func=there_and_back)

    # --- 9. AX3: trigonal planar -----------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    code = axe_eq(3, 0, cfg.FONT["section"]).move_to(MODEL_AT + np.array([-1.5, -2.6, 0]))
    shape = shape_name(bf3_spec.shape, size=cfg.FONT["section"]).next_to(code, RIGHT, buff=0.5)
    scene.play(*stage.turn(pitch=0.55, yaw=0.3), FadeOut(edge), run_time=2.0, rate_func=smooth)
    scene.play(FadeIn(code), FadeIn(shape, shift=UP * 0.1), stage.set_spin(0.3), run_time=1.2)

    # --- 10. Two make a line; three a triangle; four cannot stay flat ------------------------------------------------------------
    beat(scene, t, 9)
    hide(scene, stage, 0.8, FadeOut(VGroup(lewis, name, tally, code, shape)))
    lineup = []
    for k, dirs in enumerate((pm.ideal_directions(2), pm.ideal_directions(3),
                              np.array([RIGHT, UP, LEFT, DOWN], dtype=float))):
        small = Stage([(k - 1) * 4.6, 0.4, 0], zoom=0.85, pitch=0.15, sway=0.15)
        RegionModel(small, dirs)
        lineup.append(small)
    labels = VGroup(txt("2: a line", cfg.FONT["body"], cfg.GREEN), txt("3: a triangle", cfg.FONT["body"], cfg.GREEN),
                    txt("4: flat?", cfg.FONT["body"], cfg.RED))
    for k, label in enumerate(labels):
        label.move_to([(k - 1) * 4.6, -2.4, 0])
    for small in lineup:
        small.presence = 0.0
        scene.add(small)
    scene.play(*[s.fade(s, 1.0) for s in lineup[:2]], FadeIn(labels[:2]), run_time=1.2)
    scene.play(lineup[2].fade(lineup[2], 1.0), FadeIn(labels[2]), run_time=1.0)
    cross = cross_mark(0.5).move_to(lineup[2].center_point() + UR * 1.5)
    scene.play(Create(cross), Indicate(labels[2], color=cfg.RED, scale_factor=1.1), run_time=1.2)
    scene.play(*lineup[2].turn(pitch=0.5), run_time=2.2, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
