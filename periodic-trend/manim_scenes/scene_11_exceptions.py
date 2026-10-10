"""When the trend seems to break: Be > B and N > O, explained by orbitals.

Each atom gets a schematic energy diagram (spacing not to scale): orbital
boxes on 2s and 2p shelves, a dashed "free electron" line at the top, and a
gold arrow for the energy needed to lift the outermost electron out. The bars
on the left are the measured first ionization enthalpies (NIST).
"""

from manim_scenes.common import *

FREE_Y = 2.35
P_Y = -0.35
S_Y = -1.85
BOX = 0.74
LEFT_DIAGRAM_X = 0.95
RIGHT_DIAGRAM_X = 4.95
BAR_BASE = -2.9
BAR_SCALE = 4.4 / 1600


class Scene11Exceptions(Scene):
    def construct(self) -> None:
        play_scene(self)


def bars(symbols, xs, colours=None) -> VGroup:
    """Measured first ionization enthalpies as flat bars, with symbol and value."""
    group = VGroup()
    group.items = {}
    for index, (symbol, x) in enumerate(zip(symbols, xs)):
        value = ed.ionization_kj(symbol)
        height = value * BAR_SCALE
        colour = (colours or {}).get(symbol, block_color(pm.z_of(symbol)))
        bar = Rectangle(width=0.8, height=height, stroke_width=2, stroke_color=colour, fill_color=colour, fill_opacity=0.55)
        bar.move_to([x, BAR_BASE + height / 2, 0])
        name = txt(symbol, cfg.FONT["label"], colour).next_to(bar, DOWN, buff=0.18)
        amount = txt(str(value), cfg.FONT["small"], cfg.WHITE).next_to(bar, UP, buff=0.15)
        item = VGroup(bar, name, amount)
        item.bar, item.name, item.amount = bar, name, amount
        group.add(item)
        group.items[symbol] = item
    return group


def diagram(symbol: str, x: float) -> VGroup:
    """2s and 2p shelves with boxes filled for this element (Hund order)."""
    z = pm.z_of(symbol)
    counts = {shell.label: count for shell, count in pm.ground_configuration(z)}
    s_row = orbital_row(0, None, box=BOX).move_to([x - 1.5, S_Y, 0])
    p_row = orbital_row(1, None, box=BOX, gap=0.1).move_to([x + 0.3, P_Y, 0])
    s_tag = eq("2s", cfg.FONT["small"], cfg.BLOCK_COLORS["s"]).next_to(s_row, RIGHT, buff=0.2)
    p_tag = eq("2p", cfg.FONT["small"], cfg.BLOCK_COLORS["p"]).next_to(p_row, DOWN, buff=0.18)
    free = DashedLine([x - 1.95, FREE_Y, 0], [x + 1.6, FREE_Y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    s_arrows = VGroup(*row_arrows(s_row, counts.get("2s", 0)))
    p_arrows = VGroup(*row_arrows(p_row, counts.get("2p", 0)))
    name = txt(pm.NAMES[symbol], cfg.FONT["label"], block_color(z)).move_to([x, 3.0, 0])
    group = VGroup(free, s_row, p_row, s_tag, p_tag, s_arrows, p_arrows, name)
    group.free, group.s_row, group.p_row, group.s_arrows, group.p_arrows, group.name = free, s_row, p_row, s_arrows, p_arrows, name
    return group


def lift(start, color: str = cfg.PULL_COLOR, label: str | None = None) -> VGroup:
    """The energy needed to lift an electron from ``start`` up to the free line."""
    start = np.asarray(start, dtype=float)
    arrow = Arrow(start + UP * 0.3, [start[0], FREE_Y - 0.05, 0], buff=0, color=color, stroke_width=8,
                  tip_length=0.26, max_tip_length_to_length_ratio=0.2)
    group = VGroup(arrow)
    if label:
        group.add(txt(label, cfg.FONT["small"], color).next_to(arrow, RIGHT, buff=0.15))
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "Beryllium vs boron")

    # --- 1. The numbers say B < Be ------------------------------------------------------------
    be_b = bars(("Be", "B"), (-5.6, -4.2))
    scene.play(LaggedStart(*[GrowFromEdge(item.bar, DOWN) for item in be_b], lag_ratio=0.3),
               FadeIn(VGroup(*[VGroup(i.name, i.amount) for i in be_b])), run_time=1.4)
    expected_h = (ed.ionization_kj("Be") + 120) * BAR_SCALE
    expected = DashedVMobject(Rectangle(width=0.8, height=expected_h, stroke_color=cfg.WHITE, stroke_width=3),
                              num_dashes=30).move_to([-2.8, BAR_BASE + expected_h / 2, 0])
    expect_tag = txt("expected", cfg.FONT["tiny"], cfg.MUTED).next_to(expected, UP, buff=0.1)
    scene.play(Create(expected), FadeIn(expect_tag), be_b.items["B"].amount.animate.set_color(cfg.RED), run_time=1.2)

    # --- 2. Beryllium fills 2s --------------------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    be = diagram("Be", LEFT_DIAGRAM_X)
    scene.play(FadeIn(VGroup(be.free, be.s_row, be.p_row, be[3], be[4], be.name)), run_time=1.0)
    scene.play(LaggedStart(*[drop_in(a) for a in be.s_arrows], lag_ratio=0.3), run_time=1.0)

    # --- 3. Boron's fifth electron: 2p -------------------------------------------------------------
    beat(scene, t, 2)
    b = diagram("B", RIGHT_DIAGRAM_X)
    scene.play(FadeIn(VGroup(b.free, b.s_row, b.p_row, b[3], b[4], b.name)), FadeIn(b.s_arrows), run_time=1.0)
    scene.play(drop_in(b.p_arrows[0]), Flash(b.p_row.boxes[0], color=cfg.GREEN, flash_radius=0.5), run_time=1.0)

    # --- 4. Higher start, more shielded: less energy to remove ---------------------------------------
    beat(scene, t, 3)
    shield = SurroundingRectangle(b.s_row.boxes, color=cfg.CORE_COLOR, buff=0.12, corner_radius=0.1, stroke_width=4)
    shield_tag = txt("2s pair shields", cfg.FONT["tiny"], cfg.CORE_COLOR).next_to(shield, DOWN, buff=0.14)
    scene.play(Create(shield), FadeIn(shield_tag), run_time=0.9)
    be_lift = lift(be.s_row.boxes[0].get_top(), label=str(ed.ionization_kj("Be")))
    b_lift = lift(b.p_row.boxes[0].get_top(), label=str(ed.ionization_kj("B")))
    scene.play(GrowArrow(be_lift[0]), FadeIn(be_lift[1]), run_time=1.0)
    scene.play(GrowArrow(b_lift[0]), FadeIn(b_lift[1]), run_time=1.0)
    shorter = chip("starts higher → less energy", cfg.GREEN, cfg.FONT["small"]).move_to([3.0, -3.45, 0])
    scene.play(FadeIn(shorter, shift=UP * 0.15), run_time=0.8)
    schematic = txt("energy spacing schematic", cfg.FONT["tiny"], cfg.MUTED).move_to([-4.6, -3.95, 0])
    scene.play(FadeIn(schematic), run_time=0.5)

    # --- 5. Not broken: a different electron ---------------------------------------------------------
    beat(scene, t, 4)
    different = chip('A different subshell', cfg.GOLD, cfg.FONT["small"]).move_to([3.0, -3.45, 0])
    scene.play(*fade_labels(shorter, different), run_time=0.8)
    scene.play(Indicate(b.p_arrows[0], color=cfg.GOLD, scale_factor=1.3), run_time=1.0)

    # --- 6. Nitrogen versus oxygen ---------------------------------------------------------------------
    beat(scene, t, 5)
    head = swap_heading(scene, head, "Nitrogen vs oxygen")
    scene.play(FadeOut(VGroup(be, b, be_lift, b_lift, shield, shield_tag, different, be_b, expected, expect_tag)),
               run_time=0.8)
    n_o = bars(("N", "O"), (-5.6, -4.2))
    scene.play(LaggedStart(*[GrowFromEdge(item.bar, DOWN) for item in n_o], lag_ratio=0.3),
               FadeIn(VGroup(*[VGroup(i.name, i.amount) for i in n_o])), run_time=1.2)
    scene.play(n_o.items["O"].amount.animate.set_color(cfg.RED), run_time=0.5)

    # --- 7. Nitrogen: three unpaired --------------------------------------------------------------------
    beat(scene, t, 6)
    n = diagram("N", LEFT_DIAGRAM_X)
    scene.play(FadeIn(VGroup(n.free, n.s_row, n.p_row, n[3], n[4], n.name, n.s_arrows)), run_time=0.8)
    scene.play(LaggedStart(*[drop_in(a) for a in n.p_arrows], lag_ratio=0.3), run_time=1.2)
    scene.play(LaggedStart(*[Indicate(a, color=cfg.WHITE, scale_factor=1.25) for a in n.p_arrows], lag_ratio=0.2),
               run_time=0.8)

    # --- 8. Oxygen: a pair --------------------------------------------------------------------------------
    beat(scene, t, 7)
    o = diagram("O", RIGHT_DIAGRAM_X)
    scene.play(FadeIn(VGroup(o.free, o.s_row, o.p_row, o[3], o[4], o.name, o.s_arrows, *o.p_arrows[:3])), run_time=0.8)
    scene.play(drop_in(o.p_arrows[3]), run_time=0.9)

    # --- 9. The pair repels ----------------------------------------------------------------------------------
    beat(scene, t, 8)
    paired_box = o.p_row.boxes[0]
    spark = VGroup(*[Line(paired_box.get_center() + UP * dy + LEFT * 0.07, paired_box.get_center() + UP * (dy + 0.1) + RIGHT * 0.07,
                          stroke_color=cfg.RED, stroke_width=5) for dy in (-0.15, 0.0)])
    repel = chip("pair repels", cfg.RED, cfg.FONT["small"]).move_to([RIGHT_DIAGRAM_X - 0.6, -2.7, 0])
    scene.play(Create(spark), FadeIn(repel, shift=UP * 0.1), Wiggle(paired_box, scale_value=1.15), run_time=1.2)
    n_lift = lift(n.p_row.boxes[0].get_top(), label=str(ed.ionization_kj("N")))
    o_lift = lift(paired_box.get_top() + UP * 0.25, label=str(ed.ionization_kj("O")))
    scene.play(GrowArrow(n_lift[0]), FadeIn(n_lift[1]), run_time=0.9)
    scene.play(GrowArrow(o_lift[0]), FadeIn(o_lift[1]), run_time=0.9)

    beat(scene, t, 9)
    easier = chip("a little easier to remove", cfg.GREEN, cfg.FONT["small"]).move_to([2.6, -3.6, 0])
    scene.play(FadeIn(easier, shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(o_lift[0], color=cfg.WHITE), run_time=1.0)

    # --- 10. Period 3 repeats both dips ---------------------------------------------------------------------------
    beat(scene, t, 10)
    head = swap_heading(scene, head, "Period 3 repeats both dips")
    scene.play(FadeOut(VGroup(n, o, n_lift, o_lift, spark, repel, easier, n_o, schematic)), run_time=0.7)
    period3 = ("Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar")
    xs = [-4.9 + 1.4 * i for i in range(len(period3))]
    row = bars(period3, xs)
    scene.play(LaggedStart(*[GrowFromEdge(item.bar, DOWN) for item in row], lag_ratio=0.12),
               FadeIn(VGroup(*[VGroup(i.name, i.amount) for i in row])), run_time=1.8)
    dips = VGroup()
    for a, b_sym in (("Mg", "Al"), ("P", "S")):
        start_pt, end_pt = row.items[a].amount.get_top() + UP * 0.12, row.items[b_sym].amount.get_top() + UP * 0.12
        dips.add(CurvedArrow(start_pt, end_pt, angle=-PI / 2.5, color=cfg.RED, stroke_width=7, tip_length=0.25))
    scene.play(LaggedStart(*[Create(d) for d in dips], lag_ratio=0.5),
               *[row.items[s].amount.animate.set_color(cfg.RED) for s in ("Al", "S")], run_time=1.4)

    # --- 11. Not broken, just more detailed ------------------------------------------------------------------------
    beat(scene, t, 11)
    detail = chip('Orbitals explain the dips', cfg.GOLD, cfg.FONT["label"]).move_to([0, 2.95, 0])
    fit_width(detail, 12.0)
    scene.play(FadeIn(detail, shift=DOWN * 0.15), run_time=0.9)
    scene.play(Indicate(row.items["Al"].bar, color=cfg.RED), Indicate(row.items["S"].bar, color=cfg.RED), run_time=1.2)

    # --- 12. Reverse the experiment --------------------------------------------------------------------------------
    beat(scene, t, 12)
    reverse = chip('Next: electron gain', cfg.CYAN, cfg.FONT["label"]).move_to([0, 2.95, 0])
    scene.play(*fade_labels(detail, reverse), FadeOut(row), FadeOut(dips), run_time=0.8)
    target = Atom(1.1, [0, -0.6, 0], charge="+", core=0.3, count=300, seed=111)
    scene.play(FadeIn(target, scale=0.6), run_time=0.7)
    incoming = glow_dot([7.0, 1.6, 0], 0.14)
    scene.play(MoveAlongPath(incoming, ArcBetweenPoints(np.array([7.0, 1.6, 0]), np.array([0.9, -0.3, 0]), angle=PI / 4)),
               run_time=1.8, rate_func=rush_from)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
