"""Scene 01 — the hook. Part 1's gas returns: a 3D glass cylinder of cyan
molecules, one followed in gold, every wall hit an orange spark, and the
equation that tamed it, PV = nRT. Then a contradiction. Carbon dioxide at
20 °C is squeezed by a piston while its isotherm is traced on a P-V plot (the
van der Waals model with Maxwell's flat coexistence line, scaled to CO2): the
pressure climbs, then stops climbing as molecules condense — blue flashes —
into a deep-blue pool that rises from the floor. A dashed Boyle extrapolation
shows where an ideal gas would have gone. The ideal model's two omissions
(no size, no attraction) appear beside the equation, which softens to "≈"
with its conditions. Two molecules, each in a red forbidden sphere, pull on
each other with green arrows; the title closes the scene.
"""

from manim_scenes.common import *

TR = pm.kelvin(20.0) / pm.CRITICAL["CO2"][0]       # CO2 at room temperature, reduced
P_SAT, V_LIQ, V_GAS = pm.maxwell(TR)
V_START, V_SQUEEZE, V_END = 3.0, V_GAS + 0.06, 1.0  # reduced volumes along the squeeze
H_START = 3.4                                      # cylinder height at V_START (stage units)
COUNT = 110


class Scene01Hook(Scene):
    def construct(self) -> None:
        play_scene(self)


def cylinder_height(vr: float) -> float:
    """The drawn cylinder's height is proportional to the fluid's volume."""
    return H_START * vr / V_START


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")

    # --- 1. Part 1's gas: countless molecules, one equation -----------------------------------------------------------
    box = TwoPhaseBox((-3.7, -0.95, 0), lid="piston", count=COUNT, half_x=1.5, half_z=1.1, height=H_START, floor=-1.7,
                      zoom=1.22, yaw=-0.55, pitch=0.3, speed=1.6, follow=7, trail=3.0, liquid_spacing=0.24)
    vr = Knob(V_START)

    def drive() -> None:
        v = vr.value
        box.chamber.height = cylinder_height(v)
        x = pm.liquid_fraction(TR, v)
        box.level = x * cylinder_height(V_LIQ)
        box.set_vapour(int(round((1 - x) * COUNT)))

    box.stage.bodies.insert(0, Ticker(drive))
    question = txt("How can a gas become liquid?", cfg.FONT["body"], cfg.GOLD)
    fit_width(question, 7.1)
    question.move_to([3.6, 0.6, 0])
    show(scene, box.stage, 1.4)
    scene.play(FadeIn(question), *box.stage.turn(yaw=-0.35), run_time=6.0)

    # --- 2. PV = nRT ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    law = paint(eq(["P", "V", "=", "n", "R", "T"], 96), {0: cfg.PRESSURE, 1: cfg.VOLUME, 3: cfg.AMOUNT, 5: cfg.TEMPERATURE})
    law.move_to([3.6, 0.6, 0])
    names = VGroup(*[txt(word, cfg.FONT["small"], color) for word, color in
                     (("pressure", cfg.PRESSURE), ("volume", cfg.VOLUME), ("amount", cfg.AMOUNT),
                      ("temperature", cfg.TEMPERATURE))]).arrange(RIGHT, buff=0.42)
    fit_width(names, 7.4)
    names.next_to(law, DOWN, buff=0.55)
    swap(scene, question, law, run_time=1.8)
    scene.play(LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in names], lag_ratio=0.25), run_time=1.6)
    scene.play(Circumscribe(law, color=cfg.GOLD, buff=0.2), run_time=1.6)

    # --- 3. But there is a problem ------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(names), law.animate.scale(0.55).move_to([4.6, 3.3, 0]), box.cloud.tween("follow_alpha", 0.0),
               run_time=1.2)
    box.cloud.follow = None

    # --- 4. Squeeze carbon dioxide: the pressure climbs ----------------------------------------------------------------------------
    beat(scene, t, 3)
    tag = chip("CO₂ at 20 °C", cfg.GAS_COLORS["CO2"], cfg.FONT["label"]).move_to([-3.7, 3.45, 0])
    axes = plot_axes((0, 3.2), (0, 1.5), x_length=5.8, y_length=4.6, at=[3.6, -0.85, 0], x_label="V", y_label="P",
                     x_color=cfg.VOLUME, y_color=cfg.PRESSURE)

    def traced() -> VMobject:
        v = vr.value
        if v > V_START - 1e-3:
            return VMobject()
        vs = np.linspace(V_START, v, 60)
        return polyline([axes.c2p(x, y) for x, y in zip(vs, pm.isotherm(TR, vs))], cfg.PRESSURE, width=6)

    path = live(VMobject(), traced)
    tracer = live(VGroup(), lambda: glow_dot(axes.c2p(vr.value, float(pm.isotherm(TR, np.array([vr.value]))[0])),
                                             cfg.PRESSURE, radius=0.1))
    scene.play(FadeIn(tag, shift=DOWN * 0.15), Create(axes), run_time=1.2)
    scene.add(path, tracer)
    scene.play(vr.to(box.stage, V_SQUEEZE, run_time=5.4, rate_func=smooth), run_time=5.4)

    # --- 5. Keep squeezing: droplets, a liquid on the floor ---------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(vr.to(box.stage, V_END, run_time=6.2, rate_func=smooth), run_time=6.2)
    v_ideal = np.linspace(P_SAT * V_GAS / 1.45, V_GAS, 40)
    ideal = DashedVMobject(polyline([axes.c2p(v, P_SAT * V_GAS / v) for v in v_ideal], cfg.MUTED, width=4), num_dashes=18)
    ideal_tag = txt("ideal: keeps rising", cfg.FONT["small"], cfg.MUTED).next_to(axes.c2p(1.05, 1.42), RIGHT, buff=0.2)
    flat_tag = txt("real: flat", cfg.FONT["label"], cfg.PRESSURE).move_to(axes.c2p(2.0, 1.08))
    liquid_tag = txt("liquid!", cfg.FONT["section"], cfg.LIQUID_EDGE).move_to([-3.7, 1.6, 0])
    scene.play(FadeIn(liquid_tag, shift=UP * 0.2), run_time=0.8)
    scene.play(Create(ideal), FadeIn(ideal_tag), FadeIn(flat_tag), run_time=1.6)

    # --- 6. Ideal molecules: no size, no attraction ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    flaws = VGroup(chip("no size", cfg.LIMIT, cfg.FONT["small"]), chip("no attraction", cfg.LIMIT, cfg.FONT["small"]))
    flaws.arrange(RIGHT, buff=0.35).next_to(law, DOWN, buff=0.3).align_to(law, RIGHT)
    crack = strike(law, cfg.WARNING, width=7)
    scene.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.15) for f in flaws], lag_ratio=0.35), run_time=1.4)
    scene.play(Create(crack), Indicate(liquid_tag, color=cfg.WHITE, scale_factor=1.08), run_time=1.2)

    # --- 7. An approximation, under the right conditions --------------------------------------------------------------------------------
    beat(scene, t, 6)
    approx = paint(eq(["P", "V", r"\approx", "n", "R", "T"], 96), {0: cfg.PRESSURE, 1: cfg.VOLUME, 2: cfg.GOLD, 3: cfg.AMOUNT,
                                                                       5: cfg.TEMPERATURE}).scale(0.55).move_to(law)
    when = chip("low P · high T", cfg.GREEN, cfg.FONT["small"]).move_to(flaws)
    scene.play(FadeOut(crack), fade_through(law, approx), fade_through(flaws, when), run_time=1.4)
    scene.play(Indicate(approx[2], color=cfg.GOLD, scale_factor=1.3), run_time=1.2)

    # --- 8. Look between the molecules ------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    hide(scene, box.stage, 1.0, FadeOut(VGroup(axes, path, tracer, ideal, ideal_tag, flat_tag, liquid_tag, tag)))
    for m in (path, tracer):
        m.clear_updaters()
    pair = Stage((0.0, -0.4, 0.0), zoom=1.9, yaw=-0.3, pitch=0.22, sway=0.05)
    gap = Knob(3.2)
    a = Ball(lambda: np.array([-gap.value / 2, 0.0, 0.0]), 0.42, cfg.MOLECULE)
    b = Ball(lambda: np.array([gap.value / 2, 0.0, 0.0]), 0.42, cfg.MOLECULE)
    zones = [glass_sphere(pair, (lambda s=s: np.array([s * gap.value / 2, 0.0, 0.0])), 0.84, cfg.SIZE,
                          presence=0.0, fill_opacity=0.12) for s in (-1, 1)]
    pair.add_body(a, b)
    pulls = [Vector(lambda s=s: np.array([s * (gap.value / 2 - 0.5), 0.0, 0.0]),
                    lambda s=s: np.array([s * (gap.value / 2 - 0.5) - s * 0.5, 0.0, 0.0]), cfg.ATTRACT, width=0.1, tip=0.28)
             for s in (-1, 1)]
    for p in pulls:
        p.presence = 0.0
    pair.add_overlay(*pulls)
    show(scene, pair, 0.9, FadeOut(VGroup(approx, when)))
    attract = txt("attraction", cfg.FONT["section"], cfg.ATTRACT).move_to([0, 1.75, 0])
    size = txt("size", cfg.FONT["section"], cfg.SIZE).move_to([0, -2.75, 0])
    scene.play(*[pair.fade(p, 1.0) for p in pulls], gap.to(pair, 2.3, run_time=2.4), FadeIn(attract), run_time=2.4)
    scene.play(*[f for z in zones for f in fade_all(pair, z.parts, 1.0)], FadeIn(size), run_time=1.4)

    # --- 9. Title -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    card = title_card(cfg.PROJECT_TITLE, cfg.VIDEO_SUBTITLE).move_to(UP * 0.35)
    plate = RoundedRectangle(width=14.2, height=4.4, corner_radius=0.3, stroke_width=0, fill_color=cfg.BG,
                             fill_opacity=0.72).move_to(card)
    series = txt(cfg.SERIES_LABEL, cfg.FONT["small"], cfg.MUTED)
    fit_width(series, 12.8)
    series.next_to(card, DOWN, buff=0.55)
    scene.play(FadeOut(VGroup(attract, size)), pair.fade(pair, 0.4), FadeIn(plate), run_time=1.0)
    scene.play(FadeIn(card, scale=0.94), run_time=1.4)
    rule = Line(LEFT * 4.6, RIGHT * 4.6, stroke_color=cfg.GOLD, stroke_width=4).next_to(card, DOWN, buff=0.2)
    scene.play(Create(rule), FadeIn(series, shift=UP * 0.15), card.glow.animate.set_stroke(opacity=0.3), run_time=1.4)
    finish(scene, t, pair)
