"""Scene 29 — the same molecules. The film's opening cylinder returns, its
molecules drawn as tiny points beside PV = nRT. Three panels add what real
molecules have: a gold Maxwell-Boltzmann curve (many speeds), two molecules
pulling with green arrows (attraction) and a molecule inside its red
forbidden sphere (size); the molecules in the cylinder grow to real size.
Warmed and roomy, the gas behaves ideally (a green check); squeezed and
cooled, the same molecules condense into the deep-blue pool (the lever rule
of the van der Waals model at t_r = 0.9). The van der Waals equation and a
small coexistence dome with its purple critical point stand for the gas
chapters; evaporation flashes, a round drop and sliding layers for the
liquid chapters. Three words — how fast, how close, how strongly — frame the
cylinder, and the closing line ends the lesson.
"""

from manim_scenes.common import *

TR = 0.9                                   # a cold, sub-critical van der Waals isotherm (reduced)
P_SAT, V_LIQ, V_GAS = pm.maxwell(TR)
V_START, V_END = 3.2, 1.0
H_START = 3.3
COUNT = 100


class Scene29Synthesis(Scene):
    def construct(self) -> None:
        play_scene(self)


def height(vr: float) -> float:
    return H_START * vr / V_START


def speed_card() -> VGroup:
    axes = plot_axes((0, 1100), (0, 2.4), x_length=3.4, y_length=1.5, x_label="u", y_label="", x_color=cfg.VELOCITY)
    curve = mb_curve(axes, pm.ROOM_T, pm.MOLAR_MASS["N2"], cfg.GOLD, u_max=1100, width=5, fill_opacity=0.18)
    name = txt("many speeds", cfg.FONT["section"], cfg.GOLD)
    picture = VGroup(axes, curve)
    return VGroup(picture, name).arrange(RIGHT, buff=0.45)


def attraction_card() -> VGroup:
    left, right = bead([-0.55, 0, 0], cfg.MOLECULE, 0.24), bead([0.55, 0, 0], cfg.MOLECULE, 0.24)
    pulls = VGroup(VecArrow([-0.26, 0, 0], [0.02, 0, 0], cfg.ATTRACT, width=0.07, tip_len=0.16, live=False),
                   VecArrow([0.26, 0, 0], [-0.02, 0, 0], cfg.ATTRACT, width=0.07, tip_len=0.16, live=False))
    picture = VGroup(left, right, pulls)
    picture.scale(1.6)
    name = txt("attraction", cfg.FONT["section"], cfg.ATTRACT)
    return VGroup(picture, name).arrange(RIGHT, buff=0.45)


def size_card() -> VGroup:
    core = bead(ORIGIN, cfg.MOLECULE, 0.24)
    zone = Circle(radius=0.5, stroke_color=cfg.SIZE, stroke_width=4, fill_color=cfg.SIZE, fill_opacity=0.12)
    picture = VGroup(zone, core).scale(1.5)
    name = txt("size", cfg.FONT["section"], cfg.SIZE)
    return VGroup(picture, name).arrange(RIGHT, buff=0.45)


def dome_card() -> VGroup:
    axes = plot_axes((0.3, 4.4), (0, 1.3), x_length=4.6, y_length=2.6, x_label="V", y_label="P", x_color=cfg.VOLUME,
                     y_color=cfg.PRESSURE)
    dome = pm.binodal(40, 0.8)
    shade = Polygon(*[axes.c2p(v, p) for v, p in dome], stroke_color=cfg.GOLD, stroke_width=4, fill_color=cfg.COEXIST,
                    fill_opacity=0.35)
    vs = np.linspace(0.58, 4.4, 90)
    iso = polyline([axes.c2p(v, min(p, 1.25)) for v, p in zip(vs, pm.isotherm(0.9, vs))],
                   cfg.CYAN, width=4)
    peak = glow_dot(axes.c2p(1.0, 1.0), cfg.CRITICAL, radius=0.1, reach=3.6)
    return VGroup(axes, shade, iso, peak)


def flow_card() -> VGroup:
    layers = VGroup(*[RoundedRectangle(width=2.2, height=0.22, corner_radius=0.08, stroke_width=0, fill_color=cfg.LIQUID,
                                       fill_opacity=0.35 + 0.12 * k).shift(UP * 0.3 * k + RIGHT * 0.18 * k)
                      for k in range(4)])
    arrows = VGroup(*[VecArrow([0.9 + 0.18 * k, 0.3 * k, 0], [0.9 + 0.18 * k + 0.25 + 0.22 * k, 0.3 * k, 0], cfg.GOLD,
                               width=0.05, tip_len=0.12, live=False) for k in range(4)])
    return VGroup(layers, arrows)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "29", TITLES["29"])

    # --- 1. An ideal gas: tiny points, one equation ------------------------------------------------------------------------------------
    box = TwoPhaseBox((-3.8, -0.9, 0), lid="piston", count=COUNT, half_x=1.45, half_z=1.05, height=H_START, floor=-1.65,
                      zoom=1.2, yaw=-0.5, pitch=0.3, speed=1.6, radius=0.045, liquid_spacing=0.24)
    vr = Knob(V_START)
    driving = {"on": False}

    def drive() -> None:
        if not driving["on"]:
            return
        v = vr.value
        box.chamber.height = height(v)
        x = pm.liquid_fraction(TR, v)
        box.level = x * height(V_LIQ)
        box.set_vapour(int(round((1 - x) * COUNT)))

    box.stage.bodies.insert(0, Ticker(drive))
    show(scene, box.stage, 1.2)
    law = paint(eq(["P", "V", "=", "n", "R", "T"], cfg.FONT["hero"]), {0: cfg.PRESSURE, 1: cfg.VOLUME, 3: cfg.AMOUNT,
                                                                       5: cfg.TEMPERATURE})
    law.move_to([3.4, 0.4, 0])
    points = txt("tiny points", cfg.FONT["label"], cfg.LIMIT).next_to(law, DOWN, buff=0.5)
    scene.play(Write(law), run_time=1.6)
    scene.play(FadeIn(points, shift=UP * 0.15), *box.stage.turn(yaw=-0.35), run_time=1.6)

    # --- 2. Real molecules are richer ---------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(points), law.animate.scale(0.5).move_to([5.6, 3.3, 0]), run_time=1.0)
    scene.play(box.cloud.tween("radius", 0.085), run_time=1.6)

    # --- 3. Speeds, attraction, size ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    cards = VGroup(speed_card(), attraction_card(), size_card()).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    cards.scale(min(6.6 / cards.width, 5.6 / cards.height))
    cards.move_to([3.5, -0.35, 0])
    for card in cards:
        scene.play(FadeIn(card, shift=LEFT * 0.25), run_time=1.0)
    scene.play(box.cloud.tween("radius", 0.11), Indicate(cards[2][1], color=cfg.WHITE, scale_factor=1.08), run_time=1.4)

    # --- 4. Far apart and fast: ideal. Squeezed and slowed: real ------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(cards), run_time=0.7)
    fast = VGroup(txt("far apart · fast", cfg.FONT["label"], cfg.CYAN), check_mark(0.3, cfg.GREEN)).arrange(RIGHT, buff=0.3)
    fast.move_to([3.4, 1.3, 0])
    ideal = eq(r"PV \approx nRT", cfg.FONT["section"], cfg.WHITE).next_to(fast, DOWN, buff=0.35)
    scene.play(FadeIn(fast), FadeIn(ideal), box.heat_to(520, run_time=2.4), run_time=2.4)
    slow = txt("squeezed · slowed", cfg.FONT["label"], cfg.COLD_COLOR).move_to([3.4, -0.9, 0])
    real = txt("details take control", cfg.FONT["label"], cfg.GOLD).next_to(slow, DOWN, buff=0.35)
    driving["on"] = True
    scene.play(FadeIn(slow), box.heat_to(240, run_time=1.4), box.cloud.tween("warmth", 0.0, run_time=1.4), run_time=1.4)
    play_in(scene, t, 4, vr.to(box.stage, V_END, run_time=6.0, rate_func=smooth), FadeIn(real, run_time=1.2), run_time=6.0)

    # --- 5. Deviations, liquefaction, the critical point ------------------------------------------------------------------------------------
    beat(scene, t, 4)
    vdw = paint(eq([r"\left(P+", r"\frac{an^2}{V^2}", r"\right)", r"(V-", "nb", ")", "=", "nRT"], cfg.FONT["section"]),
                {1: cfg.ATTRACT, 4: cfg.SIZE})
    fit_width(vdw, 7.0)
    vdw.move_to([3.5, 1.75, 0])
    dome = dome_card()
    dome.scale(min(5.6 / dome.width, 3.5 / dome.height))
    dome.move_to([3.4, -1.1, 0])
    scene.play(FadeOut(VGroup(fast, ideal, slow, real)), run_time=0.7)
    scene.play(Write(vdw), run_time=1.8)
    scene.play(FadeIn(dome, shift=UP * 0.2), run_time=1.4)
    scene.play(Flash(dome[3], color=cfg.CRITICAL, flash_radius=0.45), run_time=1.0)

    # --- 6. Evaporation, round drops, flow -------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    driving["on"] = False
    exchanger = box.exchange(rate=5.0)
    drop = bead(ORIGIN, cfg.LIQUID_EDGE, 0.42, glow=0.8)
    flow = flow_card()
    liquids = VGroup(VGroup(drop, txt("round drops", cfg.FONT["label"], cfg.LIQUID_EDGE)).arrange(RIGHT, buff=0.4),
                     VGroup(flow, txt("flow", cfg.FONT["label"], cfg.GOLD)).arrange(RIGHT, buff=0.4))
    liquids.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([3.5, -0.4, 0])
    liquids.scale(min(6.4 / liquids.width, 4.6 / liquids.height, 1.6))
    evaporate = txt("evaporation", cfg.FONT["label"], cfg.EVAPORATE).move_to([-3.8, 2.85, 0])
    scene.play(FadeOut(VGroup(vdw, dome)), FadeIn(evaporate, shift=UP * 0.15), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(row, shift=LEFT * 0.2) for row in liquids], lag_ratio=0.4), run_time=1.6)

    # --- 7. How fast, how close, how strongly ------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    words = VGroup(txt("how fast they move", cfg.FONT["section"], cfg.GOLD),
                   txt("how closely they are packed", cfg.FONT["section"], cfg.SIZE),
                   txt("how strongly they interact", cfg.FONT["section"], cfg.ATTRACT)).arrange(DOWN, buff=0.45,
                                                                                               aligned_edge=LEFT)
    fit_inside(words, 7.0, 3.6)
    words.move_to([3.6, -0.2, 0])
    scene.play(FadeOut(VGroup(liquids, evaporate)), run_time=0.7)
    for w in words:
        scene.play(FadeIn(w, shift=RIGHT * 0.2), run_time=1.0)
    scene.play(*box.stage.turn(yaw=-0.6), run_time=3.0)

    # --- 8. That is the chemistry of gases and liquids ----------------------------------------------------------------------------------------
    beat(scene, t, 7)
    closing = VGroup(Text("That is the chemistry of", font=cfg.TITLE_FONT, weight=BOLD, font_size=60, color=cfg.WHITE),
                     Text("gases and liquids", font=cfg.TITLE_FONT, weight=BOLD, font_size=88, color=cfg.GOLD))
    closing.arrange(DOWN, buff=0.25)
    fit_width(closing, 13.0)
    closing[1].set_stroke("#351F05", width=4, opacity=0.8, background=True)
    closing[0].set_stroke("#06131B", width=3, opacity=0.8, background=True)
    glow = closing[1].copy().set_fill(opacity=0).set_stroke(cfg.GOLD, width=16, opacity=0.14)
    decorative(glow)
    plate = RoundedRectangle(width=14.0, height=3.6, corner_radius=0.3, stroke_width=0, fill_color=cfg.BG,
                             fill_opacity=0.75)
    card = VGroup(plate, glow, closing).move_to(UP * 0.1)
    scene.play(FadeOut(words), box.stage.fade(box.stage, 0.4), FadeIn(plate), run_time=0.9)
    scene.play(FadeIn(VGroup(glow, closing), scale=0.95), run_time=1.4)
    finish(scene, t, box.stage, fill=lambda s: [glow.animate.set_stroke(opacity=0.28)])
