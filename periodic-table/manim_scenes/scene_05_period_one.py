"""Period 1: one s orbital, two electrons, two elements — and helium's seat.

Layout: the build board (rows 1–4 of the table) across the top; the orbital
"workshop" underneath, where electrons arrive before each element is placed.
"""

from manim_scenes.common import *

BOX_AT = np.array([-4.5, -1.9, 0])
BOX = 1.3
TILE_AT = np.array([-1.0, -1.9, 0])
NOTE_AT = np.array([3.6, -1.9, 0])
SOURCE = np.array([-6.9, 0.3, 0])


class Scene05PeriodOne(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "05", "Period 1: one s orbital")

    board = build_board()
    row = orbital_row(0, None, box=BOX)
    row.boxes.move_to(BOX_AT)
    tag = eq("1s", cfg.FONT["title"], cfg.BLOCK_COLORS["s"]).next_to(row.boxes, LEFT, buff=0.45)
    room = txt("room for 2", cfg.FONT["label"], cfg.MUTED).next_to(row.boxes, DOWN, buff=0.4)
    scene.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in board], lag_ratio=0.01), run_time=1.6)
    scene.play(FadeIn(row.boxes, scale=0.7), Write(tag), run_time=1.0)
    scene.play(FadeIn(room, shift=UP * 0.15), run_time=0.6)
    scene.play(Indicate(row.boxes, color=cfg.BLUE, scale_factor=1.1), run_time=1.0)

    # --- Hydrogen -----------------------------------------------------------
    beat(scene, t, 1)
    arrows = row_arrows(row, 2)
    electron_arrives(scene, arrows[0], SOURCE, 1.6)

    beat(scene, t, 2)
    config = eq(r"1s^{1}", cfg.FONT["title"], cfg.WHITE).move_to(room)
    tile = big_tile(1, 2.0).move_to(TILE_AT)
    scene.play(ReplacementTransform(room, config), run_time=0.8)
    scene.play(FadeIn(tile, shift=LEFT * 0.4), run_time=0.8)
    scene.play(Indicate(config, color=cfg.CYAN), run_time=1.2)

    beat(scene, t, 3)
    seat = board_tile(1)
    scene.play(ReplacementTransform(tile, seat), run_time=1.4, path_arc=-PI / 5)
    scene.play(Flash(seat, color=cfg.BLUE, line_length=0.25, flash_radius=0.5), run_time=0.7)

    # --- Helium ------------------------------------------------------------
    beat(scene, t, 4)
    electron_arrives(scene, arrows[1], SOURCE, 1.6)
    spins = txt("opposite spin", cfg.FONT["label"], cfg.SPIN_DOWN).next_to(row.boxes, RIGHT, buff=0.4)
    scene.play(FadeIn(spins, shift=LEFT * 0.2), run_time=0.6)

    beat(scene, t, 5)
    config2 = eq(r"1s^{2}", cfg.FONT["title"], cfg.WHITE).move_to(config)
    full = chip("FULL", cfg.GREEN, cfg.FONT["small"]).next_to(row.boxes, UP, buff=0.3)
    tile = big_tile(2, 2.0).move_to(TILE_AT)
    scene.play(ReplacementTransform(config, config2), FadeOut(spins), FadeIn(full, scale=1.2),
               row.boxes.animate.set_stroke(cfg.GREEN), run_time=0.9)
    scene.play(FadeIn(tile, shift=LEFT * 0.4), run_time=0.7)
    # Helium's seat by filling alone: the second s seat, right next to hydrogen.
    seat_he = element_tile(2, BOARD_PITCH * 0.9).move_to(board_point(row=1, col=2))
    scene.play(ReplacementTransform(tile, seat_he), run_time=1.4, path_arc=-PI / 5)

    # --- No third state ----------------------------------------------------
    beat(scene, t, 6)
    third = glow_dot(SOURCE, 0.13)
    scene.play(FadeOut(full), FadeIn(third, scale=0.5), run_time=0.4)
    scene.play(third.animate.move_to(BOX_AT + UP * 1.2), run_time=1.0)
    block = cross_mark().move_to(BOX_AT + UP * 1.2 + RIGHT * 0.65)
    scene.play(FadeIn(block, scale=1.4), Wiggle(row.boxes), run_time=1.0)
    shell = orbital_row(0, None, box=0.85)
    shell.boxes.move_to(np.array([TILE_AT[0], -0.45, 0]))
    shell_tag = eq("2s", cfg.FONT["label"], cfg.BLUE).next_to(shell.boxes, LEFT, buff=0.35)
    shell_label = txt("new shell", cfg.FONT["small"], cfg.MUTED).next_to(shell.boxes, RIGHT, buff=0.4)
    scene.play(FadeIn(shell.boxes, shift=DOWN * 0.2), FadeIn(shell_tag), FadeIn(shell_label), FadeOut(block), run_time=1.0)
    scene.play(third.animate.move_to(shell.boxes.get_center()), run_time=1.2, path_arc=-PI / 4)
    scene.play(FadeOut(third), VGroup(shell.boxes, shell_tag, shell_label).animate.set_opacity(0.35), run_time=0.7)

    # --- The row closes after two ------------------------------------------
    beat(scene, t, 7)
    period_frame = glow_frame(VGroup(seat, seat_he), cfg.GOLD, buff=0.08)
    two = txt("2 elements", cfg.FONT["label"], cfg.GOLD).next_to(period_frame, RIGHT, buff=0.35)
    scene.play(FadeOut(VGroup(shell.boxes, shell_tag, shell_label)), Create(period_frame), run_time=1.0)
    scene.play(FadeIn(two, shift=LEFT * 0.2), Indicate(VGroup(seat, seat_he), color=cfg.GOLD), run_time=1.2)

    beat(scene, t, 8)
    reason = VGroup(
        txt("period 1", cfg.FONT["body"], cfg.WHITE),
        eq(r"=", cfg.FONT["body"]),
        eq(r"1s", cfg.FONT["body"], cfg.BLUE),
        eq(r"\rightarrow", cfg.FONT["body"]),
        eq(r"2", cfg.FONT["title"], cfg.GOLD),
    ).arrange(RIGHT, buff=0.28).move_to(NOTE_AT + UP * 0.1)
    scene.play(FadeIn(reason, shift=UP * 0.2), run_time=1.0)
    scene.play(Circumscribe(reason, color=cfg.GOLD), run_time=1.4)

    # --- Helium's surprise --------------------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "Helium: a closed shell")
    scene.play(FadeOut(reason), FadeOut(period_frame), FadeOut(two), run_time=0.6)
    s_side = glow_frame(tiles_of(board, [1, 3, 4, 11, 12, 19, 20]), cfg.BLUE, buff=0.06)
    scene.play(Create(s_side), Indicate(config2, color=cfg.BLUE, scale_factor=1.15), run_time=1.4)
    scene.play(Indicate(seat_he, color=cfg.BLUE, scale_factor=1.15), run_time=1.0)

    beat(scene, t, 10)
    nobles = VGroup(*[board_tile(z, cfg.GREEN) for z in (10, 18, 36)])
    noble_label = txt("noble gases", cfg.FONT["small"], cfg.GREEN).next_to(nobles, DOWN, buff=0.2)
    noble_label.align_to(nobles, RIGHT).shift(RIGHT * 0.25)
    scene.play(FadeOut(s_side), LaggedStart(*[FadeIn(n, scale=0.6) for n in nobles], lag_ratio=0.25), run_time=1.4)
    scene.play(FadeIn(noble_label), run_time=0.5)
    scene.play(seat_he.animate.move_to(board_point(2)), run_time=1.8, path_arc=-PI / 4)
    scene.play(Flash(seat_he, color=cfg.GREEN, line_length=0.25, flash_radius=0.5),
               row.boxes.animate.set_stroke(cfg.GREEN, width=6), run_time=0.8)
    closed = txt("closed shell", cfg.FONT["label"], cfg.GREEN).move_to(row.boxes.get_center() + UP * 1.15)
    scene.play(FadeIn(closed, shift=DOWN * 0.15), run_time=0.6)

    beat(scene, t, 11)
    pattern = chip("pattern: 1s²", cfg.BLUE, cfg.FONT["label"])
    behaviour = chip("chemistry: noble gas", cfg.GREEN, cfg.FONT["label"])
    pair = VGroup(pattern, behaviour).arrange(DOWN, buff=0.35).move_to(NOTE_AT)
    scene.play(FadeIn(pattern, shift=UP * 0.2), run_time=0.6)
    scene.play(FadeIn(behaviour, shift=UP * 0.2), run_time=0.6)
    seat_rule = txt("placed by chemistry", cfg.FONT["small"], cfg.MUTED).next_to(pair, DOWN, buff=0.35)
    scene.play(FadeIn(seat_rule), Indicate(behaviour, color=cfg.GREEN, scale_factor=1.08), run_time=1.2)

    # --- On to period 2 ----------------------------------------------------
    beat(scene, t, 12)
    scene.play(FadeOut(VGroup(pair, seat_rule, noble_label, closed)), nobles.animate.set_opacity(0.25), run_time=0.7)
    period2 = tiles_of(board, pm.period_members(2))
    scene.play(Indicate(period2, color=cfg.CYAN, scale_factor=1.15), run_time=1.6)
    preview = VGroup(*[orbital_row(l, label, box=0.75) for l, label in ((0, "2s"), (1, "2p"))])
    preview.arrange(RIGHT, buff=1.2).move_to(NOTE_AT + DOWN * 0.1)
    scene.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in preview], lag_ratio=0.4), run_time=1.4)
    scene.play(preview.animate.set_opacity(0.55), Indicate(row.boxes, color=cfg.GREEN), run_time=1.4)
    scene.play(Indicate(preview, color=cfg.CYAN, scale_factor=1.06), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
