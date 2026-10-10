"""The table as a map of chemical tendencies, then period-3 oxides.

Tile colours here are categories, not data: metals blue, metalloids teal,
non-metals green, noble gases muted. The oxide strip uses the standard
textbook classification (Na2O and MgO basic, Al2O3 amphoteric, SiO2 to Cl2O7
acidic); the full oxide chemistry is left for a later episode.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = DOWN * 0.55
METALLOIDS = ("B", "Si", "Ge", "As", "Sb", "Te")
NONMETALS = ("H", "C", "N", "O", "F", "P", "S", "Cl", "Se", "Br", "I")
TEAL = "#5FD3C7"
OXIDES = (("Na", r"\mathrm{Na_2O}"), ("Mg", r"\mathrm{MgO}"), ("Al", r"\mathrm{Al_2O_3}"), ("Si", r"\mathrm{SiO_2}"),
          ("P", r"\mathrm{P_4O_{10}}"), ("S", r"\mathrm{SO_3}"), ("Cl", r"\mathrm{Cl_2O_7}"))


class Scene17BehaviourMap(Scene):
    def construct(self) -> None:
        play_scene(self)


def category(z: int) -> str:
    symbol = pm.symbol_of(z)
    # Avoid assigning definite classes to disputed boundary/superheavy elements.
    if z > 86 or symbol in ("Po", "At"):
        return "unclassified"
    if z in pm.NOBLE_GASES:
        return "noble"
    if symbol in METALLOIDS:
        return "metalloid"
    if symbol in NONMETALS:
        return "nonmetal"
    return "metal"


COLOURS = {"metal": cfg.BLUE, "metalloid": TEAL, "nonmetal": cfg.GREEN, "noble": cfg.MUTED, "unclassified": cfg.NO_DATA}


def badge(sign: str, colour: str, at) -> VGroup:
    disc = Circle(radius=0.2, stroke_color=colour, stroke_width=3, fill_color=cfg.BG, fill_opacity=0.9)
    mark = txt(sign, cfg.FONT["small"], colour)
    return VGroup(disc, mark.move_to(disc)).move_to(at)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "A map of chemical tendencies")
    table = periodic_table(pitch=PITCH, center=CENTER)
    table.tiles[2].box.set_stroke(cfg.BLUE)
    scene.play(FadeIn(table), run_time=1.0)
    scene.play(*recolor_tiles(table.tiles.values(), lambda z: cfg.MUTED, fill=0.12), run_time=0.8)

    # --- 1. Left: metals that give electrons away --------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    left_metals = [z for z in pm.group_members(1) + pm.group_members(2) if z != 1]
    scene.play(*recolor_tiles([table.tiles[z] for z in left_metals], lambda z: cfg.BLUE, fill=0.6), run_time=1.0)
    plus_marks = VGroup(*[badge("+", cfg.CATION, table.tiles[z].get_center() + LEFT * 0.62) for z in (3, 11, 19, 37, 55)])
    scene.play(LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in plus_marks], lag_ratio=0.25), run_time=1.2)
    give = chip('Electron loss → cations', cfg.BLUE, cfg.FONT["small"]).move_to([-2.6, 2.95, 0])
    scene.play(FadeIn(give, shift=DOWN * 0.1), run_time=0.7)

    # --- 2. Metallic character: down and left -----------------------------------------------------------------
    beat(scene, t, 2)
    down_left = glow_arrow(grid_point(2.2, 4.6, pitch=PITCH, center=CENTER), grid_point(6.6, 1.2, pitch=PITCH, center=CENTER),
                           cfg.TREND_ARROW, 7, tip=0.3)
    metallic = txt("metallic character", cfg.FONT["small"], cfg.WHITE).move_to(grid_point(1.3, 7.5, pitch=PITCH, center=CENTER))
    scene.play(GrowArrow(down_left.arrow), FadeIn(down_left[0]), FadeIn(metallic), run_time=1.2)

    # --- 3. Upper right: non-metals that pull electrons in ---------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(down_left, metallic, plus_marks)), run_time=0.5)
    pullers = [pm.z_of(s) for s in ("N", "O", "F", "S", "Cl", "Se", "Br", "I")]
    scene.play(*recolor_tiles([table.tiles[z] for z in pullers], lambda z: cfg.GREEN, fill=0.6), run_time=1.0)
    minus_marks = VGroup(*[badge("−", cfg.ANION, table.tiles[pm.z_of(s)].get_center() + UP * PITCH) for s in ("F",)])
    scene.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in minus_marks], lag_ratio=0.25), run_time=1.2)
    take = chip('Halogens → anions', cfg.GREEN, cfg.FONT["small"]).move_to([2.7, 2.95, 0])
    scene.play(FadeOut(give), FadeIn(take, shift=DOWN * 0.1), run_time=0.7)
    scene.play(*[Indicate(table.tiles[pm.z_of(s)], color=cfg.WHITE, scale_factor=1.2) for s in ("F", "Cl", "Br", "I")],
               run_time=1.0)

    # --- 4. Far right: noble gases ------------------------------------------------------------------------------------
    beat(scene, t, 4)
    nobles = [table.tiles[z] for z in pm.group_members(18) if z <= 86]
    rings = VGroup(*[glow_frame(tile, cfg.WHITE, buff=0.03, width=3) for tile in nobles])
    quiet = chip('Noble gases: usually unreactive', cfg.MUTED, cfg.FONT["small"]).move_to([2.7, 2.95, 0])
    scene.play(FadeOut(minus_marks), *fade_labels(take, quiet), Create(rings), run_time=1.2)

    # --- 5. Metal fades into non-metal across each period --------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(rings), FadeOut(quiet), run_time=0.4)
    scene.play(*recolor_tiles(table.tiles.values(), lambda z: COLOURS[category(z)], fill=0.55), run_time=1.6)
    key = VGroup(*[VGroup(Square(0.3, stroke_width=0, fill_color=COLOURS[k], fill_opacity=0.9), txt(name, cfg.FONT["tiny"], COLOURS[k]))
                   .arrange(RIGHT, buff=0.15) for k, name in (("metal", "metals"), ("metalloid", "metalloids"),
                                                               ("nonmetal", "non-metals"))]).arrange(RIGHT, buff=0.5)
    key.move_to([0.6, 2.95, 0])
    scene.play(FadeIn(key), run_time=0.6)

    # --- 6-8. Oxides: basic on the left, acidic on the right -------------------------------------------------------------
    beat(scene, t, 6)
    head = swap_heading(scene, head, "Oxides across period 3")
    scene.play(FadeOut(key), FadeOut(table), run_time=0.8)
    xs = [-5.4 + 1.8 * i for i in range(len(OXIDES))]
    tiles = VGroup(*[element_tile(pm.z_of(sym), 1.1, COLOURS[category(pm.z_of(sym))], fill=0.35).move_to([x, 1.65, 0])
                     for (sym, _), x in zip(OXIDES, xs)])
    formulas = VGroup(*[eq(tex, cfg.FONT["small"], cfg.WHITE).move_to([x, 0.35, 0]) for (_, tex), x in zip(OXIDES, xs)])
    scene.play(LaggedStart(*[FadeIn(tile, shift=DOWN * 0.2) for tile in tiles], lag_ratio=0.1), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in formulas[:2]], lag_ratio=0.2), run_time=0.7)
    basic = eq_chip(r"\mathrm{Na_2O} + \mathrm{H_2O} \rightarrow 2\,\mathrm{NaOH}", cfg.BLUE, cfg.FONT["small"]).move_to([-3.6, -2.0, 0])
    basic_tag = txt("basic", cfg.FONT["label"], cfg.BLUE).next_to(basic, DOWN, buff=0.2)
    scene.play(FadeIn(basic, shift=UP * 0.15), FadeIn(basic_tag), run_time=0.9)

    beat(scene, t, 7)
    scene.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in formulas[2:]], lag_ratio=0.2), run_time=1.0)
    acidic = eq_chip(r"\mathrm{SO_3} + \mathrm{H_2O} \rightarrow \mathrm{H_2SO_4}", cfg.ORANGE, cfg.FONT["small"]).move_to([3.6, -2.0, 0])
    acidic_tag = txt("acidic", cfg.FONT["label"], cfg.ORANGE).next_to(acidic, DOWN, buff=0.2)
    scene.play(FadeIn(acidic, shift=UP * 0.15), FadeIn(acidic_tag), run_time=0.9)

    beat(scene, t, 8)
    bar = VGroup(*[Rectangle(width=12.6 / 30 + 0.01, height=0.3, stroke_width=0,
                             fill_color=interpolate_color(ManimColor(cfg.BLUE), ManimColor(cfg.ORANGE), i / 29), fill_opacity=0.95)
                   for i in range(30)]).arrange(RIGHT, buff=0).move_to([0, -0.45, 0])
    amphoteric = txt("amphoteric", cfg.FONT["tiny"], TEAL).next_to(bar, DOWN, buff=0.12).set_x(xs[2])
    scene.play(FadeIn(bar), FadeIn(amphoteric), run_time=0.9)
    later = txt('Oxides: a future episode', cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.85, 0])
    scene.play(FadeIn(later), run_time=0.6)

    # --- 9. One idea underneath -----------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "One idea underneath")
    scene.play(*fade_labels(VGroup(tiles, formulas, basic, basic_tag, acidic, acidic_tag, bar, amphoteric, later),
                            table), run_time=0.9)
    idea = VGroup(chip('Electron removal', cfg.GOLD, cfg.FONT["small"]),
                  chip('Electron attraction', cfg.GREEN, cfg.FONT["small"])).arrange(RIGHT, buff=0.5).move_to([0, 2.95, 0])
    fit_width(idea, 13.6)
    scene.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.1) for i in idea], lag_ratio=0.4), run_time=1.2)

    # --- 10. Every trend at once ------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(Indicate(table, color=cfg.GOLD, scale_factor=1.02), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["17"])
