"""Valence bond theory, part 1: overlap and the sigma bond (3D).

Every orbital surface is an isosurface computed in ``utils.bond_models``:
the two-electron density of a simple LCAO combination of hydrogen-like
functions, normalised by its overlap. Far apart it approximates two atomic
densities; as the separation shrinks the same surface merges into one shared
cloud — so the morph illustrates overlap instead of using a crossfade. Rotating
the finished bond about its axis leaves it unchanged: the defining symmetry
of a sigma bond. The p-orbital version (head-on, as in Cl2) uses the same
machinery with p functions whose facing lobes share a sign.
"""

from manim_scenes.common import *

FAR_S = 9.0
NEAR_S = 3.2
FAR_P = 11.0


class Scene08SigmaOverlap(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def nuclei_for(surface: Isosurface, scale: float) -> VGroup:
    """Two small nuclei that sit at +/- separation/2 of a morphing surface."""
    pair = VGroup(nucleus_3d([-1, 0, 0], 0.12), nucleus_3d([1, 0, 0], 0.12))

    def place(m: Mobject) -> None:
        half = surface.value / 2 * scale
        m[0].move_to([-half, 0, 0])
        m[1].move_to([half, 0, 0])

    pair.add_updater(place)
    place(pair)
    return pair


def axis_ring(x: float, radius: float = 1.25, color: str = cfg.GOLD) -> VMobject:
    """A circular arrow around the bond (x) axis."""
    arc = Arc(radius=radius, start_angle=0.2, angle=TAU * 0.8, stroke_color=color, stroke_width=6)
    arc.add_tip(tip_length=0.28)
    arc.rotate(PI / 2, axis=UP, about_point=ORIGIN).shift(RIGHT * x)
    return arc


def spin(up: bool) -> Arrow:
    start, end = (DOWN * 0.42, UP * 0.42) if up else (UP * 0.42, DOWN * 0.42)
    return Arrow(start, end, buff=0, color=cfg.SPIN_UP if up else cfg.SPIN_DOWN, stroke_width=10,
                 max_tip_length_to_length_ratio=0.35)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "08", "Valence bond theory")
    scene.set_camera_orientation(phi=68 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

    # --- 1. Each atom brings one orbital with one unpaired electron --------------------------------------
    s_bond = Isosurface(sigma_s_grid, FAR_S, cfg.SIGMA_COLOR, 0.6, colorer=orbital_shade(cfg.SIGMA_COLOR))
    s_nuclei = nuclei_for(s_bond, ORB_SCALE)
    scene.play(FadeIn(s_bond), FadeIn(s_nuclei), run_time=1.6)
    spins = VGroup(spin(True).move_to([-3.6, 2.15, 0]), spin(False).move_to([3.6, 2.15, 0]))
    hud(scene, spins)
    one_each = caption("One electron each", cfg.WHITE, cfg.FONT["label"], y=-3.55)
    hud(scene, one_each)
    scene.play(GrowArrow(spins[0]), GrowArrow(spins[1]), FadeIn(one_each), run_time=1.0)
    dismiss_opening_title(scene, t, head)

    # --- 2. Overlap, then pairing with opposite spins ----------------------------------------------------------
    beat(scene, t, 1)
    recipe = VGroup(chip("overlap", cfg.SIGMA_COLOR, cfg.FONT["label"]), eq("+", cfg.FONT["label"], cfg.MUTED),
                    chip("pairing", cfg.SPIN_DOWN, cfg.FONT["label"]), eq(r"\rightarrow", cfg.FONT["label"], cfg.MUTED),
                    chip("lower energy", cfg.GOLD, cfg.FONT["label"])).arrange(RIGHT, buff=0.25).move_to([0, 3.25, 0])
    hud(scene, recipe)
    scene.play(FadeOut(one_each), LaggedStart(*[FadeIn(part, shift=DOWN * 0.1) for part in recipe], lag_ratio=0.25),
               run_time=1.8)
    scene.play(Indicate(recipe[0], color=cfg.WHITE), run_time=0.9)
    scene.play(Indicate(recipe[2], color=cfg.WHITE), run_time=0.9)

    # --- 3. Two hydrogen 1s orbitals -----------------------------------------------------------------------------
    beat(scene, t, 2)
    hydrogen = caption("1s + 1s", cfg.CYAN, cfg.FONT["label"], y=-3.55)
    hud(scene, hydrogen)
    scene.play(FadeIn(hydrogen), run_time=0.8)
    move_camera(scene, phi=62 * DEGREES, theta=-78 * DEGREES, zoom=1.0, run_time=2.4)

    # --- 4. Bring them together: overlap ---------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(s_bond.morph_to(NEAR_S), FadeOut(spins), run_time=3.2, rate_func=smooth)
    overlap = caption("Density between nuclei", cfg.SIGMA_COLOR, cfg.FONT["label"], y=-3.55)
    hud(scene, overlap)
    scene.play(*fade_labels(hydrogen, overlap), run_time=0.8)

    # --- 5. One shared cloud along the axis ---------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(s_bond.morph_to(bm.S_BOND), run_time=3.0, rate_func=smooth)
    paired = VGroup(spin(True), spin(False)).arrange(RIGHT, buff=0.25).move_to([4.9, 1.6, 0])
    hud(scene, paired)
    scene.play(GrowArrow(paired[0]), GrowArrow(paired[1]), run_time=0.8)
    axis = DashedLine([-4.2, 0, 0], [4.2, 0, 0], stroke_color=cfg.WHITE, stroke_width=3, dash_length=0.14)
    scene.play(Create(axis), run_time=0.9)

    # --- 6. Turn it about the axis: unchanged ---------------------------------------------------------------------------
    beat(scene, t, 5)
    ring = axis_ring(-2.6)
    same = caption("Unchanged around the bond axis", cfg.WHITE, cfg.FONT["label"], y=-3.55)
    hud(scene, same)
    scene.play(*fade_labels(overlap, same), Create(ring), run_time=0.9)
    s_nuclei.clear_updaters()
    scene.play(Rotate(VGroup(s_bond, s_nuclei), angle=TAU, axis=RIGHT, about_point=ORIGIN),
               Rotate(ring, angle=TAU, axis=RIGHT, about_point=ORIGIN), run_time=5.0, rate_func=smooth)

    # --- 7. A sigma bond -------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    sigma = VGroup(eq(r"\sigma", 120, cfg.SIGMA_COLOR), txt("sigma bond", cfg.FONT["body"], cfg.SIGMA_COLOR)).arrange(RIGHT, buff=0.35)
    sigma.move_to([0, 2.4, 0])
    head_on = caption("Head-on · density on the axis", cfg.WHITE, cfg.FONT["label"], y=-3.55)
    hud(scene, sigma, head_on)
    scene.play(*fade_labels(same, head_on), FadeOut(ring), FadeOut(recipe), FadeIn(sigma, scale=0.8), run_time=1.0)
    move_camera(scene, phi=70 * DEGREES, theta=-96 * DEGREES, zoom=1.08, run_time=3.0)
    scene.play(Indicate(sigma, color=cfg.WHITE, scale_factor=1.06), run_time=1.0)

    # --- 8. p orbitals: two lobes -----------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(s_bond, s_nuclei, axis)), FadeOut(sigma), FadeOut(head_on), FadeOut(paired), run_time=0.9)
    move_camera(scene, phi=66 * DEGREES, theta=-62 * DEGREES, zoom=1.0, run_time=1.0)
    px = GridSurface(single_p_grid(), cfg.CYAN, 0.68, colorer=orbital_shade(cfg.CYAN)).scale(1.55, about_point=ORIGIN)
    core = nucleus_3d(ORIGIN, 0.15)
    scene.play(FadeIn(px), FadeIn(core), run_time=1.2)
    lobes = caption("One p orbital · two lobes", cfg.CYAN, cfg.FONT["label"], y=-3.55)
    hud(scene, lobes)
    scene.play(FadeIn(lobes), run_time=0.8)
    scene.play(Rotate(px, angle=PI / 5, axis=OUT, about_point=ORIGIN), run_time=1.6, rate_func=there_and_back)

    # --- 9. Three of them, at right angles ------------------------------------------------------------------------------------
    beat(scene, t, 8)
    py = GridSurface(single_p_grid(), "#5FA8FF", 0.68, colorer=orbital_shade("#5FA8FF")).scale(1.55, about_point=ORIGIN).rotate(PI / 2, axis=OUT, about_point=ORIGIN)
    pz = GridSurface(single_p_grid(), cfg.TEAL, 0.68, colorer=orbital_shade(cfg.TEAL)).scale(1.55, about_point=ORIGIN).rotate(PI / 2, axis=UP, about_point=ORIGIN)
    labels = VGroup(txt("x", cfg.FONT["body"], cfg.CYAN).move_to([3.45, 0, 0]),
                    txt("y", cfg.FONT["body"], "#5FA8FF").move_to([0, 3.45, 0]),
                    txt("z", cfg.FONT["body"], cfg.TEAL).move_to([0, 0, 3.4]))
    for label in labels:
        scene.add_fixed_orientation_mobjects(label)
    scene.play(FadeIn(py), FadeIn(labels[0]), FadeIn(labels[1]), run_time=1.0)
    scene.play(FadeIn(pz), FadeIn(labels[2]), run_time=1.0)
    right_angles = caption("Three perpendicular p orbitals", cfg.WHITE, cfg.FONT["label"], y=-3.55)
    hud(scene, right_angles)
    scene.play(*fade_labels(lobes, right_angles), run_time=0.7)
    scene.begin_ambient_camera_rotation(rate=0.12)

    # --- 10. Chlorine: two 3p orbitals, end to end --------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.stop_ambient_camera_rotation()
    scene.play(FadeOut(VGroup(px, py, pz, core, labels)), FadeOut(right_angles), run_time=0.9)
    move_camera(scene, phi=64 * DEGREES, theta=-82 * DEGREES, zoom=1.0, run_time=1.2)
    p_bond = Isosurface(sigma_p_grid, FAR_P, cfg.SIGMA_COLOR, 0.6, colorer=orbital_shade(cfg.SIGMA_COLOR))
    p_nuclei = nuclei_for(p_bond, P_SCALE)
    chlorine = VGroup(eq(r"\mathrm{Cl_2}", cfg.FONT["body"], cfg.GREEN), txt("3p + 3p, end to end", cfg.FONT["label"], cfg.WHITE)).arrange(RIGHT, buff=0.4)
    chlorine.move_to([0, -3.55, 0])
    hud(scene, chlorine)
    scene.play(FadeIn(p_bond), FadeIn(p_nuclei), FadeIn(chlorine), run_time=1.4)
    p_axis = DashedLine([-5.6, 0, 0], [5.6, 0, 0], stroke_color=cfg.WHITE, stroke_width=3, dash_length=0.14)
    scene.play(Create(p_axis), run_time=0.8)

    # --- 11. Head-on: the facing lobes overlap --------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(p_bond.morph_to(bm.P_BOND), run_time=3.4, rate_func=smooth)
    on_axis = caption("Head-on overlap", cfg.SIGMA_COLOR, cfg.FONT["label"], y=-3.55)
    hud(scene, on_axis)
    scene.play(*fade_labels(chlorine, on_axis), run_time=0.8)
    glow = Sphere(radius=0.42, resolution=(10, 6)).set_fill(cfg.WHITE, 0.25).set_stroke(width=0)
    scene.play(FadeIn(glow, scale=0.5), run_time=0.6)
    scene.play(FadeOut(glow, scale=1.6), run_time=0.8)

    # --- 12. Same symmetry: sigma again ------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    ring = axis_ring(-3.6, 1.35)
    again = VGroup(eq(r"\sigma", 110, cfg.SIGMA_COLOR), txt("again", cfg.FONT["body"], cfg.SIGMA_COLOR)).arrange(RIGHT, buff=0.3)
    again.move_to([0, 2.5, 0])
    hud(scene, again)
    scene.play(FadeOut(on_axis), Create(ring), run_time=0.8)
    p_nuclei.clear_updaters()
    scene.play(Rotate(VGroup(p_bond, p_nuclei), angle=TAU, axis=RIGHT, about_point=ORIGIN),
               Rotate(ring, angle=TAU, axis=RIGHT, about_point=ORIGIN), run_time=4.6, rate_func=smooth)
    scene.play(FadeIn(again, scale=0.8), run_time=0.8)

    # --- 13. Head-on gives sigma; but side by side? ------------------------------------------------------------------------------------
    beat(scene, t, 12)
    rule = VGroup(txt("head-on overlap", cfg.FONT["body"], cfg.WHITE), eq(r"\rightarrow", cfg.FONT["body"]),
                  eq(r"\sigma", 90, cfg.SIGMA_COLOR)).arrange(RIGHT, buff=0.3).move_to([0, -3.45, 0])
    hud(scene, rule)
    scene.play(FadeOut(ring), FadeIn(rule, shift=UP * 0.1), run_time=0.9)
    move_camera(scene, phi=72 * DEGREES, theta=-100 * DEGREES, zoom=1.0, run_time=3.0)
    scene.play(Indicate(rule, color=cfg.GOLD, scale_factor=1.05), run_time=1.0)

    # --- 14. Two p orbitals side by side ---------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(FadeOut(VGroup(p_bond, p_nuclei, p_axis)), FadeOut(again), FadeOut(rule), run_time=0.9)
    upper = GridSurface(pi_grid(FAR_P, True), cfg.PI_COLOR, 0.72, colorer=orbital_shade(cfg.PI_COLOR))
    lower = GridSurface(pi_grid(FAR_P, False), cfg.PI_COLOR, 0.72, colorer=orbital_shade(cfg.PI_COLOR))
    side_nuclei = VGroup(nucleus_3d([-FAR_P / 2 * P_SCALE, 0, 0], 0.12), nucleus_3d([FAR_P / 2 * P_SCALE, 0, 0], 0.12))
    scene.play(FadeIn(upper), FadeIn(lower), FadeIn(side_nuclei), run_time=1.4)
    side = caption("side by side?", cfg.PI_COLOR, cfg.FONT["body"], y=-3.5)
    hud(scene, side)
    scene.play(FadeIn(side), run_time=0.8)
    move_camera(scene, phi=66 * DEGREES, theta=-74 * DEGREES, zoom=1.0, run_time=3.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
