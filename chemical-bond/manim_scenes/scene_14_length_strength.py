"""Bond length and strength: what the valley's position and depth mean.

Every well is a Morse curve whose minimum sits at a measured bond length and
whose depth is a measured (or, for carbon-carbon, average) bond enthalpy from
``utils.bond_data``. The width parameters are illustrative; for F2 and Cl2
they follow the molecules' vibrational constants, which is why the fluorine
well is narrower as well as shallower. The vibration and the spring are a
picture of the same curve: stretch costs energy, compression meets the wall.
"""

from manim_scenes.common import *

BAND_Y = 2.45
PM = 1 / 50
CC = (("C-C", 1, cfg.CYAN, 0.019), ("C=C", 2, cfg.BLUE, 0.021), ("C#C", 3, cfg.PURPLE, 0.023))
HALOGEN = (("F-F", "F", cfg.GREEN, 0.029), ("Cl-Cl", "Cl", cfg.TEAL, 0.020))
CARBON = "#B7C4CF"


class Scene14LengthStrength(Scene):
    def construct(self) -> None:
        play_scene(self)


def well(plot: EnergyPlot, key: str, a: float, color: str, width: float = 6) -> VGroup:
    """A Morse well through the measured length and energy of ``key``."""
    depth, r_e = bd.BOND_ENTHALPY_KJ[key], bd.BOND_LENGTH_PM[key]
    start_r = max(bm.morse_inverse(plot.e_max, depth, r_e, a), 1.0)
    line = plot.axes.plot(lambda r: float(bm.morse(r, depth, r_e, a)), x_range=[start_r, plot.r_max, 0.5], color=color,
                          stroke_width=width, use_smoothing=False)
    glow = line.copy().set_stroke(color, width=width * 3.2, opacity=0.15)
    group = VGroup(glow, line)
    group.bottom = plot.axes.c2p(r_e, -depth)
    return group


def molecule(order: int, symbol: str = "C", color: str = CARBON) -> VGroup:
    left = VGroup(polished_ball(0.36, color), txt(symbol, cfg.FONT["tiny"], cfg.BG))
    right = left.copy()
    left.move_to(LEFT * 0.85)
    right.move_to(RIGHT * 0.85)
    for part in (left, right):
        part[1].move_to(part[0])
    bonds = VGroup()
    for j in range(order):
        y = (j - (order - 1) / 2) * 0.18
        # Cylindrical shading continues underneath the spheres, joining them.
        rod = VGroup(*[Line(LEFT * 0.85 + UP * y, RIGHT * 0.85 + UP * y,
                           stroke_color=interpolate_color(ManimColor("#354858"), ManimColor("#E1EDF5"), k / 8),
                           stroke_width=float(width))
                       for k, width in enumerate(np.linspace(10, 1.8, 9))])
        bonds.add(rod)
    return VGroup(bonds, left, right)


def curve_bead(point, radius: float, color: str) -> VGroup:
    """A shaded sphere with a faint halo, centred on the curve itself."""
    return VGroup(halo(radius * 2.8, color, layers=6, peak_opacity=0.13),
                  polished_ball(radius, color)).move_to(point)


def clear_energy_title(plot: EnergyPlot) -> None:
    """Keep units above the plotting area and clear of the repulsive wall."""
    plot.y_title.next_to(plot.axes.c2p(0, plot.e_max), UP, buff=0.3)
    plot.y_title.align_to(plot.axes.y_axis, LEFT)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "Bond length and strength")

    # --- 1. The valley again: two numbers ------------------------------------------------------------------------
    r = ValueTracker(H2[1])
    plot = EnergyPlot(center=DOWN * 1.5, x_length=11.0, y_length=4.2)
    plot.shift(RIGHT * 0.3)
    clear_energy_title(plot)
    cloud = bind_pair(PairCloud(LEFT, RIGHT, 0.85, count=440, seed=141, share=1.0, glow=0.14), lambda: r.get_value() * PM,
                      UP * BAND_Y + RIGHT * 0.3)
    scene.add(cloud)
    nuclei = pair_nuclei(cloud, ("+", "+"), radius=0.2, polished=True)
    # Rear samples sit behind the bodies; nearer samples cross their fronts.
    # Keep the cloud controller ahead of its negative-z children in Cairo.
    cloud.set_z_index(-6, family=False)
    for glow in cloud.glows:
        glow.set_z_index(-5)
    for index, samples in enumerate(cloud.dots):
        samples.set_z_index(-4 if index < len(cloud.dots) // 2 else -2)
    for core in nuclei:
        core.set_z_index(-3)
        core.label.set_z_index(0)
    marker = curve_bead(plot.point(r.get_value()), 0.15, cfg.ENERGY)
    marker.add_updater(lambda m: m.move_to(plot.point(r.get_value())))
    scene.play(Create(plot.axes), FadeIn(plot.frame_lines), FadeIn(plot.labels), Create(plot.curve), run_time=1.4)
    scene.play(FadeIn(cloud), FadeIn(nuclei), FadeIn(marker, scale=0.5), run_time=0.9)
    dismiss_opening_title(scene, t, head)

    # --- 2. Position of the bottom: bond length ----------------------------------------------------------------------
    beat(scene, t, 1)
    drop = plot.minimum_marks()
    span = DoubleArrow(plot.axes.c2p(0, plot.e_min + 60), plot.axes.c2p(H2[1], plot.e_min + 60), buff=0, color=cfg.WHITE,
                       stroke_width=5, tip_length=0.18)
    length_tag = txt("bond length", cfg.FONT["label"], cfg.WHITE).next_to(plot.axes.c2p(H2[1], plot.e_min + 60), RIGHT, buff=0.25)
    scene.play(Create(drop), run_time=0.7)
    scene.play(GrowFromCenter(span), FadeIn(length_tag, shift=LEFT * 0.1), run_time=1.0)

    # --- 3. Depth: bond dissociation energy ---------------------------------------------------------------------------
    beat(scene, t, 2)
    depth = plot.depth_arrow()
    energy_tag = VGroup(txt("bond dissociation", cfg.FONT["label"], cfg.ENERGY), txt("energy", cfg.FONT["label"], cfg.ENERGY))
    energy_tag.arrange(DOWN, buff=0.08).move_to(plot.axes.c2p(250, -430))
    scene.play(GrowFromCenter(depth), run_time=0.9)
    scene.play(FadeIn(energy_tag, shift=LEFT * 0.1), run_time=0.8)

    # --- 4. Deep valley strong, shallow valley weak ------------------------------------------------------------------------
    beat(scene, t, 3)
    shallow_line = plot.axes.plot(lambda x: float(bm.morse(x, 180, 120, 0.016)), x_range=[bm.morse_inverse(plot.e_max, 180, 120, 0.016), 320, 0.5],
                                  color=cfg.MUTED, stroke_width=6, use_smoothing=False)
    strong = txt("strong", cfg.FONT["label"], cfg.ENERGY).next_to(plot.point(H2[1]), DOWN, buff=0.15)
    weak = txt("weak", cfg.FONT["label"], cfg.MUTED).next_to(plot.axes.c2p(140, -180), UP, buff=0.12).shift(RIGHT * 0.6)
    scene.play(FadeOut(energy_tag), FadeOut(span), FadeOut(length_tag), Create(shallow_line), run_time=1.2)
    scene.play(FadeIn(strong), FadeIn(weak), run_time=0.8)

    # --- 5. Never frozen: vibration about the bottom -------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(shallow_line, strong, weak)), run_time=0.6)
    vibrate = txt("Bond vibration", cfg.FONT["label"], cfg.CYAN).move_to([-4.5, BAND_Y, 0])
    scene.play(FadeIn(vibrate), run_time=0.6)
    for _ in range(5):
        scene.play(track(r, H2[1] + 16), run_time=0.36, rate_func=smooth)
        scene.play(track(r, H2[1] - 9), run_time=0.36, rate_func=smooth)
    scene.play(track(r, H2[1]), run_time=0.3)

    # --- 6. Stretch costs energy; compress meets the wall; a spring ---------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(track(r, H2[1] + 70), run_time=1.6)
    stretch = txt("Stretch: energy in", cfg.FONT["small"], cfg.REQUIRED).next_to(plot.point(H2[1] + 70), RIGHT, buff=0.3)
    scene.play(FadeIn(stretch), run_time=0.6)
    scene.play(track(r, H2[1] - 30), FadeOut(stretch), run_time=1.6)
    squash = txt("Compress: repulsion", cfg.FONT["small"], cfg.REPEL).next_to(plot.point(H2[1] - 30), RIGHT, buff=0.3)
    scene.play(FadeIn(squash), run_time=0.6)
    scene.play(track(r, H2[1]), FadeOut(squash), run_time=1.0)

    def coil() -> VMobject:
        a, b = cloud.ends[0].get_center(), cloud.ends[1].get_center()
        xs = np.linspace(a[0] + 0.22, b[0] - 0.22, 26)
        ys = a[1] + 0.22 * np.array([0 if k in (0, 25) else (1 if k % 2 else -1) for k in range(26)])
        return VMobject(stroke_color=cfg.GOLD, stroke_width=5).set_points_as_corners([[x, y, 0] for x, y in zip(xs, ys)])

    spring = coil()
    spring.add_updater(lambda m: m.become(coil()))
    not_stick = VGroup(txt("not a rigid stick", cfg.FONT["label"], cfg.MUTED), txt("more like a spring", cfg.FONT["label"], cfg.GOLD))
    not_stick.arrange(DOWN, buff=0.15).move_to([4.6, BAND_Y, 0])
    scene.play(cloud.fade_to(0.3), FadeIn(spring), FadeOut(vibrate), FadeIn(not_stick), run_time=0.9)
    for target in (H2[1] + 40, H2[1] - 20, H2[1] + 25, H2[1]):
        scene.play(track(r, target), run_time=0.55, rate_func=smooth)

    # --- 7. Carbon with carbon: single, double, triple ------------------------------------------------------------------------------
    beat(scene, t, 6)
    for mob in (cloud, *nuclei, spring, marker):
        mob.clear_updaters()
    scene.play(FadeOut(VGroup(plot, drop, depth, cloud, nuclei, spring, not_stick, marker)), run_time=0.8)
    cc_plot = EnergyPlot(depth=1, r_e=1, a=1, r_max=320, e_min=-900, e_max=300, x_length=7.6, y_length=5.4, y_step=300,
                         center=[2.75, -0.55, 0], curve=False)
    clear_energy_title(cc_plot)
    rows = VGroup(*[molecule(order) for _, order, _, _ in CC]).arrange(DOWN, buff=0.95).move_to([-4.9, 0.55, 0])
    scene.play(Create(cc_plot.axes), FadeIn(cc_plot.frame_lines), FadeIn(cc_plot.labels), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.2) for row in rows], lag_ratio=0.3), run_time=1.4)

    # --- 8-10. Each one: length and energy, and its well ------------------------------------------------------------------------------
    wells, facts = [], []
    for k, (key, order, colour, a) in enumerate(CC):
        beat(scene, t, 7 + k)
        curve = well(cc_plot, key, a, colour)
        fact = txt(f"{bd.BOND_LENGTH_PM[key]} pm · {bd.BOND_ENTHALPY_KJ[key]} kJ/mol", cfg.FONT["small"], colour)
        fact.next_to(rows[k], DOWN, buff=0.22)
        scene.play(Indicate(rows[k], color=colour, scale_factor=1.08), FadeIn(fact, shift=UP * 0.1), run_time=0.9)
        scene.play(Create(curve), run_time=1.3)
        dot = curve_bead(curve.bottom, 0.13, colour)
        scene.play(FadeIn(dot, scale=0.5), run_time=0.4)
        wells.append(VGroup(curve, dot))
        facts.append(fact)

    # --- 11. Closer and deeper -------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    trend = Arrow(wells[0][1].get_center() + UP * 0.25, wells[2][1].get_center() + UP * 0.15 + RIGHT * 0.1, buff=0.1,
                  color=cfg.WHITE, stroke_width=6, max_tip_length_to_length_ratio=0.15)
    deeper = txt("shorter and stronger", cfg.FONT["label"], cfg.WHITE).move_to([3.7, 3.25, 0])
    scene.play(GrowArrow(trend), FadeIn(deeper), run_time=1.0)
    scene.play(Indicate(VGroup(*[w[1] for w in wells]), color=cfg.WHITE, scale_factor=1.3), run_time=1.0)

    # --- 12. Multiple-bond enthalpies are not simple multiples ------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(trend), FadeOut(deeper), run_time=0.5)
    single, double, triple = (bd.BOND_ENTHALPY_KJ[k] for k in ("C-C", "C=C", "C#C"))
    stack = VGroup(
        eq(rf"{double} \ne 2\times {single}", 48, cfg.BLUE),
        eq(rf"{triple} \ne 3\times {single}", 48, cfg.PURPLE),
    ).arrange(DOWN, buff=0.65).move_to([2.7, 0.1, 0])
    scene.play(FadeIn(stack), FadeOut(cc_plot), *[FadeOut(w) for w in wells], run_time=1.4)
    less = txt("Not simple multiples", cfg.FONT["label"], cfg.GOLD).move_to([2.7, 2.85, 0])
    scene.play(FadeIn(less), run_time=0.7)

    # --- 13. Is shorter always stronger? -------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    # The plot and wells were removed above; fading them twice re-adds them.
    scene.play(FadeOut(VGroup(stack, less, rows, *facts)), run_time=0.8)
    question = txt("shorter = stronger?", cfg.FONT["title"], cfg.GOLD).move_to([0, 0.5, 0])
    scene.play(FadeIn(question, scale=0.9), run_time=0.8)

    # --- 14. Fluorine shorter than chlorine -------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    hx_plot = EnergyPlot(depth=1, r_e=1, a=1, r_max=360, e_min=-300, e_max=200, x_length=7.6, y_length=5.0, y_step=100,
                         center=[2.75, -0.6, 0], curve=False)
    clear_energy_title(hx_plot)
    small_question = txt("Shorter = stronger?", cfg.FONT["small"], cfg.GOLD).move_to([-4.7, 3.1, 0])
    scene.play(*fade_labels(question, small_question), Create(hx_plot.axes), FadeIn(hx_plot.frame_lines),
               FadeIn(hx_plot.labels, rate_func=lambda a: smooth(max((a - 0.55) / 0.45, 0.0))), run_time=1.0)
    question = small_question
    hrows = VGroup(*[molecule(1, sym, colour) for _, sym, colour, _ in HALOGEN]).arrange(DOWN, buff=1.6).move_to([-4.7, 0.2, 0])
    hrows[0].scale(0.85)
    hcurves, hfacts = [], []
    for k, (key, sym, colour, a) in enumerate(HALOGEN):
        curve = well(hx_plot, key, a, colour)
        fact = txt(f"{bd.BOND_LENGTH_PM[key]} pm", cfg.FONT["label"], colour).next_to(hrows[k], DOWN, buff=0.22)
        hcurves.append(curve)
        hfacts.append(fact)
    scene.play(FadeIn(hrows[0], shift=RIGHT * 0.2), FadeIn(hfacts[0]), run_time=0.8)
    scene.play(FadeIn(hrows[1], shift=RIGHT * 0.2), FadeIn(hfacts[1]), run_time=0.8)
    scene.play(Create(hcurves[0]), Create(hcurves[1]), run_time=1.6)

    # --- 15. ... yet weaker ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    energies = VGroup(*[txt(f"{bd.BOND_ENTHALPY_KJ[key]} kJ/mol", cfg.FONT["label"], colour).next_to(hfacts[k], DOWN, buff=0.22)
                        for k, (key, _, colour, _) in enumerate(HALOGEN)])
    scene.play(FadeIn(energies[0]), FadeIn(energies[1]), run_time=0.8)
    f_dot = curve_bead(hcurves[0].bottom, 0.14, cfg.GREEN)
    cl_dot = curve_bead(hcurves[1].bottom, 0.14, cfg.TEAL)
    scene.play(FadeIn(f_dot), FadeIn(cl_dot), run_time=0.5)
    weaker = txt("shorter, yet weaker", cfg.FONT["label"], cfg.GREEN).move_to([3.7, 3.25, 0])
    scene.play(FadeIn(weaker), Indicate(f_dot, color=cfg.WHITE, scale_factor=1.15), run_time=1.0)

    # --- 16. Crowded lone pairs ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    scene.play(FadeOut(VGroup(hx_plot, *hcurves, f_dot, cl_dot, weaker, hrows, *hfacts, energies)), run_time=0.7)
    f_left = LewisAtom("F", {"up": 2, "left": 2, "down": 2}, size=110, center=[-1.15, 0.2, 0], reach=0.24)
    f_right = LewisAtom("F", {"up": 2, "right": 2, "down": 2}, size=110, center=[1.15, 0.2, 0], reach=0.24)
    ff = Line(f_left.symbol.get_right() + RIGHT * 0.12, f_right.symbol.get_left() + LEFT * 0.12, stroke_color=cfg.WHITE, stroke_width=8)
    scene.play(FadeIn(f_left), FadeIn(f_right), Create(ff), run_time=0.9)
    clashes = VGroup()
    for side in ("up", "down"):
        a, b = f_left.slots[side].get_center(), f_right.slots[side].get_center()
        clashes.add(DoubleArrow(a + RIGHT * 0.3, b + LEFT * 0.3, buff=0, color=cfg.REPEL, stroke_width=6, tip_length=0.2))
    crowd = txt("Crowded lone pairs", cfg.FONT["label"], cfg.REPEL).move_to([0, -2.1, 0])
    scene.play(LaggedStart(*[GrowFromCenter(c) for c in clashes], lag_ratio=0.3), FadeIn(crowd), run_time=1.2)
    scene.play(Wiggle(clashes, scale_value=1.1), run_time=1.0)

    # --- 17. Family versus whole story -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 16)
    scene.play(FadeOut(VGroup(f_left, f_right, ff, clashes, crowd, question)), run_time=0.7)
    rules = VGroup(
        VGroup(txt("Related bonds", cfg.FONT["label"], cfg.CYAN), txt("shorter usually stronger", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.15),
        VGroup(txt("different elements", cfg.FONT["label"], cfg.GOLD), txt("Compare the full energy balance", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.15),
    ).arrange(RIGHT, buff=1.4).move_to([0, 0.4, 0])
    scene.play(FadeIn(rules[0], shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(rules[1], shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(rules[1][1], color=cfg.ENERGY, scale_factor=1.05), run_time=1.0)

    # --- 18. Back to the rule of eight ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 17)
    scene.play(FadeOut(rules), run_time=0.6)
    eight = txt("8", 180, cfg.GOLD).move_to([0, 0.4, 0])
    ring = octet_ring(eight, 1.5, cfg.GREEN)
    scene.play(FadeIn(eight, scale=0.6), Create(ring), run_time=1.0)
    crack = VMobject(stroke_color=cfg.REPEL, stroke_width=6).set_points_as_corners(
        [[-0.4, 2.0, 0], [0.1, 1.2, 0], [-0.25, 0.5, 0], [0.3, -0.3, 0], [-0.1, -1.0, 0]])
    breaks = txt("and where it breaks", cfg.FONT["body"], cfg.REPEL).move_to([0, -2.4, 0])
    scene.play(Create(crack), FadeIn(breaks, shift=UP * 0.1), run_time=1.0)
    scene.play(Wiggle(VGroup(eight, ring), scale_value=1.05), run_time=1.6)
    scene.play(Indicate(breaks, color=cfg.WHITE, scale_factor=1.05), run_time=0.9)
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
