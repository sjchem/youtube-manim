"""Chapter 10 — one family, four shapes: PCl5 -> SF4 -> ClF3 -> XeF2.

One central model keeps all five region directions on screen (dashed
guides) while sites turn, one at a time, from atoms into lone pairs. A trial
lone pair first tries an axial site, then an equatorial one; the red arcs
are its 90-degree neighbours as counted by ``physics_models.neighbours_at_90``
(three versus two). Each family member is the library molecule, so the
seesaw's and the T's small distortions are the measured ones.
"""

from manim_scenes.common import *

CENTER = np.array([-1.7, -0.35, 0])
PANEL_X = 4.7


class Scene10TbpFamily(Scene):
    def construct(self) -> None:
        play_scene(self)


def panel_for(key: str) -> VGroup:
    mol = ml.molecule(key)
    group = VGroup(formula(key, cfg.FONT["section"]), axe_eq(len(mol.bonds), len(mol.lone_pairs), cfg.FONT["section"]))
    return group.arrange(DOWN, buff=0.35).move_to([PANEL_X, 1.9, 0])


def swap_panel(scene: Scene, panel: VGroup, key: str, *anims: Animation, run_time: float = 2.0) -> VGroup:
    """Morph the model (``anims``) while the formula and code fade through."""
    new = panel_for(key)
    scene.play(*anims, fade_through(panel, new), run_time=run_time)
    scene.remove(panel)
    return new


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "One family, four shapes")
    stage = Stage(CENTER, zoom=0.98, yaw=0.5, pitch=0.28, sway=0.1)
    model = MoleculeModel(stage, ml.molecule("PCl5"), guides=True)
    panel = panel_for("PCl5")
    show(scene, stage, 1.0, FadeIn(panel))
    dismiss_opening_title(scene, t, head)

    # --- 1. Two kinds of place for a lone pair ----------------------------------------------------------------
    trial_dir = [model.dirs[pm.AXIAL[0]].copy()]
    trial = region_lobe(ORIGIN, lambda: trial_dir[0], "E")
    trial.presence = 0.0
    stage.add_body(trial)
    replace = caption("Try a lone pair in each kind of place", cfg.PURPLE)
    scene.play(FadeIn(replace), run_time=0.8)

    def move_trial(direction, **kwargs) -> Param:
        def setter(v):
            trial_dir[0] = mu.unit(v)
        return stage.tween(lambda: trial_dir[0], setter, mu.unit(direction), mode="direction", **kwargs)

    def contact_arcs(site: int, color: str) -> list[AngleArc]:
        arcs = []
        for j in pm.neighbours_at_90(5, site):
            arc = AngleArc(ORIGIN, lambda: trial_dir[0], model._dir(j), 1.5, color, width=7)
            arc.presence = 0.0
            stage.add_overlay(arc)
            arcs.append(arc)
        return arcs

    # --- 2. Axial: three neighbours at 90 degrees ----------------------------------------------------------------
    beat(scene, t, 1)
    axial_site = pm.AXIAL[0]
    scene.play(*model.fade("atoms", 0.15, [axial_site]), *model.fade("rods", 0.0, [axial_site]),
               stage.fade(trial, 1.0), FadeOut(replace), run_time=1.0)
    red = contact_arcs(axial_site, cfg.RED)
    count = VGroup(txt(f"{len(red)} ×", cfg.FONT["section"], cfg.RED), degrees_label(90, cfg.FONT["section"], cfg.RED))
    count.arrange(RIGHT, buff=0.2).move_to([PANEL_X, -0.4, 0])
    scene.play(*[stage.fade(a, 1.0) for a in red], FadeIn(count), run_time=1.2)
    scene.play(*stage.turn(yaw=0.85), run_time=2.2, rate_func=there_and_back)

    # --- 3. Equatorial: only two at 90; the rest at 120 -----------------------------------------------------------------
    beat(scene, t, 2)
    eq_site = sorted(ml.molecule("SF4").lone_pair_indices())[0]
    scene.play(*[stage.fade(a, 0.0) for a in red], *model.fade("atoms", 1.0, [axial_site]),
               *model.fade("rods", 1.0, [axial_site]), *model.fade("atoms", 0.15, [eq_site]),
               *model.fade("rods", 0.0, [eq_site]), move_trial(model.dirs[eq_site]), run_time=1.8)
    fewer = contact_arcs(eq_site, cfg.RED)
    roomy = [AngleArc(ORIGIN, lambda: trial_dir[0], model._dir(j), 1.5, cfg.GREEN, width=7)
             for j in range(5) if j != eq_site and j not in pm.neighbours_at_90(5, eq_site)]
    for arc in roomy:
        arc.presence = 0.0
        stage.add_overlay(arc)
    count2 = VGroup(txt(f"{len(fewer)} ×", cfg.FONT["section"], cfg.RED), degrees_label(90, cfg.FONT["section"], cfg.RED))
    count2.arrange(RIGHT, buff=0.2).move_to(count)
    scene.play(*[stage.fade(a, 1.0) for a in fewer], fade_through(count, count2), run_time=1.2)
    scene.remove(count)
    scene.play(*[stage.fade(a, 1.0) for a in roomy], run_time=1.0)

    # --- 4. The equator wins --------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    wins = caption("90° contacts are the most crowded: the equator wins", cfg.GREEN)
    scene.play(FadeIn(wins), Indicate(count2, color=cfg.GREEN, scale_factor=1.1), run_time=1.4)

    # --- 5. Sulfur tetrafluoride: AX4E ------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[stage.fade(a, 0.0) for a in fewer + roomy], stage.fade(trial, 0.0), FadeOut(wins), FadeOut(count2),
               run_time=0.8)
    panel = swap_panel(scene, panel, "SF4", *model.become(ml.molecule("SF4")))

    # --- 6. Hide the lone pair: a seesaw -------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    shape = shape_name("seesaw", size=cfg.FONT["section"]).move_to([PANEL_X, -0.4, 0])
    scene.play(*model.show_lone_pairs(0.0), *stage.turn(yaw=-1.1, pitch=0.15), run_time=1.8)
    scene.play(FadeIn(shape, shift=UP * 0.1), run_time=0.9)
    nudge = caption("Measured: the bonds lean away from the lone pair", cfg.WHITE)
    scene.play(FadeIn(nudge), run_time=0.8)

    # --- 7. A second lone pair: also equatorial -------------------------------------------------------------------------------------
    beat(scene, t, 6)
    clf3 = ml.molecule("ClF3")
    second = sorted(clf3.lone_pair_indices() - ml.molecule("SF4").lone_pair_indices())[0]
    scene.play(*model.show_lone_pairs(1.0), FadeOut(nudge), FadeOut(shape), *stage.turn(yaw=0.5, pitch=0.3),
               run_time=1.2)
    panel = swap_panel(scene, panel, "ClF3", *model.become(clf3))
    lp_arc = model.arc(eq_site, second, radius=1.25, label=degrees_label(120, cfg.FONT["body"]), label_gap=0.55)
    scene.play(stage.fade(lp_arc, 1.0), run_time=0.9)

    # --- 8. Chlorine trifluoride: a T --------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    shape = shape_name(clf3.shape, size=cfg.FONT["section"]).move_to([PANEL_X, -0.4, 0])
    scene.play(stage.fade(lp_arc, 0.0), *model.show_lone_pairs(0.0), *stage.turn(yaw=np.pi / 2, pitch=0.05),
               run_time=2.0)
    scene.play(FadeIn(shape, shift=UP * 0.1), run_time=0.9)

    # --- 9. A third lone pair fills the equator ----------------------------------------------------------------------------------------
    beat(scene, t, 8)
    xef2 = ml.molecule("XeF2")
    scene.play(FadeOut(shape), *model.show_lone_pairs(1.0), *stage.turn(yaw=0.5, pitch=0.3), run_time=1.2)
    panel = swap_panel(scene, panel, "XeF2", *model.become(xef2), run_time=1.8)

    # --- 10. Xenon difluoride: AX2E3 ----------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    ring = faces(stage, [model._site_point(i, 0.7) for i in sorted(xef2.lone_pair_indices())], ((0, 1, 2),),
                 cfg.PURPLE, 0.12, 0.6)
    scene.play(stage.fade(ring[0], 1.0), stage.set_spin(0.3), run_time=1.4)

    # --- 11. Linear --------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    straight = model.arc(pm.AXIAL[0], pm.AXIAL[1], radius=1.2, label=degrees_label(180, cfg.FONT["body"]), label_gap=0.6)
    shape = shape_name(xef2.shape, size=cfg.FONT["section"]).move_to([PANEL_X, -0.4, 0])
    scene.play(stage.set_spin(0.0), stage.fade(ring[0], 0.0), *model.show_lone_pairs(0.0), *stage.turn(yaw=-0.4, pitch=0.1),
               run_time=1.6)
    scene.play(stage.fade(straight, 1.0), FadeIn(shape, shift=UP * 0.1), run_time=1.0)

    # --- 12. Like CO2, for a different reason ---------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    co2_stage, _ = mini_model("CO2", [PANEL_X, -2.2, 0], zoom=0.55, spin=0.4)
    scene.add(co2_stage)
    scene.play(co2_stage.fade(co2_stage, 1.0), run_time=1.0)
    reason = caption("Same line, different reason", cfg.GOLD)
    scene.play(*model.show_lone_pairs(0.7), FadeIn(reason), run_time=1.2)

    # --- 13-14. The whole family -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    co2_stage.clear_updaters()
    scene.play(FadeOut(co2_stage), FadeOut(reason), FadeOut(panel), FadeOut(shape), stage.fade(straight, 0.0), run_time=0.8)
    scene.remove(co2_stage)
    hide(scene, stage, 0.7)
    keys = ("PCl5", "SF4", "ClF3", "XeF2")
    family = []
    for k, key in enumerate(keys):
        small, _ = mini_model(key, [(k - 1.5) * 3.55, 0.75, 0], zoom=0.62, lone_pairs=0.45, yaw=-0.65, pitch=0.28,
                              spin=0.0)
        small.sway = 0.16
        family.append(small)
        scene.add(small)
    tags = VGroup(*[VGroup(formula(key, cfg.FONT["body"]),
                           shape_name("trigonal\nbipyramidal" if key == "PCl5" else ml.molecule(key).shape, size=cfg.FONT["small"])).arrange(DOWN, buff=0.22)
                    .move_to([(k - 1.5) * 3.55, -2.45, 0]) for k, key in enumerate(keys)])
    same = top_caption("Same five-region arrangement", cfg.CYAN)
    scene.play(*[s.fade(s, 1.0) for s in family], FadeIn(same), run_time=1.4)
    scene.play(LaggedStart(*[FadeIn(tag[0]) for tag in tags], lag_ratio=0.25), run_time=1.6)
    beat(scene, t, 13)
    scene.play(LaggedStart(*[FadeIn(tag[1]) for tag in tags], lag_ratio=0.4), run_time=2.4)
    rule = top_caption("Lone pairs claim the equator first", cfg.PURPLE)
    scene.play(fade_through(same, rule), run_time=1.0)
    scene.remove(same)

    # --- 15. One pattern ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    scene.play(LaggedStart(*[Indicate(tag[1], color=cfg.WHITE, scale_factor=1.06) for tag in tags], lag_ratio=0.25),
               run_time=2.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
