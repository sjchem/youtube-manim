"""Scene 28 — water, honey and glass. Two glass cylinders on a turning 3D
stage, one of water and one of honey; a steel ball is dropped into each. In
water it plunges; in honey it crawls (the speeds are illustrative). At room
temperature honey is roughly 2 000 to 20 000 times as viscous as water
(``pm.honey_to_water``, from ``pm.HONEY_VISCOSITY_PA_S``).

Why: small water molecules held by hydrogen bonds (green dashes) beside a
separate polymer example — honey is a concentrated sugar solution, not tangled polymers.
Strong attractions and molecular structure both make layers harder
to slide, but attraction alone does not predict viscosity. Water's viscosity
from 0 to 100 °C (``pm.WATER_VISCOSITY``, CRC) falls steadily; at 100 °C it
is less than a third of its 20 °C value. Warmed, the honey lets its ball fall
faster.

Finally the glass myth: a pane sketched thicker at the bottom is struck out.
Glass is an amorphous solid: its atoms are disordered like a liquid's (a
random network beside an ordered crystal) but locked in place — they only
vibrate, and over centuries the network does not measurably flow. Old panes
were uneven because of how they were made: some are thicker at the top.
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d, ticking
from manim_scenes.kit_d import at_word
from manim_scenes.kit_g import ShadedMesh, column_mesh, column_points

HONEY = "#E8A33D"
WATER = cfg.LIQUID_EDGE
CYL_R, CYL_BOTTOM, CYL_TOP, FILL = 0.78, -1.7, 1.7, 1.25
X_WATER, X_HONEY = -2.0, 2.0


class Scene28HoneyGlass(Scene):
    def construct(self) -> None:
        play_scene(self)


def cylinders(drop_w: Knob, drop_h: Knob) -> tuple[Stage, list]:
    stage = Stage((0.0, -0.45, 0.0), zoom=1.3, yaw=-0.25, pitch=0.3, sway=0.03)
    quads = column_mesh(30)
    parts = []
    for x, color, knob in ((X_WATER, WATER, drop_w), (X_HONEY, HONEY, drop_h)):
        glass = column_points((x, 0, 0), CYL_R, CYL_BOTTOM, CYL_TOP, 30)
        liquid = column_points((x, 0, 0), CYL_R * 0.96, CYL_BOTTOM, FILL, 30)
        parts += [ShadedMesh(glass, quads, cfg.GLASS, opacity=0.16, side="back", key=lambda: -300, edge_opacity=0.0),
                  ShadedMesh(liquid, quads, color, opacity=0.42, side="back", key=lambda: -200, edge_opacity=0.0)]
        top = Disc(np.array([x, FILL, 0.0]), CYL_R * 0.96, color, normal=(0, 1, 0), opacity=0.45, stroke=mu.mix(color, cfg.WHITE, 0.4))
        top.bias = 150.0
        ball = Ball(lambda x=x, k=knob: np.array([x, FILL + 0.9 - k.value, 0.0]), 0.2, cfg.STEEL, layers=16)
        parts += [ball, ShadedMesh(liquid, quads, color, opacity=0.3, side="front", key=lambda: 200, edge_opacity=0.0), top,
                  ShadedMesh(glass, quads, cfg.GLASS, opacity=0.12, side="front", key=lambda: 300, edge_opacity=0.3)]
    floor = Grid((0, CYL_BOTTOM - 0.02, 0), (1, 0, 0), (0, 0, 1), (-4.0, 4.0), (-2.0, 2.0), step=0.4, major=0, color=cfg.GRID,
                 opacity=0.22)
    stage.add_body(floor, *parts)
    return stage, parts


def fall(knob: Knob, holder: Mobject, depth: float, **kwargs) -> Param:
    return knob.to(holder, depth, **kwargs)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "28", TITLES["28"])
    drop_w, drop_h = Knob(0.0), Knob(0.0)
    stage, _ = cylinders(drop_w, drop_h)
    bottom_depth = FILL + 0.9 - (CYL_BOTTOM + 0.22)
    show(scene, stage, 1.0)
    names = VGroup(txt("water", cfg.FONT["section"], WATER), txt("honey", cfg.FONT["section"], HONEY))
    names[0].move_to([X_WATER * 1.3, 2.85, 0])
    names[1].move_to([X_HONEY * 1.3, 2.85, 0])
    scene.wait(1.6)
    scene.play(FadeIn(names, shift=DOWN * 0.1), run_time=0.9)
    at_word(scene, t, 0, "Drop", lead=0.2)
    play_in(scene, t, 1, fall(drop_w, stage, 0.9, rate_func=rush_into), fall(drop_h, stage, 0.9, rate_func=rush_into), run_time=0.8)

    # --- 1. It plunges in water and crawls in honey ---------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(fall(drop_w, stage, bottom_depth, rate_func=linear), fall(drop_h, stage, 1.05, rate_func=linear), run_time=1.0)
    plunge = txt("plunges", cfg.FONT["label"], WATER).next_to(names[0], DOWN, buff=0.25)
    scene.play(FadeIn(plunge), fall(drop_h, stage, 1.25, rate_func=linear), run_time=1.0)
    at_word(scene, t, 1, "crawls", lead=0.2)
    crawl = txt("crawls", cfg.FONT["label"], HONEY).next_to(names[1], DOWN, buff=0.25)
    scene.play(FadeIn(crawl), fall(drop_h, stage, 1.5, rate_func=linear), run_time=1.6)
    at_word(scene, t, 1, "thousands", lead=0.4)
    low, high = pm.honey_to_water()
    ratio = boxed(txt(f"honey ≈ {fx(round(low, -3), 0)} – {fx(round(high, -3), 0)} × water", cfg.FONT["label"], cfg.GOLD), cfg.GOLD,
                  buff=0.16).move_to([0, -3.55, 0])
    not_scale = txt("(speeds not to scale)", cfg.FONT["tiny"], cfg.MUTED).next_to(ratio, UP, buff=0.12)
    play_in(scene, t, 2, FadeIn(ratio, shift=UP * 0.1), FadeIn(not_scale), fall(drop_h, stage, 1.9, rate_func=linear), run_time=1.8)

    # --- 2. Structure and interactions decide viscosity ---------------------------------------------------------------------
    beat(scene, t, 2)
    hide(scene, stage, 0.8, FadeOut(VGroup(names, plunge, crawl, ratio, not_scale)))
    mol = Stage((-3.7, -0.3, 0.0), zoom=1.9, yaw=0.2, pitch=0.25, spin=0.3)
    centres = [np.array([-0.9, 0.5, 0.0]), np.array([0.9, 0.6, 0.3]), np.array([0.0, -0.9, -0.2])]
    waters = []
    for k, c in enumerate(centres):
        R = mu.rotation_about([0, 0, 1], 1.1 * k) @ mu.rotation_about([1, 0, 0], 0.5 * k)
        waters.append(molecule(mol, water_atoms(scale=0.8), [(0, 1), (0, 2)], centre=c, pose=lambda R=R: R, label=False))
    hbonds = [Segment(waters[0].balls[1].where, waters[1].balls[0].where, cfg.ATTRACT, width=4, opacity=0.9, dashed=True),
              Segment(waters[1].balls[2].where, waters[2].balls[0].where, cfg.ATTRACT, width=4, opacity=0.9, dashed=True),
              Segment(waters[2].balls[1].where, waters[0].balls[0].where, cfg.ATTRACT, width=4, opacity=0.9, dashed=True)]
    mol.add_body(*hbonds)
    chain = Stage((3.6, -0.3, 0.0), zoom=1.7, yaw=0.0, pitch=0.25, spin=0.25)
    rng = np.random.default_rng(cfg.SEED + 280)
    pts = [np.zeros(3)]
    for _ in range(26):
        step = mu.unit(rng.normal(size=3)) * 0.5
        nxt = pts[-1] + step
        nxt = np.clip(nxt, -1.5, 1.5)
        pts.append(nxt)
    beads_ = [Ball(p - np.mean(pts, axis=0), 0.17, HONEY if k % 3 else cfg.ATOM["O"], layers=12) for k, p in enumerate(pts)]
    rods = [Rod(beads_[k], beads_[k + 1], width=10) for k in range(len(beads_) - 1)]
    chain.add_body(*rods, *beads_)
    show(scene, mol, 0.9)
    hb_tag = txt("strong attractions", cfg.FONT["label"], cfg.ATTRACT).move_to([-3.7, 2.6, 0])
    hb_sub = txt("hydrogen bonds", cfg.FONT["small"], cfg.WHITE).next_to(hb_tag, DOWN, buff=0.24)
    scene.play(FadeIn(hb_tag, shift=DOWN * 0.1), FadeIn(hb_sub), run_time=0.9)
    at_word(scene, t, 2, "tangled", lead=0.4)
    big_tag = txt("polymers: long chains", cfg.FONT["label"], HONEY).move_to([3.6, 2.6, 0])
    show(scene, chain, 0.9, FadeIn(big_tag, shift=DOWN * 0.1))
    at_word(scene, t, 2, "alone", lead=0.4)
    caveat = chip("attraction alone can't predict it", cfg.WARNING, cfg.FONT["small"]).move_to([0, -3.4, 0])
    play_in(scene, t, 3, FadeIn(caveat, shift=UP * 0.1), run_time=1.0)

    # --- 3. Warm a liquid and its viscosity falls --------------------------------------------------------------------------
    beat(scene, t, 3)
    for st in (mol, chain):
        for member in st.get_family():
            member.clear_updaters()
    clear(scene, run_time=0.8)
    data = pm.WATER_VISCOSITY[::2]
    chart = bar_chart([v for _, v in data], [f"{c}" for c, _ in data], [WATER] * len(data), at=[0.9, -0.9, 0], width=9.0,
                      height=4.2, value_labels=[fx(v, 2) for _, v in data], bar_width=1.0, name_size=cfg.FONT["small"])
    eta_tag = VGroup(eq(r"\eta", cfg.FONT["title"], cfg.GOLD), txt("water, mPa s", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.1)
    eta_tag.next_to(chart, LEFT, buff=0.4).shift(UP * 1.0)
    t_tag = txt("°C", cfg.FONT["small"], cfg.TEMPERATURE).next_to(chart.names, RIGHT, buff=0.3)
    scene.play(Create(chart.base), FadeIn(chart.names), FadeIn(eta_tag), FadeIn(t_tag), run_time=1.0)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.15), LaggedStart(*[FadeIn(v) for v in chart.tops],
                                                                                                     lag_ratio=0.15), run_time=2.2)
    at_word(scene, t, 3, "energy", lead=0.3)
    hotter = arrow2d([-4.5, 2.4, 0], [3.5, 2.4, 0], cfg.TEMPERATURE, width=0.08, tip_len=0.26)
    hot_tag = txt("warmer → flows more easily", cfg.FONT["label"], cfg.TEMPERATURE).next_to(hotter, UP, buff=0.12)
    scene.play(FadeIn(hotter, shift=RIGHT * 0.3), FadeIn(hot_tag), run_time=1.2)
    at_word(scene, t, 3, "third", lead=0.5)
    i20 = [c for c, _ in data].index(20)
    i100 = [c for c, _ in data].index(100)
    ratio = pm.water_viscosity(100) / pm.water_viscosity(20)
    third = txt(f"100 °C: {fx(ratio, 2)} × the 20 °C value  (< 1/3)", cfg.FONT["small"], cfg.GOLD).move_to([0.9, -3.95, 0])
    play_in(scene, t, 4, Indicate(chart.bars[i20], color=cfg.WHITE), Indicate(chart.bars[i100], color=cfg.GOLD), FadeIn(third), run_time=1.4)

    # --- 4. Warm honey pours easily ----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    clear(scene, run_time=0.6)
    drop_w2, drop_h2 = Knob(bottom_depth), Knob(0.0)
    stage2, _ = cylinders(drop_w2, drop_h2)
    glow = Disc(np.array([X_HONEY, CYL_BOTTOM - 0.05, 0.0]), 1.2, cfg.HOT_COLOR, normal=(0, 1, 0), opacity=0.55, soft=True, bias=-8e3)
    stage2.add_body(glow)
    warm = txt("warm honey", cfg.FONT["section"], cfg.HOT_COLOR).move_to([X_HONEY * 1.3, 3.0, 0])
    show(scene, stage2, 0.6, FadeIn(warm))
    play_in(scene, t, 5, fall(drop_h2, stage2, bottom_depth * 0.9, rate_func=rush_into), run_time=3.2)

    # --- 5. Glass is not a slow liquid: an amorphous solid --------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, stage2, 0.7, FadeOut(warm))
    pane = Polygon([-5.9, 2.2, 0], [-5.55, 2.2, 0], [-5.25, -2.3, 0], [-6.2, -2.3, 0], stroke_color=cfg.GLASS, stroke_width=3,
                   fill_color=cfg.GLASS, fill_opacity=0.25)
    frame = Rectangle(width=1.6, height=4.9, stroke_color="#8B6B4A", stroke_width=8).move_to([-5.72, -0.05, 0])
    myth = txt("thicker at the bottom?", cfg.FONT["small"], cfg.WHITE)
    myth.move_to([-7.4 + myth.width / 2, 2.85, 0])
    flows = txt("glass flows like a liquid", cfg.FONT["label"], cfg.WHITE).move_to([1.6, 3.15, 0])
    scene.play(FadeIn(frame), FadeIn(pane), FadeIn(myth), run_time=1.0)
    at_word(scene, t, 5, "liquid", lead=0.3)
    scene.play(FadeIn(flows, shift=DOWN * 0.1), run_time=0.8)
    at_word(scene, t, 5, "isn't", lead=0.2)
    no = strike(flows)
    scene.play(Create(no), flows.animate.set_opacity(0.5), run_time=0.7)

    def lattice() -> np.ndarray:
        return np.array([[x * 0.55 + (0.275 if y % 2 else 0), y * 0.48, 0] for y in range(6) for x in range(6)])

    rng2 = np.random.default_rng(cfg.SEED + 281)
    amorph: list[np.ndarray] = []
    for _ in range(3000):                     # random sequential packing (bounded: it fills up near 30 atoms)
        p = np.array([rng2.uniform(0, 3.0), rng2.uniform(0, 2.5), 0])
        if all(np.linalg.norm(p - q) > 0.44 for q in amorph):
            amorph.append(p)
    amorph_arr = np.array(amorph)
    crystal_at = np.array([-2.9, -1.6, 0])
    glass_at = np.array([2.0, -1.6, 0])

    def network(points: np.ndarray, at: np.ndarray, color: str, jiggle: float) -> VGroup:
        phase = np.random.default_rng(cfg.SEED + len(points)).uniform(0, 2 * np.pi, points.shape)
        rest = np.linalg.norm(points[:, None] - points[None], axis=-1)
        pairs = list(zip(*np.nonzero(np.triu(rest < 0.68, 1))))          # bonds fixed at rest: a locked network
        bonds = VGroup(*[Line(ORIGIN, RIGHT, stroke_color=color, stroke_width=3, stroke_opacity=0.55) for _ in pairs])
        atoms = VGroup(*[Dot(ORIGIN, radius=0.085, color=mu.mix(color, cfg.WHITE, 0.4)) for _ in points])
        group = VGroup(bonds, atoms)

        def draw(clock: float) -> None:
            p = points + jiggle * np.sin(7.0 * clock + phase) * np.array([1, 1, 0]) + at
            for line, (a, b) in zip(bonds, pairs):
                line.put_start_and_end_on(p[a], p[b])
            for dot, q in zip(atoms, p):
                dot.move_to(q)

        return ticking(group, draw)

    crystal = network(lattice(), crystal_at, cfg.CYAN, 0.025)
    glass = network(amorph_arr, glass_at, cfg.GLASS, 0.025)
    c_tag = txt("crystal: ordered", cfg.FONT["small"], cfg.CYAN).next_to(crystal_at + np.array([1.5, 2.6, 0]), UP, buff=0.1)
    g_tag = txt("glass: disordered", cfg.FONT["small"], cfg.GLASS).next_to(glass_at + np.array([1.5, 2.6, 0]), UP, buff=0.1)
    at_word(scene, t, 5, "amorphous", lead=0.3)
    amorphous = result_label("amorphous solid", cfg.GOLD, cfg.FONT["section"]).move_to([1.6, 2.2, 0])
    scene.play(FadeIn(amorphous, shift=DOWN * 0.1), FadeIn(glass), FadeIn(g_tag), run_time=1.2)
    scene.play(FadeIn(crystal), FadeIn(c_tag), run_time=1.0)
    at_word(scene, t, 5, "locked", lead=0.3)
    locked = txt("atoms vibrate, locked in place", cfg.FONT["small"], cfg.WHITE).move_to([2.0, -2.9, 0])
    play_in(scene, t, 6, FadeIn(locked, shift=UP * 0.1), run_time=1.0)

    # --- 6. No measurable flow, even over centuries; uneven panes came from manufacture ------------------------------------------------
    beat(scene, t, 6)
    centuries = txt("centuries: no measurable flow", cfg.FONT["label"], cfg.GREEN).move_to([0.2, -3.6, 0])
    scene.play(FadeIn(centuries, shift=UP * 0.1), run_time=1.0)
    at_word(scene, t, 6, "made", lead=0.4)
    thick_top = Polygon([-6.2, 2.2, 0], [-5.25, 2.2, 0], [-5.55, -2.3, 0], [-5.9, -2.3, 0], stroke_color=cfg.GLASS,
                        stroke_width=3, fill_color=cfg.GLASS, fill_opacity=0.25)
    made = VGroup(txt("some thicker at the top:", cfg.FONT["small"], cfg.GOLD), txt("uneven from manufacture", cfg.FONT["small"], cfg.GOLD))
    made.arrange(DOWN, buff=0.08)
    made.move_to([-7.4 + made.width / 2, 3.0, 0])
    scene.play(fade_through(myth, made), Transform(pane, thick_top), run_time=1.2)
    finish(scene, t, fill=lambda s: [Indicate(made, color=cfg.WHITE, scale_factor=1.04)])
