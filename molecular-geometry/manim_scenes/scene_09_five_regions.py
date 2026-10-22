"""Chapter 09 — five regions: the trigonal bipyramid, and PCl5.

The tetrahedron gains a fifth region underneath and the repulsion model
relaxes it into the trigonal bipyramid (``physics_models.settle``). Axial
and equatorial positions are named, the three different angles are drawn,
and phosphorus pentachloride is shown with its measured axial and
equatorial bond lengths (axial longer), drawn to scale.
"""

from manim_scenes.common import *

CENTER = np.array([-1.4, -0.3, 0])
PANEL_X = 4.6


class Scene09FiveRegions(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "09", "Five electron regions")

    # --- 1. Five points cannot all be equally spaced -------------------------------------------------------
    stage = Stage(CENTER, zoom=1.0, yaw=0.45, pitch=0.3, sway=0.12)
    regions = RegionModel(stage, pm.ideal_directions(4))
    show(scene, stage, 1.0)
    dismiss_opening_title(scene, t, head)
    unequal = caption("Five can't all be equally spaced", cfg.WHITE)
    scene.play(FadeIn(unequal), stage.set_spin(0.3), run_time=1.2)

    # --- 2. Add a fifth underneath and let them settle --------------------------------------------------------
    beat(scene, t, 1)
    newcomer = regions.add_region(DOWN)
    scene.play(regions.grow(newcomer), stage.set_spin(0.0), *stage.turn(yaw=0.45), FadeOut(unequal), run_time=1.4)
    scene.play(regions.play_path(pm.settle(regions.dirs)), run_time=3.6, rate_func=smooth)
    axial = [i for i, d in enumerate(regions.dirs) if abs(d[1]) > 0.99]
    equatorial = [i for i in range(5) if i not in axial]

    # --- 3. Three around the middle: equatorial --------------------------------------------------------------------
    beat(scene, t, 2)
    eq_face = faces(stage, [regions.tip(i, 1.0) for i in equatorial], ((0, 1, 2),), cfg.GOLD, 0.12, 0.7)
    eq_tag = Tag(txt("equatorial", cfg.FONT["body"], cfg.GOLD), regions.tip(equatorial[1], 1.05), RIGHT * 1.6 + DOWN * 0.1)
    eq_tag.presence = 0.0
    stage.add_overlay(eq_tag)
    scene.play(*[stage.fade(f, 1.0) for f in eq_face], stage.fade(eq_tag, 1.0), run_time=1.4)

    # --- 4. Above and below: axial -------------------------------------------------------------------------------------
    beat(scene, t, 3)
    ax_tags = [Tag(txt("axial", cfg.FONT["body"], cfg.CYAN), regions.tip(i, 1.0), RIGHT * 1.2) for i in axial]
    for tag in ax_tags:
        tag.presence = 0.0
        stage.add_overlay(tag)
    scene.play(*[stage.fade(tag, 1.0) for tag in ax_tags], run_time=1.2)

    # --- 5. A trigonal bipyramid ----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    corners = [regions.tip(i, 1.0) for i in axial + equatorial]
    shell = faces(stage, corners, [(a, 2 + b, 2 + (b + 1) % 3) for a in (0, 1) for b in range(3)])
    tbp = shape_name("trigonal bipyramidal", cfg.CYAN, cfg.FONT["body"]).move_to([0, -3.65, 0])
    scene.play(*[stage.fade(f, 1.0) for f in shell], stage.fade(eq_face[0], 0.4), FadeIn(tbp), run_time=1.4)
    scene.play(stage.set_spin(0.35), run_time=1.6)

    # --- 6-8. Three different angles -------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(stage.set_spin(0.0), *[stage.fade(f, 0.0) for f in shell], stage.fade(eq_face[0], 0.0),
               stage.fade(eq_tag, 0.0), *[stage.fade(tag, 0.0) for tag in ax_tags], *stage.turn(yaw=0.25, pitch=0.35),
               FadeOut(tbp),
               run_time=1.6)
    pairs = ((equatorial[0], equatorial[1]), (axial[0], equatorial[1]), (axial[0], axial[1]))
    angle_rows = VGroup()
    for k, ((i, j), words) in enumerate(zip(pairs, ("equatorial–equatorial", "axial–equatorial", "axial–axial"))):
        beat(scene, t, 6 + k)
        value = mu.angle_deg(regions.dirs[i], regions.dirs[j])
        arc = regions.arc(i, j, radius=1.05, label=degrees_label(value, cfg.FONT["body"]), label_gap=0.55)
        row = VGroup(txt(words, cfg.FONT["label"], cfg.WHITE), degrees_label(value, cfg.FONT["body"]))
        row.arrange(RIGHT, buff=0.35)
        angle_rows.add(row)
        angle_rows.arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to([PANEL_X - 0.3, 1.4, 0])
        scene.play(stage.fade(arc, 1.0), FadeIn(row, shift=LEFT * 0.2), run_time=1.0)
        scene.play(stage.fade(arc, 0.0), run_time=1.6, rate_func=lambda a: 0.0 if a < 0.6 else (a - 0.6) / 0.4)

    # --- 9. The positions differ -------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    differ = caption("Two kinds of position", cfg.GOLD)
    scene.play(FadeIn(differ), Indicate(angle_rows[1], color=cfg.RED, scale_factor=1.05), run_time=1.4)

    # --- 10. Phosphorus pentachloride (gas phase): AX5 ----------------------------------------------------------------------
    beat(scene, t, 10)
    pcl5 = ml.molecule("PCl5")
    hide(scene, stage, 0.8, FadeOut(VGroup(angle_rows, differ)))
    stage = Stage(CENTER, zoom=0.95, yaw=0.3, pitch=0.25, sway=0.12)
    model = MoleculeModel(stage, pcl5, true_lengths=True, bond=2.55)
    title = VGroup(formula("PCl5", cfg.FONT["section"]), txt("gas phase", cfg.FONT["label"], cfg.MUTED)).arrange(DOWN, buff=0.2)
    title.move_to([PANEL_X, 2.4, 0])
    code = axe_eq(5, 0, cfg.FONT["section"]).move_to([PANEL_X, 0.9, 0])
    shape = shape_name(pcl5.shape, size=cfg.FONT["label"]).move_to([PANEL_X, 0.0, 0])
    show(scene, stage, 1.2, FadeIn(title))
    scene.play(FadeIn(code), FadeIn(shape, shift=UP * 0.1), stage.set_spin(0.3), run_time=1.2)

    # --- 11. Axial bonds are longer ------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    ax_len, eq_len = gd.BOND_LENGTH_PM["P-Cl axial in PCl5"], gd.BOND_LENGTH_PM["P-Cl equatorial in PCl5"]
    lengths = VGroup(VGroup(txt("axial", cfg.FONT["label"], cfg.CYAN), txt(f"{ax_len} pm", cfg.FONT["body"], cfg.WHITE)),
                     VGroup(txt("equatorial", cfg.FONT["label"], cfg.GOLD), txt(f"{eq_len} pm", cfg.FONT["body"], cfg.WHITE)))
    for row in lengths:
        row.arrange(RIGHT, buff=0.35)
    lengths.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, -1.5, 0])
    glows = [Halo(model.atoms[i], cfg.CYAN, reach=2.4, peak=0.25) for i in pm.AXIAL]
    for g in glows:
        g.presence = 0.0
    stage.add_body(*glows)
    scene.play(stage.set_spin(0.0), *stage.turn(yaw=0.0, pitch=0.12), *[stage.fade(g, 1.0) for g in glows],
               FadeIn(lengths[0]), run_time=1.6)
    scene.play(FadeIn(lengths[1]), run_time=1.0)

    # --- 12. Where do lone pairs go? ----------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    where = caption("When lone pairs appear, where do they go?", cfg.PURPLE)
    scene.play(*[stage.fade(g, 0.0) for g in glows], FadeIn(where), stage.set_spin(0.3), run_time=1.4)
    scene.play(Indicate(where, color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    scene.play(*stage.turn(pitch=0.5), run_time=2.4, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
