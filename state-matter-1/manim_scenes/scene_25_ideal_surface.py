"""Scene 25 — four laws, one surface. A table lists each law with the two
quantities it holds constant; the volume relations combine into V ~ nT/P,
then PV = nRT. Every state of one mole of ideal gas becomes one curved 3D
surface, P = RT/V, computed from R in ``physics_models`` (V from 8 to 40 L,
T from 150 to 600 K). Slices light up: constant T gives Boyle's hyperbola,
constant V gives Gay-Lussac's straight line, constant P gives Charles'
straight line. A bead rides each slice; the surface keeps turning.
"""

from manim_scenes.common import *

V_RANGE, T_RANGE, P_TOP = (8.0, 40.0), (150.0, 600.0), 6.4
R = pm.R_L_BAR


def pressure(v: float, temp: float) -> float:
    return R * temp / v


def world(v: float, temp: float, p: float | None = None) -> np.ndarray:
    """(V, T, P) -> stage point: V along x, P up, T going away from the viewer."""
    p = pressure(v, temp) if p is None else p
    x = -2.4 + 4.8 * (v - V_RANGE[0]) / (V_RANGE[1] - V_RANGE[0])
    z = 1.7 - 3.4 * (temp - T_RANGE[0]) / (T_RANGE[1] - T_RANGE[0])
    y = -1.4 + 3.6 * p / P_TOP
    return np.array([x, y, z])


class Scene25IdealSurface(Scene):
    def construct(self) -> None:
        play_scene(self)


def row(law: str, held: str, relation: str, color: str, header: bool = False) -> VGroup:
    third = txt(relation, cfg.FONT["label"], cfg.GOLD) if header else eq(relation, cfg.FONT["label"], cfg.WHITE)
    cells = VGroup(txt(law, cfg.FONT["label"], color), txt(held, cfg.FONT["label"], cfg.MUTED), third)
    for cell, x in zip(cells, (-4.2, -0.3, 3.6)):
        cell.move_to([x, 0, 0])
    return cells


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "25", "Four laws, one surface")
    header = row("law", "held constant", "relation", cfg.GOLD, header=True)
    rows = [row("Boyle", "T, n", r"V \propto \frac{1}{P}", cfg.PRESSURE), row("Charles", "P, n", r"V \propto T", cfg.VOLUME),
            row("Gay-Lussac", "V, n", r"P \propto T", cfg.TEMPERATURE), row("Avogadro", "P, T", r"V \propto n", cfg.AMOUNT)]
    for k, r in enumerate([header, *rows]):
        r.shift(UP * (2.3 - 1.05 * k))
    rule = Line([-6.2, 1.75, 0], [6.2, 1.75, 0], stroke_color=cfg.MUTED, stroke_width=2)
    scene.play(FadeIn(header), Create(rule), run_time=1.2)

    # --- 2-5. Each law: two quantities held constant ---------------------------------------------------------------------------
    for index, r in enumerate(rows, start=1):
        beat(scene, t, index)
        scene.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in r], lag_ratio=0.25), run_time=1.4)

    # --- 6. Combine the volume relations: V ~ nT/P; a constant R ------------------------------------------------------------------
    beat(scene, t, 5)
    combine = eq(r"V \propto \frac{nT}{P}", cfg.FONT["hero"], cfg.WHITE).move_to([0, 0.4, 0])
    table = VGroup(header, rule, *rows)
    scene.play(FadeOut(table), run_time=1.2)
    scene.play(Write(combine), run_time=1.6)
    with_r = eq(r"V = R\,\frac{nT}{P}", cfg.FONT["hero"], cfg.WHITE).move_to([0, 0.4, 0])
    scene.play(fade_through(combine, with_r), run_time=1.4)

    # --- 7. PV = nRT ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    final = paint(eq([r"PV", "=", "n", "R", "T"], 96), {0: cfg.PRESSURE, 2: cfg.AMOUNT, 4: cfg.TEMPERATURE})
    result = boxed(final, cfg.GOLD).move_to([0, 0.4, 0])
    scene.play(fade_through(with_r, final), run_time=1.4)
    scene.play(Create(result.frame), run_time=1.0)

    # --- 8. One mole: every state on one surface ------------------------------------------------------------------------------------
    beat(scene, t, 7)
    stage = Stage((1.6, -0.05, 0), zoom=1.2, yaw=-0.75, pitch=0.42, sway=0.03)
    vs = np.linspace(*V_RANGE, 14)
    ts = np.linspace(*T_RANGE, 10)
    faces = []
    for i in range(len(vs) - 1):
        for j in range(len(ts) - 1):
            corners = [world(vs[i], ts[j]), world(vs[i + 1], ts[j]), world(vs[i + 1], ts[j + 1]), world(vs[i], ts[j + 1])]
            level = pressure((vs[i] + vs[i + 1]) / 2, (ts[j] + ts[j + 1]) / 2) / P_TOP
            color = mu.mix(cfg.BLUE, cfg.GOLD, float(np.clip(level * 1.3, 0, 1)))
            face = Face(corners, color, opacity=0.5, edge_opacity=0.18)
            face.presence = 0.0
            faces.append(face)
    fine_v = np.linspace(*V_RANGE, 60)
    fine_t = np.linspace(*T_RANGE, 40)
    meshes = [Curve(np.array([world(v, temp) for v in fine_v]), cfg.WHITE, width=1.4, glow=False, opacity=0.35) for temp in ts]
    meshes += [Curve(np.array([world(v, temp) for temp in fine_t]), cfg.WHITE, width=1.4, glow=False, opacity=0.35) for v in vs]
    for m in meshes:
        m.presence = 0.0
    origin = world(V_RANGE[0], T_RANGE[0], 0.0)
    axes3 = [Segment(origin, world(V_RANGE[1] + 2, T_RANGE[0], 0.0), cfg.VOLUME, width=4, opacity=0.9),
             Segment(origin, world(V_RANGE[0], T_RANGE[1] + 40, 0.0), cfg.TEMPERATURE, width=4, opacity=0.9, dashed=True),
             Segment(origin, world(V_RANGE[0], T_RANGE[0], P_TOP * 1.05), cfg.PRESSURE, width=4, opacity=0.9)]
    # The temperature axis recedes under the translucent surface. Draw it behind the mesh.
    axes3[1].bias = -100.0
    axes3[1].opacity = 0.55
    tags = [Tag(eq("V", cfg.FONT["section"], cfg.VOLUME), world(V_RANGE[1] + 3.5, T_RANGE[0], 0.0)),
            # Label the near part of T's axis, outside the projected surface.
            Tag(eq("T", cfg.FONT["section"], cfg.TEMPERATURE), world(V_RANGE[0], T_RANGE[0] + 90, 0.0), LEFT * 0.45),
            Tag(eq("P", cfg.FONT["section"], cfg.PRESSURE), world(V_RANGE[0], T_RANGE[0], P_TOP * 1.15))]
    stage.add_body(*axes3, *faces, *meshes)
    stage.add_overlay(*tags)
    corner = VGroup(result.frame, final)
    scene.wait(0.4)
    scene.play(corner.animate.scale(0.5).move_to([-5.2, 3.1, 0]), run_time=0.6)
    show(scene, stage, 0.8)
    scene.play(*[stage.fade(f, 1.0) for f in faces], *stage.turn(yaw=-0.55, run_time=2.0), run_time=2.0)
    scene.play(*[stage.fade(m, 1.0) for m in meshes], run_time=1.2)
    one = txt("one mole: P = RT / V", cfg.FONT["small"], cfg.MUTED).move_to([-5.2, 2.2, 0])
    scene.play(FadeIn(one), run_time=0.8)

    def slice_bead(points: np.ndarray, color: str) -> tuple[Ball, Knob]:
        s = Knob(0.0)
        bead_ = Ball(lambda: points[int(np.clip(s.value, 0, 1) * (len(points) - 1))], 0.11, color)
        bead_.bias = 50
        bead_.presence = 0.0
        stage.add_body(bead_)
        return bead_, s

    # --- 9. Constant T: Boyle's hyperbola ------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    iso_pts = np.array([world(v, 450.0) for v in fine_v])
    iso = Curve(iso_pts, cfg.CYAN, width=6, bias=40)
    iso.presence = 0.0
    stage.add_body(iso)
    bead1, s1 = slice_bead(iso_pts, cfg.CYAN)
    name1 = txt("constant T: Boyle", cfg.FONT["label"], cfg.CYAN).move_to([4.6, 3.1, 0])
    scene.play(*[stage.fade(f, 0.45) for f in faces], stage.fade(iso, 1.0), stage.fade(bead1, 1.0), FadeIn(name1), run_time=1.2)
    scene.play(s1.to(stage, 1.0, run_time=2.4, rate_func=there_and_back), *stage.turn(yaw=-0.62, run_time=2.4), run_time=2.4)

    # --- 10. Constant V: Gay-Lussac's straight line --------------------------------------------------------------------------------------
    beat(scene, t, 9)
    chore_pts = np.array([world(16.0, temp) for temp in fine_t])
    chore = Curve(chore_pts, cfg.TEMPERATURE, width=6, bias=40)
    chore.presence = 0.0
    stage.add_body(chore)
    bead2, s2 = slice_bead(chore_pts, cfg.TEMPERATURE)
    name2 = txt("constant V: Gay-Lussac", cfg.FONT["label"], cfg.TEMPERATURE).move_to([4.6, 3.1, 0])
    scene.play(stage.fade(iso, 0.0), stage.fade(bead1, 0.0), stage.fade(chore, 1.0), stage.fade(bead2, 1.0),
               fade_through(name1, name2), run_time=1.2)
    scene.play(s2.to(stage, 1.0, run_time=2.6, rate_func=there_and_back), *stage.turn(yaw=-0.95, run_time=2.6), run_time=2.6)

    # --- 11. Constant P: Charles' straight line --------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    p_const = 2.0
    bar_t = np.linspace(V_RANGE[0] * p_const / R, T_RANGE[1], 40)
    bar_pts = np.array([world(R * temp / p_const, temp, p_const) for temp in bar_t])
    bar = Curve(bar_pts, cfg.VOLUME, width=6, bias=40)
    bar.presence = 0.0
    stage.add_body(bar)
    bead3, s3 = slice_bead(bar_pts, cfg.VOLUME)
    name3 = txt("constant P: Charles", cfg.FONT["label"], cfg.VOLUME).move_to([4.6, 3.1, 0])
    scene.play(stage.fade(chore, 0.0), stage.fade(bead2, 0.0), stage.fade(bar, 1.0), stage.fade(bead3, 1.0),
               fade_through(name2, name3), run_time=1.2)
    scene.play(s3.to(stage, 1.0, run_time=2.6, rate_func=there_and_back), *stage.turn(yaw=-0.7, run_time=2.6), run_time=2.6)

    # --- 12. Views of one surface ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    views = result_label("one surface, one equation", cfg.GOLD, cfg.FONT["body"]).move_to([-4.0, -2.9, 0])
    scene.play(stage.fade(iso, 1.0), stage.fade(chore, 1.0), stage.fade(bead3, 0.0), FadeOut(name3), FadeIn(views, scale=0.95),
               run_time=1.2)
    finish(scene, t, stage, drift=0.25)
