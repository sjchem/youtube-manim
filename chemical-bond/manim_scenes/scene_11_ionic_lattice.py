"""The crystal pays the bill: the rock-salt lattice and its collective attraction.

The crystal is a hand-projected 5x5x5 rock-salt block (125 ions). The
neighbour shells — 6 opposite charges, 12 like charges, 8 opposite charges —
are found by ``utils.bond_models.neighbour_shells`` rather than typed, and
the factor "about 1.75 times one pair" is the Madelung constant summed with
Evjen's neutral-cube method (``madelung_rock_salt``). Lattice energies,
the transfer cost and MgO's melting point come from ``utils.bond_data``.
Ion sizes are shrunk so the arrangement stays visible.
"""

from manim_scenes.common import *

CRYSTAL_AT = np.array([-1.6, -0.15, 0])
SPACING = 0.98
PER_KJ = 0.0034
PANEL_X = 4.6


class Scene11IonicLattice(Scene):
    def construct(self) -> None:
        play_scene(self)


def shell_members(sites: np.ndarray, centre: int, distance: float) -> list[int]:
    d = np.linalg.norm(sites - sites[centre], axis=1)
    return [int(i) for i in np.where(np.abs(d - distance) < 1e-6)[0]]


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "The crystal pays the bill")

    # --- 1. Ions stack into a three-dimensional pattern -----------------------------------------------------
    crystal = rock_salt_crystal(2, SPACING, CRYSTAL_AT, cation=0.19, anion=0.3, bonds=False, assembly=0.0, spin=0.16,
                                tilt=0.5, polished=True)
    crystal._live_draw_order = True
    scene.add(crystal)
    scene.play(crystal.assemble(1.0), run_time=3.4, rate_func=linear)
    legend = VGroup(VGroup(polished_ball(0.17, cfg.CATION), eq(r"\mathrm{Na^+}", cfg.FONT["label"], cfg.CATION)).arrange(RIGHT, buff=0.25),
                    VGroup(polished_ball(0.27, cfg.ANION), eq(r"\mathrm{Cl^-}", cfg.FONT["label"], cfg.ANION)).arrange(RIGHT, buff=0.25))
    legend.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 2.6, 0])
    scene.play(FadeIn(legend), run_time=0.7)
    dismiss_opening_title(scene, t, head)

    # --- 2. Alternating in every direction: rock salt ---------------------------------------------------------------
    beat(scene, t, 1)
    rock_salt = chip("Rock-salt lattice", cfg.WHITE, cfg.FONT["label"]).move_to([PANEL_X, 0.8, 0])
    scene.play(FadeIn(rock_salt, shift=UP * 0.1), run_time=0.8)
    scene.play(Tween(crystal, lambda: crystal.spin, lambda v: setattr(crystal, "spin", v), 0.5), run_time=1.0)
    scene.play(Tween(crystal, lambda: crystal.spin, lambda v: setattr(crystal, "spin", v), 0.16), run_time=1.6)

    # --- 3. One sodium ion: six chloride neighbours -------------------------------------------------------------------
    beat(scene, t, 2)
    sites = crystal.sites / SPACING
    centre = int(np.argmin(np.linalg.norm(sites, axis=1)))
    shells = bm.neighbour_shells(sites, crystal.kinds, centre, shells=3)
    first = shell_members(sites, centre, shells[0][0])
    second = shell_members(sites, centre, shells[1][0])
    third = shell_members(sites, centre, shells[2][0])
    scene.play(FadeOut(rock_salt), Tween(crystal, lambda: crystal.spin, lambda v: setattr(crystal, "spin", v), 0.08),
               run_time=0.6)
    crystal.set_highlight([centre], dim=0.12)
    crystal.set_links([(centre, j) for j in first], cfg.ATTRACT, width=6)
    crystal.set_highlight([centre, *first], dim=0.12)
    scene.play(Hold(crystal), run_time=0.8)
    count_first = VGroup(txt(str(shells[0][1]), 84, cfg.ATTRACT), txt("attractions", cfg.FONT["label"], cfg.ATTRACT)).arrange(RIGHT, buff=0.25)
    count_first.move_to([PANEL_X, 0.75, 0])
    scene.play(FadeIn(count_first, shift=LEFT * 0.15), run_time=0.8)
    directions = txt("Six nearest neighbours", cfg.FONT["tiny"], cfg.MUTED).next_to(count_first, DOWN, buff=0.2)
    scene.play(FadeIn(directions), run_time=0.6)

    # --- 4. Twelve like charges: repulsions --------------------------------------------------------------------------------
    beat(scene, t, 3)
    crystal.set_links([(centre, j) for j in second], cfg.REPEL, width=4)
    crystal.set_highlight([centre, *second], dim=0.12)
    count_second = VGroup(txt(str(shells[1][1]), 84, cfg.REPEL), txt("repulsions", cfg.FONT["label"], cfg.REPEL)).arrange(RIGHT, buff=0.25)
    count_second.move_to([PANEL_X, -0.75, 0])
    scene.play(*fade_labels(directions, count_second), run_time=0.8)
    scene.play(Indicate(count_second, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)

    # --- 5. Eight more chlorides; and on and on ------------------------------------------------------------------------------
    beat(scene, t, 4)
    crystal.set_links([(centre, j) for j in third], cfg.ATTRACT, width=4)
    crystal.set_highlight([centre, *third], dim=0.12)
    count_third = VGroup(txt(str(shells[2][1]), 84, cfg.ATTRACT), txt("attractions", cfg.FONT["label"], cfg.ATTRACT)).arrange(RIGHT, buff=0.25)
    count_third.move_to([PANEL_X, -2.25, 0])
    scene.play(FadeIn(count_third, shift=LEFT * 0.15), run_time=0.8)
    scene.play(Hold(crystal), run_time=1.0)
    crystal.set_links([], cfg.ATTRACT)
    crystal.set_highlight(None)
    on_and_on = txt("... and on and on", cfg.FONT["label"], cfg.MUTED).move_to([PANEL_X, -3.4, 0])
    scene.play(FadeIn(on_and_on), run_time=0.8)

    # --- 6. Add them all: about 1.75 times a single pair --------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(count_first, count_second, count_third, on_and_on, legend)), run_time=0.7)
    series = eq(r"6 - \tfrac{12}{\sqrt2} + \tfrac{8}{\sqrt3} - \tfrac{6}{\sqrt4} + \cdots", cfg.FONT["label"], cfg.WHITE)
    series.move_to([PANEL_X - 0.2, 2.4, 0])
    fit_width(series, 6.0)
    scene.play(Write(series), run_time=1.6)
    madelung = ValueTracker(0.0)
    value = DecimalNumber(0, num_decimal_places=2, font_size=96 * MATH_SCALE, color=cfg.ATTRACT)
    value.add_updater(lambda m: m.set_value(madelung.get_value()))
    times = txt("× one ion pair", cfg.FONT["label"], cfg.WHITE)
    result = VGroup(value, times).arrange(RIGHT, buff=0.3).move_to([PANEL_X - 0.2, 0.9, 0])
    scene.play(FadeIn(result), run_time=0.5)
    scene.play(track(madelung, bm.madelung_rock_salt()), run_time=2.6, rate_func=rush_from)
    value.clear_updaters()
    careful = txt("Electrostatic sum", cfg.FONT["tiny"], cfg.MUTED).next_to(result, DOWN, buff=0.25)
    win = txt("attractions win", cfg.FONT["label"], cfg.ATTRACT).next_to(careful, DOWN, buff=0.3)
    scene.play(FadeIn(careful), FadeIn(win, shift=UP * 0.1), run_time=0.8)

    # --- 7. The Lattice energy magnitude pays the transfer bill ----------------------------------------------------------------------------------
    beat(scene, t, 6)
    state_note = txt("Gas atoms → NaCl(s)", cfg.FONT["tiny"], cfg.MUTED).move_to([PANEL_X, 2.65, 0])
    scene.play(*fade_labels(VGroup(series, result, careful, win), state_note), run_time=0.6)
    base = -0.2
    cost = energy_step(PANEL_X - 1.6, base, base + bd.transfer_cost() * PER_KJ, cfg.REQUIRED, f"+{bd.transfer_cost()}", side=LEFT,
                       size=cfg.FONT["label"])
    lattice = energy_step(PANEL_X - 0.4, base + bd.transfer_cost() * PER_KJ, base + bd.transfer_cost() * PER_KJ - bd.LATTICE_KJ["NaCl"] * PER_KJ,
                          cfg.RELEASED, f"−{bd.LATTICE_KJ['NaCl']}", side=RIGHT, size=cfg.FONT["label"])
    cost_tag = txt("transfer", cfg.FONT["small"], cfg.REQUIRED).next_to(cost, UP, buff=0.2)
    lattice_tag = txt("lattice", cfg.FONT["small"], cfg.RELEASED).next_to(lattice.tag, UP, buff=0.24).align_to(lattice.tag, LEFT)
    start_line = DashedLine([PANEL_X - 2.4, base, 0], [PANEL_X + 1.6, base, 0], stroke_color=cfg.MUTED, stroke_width=2, dash_length=0.1)
    scene.play(Create(start_line), GrowArrow(cost.arrow.arrow), FadeIn(cost.arrow[0]), FadeIn(cost.tag), FadeIn(cost_tag), run_time=1.0)
    scene.play(GrowArrow(lattice.arrow.arrow), FadeIn(lattice.arrow[0]), FadeIn(lattice.tag), FadeIn(lattice_tag), run_time=1.4)
    net = txt(f"net {signed(bd.salt_from_gas_atoms())} kJ/mol", cfg.FONT["label"], cfg.GREEN).move_to([PANEL_X, -3.55, 0])
    scene.play(FadeIn(net, shift=UP * 0.1), Flash(crystal.center_point(), color=cfg.ENERGY, flash_radius=2.6, num_lines=16), run_time=1.0)

    # --- 8. No molecule: an endless lattice ----------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(cost, lattice, cost_tag, lattice_tag, start_line, net, state_note)), run_time=0.6)
    molecule = VGroup(eq(r"\mathrm{NaCl}", 84, cfg.WHITE), txt("molecule?", cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    molecule.move_to([PANEL_X - 0.3, 1.5, 0])
    scene.play(FadeIn(molecule), run_time=0.7)
    crystal.set_highlight([centre, first[0]], dim=0.15)
    scene.play(Hold(crystal), run_time=0.8)
    crystal.set_highlight([centre, *first], dim=0.15)
    which = txt("Six equivalent neighbours", cfg.FONT["small"], cfg.MUTED).move_to([PANEL_X - 0.3, 0.5, 0])
    scene.play(FadeIn(which), run_time=0.8)
    no_molecule = strike(molecule, cfg.REPEL, 8)
    scene.play(Create(no_molecule), run_time=0.6)
    crystal.set_highlight(None)
    lattice_of_ions = txt("An extended ionic lattice", cfg.FONT["label"], cfg.GOLD).move_to([PANEL_X - 0.3, -0.5, 0])
    scene.play(FadeIn(lattice_of_ions, shift=UP * 0.1), run_time=0.8)

    # --- 9. Doubly charged ions: magnesium oxide ------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(molecule, which, no_molecule, lattice_of_ions)), run_time=0.6)
    bars = VGroup()
    top = 2.4
    for k, (name, key, colour) in enumerate(((r"\mathrm{NaCl}", "NaCl", cfg.WHITE), (r"\mathrm{MgO}", "MgO", cfg.ENERGY))):
        height = bd.LATTICE_KJ[key] * 0.00125
        bar = Rectangle(width=0.8, height=height, stroke_width=0, fill_color=colour, fill_opacity=0.9)
        bar.move_to([PANEL_X - 1.0 + 2.0 * k, top - 4.9 + height / 2, 0])
        label = eq(name, cfg.FONT["label"], colour).next_to(bar, DOWN, buff=0.15)
        bars.add(VGroup(bar, label))
    bars_title = txt('Lattice energy magnitude', cfg.FONT["small"], cfg.MUTED).move_to([PANEL_X, 2.95, 0])
    scene.play(FadeIn(bars_title), *[GrowFromEdge(b[0], DOWN) for b in bars], *[FadeIn(b[1]) for b in bars], run_time=1.4)
    charges = eq(r"\mathrm{Mg^{2+}\;O^{2-}}", cfg.FONT["label"], cfg.ENERGY).next_to(bars[1][0], LEFT, buff=0.3).shift(UP * 0.8)
    times_five = txt("almost ×5", cfg.FONT["label"], cfg.ENERGY).next_to(bars[1][0], LEFT, buff=0.3)
    scene.play(FadeIn(charges), FadeIn(times_five), run_time=0.8)
    melts = txt(f"melts above {bd.MGO_MELTING_C // 100 * 100} °C", cfg.FONT["small"], cfg.REQUIRED).move_to([PANEL_X, -3.55, 0])
    scene.play(FadeIn(melts, shift=UP * 0.1), run_time=0.7)

    # --- 10. A whole crystal settling into a deep valley ------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(bars, bars_title, charges, times_five, melts)), run_time=0.6)
    plot = EnergyPlot(depth=bd.LATTICE_KJ["NaCl"], r_e=282, a=0.012, r_max=900, e_min=-900, e_max=400, x_length=4.6,
                      y_length=3.6, center=[PANEL_X, 0.1, 0], labels=False)
    deep = txt("Collective stability", cfg.FONT["label"], cfg.ENERGY).next_to(plot, DOWN, buff=0.25)
    scene.play(Create(plot.axes), Create(plot.curve), run_time=1.4)
    scene.play(FadeIn(deep, shift=UP * 0.1), Tween(crystal, lambda: crystal.spin, lambda v: setattr(crystal, "spin", v), 0.4),
               run_time=1.0)
    scene.play(Indicate(deep, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
