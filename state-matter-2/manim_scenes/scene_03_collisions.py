"""Scene 03 — collisions trade energy. The quietly wrong picture first: a glass
box of cyan molecules that all move at one speed, their gold velocity arrows
lined up beside the box, every one the same length. Then two identical
molecules (numbered cyan balls on a tilted 3D stage) approach with equal gold
velocity arrows and collide elastically off-centre (``pm.COLLISION``): an
orange flash at contact and the dashed line of centres, along which they swap
their velocity components. Beside them, kinetic-energy bars K1, K2 and their
total: the two bars change, the total does not (green check), and the
momentum triangle p1 + p2 morphs into p1' + p2' around the same orange total.
Faint ghost arrows of the old length show one molecule leaving faster (1.23)
and the other slower (0.70), and gold energy flows from one bar to the other.
Then a box of real-size hard spheres (``pm.HardSphereGas``): one gold molecule
is followed, every collision flashes, and a live strip chart of its speed
jumps again and again. Finally the chart gives way to a faint histogram
silhouette with a question mark: what does the whole crowd look like?
"""

from manim_scenes.common import *

C = pm.COLLISION
R_BALL = 0.42
ARROW = 1.05                       # stage units of arrow per unit speed
TAU_START, TAU_END = -2.35, 2.0   # collision clock: contact at tau = 0
N_HS = 56
HS_RADIUS = 0.15
HS_FOLLOW = 0


class Scene03Collisions(Scene):
    def construct(self) -> None:
        play_scene(self)


def _v3(v) -> np.ndarray:
    return np.array([float(v[0]), float(v[1]), 0.0])


NORMAL = _v3(C.normal)
BEFORE = [_v3(v) for v in C.before]
AFTER = [_v3(v) for v in C.after]
CONTACT = [-R_BALL * NORMAL, R_BALL * NORMAL]
K_AFTER = [float(np.dot(w, w)) for w in AFTER]          # kinetic energy relative to the start (1 each)


def ball_point(k: int, tau: float) -> np.ndarray:
    v = BEFORE[k] if tau < 0 else AFTER[k]
    return CONTACT[k] + v * tau


def ball_velocity(k: int, tau: float) -> np.ndarray:
    return BEFORE[k] if tau < 0 else AFTER[k]


def ball_path(k: int, tau: float) -> np.ndarray:
    """Points along the travelled path, sampled finely so the dashes stay even."""
    def run(p, q):
        n = max(int(np.linalg.norm(q - p) / 0.14), 1)
        return [p + (q - p) * i / n for i in range(n + 1)]
    if tau <= 0:
        return np.array(run(ball_point(k, TAU_START), ball_point(k, tau)))
    return np.array(run(ball_point(k, TAU_START), CONTACT[k]) + run(CONTACT[k], ball_point(k, tau))[1:])


def equal_speed_gas(count: int, seed: int) -> pm.IdealGas:
    """The wrong picture: every molecule at the rms speed, in a random direction."""
    gas = pm.IdealGas(count, seed)
    gas.u /= np.linalg.norm(gas.u, axis=1, keepdims=True)
    return gas


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "03", TITLES["03"])

    # --- 0. The quietly wrong picture: one speed for every molecule ------------------------------------------------
    box = GasBox((-3.7, -0.75, 0), count=36, model=equal_speed_gas(36, cfg.SEED + 303), half_x=1.5, half_z=1.1,
                 height=2.7, floor=-1.35, zoom=1.08, yaw=-0.5, pitch=0.3, speed=1.1)
    box.cloud.spark = 0.6
    shown = list(range(0, 36, 4))
    arrows = []
    for i in shown:
        a = Vector(lambda i=i: box.cloud.position(i),
                   lambda i=i: box.cloud.position(i) + box.gas.u[i] * 0.62, cfg.VELOCITY, width=0.05, tip=0.16)
        a.presence = 0.0
        arrows.append(a)
    box.stage.add_overlay(*arrows)
    show(scene, box.stage, 1.0)
    scene.play(*[box.stage.fade(a, 1.0) for a in arrows], *box.stage.turn(yaw=-0.42), run_time=1.4)
    lineup = VGroup(*[VecArrow([2.1, y, 0], [4.3, y, 0], cfg.VELOCITY, width=0.09, tip_len=0.28, live=False)
                      for y in np.linspace(1.75, -1.75, len(shown))])
    ruler = dashed_path([4.3, 2.15, 0], [4.3, -2.15, 0], cfg.WHITE, width=3, opacity=0.8)
    same = txt("same speed for all?", cfg.FONT["body"], cfg.WHITE).move_to([3.9, 2.85, 0])
    scene.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.3) for a in lineup], lag_ratio=0.12), run_time=1.8)
    scene.play(Create(ruler), FadeIn(same, shift=DOWN * 0.1), run_time=1.1)
    wrong = txt("not real", cfg.FONT["label"], cfg.WARNING)
    cross = cross_mark(0.22)
    verdict = VGroup(cross, wrong).arrange(RIGHT, buff=0.25).move_to([3.3, -2.75, 0])
    scene.play(*box.stage.turn(yaw=-0.25), run_time=2.4)
    scene.play(FadeIn(verdict, shift=UP * 0.1), Indicate(ruler, color=cfg.WARNING, scale_factor=1.0), run_time=1.2)
    scene.play(*box.stage.turn(yaw=-0.15), run_time=time_left(scene, t, 1) - 0.05)

    # --- 1. Two identical molecules, the same speed ------------------------------------------------------------------
    beat(scene, t, 1)
    tau = Knob(TAU_START)
    stage = Stage((-3.25, 0.05, 0), zoom=0.96, yaw=-0.32, pitch=0.2, sway=0.03)
    plane = Grid((0, 0, -0.55), (1, 0, 0), (0, 1, 0), (-3.4, 3.0), (-3.4, 2.6), step=0.5, major=0, color=cfg.GRID,
                 opacity=0.28, fill=cfg.PANEL, fill_opacity=0.25)
    balls = [Ball(lambda k=k: ball_point(k, tau.value), R_BALL, cfg.MOLECULE, label=str(k + 1)) for k in range(2)]
    trails = [Curve(lambda k=k: ball_path(k, tau.value), cfg.MUTED, width=2.4, glow=False, dashed=True, opacity=0.7)
              for k in range(2)]
    line = Segment(-NORMAL * 1.5, NORMAL * 1.5, cfg.WHITE, width=3, opacity=0.85, dashed=True)
    line.presence = 0.0

    def arrow_ends(k: int, length: float | None = None):
        p = ball_point(k, tau.value)
        v = ball_velocity(k, tau.value)
        d = v / np.linalg.norm(v)
        start_pt = p + d * R_BALL * 0.85
        size = np.linalg.norm(v) if length is None else length
        return start_pt, start_pt + d * size * ARROW

    vecs = [Vector(lambda k=k: arrow_ends(k)[0], lambda k=k: arrow_ends(k)[1], cfg.VELOCITY, width=0.09, tip=0.27)
            for k in range(2)]
    ghosts = [Vector(lambda k=k: arrow_ends(k, 1.0)[0], lambda k=k: arrow_ends(k, 1.0)[1], cfg.WHITE, width=0.05,
                     tip=0.18, glow=False) for k in range(2)]
    for g in ghosts:
        g.presence = 0.0
    stage.add_body(plane, *trails, line, *balls)
    stage.add_overlay(*ghosts, *vecs)

    def speed_tag(k: int, value: float, offset, color: str = cfg.VELOCITY) -> Tag:
        return Tag(txt(fx(value, 2), cfg.FONT["label"], color), lambda k=k: ball_point(k, tau.value), offset)

    tags_before = [speed_tag(0, 1.0, (-0.35, -0.85, 0)), speed_tag(1, 1.0, (0.25, 0.85, 0))]
    stage.add_overlay(*tags_before)
    stage.presence = 0.0
    stage.refresh()
    scene.add(stage)
    scene.play(box.stage.fade(box.stage, 0.0), stage.fade(stage, 1.0), FadeOut(VGroup(lineup, ruler, same, verdict)),
               tau.to(stage, -1.95, run_time=1.0, rate_func=linear), run_time=1.0)
    for member in box.stage.get_family():
        member.clear_updaters()
    scene.remove(box.stage)

    # The right-hand panel: kinetic energy (K1 + K2 = total) and momentum (p1 + p2 = total).
    swap_e, swap_p = Knob(0.0), Knob(0.0)
    base_y, k_unit, xs = 0.15, 1.05, (2.45, 3.65, 5.35)

    def k_values() -> list[float]:
        s = swap_e.value
        k1 = 1 + (K_AFTER[0] - 1) * s
        k2 = 1 + (K_AFTER[1] - 1) * s
        return [k1, k2, k1 + k2]

    bar_colors = (cfg.MOLECULE, cfg.MOLECULE, cfg.GOLD)

    def build_bars() -> VGroup:
        group = VGroup()
        for x, value, color in zip(xs, k_values(), bar_colors):
            h = max(value * k_unit, 0.02)
            group.add(Rectangle(width=0.78, height=h, stroke_color=color, stroke_width=2.5, fill_color=color,
                                fill_opacity=0.55).move_to([x, base_y + h / 2, 0]))
        return group

    bars = live(VGroup(), build_bars)
    baseline = Line([1.85, base_y, 0], [6.0, base_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    names = VGroup(eq("K_1", cfg.FONT["label"], cfg.MOLECULE), eq("K_2", cfg.FONT["label"], cfg.MOLECULE),
                   txt("total", cfg.FONT["small"], cfg.GOLD))
    for name, x in zip(names, xs):
        name.move_to([x, base_y - 0.42, 0])
    signs = VGroup(eq("+", cfg.FONT["section"], cfg.MUTED).move_to([(xs[0] + xs[1]) / 2, base_y + 0.5, 0]),
                   eq("=", cfg.FONT["section"], cfg.MUTED).move_to([(xs[1] + xs[2]) / 2, base_y + 0.5, 0]))
    energy_head = txt("kinetic energy", cfg.FONT["label"], cfg.WHITE).move_to([3.9, 3.15, 0])
    energy = VGroup(baseline, names, signs, energy_head)
    scene.play(Create(baseline), FadeIn(VGroup(names, signs, energy_head)), FadeIn(bars),
               tau.to(stage, -1.3, run_time=1.3, rate_func=linear), run_time=1.3)
    same_speed = chip("identical · same speed", cfg.MOLECULE, cfg.FONT["small"]).move_to([-3.35, 3.0, 0])
    scene.play(FadeIn(same_speed, shift=DOWN * 0.1), Indicate(VGroup(*bars[:2]), color=cfg.WHITE, scale_factor=1.04),
               tau.to(stage, -0.65, run_time=1.4, rate_func=linear), run_time=1.4)
    play_in(scene, t, 2, tau.to(stage, -0.15, run_time=1.6, rate_func=linear), run_time=1.6)

    # --- 2. Contact: an elastic collision; energy and momentum both conserved ----------------------------------------
    beat(scene, t, 2)
    flash_at = stage.screen_point(np.zeros(3))
    scene.play(tau.to(stage, 0.0, run_time=0.3, rate_func=linear), stage.fade(line, 1.0, run_time=0.3),
               FadeOut(same_speed), *[stage.fade(tg, 0.0, run_time=0.3) for tg in tags_before], run_time=0.3)
    scene.play(Flash(flash_at, color=cfg.IMPULSE, line_length=0.35, num_lines=14, flash_radius=0.75),
               swap_e.to(stage, 1.0, run_time=0.9), tau.to(stage, 0.15, run_time=0.9, rate_func=linear), run_time=0.9)
    tags_after = [speed_tag(0, C.speeds_after[0], (-0.95, -0.25, 0), mu.mix(cfg.FAST, cfg.WHITE, 0.15)),
                  speed_tag(1, C.speeds_after[1], (0.95, 0.15, 0), mu.mix(cfg.SLOW, cfg.WHITE, 0.25))]
    for tg in tags_after:
        tg.presence = 0.0
    stage.add_overlay(*tags_after)
    elastic = chip("elastic", cfg.GREEN, cfg.FONT["small"]).move_to([-3.35, 3.0, 0])
    check_e = check_mark(0.24).next_to(names[2], RIGHT, buff=0.3)
    scene.play(FadeIn(elastic, shift=DOWN * 0.1), stage.fade(line, 0.35, run_time=1.2),
               tau.to(stage, 0.35, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(Create(check_e), Indicate(names[2], color=cfg.GREEN, scale_factor=1.15),
               tau.to(stage, 0.5, run_time=1.0, rate_func=linear), run_time=1.0)

    # Momentum: the triangle p1 + p2 morphs into p1' + p2' around one fixed total.
    origin, p_unit = np.array([2.2, -1.5, 0]), 1.45
    p_head = txt("momentum", cfg.FONT["label"], cfg.WHITE).move_to([3.9, -0.85, 0])

    def p_tip1() -> np.ndarray:
        s = swap_p.value
        return origin + (BEFORE[0] + (AFTER[0] - BEFORE[0]) * s) * p_unit

    total_tip = origin + (BEFORE[0] + BEFORE[1]) * p_unit
    p1 = VecArrow(origin, p_tip1, cfg.VELOCITY, width=0.07, tip_len=0.22)
    p2 = VecArrow(p_tip1, total_tip, cfg.VELOCITY, width=0.07, tip_len=0.22)
    p_total = VecArrow(origin, total_tip, cfg.IMPULSE, width=0.09, tip_len=0.22)
    p_names = VGroup(eq(r"p_1 + p_2", cfg.FONT["label"], cfg.VELOCITY),
                     eq(r"= \text{total}", cfg.FONT["label"], cfg.IMPULSE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    p_names.move_to([5.45, -1.95, 0])
    scene.play(FadeIn(p_head), p1.grow_in(run_time=0.8), p2.grow_in(run_time=0.8),
               tau.to(stage, 0.65, run_time=0.8, rate_func=linear), run_time=0.8)
    scene.play(p_total.grow_in(run_time=0.7), FadeIn(p_names), tau.to(stage, 0.8, run_time=0.7, rate_func=linear),
               run_time=0.7)
    scene.play(swap_p.to(stage, 1.0, run_time=1.5), tau.to(stage, 1.0, run_time=1.5, rate_func=linear), run_time=1.5)
    check_p = check_mark(0.24).next_to(p_names, DOWN, buff=0.3)
    play_in(scene, t, 3, Create(check_p), Indicate(p_total, color=cfg.GREEN, scale_factor=1.0),
            tau.to(stage, 1.15, run_time=1.0, rate_func=linear), run_time=1.0)

    # --- 3. But the individual speeds changed: energy passed from one to the other ------------------------------------
    beat(scene, t, 3)
    scene.play(*[stage.fade(tg, 1.0) for tg in tags_after], stage.fade(line, 0.0), FadeOut(elastic),
               tau.to(stage, 1.3, run_time=1.0, rate_func=linear), run_time=1.0)
    faster = txt("faster", cfg.FONT["label"], cfg.FAST)
    slower = txt("slower", cfg.FONT["label"], cfg.SLOW)
    faster_tag = Tag(faster, lambda: ball_point(0, tau.value), (-1.05, -0.95, 0))
    slower_tag = Tag(slower, lambda: ball_point(1, tau.value), (1.05, 0.9, 0))
    for tg in (faster_tag, slower_tag):
        tg.presence = 0.0
    stage.add_overlay(faster_tag, slower_tag)
    scene.play(*[stage.fade(g, 0.55) for g in ghosts], tau.to(stage, 1.45, run_time=1.2, rate_func=linear),
               run_time=1.2)
    scene.play(stage.fade(faster_tag, 1.0), tau.to(stage, 1.58, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(stage.fade(slower_tag, 1.0), tau.to(stage, 1.7, run_time=1.0, rate_func=linear), run_time=1.0)
    # Energy flows from bar 2 to bar 1.
    flow = CurvedArrow(np.array([xs[1], base_y + K_AFTER[1] * k_unit + 0.2, 0]),
                       np.array([xs[0] + 0.1, base_y + K_AFTER[0] * k_unit + 0.25, 0]), angle=0.9,
                       color=cfg.GOLD, stroke_width=6, tip_length=0.24)
    passed = txt("energy passed", cfg.FONT["small"], cfg.GOLD).move_to([0.95, 2.3, 0])
    scene.play(Create(flow), FadeIn(passed, shift=LEFT * 0.1), tau.to(stage, 1.82, run_time=1.4, rate_func=linear),
               run_time=1.4)
    scene.play(Indicate(bars[0], color=cfg.FAST, scale_factor=1.05), Indicate(bars[1], color=cfg.SLOW,
                                                                             scale_factor=1.05),
               tau.to(stage, TAU_END, run_time=1.4, rate_func=linear), run_time=1.4)
    play_in(scene, t, 4, *stage.turn(yaw=-0.12, pitch=0.26), run_time=time_left(scene, t, 4) - 0.1)

    # --- 4. Billions of collisions a second: a followed molecule's speed keeps jumping ---------------------------------
    beat(scene, t, 4)
    bars.clear_updaters()
    hide(scene, stage, 0.8, FadeOut(VGroup(energy, bars, flow, passed, check_e, p_head, p_names, check_p)),
         *[a.fade_to(0.0) for a in (p1, p2, p_total)])
    for a in (p1, p2, p_total):
        a.clear_updaters()
    scene.remove(p1, p2, p_total)
    model = pm.HardSphereGas(N_HS, cfg.SEED + 31, HS_RADIUS, (3.0, 2.7, 2.2))
    gas = GasBox((-3.5, -0.7, 0), count=N_HS, model=model, radius=HS_RADIUS, half_x=1.5, half_z=1.1, height=2.7,
                 floor=-1.35, zoom=1.1, yaw=-0.55, pitch=0.3, speed=1.25, follow=HS_FOLLOW, trail=1.6)
    gas.cloud.spark = 0.0
    sparks = TimedFlashes(cfg.IMPULSE, 1.6)
    gas.stage.add_overlay(sparks)
    history: list[tuple[float, float]] = []
    last = {"u": float(np.linalg.norm(model.u[HS_FOLLOW]))}

    def watch() -> None:
        u = float(np.linalg.norm(model.u[HS_FOLLOW]))
        now = gas.cloud.time
        if abs(u - last["u"]) > 1e-3:
            sparks.spark(gas.cloud.position(HS_FOLLOW).copy(), 2)
            history.append((now, last["u"]))       # a vertical jump in the trace
        last["u"] = u
        history.append((now, u))
        while history and history[0][0] < now - 8.0:
            history.pop(0)

    gas.stage.bodies.append(Ticker(watch))
    show(scene, gas.stage, 0.9)
    window = 6.0
    chart = plot_axes((0, window), (0, 2.6), x_length=5.2, y_length=3.0, at=[3.45, -0.55, 0], x_label=r"\text{time}",
                      y_label=r"\text{speed}", y_color=cfg.VELOCITY)

    def trace() -> VMobject:
        now = gas.cloud.time
        pts = [chart.c2p(np.clip(tt - now + window, 0, window), min(u, 2.55)) for tt, u in history
               if tt >= now - window]
        if len(pts) < 2:
            return VMobject()
        group = VGroup(polyline(pts, cfg.VELOCITY, width=9, opacity=0.15), polyline(pts, cfg.VELOCITY, width=4.5))
        group.add(glow_dot(pts[-1], cfg.VELOCITY, radius=0.08))
        return group

    speed_line = live(VGroup(), trace)
    billions = txt("air: billions of collisions/s", cfg.FONT["label"], cfg.IMPULSE)
    fit_width(billions, 13.0)
    billions.move_to([0, 2.95, 0])
    scene.play(Create(chart), FadeIn(speed_line), run_time=1.2)
    scene.play(FadeIn(billions, shift=DOWN * 0.1), *gas.stage.turn(yaw=-0.4), run_time=1.2)
    play_in(scene, t, 5, *gas.stage.turn(yaw=-0.1), run_time=time_left(scene, t, 5) - 0.05)

    # --- 5. No molecule keeps one speed: so what does the whole crowd look like? ---------------------------------------
    beat(scene, t, 5)
    scene.play(*gas.stage.turn(yaw=0.05), run_time=2.0)
    speed_line.clear_updaters()
    crowd = plot_axes((0, 3.0), (0, 1.1), x_length=5.2, y_length=3.0, at=[3.45, -0.55, 0], x_label=r"\text{speed}",
                      y_label=r"\text{number}", x_color=cfg.VELOCITY)
    edges = np.linspace(0, 2.8, 15)
    shape = pm.maxwell_pdf((edges[:-1] + edges[1:]) / 2)
    ghost = VGroup()
    for a, b, d in zip(edges[:-1], edges[1:], shape):
        corners = [crowd.c2p(a, 0), crowd.c2p(a, d), crowd.c2p(b, d), crowd.c2p(b, 0)]
        ghost.add(VGroup(Polygon(*corners, stroke_width=0, fill_color=cfg.MUTED, fill_opacity=0.1),
                         DashedVMobject(polyline(corners, cfg.MUTED, width=2.5, opacity=0.65), num_dashes=9)))
    mark = txt("?", 120, cfg.GOLD).move_to(crowd.c2p(1.3, 0.62))
    scene.play(FadeOut(VGroup(chart, speed_line)), gas.cloud.tween("follow_alpha", 0.0), run_time=1.0)
    scene.play(Create(crowd), LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in ghost], lag_ratio=0.06),
               *gas.stage.turn(yaw=0.2), run_time=1.8)
    scene.play(FadeIn(mark, scale=0.7), *gas.stage.turn(yaw=0.32), run_time=1.2)
    finish(scene, t, gas.stage, fill=lambda s: [Indicate(mark, color=cfg.WHITE, scale_factor=1.12, run_time=s)])
