"""What is a stable bond? The valley's depth, and a reaction's energy ledger.

The curve is chapter 04's Morse model of H2; its depth is the measured bond
enthalpy (436 kJ/mol). The ledger for H2 + Cl2 -> 2 HCl is computed by
``utils.bond_data.h2_cl2_ledger`` from bond enthalpies (436 + 243 broken,
2 x 432 formed); the data check confirms it lands within a few kJ/mol of the
measured heat of reaction. Arrow lengths are drawn to one shared kJ scale.
"""

from manim_scenes.common import *

PER_KJ = 0.0048
BASE_Y = -1.35
H_COLOR = "#E8F1F8"
CL_COLOR = cfg.GREEN


class Scene05StableBond(Scene):
    def construct(self) -> None:
        play_scene(self)


def atom_icon(symbol: str) -> VGroup:
    radius = 0.28 if symbol == "H" else 0.44
    ball = polished_ball(radius, H_COLOR if symbol == "H" else CL_COLOR)
    ball.symbol = symbol
    return ball


def molecule_icon(a: str, b: str) -> VGroup:
    first, second = atom_icon(a), atom_icon(b)
    second.next_to(first, RIGHT, buff=-0.12)
    return VGroup(first, second)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "What is a stable bond?")

    # --- 1. Up here, apart; down there, bonded ------------------------------------------------------
    plot = EnergyPlot(center=DOWN * 0.75, x_length=11.0, y_length=5.0)
    plot.shift(RIGHT * 0.2)
    # Keep the unit title above the plotting area: the steep wall reaches the
    # top edge near the old inline kJ/mol position.
    plot.y_title.next_to(plot.axes.c2p(0, plot.e_max), UP, buff=0.3)
    plot.y_title.align_to(plot.axes.y_axis, LEFT)
    r = ValueTracker(H2[1])
    marker = plot.marker(r, radius=0.15)
    scene.play(Create(plot.axes), FadeIn(plot.frame_lines), FadeIn(plot.labels), run_time=1.0)
    scene.play(Create(plot.curve), FadeIn(marker, scale=0.5), run_time=1.4)
    apart = VGroup(atom_icon("H"), atom_icon("H")).arrange(RIGHT, buff=0.55).next_to(plot.axes.c2p(270, 0), UP, buff=0.35)
    bonded = molecule_icon("H", "H").next_to(plot.point(H2[1]), RIGHT, buff=0.75).shift(DOWN * 0.15)
    apart_tag = txt("separated", cfg.FONT["small"], cfg.MUTED).next_to(apart, UP, buff=0.18)
    bonded_tag = txt("molecule", cfg.FONT["small"], cfg.CYAN).next_to(bonded, RIGHT, buff=0.25)
    scene.play(FadeIn(apart, shift=DOWN * 0.1), FadeIn(apart_tag), run_time=0.8)
    dismiss_opening_title(scene, t, head)
    scene.play(FadeIn(bonded, shift=UP * 0.1), FadeIn(bonded_tag), run_time=0.8)

    # --- 2. The drop is the Gas phase · 298 K ----------------------------------------------------------------
    beat(scene, t, 1)
    depth = plot.depth_arrow()
    value = txt(f"{bd.BOND_ENTHALPY_KJ['H-H']} kJ/mol", cfg.FONT["label"], cfg.ENERGY)
    value.move_to(plot.axes.c2p(190, -330))
    scene.play(FadeOut(VGroup(bonded, bonded_tag)), GrowFromCenter(depth), run_time=1.0)
    scene.play(FadeIn(value, shift=LEFT * 0.1), run_time=0.8)
    bond_energy = chip('Gas phase · 298 K', cfg.ENERGY, cfg.FONT["small"]).next_to(value, DOWN, buff=0.25).align_to(value, LEFT)
    scene.play(FadeIn(bond_energy, shift=UP * 0.1), run_time=0.7)
    scene.play(Indicate(depth, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)

    # --- 3. Breaking costs: climb out of the valley ------------------------------------------------------
    beat(scene, t, 2)
    breaking = eq(r"\mathrm{H_2(g)} \;\rightarrow\; 2\,\mathrm{H(g)}", 46, cfg.WHITE)
    cost = txt(f"+{bd.BOND_ENTHALPY_KJ['H-H']} kJ/mol", cfg.FONT["label"], cfg.REQUIRED)
    top_line = VGroup(breaking, cost).arrange(RIGHT, buff=0.6).move_to([0.2, 3.3, 0])
    scene.play(Write(breaking), run_time=1.1)
    scene.play(track(r, 300), FadeIn(cost, shift=UP * 0.15), run_time=2.6, rate_func=smooth)
    x_arrow = H2[1] + 26
    climb = glow_arrow(plot.axes.c2p(x_arrow, -H2[0] + 8), plot.axes.c2p(x_arrow, -8), cfg.REQUIRED, 8)
    pay = txt("costs", cfg.FONT["label"], cfg.REQUIRED).next_to(climb, LEFT, buff=0.12)
    scene.play(FadeOut(depth), GrowArrow(climb.arrow), FadeIn(climb[0]), FadeIn(pay), run_time=0.9)
    scene.play(Indicate(apart, color=cfg.WHITE, scale_factor=1.15), run_time=0.9)

    # --- 4. Forming pays: fall back in, energy released --------------------------------------------------------
    beat(scene, t, 3)
    forming = eq(r"2\,\mathrm{H(g)} \;\rightarrow\; \mathrm{H_2(g)}", 46, cfg.WHITE)
    gain = txt(f"−{bd.BOND_ENTHALPY_KJ['H-H']} kJ/mol", cfg.FONT["label"], cfg.RELEASED)
    VGroup(forming, gain).arrange(RIGHT, buff=0.6).move_to(top_line)
    scene.play(FadeThrough(breaking, forming), FadeThrough(cost, gain), FadeOut(VGroup(climb, pay)), run_time=1.0)
    scene.play(track(r, H2[1]), run_time=2.0, rate_func=rush_into)
    fall = glow_arrow(plot.axes.c2p(x_arrow, -8), plot.axes.c2p(x_arrow, -H2[0] + 8), cfg.RELEASED, 8)
    pays = txt("pays", cfg.FONT["label"], cfg.RELEASED).move_to(pay)
    scene.play(GrowArrow(fall.arrow), FadeIn(fall[0]), FadeIn(pays), run_time=0.8)
    sparks = VGroup(*[Line(ORIGIN, RIGHT * 0.55, stroke_color=cfg.ENERGY, stroke_width=5)
                      .rotate(angle, about_point=ORIGIN).shift(plot.point(H2[1]) + 0.35 * np.array([np.cos(angle), np.sin(angle), 0]))
                      for angle in np.linspace(0, TAU, 10, endpoint=False)])
    scene.play(LaggedStart(*[ShowPassingFlash(s.copy(), time_width=0.6) for s in sparks], lag_ratio=0.05),
               Flash(marker, color=cfg.ENERGY, line_length=0.45, num_lines=12), run_time=1.2)
    heat = txt("Energy carried away", cfg.FONT["label"], cfg.ENERGY).move_to(plot.axes.c2p(160, 260))
    scene.play(FadeIn(heat, shift=UP * 0.1), run_time=0.6)

    # --- 5. Not batteries: breaking costs, forming pays ---------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(plot, marker, value, bond_energy, apart, apart_tag, fall, pays, heat, forming, gain)),
               run_time=0.8)
    marker.clear_updaters()
    myth = txt("breaking bonds releases energy", cfg.FONT["title"], cfg.MUTED).move_to([0, 1.4, 0])
    scene.play(FadeIn(myth), run_time=0.7)
    myth_strike = strike(myth, cfg.REPEL, 8)
    scene.play(Create(myth_strike), run_time=0.6)
    rules = VGroup(chip("Breaking costs", cfg.REQUIRED, cfg.FONT["section"]),
                   chip("Forming pays", cfg.RELEASED, cfg.FONT["section"])).arrange(RIGHT, buff=0.8).move_to([0, -0.9, 0])
    scene.play(FadeIn(rules[0], shift=UP * 0.2), run_time=0.8)
    scene.play(FadeIn(rules[1], shift=UP * 0.2), run_time=0.8)
    up = glow_arrow(rules[0].get_bottom() + DOWN * 1.9, rules[0].get_bottom() + DOWN * 0.3, cfg.REQUIRED, 8)
    down = glow_arrow(rules[1].get_bottom() + DOWN * 0.3, rules[1].get_bottom() + DOWN * 1.9, cfg.RELEASED, 8)
    scene.play(GrowArrow(up.arrow), FadeIn(up[0]), GrowArrow(down.arrow), FadeIn(down[0]), run_time=0.9)
    scene.play(Wiggle(rules, scale_value=1.06), run_time=1.2)

    # --- 6. A reaction: hydrogen meets chlorine ----------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(myth, myth_strike, rules, up, down)), run_time=0.7)
    reaction = eq(r"\mathrm{H_2} \;+\; \mathrm{Cl_2} \;\rightarrow\; 2\,\mathrm{HCl}", 58, cfg.WHITE).move_to([0, 3.25, 0])
    scene.play(Write(reaction), run_time=1.4)
    broken, formed, net = bd.h2_cl2_ledger()
    y0, y1, y2 = BASE_Y, BASE_Y + broken * PER_KJ, BASE_Y + (broken - formed) * PER_KJ
    start_shelf = level_shelf(y0, -6.7, -4.1, cfg.WHITE, r"\mathrm{H_2 + Cl_2}", side=DOWN, size=cfg.FONT["label"])
    start_shelf.label.next_to(start_shelf.shelf, DOWN, buff=0.18)
    scene.play(Create(start_shelf.shelf), FadeIn(start_shelf.label), run_time=0.8)
    stage = VGroup(molecule_icon("H", "H"), molecule_icon("Cl", "Cl")).arrange(RIGHT, buff=0.8).move_to([4.7, 0.5, 0])
    scene.play(FadeIn(stage, scale=0.8), run_time=0.8)
    scene.play(Indicate(stage, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)

    # --- 7. Break both bonds: costs 679 -------------------------------------------------------------------------
    beat(scene, t, 6)
    up_step = energy_step(-3.85, y0, y1, cfg.REQUIRED, f"+{broken}", side=LEFT, size=cfg.FONT["label"])
    up_step.tag.next_to(up_step.arrow, LEFT, buff=0.15)
    atoms_shelf = level_shelf(y1, -3.6, -0.9, cfg.WHITE, r"\mathrm{2H + 2Cl}", side=UP, size=cfg.FONT["label"])
    atoms_shelf.label.next_to(atoms_shelf.shelf, UP, buff=0.18)
    scene.play(GrowArrow(up_step.arrow.arrow), FadeIn(up_step.arrow[0]), FadeIn(up_step.tag), run_time=1.0)
    scene.play(Create(atoms_shelf.shelf), FadeIn(atoms_shelf.label), run_time=0.7)
    h1, h2 = stage[0]
    c1, c2 = stage[1]
    scene.play(h1.animate.shift(LEFT * 0.5 + UP * 0.5), h2.animate.shift(RIGHT * 0.3 + UP * 0.75),
               c1.animate.shift(LEFT * 0.15 + DOWN * 0.7), c2.animate.shift(RIGHT * 0.6 + DOWN * 0.4), run_time=1.0)
    broken_tag = txt("bonds broken", cfg.FONT["label"], cfg.REQUIRED).move_to([4.7, -0.95, 0])
    scene.play(FadeIn(broken_tag), run_time=0.6)

    # --- 8. Form two H-Cl bonds: releases 864 ------------------------------------------------------------------------
    beat(scene, t, 7)
    down_step = energy_step(-0.65, y1, y2, cfg.RELEASED, f"−{formed}", side=RIGHT, size=cfg.FONT["label"])
    end_shelf = level_shelf(y2, -0.4, 1.9, cfg.WHITE, r"\mathrm{2HCl}", side=DOWN, size=cfg.FONT["label"])
    end_shelf.label.next_to(end_shelf.shelf, DOWN, buff=0.18)
    scene.play(GrowArrow(down_step.arrow.arrow), FadeIn(down_step.arrow[0]), FadeIn(down_step.tag), run_time=1.0)
    scene.play(Create(end_shelf.shelf), FadeIn(end_shelf.label), run_time=0.7)
    hcl_a, hcl_b = molecule_icon("H", "Cl"), molecule_icon("H", "Cl")
    VGroup(hcl_a, hcl_b).arrange(DOWN, buff=0.6).move_to([4.7, 0.5, 0])
    scene.play(h1.animate.move_to(hcl_a[0]), c1.animate.move_to(hcl_a[1]), h2.animate.move_to(hcl_b[0]),
               c2.animate.move_to(hcl_b[1]), FadeOut(broken_tag), run_time=1.1)
    formed_tag = txt("bonds formed", cfg.FONT["label"], cfg.RELEASED).move_to([4.7, -0.95, 0])
    scene.play(FadeIn(formed_tag), run_time=0.6)

    # --- 9. The difference is the heat of reaction -----------------------------------------------------------------------
    beat(scene, t, 8)
    net_step = energy_step(2.3, y0, y2, cfg.GREEN, f"{signed(net)} kJ/mol", side=RIGHT, size=cfg.FONT["label"])
    guide = DashedLine([-4.1, y0, 0], [2.3, y0, 0], stroke_color=cfg.MUTED, stroke_width=2, dash_length=0.1)
    scene.play(Create(guide), run_time=0.6)
    scene.play(GrowArrow(net_step.arrow.arrow), FadeIn(net_step.arrow[0]), FadeIn(net_step.tag), run_time=1.0)
    released = txt("released as heat", cfg.FONT["small"], cfg.GREEN).next_to(net_step.tag, DOWN, buff=0.36).align_to(net_step.tag, LEFT)
    scene.play(FadeOut(formed_tag), FadeIn(released, shift=UP * 0.1), Flash(VGroup(hcl_a, hcl_b).get_center(), color=cfg.ENERGY,
                                                                line_length=0.5, num_lines=14, flash_radius=1.3), run_time=1.0)

    # --- 10. A balance: broken against formed ----------------------------------------------------------------------------
    beat(scene, t, 9)
    balance = MathTex(r"\Delta H", r"=", r"\textstyle\sum \text{broken}", r"-", r"\textstyle\sum \text{formed}",
                      font_size=48 * MATH_SCALE, color=cfg.WHITE)
    balance.set_stroke(cfg.BG, width=0.65, opacity=0.85, background=True)
    balance.move_to([0, 0.4, 0])
    balance[0].set_color(cfg.ENERGY)
    balance[2].set_color(cfg.REQUIRED)
    balance[4].set_color(cfg.RELEASED)
    ledger = VGroup(start_shelf, up_step, atoms_shelf, down_step, end_shelf, net_step, guide, released, h1, h2, c1, c2)
    scene.play(FadeOut(ledger), run_time=1.0)
    scene.play(Write(balance), run_time=1.8)
    box = glow_frame(balance, cfg.ENERGY, buff=0.18)
    scene.play(Create(box), run_time=0.8)
    scene.play(Indicate(balance[2], color=cfg.REQUIRED, scale_factor=1.12),
               run_time=1.2)
    scene.play(Indicate(balance[4], color=cfg.RELEASED, scale_factor=1.12),
               run_time=1.2)
    net_summary = txt(f"{signed(net)} kJ/mol", cfg.FONT["section"], cfg.GREEN).move_to([0, -1.4, 0])
    scene.play(FadeIn(net_summary), run_time=0.8)
    question = txt("What are the electrons doing?", cfg.FONT["body"], cfg.CYAN).move_to([0, 1.85, 0])
    scene.play(FadeIn(question, shift=UP * 0.1), run_time=1.2)
    scene.play(Indicate(question, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)
    scene.play(Circumscribe(balance, color=cfg.ENERGY, fade_out=True), run_time=2.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
