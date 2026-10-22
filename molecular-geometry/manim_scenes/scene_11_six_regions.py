"""Chapter 11 — six regions: the octahedron, and SF6.

The bipyramid gains a sixth region on its equator and the repulsion model
relaxes it into the octahedron. Its eight faces are drawn between the
region tips; sulfur hexafluoride is turned about two axes to show that
every direction is equivalent.
"""

from manim_scenes.common import *

CENTER = np.array([-1.6, -0.3, 0])
PANEL_X = 4.7


class Scene11SixRegions(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "Six electron regions")

    # --- 1. Add a sixth region and let them settle ---------------------------------------------------------------
    stage = Stage(CENTER, zoom=1.0, yaw=0.45, pitch=0.3, sway=0.1)
    regions = RegionModel(stage, pm.ideal_directions(5))
    show(scene, stage, 1.0)
    dismiss_opening_title(scene, t, head, at=2.6)
    newcomer = regions.add_region(OUT)
    scene.play(regions.grow(newcomer), run_time=1.0)

    # --- 2. Everything evens out --------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(regions.play_path(pm.settle(regions.dirs)), run_time=3.4, rate_func=smooth)
    evens = caption("A square round the middle, one above, one below", cfg.CYAN)
    scene.play(FadeIn(evens), stage.set_spin(0.3), run_time=1.0)

    # --- 3. 90 to four neighbours, 180 to the last ------------------------------------------------------------------------
    beat(scene, t, 2)
    up = int(np.argmax([d[1] for d in regions.dirs]))
    down = int(np.argmin([d[1] for d in regions.dirs]))
    side = int(np.argmax([d[0] for d in regions.dirs]))
    right_angle = regions.arc(up, side, radius=1.1, label=degrees_label(90, cfg.FONT["body"]), label_gap=0.55)
    straight = regions.arc(up, down, radius=1.25, label=degrees_label(180, cfg.FONT["body"]), label_gap=0.6)
    scene.play(stage.set_spin(0.0), *stage.turn(yaw=0.3, pitch=0.2), FadeOut(evens), run_time=1.0)
    scene.play(stage.fade(right_angle, 1.0), run_time=1.0)
    scene.play(stage.fade(straight, 1.0), run_time=1.0)

    # --- 4. Eight faces: an octahedron ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    pos = {name: int(np.argmax([np.dot(d, axis) for d in regions.dirs]))
           for name, axis in (("+y", UP), ("-y", DOWN), ("+x", RIGHT), ("-x", LEFT), ("+z", OUT), ("-z", IN))}
    tips = [regions.tip(i, 1.0) for i in range(6)]
    octa = faces(stage, tips, [(pos[a], pos[b], pos[c]) for a in ("+y", "-y") for b in ("+x", "-x") for c in ("+z", "-z")],
                 cfg.CYAN, 0.1, 0.5)
    octa_name = shape_name("octahedral", cfg.CYAN, cfg.FONT["section"]).move_to([PANEL_X, 0.0, 0])
    scene.play(stage.fade(right_angle, 0.0), stage.fade(straight, 0.0), *[stage.fade(f, 1.0) for f in octa],
               FadeIn(octa_name), stage.set_spin(0.35), run_time=1.6)

    # --- 5. Sulfur hexafluoride: AX6 ---------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    sf6 = ml.molecule("SF6")
    hide(scene, stage, 0.8, FadeOut(octa_name))
    stage = Stage(CENTER, zoom=1.0, yaw=0.45, pitch=0.3, sway=0.08)
    model = MoleculeModel(stage, sf6)
    panel = VGroup(formula("SF6", cfg.FONT["section"]), axe_eq(6, 0, cfg.FONT["section"]),
                   shape_name(sf6.shape, size=cfg.FONT["section"])).arrange(DOWN, buff=0.4).move_to([PANEL_X, 0.9, 0])
    show(scene, stage, 1.0, FadeIn(panel[:2]))
    scene.play(FadeIn(panel[2], shift=UP * 0.1), run_time=0.9)

    # --- 6. Every position equivalent -------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    same = caption("The same view along every axis", cfg.WHITE)
    scene.play(FadeIn(same), stage.rock(RIGHT, np.pi / 2), run_time=2.4, rate_func=smooth)
    scene.play(stage.rock(UP, np.pi / 2), run_time=2.4, rate_func=smooth)

    # --- 7. Beyond the octet, no problem for counting ---------------------------------------------------------------------------------------
    beat(scene, t, 6)
    octet = VGroup(chip("Lewis count: 12 electrons", cfg.ORANGE, cfg.FONT["small"]),
                   chip("6 regions → 6 directions", cfg.CYAN, cfg.FONT["small"])).arrange(DOWN, buff=0.3)
    octet.move_to([PANEL_X - 0.2, -2.0, 0])
    scene.play(FadeOut(same), FadeIn(octet[0], shift=UP * 0.1), run_time=1.0)
    scene.play(FadeIn(octet[1], shift=UP * 0.1), stage.set_spin(0.3), run_time=1.0)

    # --- 8. Lone pairs in an octahedron? -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    question = caption("What happens when lone pairs move in?", cfg.PURPLE)
    lone = region_lobe(ORIGIN, model._dir(1), "E")
    lone.presence = 0.0
    stage.add_body(lone)
    scene.play(FadeIn(question), FadeOut(octet), stage.fade(lone, 0.6), run_time=1.4)
    scene.play(stage.fade(lone, 0.15), run_time=2.0, rate_func=there_and_back)
    scene.play(Indicate(question, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
