"""Scene 18 — Andrews squeezes carbon dioxide. A big 3D glass cylinder of CO2
with a steel piston (left) and a P-V plot (right) of the 21.5 °C isotherm —
the van der Waals model with Maxwell's flat coexistence line, scaled to CO2 and
labelled "model". The drawn cylinder's height is proportional to the fluid's
volume, and one knob (the reduced volume) drives everything: the piston, the
liquid level (lever rule), the number of vapour molecules, a teal push arrow
on the piston whose length follows the pressure, and a glowing tracer that
draws the isotherm as it goes, coloured by phase. Squeezing the gas raises the
pressure (cyan "gas" branch). At the vapour volume the first drops form (blue
flashes; a marker "first drops"). On the flat stretch the pool rises while
vapour molecules condense: two bars show why — the vapour's crowding stays the
same while the liquid grows. At the liquid volume the last bubble goes; the
piston barely moves while the tracer shoots up the steep "liquid" branch.
Three chips, each with a sketch of its stretch of curve, sum up the three
behaviours, and "same molecules" closes as the piston lifts and the liquid
boils back into gas (gold flashes).
"""

from manim_scenes.common import *
from manim_scenes.kit_e import SqueezeBox, phase_chip

TR = pm.co2_reduced_temperature(pm.ANDREWS_FOLLOW_C)
P_SAT, V_LIQ, V_GAS = pm.maxwell(TR)
V_START, V_END, V_BACK = 3.6, 0.585, 1.15          # reduced volumes: start, end of squeeze, final release
H_START = 4.2                                     # cylinder height at V_START (stage units)
COUNT = 110
STAGE_AT = (-4.25, -0.55, 0.0)
CLOSE_AT, CLOSE_ZOOM = (-4.25, 0.1, 0.0), 1.42      # the camera moves in once the drops form


class Scene18Andrews(Scene):
    def construct(self) -> None:
        play_scene(self)


def cylinder_height(vr: float) -> float:
    """The drawn cylinder's height is proportional to the fluid's volume."""
    return H_START * vr / V_START


def pressure(vr: float) -> float:
    return float(pm.isotherm(TR, np.array([vr]))[0])


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "18", TITLES["18"])

    # --- 0. A cylinder of carbon dioxide, a piston, and P against V -------------------------------------------------
    box = SqueezeBox(STAGE_AT, lid="piston", count=COUNT, half_x=1.45, half_z=1.05, height=H_START, floor=-2.05,
                     zoom=0.98, yaw=-0.62, pitch=0.3, speed=1.6, liquid_spacing=0.23, sway=0.03)
    vr = Knob(V_START)
    lowest = Knob(V_START)

    def drive() -> None:
        v = vr.value
        lowest.value = min(lowest.value, v)
        box.chamber.height = cylinder_height(v)
        x = pm.liquid_fraction(TR, v)
        box.level = min(x * cylinder_height(V_LIQ), cylinder_height(v))
        box.squash = min(cylinder_height(v) / cylinder_height(V_LIQ), 1.0)
        box.set_vapour(int(round((1 - x) * COUNT)))

    box.stage.bodies.insert(0, Ticker(drive))
    show(scene, box.stage, 1.2)

    axes = plot_axes((0, 4.0), (0, 1.6), x_length=6.0, y_length=5.2, at=[3.85, -0.3, 0], x_label="V", y_label="P",
                     x_color=cfg.VOLUME, y_color=cfg.PRESSURE)
    co2 = chip("CO₂", cfg.GAS_COLORS["CO2"], cfg.FONT["label"]).move_to([-5.15, -3.55, 0])
    o = axes.c2p(0, 0)
    shrink = VecArrow(axes.c2p(3.4, 0) + DOWN * 0.42, axes.c2p(1.2, 0) + DOWN * 0.42, cfg.VOLUME, width=0.09, tip_len=0.26)
    rise = VecArrow(o + LEFT * 0.42 + UP * 0.8, o + LEFT * 0.42 + UP * 3.4, cfg.PRESSURE, width=0.09, tip_len=0.26)
    scene.play(Create(axes), *box.stage.turn(yaw=-0.5), run_time=1.8)
    scene.play(FadeIn(co2, shift=UP * 0.15), *box.stage.turn(yaw=-0.46), run_time=1.0)
    scene.add(shrink, rise)
    scene.play(shrink.grow_in(run_time=1.3), Indicate(axes.labels[0], color=cfg.WHITE, scale_factor=1.35),
               *box.stage.turn(yaw=-0.41), run_time=1.3)
    scene.play(rise.grow_in(run_time=1.3), Indicate(axes.labels[1], color=cfg.WHITE, scale_factor=1.35),
               *box.stage.turn(yaw=-0.36), run_time=1.3)
    scene.play(*box.stage.turn(yaw=-0.3), run_time=max(time_left(scene, t, 1) - 0.05, 0.1))

    # --- 1. One isotherm: 21.5 °C, held by a thermostat -------------------------------------------------------------------------
    beat(scene, t, 1)
    temp = chip(f"{fx(pm.ANDREWS_FOLLOW_C, 1)} °C", cfg.TEMPERATURE, cfg.FONT["label"])
    temp.next_to(co2, RIGHT, buff=0.3)
    model = txt("van der Waals model", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(4.0, 0), DL, buff=0.22)
    start_dot = glow_dot(axes.c2p(V_START, pressure(V_START)), cfg.CYAN, radius=0.1)
    ring = Circle(radius=0.32, stroke_color=cfg.TEMPERATURE, stroke_width=4).move_to(start_dot)
    scene.play(FadeIn(temp, shift=UP * 0.15), FadeIn(model), shrink.fade_to(0.0), rise.fade_to(0.0), run_time=1.0)
    scene.remove(shrink, rise)
    scene.play(Circumscribe(temp, color=cfg.TEMPERATURE, buff=0.1), FadeIn(start_dot, scale=0.5), run_time=1.4)
    scene.play(Create(ring), run_time=0.8)
    play_in(scene, t, 2, FadeOut(ring, scale=1.6), *box.stage.turn(yaw=-0.25), run_time=1.6)

    # --- 2. Squeeze the gas: the pressure rises ---------------------------------------------------------------------------------
    beat(scene, t, 2)
    segments = ((V_START, V_GAS, cfg.CYAN), (V_GAS, V_LIQ, cfg.COEXIST), (V_LIQ, V_END, cfg.LIQUID))

    def traced() -> VGroup:
        low = min(lowest.value, vr.value)
        group = VGroup()
        for a, b, color in segments:
            if low >= a - 1e-4:
                break
            vs = np.linspace(a, max(low, b), 50)
            pts = [axes.c2p(x, y) for x, y in zip(vs, pm.isotherm(TR, vs))]
            core = mu.mix(color, cfg.WHITE, 0.25) if color == cfg.LIQUID else color
            group.add(polyline(pts, color, width=18, opacity=0.16), polyline(pts, core, width=6))
        return group

    path = live(VGroup(), traced)
    tracer = live(VGroup(), lambda: glow_dot(axes.c2p(vr.value, pressure(vr.value)), cfg.WHITE, radius=0.1))
    knob_top = lambda: box.stage.screen_point(box.lid_point(1.5))
    push = VecArrow(lambda: knob_top() + UP * (0.3 + 1.0 * pressure(vr.value)), knob_top, cfg.PRESSURE,
                    width=0.12, tip_len=0.3)
    scene.add(path, push)
    scene.play(FadeOut(start_dot), FadeIn(tracer), push.grow_in(run_time=0.8), run_time=0.8)
    gas_tag = txt("gas", cfg.FONT["label"], cfg.CYAN).move_to(axes.c2p(2.75, pressure(2.75)) + UP * 0.5)
    scene.play(vr.to(box.stage, 2.4, run_time=3.6, rate_func=rate_functions.ease_in_sine), run_time=3.6)
    scene.play(vr.to(box.stage, V_GAS + 0.002, run_time=3.4, rate_func=rate_functions.ease_out_sine),
               FadeIn(gas_tag, shift=UP * 0.15, run_time=1.0), run_time=3.4)

    # --- 3. The first drops: move in close ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    first = axes.c2p(V_GAS, P_SAT)
    first_drop = dashed_path(axes.c2p(V_GAS, 0), first, cfg.COEXIST, width=3, opacity=0.8)
    first_ring = Circle(radius=0.2, stroke_color=cfg.LIQUID_EDGE, stroke_width=5).move_to(first)
    first_tag = txt("first drops", cfg.FONT["small"], cfg.LIQUID_EDGE).next_to(axes.c2p(V_GAS, P_SAT * 0.6), RIGHT, buff=0.12)
    scene.play(Create(first_drop), GrowFromCenter(first_ring), FadeIn(first_tag, shift=LEFT * 0.15), run_time=1.0)
    scene.play(vr.to(box.stage, V_GAS - 0.07, run_time=4.6, rate_func=linear), box.stage.zoom_to(CLOSE_ZOOM, run_time=4.6),
               box.stage.glide(CLOSE_AT, run_time=4.6), first_ring.animate.scale(0.6).set_stroke(opacity=0.5), run_time=4.6)

    # --- 4. Keep squeezing: flat pressure, liquid and vapour coexist -----------------------------------------------------------
    beat(scene, t, 4)
    coexist_tag = txt("gas + liquid", cfg.FONT["label"], cfg.COEXIST)
    coexist_tag.next_to(axes.c2p(V_LIQ + 0.07, P_SAT), UP, buff=0.32).align_to(axes.c2p(V_LIQ + 0.07, 0), LEFT)
    ch = box.chamber

    def beside(height: Callable[[], float]) -> np.ndarray:
        corners = [box.stage.screen_point([ch.cx + sx * ch.half_x, height(), ch.cz + sz * ch.half_z])
                   for sx in (-1, 1) for sz in (-1, 1)]
        return max(corners, key=lambda p: p[0])

    def side_label(name: str, color: str, height: Callable[[], float]) -> Text:
        label = txt(name, cfg.FONT["tiny"], color)
        label.add_updater(lambda m: m.move_to(beside(height) + RIGHT * (0.18 + m.width / 2)))
        label.update()
        return label

    vap_tag = side_label("vapour", cfg.CYAN, lambda: (box.surface_y() + ch.top()) / 2)
    liq_tag = side_label("liquid", cfg.LIQUID_EDGE, lambda: (ch.floor + box.surface_y()) / 2)
    scene.play(vr.to(box.stage, 1.2, run_time=6.0, rate_func=linear), FadeIn(coexist_tag, shift=UP * 0.15, run_time=1.2),
               run_time=6.0)
    scene.play(vr.to(box.stage, 1.02, run_time=5.4, rate_func=linear), FadeIn(vap_tag, run_time=1.0),
               FadeIn(liq_tag, run_time=1.0), run_time=5.4)

    # --- 5. Why flat? The vapour is no more crowded; more of it is liquid ---------------------------------------------------------------
    beat(scene, t, 5)
    track_len = 2.2

    def bar_row(name: str, color: str, value, y: float, fill_color: str) -> VGroup:
        label = txt(name, cfg.FONT["small"], color)
        label.move_to([4.3 - label.width / 2, y, 0])
        track = RoundedRectangle(width=track_len, height=0.3, corner_radius=0.15, stroke_color=color, stroke_width=2,
                                 stroke_opacity=0.7, fill_color=cfg.PANEL, fill_opacity=0.8)
        track.move_to([4.55 + track_len / 2, y, 0])
        fill = live(VMobject(), lambda: RoundedRectangle(width=max(track_len * value(), 0.02), height=0.3,
                                                         corner_radius=0.15, stroke_width=0, fill_color=fill_color,
                                                         fill_opacity=0.9).align_to(track, LEFT).set_y(track.get_y()))
        group = VGroup(label, track, fill)
        group.label, group.track, group.fill = label, track, fill
        return group

    crowd_row = bar_row("vapour crowding", cfg.CYAN, lambda: V_GAS / max(vr.value, V_GAS) / 1.25, 3.46, cfg.CYAN)
    liquid_row = bar_row("liquid", cfg.LIQUID_EDGE, lambda: pm.liquid_fraction(TR, vr.value), 2.74, cfg.LIQUID)
    scene.play(FadeIn(crowd_row, shift=DOWN * 0.15), FadeIn(liquid_row, shift=DOWN * 0.15),
               vr.to(box.stage, 0.97, run_time=1.2, rate_func=linear), run_time=1.2)
    flat = Line(axes.c2p(V_GAS, P_SAT), axes.c2p(V_LIQ, P_SAT), stroke_color=cfg.WHITE, stroke_width=10)
    scene.play(vr.to(box.stage, 0.92, run_time=2.4, rate_func=linear), Indicate(crowd_row.label, color=cfg.WHITE),
               ShowPassingFlash(flat, time_width=0.6, run_time=2.4), run_time=2.4)
    scene.play(vr.to(box.stage, 0.86, run_time=2.8, rate_func=linear),
               Circumscribe(crowd_row.track, color=cfg.CYAN, buff=0.08, run_time=2.0),
               set_attr(push, push, "thickness", 0.2, run_time=2.0, rate_func=there_and_back),
               run_time=2.8)
    play_in(scene, t, 6, vr.to(box.stage, 0.8, run_time=2.8, rate_func=linear),
            Indicate(liquid_row.label, color=cfg.WHITE), Circumscribe(liquid_row.track, color=cfg.LIQUID_EDGE, buff=0.08),
            run_time=2.8)

    # --- 6. The last bubble goes; a liquid barely compresses -------------------------------------------------------------------------
    beat(scene, t, 6)
    last = axes.c2p(V_LIQ, P_SAT)
    last_drop = dashed_path(axes.c2p(V_LIQ, 0), last, cfg.COEXIST, width=3, opacity=0.8)
    last_tag = txt("last bubble", cfg.FONT["small"], cfg.LIQUID_EDGE).next_to(axes.c2p(V_LIQ, P_SAT * 0.3), RIGHT, buff=0.12)
    scene.play(FadeOut(VGroup(crowd_row, liquid_row, first_tag, vap_tag)), first_ring.animate.set_stroke(opacity=0.0),
               vr.to(box.stage, V_LIQ + 0.02, run_time=2.2, rate_func=linear), run_time=2.2)
    for m in (crowd_row.fill, liquid_row.fill, vap_tag):
        m.clear_updaters()
    last_ring = Circle(radius=0.2, stroke_color=cfg.LIQUID_EDGE, stroke_width=5).move_to(last)
    scene.play(vr.to(box.stage, V_LIQ - 0.001, run_time=0.8, rate_func=linear), Create(last_drop), GrowFromCenter(last_ring),
               FadeIn(last_tag, shift=LEFT * 0.15), run_time=0.8)
    liquid_tag = txt("liquid", cfg.FONT["label"], cfg.LIQUID_EDGE).next_to(axes.c2p(0.66, 1.38), RIGHT, buff=0.3)
    scene.play(vr.to(box.stage, V_END, run_time=5.2, rate_func=rate_functions.ease_in_out_sine),
               last_ring.animate.scale(0.6).set_stroke(opacity=0.4), FadeIn(liquid_tag, shift=UP * 0.15, run_time=1.4),
               run_time=5.2)
    play_in(scene, t, 7, Indicate(liquid_tag, color=cfg.WHITE), Flash(axes.c2p(V_END, pressure(V_END)), color=cfg.LIQUID_EDGE),
            run_time=1.4)

    # --- 7. Three behaviours, one substance: the same molecules ------------------------------------------------------------------------
    beat(scene, t, 7)
    chips = VGroup(phase_chip("gas", cfg.CYAN, "gas"), phase_chip("gas + liquid", cfg.COEXIST, "flat"),
                   phase_chip("liquid", cfg.LIQUID_EDGE, "steep")).arrange(RIGHT, buff=0.3).move_to([0, 3.32, 0])
    tags = (gas_tag, coexist_tag, liquid_tag)
    scene.play(push.fade_to(0.0, run_time=0.8), FadeOut(liq_tag), FadeOut(VGroup(last_tag, last_ring, first_ring)),
               run_time=0.8)
    liq_tag.clear_updaters()
    for chip_, tag in zip(chips, tags):
        scene.play(FadeIn(chip_, shift=DOWN * 0.15), Indicate(tag, color=cfg.WHITE, scale_factor=1.15), run_time=0.9)
    same = result_label("same molecules", cfg.GOLD, cfg.FONT["section"]).move_to([-4.1, 2.05, 0])
    scene.play(FadeIn(same, scale=0.92), vr.to(box.stage, 0.66, run_time=1.4), run_time=1.4)
    finish(scene, t, box.stage, fill=lambda s: [vr.to(box.stage, V_BACK, run_time=s, rate_func=smooth),
                                                box.stage.zoom_to(1.3, run_time=s)])

