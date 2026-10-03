"""The four blocks appear, rise as a 3D skyline, and wear the orbital that built them.

Each block's height is proportional to its capacity (2, 6, 10, 14), so the
skyline is the same fact as the widths, seen from a new angle.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = DOWN * 0.45
CAPACITY = {"s": 2, "p": 6, "d": 10, "f": 14}
HEIGHT_PER_ELECTRON = 0.055
SHAPE_SIZE = {"s": 0.6, "p": 0.85, "d": 0.95, "f": 1.0}
SKYLINE_LIFT = UP * 0.85


class Scene12FourBlocks(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _pill(number: int, color: str, where: Mobject) -> VGroup:
    label = txt(str(number), cfg.FONT["title"], color)
    pill = RoundedRectangle(width=label.width + 0.5, height=label.height + 0.3, corner_radius=0.22,
                            stroke_color=color, stroke_width=3, fill_color=cfg.BG, fill_opacity=0.9)
    return VGroup(pill, label.move_to(pill)).move_to(where)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "12", "Four blocks")
    table = periodic_table(pitch=PITCH, center=CENTER, style="plain")
    scene.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in table], lag_ratio=0.008), run_time=1.8)

    pills = {}
    for index, letter in enumerate(("s", "p", "d", "f")):
        beat(scene, t, 1 + index)
        block = VGroup(*[table.tiles[z] for z in pm.elements_in_block(letter) if z != 2])
        colour = cfg.BLOCK_COLORS[letter]
        scene.play(*recolor_tiles(block, lambda _z, c=colour: c), run_time=1.0)
        pills[letter] = _pill(pm.block_width(letter), colour, block)
        hidden = covered_labels(pills[letter], table)
        scene.play(FadeIn(pills[letter], scale=1.3), *[m.animate.set_opacity(0) for m in hidden], run_time=0.6)

    beat(scene, t, 5)
    helium = table.tiles[2]
    scene.play(*recolor_tiles([helium], lambda _z: cfg.BLUE), run_time=0.8)
    he_note = txt("1s² · noble gas", cfg.FONT["small"], cfg.BLUE)
    he_note.next_to(helium, LEFT, buff=0.3)
    scene.play(FadeIn(he_note, shift=LEFT * 0.2), Flash(helium, color=cfg.BLUE, flash_radius=0.45), run_time=1.0)
    scene.play(Indicate(helium, color=cfg.BLUE, scale_factor=1.3), run_time=1.0)

    # --- Raise the blocks ---------------------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "Same capacity, seen in 3D")
    scene.play(FadeOut(VGroup(*pills.values())), FadeOut(he_note),
               *[t.symbol.animate.set_opacity(1) for t in table if hasattr(t, "symbol")], run_time=0.5)
    prisms = {}
    for z in range(1, 119):
        prisms[z] = tile_prism(table.tiles[z].get_center(), PITCH * 0.88, 0.06, block_color(z), opacity=0.9)
    skyline = VGroup(*prisms.values())
    scene.add(skyline)
    scene.remove(table, *table.submobjects)
    # Lift the geometry itself so the fixed heading and legend retain their margins.
    move_camera(scene, phi=48 * DEGREES, theta=-84 * DEGREES, zoom=1.0, frame_center=ORIGIN,
                added_anims=[skyline.animate.shift(SKYLINE_LIFT)], run_time=1.7)
    grow = []
    for z, prism in prisms.items():
        height = CAPACITY[pm.block(z)] * HEIGHT_PER_ELECTRON
        grow.append(prism.animate.stretch(height / 0.06, 2, about_edge=IN))
    scene.play(LaggedStart(*grow, lag_ratio=0.004), run_time=1.6)

    # --- The orbital over each block -------------------------------------------------
    beat(scene, t, 7)
    scene.begin_ambient_camera_rotation(rate=0.01)
    shapes = {}
    for letter in ("s", "p", "d", "f"):
        block = VGroup(*[prisms[z] for z in pm.elements_in_block(letter) if z != 2])
        top = CAPACITY[letter] * HEIGHT_PER_ELECTRON
        l, m = ORBITAL_FAMILY[letter]
        shape = orbital_surface(l, m, SHAPE_SIZE[letter])
        if letter == "p":
            shape.rotate(PI / 2, axis=UP)  # lie along x, so the full dumbbell faces the camera
        if letter == "d":
            shape.rotate(55 * DEGREES, axis=RIGHT)  # tip the clover's plane toward the camera
        shape.move_to(np.array([block.get_center()[0], block.get_center()[1], top + SHAPE_SIZE[letter] + 0.3]))
        spin_forever(shape, 0.4, axis=OUT)
        shapes[letter] = shape
    for index, letter in enumerate(("s", "p", "d", "f")):
        beat(scene, t, 8 + index)
        scene.play(FadeIn(shapes[letter], shift=IN * 0.6, scale=0.5), run_time=1.4)

    beat(scene, t, 12)
    legend = VGroup(*[
        VGroup(eq(letter, cfg.FONT["label"], cfg.BLOCK_COLORS[letter]),
               eq(rf"{2 * pm.L_LETTERS.index(letter) + 1}\times 2 = {CAPACITY[letter]}", cfg.FONT["small"], cfg.WHITE))
        .arrange(RIGHT, buff=0.2)
        for letter in ("s", "p", "d", "f")
    ]).arrange(RIGHT, buff=0.75).move_to(DOWN * 3.75)
    fit_width(legend, 14.4)
    backing = RoundedRectangle(width=legend.width + 0.6, height=legend.height + 0.35, corner_radius=0.2,
                               stroke_color=cfg.MUTED, stroke_width=1.5, fill_color=cfg.BG, fill_opacity=0.85)
    backing.move_to(legend)
    hud(scene, backing, legend)
    scene.play(FadeIn(backing), LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in legend], lag_ratio=0.25), run_time=1.6)

    # --- Back to the flat table: every feature explained ---------------------------------
    beat(scene, t, 13)
    scene.stop_ambient_camera_rotation()
    for shape in shapes.values():
        shape.clear_updaters()
    scene.play(*[FadeOut(s, scale=0.4) for s in shapes.values()], FadeOut(VGroup(backing, legend)), run_time=0.8)
    flat = []
    for z, prism in prisms.items():
        flat.append(prism.animate.stretch(0.06 / prism.depth, 2, about_edge=IN).shift(-SKYLINE_LIFT))
    scene.play(*flat, run_time=1.0)
    move_camera(scene, phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN, run_time=1.8)
    final = periodic_table(pitch=PITCH, center=CENTER)
    final.tiles[2].box.set_stroke(cfg.BLUE)
    scene.play(FadeIn(final), FadeOut(skyline), run_time=0.6)
    features = [
        glow_frame(VGroup(*[final.tiles[z] for z in pm.elements_in_block("d")]), cfg.GOLD, buff=0.06),
        glow_frame(VGroup(final.tiles[4], final.tiles[5], final.tiles[12], final.tiles[13]), cfg.GOLD, buff=0.06),
        glow_frame(VGroup(*[final.tiles[z] for z in pm.elements_in_block("f")]), cfg.GOLD, buff=0.06),
    ]
    gap_box = DashedVMobject(Rectangle(
        width=grid_point(3, 12, pitch=PITCH, center=CENTER)[0] - grid_point(2, 3, pitch=PITCH, center=CENTER)[0] + PITCH * 0.9,
        height=PITCH * 1.9, stroke_color=cfg.GOLD, stroke_width=3), num_dashes=50)
    gap_box.move_to((grid_point(2, 3, pitch=PITCH, center=CENTER) + grid_point(3, 12, pitch=PITCH, center=CENTER)) / 2)
    features[1] = gap_box
    for feature in features:
        scene.play(Create(feature), run_time=0.9)
        scene.play(FadeOut(feature), run_time=0.4)

    beat(scene, t, 14)
    question = caption("Why does it repeat?", cfg.GOLD, cfg.FONT["label"], y=-4.05)
    hud(scene, question)
    scene.play(FadeIn(question, shift=UP * 0.2), run_time=0.8)
    rows = [VGroup(*[final.tiles[z] for z in pm.period_members(p) if pm.position(z)[0] <= 7]) for p in (2, 3, 4)]
    scene.play(LaggedStart(*[Indicate(r, color=cfg.CYAN, scale_factor=1.05) for r in rows], lag_ratio=0.4), run_time=2.2)
    scene.play(Indicate(question, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
