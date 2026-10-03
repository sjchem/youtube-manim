"""Hook: the familiar silhouette, its four strange widths, and the title.

The tiles fall into place in atomic-number order — a quiet foreshadowing of
the whole film, which rebuilds the table one electron at a time.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = ORIGIN + DOWN * 0.05


class Scene01Hook(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _count_columns(table: VGroup, letter: str, color: str) -> tuple[list[Animation], VGroup]:
    """Light a block column by column, so its width is counted, not asserted."""
    zs = [z for z in pm.elements_in_block(letter) if z != 2]
    columns: dict[int, list[int]] = {}
    for z in zs:
        columns.setdefault(pm.position(z)[1], []).append(z)
    waves = []
    for col in sorted(columns):
        group = tiles_of(table, columns[col])
        waves.append(AnimationGroup(*recolor_tiles(group, lambda _z: color)))
    return waves, tiles_of(table, zs)


def _number_on(block: VGroup, number: int, color: str) -> VGroup:
    """A big number on a dark pill, centred over a block."""
    label = txt(str(number), cfg.FONT["hero"], color)
    pill = RoundedRectangle(width=label.width + 0.55, height=label.height + 0.35, corner_radius=0.25,
                            stroke_color=color, stroke_width=3, fill_color=cfg.BG, fill_opacity=0.88)
    return VGroup(pill, label.move_to(pill)).move_to(block)


def play_scene(scene: ThreeDScene) -> None:
    t, _ = start(scene, "01")

    # --- 1. Tiles rain into place in 3D, in atomic-number order -------------
    scene.set_camera_orientation(phi=58 * DEGREES, theta=-90 * DEGREES, zoom=0.92)
    prisms = VGroup(*[
        tile_prism(table_point(z, pitch=PITCH, center=CENTER), PITCH * 0.88, 0.16,
                   interpolate_color(ManimColor(cfg.CYAN), ManimColor(cfg.PANEL), 0.35))
        for z in range(1, 119)
    ])
    scene.play(LaggedStart(*[FadeIn(p, shift=IN * 2.6) for p in prisms], lag_ratio=0.03), run_time=3.6)
    move_camera(scene, phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=1.8)

    table = periodic_table(pitch=PITCH, center=CENTER, style="silhouette")
    scene.play(FadeOut(prisms), FadeIn(table), run_time=0.5)

    beat(scene, t, 1)
    wave = LaggedStart(*[
        Indicate(tiles_of(table, [z for z in range(1, 119) if pm.position(z)[1] == col]),
                 color=cfg.CYAN, scale_factor=1.06)
        for col in range(1, 19)
    ], lag_ratio=0.12)
    scene.play(wave, run_time=3.0)

    # --- 2. Count the four widths ------------------------------------------
    numbers = {}
    for index, (letter, width) in enumerate((("s", 2), ("d", 10), ("p", 6), ("f", 14))):
        beat(scene, t, 2 + index)
        colour = cfg.BLOCK_COLORS[letter]
        waves, block = _count_columns(table, letter, colour)
        scene.play(LaggedStart(*waves, lag_ratio=0.35), run_time=1.6 if width < 10 else 2.2)
        numbers[letter] = _number_on(block, width, colour)
        stretched = block.copy()
        scene.play(FadeIn(numbers[letter], scale=1.3),
                   block.animate.stretch(1.08, 0), run_time=0.6)
        scene.play(block.animate.stretch(1 / 1.08, 0), run_time=0.4)
        del stretched

    # --- 3. Why? Two families glow -----------------------------------------
    beat(scene, t, 6)
    marks = VGroup(*[txt("?", 96, cfg.GOLD) for _ in range(3)])
    marks[0].move_to(grid_point(2, 7, pitch=PITCH, center=CENTER) + DOWN * 0.15)
    marks[1].move_to(grid_point(2, 9, pitch=PITCH, center=CENTER) + UP * 0.35)
    marks[2].move_to(grid_point(2, 11, pitch=PITCH, center=CENTER) + DOWN * 0.05)
    scene.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in marks], lag_ratio=0.25), run_time=1.2)
    families = VGroup(
        glow_frame(tiles_of(table, pm.group_members(1)[1:]), cfg.GOLD, buff=0.06),
        glow_frame(tiles_of(table, pm.group_members(18)), cfg.GOLD, buff=0.06),
    )
    scene.play(Create(families), run_time=1.4)
    scene.play(*[Indicate(tiles_of(table, pm.group_members(c)[1:]), color=cfg.GOLD, scale_factor=1.05)
                 for c in (1, 18)], run_time=1.4)

    # --- 4. 2, 6, 10, 14 become s, p, d, f ---------------------------------
    beat(scene, t, 7)
    order = ("s", "p", "d", "f")
    slots = [LEFT * 4.5 + RIGHT * 3.0 * i for i in range(4)]
    scene.play(
        table.animate.set_opacity(0.18), FadeOut(marks), FadeOut(families),
        *[numbers[letter].animate.move_to(slots[i] + UP * 0.6) for i, letter in enumerate(order)],
        run_time=1.4,
    )
    letters = VGroup(*[
        eq(letter, 104, cfg.BLOCK_COLORS[letter]).move_to(slots[i] + DOWN * 1.15)
        for i, letter in enumerate(order)
    ])
    arrows = VGroup(*[
        Arrow(slots[i] + UP * 0.05, slots[i] + DOWN * 0.55, buff=0, color=cfg.MUTED, stroke_width=5)
        for i in range(4)
    ])
    scene.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=0.8)
    scene.play(LaggedStart(*[
        TransformFromCopy(numbers[letter][1], letters[i]) for i, letter in enumerate(order)
    ], lag_ratio=0.2), run_time=1.8)

    # --- 5. Title ----------------------------------------------------------
    beat(scene, t, 8)
    line_one = Text("THE PERIODIC TABLE", font=cfg.TITLE_FONT, weight=BOLD, font_size=66, color=cfg.GOLD)
    line_two = Text("WHY THIS SHAPE?", font=cfg.TITLE_FONT, weight=BOLD, font_size=88, color=cfg.GOLD)
    title = VGroup(line_one, line_two).arrange(DOWN, buff=0.22)
    fit_width(title, 13.4)
    title.move_to(UP * 1.75)
    title.set_stroke("#351F05", width=3, opacity=0.8, background=True)
    shadow = title.copy().set_color(cfg.BG).set_opacity(0.9).shift(RIGHT * 0.08 + DOWN * 0.08)
    shadow.set_stroke(width=0)
    decorative(shadow)
    rule = Line(LEFT * 5.6, RIGHT * 5.6, stroke_color=cfg.CYAN, stroke_width=3).next_to(title, DOWN, buff=0.3)
    part = txt(cfg.PROJECT_PART, cfg.FONT["small"], cfg.CYAN).next_to(rule, DOWN, buff=0.28)
    scene.play(
        FadeOut(VGroup(*numbers.values())), FadeOut(arrows),
        letters.animate.arrange(RIGHT, buff=1.2).move_to(DOWN * 2.35),
        table.animate.set_opacity(0.08),
        run_time=1.0,
    )
    scene.play(FadeIn(shadow, title, shift=DOWN * 0.15), Create(rule), run_time=1.2)
    scene.play(FadeIn(part, shift=UP * 0.1), run_time=0.6)
    scene.play(LaggedStart(*[Indicate(letter, color=cfg.WHITE, scale_factor=1.12) for letter in letters],
                           lag_ratio=0.25), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
