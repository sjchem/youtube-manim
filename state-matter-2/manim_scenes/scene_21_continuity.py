"""Scene 21 — around the critical point. The pressure-volume-temperature
surface of a van der Waals fluid with Maxwell's flat coexistence region
(``pm.isotherm``), built as a translucent 3D surface on a slowly turning stage
(logarithmic volume and a compressed log(1 + reduced pressure) scale so the whole fluid fits). Patches are
coloured by phase: liquid deep blue, gas cyan, the coexistence valley
blue-violet, the supercritical region purple. A purple ball marks the critical
point where the two coexistence edges meet.

Two routes from the same gas to the same liquid, each a gold or purple ball
riding on the surface with a glowing trail:

1. squeeze at low temperature (reduced T 0.85): straight through the valley,
   where blue condensation sparks fly — droplets, a surface;
2. heat at constant volume to reduced T 1.4, squeeze, then cool at constant
   volume: it passes above the critical point and never enters the valley
   (every point of it has v below the liquid volume or T above T_c).

The supercritical region then glows, and three chips separate condensation,
the critical point and the supercritical fluid.
"""

from manim_scenes.common import *
from manim_scenes.kit_d import at_word

V_LO, V_HI = 0.47, 4.5
T_LO, T_HI = 0.85, 1.45
V_GAS, V_LIQ = 4.3, 0.5          # start (a gas) and end (a liquid) of both routes
T_COLD, T_HOT = 0.85, 1.4
STAGE_AT = (-1.6, -0.75, 0.0)
CHIP_X = 4.6
# Label colours contrast with the purple surface beneath them.
CRITICAL_LABEL = cfg.GOLD
SUPERCRITICAL_LABEL = cfg.WHITE


class Scene21Continuity(Scene):
    def construct(self) -> None:
        play_scene(self)


def P(v: float, tr: float) -> float:
    return float(pm.isotherm(tr, np.array([v]))[0])


def world(v: float, tr: float, lift: float = 0.0) -> np.ndarray:
    return np.array([2.0 * np.log(v) - 0.75, 1.2 * np.log1p(P(v, tr)) + lift, 1.6 - (tr - T_LO) / (T_HI - T_LO) * 3.2])


def phase_color(v: float, tr: float) -> str:
    if tr >= 1.0:
        return cfg.SUPERCRITICAL if P(v, tr) > 1.0 else cfg.VAPOUR
    _, vl, vg = pm.maxwell(round(tr, 4))
    if v < vl:
        return cfg.LIQUID
    if v > vg:
        return cfg.VAPOUR
    return cfg.COEXIST


def route_two() -> np.ndarray:
    """(v, tr) samples: heat at V_GAS, squeeze at T_HOT, cool at V_LIQ."""
    heat = [(V_GAS, x) for x in np.linspace(T_COLD, T_HOT, 40)]
    squeeze = [(v, T_HOT) for v in np.geomspace(V_GAS, V_LIQ, 70)]
    cool = [(V_LIQ, x) for x in np.linspace(T_HOT, T_COLD, 40)]
    return np.array(heat + squeeze + cool)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "21", TITLES["21"])
    stage = Stage(STAGE_AT, zoom=1.08, yaw=-0.62, pitch=0.4, sway=0.03)

    # --- 0. The P-V-T surface --------------------------------------------------------------------------------------------
    vs = np.geomspace(V_LO, V_HI, 25)
    ts = np.linspace(T_LO, T_HI, 13)
    faces = surface_faces(lambda v, tr: world(v, tr), vs, ts, phase_color, opacity=0.5, edge_opacity=0.12)
    for f in faces:
        f.presence = 0.0
    stage.add_body(*faces)
    lines = [Curve(np.array([world(v, tr) for v in np.geomspace(V_LO, V_HI, 70)]), cfg.WHITE, width=1.4, glow=False, opacity=0.35)
             for tr in ts]
    for c in lines:
        c.presence = 0.0
    stage.add_body(*lines)
    corner = np.array([2.0 * np.log(V_LO) - 0.75, -0.05, 1.6])
    triad = axis_triad(stage, corner, [corner + [5.0, 0, 0], corner + [0, 3.6, 0], corner + [0, 0, -3.6]],
                       [cfg.VOLUME, cfg.PRESSURE, cfg.TEMPERATURE], ["V", "P", "T"], width=3.0, label_size=cfg.FONT["section"],
                       offsets=[(0, 0, 0), (0, 0, 0), (-1.15, 0.35, 0)])
    triad.segments[2].bias = -500.0
    for part in triad.parts:
        part.presence = 0.0
    show(scene, stage, 0.8)
    scene.play(*fade_all(stage, triad.parts, 1.0), run_time=1.0)
    at_word(scene, t, 0, "together", lead=0.3)
    # Keep the shared stage live while its surface patches fade in.
    scene.play(LaggedStart(*[stage.fade(f, 1.0) for f in faces], lag_ratio=0.006,
                           suspend_mobject_updating=False), *fade_all(stage, lines, 1.0),
               stage.turn(yaw=-0.45)[0], run_time=3.4)
    log_note = chip("V: log · P: compressed", cfg.MUTED, cfg.FONT["tiny"])
    fit_width(log_note, 4.6)
    log_note.move_to([-5.2, -3.65, 0])
    at_word(scene, t, 0, "flat", lead=0.3)
    play_in(scene, t, 1, FadeIn(log_note), stage.turn(yaw=-0.5)[0], run_time=1.0)

    # --- 1. A valley where gas and liquid coexist ------------------------------------------------------------------------------
    beat(scene, t, 1)
    ideal_note = txt("same molecules · two routes", cfg.FONT["small"], cfg.MUTED).move_to([CHIP_X, 3.0, 0])
    scene.play(FadeIn(ideal_note, shift=DOWN * 0.1), run_time=0.9)
    at_word(scene, t, 1, "valley", lead=0.3)
    _, vl, vg = pm.maxwell(0.9)
    tag_mix = Tag(txt("gas + liquid", cfg.FONT["label"], cfg.COEXIST), world(np.sqrt(vl * vg), 0.9, 0.25), DOWN * 0.45 + RIGHT * 0.3)
    tag_liq = Tag(txt("liquid", cfg.FONT["label"], cfg.LIQUID_EDGE), world(0.5, T_LO, 0.2), LEFT * 0.75 + DOWN * 0.55)
    tag_gas = Tag(txt("gas", cfg.FONT["label"], cfg.VAPOUR), world(4.2, T_LO, 0.2), DOWN * 0.45 + RIGHT * 0.3)
    for tag in (tag_mix, tag_liq, tag_gas):
        tag.presence = 0.0
    stage.add_overlay(tag_mix, tag_liq, tag_gas)
    scene.play(stage.fade(tag_mix, 1.0), run_time=0.9)
    play_in(scene, t, 2, stage.fade(tag_liq, 1.0), stage.fade(tag_gas, 1.0), run_time=1.0)

    # --- 2. The rim of the valley peaks at the critical point --------------------------------------------------------------------
    beat(scene, t, 2)
    rim_trs = np.linspace(T_LO, 0.995, 30)
    rim_pts = ([world(pm.maxwell(round(x, 4))[1], x, 0.03) for x in rim_trs] + [world(1.0, 1.0, 0.03)] +
               [world(pm.maxwell(round(x, 4))[2], x, 0.03) for x in rim_trs[::-1]])
    rim = Curve(np.array(rim_pts), cfg.WHITE, width=3.2)
    rim.presence = 0.0
    cp = Ball(world(1.0, 1.0, 0.05), 0.14, cfg.CRITICAL, layers=14)
    cp_halo = Halo(cp, cfg.CRITICAL, reach=3.2, peak=0.3)
    cp.presence = cp_halo.presence = 0.0
    cp.bias = cp_halo.bias = 200.0
    cp_tag = Tag(result_label("critical point", CRITICAL_LABEL, cfg.FONT["label"]), world(1.0, 1.0, 0.05), UP * 0.6 + RIGHT * 1.3)
    cp_tag.content.set_stroke(cfg.BG, width=2.4, opacity=1, background=True)
    cp_tag.presence = 0.0
    stage.add_body(rim, cp_halo, cp)
    stage.add_overlay(cp_tag)
    scene.play(stage.fade(rim, 1.0), run_time=1.4)
    at_word(scene, t, 2, "critical", lead=0.3)
    play_in(scene, t, 3, stage.fade(cp, 1.0), stage.fade(cp_halo, 1.0), stage.fade(cp_tag, 1.0), run_time=1.2)

    # --- 3. Route 1: squeeze at low temperature, straight through the valley -------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(ideal_note), stage.fade(tag_mix, 0.0), stage.fade(rim, 0.4), run_time=0.8)
    r1 = Knob(0.0)
    path_1 = np.array([world(v, T_COLD, 0.06) for v in np.geomspace(V_GAS, V_LIQ, 140)])
    vs_1 = np.geomspace(V_GAS, V_LIQ, 140)

    def at_1() -> np.ndarray:
        return path_1[int(round(r1.value * (len(path_1) - 1)))]

    ball_1 = Ball(at_1, 0.13, cfg.GOLD, layers=14)
    trail_1 = Curve(lambda: path_1[: int(round(r1.value * (len(path_1) - 1))) + 1], cfg.GOLD, width=6)
    ball_1.bias = trail_1.bias = 150.0
    drops = TimedFlashes(cfg.CONDENSE, 1.2)
    _, vl_c, vg_c = pm.maxwell(T_COLD)

    def sparkle() -> None:
        k = int(round(r1.value * (len(path_1) - 1)))
        if vl_c < vs_1[k] < vg_c and stage.clock * 7 % 1 < 0.5:
            drops.spark(path_1[k] + np.array([0, 0.05, 0]), 1)

    stage.add_body(Ticker(sparkle), trail_1, ball_1)
    stage.add_overlay(drops)
    label_1 = chip("1  squeeze cold", cfg.GOLD, cfg.FONT["small"]).move_to([CHIP_X, 2.9, 0])
    scene.play(FadeIn(label_1, shift=DOWN * 0.1), run_time=0.8)
    scene.play(r1.to(stage, 0.42, rate_func=smooth), run_time=2.6)
    at_word(scene, t, 3, "Droplets", lead=0.3)
    droplets = txt("droplets · a surface", cfg.FONT["small"], cfg.CONDENSE).next_to(label_1, DOWN, buff=0.25)
    scene.play(r1.to(stage, 0.9, rate_func=linear), FadeIn(droplets, shift=DOWN * 0.1), run_time=3.2)
    play_in(scene, t, 4, r1.to(stage, 1.0, rate_func=smooth), run_time=1.2)

    # --- 4. Route 2: heat, squeeze, cool -----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    r2 = Knob(0.0)
    samples = route_two()
    path_2 = np.array([world(v, tr, 0.08) for v, tr in samples])

    def at_2() -> np.ndarray:
        return path_2[int(round(r2.value * (len(path_2) - 1)))]

    ball_2 = Ball(at_2, 0.13, cfg.CRITICAL, layers=14)
    halo_2 = Halo(ball_2, cfg.CRITICAL, reach=2.6, peak=0.25)
    trail_2 = Curve(lambda: path_2[: int(round(r2.value * (len(path_2) - 1))) + 1], cfg.CRITICAL, width=6)
    ball_2.bias = halo_2.bias = trail_2.bias = 160.0
    stage.add_body(trail_2, halo_2, ball_2)
    label_2 = chip("2  heat · squeeze · cool", cfg.CRITICAL, cfg.FONT["small"]).move_to([CHIP_X, 1.35, 0])
    n_heat, n_squeeze = 40, 70
    total = len(samples) - 1
    scene.play(FadeIn(label_2, shift=DOWN * 0.1), stage.fade(rim, 0.15), run_time=0.7)
    at_word(scene, t, 4, "Heat", lead=0.2)
    scene.play(r2.to(stage, (n_heat - 1) / total, rate_func=smooth), run_time=2.0)
    at_word(scene, t, 4, "Squeeze", lead=0.2)
    scene.play(r2.to(stage, (n_heat + n_squeeze - 1) / total, rate_func=smooth), run_time=2.4)
    at_word(scene, t, 4, "cool", lead=0.2)
    play_in(scene, t, 5, r2.to(stage, 1.0, rate_func=smooth), run_time=2.4)

    # --- 5. The same liquid, without droplets or a surface -------------------------------------------------------------------------
    beat(scene, t, 5)
    same = VGroup(txt("same liquid", cfg.FONT["label"], cfg.WHITE), check_mark(0.24)).arrange(RIGHT, buff=0.2)
    same.next_to(label_2, DOWN, buff=0.3)
    scene.play(FadeIn(same, shift=DOWN * 0.1), Indicate(label_2, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)
    at_word(scene, t, 5, "surface", lead=0.3)
    no_surface = txt("no droplets · no surface", cfg.FONT["small"], cfg.CRITICAL).next_to(same, DOWN, buff=0.32)
    scene.play(FadeIn(no_surface, shift=DOWN * 0.1), run_time=0.9)
    at_word(scene, t, 5, "smoothly", lead=0.3)
    replay = Knob(0.0)
    glint = Ball(lambda: path_2[int(round(replay.value * (len(path_2) - 1)))], 0.09, cfg.WHITE, layers=10)
    glint.bias = 170.0
    stage.add_body(glint)
    play_in(scene, t, 6, replay.to(stage, 1.0, rate_func=linear), run_time=3.2)
    stage.drop(glint)

    # --- 6. Gas and liquid are connected: the supercritical fluid -------------------------------------------------------------------
    beat(scene, t, 6)
    super_faces = [f for f, (i, j) in zip(faces, [(i, j) for i in range(len(vs) - 1) for j in range(len(ts) - 1)])
                   if phase_color((vs[i] + vs[i + 1]) / 2, (ts[j] + ts[j + 1]) / 2) == cfg.SUPERCRITICAL]
    gain = Knob(0.5)

    def brighten() -> None:
        for f in super_faces:
            f.opacity = gain.value
    stage.bodies.insert(0, Ticker(brighten))
    scene.play(gain.to(stage, 0.85, rate_func=there_and_back_with_pause), run_time=2.4)
    at_word(scene, t, 6, "supercritical", lead=0.3)
    sc_tag = Tag(result_label("supercritical fluid", SUPERCRITICAL_LABEL, cfg.FONT["label"]), world(0.75, 1.32, 0.3), UP * 0.5)
    sc_tag.content.set_stroke(cfg.BG, width=2.4, opacity=1, background=True)
    sc_tag.presence = 0.0
    stage.add_overlay(sc_tag)
    scene.play(stage.fade(sc_tag, 1.0), gain.to(stage, 0.72), run_time=1.2)
    at_word(scene, t, 6, "continuously", lead=0.3)
    play_in(scene, t, 7, stage.turn(yaw=-0.36)[0], run_time=2.6)

    # --- 7. Three ideas, kept apart ----------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(label_1, label_2, droplets, same, no_surface)), run_time=0.7)
    ideas = [("condensation", "crosses the boundary", cfg.CONDENSE),
             ("critical point", "the boundary ends", CRITICAL_LABEL),
             ("supercritical fluid", "no boundary to cross", SUPERCRITICAL_LABEL)]
    cards = VGroup()
    for name, what, color in ideas:
        cards.add(on_panel(VGroup(txt(name, cfg.FONT["label"], color), txt(what, cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.12),
                           color, pad=0.22))
    cards.arrange(DOWN, buff=0.28).move_to([CHIP_X + 0.4, 0.4, 0])
    cues = ("Condensation", "critical", "supercritical")
    for k, (card, word) in enumerate(zip(cards, cues)):
        at_word(scene, t, 7, word, nth=1, lead=0.3)
        scene.play(FadeIn(card, shift=LEFT * 0.2), run_time=0.9)
    finish(scene, t, stage, drift=0.12)
