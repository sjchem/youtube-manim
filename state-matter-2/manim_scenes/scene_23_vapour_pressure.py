"""Scene 23 — A liquid never rests. A large glass vessel on a slowly turning 3D
stage holds a deep-blue pool whose molecules jitter in place. One surface
molecule (gold) keeps hopping up and is pulled back by its neighbours (a green
arrow): attraction. An inset of the Maxwell-Boltzmann speed distribution
lights up its fast tail (orange) — the few molecules with enough energy to
escape — and the followed molecule breaks free with a gold flash; others
follow out of the open top: evaporation.

A glass lid seals the vessel and ``FluxExchange`` (a ``VapourExchange`` with
flux-weighted escape velocities and collisional re-thermalising) runs
molecule by molecule: gold flashes as molecules leave, cyan vapour building
above, blue flashes as vapour molecules strike the surface and are
captured. Two live rate bars (evaporation gold, condensation blue, each the
count over the last three seconds) and a strip chart of the vapour pressure
(teal, the model's n/V x T, smoothed) show condensation rising to meet
evaporation while the pressure levels off: a dynamic equilibrium, with
flashes still going both ways. The lid is then pushed down to make the
container smaller: the pressure spikes, the extra vapour condenses (a burst
of blue flashes) and the trace returns to the same dashed plateau — the
saturated vapour pressure does not depend on the container. The heater
glows: the speed inset warms and its escaping tail grows, the evaporation
bar jumps, condensation catches up and the trace settles on a higher
plateau. Finally two small sealed vessels at the same temperature compare a
liquid with weaker cohesion (short green pulls, many escapes, more vapour)
and one with stronger cohesion (long green pulls, fewer escapes): the teal
vapour-pressure bars differ.
"""

from manim_scenes.common import *
from manim_scenes.kit_f import Escapes, FluxExchange, GlassLid, sink_heater

M_WATER = pm.MOLAR_MASS["H2O"]
T_LIQ = 298.0                                  # K: the liquid at room temperature
T_WARM = 370.0                                 # K: after the heater has warmed it
U_MAX = 1700.0                                 # m/s, speed axis of the inset
U_ESC = 2.0 * pm.u_mp(T_LIQ, M_WATER)          # schematic escape threshold (twice the most probable speed)

BOX_START, BOX_AT = (-0.2, -0.45, 0.0), (-3.75, -0.4, 0.0)
HEIGHT, SMALL_HEIGHT, LEVEL = 3.0, 2.1, 0.9    # vessel height, after the squeeze, pool depth (stage units)
COUNT = 150
SPEED = 2.3
RATE, CAPTURE = 14.0, 1.0                      # escapes per second; capture probability per surface hit
WARM_RATE = 2 * RATE                           # the hotter tail holds about twice as many escapers
WARM_HEAT = float(np.sqrt(T_WARM / T_LIQ))     # cloud speed scale sqrt(T / T_ref)

BAR_X, BAR_LEN, BAR_TOP = 3.05, 3.85, 32.0     # rate bars: left end, full length, rate at full length
ROW_EVAP, ROW_COND = 1.3, 0.6
CHART_T, CHART_P = 54.0, 2.8                   # chart: seconds after sealing, relative vapour pressure

WEAK_RATE, STRONG_RATE = 16.0, 5.0             # final comparison: escapes per second, same temperature


class Scene23VapourPressure(Scene):
    def construct(self) -> None:
        play_scene(self)


def parabola(a: float) -> float:
    """A hop under a constant pull: up and back down."""
    return 4 * a * (1 - a)


def breakaway(a: float) -> float:
    """Slowed at first by the pull of the liquid, then coasting free."""
    return 0.62 * a + 0.38 * (1 - (1 - a) ** 3)


def speed_inset(at, x_length: float, y_length: float, temp: Knob, tail: Knob) -> VGroup:
    """The Maxwell-Boltzmann speed curve of the liquid's molecules with its fast tail (beyond U_ESC) lit."""
    axes = speed_axes(U_MAX, 1.85, at=at, x_length=x_length, y_length=y_length)

    def tail_area() -> VMobject:
        if tail.value < 0.01:
            return VMobject()
        us = np.linspace(U_ESC, U_MAX, 40)
        ys = pm.mb_pdf(us, temp.value, M_WATER) * PDF_SCALE
        return Polygon(axes.c2p(U_ESC, 0), *[axes.c2p(u, y) for u, y in zip(us, ys)], axes.c2p(U_MAX, 0),
                       stroke_width=0, fill_color=cfg.FAST, fill_opacity=0.85 * tail.value)

    area = live(VMobject(), tail_area)
    curve = live(VGroup(), lambda: mb_curve(axes, temp.value, M_WATER, cfg.GOLD, u_max=U_MAX, fill_opacity=0.1))
    top = axes.c2p(U_ESC, 1.25)
    gate = dashed_path(axes.c2p(U_ESC, 0), top, cfg.GOLD, width=3, opacity=0.9)
    group = VGroup(axes, area, curve, gate)
    group.axes, group.area, group.curve, group.gate = axes, area, curve, gate
    return group


def rate_bar(value: Callable[[], float], y: float, color: str) -> Rectangle:
    """A horizontal bar from BAR_X whose length follows a smoothed rate."""
    bar = Rectangle(width=0.05, height=0.36, stroke_color=mu.mix(color, cfg.WHITE, 0.3), stroke_width=2,
                    fill_color=color, fill_opacity=0.85)
    bar.move_to([BAR_X, y, 0], aligned_edge=LEFT)

    def fit(m):
        w = float(np.clip(value() / BAR_TOP, 0.0, 1.0)) * BAR_LEN
        m.stretch_to_fit_width(max(w, 0.04)).move_to([BAR_X, y, 0], aligned_edge=LEFT)

    bar.add_updater(fit)
    return bar


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "23", TITLES["23"])

    # --- 1. Liquid molecules attract one another: a surface molecule is pulled back ----------------------------
    box = TwoPhaseBox(BOX_START, lid="open", count=COUNT, active=0, level=LEVEL, half_x=1.7, half_z=1.15,
                      height=HEIGHT, floor=-1.5, heater=True, zoom=1.42, yaw=-0.7, pitch=0.32, speed=SPEED,
                      liquid_spacing=0.24)
    stage, ch = box.stage, box.chamber
    sink_heater(box)
    hops = Escapes(box, rate=5.0, fast=0.0)
    hop = Knob(0.0)
    x0, z0 = ch.cx + 0.35, ch.cz + 0.45

    def star_point() -> np.ndarray:
        return np.array([x0, box.surface_y() + 0.1 + hop.value, z0])

    star = Ball(star_point, 0.12, cfg.FOLLOWED)
    glow = Halo(star, cfg.FOLLOWED, reach=2.6)
    stage.add_body(glow, star)
    pull = Vector(lambda: star_point() + np.array([0.0, -0.14, 0.0]),
                  lambda: star_point() + np.array([0.0, -0.66, 0.0]), cfg.ATTRACT, width=0.075, tip=0.22)
    pull.presence = 0.0
    pull_tag = Tag(chip("attraction", cfg.ATTRACT, cfg.FONT["small"]), lambda: star_point(), (1.75, -0.42, 0.0))
    pull_tag.presence = 0.0
    ask_path = Curve(lambda: np.array([[x0, box.surface_y() + 0.45, z0], [x0, ch.top() + 0.45, z0]]), cfg.GOLD,
                     width=3.5, dashed=True, glow=False)
    ask_path.presence = 0.0
    ask = Tag(txt("?", cfg.FONT["title"], cfg.GOLD), lambda: np.array([x0, ch.top() + 0.8, z0]))
    ask.presence = 0.0
    stage.add_body(ask_path)
    stage.add_overlay(pull, pull_tag, ask)
    show(scene, stage, 1.2)
    scene.play(hop.to(stage, 0.34, rate_func=parabola), stage.fade(pull, 1.0, run_time=0.5), run_time=1.1)
    scene.play(hop.to(stage, 0.3, rate_func=parabola), stage.fade(pull_tag, 1.0), run_time=1.1)
    scene.play(hop.to(stage, 0.36, rate_func=parabola), stage.fade(ask_path, 1.0), stage.fade(ask, 1.0),
               run_time=1.1)
    while time_left(scene, t, 1) > 1.25:
        scene.play(hop.to(stage, 0.32, rate_func=parabola), *stage.turn(yaw=stage.yaw + 0.03), run_time=1.1)

    # --- 2. The speed distribution: a few have enough energy to break free. Evaporation -----------------------------------
    beat(scene, t, 1)
    temp, tail = Knob(T_LIQ), Knob(0.0)
    inset = speed_inset([3.35, 0.2, 0], 5.4, 3.5, temp, tail)
    scene.play(stage.fade(ask, 0.0), stage.fade(ask_path, 0.0), stage.glide(BOX_AT), stage.zoom_to(1.28),
               hop.to(stage, 0.3, rate_func=parabola), run_time=1.6)
    scene.play(FadeIn(inset.axes), Create(inset.curve), hop.to(stage, 0.32, rate_func=parabola), run_time=1.3)
    scene.add(inset.area)
    scene.play(hop.to(stage, 0.34, rate_func=parabola), *stage.turn(yaw=-0.62), run_time=1.2)
    scene.play(hop.to(stage, 0.28, rate_func=parabola), Indicate(inset.curve, color=cfg.WHITE, scale_factor=1.0),
               run_time=1.2)
    enough = VGroup(txt("enough energy", cfg.FONT["small"], cfg.FAST), txt("to escape", cfg.FONT["small"], cfg.FAST))
    enough.arrange(DOWN, buff=0.1).move_to(inset.axes.c2p(1380, 0.95))
    pointer = Arrow(enough.get_bottom() + DOWN * 0.05, inset.axes.c2p(1220, 0.12), buff=0.05, color=cfg.FAST,
                    stroke_width=4, max_tip_length_to_length_ratio=0.25)
    scene.play(Create(inset.gate), tail.to(stage, 1.0), FadeIn(enough, shift=DOWN * 0.1), GrowArrow(pointer),
               run_time=1.3)
    # The followed molecule is one of the fast few: it breaks free.
    rim = ch.top() + 1.1 - box.surface_y()
    flashed = {"done": False}

    def flash_when_free() -> None:
        if not flashed["done"] and hop.value > hops.layer:
            flashed["done"] = True
            box.up_flashes.spark(np.array([x0, box.surface_y() + hops.layer, z0]), 1)

    stage.bodies.insert(0, Ticker(flash_when_free))
    hops.fast = 0.3
    scene.play(hop.to(stage, rim, rate_func=breakaway), stage.fade(pull, 0.0, run_time=0.5),
               stage.fade(pull_tag, 0.0, run_time=0.6), run_time=2.4)
    scene.play(stage.fade(star, 0.0), stage.fade(glow, 0.0), hops.tween_rate(9.0), run_time=0.8)
    model_note = txt("schematic escape model", cfg.FONT["tiny"], cfg.MUTED).move_to([3.35, 2.65, 0])
    scene.play(FadeIn(model_note), run_time=0.5)
    word = result_label("evaporation", cfg.EVAPORATE, cfg.FONT["section"]).move_to([-3.75, 3.3, 0])
    scene.play(FadeIn(word, shift=UP * 0.15), *stage.turn(yaw=-0.55), run_time=1.0)
    play_in(scene, t, 2, *stage.turn(yaw=-0.5), run_time=time_left(scene, t, 2) - 0.05)

    # --- 3. Seal the container: vapour builds up -------------------------------------------------------------------------
    beat(scene, t, 2)
    lid = GlassLid(box, lift=1.3)
    scene.play(FadeOut(VGroup(inset.axes, inset.gate, enough, pointer, word, model_note)), FadeOut(inset.area),
               FadeOut(inset.curve), hops.tween_rate(0.0), *lid.lower(run_time=1.2, rate_func=rush_into), run_time=1.2)
    for m in (inset.area, inset.curve):
        m.clear_updaters()
    ex = FluxExchange(box, RATE, CAPTURE)
    v_ref = box.region.volume()
    p_ref = ex.plateau() / v_ref
    sealed_at = stage.clock
    state = {"p": 0.0, "evap": 0.0, "cond": 0.0, "last": stage.clock}
    samples: list[tuple[float, float]] = [(0.0, 0.0)]

    def pressure_now() -> float:
        return box.vapour_count() / box.region.volume() * box.cloud.heat ** 2 / p_ref

    def track() -> None:
        now = stage.clock
        dt = now - state["last"]
        state["last"] = now
        if dt <= 0:
            return
        up, down = ex.rates(3.0)
        k = 1 - np.exp(-dt / 0.7)
        state["p"] += (pressure_now() - state["p"]) * k
        state["evap"] += (up - state["evap"]) * (1 - np.exp(-dt / 0.5))
        state["cond"] += (down - state["cond"]) * (1 - np.exp(-dt / 0.5))
        clock = now - sealed_at
        if clock - samples[-1][0] >= 0.1 and clock <= CHART_T:
            samples.append((clock, state["p"]))

    stage.bodies.insert(0, Ticker(track))
    chart = plot_axes((0, CHART_T), (0, CHART_P), x_length=5.6, y_length=2.75, at=[3.95, -2.15, 0], x_label="t",
                      y_label="P")
    chart.labels.remove(chart.labels[1])
    p_title = txt("vapour pressure", cfg.FONT["small"], cfg.PRESSURE)
    p_title.next_to(chart.c2p(0, CHART_P), UP, buff=0.22).align_to(chart.c2p(0, 0), LEFT).shift(LEFT * 0.1)

    def trace() -> VMobject:
        if len(samples) < 2:
            return VMobject()
        return polyline([chart.c2p(a, b) for a, b in samples], cfg.PRESSURE, width=5)

    path = live(VMobject(), trace)
    head_dot = live(VGroup(), lambda: glow_dot(chart.c2p(*samples[-1]), cfg.PRESSURE, radius=0.08))
    evap_name = txt("evaporation", cfg.FONT["small"], cfg.EVAPORATE)
    evap_name.move_to([BAR_X - 0.22, ROW_EVAP, 0], aligned_edge=RIGHT)
    evap_bar = rate_bar(lambda: state["evap"], ROW_EVAP, cfg.EVAPORATE)
    base_line = Line([BAR_X, ROW_COND - 0.32, 0], [BAR_X, ROW_EVAP + 0.32, 0], stroke_color=cfg.MUTED, stroke_width=3)
    scene.play(FadeIn(chart), FadeIn(p_title), FadeIn(evap_name, shift=LEFT * 0.1), Create(base_line),
               *stage.turn(yaw=-0.45), run_time=1.2)
    scene.add(evap_bar, path, head_dot)
    play_in(scene, t, 3, *stage.turn(yaw=-0.38), run_time=time_left(scene, t, 3) - 0.05)

    # --- 4. Condensation: the more vapour, the faster it condenses -----------------------------------------------------------
    beat(scene, t, 3)
    cond_name = txt("condensation", cfg.FONT["small"], cfg.CONDENSE)
    cond_name.move_to([BAR_X - 0.22, ROW_COND, 0], aligned_edge=RIGHT)
    cond_bar = rate_bar(lambda: state["cond"], ROW_COND, cfg.CONDENSE)
    scene.play(FadeIn(cond_name, shift=LEFT * 0.1), set_attr(stage, box.down_flashes, "size", 1.5), run_time=1.0)
    scene.add(cond_bar)
    scene.play(Indicate(cond_name, color=cfg.WHITE, scale_factor=1.06), *stage.turn(yaw=-0.3), run_time=1.4)
    scene.play(*stage.turn(yaw=-0.2, rate_func=linear), run_time=3.2)
    scene.play(Circumscribe(VGroup(cond_name, cond_bar), color=cfg.CONDENSE, buff=0.12), run_time=1.6)
    play_in(scene, t, 4, *stage.turn(yaw=-0.14), set_attr(stage, box.down_flashes, "size", 0.9),
            run_time=time_left(scene, t, 4) - 0.05)

    # --- 5. The rates become equal: dynamic equilibrium ---------------------------------------------------------------------
    beat(scene, t, 4)
    level = BAR_X + RATE / BAR_TOP * BAR_LEN
    equal = dashed_path([level, ROW_COND - 0.3, 0], [level, ROW_EVAP + 0.3, 0], cfg.WHITE, width=3, opacity=0.9)
    scene.play(Create(equal), *stage.turn(yaw=-0.08), run_time=1.0)
    scene.play(Indicate(evap_bar, color=cfg.WHITE, scale_factor=1.0), Indicate(cond_bar, color=cfg.WHITE,
                                                                                  scale_factor=1.0), run_time=1.2)
    # Molecules still leave and still return: every flash swells for a moment.
    scene.play(set_attr(stage, box.up_flashes, "size", 1.8), set_attr(stage, box.down_flashes, "size", 1.8),
               *stage.turn(yaw=0.0), run_time=1.4)
    scene.play(set_attr(stage, box.up_flashes, "size", 0.9), set_attr(stage, box.down_flashes, "size", 0.9),
               *stage.turn(yaw=0.04), run_time=1.4)
    # ... but the amount of vapour stops changing.
    now = samples[-1][0]
    span = Rectangle(width=chart.c2p(10, 0)[0] - chart.c2p(0, 0)[0], height=0.7).move_to(
        chart.c2p(now - 5.0, samples[-1][1]))
    scene.play(Circumscribe(span, color=cfg.PRESSURE, buff=0.05), *stage.turn(yaw=0.08), run_time=1.6)
    scene.play(*stage.turn(yaw=0.1), run_time=max(time_left(scene, t, 5) - 4.6, 0.3))
    both = VGroup(eq(r"\rightleftharpoons", cfg.FONT["section"], cfg.GOLD),
                  txt("dynamic equilibrium", cfg.FONT["section"], cfg.GOLD)).arrange(RIGHT, buff=0.3)
    fit_width(both, 6.2)
    both.move_to([3.9, 2.55, 0])
    scene.play(FadeIn(both, scale=0.94), *stage.turn(yaw=0.13), run_time=1.0)
    play_in(scene, t, 5, *stage.turn(yaw=0.18), run_time=time_left(scene, t, 5) - 0.05)

    # --- 6. The saturated vapour pressure: not the size of the container -------------------------------------------------------
    beat(scene, t, 5)
    recent = [p for c, p in samples if c > samples[-1][0] - 10.0] or [state["p"]]
    plateau = float(np.mean(recent))
    flat = DashedLine(chart.c2p(0, plateau), chart.c2p(CHART_T, plateau), stroke_color=cfg.PRESSURE, stroke_width=3,
                      dash_length=0.12, stroke_opacity=0.8)
    sat_title = txt("saturated vapour pressure", cfg.FONT["small"], cfg.PRESSURE).move_to(p_title, aligned_edge=LEFT)
    scene.play(Create(flat), fade_through(p_title, sat_title), FadeOut(both), run_time=1.4)
    scene.play(Indicate(sat_title, color=cfg.WHITE, scale_factor=1.05), *stage.turn(yaw=0.22), run_time=1.6)
    scene.play(*stage.turn(yaw=0.26), run_time=2.6)
    smaller = chip("smaller container", cfg.VOLUME, cfg.FONT["small"]).move_to([-3.75, 2.9, 0])
    scene.play(box.height_to(SMALL_HEIGHT, run_time=1.6, rate_func=smooth), FadeIn(smaller, shift=DOWN * 0.1),
               run_time=1.6)
    scene.play(*stage.turn(yaw=0.32, rate_func=linear), run_time=4.6)
    same = check_mark(0.24).next_to(sat_title, RIGHT, buff=0.25)
    scene.play(Create(same), Indicate(flat, color=cfg.WHITE, scale_factor=1.0), run_time=1.0)
    play_in(scene, t, 6, *stage.turn(yaw=0.34), run_time=time_left(scene, t, 6) - 0.05)

    # --- 7. Warm the liquid: more can escape, the vapour pressure rises -------------------------------------------------------
    beat(scene, t, 6)
    temp.value, tail.value = T_LIQ, 1.0
    small_inset = speed_inset([-4.0, 2.2, 0], 4.4, 1.7, temp, tail)
    scene.play(FadeOut(smaller), FadeOut(same), *box.heater_on(1.0, run_time=1.2),
               FadeIn(small_inset.axes), FadeIn(small_inset.gate), FadeIn(small_inset.area), FadeIn(small_inset.curve),
               run_time=1.2)
    scene.play(temp.to(stage, T_WARM, run_time=3.0), box.cloud.tween("heat", WARM_HEAT, run_time=3.0),
               box.cloud.tween("warmth", 0.3, run_time=3.0), ex.tween_rate(WARM_RATE, run_time=3.0),
               *stage.turn(yaw=0.42), run_time=3.0)
    rise = Arrow(chart.c2p(CHART_T + 1.0, plateau), chart.c2p(CHART_T + 1.0, plateau * 1.95), buff=0,
                 color=cfg.TEMPERATURE, stroke_width=6, max_tip_length_to_length_ratio=0.3)
    scene.play(GrowArrow(rise), *stage.turn(yaw=0.48), run_time=1.2)
    play_in(scene, t, 7, *stage.turn(yaw=0.6, rate_func=linear), run_time=time_left(scene, t, 7) - 0.05)

    # --- 8. Stronger cohesion, lower vapour pressure ---------------------------------------------------------------------------
    beat(scene, t, 7)
    for m in (evap_bar, cond_bar, path, head_dot, small_inset.area, small_inset.curve):
        m.clear_updaters()
    hide(scene, stage, 0.9, FadeOut(VGroup(chart, flat, sat_title, path, head_dot, evap_name, cond_name, evap_bar,
                                           cond_bar, base_line, equal, rise, small_inset)))
    pair = []
    for k, (x, rate, pull_len, name) in enumerate(((-3.6, WEAK_RATE, 0.32, "weaker cohesion"),
                                                     (3.6, STRONG_RATE, 0.75, "stronger cohesion"))):
        b = TwoPhaseBox((x, -0.2, 0), lid="glass", count=90, active=0, level=0.75, half_x=1.3, half_z=0.95,
                        height=2.4, floor=-1.2, zoom=1.28, yaw=-0.55 + 0.2 * k, pitch=0.34, speed=SPEED,
                        liquid_spacing=0.22, seed=cfg.SEED + 40 * (k + 1))
        e = FluxExchange(b, rate, CAPTURE, seed=cfg.SEED + 41 * (k + 1))
        e.fill(int(round(e.plateau())))
        bch = b.chamber
        arrows = []
        for fx_, fz_ in ((-0.55, 0.45), (0.05, -0.1), (0.6, 0.5)):
            px, pz = bch.cx + fx_ * bch.half_x, bch.cz + fz_ * bch.half_z
            arrows.append(Vector(lambda px=px, pz=pz, b=b: np.array([px, b.surface_y() + 0.12, pz]),
                                 lambda px=px, pz=pz, b=b, L=pull_len: np.array([px, b.surface_y() + 0.12 - L, pz]),
                                 cfg.ATTRACT, width=0.07 + 0.05 * k, tip=0.18 + 0.08 * k))
        b.stage.add_overlay(*arrows)
        level_now = Knob(e.plateau() / b.region.volume())
        ref = 50.0 / (2 * 1.3 * 2 * 0.95 * 1.65)

        def follow(m, dt, b=b, level_now=level_now):
            level_now.value += (b.vapour_count() / b.region.volume() - level_now.value) * (1 - np.exp(-dt / 0.6))
            m.stretch_to_fit_width(max(2.6 * level_now.value / ref, 0.05)).move_to([b.stage.anchor.get_x() - 1.0,
                                                                                    -3.35, 0], aligned_edge=LEFT)

        bar = Rectangle(width=0.1, height=0.38, stroke_width=2, stroke_color=mu.mix(cfg.PRESSURE, cfg.WHITE, 0.3),
                        fill_color=cfg.PRESSURE, fill_opacity=0.85)
        bar.add_updater(follow)
        follow(bar, 0.0)
        sym = eq(r"P_{\text{vap}}", cfg.FONT["label"], cfg.PRESSURE).move_to([x - 1.55, -3.35, 0])
        title = txt(name, cfg.FONT["label"], cfg.ATTRACT).move_to([x, 2.95, 0])
        pair.append(SimpleNamespace(box=b, ex=e, bar=bar, sym=sym, title=title))
    same_t = chip("same T", cfg.TEMPERATURE, cfg.FONT["small"]).move_to([0, 2.95, 0])
    for p in pair:
        p.box.stage.presence = 0.0
        p.box.stage.refresh()
        scene.add(p.box.stage)
    scene.play(*[p.box.stage.fade(p.box.stage, 1.0) for p in pair], *[FadeIn(p.title, shift=DOWN * 0.1) for p in pair],
               FadeIn(same_t), run_time=1.2)
    scene.play(*[FadeIn(VGroup(p.sym, p.bar)) for p in pair], run_time=0.8)
    for p in pair:
        scene.remove(p.bar)
        scene.add(p.bar)
    scene.play(*pair[0].box.stage.turn(yaw=-0.45), *pair[1].box.stage.turn(yaw=-0.25), run_time=2.4)
    scene.play(Indicate(pair[1].bar, color=cfg.WHITE, scale_factor=1.0), Indicate(pair[1].title, color=cfg.WHITE,
                                                                                   scale_factor=1.05), run_time=1.4)
    finish(scene, t, pair[0].box.stage, fill=lambda s: pair[1].box.stage.turn(yaw=-0.15))
