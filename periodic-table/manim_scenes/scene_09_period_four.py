"""Period 4 gets long: 4s fills before 3d, and ten d seats make the d block.

The ladder starts in shell-number order (3p, 3d, 4s, 4p), so electron 19
visibly passes the empty 3d to reach 4s. Then the rows re-sort into the order
electrons actually fill them for atoms like potassium and calcium.
"""

from manim_scenes.common import *

LADDER_X = -2.7
SHELL_ORDER_Y = {"3p": -3.6, "3d": -2.65, "4s": -1.7, "4p": -0.75}
FILL_ORDER_Y = {"3p": -3.6, "4s": -2.65, "3d": -1.7, "4p": -0.75}
TILE_AT = np.array([2.7, -2.15, 0])
CONFIG_AT = np.array([5.5, -2.15, 0])
SOURCE = np.array([0.9, -0.3, 0])
BOX = 0.62


class Scene09PeriodFour(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _row(label: str) -> VGroup:
    l = pm.L_LETTERS.index(label[-1])
    row = orbital_row(l, label, box=BOX, gap=BOX * 0.16, label_size=cfg.FONT["label"])
    row.boxes.move_to([LADDER_X, SHELL_ORDER_Y[label], 0])
    row.tag.move_to([LADDER_X - 2.55, SHELL_ORDER_Y[label], 0])
    return row


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "09", "Where does electron 19 go?")

    board = build_board()
    placed = VGroup(*[board_tile(z) for z in range(1, 19)])
    rows = {label: _row(label) for label in ("3p", "3d", "4s", "4p")}
    core_arrows = row_arrows(rows["3p"], 6)
    core = chip("[Ar] core", cfg.GREEN, cfg.FONT["tiny"]).next_to(rows["3p"].boxes, RIGHT, buff=0.5)
    scene.play(FadeIn(board), LaggedStart(*[FadeIn(m, scale=0.8) for m in placed], lag_ratio=0.04), run_time=1.6)
    scene.play(FadeIn(rows["3p"]), *[FadeIn(a) for a in core_arrows], run_time=0.8)
    scene.play(FadeIn(core, shift=LEFT * 0.2), rows["3p"].boxes.animate.set_stroke(cfg.GREEN), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(rows[k], shift=UP * 0.15) for k in ("3d", "4s", "4p")], lag_ratio=0.25), run_time=1.2)

    # --- Potassium: the nineteenth electron ----------------------------------
    beat(scene, t, 1)
    k_tile = big_tile(19, 1.7).move_to(TILE_AT)
    electron = glow_dot(SOURCE, 0.13)
    nineteen = txt("electron 19", cfg.FONT["small"], cfg.CYAN).next_to(electron, RIGHT, buff=0.25)
    scene.play(FadeIn(k_tile, shift=LEFT * 0.3), FadeIn(electron, scale=0.4), FadeIn(nineteen), run_time=0.9)

    beat(scene, t, 2)
    empty = txt("empty", cfg.FONT["small"], cfg.GOLD).next_to(rows["3d"].boxes, RIGHT, buff=0.35)
    scene.play(Indicate(rows["3d"].boxes, color=cfg.GOLD, scale_factor=1.08), FadeIn(empty), run_time=1.2)
    scene.play(Circumscribe(rows["3d"].boxes, color=cfg.GOLD), run_time=1.2)

    beat(scene, t, 3)
    guess = DashedLine(electron.get_center(), rows["3d"].boxes[-1].get_right() + RIGHT * 0.05,
                       stroke_color=cfg.GOLD, stroke_width=3, dash_length=0.12)
    mark = txt("?", cfg.FONT["title"], cfg.GOLD).next_to(guess.get_center(), RIGHT, buff=0.25)
    scene.play(Create(guess), FadeIn(mark), FadeOut(nineteen), run_time=1.0)
    scene.play(electron.animate.move_to(interpolate(guess.get_start(), guess.get_end(), 0.6)), run_time=1.0)

    beat(scene, t, 4)
    s_arrows = row_arrows(rows["4s"], 2)
    path = ArcBetweenPoints(electron.get_center(), s_arrows[0].get_center(), angle=-PI / 2)
    scene.play(FadeOut(guess), FadeOut(mark), MoveAlongPath(electron, path), run_time=1.1)
    scene.play(ReplacementTransform(electron, s_arrows[0]), run_time=0.4)
    config = eq(pm.config_latex(19), cfg.FONT["label"]).move_to(CONFIG_AT)
    scene.play(FadeIn(config, shift=LEFT * 0.2), run_time=0.6)
    seat = board_tile(19)
    scene.play(ReplacementTransform(k_tile, seat), run_time=1.0, path_arc=-PI / 6)
    placed.add(seat)

    beat(scene, t, 5)
    ca_tile = big_tile(20, 1.7).move_to(TILE_AT)
    scene.play(FadeIn(ca_tile, shift=LEFT * 0.3), run_time=0.5)
    electron_arrives(scene, s_arrows[1], SOURCE, 1.1)
    new_config = eq(pm.config_latex(20), cfg.FONT["label"]).move_to(CONFIG_AT)
    scene.play(ReplacementTransform(config, new_config), run_time=0.5)
    config = new_config
    seat = board_tile(20)
    scene.play(ReplacementTransform(ca_tile, seat), run_time=0.9, path_arc=-PI / 6)
    placed.add(seat)

    beat(scene, t, 6)
    next_guess = txt("4p next?", cfg.FONT["small"], cfg.GREEN).next_to(rows["4p"].boxes, RIGHT, buff=0.35)
    scene.play(Indicate(rows["4p"].boxes, color=cfg.GREEN, scale_factor=1.1), FadeIn(next_guess), run_time=1.2)

    # --- Re-sort by filling order --------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "Follow the filling sequence")
    axis = Arrow([LADDER_X - 3.45, -3.95, 0], [LADDER_X - 3.45, -0.35, 0], buff=0, color=cfg.MUTED, stroke_width=4)
    axis_tag = txt("fill order", cfg.FONT["tiny"], cfg.MUTED).rotate(PI / 2).next_to(axis, LEFT, buff=0.1)
    scene.play(GrowArrow(axis), FadeIn(axis_tag), FadeOut(empty), FadeOut(next_guess), FadeOut(core), run_time=0.8)
    scene.play(Wiggle(VGroup(rows["3d"], rows["4s"])), run_time=1.2)

    beat(scene, t, 8)
    moving = {label: VGroup(rows[label], *(s_arrows if label == "4s" else [])) for label in ("3d", "4s")}
    scene.play(*[moving[label].animate.shift(UP * (FILL_ORDER_Y[label] - SHELL_ORDER_Y[label])) for label in moving],
               run_time=1.6, path_arc=PI / 3)
    note = txt("schematic sequence", cfg.FONT["tiny"], cfg.MUTED).next_to(rows["4p"].boxes, RIGHT, buff=0.45)
    scene.play(FadeIn(note, shift=LEFT * 0.2), run_time=0.6)

    beat(scene, t, 9)
    between = glow_frame(rows["3d"].boxes, cfg.GOLD, buff=0.1)
    scene.play(Create(between), run_time=0.8)
    scene.play(Indicate(rows["3d"].tag, color=cfg.GOLD, scale_factor=1.3), run_time=1.0)

    # --- Ten seats: Sc to Zn ----------------------------------------------------
    beat(scene, t, 10)
    head = swap_heading(scene, head, "The d block: ten places")
    d_arrows = row_arrows(rows["3d"], 10)
    scene.play(FadeOut(between), FadeOut(config), FadeOut(note), run_time=0.5)

    beat(scene, t, 11)
    d_tiles = VGroup()
    for z in range(21, 31):
        seat = board_tile(z)
        counts = {shell.label: count for shell, count in pm.ground_configuration(z)}
        new_d = row_arrows(rows["3d"], counts["3d"])
        new_s = row_arrows(rows["4s"], counts["4s"])
        old_d = d_arrows if z > 21 else []
        scene.play(*[FadeOut(a) for a in old_d + s_arrows],
                   *[FadeIn(a) for a in new_d + new_s],
                   FadeIn(seat, shift=DOWN * 0.3, scale=1.3), run_time=0.95)
        d_arrows, s_arrows = new_d, new_s
        d_tiles.add(seat)
    placed.add(*d_tiles)

    beat(scene, t, 12)
    ten = txt("10", cfg.FONT["hero"], cfg.GOLD).move_to(board_point(row=2, col=7.5) + DOWN * BOARD_PITCH * 0.5)
    scene.play(Circumscribe(d_tiles, color=cfg.GOLD), FadeIn(ten, scale=1.3), run_time=1.4)

    beat(scene, t, 13)
    product = VGroup(eq("5", cfg.FONT["title"], cfg.GOLD), txt("d orbitals", cfg.FONT["small"], cfg.MUTED),
                     eq(r"\times\,2", cfg.FONT["title"]), eq("=", cfg.FONT["title"]),
                     eq("10", cfg.FONT["title"], cfg.GOLD)).arrange(RIGHT, buff=0.2).move_to(np.array([3.9, -1.8, 0]))
    fit_width(product, 6.4)
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in product], lag_ratio=0.15), run_time=1.2)
    scene.play(Indicate(rows["3d"].boxes, color=cfg.GOLD), run_time=1.0)

    # --- Chromium and copper: honest exceptions ---------------------------------
    beat(scene, t, 14)
    scene.play(FadeOut(product), run_time=0.4)
    rebels = VGroup()
    for z in (24, 29):
        tile = next(m for m in placed if m.z == z)
        name = txt(pm.symbol_of(z), cfg.FONT["label"], cfg.ORANGE)
        actual = eq(pm.config_latex(z), cfg.FONT["small"], cfg.WHITE)
        card = VGroup(name, actual)
        card.arrange(RIGHT, buff=0.35)
        rebels.add(card)
        scene.play(tile.box.animate.set_stroke(cfg.ORANGE, width=5), Flash(tile, color=cfg.ORANGE, flash_radius=0.45),
                   run_time=0.8)
    rebels.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(np.array([3.9, -2.0, 0]))
    scene.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in rebels], lag_ratio=0.4), run_time=1.6)
    scene.play(Indicate(rebels[0], color=cfg.ORANGE, scale_factor=1.05), run_time=1.0)
    scene.play(Indicate(rebels[1], color=cfg.ORANGE, scale_factor=1.05), run_time=1.0)
    scene.wait(0.4)
    still = chip("still 10 seats", cfg.GOLD, cfg.FONT["small"]).move_to(ten)
    scene.play(FadeOut(ten), FadeIn(still, scale=1.2), run_time=0.7)

    # --- 4p closes the period ----------------------------------------------------
    beat(scene, t, 15)
    scene.play(FadeOut(rebels), FadeOut(still), FadeIn(ten), run_time=0.5)
    p_arrows = row_arrows(rows["4p"], 6)
    for z, arrow in zip(range(31, 37), p_arrows):
        seat = board_tile(z)
        scene.play(drop_in(arrow), FadeIn(seat, shift=DOWN * 0.3, scale=1.3), run_time=0.75)
        placed.add(seat)

    beat(scene, t, 16)
    recipe = pm.period_recipe(4)
    parts = []
    for index, (shell, count) in enumerate(recipe):
        if index:
            parts.append(eq("+", cfg.FONT["title"]))
        parts.append(eq(str(count), cfg.FONT["title"], cfg.BLOCK_COLORS[shell.letter]))
    parts += [eq("=", cfg.FONT["title"]), eq(str(sum(c for _, c in recipe)), cfg.FONT["hero"], cfg.GOLD)]
    total = VGroup(*parts).arrange(RIGHT, buff=0.25).move_to(np.array([3.9, -2.0, 0]))
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in total], lag_ratio=0.15), run_time=1.4)

    beat(scene, t, 17)
    d_frame = glow_frame(d_tiles, cfg.GOLD, buff=0.07)
    tm = txt("d block", cfg.FONT["label"], cfg.GOLD).move_to(ten)
    scene.play(Create(d_frame), ReplacementTransform(ten, tm), run_time=1.2)
    scene.play(Indicate(d_tiles, color=cfg.GOLD, scale_factor=1.1), Indicate(rows["3d"].boxes, color=cfg.GOLD),
               run_time=1.6)
    scene.play(Indicate(total, color=cfg.WHITE, scale_factor=1.06), run_time=1.7)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
