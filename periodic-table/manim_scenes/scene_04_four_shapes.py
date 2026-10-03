"""The signature scene: orbital capacities literally become the table's widths.

Act one meets each family as a lit 3D shape and counts its orbitals and
electrons. Act two turns every electron seat a subshell offers into one column
of tiles, lays the four blocks out in an exploded view, and slides them
together into the periodic table.
"""

from manim_scenes.common import *

FAMILIES = ("s", "p", "d", "f")
HERO_X = 4.25
SHAPES_Y = 1.15
HERO_BOXES_Y = -1.2
HERO_MATH_Y = -2.85
SUMMARY_Y = {"s": 2.4, "p": 1.0, "d": -0.4, "f": -1.8}
SUMMARY_LETTER_X = -6.85
SUMMARY_SHAPE_X = -5.85
SUMMARY_BOX_LEFT = -5.1
SUMMARY_BOX = 0.5
SUMMARY_NUMBER_X = -0.15
# Box size, gap and per-shape display size for the hero rows: one shape per box.
HERO_ROW = {"s": (1.0, 0.0, 1.0), "p": (1.0, 0.55, 0.62), "d": (0.86, 0.28, 0.5), "f": (0.72, 0.13, 0.4)}
SHAPE_RES = {0: (14, 28), 1: (14, 22), 2: (16, 26), 3: (16, 28)}

# Exploded table: the blocks pulled apart, then slid together.
PITCH = 0.6
CENTER = DOWN * 0.62
# Give the p-block headers room beside the staged f-orbital boxes.
EXPLODE = {"s": LEFT * 0.55, "d": ORIGIN, "p": RIGHT * 1.3, "f": DOWN * 0.5}
STAGE_BOX = 0.3
STAGE_AT = np.array([-0.55, 1.72, 0])


class Scene04FourShapes(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _hero_shapes(letter: str, row: VGroup) -> VGroup:
    """One lit 3D shape above each orbital box: m = -l .. l in the real basis."""
    l = pm.L_LETTERS.index(letter)
    size = HERO_ROW[letter][2]
    shapes = VGroup()
    for m, box in zip(range(-l, l + 1), row.boxes):
        shape = present_3d(orbital_surface(l, m, size, resolution=SHAPE_RES[l]), tilt=58 * DEGREES, turn=28 * DEGREES)
        shape.move_to([box.get_center()[0], SHAPES_Y + (0.15 if l == 0 else 0), 0])
        shapes.add(shape)
    return shapes


def _math(letter: str) -> VGroup:
    l = pm.L_LETTERS.index(letter)
    orbitals, capacity = 2 * l + 1, 2 * (2 * l + 1)
    pieces = VGroup(
        eq(str(orbitals), cfg.FONT["section"], cfg.BLOCK_COLORS[letter]),
        eq(r"\times\, 2", cfg.FONT["section"]),
        eq("=", cfg.FONT["section"]),
        eq(str(capacity), cfg.FONT["title"], cfg.GOLD),
    ).arrange(RIGHT, buff=0.3).move_to([HERO_X, HERO_MATH_Y, 0])
    return pieces


def _exploded_point(z: int) -> np.ndarray:
    return table_point(z, pitch=PITCH, center=CENTER) + EXPLODE[pm.block(z)]


def _natural_column(z: int) -> tuple[str, int]:
    """Block and seat number from filling alone — helium included, at seat 2 of s."""
    shell, seat = pm.filling_step(z)
    return shell.letter, seat


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "04", "Four families of orbitals")

    letters = VGroup(*[
        eq(letter, cfg.FONT["title"], cfg.BLOCK_COLORS[letter]).move_to([SUMMARY_LETTER_X, SUMMARY_Y[letter], 0])
        for letter in FAMILIES
    ])
    scene.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in letters], lag_ratio=0.2), run_time=1.6)

    summary: dict[str, VGroup] = {}
    numbers: dict[str, Mobject] = {}
    minis: dict[str, Mobject] = {}
    beats = {"s": (1, 2, 3), "p": (4, 5, 5), "d": (6, 7, 7), "f": (8, 9, 9)}
    for letter in FAMILIES:
        intro, fill, total = beats[letter]
        l = pm.L_LETTERS.index(letter)
        beat(scene, t, intro)

        box, gap, _ = HERO_ROW[letter]
        row = orbital_row(l, None, box=box, gap=gap).move_to([HERO_X, HERO_BOXES_Y, 0])
        shapes = _hero_shapes(letter, row)
        for shape in shapes:
            spin_forever(shape, 0.3)
        count = txt(f"{2 * l + 1} orbital{'s' if l else ''}", cfg.FONT["small"], cfg.MUTED)
        count.move_to([HERO_X, HERO_BOXES_Y + box / 2 + 0.42, 0])
        scene.play(LaggedStart(*[FadeIn(sh, scale=0.5) for sh in shapes], lag_ratio=0.15),
                   Indicate(letters[l], color=cfg.WHITE), run_time=1.4)
        scene.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in row.boxes], lag_ratio=0.12),
                   FadeIn(count), run_time=0.9)

        if fill != intro:
            beat(scene, t, fill)
        arrows = VGroup(*row_arrows(row, 2 * (2 * l + 1)))
        scene.play(LaggedStart(*[drop_in(a) for a in arrows], lag_ratio=0.5 if l == 0 else 0.12),
                   run_time=1.4 if l == 0 else 1.6)

        if total != fill:
            beat(scene, t, total)
        math = _math(letter)
        scene.play(LaggedStart(*[FadeIn(piece, shift=UP * 0.15) for piece in math], lag_ratio=0.2), run_time=1.0)

        # Shrink the whole station into its summary row on the left.
        target_y = SUMMARY_Y[letter]
        factor = SUMMARY_BOX / box
        target = np.array([SUMMARY_BOX_LEFT + row.width * factor / 2, target_y, 0])
        mini = present_3d(family_orbital(letter, 0.42 if letter != "s" else 0.32, small=True))
        mini.move_to([SUMMARY_SHAPE_X, target_y, 0])
        boxed = VGroup(row, arrows)
        final_number = eq(f"= {2 * (2 * l + 1)}", cfg.FONT["section"], cfg.GOLD)
        final_number.move_to([SUMMARY_NUMBER_X, target_y, 0])
        scene.play(
            boxed.animate.scale(factor).move_to(target),
            ReplacementTransform(math, final_number),
            FadeOut(count),
            *[FadeOut(sh, scale=0.4) for sh in shapes],
            FadeIn(mini, scale=0.4),
            run_time=1.2,
        )
        summary[letter], numbers[letter], minis[letter] = boxed, final_number, mini

    # --- 2, 6, 10, 14 ------------------------------------------------------
    beat(scene, t, 10)
    frames = VGroup(glow_frame(VGroup(*numbers.values()), cfg.GOLD, buff=0.2))
    scene.play(Create(frames), run_time=1.0)
    scene.play(LaggedStart(*[Indicate(numbers[f], color=cfg.WHITE, scale_factor=1.2) for f in FAMILIES],
                           lag_ratio=0.3), run_time=2.0)

    beat(scene, t, 11)
    rule = VGroup(
        txt("orbitals", cfg.FONT["label"], cfg.MUTED),
        eq(r"= 2l+1", cfg.FONT["section"]),
    ).arrange(RIGHT, buff=0.3)
    rule2 = VGroup(
        txt("capacity", cfg.FONT["label"], cfg.MUTED),
        eq(r"= 2\,(2l+1)", cfg.FONT["section"], cfg.GOLD),
    ).arrange(RIGHT, buff=0.3)
    ls = eq(r"l = 0,\ 1,\ 2,\ 3", cfg.FONT["label"], cfg.CYAN)
    rules = VGroup(ls, rule, rule2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * HERO_X + UP * 0.3)
    scene.play(FadeIn(ls, shift=UP * 0.2), run_time=0.7)
    scene.play(FadeIn(rule, shift=UP * 0.2), run_time=0.8)
    scene.play(FadeIn(rule2, shift=UP * 0.2), run_time=0.8)

    # --- Act two: every seat becomes a column ------------------------------
    beat(scene, t, 12)
    head = swap_heading(scene, head, "Capacity becomes width")
    scene.play(FadeOut(VGroup(*minis.values())), FadeOut(rules), FadeOut(frames), FadeOut(letters),
               FadeOut(VGroup(*numbers.values())), run_time=0.8)
    # Park the four rows in the empty top-centre of the table-to-be.
    staged = VGroup(*[summary[f].copy() for f in FAMILIES])
    for mob in staged:
        mob.scale(STAGE_BOX / SUMMARY_BOX)
    staged.arrange(RIGHT, buff=0.45).move_to(STAGE_AT)
    scene.play(*[summary[f].animate.become(staged[i]) for i, f in enumerate(FAMILIES)], run_time=1.0)

    tiles = {z: element_tile(z, PITCH * 0.88).move_to(_exploded_point(z)) for z in range(1, 119)}
    # He sits in seat 2 of the s block while the blocks are apart: its place by filling.
    tiles[2].move_to(grid_point(1, 2, pitch=PITCH, center=CENTER) + EXPLODE["s"])
    columns: dict[str, dict[int, list[int]]] = {f: {} for f in FAMILIES}
    for z in range(1, 119):
        letter, seat = _natural_column(z)
        columns[letter].setdefault(seat, []).append(z)

    headers: dict[str, VGroup] = {}
    blocks: dict[str, VGroup] = {}
    widths = {}
    for letter, (index, run) in zip(FAMILIES, ((12, 1.6), (14, 1.4), (14, 1.6), (15, 1.8))):
        if letter in ("p", "f"):
            beat(scene, t, index)
        boxed = summary[letter]
        row, arrows = boxed
        seats = sorted(columns[letter])
        tops = [min((tiles[z] for z in columns[letter][k]), key=lambda m: -m.get_center()[1]) for k in seats]
        head_points = [top.get_center() + UP * PITCH * 0.95 for top in tops]
        if letter == "f":
            head_points = [top.get_center() + UP * PITCH * 0.82 for top in tops]
        moved = VGroup(*[a.copy().scale_to_fit_height(PITCH * 0.62).move_to(p) for a, p in zip(arrows, head_points)])
        slot = row.copy()
        scene.play(
            *[Transform(a, m) for a, m in zip(arrows, moved)],
            row.animate.set_opacity(0.15),
            run_time=run * 0.55,
        )
        row.set_opacity(0)
        headers[letter] = arrows
        seat_boxes = VGroup(*[
            RoundedRectangle(width=PITCH * 0.88, height=PITCH * 0.88, corner_radius=0.06,
                             stroke_color=cfg.BLOCK_COLORS[letter], stroke_width=3,
                             fill_color=cfg.PANEL, fill_opacity=0.9).move_to(p + DOWN * PITCH * 0.95)
            for p in head_points
        ])
        column_groups = [VGroup(*[tiles[z] for z in sorted(columns[letter][k], key=lambda z: -tiles[z].get_center()[1])])
                         for k in seats]
        scene.play(FadeIn(seat_boxes, shift=DOWN * 0.1), run_time=0.3)
        scene.play(*[ReplacementTransform(box, group) for box, group in zip(seat_boxes, column_groups)],
                   run_time=run * 0.7, rate_func=rate_functions.ease_out_cubic)
        blocks[letter] = VGroup(*column_groups)
        # The count takes the place the row just left in the staging line.
        width_label = txt(str(len(seats)), cfg.FONT["section"], cfg.BLOCK_COLORS[letter])
        width_label.move_to(slot)
        scene.remove(row)
        widths[letter] = width_label
        if letter == "s":
            beat(scene, t, 13)
        scene.play(FadeIn(width_label, shift=UP * 0.1), run_time=0.5)

    # --- Slide them together ------------------------------------------------
    beat(scene, t, 16)
    scene.play(FadeOut(VGroup(*headers.values())), FadeOut(VGroup(*widths.values())), run_time=0.6)
    scene.play(
        *[blocks[f].animate.shift(-EXPLODE[f]) for f in FAMILIES],
        run_time=1.8, rate_func=rate_functions.ease_in_out_cubic,
    )
    scene.play(tiles[2].animate.move_to(table_point(2, pitch=PITCH, center=CENTER)).set_stroke(width=None),
               run_time=1.0, path_arc=-PI / 4)

    beat(scene, t, 17)
    head = swap_heading(scene, head, "Capacity sets the width")
    labels = VGroup()
    for letter, capacity in zip(FAMILIES, (2, 6, 10, 14)):
        block = VGroup(*[tiles[z] for z in pm.elements_in_block(letter) if z != 2])
        tag = txt(str(capacity), cfg.FONT["hero"], cfg.BLOCK_COLORS[letter])
        pill = RoundedRectangle(width=tag.width + 0.5, height=tag.height + 0.3, corner_radius=0.22,
                                stroke_color=cfg.BLOCK_COLORS[letter], stroke_width=3,
                                fill_color=cfg.BG, fill_opacity=0.9)
        labels.add(VGroup(pill, tag.move_to(pill)).move_to(block))
    hidden = [label for pill in labels for label in covered_labels(pill, tiles.values())]
    scene.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in labels], lag_ratio=0.25),
               *[m.animate.set_opacity(0) for m in hidden], run_time=1.8)

    beat(scene, t, 18)
    verdict = caption("1 · 3 · 5 · 7 orbitals × 2", cfg.GOLD, cfg.FONT["small"], y=-4.1)
    hud(scene, verdict)
    scene.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.8)
    move_camera(scene, zoom=1.05, run_time=4.0)
    scene.play(LaggedStart(*[Indicate(m, color=cfg.WHITE, scale_factor=1.1) for m in labels], lag_ratio=0.2),
               run_time=2.0)
    move_camera(scene, zoom=1.0, run_time=3.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
