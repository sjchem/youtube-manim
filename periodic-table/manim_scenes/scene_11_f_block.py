"""The giant gap at the bottom: the f block is cut out of a 32-column table.

Tiles move between two layouts that the filling model computes: the expanded
32-column ``wide`` form, where each f strip sits inside its period, and the
familiar 18-column ``standard`` form, where the strips are parked below.
"""

from manim_scenes.common import *

STD_PITCH = 0.66
STD_CENTER = DOWN * 0.12
WIDE_PITCH = 0.43
WIDE_CENTER = UP * 0.55
F_ROW_Y = -2.75


class Scene11FBlock(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _std(z: int) -> np.ndarray:
    return table_point(z, "standard", STD_PITCH, STD_CENTER)


def _wide(z: int) -> np.ndarray:
    return table_point(z, "wide", WIDE_PITCH, WIDE_CENTER)


def _to(tile: VGroup, point, pitch: float) -> Animation:
    return tile.animate.scale_to_fit_width(pitch * 0.9).move_to(point)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "11", "Period 6 begins: 6s")
    tiles: dict[int, VGroup] = {}
    for z in range(1, 55):
        tiles[z] = element_tile(z, STD_PITCH * 0.9).move_to(_std(z))
    scene.play(FadeIn(VGroup(*tiles.values())), run_time=0.8)
    for z in (55, 56):
        tiles[z] = element_tile(z, STD_PITCH * 0.9).move_to(_std(z))
        scene.play(FadeIn(tiles[z], shift=DOWN * 0.3, scale=1.4), run_time=0.8)
    s_tag = eq("6s", cfg.FONT["label"], cfg.BLUE).next_to(VGroup(tiles[55], tiles[56]), RIGHT, buff=0.3)
    scene.play(FadeIn(s_tag), run_time=0.5)

    # --- 4f opens: seven orbitals -------------------------------------------
    beat(scene, t, 1)
    head = swap_heading(scene, head, "4f adds fourteen places")
    f_row = orbital_row(3, "4f", box=0.62, gap=0.1, label_size=cfg.FONT["label"])
    f_row.move_to(np.array([0.4, -3.55, 0]))
    scene.play(FadeOut(s_tag), FadeIn(f_row, shift=UP * 0.2), run_time=1.0)

    beat(scene, t, 2)
    f_zs = [z for z in pm.period_members(6) if pm.block(z) == "f"]
    arrows = row_arrows(f_row, 14)
    strip = VGroup()
    for index, (z, arrow) in enumerate(zip(f_zs, arrows)):
        tile = element_tile(z, STD_PITCH * 0.9).move_to(np.array([(index - 6.5) * STD_PITCH, -2.45, 0]))
        tiles[z] = tile
        strip.add(tile)
    scene.play(LaggedStart(*[AnimationGroup(drop_in(a), FadeIn(m, shift=UP * 0.3)) for a, m in zip(arrows, strip)],
                           lag_ratio=0.3), run_time=4.6)
    fourteen = txt("14", cfg.FONT["title"], cfg.PURPLE).next_to(strip, RIGHT, buff=0.35)
    scene.play(FadeIn(fourteen, scale=1.3), run_time=0.6)

    # --- Keep atomic-number order ------------------------------------
    beat(scene, t, 3)
    head = swap_heading(scene, head, "Keep atomic-number order")
    scene.play(FadeOut(f_row), FadeOut(VGroup(*arrows)), FadeOut(fourteen), run_time=0.5)
    scene.play(*[_to(tile, _wide(z), WIDE_PITCH) for z, tile in tiles.items()], run_time=2.6,
               rate_func=rate_functions.ease_in_out_cubic)

    beat(scene, t, 4)
    rest6 = [z for z in pm.period_members(6) if z not in tiles]
    for z in rest6:
        tiles[z] = element_tile(z, WIDE_PITCH * 0.9).move_to(_wide(z))
    scene.play(LaggedStart(*[FadeIn(tiles[z], shift=DOWN * 0.25, scale=1.3) for z in rest6], lag_ratio=0.12),
               run_time=2.4)

    beat(scene, t, 5)
    recipe = pm.period_recipe(6)
    parts = []
    for index, (shell, count) in enumerate(recipe):
        if index:
            parts.append(eq("+", cfg.FONT["title"]))
        parts.append(eq(str(count), cfg.FONT["title"], cfg.BLOCK_COLORS[shell.letter]))
    parts += [eq("=", cfg.FONT["title"]), eq(str(sum(c for _, c in recipe)), cfg.FONT["hero"], cfg.GOLD)]
    total = VGroup(*parts).arrange(RIGHT, buff=0.25).move_to(DOWN * 2.35)
    labels = VGroup(*[eq(shell.label, cfg.FONT["tiny"], cfg.BLOCK_COLORS[shell.letter]).next_to(parts[2 * i], DOWN, buff=0.2)
                      for i, (shell, _) in enumerate(recipe)])
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in total], lag_ratio=0.12), run_time=1.6)
    scene.play(FadeIn(labels), run_time=0.6)
    row6 = VGroup(*[tiles[z] for z in pm.period_members(6)])
    scene.play(Indicate(row6, color=cfg.GOLD, scale_factor=1.05), run_time=1.4)

    beat(scene, t, 6)
    scene.play(FadeOut(total), FadeOut(labels), run_time=0.5)
    for z in pm.period_members(7):
        tiles[z] = element_tile(z, WIDE_PITCH * 0.9).move_to(_wide(z))
    row7 = [tiles[z] for z in pm.period_members(7)]
    scene.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.25, scale=1.3) for m in row7], lag_ratio=0.05), run_time=2.6)

    # --- The expanded shape: 32 wide ----------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "The expanded table: 32 columns")
    everything = VGroup(*tiles.values())
    brace = width_brace(everything, 32, cfg.GOLD, direction=DOWN, size=cfg.FONT["title"])
    scene.play(GrowFromCenter(brace.brace), FadeIn(brace.label, shift=UP * 0.2), run_time=1.2)
    move_camera(scene, zoom=0.94, run_time=2.0)

    beat(scene, t, 8)
    awkward = chip("32 columns → tiny print", cfg.ORANGE, cfg.FONT["label"]).move_to(DOWN * 3.65)
    hud(scene, awkward)
    scene.play(FadeIn(awkward, shift=UP * 0.2), run_time=0.8)
    scene.play(everything.animate.scale(0.9), rate_func=there_and_back, run_time=1.6)

    # --- Cut, slide, park ------------------------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "Cut out the two f strips")
    move_camera(scene, zoom=1.0, run_time=0.8)
    f_tiles = VGroup(*[tiles[z] for z in pm.elements_in_block("f")])
    cut = DashedVMobject(SurroundingRectangle(f_tiles, color=cfg.ORANGE, buff=0.06, stroke_width=4), num_dashes=70)
    scene.play(FadeOut(brace), FadeOut(awkward), Create(cut), run_time=1.4)
    scene.play(f_tiles.animate.set_opacity(0.9), Indicate(f_tiles, color=cfg.PURPLE, scale_factor=1.04), run_time=1.2)

    beat(scene, t, 10)
    head = swap_heading(scene, head, "Close the gap")
    right_side = [z for z in tiles if pm.position(z, "wide")[1] >= 17]
    lift = DOWN * 2.45
    scene.play(VGroup(f_tiles, cut).animate.shift(lift), run_time=1.4)
    scene.play(*[tiles[z].animate.shift(LEFT * 14 * WIDE_PITCH) for z in right_side], FadeOut(cut), run_time=1.8,
               rate_func=rate_functions.ease_in_out_cubic)

    beat(scene, t, 11)
    head = swap_heading(scene, head, "Park the strips underneath")
    scene.play(*[_to(tile, _std(z), STD_PITCH) for z, tile in tiles.items()], run_time=2.2,
               rate_func=rate_functions.ease_in_out_cubic)

    # --- They still belong to periods 6 and 7 -------------------------------------
    beat(scene, t, 12)
    head = swap_heading(scene, head, "Still part of periods 6 and 7")
    markers = VGroup()
    links = VGroup()
    for period_row, first_f in ((6, 57), (7, 89)):
        gap_point = (grid_point(period_row, 2, pitch=STD_PITCH, center=STD_CENTER)
                     + grid_point(period_row, 3, pitch=STD_PITCH, center=STD_CENTER)) / 2
        marker = Line(gap_point + UP * STD_PITCH * 0.42, gap_point + DOWN * STD_PITCH * 0.42,
                      stroke_color=cfg.PURPLE, stroke_width=7)
        markers.add(marker)
        start_tile = tiles[first_f]
        links.add(DashedLine(start_tile.get_left() + LEFT * 0.08, gap_point + DOWN * STD_PITCH * 0.42,
                             stroke_color=cfg.PURPLE, stroke_width=3.5, dash_length=0.08))
    scene.play(LaggedStart(*[Create(m) for m in markers], lag_ratio=0.4), run_time=1.0)
    scene.play(LaggedStart(*[Create(a) for a in links], lag_ratio=0.4), run_time=1.6)
    side = (tiles[57].get_left() + tiles[89].get_left()) / 2 + LEFT * 0.45
    belong = VGroup(txt("they", cfg.FONT["small"], cfg.PURPLE), txt("belong", cfg.FONT["small"], cfg.PURPLE),
                    txt("here", cfg.FONT["small"], cfg.PURPLE)).arrange(DOWN, buff=0.06)
    belong.move_to(side + DOWN * 0.15).align_to(side, RIGHT).shift(LEFT * 0.6)
    scene.play(FadeIn(belong), run_time=0.6)
    compact = txt("Same elements. Compact layout.", cfg.FONT["small"], cfg.GOLD).move_to(DOWN * 3.85)
    hud(scene, compact)
    scene.play(FadeIn(compact, shift=UP * 0.15), run_time=0.7)

    beat(scene, t, 13)
    head = swap_heading(scene, head, "Seven orbitals → fourteen columns")
    scene.play(FadeOut(VGroup(links, belong, compact)), run_time=0.6)
    f_frame = glow_frame(f_tiles, cfg.PURPLE, buff=0.08)
    seven = VGroup(eq("7", cfg.FONT["label"], cfg.PURPLE), eq(r"\times\,2 = 14", cfg.FONT["label"], cfg.GOLD))
    seven.arrange(RIGHT, buff=0.15).next_to(f_frame, DOWN, buff=0.12)
    scene.play(Create(f_frame), FadeIn(seven, shift=LEFT * 0.2), run_time=1.2)

    beat(scene, t, 14)
    scene.play(FadeOut(markers), run_time=0.4)
    scene.play(LaggedStart(*[Indicate(VGroup(*[tiles[z] for z in pm.elements_in_block(b) if z != 2]),
                                      color=cfg.BLOCK_COLORS[b], scale_factor=1.05) for b in "sdpf"], lag_ratio=0.25),
               run_time=2.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
