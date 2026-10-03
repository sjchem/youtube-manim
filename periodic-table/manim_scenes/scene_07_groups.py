"""One column, one pattern, not a list of look-alikes.

Four families are stacked with their outermost electrons, each stack collapses
into one shell-free pattern, the elements vanish, and the patterns take their
places as column headers over the table — then the elements come back.
"""

from manim_scenes.common import *

FAMILY_COLUMNS = (1, 2, 17, 18)
FAMILY_X = {1: -6.45, 2: -2.75, 17: 0.95, 18: 4.65}
STACK_TOP = 2.55
STACK_STEP = 1.2
TILE = 1.0
PITCH = 0.66
CENTER = DOWN * 0.6


class Scene07Groups(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _members(column: int) -> list[int]:
    """The first few members of a column, skipping H and He (they come later)."""
    count = 5 if column in (1, 2) else 4
    return [z for z in pm.group_members(column) if z > 2][:count]


def _stack(column: int) -> tuple[VGroup, VGroup]:
    tiles, configs = VGroup(), VGroup()
    for index, z in enumerate(_members(column)):
        y = STACK_TOP - index * STACK_STEP
        tile = element_tile(z, TILE, number=True).move_to([FAMILY_X[column], y, 0])
        config = eq(pm.outer_latex(z), cfg.FONT["label"], cfg.WHITE).next_to(tile, RIGHT, buff=0.3)
        tiles.add(tile)
        configs.add(config)
    return tiles, configs


def _pattern(column: int, size: int | None = None) -> MathTex:
    z = _members(column)[0]
    return eq(pm.generic_outer_latex(z), size or cfg.FONT["section"], cfg.GOLD)


def _header(column: int) -> MathTex:
    """Short header for a table column: s1, s2, p1..p6."""
    if column <= 2:
        latex, colour = rf"s^{{{column}}}", cfg.BLOCK_COLORS["s"]
    else:
        latex, colour = rf"p^{{{column - 12}}}", cfg.BLOCK_COLORS["p"]
    return eq(latex, cfg.FONT["small"], colour)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "07", "The pattern repeats")

    stacks = {c: _stack(c) for c in FAMILY_COLUMNS}
    patterns = {c: _pattern(c) for c in FAMILY_COLUMNS}
    tiles1, configs1 = stacks[1]
    scene.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.3) for m in tiles1], lag_ratio=0.25), run_time=2.0)

    beat(scene, t, 1)
    slots = VGroup(*[DashedVMobject(RoundedRectangle(width=1.3, height=0.6, corner_radius=0.1,
                                                     stroke_color=cfg.MUTED, stroke_width=2), num_dashes=24)
                     .move_to(c) for c in configs1])
    scene.play(Create(slots), run_time=1.0)

    beat(scene, t, 2)
    for slot, config in zip(slots, configs1):
        scene.play(ReplacementTransform(slot, config), run_time=0.7)

    beat(scene, t, 3)
    shells = VGroup(*[c[0][0] for c in configs1])
    scene.play(Indicate(shells, color=cfg.CYAN, scale_factor=1.4), run_time=1.0)
    patterns[1].next_to(tiles1, DOWN, buff=0.35).align_to(tiles1, LEFT)
    scene.play(TransformFromCopy(configs1, patterns[1]), run_time=1.2)

    # --- Three more families, faster ----------------------------------------
    for index, column in zip((4, 5, 6), (2, 17, 18)):
        beat(scene, t, index)
        tiles, configs = stacks[column]
        scene.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.3) for m in tiles], lag_ratio=0.15),
                   LaggedStart(*[FadeIn(m, shift=LEFT * 0.2) for m in configs], lag_ratio=0.15), run_time=1.6)
        # Every pattern sits on one baseline, under the tallest (five-element) stacks.
        patterns[column].move_to([0, patterns[1].get_y(), 0]).align_to(tiles, LEFT)
        scene.play(TransformFromCopy(configs, patterns[column]), run_time=1.1)
        if column == 17:
            short = txt("one short of full", cfg.FONT["tiny"], cfg.ORANGE).next_to(patterns[column], DOWN, buff=0.22)
            short.align_to(patterns[column], LEFT)
            scene.play(FadeIn(short), run_time=0.5)
            patterns["short"] = short
        if column == 18:
            full = txt("closed s + p", cfg.FONT["tiny"], cfg.GREEN).next_to(patterns[column], DOWN, buff=0.22)
            full.align_to(patterns[column], LEFT)
            scene.play(FadeIn(full), run_time=0.5)
            patterns["full"] = full

    # --- Elements vanish; patterns remain ----------------------------------
    beat(scene, t, 7)
    everything = VGroup(*[VGroup(*stacks[c]) for c in FAMILY_COLUMNS])
    scene.play(FadeOut(everything, shift=DOWN * 0.2), FadeOut(patterns["short"]), FadeOut(patterns["full"]),
               run_time=1.2)
    keep = VGroup(*[patterns[c] for c in FAMILY_COLUMNS])
    scene.play(keep.animate.arrange(RIGHT, buff=1.0).move_to(ORIGIN).scale(1.25), run_time=1.2)

    beat(scene, t, 8)
    head = swap_heading(scene, head, "Keep only the patterns")
    ghost = periodic_table(pitch=PITCH, center=CENTER, style="silhouette").set_opacity(0.3)
    header_y = grid_point(1, 1, pitch=PITCH, center=CENTER)[1] + PITCH * 0.95
    headers = VGroup(*[_header(c).move_to([grid_point(1, c, pitch=PITCH, center=CENTER)[0], header_y, 0])
                       for c in (1, 2, *range(13, 19))])
    scene.play(FadeIn(ghost), keep.animate.scale(0.8).move_to(DOWN * 0.2), run_time=1.0)
    targets = {1: headers[0], 2: headers[1], 17: headers[6], 18: headers[7]}
    scene.play(*[ReplacementTransform(patterns[c], targets[c]) for c in FAMILY_COLUMNS], run_time=1.4)
    rest = [headers[i] for i in (2, 3, 4, 5)]
    scene.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in rest], lag_ratio=0.2), run_time=1.2)
    prefix = eq(r"ns^{2}\,n", cfg.FONT["tiny"], cfg.MUTED).next_to(headers[2], LEFT, buff=0.25)
    prefix.shift(LEFT * 0.0)

    beat(scene, t, 9)
    sweeps = []
    for column in (1, 2, *range(13, 19)):
        members = tiles_of(ghost, pm.group_members(column))
        sweeps.append(LaggedStart(*[Indicate(m, color=cfg.GOLD, scale_factor=1.25) for m in members], lag_ratio=0.25))
    scene.play(LaggedStart(*sweeps, lag_ratio=0.12), run_time=4.0)

    beat(scene, t, 10)
    head = swap_heading(scene, head, "One column, one pattern")
    columns = VGroup(*[glow_frame(tiles_of(ghost, pm.group_members(c)), cfg.GOLD, buff=0.04, width=3)
                       for c in (1, 18)])
    scene.play(Create(columns), run_time=1.2)
    scene.play(Indicate(VGroup(headers[0], headers[7]), color=cfg.WHITE, scale_factor=1.3), run_time=1.2)

    beat(scene, t, 11)
    consequence = VGroup(
        eq(r"ns^{1}", cfg.FONT["label"], cfg.GOLD),
        eq(r"\Rightarrow", cfg.FONT["label"]),
        txt("1 valence electron", cfg.FONT["small"], cfg.WHITE),
    ).arrange(RIGHT, buff=0.3)
    note = txt("outer electrons", cfg.FONT["tiny"], cfg.MUTED)
    box = VGroup(consequence, note).arrange(DOWN, buff=0.18)
    box.move_to(grid_point(2, 7.5, pitch=PITCH, center=CENTER) + DOWN * 0.15)
    backing = panel(box.width + 0.5, box.height + 0.4, cfg.MUTED, 0.92).move_to(box)
    scene.play(FadeIn(backing), FadeIn(consequence, shift=UP * 0.2), run_time=0.9)
    scene.play(FadeIn(note), run_time=0.6)

    beat(scene, t, 12)
    table = periodic_table(pitch=PITCH, center=CENTER)
    scene.play(FadeOut(VGroup(backing, box, columns)), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(table.tiles[z], scale=0.8) for z in range(1, 119)], lag_ratio=0.01),
               FadeOut(ghost), run_time=2.4)

    beat(scene, t, 13)
    question = caption("Pattern → chemistry", cfg.GOLD, cfg.FONT["small"], y=-4.12)
    hud(scene, question)
    scene.play(FadeIn(question, shift=UP * 0.2), run_time=0.8)
    scene.play(Indicate(tiles_of(table, pm.group_members(1)[1:]), color=cfg.GOLD), run_time=1.4)
    scene.play(Indicate(tiles_of(table, pm.group_members(18)), color=cfg.GREEN), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
