"""Scene 26 — drops, tubes and heat. A translucent liquid cube (a lit quad
mesh, ``kit_g.ShadedMesh``) melts into a sphere. Its volume is held fixed by
rescaling the mesh every frame, and its surface area is measured from the
mesh itself (``kit_g.mesh_volume_area``) and read out live: about a fifth
less (``pm.sphere_vs_cube_area``). On a table the drop sags, flattened by
gravity and contact; lifted free it rounds up again.

Two glass capillaries stand in dishes. Water wets the glass and climbs, its
meniscus a bowl curving up at the walls; mercury is depressed, its meniscus a
dome curving down. (The heights are illustrative.) Finally the surface
tension of water against temperature (``pm.water_surface_tension``, the IAPWS
formula): it falls as the water warms and reaches zero at the critical
temperature, about 374 °C, where the surface itself disappears.
"""

from manim_scenes.common import *
from manim_scenes.kit_d import Trace, at_word
from manim_scenes.kit_g import ShadedMesh, column_mesh, column_points, cube_mesh, mesh_volume_area

WATER_COLOR = cfg.LIQUID_EDGE
MERCURY = "#C9D3DD"
DROP_AT = (-3.2, -0.55, 0.0)
COL_X = 4.3


class Scene26DropsTubes(Scene):
    def construct(self) -> None:
        play_scene(self)


def meniscus(centre, radius: float, y: Callable[[], float], curve: float, rings: int = 6, segments: int = 28):
    """A bowl (curve > 0) or dome (curve < 0) cap: rings of quads from the axis out to the wall."""
    c = np.asarray(centre, dtype=float)
    a = np.linspace(0, 2 * np.pi, segments, endpoint=False)
    radii = np.linspace(0.02, radius, rings + 1)

    def verts() -> np.ndarray:
        y0 = float(y())
        pts = []
        for r in radii:
            pts.extend([[c[0] + np.cos(x) * r, y0 + curve * (r / radius) ** 2, c[2] - np.sin(x) * r] for x in a])
        return np.array(pts)

    quads = []
    for i in range(rings):
        for k in range(segments):
            p, q = i * segments + k, i * segments + (k + 1) % segments
            quads.append([p, q, q + segments, p + segments])
    return verts, np.array(quads)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "26", TITLES["26"])

    # --- 0. Which shape has the least area? ---------------------------------------------------------------------------
    stage = Stage(DROP_AT, zoom=1.55, yaw=-0.55, pitch=0.35, sway=0.04)
    cube, quads = cube_mesh(12)
    unit = cube / np.linalg.norm(cube, axis=1, keepdims=True)
    v_cube, a_cube = mesh_volume_area(cube, quads)
    morph, squash, lift = Knob(0.0), Knob(1.0), Knob(0.0)

    def shape() -> np.ndarray:
        s = morph.value
        p = cube * (1 - s) + unit * s
        v, _ = mesh_volume_area(p, quads)
        p = p * (v_cube / v) ** (1 / 3)
        k = squash.value
        p = p * np.array([1 / np.sqrt(k), k, 1 / np.sqrt(k)])
        p[:, 1] += -p[:, 1].min() - 1.3 + lift.value
        return p

    back = ShadedMesh(shape, quads, WATER_COLOR, opacity=0.42, side="back", key=lambda: -100, edge_opacity=0.0)
    front = ShadedMesh(shape, quads, WATER_COLOR, opacity=0.62, side="front", key=lambda: 100, edge_opacity=0.035, gloss=0.9)
    floor = Grid((0, -1.32, 0), (1, 0, 0), (0, 0, 1), (-3.0, 3.0), (-3.0, 3.0), step=0.4, major=0, color=cfg.GRID, opacity=0.25)
    floor.presence = 0.0
    stage.add_body(floor, back, front)
    show(scene, stage, 1.0)
    question = VGroup(txt("same volume,", cfg.FONT["label"], cfg.WHITE), txt("least area?", cfg.FONT["section"], cfg.GOLD))
    question.arrange(DOWN, buff=0.15).move_to([COL_X, 2.0, 0])
    scene.play(FadeIn(question, shift=DOWN * 0.1), *stage.turn(yaw=-0.4), run_time=1.2)
    at_word(scene, t, 0, "sphere", lead=0.3)
    answer = result_label("a sphere", cfg.GOLD, cfg.FONT["title"]).next_to(question, DOWN, buff=0.35)
    play_in(scene, t, 1, FadeIn(answer, scale=1.15), run_time=1.0)

    # --- 1. Cube to sphere at the same volume: the area shrinks by about a fifth ------------------------------------------
    beat(scene, t, 1)

    def area_ratio() -> float:
        return mesh_volume_area(shape(), quads)[1] / a_cube

    area_row = live(VGroup(), lambda: VGroup(txt("area", cfg.FONT["label"], cfg.MUTED),
                                             txt(f"{fx(100 * area_ratio(), 0)} %", cfg.FONT["hero"], cfg.WHITE))
                    .arrange(RIGHT, buff=0.3).move_to([COL_X, -0.4, 0]))
    vol_row = txt("volume fixed", cfg.FONT["small"], cfg.VOLUME).move_to([COL_X, -1.35, 0])
    scene.play(FadeOut(question), run_time=0.4)
    scene.play(answer.animate.scale(0.75).move_to([COL_X, 2.6, 0]), FadeIn(area_row), FadeIn(vol_row), run_time=0.7)
    at_word(scene, t, 1, "sphere", lead=0.6)
    scene.play(morph.to(stage, 1.0, rate_func=smooth), *stage.turn(yaw=-0.2), run_time=4.4)
    area_row.clear_updaters()
    fifth = boxed(txt(f"−{fx(100 * (1 - pm.sphere_vs_cube_area()), 0)} %  ≈ a fifth", cfg.FONT["label"], cfg.GOLD), cfg.GOLD, buff=0.16)
    fifth.move_to([COL_X, -2.35, 0])
    scene.play(FadeIn(fifth, shift=UP * 0.1), run_time=1.0)
    at_word(scene, t, 1, "round", lead=0.4)
    play_in(scene, t, 2, *stage.turn(yaw=-0.45), run_time=1.6)

    # --- 2. On a table it sags; floating free it is round ---------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(area_row, vol_row, fifth, answer)), stage.fade(floor, 1.0), squash.to(stage, 0.6, rate_func=smooth),
               run_time=2.0)
    table = txt("on a table: it sags", cfg.FONT["label"], cfg.WHITE).move_to([COL_X, 1.0, 0])
    scene.play(FadeIn(table, shift=DOWN * 0.1), run_time=0.8)
    at_word(scene, t, 2, "orbit", lead=0.3)
    orbit = txt("floating free: a sphere", cfg.FONT["label"], cfg.GOLD).move_to([COL_X, -0.2, 0])
    play_in(scene, t, 3, stage.fade(floor, 0.0), squash.to(stage, 1.0, rate_func=smooth), lift.to(stage, 0.6, rate_func=smooth),
            FadeIn(orbit, shift=UP * 0.1), run_time=2.6)

    # --- 3. Water climbs a clean glass tube ---------------------------------------------------------------------------------
    beat(scene, t, 3)
    hide(scene, stage, 0.8, FadeOut(VGroup(table, orbit)))
    rig = Stage((0.0, -1.0, 0.0), zoom=1.55, yaw=-0.3, pitch=0.28, sway=0.03)
    R_TUBE = 0.42
    tube_quads = column_mesh(28)
    rise, sink = Knob(0.0), Knob(0.0)

    def tube(x: float, liquid: str, level: Callable[[], float], curve: float) -> list:
        glass_pts = column_points((x, 0, 0), R_TUBE, -1.25, 2.3)
        glass_back = ShadedMesh(glass_pts, tube_quads, cfg.GLASS, opacity=0.22, side="back", key=lambda: -200, edge_opacity=0.0)
        glass_front = ShadedMesh(glass_pts, tube_quads, cfg.GLASS, opacity=0.16, side="front", key=lambda: 200, edge_opacity=0.12)
        col = ShadedMesh(lambda: column_points((x, 0, 0), R_TUBE * 0.97, -1.25, level() + curve), tube_quads, liquid,
                         opacity=0.85, side="both", key=lambda: 0, edge_opacity=0.0)
        mv, mq = meniscus((x, 0, 0), R_TUBE * 0.97, level, curve)
        cap = ShadedMesh(mv, mq, liquid, opacity=0.95, side="both", key=lambda: 10, edge_opacity=0.18, gloss=0.9)
        dish = Face([np.array([x - 1.2, 0, -0.8]), np.array([x + 1.2, 0, -0.8]), np.array([x + 1.2, 0, 0.8]),
                     np.array([x - 1.2, 0, 0.8])], liquid, opacity=0.3, edge_opacity=0.6)
        dish.bias = 50.0
        dish_walls = [Segment(np.array([x + sx * 1.2, -0.45, sz * 0.8]), np.array([x + sx * 1.2, 0.15, sz * 0.8]), cfg.GLASS, 2.4, 0.6)
                      for sx in (-1, 1) for sz in (-1, 1)]
        return [glass_back, col, cap, dish, *dish_walls, glass_front]

    water = tube(-1.9, cfg.BLUE, lambda: rise.value, 0.2)
    mercury = tube(1.9, MERCURY, lambda: sink.value, -0.16)
    for part in mercury:
        part.presence = 0.0
    rig.add_body(*water, *mercury)
    show(scene, rig, 1.0)
    wets = txt("water wets glass", cfg.FONT["label"], WATER_COLOR).move_to([-3.4, 3.2, 0])
    scene.play(FadeIn(wets, shift=DOWN * 0.1), run_time=0.8)
    at_word(scene, t, 3, "climbs", lead=0.3)
    scene.play(rise.to(rig, 1.7, rate_func=smooth), run_time=2.6)
    at_word(scene, t, 3, "curves", lead=0.3)
    bowl = txt("curves up at the glass", cfg.FONT["small"], cfg.WHITE).move_to([-3.4, -3.55, 0])
    play_in(scene, t, 4, FadeIn(bowl, shift=DOWN * 0.1), rig.zoom_to(1.75), run_time=1.4)

    # --- 4. Mercury does the opposite ------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*fade_all(rig, mercury, 1.0), rig.zoom_to(1.55), run_time=1.0)
    hg = txt("mercury", cfg.FONT["label"], MERCURY).move_to([3.4, 3.2, 0])
    scene.play(FadeIn(hg, shift=DOWN * 0.1), run_time=0.7)
    at_word(scene, t, 4, "sinks", lead=0.6)
    scene.play(sink.to(rig, -0.75, rate_func=smooth), run_time=2.2)
    dome = txt("curves down, sinks", cfg.FONT["small"], cfg.WHITE).move_to([3.4, -3.55, 0])
    play_in(scene, t, 5, FadeIn(dome, shift=DOWN * 0.1), run_time=1.0)

    # --- 5. Heat lowers the surface tension ------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, rig, 0.8, FadeOut(VGroup(wets, bowl, hg, dome)))
    tc = pm.celsius(pm.WATER_TC)
    axes = plot_axes((0, 400), (0, 80), x_length=9.4, y_length=5.2, at=[-0.3, -0.45, 0], x_label="T", y_label=r"\gamma",
                     x_color=cfg.TEMPERATURE, y_color=cfg.GOLD, x_ticks=(100, 200, 300, 400), y_ticks=(20, 40, 60, 80))
    units = VGroup(txt("°C", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.labels[0], RIGHT, buff=0.1, aligned_edge=DOWN),
                   txt("mN/m", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.labels[1], RIGHT, buff=0.12))
    axes.add(decorative(units))
    ts = np.linspace(0, tc, 300)
    trace = Trace(axes, ts, [pm.water_surface_tension(pm.kelvin(x)) for x in ts], WATER_COLOR, start=0.0)
    name = txt("water", cfg.FONT["label"], WATER_COLOR).move_to(axes.c2p(60, 50))
    scene.play(Create(axes), FadeIn(name), run_time=1.2)
    scene.add(trace.curve, trace.bead)
    play_in(scene, t, 6, trace.grow(100.0, rate_func=smooth), run_time=3.0)

    # --- 6. All the way to zero at the critical temperature ------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(trace.grow(tc, rate_func=smooth), run_time=5.0)
    at_word(scene, t, 6, "critical", lead=0.3)
    cp = glow_dot(axes.c2p(tc, 0), cfg.CRITICAL, radius=0.16, reach=4)
    cp_tag = VGroup(result_label("critical temperature", cfg.CRITICAL, cfg.FONT["label"]),
                    txt(f"≈ {fx(tc, 0)} °C", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.24)
    cp_tag.move_to(axes.c2p(300, 40))
    scene.play(FadeIn(cp, scale=2), FadeIn(cp_tag, shift=DOWN * 0.1), trace.fade_bead(0.0), run_time=1.2)
    at_word(scene, t, 6, "disappears", lead=0.4)
    zero = eq(r"\gamma = 0", cfg.FONT["title"], cfg.CRITICAL).next_to(cp_tag, UP, buff=0.3)
    scene.play(FadeIn(zero, shift=DOWN * 0.1), run_time=1.0)
    finish(scene, t, fill=lambda s: [Indicate(cp, color=cfg.WHITE, scale_factor=1.3)])
