"""Scene 22 — why cooling matters. A glass box of gas is squeezed (molecules
pushed close) and cooled (molecules slowed), and green links show attraction
holding neighbours together. Then a kelvin axis with room temperature marked
in gold: each gas's critical temperature (``pm.CRITICAL``) is placed on it,
with a small turning 3D molecule above. Carbon dioxide sits just above room
temperature (squeezing at room temperature liquefies it, green check);
nitrogen far below (−147 °C: it must be cooled first, red cross); ammonia
higher still, helped by hydrogen bonds. Finally T_c against a/b (``pm.VDW``) for six gases illustrates the model balance
T_c = 8a/(27Rb). Molecular size matters alongside attraction; fitted critical
constants make this a model consistency illustration, not an independent proof.
"""

from manim_scenes.common import *
from manim_scenes.kit_d import PairLinks, at_word

T_MAX = 460.0
AXIS_Y = -0.9


class Scene22Cooling(Scene):
    def construct(self) -> None:
        play_scene(self)


def kx(kelvin: float) -> float:
    return -6.5 + kelvin / T_MAX * 13.0


def molecule_stage(at, atoms, bonds, scale: float = 1.0) -> Stage:
    stage = Stage(at, zoom=1.35, yaw=0.3, pitch=0.25, spin=0.5)
    molecule(stage, atoms, bonds, scale=scale, label=False)
    return stage


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "22", TITLES["22"])

    # --- 0. Cooling and compression together --------------------------------------------------------------------------
    box = GasBox((-3.6, -0.6, 0), count=70, half_x=1.3, half_z=1.0, height=2.6, floor=-1.3, lid="piston", zoom=1.12, yaw=-0.5,
                 pitch=0.3, speed=1.6, radius=0.09, seed=cfg.SEED + 220)
    links = PairLinks(box.cloud, cutoff=0.5)
    box.stage.add_body(links)
    show(scene, box.stage, 1.0)
    squeeze = chip("compress", cfg.PRESSURE, cfg.FONT["section"])
    plus = txt("+", cfg.FONT["title"], cfg.WHITE)
    cool = chip("cool", cfg.COLD_COLOR, cfg.FONT["section"])
    recipe = VGroup(squeeze, plus, cool).arrange(DOWN, buff=0.3).move_to([3.6, 0.3, 0])
    at_word(scene, t, 0, "cooling", lead=0.3)
    scene.play(FadeIn(cool, shift=LEFT * 0.2), run_time=0.8)
    at_word(scene, t, 0, "compression", lead=0.3)
    play_in(scene, t, 1, FadeIn(plus), FadeIn(squeeze, shift=LEFT * 0.2), run_time=0.9)

    # --- 1. Compression pushes them together; cooling lets attraction hold them -----------------------------------------
    beat(scene, t, 1)
    scene.play(box.volume_to(0.42, rate_func=smooth), Indicate(squeeze, color=cfg.WHITE, scale_factor=1.06), run_time=2.4)
    at_word(scene, t, 1, "Cooling", lead=0.3)
    scene.play(box.heat_to(70.0, rate_func=smooth), box.cloud.tween("radius", 0.1), Indicate(cool, color=cfg.WHITE, scale_factor=1.06),
               run_time=2.2)
    at_word(scene, t, 1, "attraction", lead=0.3)
    hold = txt("attraction holds them", cfg.FONT["label"], cfg.ATTRACT).move_to([-3.6, -3.5, 0])
    play_in(scene, t, 2, set_attr(box.stage, links, "alpha", 1.0), FadeIn(hold, shift=UP * 0.1), run_time=1.4)

    # --- 2. Every gas has a critical temperature --------------------------------------------------------------------------
    beat(scene, t, 2)
    hide(scene, box.stage, 0.8, FadeOut(VGroup(recipe, hold)))
    axis = Arrow([kx(0) - 0.1, AXIS_Y, 0], [kx(T_MAX) + 0.3, AXIS_Y, 0], buff=0, stroke_width=5, color=cfg.MUTED,
                 max_tip_length_to_length_ratio=0.02)
    ticks = VGroup(*[VGroup(Line([kx(k), AXIS_Y - 0.1, 0], [kx(k), AXIS_Y + 0.1, 0], stroke_color=cfg.MUTED, stroke_width=3),
                            txt(str(k), cfg.FONT["tiny"], cfg.MUTED).move_to([kx(k), AXIS_Y - 0.42, 0]))
                     for k in (0, 100, 200, 300, 400)])
    decorative(ticks)
    unit = txt("K", cfg.FONT["small"], cfg.MUTED).next_to(axis, RIGHT, buff=0.15)
    room = DashedLine([kx(pm.ROOM_T), AXIS_Y - 0.15, 0], [kx(pm.ROOM_T), 2.95, 0], stroke_color=cfg.GOLD, stroke_width=3.5,
                      dash_length=0.12)
    room_tag = txt("room temperature", cfg.FONT["small"], cfg.GOLD).next_to([kx(pm.ROOM_T), 2.95, 0], UP, buff=0.12)
    tc_line = eq(r"T_c", cfg.FONT["title"], cfg.CRITICAL).move_to([-5.6, 2.6, 0])
    tc_note = txt("above it, no squeezing makes a liquid", cfg.FONT["small"], cfg.WHITE).next_to(tc_line, DOWN, buff=0.2)
    tc_note.align_to(tc_line, LEFT)
    scene.play(GrowArrow(axis), FadeIn(ticks), FadeIn(unit), run_time=1.2)
    scene.play(FadeIn(tc_line, shift=DOWN * 0.1), Create(room), FadeIn(room_tag), run_time=1.2)
    play_in(scene, t, 3, FadeIn(tc_note, shift=UP * 0.1), run_time=1.0)

    def marker(gas: str, color: str) -> VGroup:
        T = pm.CRITICAL[gas][0]
        dot = glow_dot([kx(T), AXIS_Y, 0], color, radius=0.13)
        stem = Line([kx(T), AXIS_Y + 0.15, 0], [kx(T), 0.45, 0], stroke_color=color, stroke_width=3, stroke_opacity=0.8)
        return VGroup(stem, dot)

    # --- 3. Carbon dioxide: just above room temperature ------------------------------------------------------------------------
    beat(scene, t, 3)
    co2_T = pm.CRITICAL["CO2"][0]
    co2 = marker("CO2", cfg.GAS_COLORS["CO2"])
    co2_mol = molecule_stage([kx(co2_T) + 0.45, 1.45, 0], [("O", (-1.16, 0, 0)), ("C", (0, 0, 0)), ("O", (1.16, 0, 0))],
                             [(0, 1), (1, 2)], scale=0.62)
    co2_tag = VGroup(txt("CO₂", cfg.FONT["label"], cfg.GAS_COLORS["CO2"]),
                     txt(f"{fx(pm.celsius(co2_T), 0)} °C", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.06)
    co2_tag.move_to([kx(co2_T) + 1.25, 0.05, 0])
    scene.play(FadeIn(co2, shift=DOWN * 0.2), FadeOut(tc_note), run_time=0.8)
    show(scene, co2_mol, 0.8, FadeIn(co2_tag, shift=LEFT * 0.1))
    at_word(scene, t, 3, "just", lead=0.3)
    gap = Brace(Line([kx(pm.ROOM_T), AXIS_Y, 0], [kx(co2_T), AXIS_Y, 0]), DOWN, buff=0.55, color=cfg.GOLD)
    scene.play(GrowFromCenter(gap), run_time=0.8)
    at_word(scene, t, 3, "liquefy", lead=0.3)
    works = VGroup(txt("squeeze at room T", cfg.FONT["small"], cfg.WHITE), check_mark(0.22)).arrange(RIGHT, buff=0.18)
    works.move_to([kx(co2_T) + 1.7, -2.45, 0])
    play_in(scene, t, 4, FadeIn(works, shift=UP * 0.1), run_time=1.0)

    # --- 4. Nitrogen: far below; it must be cooled first --------------------------------------------------------------------------
    beat(scene, t, 4)
    n2_T = pm.CRITICAL["N2"][0]
    n2 = marker("N2", cfg.GAS_COLORS["N2"])
    n2_mol = molecule_stage([kx(n2_T), 1.45, 0], [("N", (-0.55, 0, 0)), ("N", (0.55, 0, 0))], [(0, 1)], scale=0.7)
    n2_tag = VGroup(txt("N₂", cfg.FONT["label"], cfg.GAS_COLORS["N2"]),
                    txt(f"{fx(n2_T, 0)} K = {fx(pm.celsius(n2_T), 0)} °C".replace("-", "−"), cfg.FONT["small"], cfg.WHITE))
    n2_tag.arrange(DOWN, buff=0.06).move_to([kx(n2_T) + 1.55, 0.05, 0])
    scene.play(FadeIn(n2, shift=DOWN * 0.2), run_time=0.8)
    show(scene, n2_mol, 0.8, FadeIn(n2_tag, shift=RIGHT * 0.1))
    at_word(scene, t, 4, "squeezing", lead=0.3)
    fails = VGroup(txt("squeeze at room T", cfg.FONT["small"], cfg.WHITE), cross_mark(0.2)).arrange(RIGHT, buff=0.18)
    fails.move_to([kx(n2_T) + 0.6, -2.45, 0])
    scene.play(FadeIn(fails, shift=UP * 0.1), run_time=0.9)
    at_word(scene, t, 4, "cooled", lead=0.3)
    first = Arrow([kx(pm.ROOM_T) - 0.2, -3.2, 0], [kx(n2_T) + 0.1, -3.2, 0], buff=0, stroke_width=6,
                               color=cfg.COLD_COLOR, max_tip_length_to_length_ratio=0.06)
    first_tag = txt("cool first", cfg.FONT["label"], cfg.COLD_COLOR).next_to(first, DOWN, buff=0.12)
    play_in(scene, t, 5, GrowArrow(first), FadeIn(first_tag), run_time=1.2)

    # --- 5. Ammonia: higher still; hydrogen bonds ---------------------------------------------------------------------------------
    beat(scene, t, 5)
    nh3_T = pm.CRITICAL["NH3"][0]
    nh3 = marker("NH3", cfg.GAS_COLORS["NH3"])
    nh3_mol = molecule_stage([kx(nh3_T), 1.5, 0], ammonia_atoms(), [(0, 1), (0, 2), (0, 3)], scale=1.0)
    nh3_tag = VGroup(txt("NH₃", cfg.FONT["label"], cfg.GAS_COLORS["NH3"]),
                     txt(f"{fx(nh3_T, 1)} K", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.06)
    nh3_tag.move_to([kx(nh3_T) + 1.15, 0.05, 0])
    scene.play(FadeIn(nh3, shift=DOWN * 0.2), run_time=0.8)
    show(scene, nh3_mol, 0.8, FadeIn(nh3_tag, shift=LEFT * 0.1))
    at_word(scene, t, 5, "hydrogen", lead=0.3)
    hb = chip("hydrogen bonds", cfg.ATTRACT, cfg.FONT["small"]).move_to([kx(nh3_T) + 0.9, 2.75, 0])
    play_in(scene, t, 6, FadeIn(hb, shift=DOWN * 0.1), run_time=0.9)

    # --- 6. Stronger attraction, higher critical temperature ------------------------------------------------------------------------
    beat(scene, t, 6)
    for st in (co2_mol, n2_mol, nh3_mol):
        for member in st.get_family():
            member.clear_updaters()
    clear(scene, run_time=0.9)
    gases = ("H2", "N2", "O2", "CO2", "NH3", "H2O")
    names = {"H2": "H₂", "N2": "N₂", "O2": "O₂", "CO2": "CO₂", "NH3": "NH₃", "H2O": "H₂O"}
    axes = plot_axes((0, 210), (0, 700), x_length=9.0, y_length=5.4, at=[-0.3, -0.35, 0], x_label=r"a/b", y_label="T_c",
                     x_color=cfg.ATTRACT, y_color=cfg.CRITICAL, x_ticks=(50, 100, 150, 200), y_ticks=(200, 400, 600))
    scene.play(Create(axes), run_time=1.2)
    dots = VGroup()
    offsets = {"H2": UR, "N2": DR, "O2": UL, "CO2": UL, "NH3": UL, "H2O": LEFT}
    for g in gases:
        a = pm.VDW[g][0] / pm.VDW[g][1]
        T = pm.CRITICAL[g][0]
        d = glow_dot(axes.c2p(a, T), cfg.GAS_COLORS.get(g, cfg.ROSE), radius=0.12)
        lab = txt(names[g], cfg.FONT["small"], cfg.GAS_COLORS.get(g, cfg.ROSE)).next_to(d, offsets[g], buff=0.08)
        dots.add(VGroup(d, lab))
    scene.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.25), run_time=2.4)
    at_word(scene, t, 6, "balance", lead=0.3)
    trend = arrow2d_trend(axes)
    msg = txt("van der Waals: T_c = 8a / 27Rb", cfg.FONT["label"], cfg.WHITE).move_to([-0.3, 3.45, 0])
    scene.play(GrowArrow(trend), FadeIn(msg, shift=DOWN * 0.1), run_time=1.4)
    finish(scene, t, fill=lambda s: [Indicate(dots, color=cfg.WHITE, scale_factor=1.05)])


def arrow2d_trend(axes: Axes) -> Arrow:
    return Arrow(axes.c2p(18, 60), axes.c2p(180, 640), buff=0, stroke_width=6, color=cfg.GOLD, stroke_opacity=0.6,
                 max_tip_length_to_length_ratio=0.05)
