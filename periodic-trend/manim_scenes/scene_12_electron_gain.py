"""Electron gain enthalpy: send an electron in instead.

The energy diagram is the film's sign convention made visible: a level that
drops means energy released (green, a negative value); a level that rises
means energy must be supplied (orange). The bars are the NCERT / measured
values; elements whose anion is not stable get no bar, only a mark.
"""

from manim_scenes.common import *

ATOM_AT = np.array([-4.3, 0.55, 0])
DIAGRAM_X = 2.9
TOP_Y = 1.25
BAR_BASE = -2.75
BAR_SCALE = 3.9 / 360


class Scene12ElectronGain(Scene):
    def construct(self) -> None:
        play_scene(self)


def released_bars(symbols, xs) -> VGroup:
    """Energy released on gaining an electron; a flat orange mark if none is."""
    group = VGroup()
    group.items = {}
    for symbol, x in zip(symbols, xs):
        value = ed.ELECTRON_GAIN_KJ[symbol]
        name = txt(symbol, cfg.FONT["label"], block_color(pm.z_of(symbol))).move_to([x, BAR_BASE - 0.35, 0])
        if value is None or value > 0:
            bar = Rectangle(width=0.8, height=0.08, stroke_width=0, fill_color=cfg.REQUIRED, fill_opacity=1)
            bar.move_to([x, BAR_BASE + 0.04, 0])
            amount = txt("needs energy", cfg.FONT["tiny"], cfg.REQUIRED)
            amount.rotate(PI / 2).next_to(bar, UP, buff=0.15)
        else:
            height = -value * BAR_SCALE
            bar = Rectangle(width=0.8, height=height, stroke_width=2, stroke_color=cfg.RELEASED, fill_color=cfg.RELEASED,
                            fill_opacity=0.5).move_to([x, BAR_BASE + height / 2, 0])
            amount = txt(signed(value), cfg.FONT["small"], cfg.WHITE).next_to(bar, UP, buff=0.12)
        item = VGroup(bar, name, amount)
        item.bar, item.name, item.amount = bar, name, amount
        group.add(item)
        group.items[symbol] = item
    return group


def level_diagram(drop: float, label: str, colour: str, *, final_label: str = r"\mathrm{X}^{-}") -> VGroup:
    """'X + e-' on a top shelf, 'X-' on a shelf ``drop`` lower (negative = higher)."""
    top = energy_level(TOP_Y, DIAGRAM_X - 1.4, DIAGRAM_X + 0.4, cfg.WHITE, r"\mathrm{X} + e^{-}")
    bottom_y = TOP_Y - drop
    bottom = energy_level(bottom_y, DIAGRAM_X - 1.4, DIAGRAM_X + 0.4, colour, final_label)
    arrow = Arrow([DIAGRAM_X - 0.5, TOP_Y, 0], [DIAGRAM_X - 0.5, bottom_y, 0], buff=0.08, color=colour, stroke_width=8,
                  tip_length=0.26, max_tip_length_to_length_ratio=0.3)
    tag = txt(label, cfg.FONT["small"], colour).next_to(arrow, LEFT, buff=0.25)
    group = VGroup(top, bottom, arrow, tag)
    group.top, group.bottom, group.arrow, group.tag = top, bottom, arrow, tag
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "Send an electron in")

    # --- 1. An electron arrives ---------------------------------------------------------------
    atom = Atom(1.35, ATOM_AT, charge="+17", core=0.55, count=380, seed=121)
    scene.play(FadeIn(atom, scale=0.6), run_time=1.0)
    incoming = glow_dot([7.0, 2.6, 0], 0.14)
    path = ArcBetweenPoints(np.array([7.0, 2.6, 0]), ATOM_AT + np.array([1.0, 0.4, 0]), angle=PI / 5)
    scene.play(FadeIn(incoming, scale=0.4), run_time=0.3)
    scene.play(MoveAlongPath(incoming, path), run_time=1.8, rate_func=rush_from)

    # --- 2. The definition ---------------------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    name = VGroup(txt("electron gain enthalpy", cfg.FONT["body"], cfg.GOLD),
                  txt('energy change · gas phase', cfg.FONT["small"], cfg.WHITE),
                  txt('add one electron', cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.16)
    name.move_to([2.6, 0.6, 0])
    scene.play(FadeIn(name, shift=LEFT * 0.2), run_time=1.0)

    # --- 3. The equation -------------------------------------------------------------------------
    beat(scene, t, 2)
    equation = eq(r"\mathrm{X(g)} + e^{-} \;\rightarrow\; \mathrm{X^{-}(g)}", cfg.FONT["title"], cfg.WHITE).move_to([0, -2.9, 0])
    scene.play(Write(equation), run_time=1.4)

    # --- 4. Released energy is negative -------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(name), FadeOut(incoming), run_time=0.5)
    released = level_diagram(2.2, "released", cfg.RELEASED)
    scene.play(FadeIn(released.top), run_time=0.6)
    scene.play(GrowArrow(released.arrow), FadeIn(released.bottom), FadeIn(released.tag), run_time=1.2)
    sign = eq_chip(r"\text{released} \;\Rightarrow\; \Delta H < 0", cfg.RELEASED, cfg.FONT["small"]).move_to([2.9, 2.75, 0])
    scene.play(FadeIn(sign, shift=DOWN * 0.15), run_time=0.8)
    more = txt('More negative = more released', cfg.FONT["small"], cfg.WHITE).move_to([2.9, -1.95, 0])
    scene.play(FadeIn(more), run_time=0.7)

    # --- 5. Chlorine: one short of a closed set -------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(equation), FadeOut(more), run_time=0.5)
    row = orbital_row(1, "3p", box=0.68, gap=0.1).move_to(ATOM_AT + DOWN * 2.55 + RIGHT * 0.2)
    arrows = VGroup(*row_arrows(row, 5))
    newcomer = row_arrows(row, 6)[-1]
    scene.play(FadeIn(row), FadeIn(arrows), run_time=0.8)
    scene.play(drop_in(newcomer), Flash(row.boxes[2], color=cfg.GREEN, flash_radius=0.5), run_time=0.9)
    full = VGroup(check_mark(0.22), txt("full", cfg.FONT["small"], cfg.GREEN)).arrange(RIGHT, buff=0.15)
    full.next_to(row, RIGHT, buff=0.3)
    cl_value = level_diagram(-ed.ELECTRON_GAIN_KJ["Cl"] / 160, f"{signed(ed.ELECTRON_GAIN_KJ['Cl'])} kJ/mol", cfg.RELEASED)
    scene.play(FadeIn(full, scale=1.2), FadeThrough(released, cl_value), run_time=1.2)
    released = cl_value

    # --- 6. Neon: shells closed, energy must be supplied -------------------------------------------------------
    beat(scene, t, 5)
    head = swap_heading(scene, head, 'Neon: a closed shell')
    scene.play(*atom.resize(0.75, 0.2), *relabel_nucleus(atom, "+10"), FadeOut(VGroup(row, arrows, newcomer, full, sign)),
               run_time=1.0)
    full_row = orbital_row(1, "2p", box=0.68, gap=0.1).move_to(ATOM_AT + DOWN * 2.55 + RIGHT * 0.2)
    pairs = VGroup(*row_arrows(full_row, 6))
    next_row = orbital_row(0, "3s", box=0.68).move_to(ATOM_AT + DOWN * 1.55 + RIGHT * 1.55)
    scene.play(FadeIn(full_row), FadeIn(pairs), run_time=0.7)
    scene.play(FadeIn(next_row), run_time=0.6)
    lone = spin_arrow(next_row.boxes[0], 1, 0.68)
    scene.play(drop_in(lone), run_time=0.8)
    needed = level_diagram(-1.2, "needs energy", cfg.REQUIRED, final_label=r"\text{unbound}")
    scene.play(FadeThrough(released, needed), lone.animate.set_opacity(0.15), run_time=1.2)
    released = needed
    new_shell = eq_chip(r"\text{No stable } \mathrm{Ne}^{-}", cfg.ORANGE, cfg.FONT["small"]).move_to(ATOM_AT + UP * 2.2)
    scene.play(FadeIn(new_shell, scale=1.1), run_time=0.7)

    # --- 7. Across a period: generally more negative ------------------------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "The broad pattern")
    scene.play(FadeOut(VGroup(atom, full_row, pairs, next_row, lone, released, new_shell)), run_time=0.8)
    period3 = ("Na", "Mg", "Al", "Si", "P", "S", "Cl")
    xs = [-6.2 + 1.1 * i for i in range(len(period3))]
    across = released_bars(period3, xs)
    scene.play(LaggedStart(*[AnimationGroup(GrowFromEdge(i.bar, DOWN), FadeIn(i.name), FadeIn(i.amount)) for i in across],
                           lag_ratio=0.15), run_time=2.0)
    arrow = glow_arrow([xs[0], 2.3, 0], [xs[-1], 2.3, 0], cfg.RELEASED, 6)
    tag = txt("generally more negative →", cfg.FONT["small"], cfg.RELEASED).next_to(arrow, UP, buff=0.12)
    scene.play(GrowArrow(arrow.arrow), FadeIn(arrow[0]), FadeIn(tag), run_time=0.9)

    # --- 8. Down a group: generally less negative -------------------------------------------------------------------
    beat(scene, t, 7)
    group17 = ("F", "Cl", "Br", "I")
    gxs = [2.2 + 1.35 * i for i in range(len(group17))]
    down = released_bars(group17, gxs)
    scene.play(LaggedStart(*[AnimationGroup(GrowFromEdge(i.bar, DOWN), FadeIn(i.name), FadeIn(i.amount)) for i in down],
                           lag_ratio=0.2), run_time=1.6)
    fall = glow_arrow([gxs[1], 2.3, 0], [gxs[-1], 2.3, 0], cfg.CYAN, 6)
    fall_tag = txt("down: less negative", cfg.FONT["small"], cfg.CYAN).next_to(fall, UP, buff=0.12)
    scene.play(GrowArrow(fall.arrow), FadeIn(fall[0]), FadeIn(fall_tag), run_time=0.9)
    farther = txt('New electron: farther out', cfg.FONT["tiny"], cfg.MUTED).move_to([4.2, -3.75, 0])
    scene.play(FadeIn(farther), run_time=0.6)

    # --- 9. ...with one famous exception ------------------------------------------------------------------------------
    beat(scene, t, 8)
    fluorine = down.items["F"]
    question = txt("?", 96, cfg.RED).next_to(fluorine.amount, UP, buff=0.28)
    scene.play(fluorine.bar.animate.set_stroke(cfg.RED).set_fill(cfg.RED, 0.45), fluorine.amount.animate.set_color(cfg.RED),
               FadeIn(question, scale=0.5), run_time=1.0)
    scene.play(Wiggle(question), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
