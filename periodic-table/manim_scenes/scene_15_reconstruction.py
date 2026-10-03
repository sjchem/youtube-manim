"""The final reconstruction: table -> blocks -> orbitals -> four numbers, and back.

The reverse transformation strips the finished table down to 2, 6, 10, 14;
the forward one rebuilds it, and the film closes on a 3D skyline of the table
under its one-sentence answer.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = DOWN * 0.45
ROW_Y = {"s": 2.0, "p": 0.75, "d": -0.5, "f": -1.75}
ROW_X = -0.3
SHAPE_X = -4.6
NUMBER_X = 4.3


class Scene15Reconstruction(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _block_columns(table: VGroup, letter: str) -> list[VGroup]:
    zs = [z for z in pm.elements_in_block(letter) if z != 2]
    columns: dict[int, list[int]] = {}
    for z in zs:
        columns.setdefault(pm.position(z)[1], []).append(z)
    return [VGroup(*[table.tiles[z] for z in columns[c]]) for c in sorted(columns)]


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "15", "So: why this shape?")
    table = periodic_table(pitch=PITCH, center=CENTER)
    table.tiles[2].box.set_stroke(cfg.BLUE)
    scene.play(FadeIn(table, scale=0.96), run_time=1.4)
    scene.play(Indicate(table, color=cfg.WHITE, scale_factor=1.02), run_time=1.4)

    # --- Strip it back -----------------------------------------------------------
    beat(scene, t, 1)
    head = swap_heading(scene, head, "Strip it back")
    bars = {}
    animations = []
    for letter in "spdf":
        bars[letter] = []
        for column in _block_columns(table, letter):
            bar = RoundedRectangle(width=column.width, height=column.height, corner_radius=0.08,
                                   stroke_color=cfg.BLOCK_COLORS[letter], stroke_width=3,
                                   fill_color=cfg.BLOCK_COLORS[letter], fill_opacity=0.35).move_to(column)
            bars[letter].append(bar)
            animations.append(ReplacementTransform(column, bar))
    helium = table.tiles[2]
    scene.play(*animations, FadeOut(helium), run_time=1.6)

    beat(scene, t, 2)
    rows = {}
    for letter in "spdf":
        l = pm.L_LETTERS.index(letter)
        row = orbital_row(l, None, box=0.72, gap=0.14).move_to([ROW_X, ROW_Y[letter], 0])
        rows[letter] = row
    scene.play(*[ReplacementTransform(VGroup(*bars[letter]), rows[letter].boxes) for letter in "spdf"], run_time=1.4)

    beat(scene, t, 3)
    shapes = {}
    for letter in "spdf":
        shape = present_3d(family_orbital(letter, 0.5 if letter != "s" else 0.42, small=True)).move_to([SHAPE_X, ROW_Y[letter], 0])
        spin_forever(shape, 0.4)
        shapes[letter] = shape
    letters = VGroup(*[eq(letter, cfg.FONT["section"], cfg.BLOCK_COLORS[letter]).move_to([SHAPE_X - 1.2, ROW_Y[letter], 0])
                       for letter in "spdf"])
    scene.play(*[FadeIn(s, scale=0.5) for s in shapes.values()], FadeIn(letters), run_time=1.2)

    beat(scene, t, 4)
    numbers = VGroup(*[eq(str(pm.block_width(letter)), cfg.FONT["title"], cfg.GOLD).move_to([NUMBER_X, ROW_Y[letter], 0])
                       for letter in "spdf"])
    scene.play(LaggedStart(*[FadeIn(n, scale=1.4) for n in numbers], lag_ratio=0.25), run_time=1.6)
    scene.play(Circumscribe(numbers, color=cfg.GOLD), run_time=1.2)

    # --- Run it forward ------------------------------------------------------------
    beat(scene, t, 5)
    head = swap_heading(scene, head, "Now run it forward")
    arrows = {letter: VGroup(*row_arrows(rows[letter], pm.block_width(letter))) for letter in "spdf"}
    scene.play(LaggedStart(*[LaggedStart(*[drop_in(a, 0.3) for a in arrows[letter]], lag_ratio=0.1) for letter in "spdf"],
                           lag_ratio=0.25), run_time=2.6)
    configs = VGroup(*[eq(pm.config_latex(z, core=True), cfg.FONT["small"], cfg.WHITE) for z in (11, 26, 35)])
    configs.arrange(DOWN, buff=0.25).move_to([NUMBER_X + 0.4, 0.1, 0])
    scene.play(FadeOut(numbers), LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in configs], lag_ratio=0.3), run_time=1.4)
    rebuilt = periodic_table(pitch=PITCH, center=CENTER)
    rebuilt.tiles[2].box.set_stroke(cfg.BLUE)
    for shape in shapes.values():
        shape.clear_updaters()
    scene.play(FadeOut(VGroup(*shapes.values())), FadeOut(letters), FadeOut(configs), run_time=0.6)
    scene.play(*[ReplacementTransform(VGroup(rows[letter].boxes, arrows[letter]),
                                      VGroup(*[rebuilt.tiles[z] for z in pm.elements_in_block(letter) if z != 2]))
                 for letter in "spdf"], FadeIn(rebuilt.tiles[2]), run_time=2.2)

    # --- Begin with electrons ---------------------------------------------------------
    beat(scene, t, 6)
    line_one = caption("Begin with the electrons.", cfg.WHITE, cfg.FONT["small"], y=-4.1)
    hud(scene, line_one)
    scene.play(FadeIn(line_one, shift=UP * 0.15), run_time=0.8)

    beat(scene, t, 7)
    line_two = caption("The pattern builds the table.", cfg.GOLD, cfg.FONT["small"], y=-4.1)
    hud(scene, line_two)
    scene.play(FadeOut(line_one, shift=UP * 0.15), FadeIn(line_two, shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(rebuilt, color=cfg.GOLD, scale_factor=1.02), run_time=1.6)

    beat(scene, t, 8)
    head = swap_heading(scene, head, "Elements · groups · blocks")
    fe = rebuilt.tiles[26]
    step = glow_frame(fe, cfg.WHITE, buff=0.06)
    column = glow_frame(VGroup(*[rebuilt.tiles[z] for z in pm.group_members(1)]), cfg.BLUE, buff=0.05)
    d_block = glow_frame(VGroup(*[rebuilt.tiles[z] for z in pm.elements_in_block("d")]), cfg.GOLD, buff=0.06)
    notes = VGroup(txt("element: atomic number", cfg.FONT["tiny"], cfg.WHITE),
                   txt("group: repeating pattern", cfg.FONT["tiny"], cfg.BLUE),
                   txt("block: subshell family", cfg.FONT["tiny"], cfg.GOLD)).arrange(DOWN, buff=0.2)
    fit_width(notes, 5.2)
    notes.move_to(grid_point(2, 7.5, pitch=PITCH, center=CENTER) + UP * 0.05)
    scene.play(FadeOut(line_two), Create(step), FadeIn(notes[0]), run_time=0.9)
    scene.play(Create(column), FadeIn(notes[1]), run_time=0.9)
    scene.play(Create(d_block), FadeIn(notes[2]), run_time=0.9)

    # --- The answer, over a 3D skyline ------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(step, column, d_block, notes)), FadeOut(head), run_time=0.6)
    prisms = VGroup(*[tile_prism(rebuilt.tiles[z].get_center(), PITCH * 0.88, 0.06 + 0.05 * pm.block_width(pm.block(z)),
                                 block_color(z), opacity=0.9) for z in range(1, 119)])
    answer = VGroup(txt("A map of atoms", cfg.FONT["title"], cfg.GOLD),
                    txt("written in quantum states.", cfg.FONT["title"], cfg.GOLD)).arrange(DOWN, buff=0.15)
    fit_width(answer, 13.6)
    answer.move_to(UP * 3.2)
    shadow = answer.copy().set_color(cfg.BG).set_opacity(0.85).shift(RIGHT * 0.05 + DOWN * 0.05)
    decorative(shadow)
    chain = VGroup(*[chip(word, colour, cfg.FONT["tiny"]) for word, colour in (
        ("orbitals", cfg.CYAN), ("configurations", cfg.GOLD),
        ("table", cfg.BLUE), ("chemistry", cfg.GREEN))])
    chain.arrange(RIGHT, buff=0.42)
    fit_width(chain, 14.6)
    chain.move_to(DOWN * 3.95)
    links = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.04, color=cfg.MUTED, stroke_width=3,
                           max_tip_length_to_length_ratio=0.4) for i in range(len(chain) - 1)])
    hud(scene, answer, shadow, chain, links)
    scene.add(prisms)
    scene.remove(rebuilt, *rebuilt.submobjects)
    move_camera(scene, phi=50 * DEGREES, theta=-80 * DEGREES, zoom=0.95, frame_center=DOWN * 0.3, run_time=2.4)
    scene.play(FadeIn(shadow), Write(answer), run_time=2.0)
    scene.begin_ambient_camera_rotation(rate=0.02)
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(c, shift=UP * 0.15), *([GrowArrow(links[i - 1])] if i else []))
                             for i, c in enumerate(chain)], lag_ratio=0.35), run_time=3.2)
    cue(scene, t, cfg.SCENE_DURATIONS["15"] - 2.4)
    scene.stop_ambient_camera_rotation()
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
