"""How hard is it to steal an electron? Lithium versus neon, with meters.

Both meters fill at the same rate; each electron escapes exactly when its
meter reaches the measured first ionization enthalpy (NIST, kJ/mol). The
cloud sizes here are schematic extents of the outermost orbital (lithium's
2s reaches much farther than neon's 2p), not measured radii.
"""

from manim_scenes.common import *

LI_AT = np.array([-5.35, 0.2, 0])
NE_AT = np.array([1.95, 0.2, 0])
LI_METER_X = -1.85
NE_METER_X = 5.75
METER_Y = -0.25
RATE = 145.0     # kJ/mol per second while the energy pours in


class Scene09Ionization(Scene):
    def construct(self) -> None:
        play_scene(self)


def readout_for(meter: EnergyMeter, x: float) -> VGroup:
    value = number(0, cfg.FONT["label"], cfg.GOLD)
    unit = txt("kJ/mol", cfg.FONT["tiny"], cfg.MUTED)
    group = VGroup(value, unit).arrange(RIGHT, buff=0.24, aligned_edge=DOWN)
    group.move_to([x, 3.0, 0])

    def follow(mob: VGroup) -> None:
        mob[0].set_value(round(meter.value))
        mob.arrange(RIGHT, buff=0.24, aligned_edge=DOWN).move_to([x, 3.0, 0])

    group.add_updater(follow)
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "09", 'Removing an electron')

    # --- 1. Hypothesis -----------------------------------------------------------------------
    atom = Atom(1.3, [-3.4, 0.2, 0], charge="+", core=0.4, count=360, seed=91)
    electron = glow_dot(atom.center_point() + RIGHT * 1.0 + UP * 0.35, 0.14)
    pull = pull_arrows(atom.center_point(), 1.3, 4.5, count=6)
    scene.play(FadeIn(atom, scale=0.6), run_time=1.0)
    scene.play(FadeIn(electron, scale=0.4), FadeIn(pull), run_time=0.8)
    guess = VGroup(txt("close + strong pull", cfg.FONT["body"], cfg.GOLD), eq(r"\Rightarrow", cfg.FONT["body"]),
                   txt("harder to remove?", cfg.FONT["body"], cfg.WHITE)).arrange(DOWN, buff=0.2).move_to([3.2, 0.2, 0])
    scene.play(FadeIn(guess, shift=LEFT * 0.2), run_time=1.0)

    # --- 2. Definition: isolated, gas phase -----------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    box = DashedVMobject(RoundedRectangle(width=4.6, height=4.6, corner_radius=0.3, stroke_color=cfg.MUTED,
                                          stroke_width=3), num_dashes=60).move_to(atom.center_point())
    gas = txt('Isolated gas-phase atom', cfg.FONT["small"], cfg.MUTED).next_to(box, DOWN, buff=0.22)
    name = VGroup(txt("first ionization enthalpy", cfg.FONT["body"], cfg.GOLD),
                  txt('remove one electron · gas phase', cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.2)
    name.move_to([3.2, 0.2, 0])
    scene.play(FadeOut(guess), Create(box), FadeIn(gas), run_time=1.0)
    scene.play(FadeIn(name, shift=LEFT * 0.2), run_time=0.9)
    _, path = escape_electron(electron.get_center(), np.array([0.6, 2.9, 0]))
    scene.play(MoveAlongPath(electron, path), run_time=1.3, rate_func=rush_into)

    # --- 3. The equation ---------------------------------------------------------------------------
    beat(scene, t, 2)
    equation = eq(r"\mathrm{X(g)} \;\rightarrow\; \mathrm{X^{+}(g)} + e^{-}", 62, cfg.WHITE).move_to([0, -0.2, 0])
    frame = glow_frame(equation, cfg.WHITE, buff=0.3)
    scene.play(FadeOut(VGroup(atom, pull, box, gas, name, electron)), run_time=0.7)
    scene.play(Write(equation), Create(frame), run_time=1.5)

    # --- 4. Lithium versus neon ------------------------------------------------------------------------
    beat(scene, t, 3)
    head = swap_heading(scene, head, "Lithium vs neon: same shell")
    scene.play(FadeOut(equation), FadeOut(frame), run_time=0.6)
    lithium = Atom(1.6, LI_AT, charge="+3", core=0.32, count=200, core_count=140, seed=92, glow=0.12)
    neon = Atom(0.72, NE_AT, charge="+10", core=0.15, count=440, core_count=90, seed=93, glow=0.22)
    li_meter = EnergyMeter(height=5.2).move_to([LI_METER_X, METER_Y, 0])
    ne_meter = EnergyMeter(height=5.2).move_to([NE_METER_X, METER_Y, 0])
    names = VGroup(txt("lithium", cfg.FONT["label"], cfg.BLUE).move_to([LI_AT[0], -2.75, 0]),
                   txt("neon", cfg.FONT["label"], cfg.GREEN).move_to([NE_AT[0], -2.75, 0]))
    scene.play(FadeIn(lithium, scale=0.6), FadeIn(neon, scale=0.6), FadeIn(names), run_time=1.2)
    scene.play(FadeIn(li_meter), FadeIn(ne_meter), run_time=0.8)
    li_e = glow_dot(LI_AT + 1.25 * np.array([np.cos(0.5), np.sin(0.5), 0]), 0.14)
    ne_e = glow_dot(NE_AT + 0.6 * np.array([np.cos(0.5), np.sin(0.5), 0]), 0.14)
    scene.play(FadeIn(li_e, scale=0.4), FadeIn(ne_e, scale=0.4), run_time=0.6)

    # --- 5. Pour in energy -----------------------------------------------------------------------------
    beat(scene, t, 4)
    li_read, ne_read = readout_for(li_meter, LI_METER_X), readout_for(ne_meter, NE_METER_X)
    scene.add(li_read, ne_read)
    li_ie, ne_ie = ed.ionization_kj("Li"), ed.ionization_kj("Ne")
    scene.play(li_meter.fill_to(li_ie, rate_func=linear), ne_meter.fill_to(li_ie, rate_func=linear),
               run_time=li_ie / RATE)

    # --- 6. Lithium lets go ------------------------------------------------------------------------------
    beat(scene, t, 5)
    _, li_path = escape_electron(li_e.get_center(), np.array([-3.0, 3.6, 0]))
    level = DashedLine(li_meter.level_point(li_ie) + LEFT * 0.45, li_meter.level_point(li_ie) + RIGHT * 0.45,
                       stroke_color=cfg.WHITE, stroke_width=3)
    scene.play(MoveAlongPath(li_e, li_path), lithium.cloud.fade_to(0.15), Create(level), run_time=1.3, rate_func=rush_into)
    gone = chip("escaped!", cfg.GREEN, cfg.FONT["small"]).move_to(LI_AT + UP * 2.2)
    scene.play(FadeIn(gone, scale=1.2), run_time=0.6)
    li_read.clear_updaters()

    # --- 7. Neon holds on ----------------------------------------------------------------------------------
    beat(scene, t, 6)
    holding = chip("still held", cfg.ORANGE, cfg.FONT["small"]).move_to(NE_AT + UP * 2.2)
    scene.play(FadeIn(holding, scale=1.1), run_time=0.5)
    for target in (1000, 1500, 2000):
        scene.play(ne_meter.fill_to(target, rate_func=linear), ne_e.animate(rate_func=there_and_back).shift(UR * 0.12),
                   run_time=(target - ne_meter.value) / (RATE * 1.65))

    # --- 8. Neon lets go, at four times the energy ---------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(ne_meter.fill_to(ne_ie, rate_func=linear), run_time=0.8)
    _, ne_path = escape_electron(ne_e.get_center(), np.array([4.0, 3.6, 0]))
    scene.play(MoveAlongPath(ne_e, ne_path), FadeOut(holding), run_time=1.2, rate_func=rush_into)
    ne_read.clear_updaters()
    four = chip(f"≈ {ne_ie / li_ie:.0f} × the energy", cfg.GOLD, cfg.FONT["label"]).move_to([NE_AT[0], 2.2, 0])
    scene.play(FadeIn(four, scale=1.2), run_time=0.7)
    scene.play(Indicate(ne_read, color=cfg.WHITE), run_time=1.0)

    # --- 9. Why: distance and felt charge ------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(gone, four)), lithium.cloud.fade_to(1.0), run_time=0.7)
    li_pull = pull_arrows(LI_AT, 1.6, pm.slater_zeff(3), count=6)
    ne_pull = pull_arrows(NE_AT, 0.72, pm.slater_zeff(10), count=6)
    li_tag = VGroup(txt("far out", cfg.FONT["small"], cfg.CYAN), txt("weak", cfg.FONT["small"], cfg.ZEFF_COLOR),
                    eq(r"Z_{\mathrm{eff}}", cfg.FONT["small"], cfg.ZEFF_COLOR))
    li_tag[1:].arrange(RIGHT, buff=0.15)
    li_tag.arrange(DOWN, buff=0.15).move_to(LI_AT + UP * 2.45)
    ne_tag = VGroup(txt("close in", cfg.FONT["small"], cfg.CYAN), txt("strong", cfg.FONT["small"], cfg.ZEFF_COLOR),
                    eq(r"Z_{\mathrm{eff}}", cfg.FONT["small"], cfg.ZEFF_COLOR))
    ne_tag[1:].arrange(RIGHT, buff=0.15)
    ne_tag.arrange(DOWN, buff=0.15).move_to(NE_AT + UP * 2.2)
    scene.play(LaggedStart(*[GrowArrow(a) for a in li_pull], lag_ratio=0.1), FadeIn(li_tag), run_time=1.2)
    scene.play(LaggedStart(*[GrowArrow(a) for a in ne_pull], lag_ratio=0.1), FadeIn(ne_tag), run_time=1.2)

    # --- 10. One trend explains another ---------------------------------------------------------------------------
    beat(scene, t, 9)
    chain = VGroup(chip("smaller atom", cfg.CYAN, cfg.FONT["small"]), chip("tighter grip", cfg.GOLD, cfg.FONT["small"]),
                   chip('higher ionization', cfg.GREEN, cfg.FONT["small"])).arrange(RIGHT, buff=0.7)
    fit_width(chain, 13.6)
    chain.move_to([0, -3.75, 0])
    links = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.08, color=cfg.MUTED, stroke_width=4,
                           max_tip_length_to_length_ratio=0.35) for i in range(2)])
    scene.play(FadeOut(names), LaggedStart(*[AnimationGroup(FadeIn(c, shift=UP * 0.15), *([GrowArrow(links[i - 1])] if i else []))
                                             for i, c in enumerate(chain)], lag_ratio=0.4), run_time=2.0)

    # --- 11. Every element? ------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    every = chip("now: every element", cfg.GOLD, cfg.FONT["body"]).move_to([0, 2.95, 0])
    scene.play(*fade_labels(VGroup(li_tag, ne_tag, li_read, ne_read), every), run_time=0.9)
    scene.play(Circumscribe(every, color=cfg.GOLD), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
