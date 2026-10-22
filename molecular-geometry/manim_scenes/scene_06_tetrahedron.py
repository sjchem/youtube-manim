"""Chapter 06 — the tetrahedron, and where 109.47 degrees comes from.

Four regions start in the flat square a Lewis structure suggests; every
region has two neighbours at 90 degrees (red). Tilting two up and two down
opens every gap to the tetrahedral angle (a live readout tracks it). The
tetrahedron grown from the square sits exactly on alternate corners of a
cube after a 45-degree turn, which is how the dot-product argument is shown:
(1,1,1).(1,-1,-1) = -1, |a||b| = 3, cos = -1/3 — all taken from
``physics_models.cube_dot_product``.
"""

from manim_scenes.common import *

MODEL_AT = np.array([-3.3, 0.1, 0])
VECTOR_A_COLOR = "#B6FF00"  # Fluorescent lime, shared by the arrow and its coordinates.
VECTOR_B_COLOR = "#FF4DDB"  # Fluorescent pink, distinct from the white bonds and gold angles.
A, B = np.sqrt(2 / 3), np.sqrt(1 / 3)
TETRA_FROM_SQUARE = [np.array(v) for v in ([A, 0, B], [0, A, -B], [-A, 0, B], [0, -A, -B])]


class Scene06Tetrahedron(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "06", "The tetrahedron")

    # --- 1. Methane: four regions, AX4 ------------------------------------------------------------------------
    spec = ml.molecule("CH4")
    stage = Stage([0, 0.1, 0], zoom=1.15, pitch=0.0, sway=0.08)
    model = MoleculeModel(stage, spec, domains=True)
    for i, d in enumerate((RIGHT, UP, LEFT, DOWN)):
        model.dirs[i] = d.astype(float)
    for i in range(4):
        model.atoms[i].presence = model.rods[i].presence = 0.0
    show(scene, stage, 1.0)
    code = axe_eq(4, 0, cfg.FONT["section"]).move_to([4.9, 2.4, 0])
    scene.play(FadeIn(code, shift=LEFT * 0.2), run_time=0.8)
    dismiss_opening_title(scene, t, head)

    # --- 2. The flat guess: a square ----------------------------------------------------------------------------
    beat(scene, t, 1)
    square_arcs = [model.arc(i, (i + 1) % 4, radius=0.95, label=degrees_label(90, cfg.FONT["label"]), label_gap=0.5)
                   for i in range(4)]
    guess = caption("The flat guess: a square", cfg.WHITE)
    scene.play(*[stage.fade(a, 1.0) for a in square_arcs], FadeIn(guess), run_time=1.4)

    # --- 3. Every region crowded by two neighbours at 90 degrees --------------------------------------------------
    beat(scene, t, 2)
    crowded = caption("Each region: two neighbours at 90°", cfg.RED)
    for arc in square_arcs:
        arc.arc.set_stroke(cfg.RED)
        arc.glow.set_stroke(cfg.RED)
    scene.play(fade_through(guess, crowded), run_time=0.9)
    scene.remove(guess)
    pushes = [Vector(model._site_point(i, 1.12), model._site_point((i + 1) % 4, 1.12), cfg.RED, width=0.06, tip=0.2)
              for i in range(4)]
    for p in pushes:
        p.presence = 0.0
        stage.add_overlay(p)
    scene.play(*[stage.fade(p, 0.8) for p in pushes], run_time=0.8)
    scene.play(*[stage.fade(p, 0.0) for p in pushes], run_time=1.6, rate_func=there_and_back_with_pause)

    # --- 4. Use the third dimension ---------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*[stage.fade(a, 0.0) for a in square_arcs], *[stage.fade(p, 0.0) for p in pushes],
               *stage.turn(yaw=0.4, pitch=0.42), run_time=1.6)
    live = model.arc(0, 1, radius=1.1, live=True, label_gap=0.6, size=cfg.FONT["body"])
    lift = caption("Two tilt up, two tilt down", cfg.CYAN)
    scene.play(stage.fade(live, 1.0), fade_through(crowded, lift), run_time=0.8)
    scene.remove(crowded)
    scene.play(*[model.aim(i, d) for i, d in enumerate(TETRA_FROM_SQUARE)], run_time=3.8, rate_func=smooth)

    # --- 5. All equally spaced: the tetrahedron ------------------------------------------------------------------------
    beat(scene, t, 4)
    faces = [Face([model._site_point(a), model._site_point(b), model._site_point(c)], cfg.CYAN, 0.08, 0.45)
             for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))]
    for face in faces:
        face.presence = 0.0
    stage.add_body(*faces)
    equal = caption("Every region equally spaced", cfg.GREEN)
    scene.play(*[stage.fade(f, 1.0) for f in faces], fade_through(lift, equal), run_time=1.2)
    scene.remove(lift)
    scene.play(stage.set_spin(0.5), run_time=1.0)
    scene.play(Indicate(equal, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)

    # --- 6. Hydrogens at the tips: methane ------------------------------------------------------------------------------
    beat(scene, t, 5)
    shape = shape_name(spec.shape, size=cfg.FONT["section"]).move_to([4.9, 1.35, 0])
    scene.play(*model.fade("atoms", 1.0), *model.fade("rods", 1.0), *model.fade("domains", 0.25),
               *[stage.fade(f, 0.35) for f in faces], FadeIn(shape, shift=UP * 0.1), FadeOut(equal), run_time=1.6)
    scene.play(stage.set_spin(0.25), run_time=1.5)

    # --- 7. Where does the number come from? A cube ------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(stage.set_spin(0.0), *[stage.fade(f, 0.0) for f in faces], *model.fade("domains", 0.0),
               FadeOut(code), FadeOut(shape), stage.fade(live, 0.0), stage.glide(MODEL_AT), run_time=1.2)
    scene.play(stage.rock(OUT, np.pi / 4), *stage.turn(yaw=0.42, pitch=0.38), run_time=1.6, rate_func=smooth)
    half = BOND / np.sqrt(3)
    # The stage now turns the model 45 degrees about z; express the cube in the
    # model's own frame so the two line up on screen.
    undo = mu.rotation_z(-np.pi / 4)
    corners = {(i, j, k): undo @ (np.array([i, j, k], dtype=float) * half)
               for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)}
    edges = [Segment(corners[a], corners[b], cfg.MUTED, 3.0, 0.75)
             for a in corners for b in corners if a < b and sum(x != y for x, y in zip(a, b)) == 1]
    for e in edges:
        e.presence = 0.0
    stage.add_body(*edges)
    cube = caption("Carbon at the centre of a cube", cfg.WHITE)
    scene.play(*[stage.fade(e, 1.0) for e in edges], FadeIn(cube), run_time=1.6)

    # --- 8. Alternate corners -----------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    glows = [Halo(model.atoms[i], cfg.GOLD, reach=2.6, peak=0.22) for i in range(4)]
    for g in glows:
        g.presence = 0.0
    stage.add_body(*glows)
    alternate = caption("Hydrogens on alternate corners", cfg.GOLD)
    scene.play(*[stage.fade(g, 1.0) for g in glows], fade_through(cube, alternate), run_time=1.2)
    scene.remove(cube)
    scene.play(*stage.turn(yaw=1.0), run_time=3.0, rate_func=there_and_back)

    # --- 9. Two bond directions ------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    # After the 45-degree turn, sites 0 and 3 sit on the corners (1,1,1) and (1,-1,-1).
    a_vec = Vector(ORIGIN, lambda: model.point(0) * 0.96, VECTOR_A_COLOR, width=0.11, tip=0.30)
    b_vec = Vector(ORIGIN, lambda: model.point(3) * 0.96, VECTOR_B_COLOR, width=0.11, tip=0.30)
    corner_a, corner_b = pm.CUBE_CORNERS[0], pm.CUBE_CORNERS[1]
    a_tag = Tag(eq(r"\vec a=(1,1,1)", cfg.FONT["label"], VECTOR_A_COLOR), lambda: model.point(0), UP * 0.6 + LEFT * 0.4)
    b_tag = Tag(eq(r"\vec b=(1,-1,-1)", cfg.FONT["label"], VECTOR_B_COLOR), lambda: model.point(3), DOWN * 0.65)
    for item in (a_vec, b_vec, a_tag, b_tag):
        item.presence = 0.0
        stage.add_overlay(item)
    scene.play(*[stage.fade(g, 0.0) for g in glows], FadeOut(alternate), stage.fade(a_vec, 1.0), stage.fade(b_vec, 1.0),
               run_time=1.0)
    scene.play(stage.fade(a_tag, 1.0), stage.fade(b_tag, 1.0), run_time=1.0)
    on_screen = [mu.unit(stage.model @ model.point(i)) for i in (0, 3)]
    assert np.allclose(on_screen[0], mu.unit(corner_a)) and np.allclose(on_screen[1], mu.unit(corner_b))

    # --- 10. Dot product and lengths ---------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    dot, lengths, cosine = pm.cube_dot_product()
    rows = VGroup(
        eq(r"\vec a\cdot\vec b = 1 - 1 - 1 = " + f"{dot:.0f}", cfg.FONT["body"]),
        eq(r"|\vec a|=|\vec b|=\sqrt{3}", cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([3.6, 1.6, 0])
    scene.play(Write(rows[0]), run_time=1.6)
    scene.play(Write(rows[1]), run_time=1.3)

    # --- 11. cos = -1/3 -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    cos_row = eq(r"\cos\theta = \frac{-1}{\sqrt3\,\sqrt3} = -\frac{1}{3}", cfg.FONT["body"]).move_to([3.6, -0.35, 0])
    assert abs(cosine + 1 / 3) < 1e-12 and abs(lengths - 3) < 1e-12
    scene.play(Write(cos_row), run_time=1.8)
    theta = model.arc(0, 3, radius=0.9, color=cfg.GOLD)
    scene.play(stage.fade(theta, 1.0), run_time=0.8)

    # --- 12. theta = 109.47 degrees ------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    result = eq(r"\theta=\cos^{-1}\!\left(-\tfrac13\right)\approx" + f"{np.degrees(np.arccos(cosine)):.2f}" + r"^\circ",
                cfg.FONT["body"], cfg.GOLD).move_to([3.6, -2.0, 0])
    scene.play(Write(result), run_time=1.8)
    box = glow_frame(result, cfg.GOLD, buff=0.2)
    scene.play(Create(box), run_time=0.9)

    # --- 13. Just the geometry of four equal directions --------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(*[stage.fade(e, 0.3) for e in edges], stage.fade(a_tag, 0.0),
               stage.fade(b_tag, 0.0), stage.fade(a_vec, 0.0), stage.fade(b_vec, 0.0),
               stage.set_spin(0.12), run_time=1.5)
    scene.play(Indicate(result, color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    scene.play(*stage.turn(pitch=0.6), run_time=2.6, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
