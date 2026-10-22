"""Chapter 12 — flat from six: SF6 -> BrF5 -> XeF4.

The same octahedral model loses one site to a lone pair (square pyramid,
with the measured upward tilt of the base), then a second. A trial lone
pair is tried next to the first (90 degrees, red) and opposite it (180
degrees, green) — the placement ``best_lone_pair_sites`` picks — leaving
xenon tetrafluoride's four fluorines in a flat square.
"""

from manim_scenes.common import *

CENTER = np.array([-1.6, -0.3, 0])
PANEL_X = 4.7
# View the square pyramid slightly from below: the lower lone pair is
# on the near side of Br, while its actual octahedral direction is retained.
LONE_PAIR_VIEW_PITCH = -0.30


class Scene12FlatFromSix(Scene):
    def construct(self) -> None:
        play_scene(self)


def panel_for(key: str) -> VGroup:
    mol = ml.molecule(key)
    group = VGroup(formula(key, cfg.FONT["section"]), axe_eq(len(mol.bonds), len(mol.lone_pairs), cfg.FONT["section"]))
    return group.arrange(DOWN, buff=0.35).move_to([PANEL_X, 1.9, 0])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "Flat from six")
    stage = Stage(CENTER, zoom=1.0, yaw=0.45, pitch=0.3, sway=0.1)
    model = MoleculeModel(stage, ml.molecule("SF6"), guides=True)
    panel = panel_for("SF6")
    show(scene, stage, 1.0, FadeIn(panel))
    dismiss_opening_title(scene, t, head, at=2.6)
    scene.play(stage.set_spin(0.3), run_time=1.0)

    # --- 2. Every position the same: put the lone pair at the bottom ------------------------------------------------
    beat(scene, t, 1)
    brf5 = ml.molecule("BrF5")
    first = sorted(brf5.lone_pair_indices())[0]
    any_site = caption("Every position is equivalent", cfg.WHITE)
    scene.play(FadeIn(any_site), stage.set_spin(0.0),
               *stage.turn(yaw=0.45, pitch=LONE_PAIR_VIEW_PITCH), run_time=1.0)
    scene.play(*model.to_lone_pair(first), run_time=1.6)

    # --- 3. Bromine pentafluoride: AX5E ----------------------------------------------------------------------------------
    beat(scene, t, 2)
    new = panel_for("BrF5")
    scene.play(*model.become(brf5), fade_through(panel, new), FadeOut(any_site), run_time=1.8)
    scene.remove(panel)
    panel = new

    # --- 4. Hide it: square pyramidal --------------------------------------------------------------------------------------
    beat(scene, t, 3)
    shape = shape_name(brf5.shape, size=cfg.FONT["section"]).move_to([PANEL_X, -0.3, 0])
    base = faces(stage, [model._site_point(i) for i in (2, 4, 3, 5)], ((0, 1, 2, 3),), cfg.GREEN, 0.12, 0.6)
    scene.play(*model.show_lone_pairs(0.0), stage.fade(base[0], 1.0), run_time=1.4)
    scene.play(FadeIn(shape, shift=UP * 0.1), run_time=0.9)

    # --- 5. The base tilts up, away from the lone pair -----------------------------------------------------------------------
    beat(scene, t, 4)
    tilt = caption("The base tilts slightly up, away from it", cfg.WHITE)
    # Measure the opposite basal bond to keep the gold value clear of the near fluorine.
    apex_arc = model.arc(0, 3, radius=1.1, live=True, label_gap=0.6, size=cfg.FONT["body"])
    scene.play(*model.show_lone_pairs(1.0), stage.fade(base[0], 0.0), FadeIn(tilt), *stage.turn(yaw=0.45, pitch=LONE_PAIR_VIEW_PITCH),
               run_time=1.4)
    scene.play(stage.fade(apex_arc, 1.0), run_time=1.0)

    # --- 6. A second lone pair: where? -----------------------------------------------------------------------------------------
    beat(scene, t, 5)
    xef4 = ml.molecule("XeF4")
    second = sorted(xef4.lone_pair_indices() - brf5.lone_pair_indices())[0]
    cis = [j for j in pm.neighbours_at_90(6, first) if j != second][0]
    trial_dir = [model.dirs[cis].copy()]
    trial = region_lobe(ORIGIN, lambda: trial_dir[0], "E")
    trial.presence = 0.0
    stage.add_body(trial)
    where = caption("A second lone pair: where?", cfg.PURPLE)
    scene.play(stage.fade(apex_arc, 0.0), fade_through(tilt, where), FadeOut(shape),
               *stage.turn(yaw=0.45, pitch=LONE_PAIR_VIEW_PITCH),
               run_time=1.2)
    scene.remove(tilt)

    # --- 7. Next to the first: 90 degrees --------------------------------------------------------------------------------------
    beat(scene, t, 6)
    near = AngleArc(ORIGIN, lambda: trial_dir[0], model._dir(first), 1.5, cfg.RED, width=7,
                    label=degrees_label(90, cfg.FONT["body"], cfg.RED), label_gap=0.5)
    near.presence = 0.0
    stage.add_overlay(near)
    scene.play(*model.fade("atoms", 0.15, [cis]), *model.fade("rods", 0.0, [cis]), stage.fade(trial, 1.0), run_time=1.0)
    scene.play(stage.fade(near, 1.0), run_time=1.0)
    no = cross_mark(0.35).move_to([PANEL_X, -0.4, 0])
    scene.play(Create(no), run_time=0.8)

    # --- 8. Opposite: 180 degrees, as far as possible --------------------------------------------------------------------------
    beat(scene, t, 7)
    assert frozenset({first, second}) in pm.best_lone_pair_sites(6, 2)

    def move_trial(direction, **kwargs) -> Param:
        def setter(v):
            trial_dir[0] = mu.unit(v)
        return stage.tween(lambda: trial_dir[0], setter, mu.unit(direction), mode="direction", **kwargs)

    far = AngleArc(ORIGIN, lambda: trial_dir[0], model._dir(first), 1.5, cfg.GREEN, width=7,
                   label=degrees_label(180, cfg.FONT["body"], cfg.GREEN), label_gap=0.55)
    far.presence = 0.0
    stage.add_overlay(far)
    yes = check_mark(0.4).move_to(no)
    scene.play(stage.fade(near, 0.0), FadeOut(no), *model.fade("atoms", 1.0, [cis]), *model.fade("rods", 1.0, [cis]),
               *model.fade("atoms", 0.15, [second]), *model.fade("rods", 0.0, [second]), move_trial(model.dirs[second]),
               *stage.turn(yaw=0.2, pitch=-0.12), run_time=2.0)
    scene.play(stage.fade(far, 1.0), Create(yes), run_time=1.0)

    # --- 9. Xenon tetrafluoride: AX4E2 -------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    new = panel_for("XeF4")
    scene.play(stage.fade(far, 0.0), stage.fade(trial, 0.0), FadeOut(yes), FadeOut(where), *model.become(xef4),
               fade_through(panel, new), *stage.turn(yaw=0.45, pitch=0.3), run_time=1.8)
    scene.remove(panel)
    panel = new

    # --- 10. Hide them -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(*model.show_lone_pairs(0.0), *model.fade("guides", 0.0), run_time=1.4)

    # --- 11. Completely flat: square planar ------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    square = faces(stage, [model._site_point(i) for i in (2, 4, 3, 5)], ((0, 1, 2, 3),), cfg.GREEN, 0.14, 0.7)
    shape = shape_name(xef4.shape, size=cfg.FONT["section"]).move_to([PANEL_X, -0.3, 0])
    scene.play(stage.fade(square[0], 1.0), *stage.turn(pitch=1.05), run_time=1.8)
    scene.play(FadeIn(shape, shift=UP * 0.1), run_time=0.8)
    scene.play(*stage.turn(pitch=0.0), run_time=2.0, rate_func=smooth)

    # --- 12. How can six regions look flat? -----------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    how = caption("Six regions… and flat?", cfg.GOLD)
    scene.play(FadeIn(how), *stage.turn(pitch=0.35), run_time=1.4)

    # --- 13. Two lone pairs, above and below ---------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    answer = caption("Two lone pairs: one above, one below", cfg.PURPLE)
    scene.play(*model.show_lone_pairs(1.0), fade_through(how, answer), run_time=1.4)
    scene.remove(how)
    scene.play(stage.set_spin(0.35), run_time=1.6)

    # --- 14. The three octahedral shapes -------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    hide(scene, stage, 0.8, FadeOut(VGroup(panel, shape, answer)))
    keys = ("SF6", "BrF5", "XeF4")
    family = []
    for k, key in enumerate(keys):
        small, _ = mini_model(key, [(k - 1) * 4.6, 0.75, 0], zoom=0.72, lone_pairs=0.65, spin=0.3,
                              pitch=LONE_PAIR_VIEW_PITCH if key == "BrF5" else 0.3)
        family.append(small)
        scene.add(small)
    tags = VGroup(*[VGroup(formula(key, cfg.FONT["body"]), shape_name(ml.molecule(key).shape, size=cfg.FONT["body"]))
                    .arrange(DOWN, buff=0.2).move_to([(k - 1) * 4.6, -2.4, 0]) for k, key in enumerate(keys)])
    scene.play(*[s.fade(s, 1.0) for s in family], LaggedStart(*[FadeIn(tag, shift=UP * 0.1) for tag in tags],
                                                                lag_ratio=0.3), run_time=2.0)
    done = top_caption("All the main VSEPR families: 2 to 6 regions", cfg.GREEN)
    scene.play(FadeIn(done), run_time=1.0)
    scene.play(LaggedStart(*[Indicate(tag[1], color=cfg.WHITE, scale_factor=1.05) for tag in tags], lag_ratio=0.3),
               run_time=2.0)
    scene.play(*[s.turn(pitch=-0.55 if key == "BrF5" else 0.55)[0] for key, s in zip(keys, family)], run_time=1.6, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
