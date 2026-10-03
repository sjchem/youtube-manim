"""Period 2, electron by electron: 2s gives two elements, 2p gives six.

Every configuration on screen is computed by the filling model, and every
tile flies to the seat the model gives it on the build board.
"""

from manim_scenes.common import *

LADDER_X = -3.6
ROW_Y = {"1s": -3.4, "2s": -2.25, "2p": -1.1}
TILE_AT = np.array([1.75, -2.25, 0])
CONFIG_AT = np.array([5.0, -2.25, 0])
SOURCE = np.array([-7.0, -0.3, 0])


class Scene06PeriodTwo(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _ladder() -> dict[str, VGroup]:
    rows = {}
    for label, y in ROW_Y.items():
        l = pm.L_LETTERS.index(label[-1])
        row = orbital_row(l, label, box=0.84, label_size=cfg.FONT["label"])
        row.boxes.move_to([LADDER_X + (0.98 if l == 1 else 0), y, 0])
        row.tag.next_to(row.boxes, LEFT, buff=0.35)
        if l == 0:
            row.tag.move_to([LADDER_X - 1.75, y, 0])
        else:
            row.tag.move_to([LADDER_X - 1.75, y, 0])
        rows[label] = row
    return rows


def _outer_pieces(z: int) -> VGroup:
    """``[core] n s^k`` as separate pieces, so the shell number and the pattern can glow apart."""
    gas = pm.noble_core(z)
    shell, count = pm.ground_configuration(z)[-1]
    pieces = VGroup(
        eq(rf"[\mathrm{{{pm.symbol_of(gas)}}}]", cfg.FONT["section"], cfg.MUTED),
        eq(str(shell.n), cfg.FONT["section"], cfg.CYAN),
        eq(rf"{shell.letter}^{{{count}}}", cfg.FONT["section"], cfg.WHITE),
    ).arrange(RIGHT, buff=0.12)
    pieces[2].align_to(pieces[1], DOWN)
    return pieces


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "06", "Building period 2")

    board = build_board()
    placed = VGroup(board_tile(1), board_tile(2))
    rows = _ladder()
    core_arrows = row_arrows(rows["1s"], 2)
    core_label = chip("core, like helium", cfg.MUTED, cfg.FONT["tiny"]).next_to(rows["1s"].boxes, RIGHT, buff=0.4)
    scene.play(FadeIn(board), FadeIn(placed), run_time=1.0)
    scene.play(FadeIn(rows["1s"]), *[FadeIn(a) for a in core_arrows], run_time=0.8)
    scene.play(FadeIn(core_label, shift=LEFT * 0.2), rows["1s"].boxes.animate.set_stroke(cfg.GREEN), run_time=0.8)
    scene.play(FadeIn(rows["2s"], shift=UP * 0.2), FadeIn(rows["2p"].tag, shift=UP * 0.2), run_time=0.8)

    s_arrows = row_arrows(rows["2s"], 2)
    p_arrows = row_arrows(rows["2p"], 6)
    state = {"config": None, "tile": None}

    def show(z: int, arrow: Mobject, fly: bool = True, arrive: float = 1.1) -> VGroup:
        electron_arrives(scene, arrow, SOURCE, arrive)
        config = eq(pm.config_latex(z, core=True), cfg.FONT["label"], cfg.WHITE).move_to(CONFIG_AT)
        tile = big_tile(z, 1.8).move_to(TILE_AT)
        animations = [FadeIn(tile, shift=LEFT * 0.3)]
        animations.append(ReplacementTransform(state["config"], config) if state["config"] else FadeIn(config))
        scene.play(*animations, run_time=0.6)
        state["config"] = config
        seat = board_tile(z)
        if fly:
            scene.play(ReplacementTransform(tile, seat), run_time=0.85, path_arc=-PI / 6)
            placed.add(seat)
        else:
            state["tile"] = tile
        return seat if fly else tile

    def place(tile: VGroup, z: int) -> VGroup:
        seat = board_tile(z)
        scene.play(ReplacementTransform(tile, seat), run_time=1.0, path_arc=-PI / 6)
        placed.add(seat)
        return seat

    # --- Lithium: a new shell ----------------------------------------------
    beat(scene, t, 1)
    li_tile = show(3, s_arrows[0], fly=False, arrive=1.4)

    beat(scene, t, 2)
    li = place(li_tile, 3)
    below = DashedLine(placed[0].get_bottom(), li.get_top(), stroke_color=cfg.GOLD, stroke_width=4, dash_length=0.06)
    scene.play(Create(below), Indicate(VGroup(placed[0], li), color=cfg.GOLD, scale_factor=1.15), run_time=1.2)

    beat(scene, t, 3)
    show(4, s_arrows[1])
    scene.play(rows["2s"].boxes.animate.set_stroke(cfg.GREEN), FadeOut(below), run_time=0.6)

    # --- 2p opens ----------------------------------------------------------
    beat(scene, t, 4)
    places = txt("3 orbitals · 6 places", cfg.FONT["small"], cfg.GREEN).next_to(rows["2p"].boxes, UP, buff=0.22)
    scene.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in rows["2p"].boxes], lag_ratio=0.2),
               FadeIn(places), run_time=1.2)
    scene.play(Indicate(rows["2p"].boxes, color=cfg.GREEN, scale_factor=1.08), run_time=1.0)

    beat(scene, t, 5)
    show(5, p_arrows[0])

    # --- Carbon: Hund's choice ---------------------------------------------
    beat(scene, t, 6)
    paired = spin_arrow(rows["2p"].boxes[0], -1, rows["2p"].box_size).set_color(cfg.RED).set_opacity(0.55)
    option_a = cross_mark(0.15).move_to(rows["2p"].boxes[0].get_corner(DR) + np.array([0.08, -0.02, 0]))
    option_b = check_mark(0.17).move_to(rows["2p"].boxes[1].get_corner(DR) + np.array([0.1, 0.02, 0]))
    scene.play(FadeOut(places), FadeIn(paired, shift=DOWN * 0.3), run_time=0.8)
    hint = txt("pair up?", cfg.FONT["small"], cfg.RED).next_to(rows["2p"].boxes, UP, buff=0.22)
    scene.play(FadeIn(hint), run_time=0.5)
    scene.play(FadeIn(option_a, scale=1.3), FadeOut(paired), run_time=0.7)
    hund = txt("Spread out first", cfg.FONT["small"], cfg.GREEN).move_to(hint)
    scene.play(ReplacementTransform(hint, hund), run_time=0.5)
    show(6, p_arrows[1])
    scene.play(FadeIn(option_b, scale=1.3), run_time=0.5)

    beat(scene, t, 7)
    scene.play(FadeOut(option_a), FadeOut(option_b), run_time=0.4)
    show(7, p_arrows[2])
    scene.play(Indicate(VGroup(*p_arrows[:3]), color=cfg.WHITE), run_time=0.8)

    beat(scene, t, 8)
    paired_label = txt("now they pair", cfg.FONT["small"], cfg.PURPLE).move_to(hund)
    scene.play(ReplacementTransform(hund, paired_label), run_time=0.4)
    show(8, p_arrows[3], arrive=0.9)
    show(9, p_arrows[4], arrive=0.9)

    beat(scene, t, 9)
    show(10, p_arrows[5], arrive=1.0)
    full = chip("shell 2 FULL", cfg.GREEN, cfg.FONT["small"]).move_to(paired_label)
    scene.play(ReplacementTransform(paired_label, full), rows["2p"].boxes.animate.set_stroke(cfg.GREEN),
               Flash(rows["2p"].boxes.get_center(), color=cfg.GREEN, flash_radius=1.6, line_length=0.3), run_time=1.0)

    # --- Count the row -----------------------------------------------------
    beat(scene, t, 10)
    head = swap_heading(scene, head, "2 + 6 = 8 elements")
    s_tiles = VGroup(*[m for m in placed if m.z in (3, 4)])
    p_tiles = VGroup(*[m for m in placed if 5 <= m.z <= 10])
    s_count = width_brace(s_tiles, 2, cfg.BLUE, direction=DOWN, size=cfg.FONT["label"])
    p_count = width_brace(p_tiles, 6, cfg.GREEN, direction=DOWN, size=cfg.FONT["label"])
    for brace in (s_count, p_count):
        brace.brace.set_opacity(0)
        brace.label.move_to(brace.brace)
    scene.play(FadeOut(full), FadeOut(core_label), run_time=0.4)
    scene.play(Circumscribe(s_tiles, color=cfg.BLUE), FadeIn(s_count.label), run_time=1.2)
    scene.play(Circumscribe(p_tiles, color=cfg.GREEN), FadeIn(p_count.label), run_time=1.2)

    beat(scene, t, 11)
    total = VGroup(eq("2", cfg.FONT["title"], cfg.BLUE), eq("+", cfg.FONT["title"]),
                   eq("6", cfg.FONT["title"], cfg.GREEN), eq("=", cfg.FONT["title"]),
                   eq("8", cfg.FONT["hero"], cfg.GOLD)).arrange(RIGHT, buff=0.3).move_to(CONFIG_AT + LEFT * 0.4 + UP * 0.35)
    scene.play(FadeOut(state["config"]), LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in total], lag_ratio=0.2),
               run_time=1.4)

    # --- Left and right; the gap waits --------------------------------------
    beat(scene, t, 12)
    left = glow_frame(s_tiles, cfg.BLUE, buff=0.07)
    right = glow_frame(p_tiles, cfg.GREEN, buff=0.07)
    scene.play(Create(left), run_time=0.8)
    scene.play(Create(right), run_time=0.8)

    beat(scene, t, 13)
    gap_left = board_point(row=2, col=3) + LEFT * BOARD_PITCH * 0.45 + UP * BOARD_PITCH * 0.45
    gap_right = board_point(row=3, col=12) + RIGHT * BOARD_PITCH * 0.45 + DOWN * BOARD_PITCH * 0.45
    gap = DashedVMobject(Rectangle(width=gap_right[0] - gap_left[0], height=gap_left[1] - gap_right[1],
                                   stroke_color=cfg.GOLD, stroke_width=3), num_dashes=60)
    gap.move_to((gap_left + gap_right) / 2)
    wait = txt("d comes later", cfg.FONT["small"], cfg.GOLD).move_to(gap)
    scene.play(Create(gap), run_time=1.0)
    scene.play(FadeIn(wait), run_time=0.6)

    # --- Period 3, fast-forward ---------------------------------------------
    beat(scene, t, 14)
    scene.play(FadeOut(VGroup(left, right, gap, wait, total, s_count.label, p_count.label)),
               *[FadeOut(r) for r in rows.values()], *[FadeOut(a) for a in core_arrows + s_arrows + p_arrows],
               run_time=0.8)
    period3 = VGroup(*[board_tile(z) for z in pm.period_members(3)])
    scene.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.4, scale=1.3) for m in period3], lag_ratio=0.3), run_time=3.0)
    placed.add(*period3)
    again = txt("8 again", cfg.FONT["label"], cfg.GOLD).move_to(board_point(row=3, col=7.5))
    scene.play(FadeIn(again, scale=1.2), run_time=0.6)

    # --- Lithium and sodium --------------------------------------------------
    beat(scene, t, 15)
    head = swap_heading(scene, head, "Same outer pattern")
    li_big = big_tile(3, 1.9).move_to([-4.7, -1.55, 0])
    na_big = big_tile(11, 1.9).move_to([4.7, -1.55, 0])
    scene.play(FadeOut(again), FadeIn(li_big, shift=UP * 0.3), FadeIn(na_big, shift=UP * 0.3), run_time=1.0)

    beat(scene, t, 16)
    li_conf = _outer_pieces(3).next_to(li_big, DOWN, buff=0.35)
    scene.play(FadeIn(li_conf, shift=UP * 0.2), run_time=0.8)

    beat(scene, t, 17)
    na_conf = _outer_pieces(11).next_to(na_big, DOWN, buff=0.35)
    scene.play(FadeIn(na_conf, shift=UP * 0.2), run_time=0.8)

    beat(scene, t, 18)
    scene.play(Indicate(li_conf[1], color=cfg.CYAN, scale_factor=1.4), Indicate(na_conf[1], color=cfg.CYAN, scale_factor=1.4),
               run_time=1.2)
    scene.play(li_conf[2].animate.set_color(cfg.GOLD), na_conf[2].animate.set_color(cfg.GOLD), run_time=0.6)
    same = VGroup(eq(r"s^{1}", cfg.FONT["title"], cfg.GOLD), txt("same pattern", cfg.FONT["label"], cfg.GOLD))
    same.arrange(RIGHT, buff=0.25).move_to([0, -1.7, 0])
    scene.play(TransformFromCopy(VGroup(li_conf[2], na_conf[2]), same[0]), FadeIn(same[1]), run_time=1.2)

    beat(scene, t, 19)
    column = VGroup(*[m for m in placed if m.z in (1, 3, 11)])
    spine = glow_frame(VGroup(*[m for m in placed if m.z in (3, 11)]), cfg.GOLD, buff=0.08)
    scene.play(Create(spine), run_time=0.8)
    li_seat = next(m for m in placed if m.z == 3)
    na_seat = next(m for m in placed if m.z == 11)
    arrow = CurvedArrow(li_big.get_top() + UP * 0.05, li_seat.get_left() + LEFT * 0.12, angle=-PI / 4,
                        color=cfg.GOLD, stroke_width=4)
    arrow2 = CurvedArrow(na_big.get_top() + UP * 0.05, na_seat.get_bottom() + DOWN * 0.1,
                         angle=PI / 6, color=cfg.GOLD, stroke_width=4)
    scene.play(Create(arrow), Create(arrow2), run_time=0.8)
    scene.play(Indicate(column, color=cfg.GOLD, scale_factor=1.12), run_time=1.4)
    scene.play(Indicate(same, color=cfg.WHITE, scale_factor=1.1), run_time=1.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
