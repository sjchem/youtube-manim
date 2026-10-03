"""Protons decide the element and give the order — but not the shape.

The chapter ends by trying the obvious idea, wrapping the line of 118 elements
every 18 tiles, and letting the real outline show that order alone cannot
produce the table.
"""

from manim_scenes.common import *

NUCLEUS_AT = np.array([-3.7, -0.15, 0])
TILE_AT = np.array([3.8, -0.15, 0])
DISPLAY_RADIUS = {1: 0.42, 2: 0.34, 6: 0.25, 79: 0.122}


class Scene02AtomicNumber(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def _nucleus(z: int) -> VGroup:
    core = nucleus(z, radius=DISPLAY_RADIUS[z]).move_to(NUCLEUS_AT)
    glow = halo(max(core.width, core.height) * 0.9, cfg.NUCLEUS_COLOR, peak_opacity=0.12).move_to(NUCLEUS_AT)
    return VGroup(glow, core)


def _count_label(z: int) -> Text:
    return txt(f"{z} proton{'s' if z > 1 else ''}", cfg.FONT["label"], cfg.PROTON_COLOR).move_to(
        NUCLEUS_AT + DOWN * 2.75)


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "02", "What makes an element?")

    # --- Hydrogen ----------------------------------------------------------
    current = _nucleus(1)
    scene.play(FadeIn(current[0], scale=0.4), run_time=1.2)
    beat(scene, t, 1)
    scene.play(GrowFromCenter(current[1]), run_time=0.8)
    label = _count_label(1)
    tile = big_tile(1, 2.8).move_to(TILE_AT)
    link = Arrow(NUCLEUS_AT + RIGHT * 1.95, tile.get_left() + LEFT * 0.65,
                 buff=0, color=cfg.MUTED, stroke_width=5)
    scene.play(FadeIn(label, shift=UP * 0.2), GrowArrow(link), FadeIn(tile, shift=LEFT * 0.4), run_time=1.0)

    # --- One more proton at a time -----------------------------------------
    for index, z in ((2, 2), (3, 6), (4, 79)):
        beat(scene, t, index)
        incoming = VGroup(*[nucleon(cfg.PROTON_COLOR, DISPLAY_RADIUS[z]).move_to(NUCLEUS_AT + LEFT * 3.2 + UP * (0.6 * k - 0.3))
                            for k in range(min(z - (1 if z == 2 else 0), 3) if z < 79 else 3)])
        scene.play(FadeIn(incoming, shift=RIGHT * 0.6), run_time=0.5)
        new_nucleus = _nucleus(z)
        new_tile = big_tile(z, 2.8).move_to(TILE_AT)
        scene.play(
            incoming.animate.move_to(NUCLEUS_AT).set_opacity(0),
            ReplacementTransform(current, new_nucleus),
            run_time=1.1 if z < 79 else 1.6,
        )
        scene.remove(incoming)
        current = new_nucleus
        scene.play(ReplacementTransform(label, new_label := _count_label(z)),
                   FadeOut(tile, shift=UP * 0.3), FadeIn(new_tile, shift=UP * 0.3),
                   Flash(NUCLEUS_AT, color=cfg.GOLD, line_length=0.4, flash_radius=current.width / 2 + 0.2),
                   run_time=0.9)
        label, tile = new_label, new_tile

    # --- Z = number of protons ---------------------------------------------
    beat(scene, t, 5)
    law = eq(r"Z", cfg.FONT["title"], cfg.GOLD)
    rest = VGroup(eq("=", cfg.FONT["body"]), txt("number of protons", cfg.FONT["body"]))
    rest.arrange(RIGHT, buff=0.25)
    formula = VGroup(law, rest).arrange(RIGHT, buff=0.25).move_to(DOWN * 3.1)
    scene.play(ReplacementTransform(label, formula), run_time=1.0)
    scene.play(Circumscribe(tile.number, color=cfg.GOLD, buff=0.08), Indicate(law, color=cfg.GOLD), run_time=1.4)

    # --- A single line of 118 ----------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "One proton at a time")
    pitch = 1.08
    line = VGroup(*[element_tile(z, 0.94, cfg.CYAN, number=True) for z in range(1, 119)])
    for index, tile_mob in enumerate(line):
        tile_mob.move_to(np.array([-6.5 + index * pitch, 0.25, 0]))
    scene.play(FadeOut(current), FadeOut(link), FadeOut(formula),
               ReplacementTransform(tile, line[78].copy().set_opacity(0)), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.5) for m in line[:13]], lag_ratio=0.12), run_time=2.4)
    # The rest of the line joins the scene only as it slides into view.
    counter = number(13, cfg.FONT["section"]).move_to(DOWN * 2.4)
    unit = txt("elements", cfg.FONT["label"], cfg.MUTED).next_to(counter, RIGHT, buff=0.3)
    unit.add_updater(lambda m: m.next_to(counter, RIGHT, buff=0.3))
    scene.play(FadeIn(counter), FadeIn(unit), run_time=0.6)

    beat(scene, t, 7)
    scene.play(line.animate.scale(14.0 / line.width).move_to(UP * 0.25),
               ChangeDecimalToValue(counter, 118), run_time=4.5, rate_func=smooth)
    ends = VGroup(
        txt("H", cfg.FONT["small"], cfg.CYAN).next_to(line, UP, buff=0.3).align_to(line, LEFT),
        txt("Og", cfg.FONT["small"], cfg.CYAN).next_to(line, UP, buff=0.3).align_to(line, RIGHT),
    )
    scene.play(FadeIn(ends), run_time=0.6)

    # --- Order, yes. Shape, no. --------------------------------------------
    beat(scene, t, 8)
    order_chip = chip("ORDER  ✓", cfg.GREEN, cfg.FONT["label"]).move_to(DOWN * 1.35)
    unit.clear_updaters()
    scene.play(FadeOut(counter), FadeOut(unit), FadeIn(order_chip, scale=1.2), run_time=0.8)
    scene.play(Indicate(line, color=cfg.GREEN, scale_factor=1.02), run_time=1.4)

    beat(scene, t, 9)
    head = swap_heading(scene, head, "Order is only the beginning")
    naive_pitch = 0.6
    naive_center = DOWN * 0.55
    # The naive idea: same grid as the real table, filled 18 to a row.
    targets = [grid_point(index // 18 + 1, index % 18 + 1, pitch=naive_pitch, center=naive_center)
               for index in range(118)]
    scene.play(FadeOut(ends), FadeOut(order_chip),
               *[m.animate.scale_to_fit_width(naive_pitch * 0.88).move_to(p) for m, p in zip(line, targets)],
               run_time=2.0)
    truth = periodic_table(pitch=naive_pitch, center=naive_center, style="silhouette")
    outline = VGroup(*[tile_mob.box.copy().set_fill(opacity=0).set_stroke(cfg.GOLD, 2.5, 0.85) for tile_mob in truth])
    scene.play(LaggedStart(*[Create(o) for o in outline], lag_ratio=0.004), run_time=1.6)
    wrong = [m for z, m in zip(range(1, 119), line)
             if not np.allclose(m.get_center(), truth.tiles[z].get_center(), atol=0.05)]
    scene.play(*[m.box.animate.set_stroke(cfg.ORANGE).set_fill(interpolate_color(ManimColor(cfg.PANEL), ManimColor(cfg.ORANGE), 0.25))
                 for m in wrong], run_time=1.0)
    shape_chip = chip("SHAPE  ?", cfg.ORANGE, cfg.FONT["label"]).move_to(DOWN * 3.85)
    scene.play(FadeIn(shape_chip, scale=1.2), run_time=0.6)
    scene.play(FadeOut(line), FadeOut(outline), run_time=1.0)
    electron = glow_dot(ORIGIN + UP * 0.2, 0.32)
    tag = eq(r"e^-", cfg.FONT["section"], cfg.ELECTRON_COLOR).next_to(electron, DOWN, buff=0.35)
    scene.play(FadeIn(electron, scale=0.3), FadeIn(tag), run_time=1.0)
    scene.play(electron.animate.scale(1.25), rate_func=there_and_back, run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
