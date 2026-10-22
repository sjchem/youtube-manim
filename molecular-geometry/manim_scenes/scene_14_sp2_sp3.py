"""Chapter 14 — sp2 and sp3, and why the angles come out by themselves.

Three (then four) copies of carbon's s orbital are mixed toward the sp2
(sp3) mixing angle along the directions in ``orbital_models.hybrid_directions``
while the p orbitals they use fade away; the unused p stays, in purple.
The closing argument is the orthogonality condition: equivalent hybrids
s + sqrt(n) p_i have zero overlap only if cos(theta) = -1/n, evaluated by
``orbital_models.equivalent_hybrid_cosine`` for n = 1, 2, 3.
"""

from manim_scenes.common import *

ORB_AT = np.array([-2.0, -0.3, 0])
PANEL_X = 4.4
UNITS = 0.62


class Scene14Sp2Sp3(Scene):
    def construct(self) -> None:
        play_scene(self)


def hybrid_set(stage: Stage, kind: str, central: str = "C") -> tuple[list[Orbital], list[Orbital]]:
    """Spheres (pure s) along each hybrid direction, plus the p orbitals to be used up."""
    hybrids = [Orbital(stage, ORIGIN, d, 0.0, units=UNITS, opacity=0.62) for d in om.hybrid_directions(kind)]
    used = [axis for axis in (RIGHT, UP, OUT)
            if not any(np.allclose(axis, p) for p in om.leftover_p(kind))]
    p_used = [Orbital(stage, ORIGIN, axis, np.pi / 2, units=UNITS * 0.8, opacity=0.6) for axis in used]
    stage.add_body(element_ball(central, ORIGIN, scale=0.35, label=False))
    return hybrids, p_used


def tip(direction, alpha: float, stretch: float = 0.92) -> np.ndarray:
    return mu.unit(direction) * om.polar_reach(alpha) * UNITS * stretch


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "sp² and sp³")

    # --- 1. s + 2p -> three sp2 hybrids -----------------------------------------------------------------------------
    stage = Stage(ORB_AT, zoom=1.0, yaw=0.0, pitch=0.15, sway=0.1)
    hybrids, p_used = hybrid_set(stage, "sp2", central="B")
    recipe = eq(r"s + 2p \;\rightarrow\; 3\,sp^2", cfg.FONT["section"], cfg.BLUE).move_to([PANEL_X, 2.4, 0])
    show(scene, stage, 1.0, FadeIn(recipe))
    dismiss_opening_title(scene, t, head, at=2.0)
    alpha2 = om.SP_ALPHA["sp2"]
    scene.play(*[h.mix_to(alpha2) for h in hybrids], *[a for p in p_used for a in p.fade(0.0)], run_time=3.0,
               rate_func=smooth)

    # --- 2. One plane, 120 degrees apart ---------------------------------------------------------------------------
    beat(scene, t, 1)
    d2 = om.hybrid_directions("sp2")
    arc = AngleArc(ORIGIN, d2[1], d2[2], 1.0, label=degrees_label(mu.angle_deg(d2[1], d2[2]), cfg.FONT["body"]),
                   label_gap=0.5)
    arc.presence = 0.0
    stage.add_overlay(arc)
    same = caption("The same directions VSEPR gives three regions", cfg.CYAN)
    scene.play(stage.fade(arc, 1.0), FadeIn(same), run_time=1.2)

    # --- 3. One p orbital left over, upright ------------------------------------------------------------------------
    beat(scene, t, 2)
    p_left = p_orbital(stage, ORIGIN, om.leftover_p("sp2")[0], units=UNITS * 0.85, opacity=0.8)
    p_left.set_presence(0.0)
    left_tag = txt("unused p", cfg.FONT["body"], cfg.PURPLE).move_to([PANEL_X, 0.8, 0])
    scene.play(stage.fade(arc, 0.0), *p_left.fade(1.0), *stage.turn(yaw=0.4, pitch=0.55), FadeOut(same),
               FadeIn(left_tag), run_time=1.8)

    # --- 4. Boron trifluoride: three hybrids, three fluorines ------------------------------------------------------------
    beat(scene, t, 3)
    fluorines = [element_ball("F", tip(d, alpha2, 1.0), scale=0.85) for d in d2]
    for f in fluorines:
        f.presence = 0.0
    stage.add_body(*fluorines)
    bf3 = formula("BF3", cfg.FONT["section"]).move_to([PANEL_X, -0.4, 0])
    scene.play(*[stage.fade(f, 1.0) for f in fluorines], FadeIn(bf3), *stage.turn(yaw=0.2, pitch=0.35), run_time=1.6)
    scene.play(stage.set_spin(0.3), run_time=1.2)

    # --- 5. s + 3p -> four sp3 hybrids -----------------------------------------------------------------------------------
    beat(scene, t, 4)
    hide(scene, stage, 0.7, FadeOut(VGroup(recipe, left_tag, bf3)))
    stage = Stage(ORB_AT, zoom=1.0, yaw=0.45, pitch=0.3, sway=0.1)
    hybrids, p_used = hybrid_set(stage, "sp3")
    recipe = eq(r"s + 3p \;\rightarrow\; 4\,sp^3", cfg.FONT["section"], cfg.BLUE).move_to([PANEL_X, 2.4, 0])
    show(scene, stage, 0.8, FadeIn(recipe))
    alpha3 = om.SP_ALPHA["sp3"]
    scene.play(*[h.mix_to(alpha3) for h in hybrids], *[a for p in p_used for a in p.fade(0.0)], run_time=2.8,
               rate_func=smooth)

    # --- 6. A tetrahedron; nothing left over ---------------------------------------------------------------------------------
    beat(scene, t, 5)
    d3 = om.hybrid_directions("sp3")
    tips = [lambda d=d: tip(d, alpha3, 1.0) for d in d3]
    tetra = faces(stage, tips, ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)), cfg.GOLD, 0.06, 0.6)
    none_left = txt("no p left over", cfg.FONT["body"], cfg.WHITE).move_to([PANEL_X, 0.8, 0])
    scene.play(*[stage.fade(f, 1.0) for f in tetra], FadeIn(none_left), stage.set_spin(0.3), run_time=1.4)

    # --- 7. Methane lines up with them ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    hydrogens = [element_ball("H", tip(d, alpha3, 1.02)) for d in d3]
    for h in hydrogens:
        h.presence = 0.0
    stage.add_body(*hydrogens)
    ch4 = formula("CH4", cfg.FONT["section"]).move_to([PANEL_X, -0.4, 0])
    scene.play(*[stage.fade(f, 0.0) for f in tetra], *[stage.fade(h, 1.0) for h in hydrogens], FadeIn(ch4), run_time=1.4)

    # --- 8. Not put in by hand ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    by_hand = caption("Why do ideal hybrids point this way?", cfg.GOLD)
    scene.play(FadeIn(by_hand), run_time=0.9)
    scene.play(*stage.turn(pitch=0.6), run_time=2.4, rate_func=there_and_back)

    # --- 9. Hybrids must be orthogonal ------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    hide(scene, stage, 0.7, FadeOut(VGroup(recipe, none_left, ch4, by_hand)))
    hybrid_eq = eq(r"h_i = \frac{s + \sqrt{n}\,p_i}{\sqrt{1+n}}", cfg.FONT["section"]).move_to([0, 2.2, 0])
    ortho = eq(r"\langle h_i | h_j \rangle = \frac{1 + n\cos\theta}{1+n} = 0", cfg.FONT["section"]).move_to([0, 0.4, 0])
    independent = caption("Ideal equivalent hybrids: orthogonal", cfg.WHITE)
    scene.play(Write(hybrid_eq), FadeIn(independent), run_time=1.8)
    scene.play(Write(ortho), run_time=2.0)

    # --- 10. So cos(theta) = -1/n -------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    result = eq(r"\cos\theta = -\frac{1}{n}", cfg.FONT["hero"], cfg.GOLD).move_to([0, -1.9, 0])
    scene.play(Write(result), FadeOut(independent), run_time=1.6)
    frame = glow_frame(result, cfg.GOLD, buff=0.25)
    scene.play(Create(frame), run_time=0.9)

    # --- 11-13. sp, sp2, sp3 ----------------------------------------------------------------------------------------------------------------
    scene.play(FadeOut(hybrid_eq), FadeOut(ortho), run_time=0.5)
    scene.play(VGroup(result, frame).animate.move_to([-3.9, 0.3, 0]), run_time=0.7)
    rows = VGroup()
    for k, (kind, label) in enumerate((("sp", "sp"), ("sp2", "sp^2"), ("sp3", "sp^3"))):
        n = om.HYBRID_P_PER_S[kind]
        cosine = om.equivalent_hybrid_cosine(n)
        angle = np.degrees(np.arccos(cosine))
        fraction, value = {1: ("-1", -1.0), 2: (r"-\tfrac12", -1 / 2), 3: (r"-\tfrac13", -1 / 3)}[n]
        assert abs(value - cosine) < 1e-12, "the typeset fraction must match the computed cosine"
        row = VGroup(eq(label, cfg.FONT["section"], cfg.BLUE), eq(r"\cos\theta=" + fraction, cfg.FONT["section"]),
                     degrees_label(angle, cfg.FONT["section"]))
        row.arrange(RIGHT, buff=0.6)
        rows.add(row)
    rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([3.4, 0.3, 0])
    for k, row in enumerate(rows):
        beat(scene, t, 10 + k)
        scene.play(FadeIn(row, shift=LEFT * 0.2), run_time=1.0)
        scene.play(Indicate(row[2], color=cfg.WHITE, scale_factor=1.08), run_time=1.0)
    cube = chip("the cube's −1/3 again", cfg.GOLD, cfg.FONT["label"]).next_to(rows[2], DOWN, buff=0.45)
    scene.play(FadeIn(cube, shift=UP * 0.1), run_time=0.9)

    # --- 14. Two routes, the same directions --------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(FadeOut(VGroup(result, frame, rows, cube)), run_time=0.8)
    routes = VGroup(chip("repulsion (VSEPR)", cfg.CYAN, cfg.FONT["body"]),
                    chip("orbital mixing", cfg.BLUE, cfg.FONT["body"])).arrange(DOWN, buff=1.2).move_to([-4.2, 0.2, 0])
    target = Stage([3.2, 0.1, 0], zoom=0.9, yaw=0.45, pitch=0.3, spin=0.35)
    RegionModel(target, pm.ideal_directions(4))
    arrows = VGroup(*[Arrow(r.get_right(), [1.2, 0.1, 0], buff=0.2, color=cfg.MUTED, stroke_width=6) for r in routes])
    scene.play(FadeIn(routes[0], shift=RIGHT * 0.2), run_time=0.8)
    scene.play(FadeIn(routes[1], shift=RIGHT * 0.2), run_time=0.8)
    show(scene, target, 1.0, *[GrowArrow(a) for a in arrows])
    same_dirs = caption("Same directions", cfg.GREEN)
    scene.play(FadeIn(same_dirs), run_time=0.8)

    # --- 15. Why the pictures fit together ----------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    scene.play(Indicate(same_dirs, color=cfg.WHITE, scale_factor=1.06), run_time=1.4)
    scene.play(*target.turn(pitch=0.6), run_time=2.6, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
