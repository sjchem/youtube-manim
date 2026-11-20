"""Scene 12 — a tug of war. Every real gas holds one: attraction pulls the
pressure down, size pushes it up. A rope runs under a turning glass box of
methane; a green arrow (attraction) hauls its knot left, a red arrow (size)
hauls it right, and the knot sits at P_real / P_ideal on a scale whose purple
mark is the ideal value 1. Both arrows are the two rival terms of the van der
Waals gas at the box's pressure and temperature (``kit_c.vdw_terms``), and the
knot is their outcome. On the right the same ratio is traced against pressure
(methane at 300 K, ``pm.z_vdw``), with a bead at the box's pressure.

Squeeze from 5 bar (both arrows tiny: nearly ideal) to 150 bar (green wins:
negative deviation) to 800 bar (red wins: positive deviation). Heat to 600 K at
150 bar: the green arrow shrinks and the knot returns to 1, and the 600 K curve
barely dips. Helium at 300 K: almost no green arrow; its curve rises from the
start. A quick check with a three-second countdown closes the scene: pressure
below ideal means attraction is winning.
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d
from manim_scenes.kit_c import vdw_terms
from manim_scenes.kit_d import PairLinks, Trace, at_word

P_TOP = 800.0
Z_RANGE = (0.7, 2.0)
BOX_AT = (-4.4, 0.35, 0.0)
ROPE_Y = -2.75
KNOT_X0 = -4.4             # knot position at P_real / P_ideal = 1
KNOT_SCALE = 2.1           # screen units per unit of the ratio
ARROW_SCALE = 0.75         # screen units per unit of each term
H0 = 2.4


class Scene12TugOfWar(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "12", TITLES["12"])
    P, T = Knob(60.0), Knob(pm.ROOM_T)
    gas = {"g": "CH4"}

    def terms() -> tuple[float, float, float]:
        return vdw_terms(P.value, T.value, gas["g"])

    # --- the box: squeezed with pressure, warmed with temperature, links show attraction ------------------------------
    box = GasBox(BOX_AT, count=64, half_x=1.2, half_z=0.9, height=H0, floor=-1.2, lid="piston", zoom=0.95, yaw=-0.5,
                 pitch=0.3, speed=1.4, radius=0.085, seed=cfg.SEED + 120)
    links = PairLinks(box.cloud, cutoff=0.5)
    box.stage.add_body(links)

    def sync() -> None:
        push, pull, _ = terms()
        box.chamber.height = H0 * float(np.clip(1 / (1 + P.value / 160), 0.32, 1.0))
        box.cloud.heat = float(np.sqrt(T.value / pm.ROOM_T))
        box.cloud.warmth = float(np.clip((T.value - pm.ROOM_T) / 600, 0, 0.5))
        links.alpha = float(np.clip(pull / 0.9, 0, 1)) * link_gain.value
        box.cloud.radius = 0.085 + 0.05 * float(np.clip(push / 2.5, 0, 1))

    link_gain = Knob(1.0)
    box.stage.bodies.insert(0, Ticker(sync))

    # --- the rope ---------------------------------------------------------------------------------------------------------------
    def knot_x() -> float:
        return KNOT_X0 + (terms()[2] - 1.0) * KNOT_SCALE

    rope = Line([-7.4, ROPE_Y, 0], [-1.1, ROPE_Y, 0], stroke_color=cfg.MUTED, stroke_width=5, stroke_opacity=0.6)
    ideal_mark = VGroup(DashedLine([KNOT_X0, ROPE_Y - 0.45, 0], [KNOT_X0, ROPE_Y + 0.45, 0], stroke_color=cfg.LIMIT,
                                   stroke_width=4, dash_length=0.08),
                        txt("ideal", cfg.FONT["tiny"], cfg.LIMIT).move_to([KNOT_X0, ROPE_Y - 0.72, 0]))

    def tug() -> VGroup:
        push, pull, _ = terms()
        x = knot_x()
        group = VGroup()
        if pull > 0.004:
            group.add(arrow2d([x, ROPE_Y, 0], [x - min(pull * ARROW_SCALE + 0.2, 2.6), ROPE_Y, 0], cfg.ATTRACT, width=0.16,
                              tip_len=0.32))
        if push > 0.004:
            group.add(arrow2d([x, ROPE_Y, 0], [x + min(push * ARROW_SCALE + 0.2, 2.9), ROPE_Y, 0], cfg.SIZE, width=0.16,
                              tip_len=0.32))
        knot = Circle(radius=0.2, stroke_color=cfg.WHITE, stroke_width=5, fill_color=cfg.PANEL, fill_opacity=1).move_to([x, ROPE_Y, 0])
        group.add(knot)
        return group

    pull_tag = txt("attraction", cfg.FONT["label"], cfg.ATTRACT).move_to([-6.3, ROPE_Y + 0.55, 0])
    push_tag = txt("size", cfg.FONT["label"], cfg.SIZE).move_to([-1.8, ROPE_Y + 0.55, 0])
    down = txt("P down", cfg.FONT["tiny"], cfg.ATTRACT).next_to(pull_tag, DOWN, buff=0.5).shift(LEFT * 0.2)
    up = txt("P up", cfg.FONT["tiny"], cfg.SIZE).next_to(push_tag, DOWN, buff=0.5)

    # --- 0. Attraction pulls down, size pushes up ---------------------------------------------------------------------------
    show(scene, box.stage, 1.0, Create(rope), FadeIn(ideal_mark))
    rope_live = live(VGroup(), tug)
    scene.add(rope_live)
    at_word(scene, t, 0, "Attraction", lead=0.3)
    scene.play(FadeIn(rope_live), FadeIn(pull_tag, shift=RIGHT * 0.2), FadeIn(down), run_time=1.0)
    at_word(scene, t, 0, "Size", lead=0.2)
    scene.play(FadeIn(push_tag, shift=LEFT * 0.2), FadeIn(up), run_time=1.0)
    play_in(scene, t, 1, *box.stage.turn(yaw=-0.35), run_time=1.6)

    # --- 1. Which side wins depends on how hard we squeeze ---------------------------------------------------------------------
    beat(scene, t, 1)
    axes = plot_axes((0, P_TOP), Z_RANGE, x_length=5.9, y_length=4.5, at=[3.35, -0.35, 0], x_label="P",
                     y_label=r"P_{\text{real}}/P_{\text{ideal}}", x_color=cfg.PRESSURE, y_color=cfg.WHITE,
                     x_ticks=(200, 400, 600, 800), y_ticks=(1.0, 1.5))
    unit = txt("bar", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.labels[0], RIGHT, buff=0.12, aligned_edge=DOWN)
    axes.add(decorative(unit))
    one = DashedLine(axes.c2p(0, 1), axes.c2p(P_TOP, 1), stroke_color=cfg.LIMIT, stroke_width=3.5, dash_length=0.14)
    ps = np.linspace(0.5, P_TOP, 200)
    ch4 = Trace(axes, ps, [pm.z_vdw(p, pm.ROOM_T, "CH4") for p in ps], cfg.GAS_COLORS["CH4"], start=P.value)
    name = txt(f"CH₄ · {fx(pm.ROOM_T, 0)} K", cfg.FONT["small"], cfg.GAS_COLORS["CH4"]).move_to(axes.c2p(560, 1.85))
    scene.play(Create(axes), Create(one), FadeIn(name), run_time=1.4)
    scene.add(ch4.curve, ch4.bead)
    play_in(scene, t, 2, P.to(rope_live, 5.0, rate_func=smooth), ch4.grow(5.0, rate_func=smooth), run_time=1.6)

    # --- 2. Low pressure: nearly ideal ---------------------------------------------------------------------------------------
    beat(scene, t, 2)
    note = txt("nearly ideal", cfg.FONT["label"], cfg.LIMIT).move_to([-4.4, -1.4, 0])
    at_word(scene, t, 2, "Neither", lead=0.3)
    scene.play(FadeIn(note, shift=UP * 0.1), Indicate(ideal_mark, color=cfg.WHITE), run_time=1.2)
    play_in(scene, t, 3, *box.stage.turn(yaw=-0.6), run_time=2.0)

    # --- 3. Moderate pressure: attraction wins -------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(note), P.to(rope_live, 150.0, rate_func=smooth), ch4.grow(150.0, rate_func=smooth), run_time=3.6)
    at_word(scene, t, 3, "wins", lead=0.3)
    neg = txt("attraction wins", cfg.FONT["label"], cfg.ATTRACT).move_to(axes.c2p(560, 0.9))
    play_in(scene, t, 4, FadeIn(neg, shift=UP * 0.1), run_time=1.0)

    # --- 4. Very high pressure: size wins --------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(P.to(rope_live, P_TOP, rate_func=smooth), ch4.grow(P_TOP, rate_func=smooth), run_time=4.4)
    at_word(scene, t, 4, "positive", lead=0.3)
    pos = txt("size wins", cfg.FONT["label"], cfg.SIZE).move_to(axes.c2p(330, 1.62))
    play_in(scene, t, 5, FadeIn(pos, shift=DOWN * 0.1), run_time=1.0)

    # --- 5. Heating weakens the negative deviation ----------------------------------------------------------------------------
    beat(scene, t, 5)
    hot = Trace(axes, ps, [pm.z_vdw(p, 600.0, "CH4") for p in ps], cfg.TEMPERATURE, start=0.5)
    hot_name = txt("600 K", cfg.FONT["small"], cfg.TEMPERATURE).move_to(axes.c2p(700, 1.22))
    scene.play(P.to(rope_live, 150.0, rate_func=smooth), ch4.fade_bead(0.0), run_time=1.6)
    scene.play(T.to(rope_live, 600.0, rate_func=smooth), run_time=2.4)
    scene.add(hot.curve, hot.bead)
    play_in(scene, t, 6, hot.grow(P_TOP, rate_func=smooth), FadeIn(hot_name), run_time=2.4)

    # --- 6. Helium and hydrogen: size wins from the start ----------------------------------------------------------------------
    beat(scene, t, 6)
    he = Trace(axes, ps, [pm.z_vdw(p, pm.ROOM_T, "He") for p in ps], cfg.GAS_COLORS["He"], start=0.5)
    he_name = txt("He · 300 K", cfg.FONT["small"], cfg.GAS_COLORS["He"]).move_to(axes.c2p(230, 1.62))
    scene.play(T.to(rope_live, pm.ROOM_T), P.to(rope_live, 1.0), hot.fade_bead(0.0), FadeOut(VGroup(neg, pos)), run_time=1.2)
    gas["g"] = "He"
    scene.add(he.curve, he.bead)
    scene.play(FadeIn(he_name), he.grow(400.0, rate_func=smooth), P.to(rope_live, 400.0, rate_func=smooth),
               link_gain.to(rope_live, 0.0), run_time=3.4)
    at_word(scene, t, 6, "positive", lead=0.3)
    play_in(scene, t, 7, he.grow(P_TOP, rate_func=smooth), P.to(rope_live, P_TOP, rate_func=smooth), run_time=2.2)

    # --- 7. Quick check -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    card_lines = VGroup(txt("quick check", cfg.FONT["label"], cfg.GOLD),
                        txt("same n, V, T", cfg.FONT["small"], cfg.MUTED),
                        eq(r"P_{\text{measured}} < P_{\text{ideal}}", cfg.FONT["section"], cfg.WHITE),
                        txt("which effect is winning?", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.28)
    card = on_panel(card_lines, cfg.GOLD, pad=0.4, opacity=0.96).move_to([0.6, 0.1, 0])
    scrim = Rectangle(width=16.5, height=9.5, stroke_width=0, fill_color=cfg.BG, fill_opacity=0.72)
    scene.play(FadeIn(scrim), FadeOut(VGroup(name, hot_name, he_name, pull_tag, push_tag, down, up, ideal_mark)), run_time=0.5)
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    at_word(scene, t, 7, "winning", lead=0.0)
    countdown(scene, card.get_right() + RIGHT * 1.1, 3)

    # --- 8. Attraction ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    answer = VGroup(txt("attraction", cfg.FONT["title"], cfg.ATTRACT), check_mark(0.34)).arrange(RIGHT, buff=0.3)
    answer.next_to(card_lines, DOWN, buff=0.35)
    scene.play(FadeIn(answer, scale=1.15), card.back.animate.stretch_to_fit_height(card.back.height + answer.height + 0.4)
               .shift(DOWN * (answer.height + 0.4) / 2), run_time=0.8)
    finish(scene, t, box.stage)
