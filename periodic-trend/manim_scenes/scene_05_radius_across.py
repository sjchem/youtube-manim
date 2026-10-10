"""Experiment 1: walk across period 2 while the graph draws itself.

The cloud on the left and the point on the right always show the same
number (NCERT atomic radius). The honest note is drawn, not just said: the
covalent-only data set (Cordero 2008) is overlaid as a dashed line, and it
falls the same way. Period 3 then repeats the walk one shell further out.
"""

from manim_scenes.common import *

PERIOD_2 = ("Li", "Be", "B", "C", "N", "O", "F")
PERIOD_3 = ("Na", "Mg", "Al", "Si", "P", "S", "Cl")
SCALE = 0.0105
ATOM_AT = np.array([-4.75, 0.45, 0])
AXES_AT = np.array([2.95, -0.05, 0])


class Scene05RadiusAcross(Scene):
    def construct(self) -> None:
        play_scene(self)


def radius_of(symbol: str) -> float:
    return ed.ATOMIC_RADII_PM[symbol] * SCALE


def core_of(symbol: str) -> float:
    n = pm.outer_shell(pm.z_of(symbol))
    return radius_of(symbol) * (0.25 + 0.07 * (n - 2))


def readout(symbol: str, value: int, color: str = cfg.WHITE) -> VGroup:
    name = txt(symbol, cfg.FONT["title"], block_color(pm.z_of(symbol)))
    amount = txt(f"{value} pm", cfg.FONT["title"], color)
    return VGroup(name, amount).arrange(RIGHT, buff=0.45).move_to(ATOM_AT[0] * RIGHT + DOWN * 2.75)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Experiment 1: across period 2")

    axes = trend_axes(7.4, 5.0, 210, 35, x_count=7).move_to(AXES_AT)
    unit = txt("radius (pm)", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(0, 210), RIGHT, buff=0.3)
    labels2 = VGroup(*[txt(s, cfg.FONT["small"], block_color(pm.z_of(s))).next_to(axes.c2p(i + 1, 0), DOWN, buff=0.2)
                       for i, s in enumerate(PERIOD_2)])
    atom = Atom(radius_of("Li"), ATOM_AT, charge="+3", core=core_of("Li"), count=380, seed=51, nucleus_radius=0.3)
    scene.play(Create(axes), FadeIn(unit), LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labels2], lag_ratio=0.1),
               run_time=1.6)
    scene.play(FadeIn(atom, scale=0.6), run_time=1.2)

    # --- Lithium ---------------------------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    points = [axes.c2p(i + 1, ed.ATOMIC_RADII_PM[s]) for i, s in enumerate(PERIOD_2)]
    dots = [glow_dot(p, 0.09, cfg.CYAN) for p in points]
    value = readout("Li", ed.ATOMIC_RADII_PM["Li"])
    scene.play(FadeIn(dots[0], scale=0.4), FadeIn(value, shift=UP * 0.15), run_time=0.9)
    guide = DashedLine(axes.c2p(0, 152), points[0], stroke_color=cfg.CYAN, stroke_width=2, dash_length=0.08)
    scene.play(Create(guide), run_time=0.6)
    tiny = eq(r"1\,\mathrm{pm} = 10^{-12}\,\mathrm{m}", cfg.FONT["small"], cfg.MUTED).move_to([-4.75, -3.75, 0])
    scene.play(FadeIn(tiny, shift=UP * 0.1), run_time=0.8)

    # --- Beryllium: one more proton, same shell ------------------------------------------------
    beat(scene, t, 2)
    plus = VGroup(chip("+1 proton", cfg.PROTON_COLOR, cfg.FONT["small"]),
                  chip("electron: same shell", cfg.CYAN, cfg.FONT["small"])).arrange(DOWN, buff=0.18)
    plus.move_to([-4.75, 2.35, 0])
    scene.play(*relabel_nucleus(atom, "+4"), FadeIn(plus, shift=DOWN * 0.15), FadeOut(guide), run_time=1.0)
    scene.play(Flash(atom.center_point(), color=cfg.PROTON_COLOR, flash_radius=0.55, num_lines=12), run_time=0.8)

    beat(scene, t, 3)
    segments = VGroup()

    def step(index: int, run_time: float) -> None:
        nonlocal value
        symbol = PERIOD_2[index]
        new_value = readout(symbol, ed.ATOMIC_RADII_PM[symbol])
        segment = glow_polyline([points[index - 1], points[index]], cfg.CYAN, 4)
        segments.add(segment)
        animations = [*atom.resize(radius_of(symbol), core_of(symbol)), Create(segment),
                      FadeIn(dots[index], scale=0.4), FadeThrough(value, new_value)]
        if index > 1:
            animations += relabel_nucleus(atom, f"+{pm.z_of(symbol)}")
        scene.play(*animations, run_time=run_time)
        value = new_value

    step(1, 1.6)

    # --- Boron to fluorine --------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(plus), run_time=0.4)
    for index in range(2, 7):
        step(index, 1.55)

    beat(scene, t, 5)
    arrows = pull_arrows(atom.center_point(), radius_of("F"), pm.slater_zeff(9), count=8)
    felt = VGroup(eq(r"Z_{\mathrm{eff}}", cfg.FONT["label"], cfg.ZEFF_COLOR),
                  txt("rises", cfg.FONT["label"], cfg.ZEFF_COLOR)).arrange(RIGHT, buff=0.2).move_to([-4.75, 3.0, 0])
    scene.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), FadeIn(felt), run_time=1.2)
    scene.play(*atom.resize(radius_of("F") * 0.9), run_time=1.0, rate_func=there_and_back)

    # --- Less than half --------------------------------------------------------------------------------
    beat(scene, t, 6)
    ghost = DashedVMobject(Circle(radius=radius_of("Li"), stroke_color=cfg.MUTED, stroke_width=3), num_dashes=44)
    ghost.move_to(atom.center_point())
    half = chip('F < half of Li', cfg.GOLD, cfg.FONT["small"]).move_to([-4.75, 3.0, 0])
    scene.play(FadeOut(arrows), *fade_labels(felt, half), Create(ghost), run_time=1.2)
    scene.play(Indicate(value, color=cfg.GOLD, scale_factor=1.06), run_time=1.0)

    # --- The graph falls ------------------------------------------------------------------------------------
    beat(scene, t, 7)
    fall = glow_arrow(axes.c2p(1.2, 190), axes.c2p(6.6, 95), cfg.GOLD, 6)
    scene.play(GrowArrow(fall.arrow), FadeIn(fall[0]), run_time=1.0)
    scene.play(LaggedStart(*[Indicate(d, color=cfg.WHITE, scale_factor=1.5) for d in dots], lag_ratio=0.12),
               run_time=1.6)

    # --- An honest note: two measuring methods ------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(fall), FadeOut(half), FadeOut(ghost), run_time=0.6)
    metal_brace = Brace(VGroup(labels2[0], labels2[1]), DOWN, color=cfg.BLUE, buff=0.1)
    metal_tag = txt("metallic", cfg.FONT["tiny"], cfg.BLUE).next_to(metal_brace, DOWN, buff=0.1)
    cov_brace = Brace(VGroup(*labels2[2:]), DOWN, color=cfg.GREEN, buff=0.1)
    cov_tag = txt("covalent", cfg.FONT["tiny"], cfg.GREEN).next_to(cov_brace, DOWN, buff=0.1)
    scene.play(GrowFromCenter(metal_brace), FadeIn(metal_tag), run_time=0.8)
    scene.play(GrowFromCenter(cov_brace), FadeIn(cov_tag), run_time=0.8)
    bond = VGroup(txt("measured from", cfg.FONT["small"], cfg.MUTED),
                  txt("bonded atoms", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.1).move_to([-4.75, 2.8, 0])
    scene.play(FadeIn(bond, shift=DOWN * 0.15), run_time=0.8)

    beat(scene, t, 9)
    covalent = [axes.c2p(i + 1, ed.COVALENT_RADII_PM[s]) for i, s in enumerate(PERIOD_2)]
    dashed = DashedVMobject(VMobject(stroke_color=cfg.MUTED, stroke_width=4).set_points_as_corners(covalent),
                            num_dashes=40)
    cov_dots = VGroup(*[Dot(p, radius=0.07, fill_color=cfg.MUTED) for p in covalent])
    key = VGroup(
        VGroup(Line(ORIGIN, RIGHT * 0.6, stroke_color=cfg.CYAN, stroke_width=5), txt("textbook", cfg.FONT["tiny"], cfg.CYAN)).arrange(RIGHT, buff=0.2),
        VGroup(DashedLine(ORIGIN, RIGHT * 0.6, stroke_color=cfg.MUTED, stroke_width=4, dash_length=0.1),
               txt("covalent only", cfg.FONT["tiny"], cfg.MUTED)).arrange(RIGHT, buff=0.2),
    ).arrange(DOWN, buff=0.26, aligned_edge=LEFT).move_to(axes.c2p(5.7, 185))
    scene.play(Create(dashed), FadeIn(cov_dots), FadeIn(key), run_time=1.6)
    same = VGroup(check_mark(0.24), txt("same trend", cfg.FONT["small"], cfg.GREEN)).arrange(RIGHT, buff=0.2)
    same.move_to([-4.75, 3.05, 0])
    scene.play(*fade_labels(bond, same), run_time=0.8)

    # --- Period 3 ---------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    head = swap_heading(scene, head, "Period 3: the same walk")
    scene.play(FadeOut(VGroup(dashed, cov_dots, key, same, metal_brace, metal_tag, cov_brace, cov_tag, tiny)),
               segments.animate.fade(0.6), *[d.animate.fade(0.6) for d in dots],
               labels2.animate.fade(0.55), run_time=0.8)
    labels3 = VGroup(*[txt(s, cfg.FONT["small"], cfg.GOLD).next_to(labels2[i], DOWN, buff=0.18)
                       for i, s in enumerate(PERIOD_3)])
    points3 = [axes.c2p(i + 1, ed.ATOMIC_RADII_PM[s]) for i, s in enumerate(PERIOD_3)]
    dots3 = [glow_dot(p, 0.09, cfg.GOLD) for p in points3]
    new_value = readout("Na", ed.ATOMIC_RADII_PM["Na"])
    scene.play(FadeIn(labels3), *atom.resize(radius_of("Na"), core_of("Na")), *relabel_nucleus(atom, "+11"),
               FadeThrough(value, new_value), FadeIn(dots3[0], scale=0.4), run_time=1.0)
    value = new_value
    line3 = glow_polyline(points3, cfg.GOLD, 4)
    final_value = readout("Cl", ed.ATOMIC_RADII_PM["Cl"])
    scene.play(Create(line3), LaggedStart(*[FadeIn(d, scale=0.4) for d in dots3[1:]], lag_ratio=0.3),
               *atom.resize(radius_of("Cl"), core_of("Cl")), *relabel_nucleus(atom, "+17"),
               FadeThrough(value, final_value), run_time=3.2)
    value = final_value

    beat(scene, t, 11)
    wins = VGroup(txt('Stronger nuclear', cfg.FONT["label"], cfg.GOLD),
                  txt('attraction', cfg.FONT["label"], cfg.GOLD)).arrange(DOWN, buff=0.12).move_to([-4.75, 2.75, 0])
    scene.play(FadeIn(wins, shift=DOWN * 0.15), run_time=0.8)
    scene.play(Indicate(line3, color=cfg.WHITE), Indicate(segments, color=cfg.WHITE), run_time=1.4)

    # --- What about down? -------------------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(FadeOut(VGroup(wins, atom)), FadeOut(value), run_time=0.7)
    down = glow_arrow([-6.0, 2.2, 0], [-6.0, -1.6, 0], cfg.CYAN, 8, tip=0.36)
    ask = txt("and down?", cfg.FONT["title"], cfg.CYAN).next_to(down, RIGHT, buff=0.35)
    scene.play(GrowArrow(down.arrow), FadeIn(down[0]), FadeIn(ask, shift=DOWN * 0.15), run_time=1.0)
    scene.play(Wiggle(ask), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
