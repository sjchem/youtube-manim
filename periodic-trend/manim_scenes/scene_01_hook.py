"""Hook: one glowing atom shrinks across period 2, then grows down group 1.

Every cloud size is the NCERT atomic radius on one shared screen scale, so
the contradiction is measured, not drawn. A faint dashed ring keeps lithium's
size on screen for comparison. The answer is held back until chapter 04.
"""

from manim_scenes.common import *

PERIOD_2 = ("Li", "Be", "B", "C", "N", "O", "F")
GROUP_1 = ("Li", "Na", "K", "Rb", "Cs")
SCALE = 0.0100              # screen units per picometre, shared by every atom here
ATOM_AT = np.array([0.0, 0.45, 0.0])
INFO_AT = np.array([-5.55, 1.1, 0.0])
STRIP_Y = -3.35
COLUMN_X = 5.65


class Scene01Hook(Scene):
    def construct(self) -> None:
        play_scene(self)


def radius_of(symbol: str, scale: float = SCALE) -> float:
    return ed.ATOMIC_RADII_PM[symbol] * scale


def core_of(symbol: str, scale: float = SCALE) -> float:
    """Schematic size of the inner shells: a bigger share of the atom further down."""
    n = pm.outer_shell(pm.z_of(symbol))
    return radius_of(symbol, scale) * (0.25 + 0.07 * (n - 2))


def info_card(symbol: str) -> VGroup:
    z = pm.z_of(symbol)
    tile = element_tile(z, 1.55, number=True, fill=0.24)
    name = txt(pm.NAMES[symbol], cfg.FONT["small"], cfg.MUTED).next_to(tile, DOWN, buff=0.22)
    return VGroup(tile, name).move_to(INFO_AT)


def step_to(scene: Scene, atom: Atom, card: VGroup, marker: VGroup, tile: VGroup, symbol: str,
            run_time: float) -> VGroup:
    """One element further: new charge, new size, new card, marker slides on."""
    new_card = info_card(symbol)
    scene.play(
        *atom.resize(radius_of(symbol), core_of(symbol)),
        *relabel_nucleus(atom, f"+{pm.z_of(symbol)}"),
        FadeThrough(card, new_card),
        marker.animate.move_to(tile),
        run_time=run_time,
    )
    return new_card


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")

    # --- 1. A lithium atom --------------------------------------------------------
    atom = Atom(radius_of("Li"), ATOM_AT, charge="+3", core=core_of("Li"), count=420, seed=1,
                nucleus_radius=0.32, glow=0.2)
    card = info_card("Li")
    strip = VGroup(*[element_tile(pm.z_of(s), 0.86) for s in PERIOD_2]).arrange(RIGHT, buff=0.12)
    strip.move_to([0, STRIP_Y, 0])
    marker = glow_frame(strip[0], cfg.WHITE, buff=0.07)
    scene.play(FadeIn(atom, scale=0.6), run_time=1.6)
    scene.play(FadeIn(card, shift=RIGHT * 0.3), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(tile, shift=UP * 0.2) for tile in strip], lag_ratio=0.08), Create(marker),
               run_time=1.2)

    # --- 2. Across period 2: it shrinks -----------------------------------------------
    beat(scene, t, 1)
    ghost = DashedVMobject(Circle(radius=radius_of("Li"), stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.7),
                           num_dashes=48).move_to(ATOM_AT)
    scene.play(FadeIn(ghost), run_time=0.4)
    for symbol, tile in zip(PERIOD_2[1:], strip[1:]):
        card = step_to(scene, atom, card, marker, tile, symbol, 1.25)

    beat(scene, t, 2)
    across = glow_arrow(strip.get_corner(UL) + UP * 0.28, strip.get_corner(UR) + UP * 0.28, cfg.GOLD, 6)
    shrink = chip("Across a period: generally shrinks", cfg.GOLD, cfg.FONT["small"]).move_to([0, -1.75, 0])
    scene.play(GrowFromEdge(across, LEFT), FadeIn(shrink, shift=UP * 0.15), run_time=1.0)
    scene.play(Indicate(ghost, color=cfg.WHITE, scale_factor=1.03), run_time=1.2)

    # --- 3. Back to lithium, then down group 1: it grows ---------------------------------
    beat(scene, t, 3)
    column = VGroup(*[element_tile(pm.z_of(s), 0.92) for s in GROUP_1]).arrange(DOWN, buff=0.22)
    column.move_to([COLUMN_X, 0.15, 0])
    li_card = info_card("Li")
    scene.play(*atom.resize(radius_of("Li"), core_of("Li")), *relabel_nucleus(atom, "+3"),
               FadeThrough(card, li_card), FadeOut(VGroup(strip, across, shrink, marker)), run_time=1.1)
    card = li_card
    marker = glow_frame(column[0], cfg.WHITE, buff=0.07)
    scene.play(LaggedStart(*[FadeIn(tile, shift=LEFT * 0.2) for tile in column], lag_ratio=0.1), Create(marker),
               run_time=1.0)
    for symbol, tile in zip(GROUP_1[1:], column[1:]):
        card = step_to(scene, atom, card, marker, tile, symbol, 1.35)

    beat(scene, t, 4)
    down = glow_arrow(column.get_corner(UL) + LEFT * 0.3, column.get_corner(DL) + LEFT * 0.3, cfg.CYAN, 6)
    grow = chip("Down a group: generally grows", cfg.CYAN, cfg.FONT["small"]).move_to([0, -3.75, 0])
    scene.play(GrowFromEdge(down, UP), FadeIn(grow, shift=UP * 0.15), run_time=1.0)
    scene.play(Indicate(ghost, color=cfg.WHITE, scale_factor=1.03), run_time=1.2)

    # --- 4. The contradiction, side by side -------------------------------------------------
    beat(scene, t, 5)
    small_scale = 0.0072
    left_at, right_at = np.array([-3.7, 0.35, 0]), np.array([3.4, 0.35, 0])
    fluorine = Atom(radius_of("F", small_scale), left_at, charge="+9", core=core_of("F", small_scale), count=320,
                    seed=4, nucleus_radius=0.3, glow=0.2)
    scene.play(FadeOut(VGroup(card, column, marker, down, grow, ghost)),
               atom.glide(right_at), run_time=1.0)
    scene.play(*atom.resize(radius_of("Cs", small_scale), core_of("Cs", small_scale)), FadeIn(fluorine, scale=0.5),
               run_time=1.0)
    names = VGroup(txt("fluorine", cfg.FONT["label"], cfg.GREEN).move_to(left_at + DOWN * 2.45),
                   txt("caesium", cfg.FONT["label"], cfg.BLUE).move_to(right_at + DOWN * 2.45))
    more = VGroup(eq(r"Z = 9", cfg.FONT["label"], cfg.WHITE).move_to(left_at + UP * 2.45),
                  eq(r"Z = 55", cfg.FONT["label"], cfg.WHITE).move_to(right_at + UP * 2.45))
    question = txt("?", 150, cfg.GOLD).move_to([0, 0.35, 0])
    scene.play(FadeIn(names, shift=UP * 0.15), FadeIn(more, shift=DOWN * 0.15), run_time=0.9)
    scene.play(FadeIn(question, scale=0.4), run_time=0.8)
    scene.play(Wiggle(question, scale_value=1.15), run_time=1.2)

    # --- 5. Foreshadow: one gives an electron away, one pulls one in ----------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(question), run_time=0.4)
    leaving, out_path = escape_electron(atom.center_point() + np.array([1.2, 1.0, 0]), np.array([7.2, 3.6, 0]))
    scene.play(FadeIn(leaving, scale=0.4), run_time=0.4)
    gives = txt("gives one away", cfg.FONT["small"], cfg.ORANGE).next_to(names[1], DOWN, buff=0.25)
    scene.play(MoveAlongPath(leaving, out_path), FadeIn(gives), run_time=1.8, rate_func=rush_into)
    arriving = glow_dot(np.array([-7.4, 3.4, 0]), 0.12)
    in_path = ArcBetweenPoints(np.array([-7.4, 3.4, 0]), left_at + np.array([0.35, 0.25, 0]), angle=PI / 4)
    pulls = txt("pulls one in", cfg.FONT["small"], cfg.GREEN).next_to(names[0], DOWN, buff=0.25)
    scene.play(FadeIn(arriving, scale=0.4), run_time=0.4)
    scene.play(MoveAlongPath(arriving, in_path), FadeIn(pulls), run_time=2.0, rate_func=rush_from)
    scene.play(FadeOut(arriving, scale=0.3), Indicate(fluorine.nucleus, color=cfg.GOLD), run_time=0.8)

    # --- 6. Title -------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(names, more, gives, pulls, leaving)), atom.nucleus.animate.set_opacity(0), fluorine.nucleus.animate.set_opacity(0),
               atom.cloud.fade_to(0.22), fluorine.cloud.fade_to(0.3), run_time=1.0)
    scene.play(atom.glide(np.array([6.9, 0.3, 0])),
               fluorine.glide(np.array([-6.6, 0.3, 0])), run_time=1.2)
    card_title = title_card("PERIODIC TRENDS", "EXPLAINED VISUALLY")
    card_title.move_to(UP * 0.55)
    rule = Line(LEFT * 5.2, RIGHT * 5.2, stroke_color=cfg.CYAN, stroke_width=3).next_to(card_title, DOWN, buff=0.32)
    part = txt(cfg.PROJECT_PART, cfg.FONT["small"], cfg.MUTED).next_to(rule, DOWN, buff=0.28)
    scene.play(FadeIn(card_title, shift=DOWN * 0.15), Create(rule), run_time=1.4)
    scene.play(FadeIn(part, shift=UP * 0.1), run_time=0.6)
    scene.play(Indicate(card_title.title[0], color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    scene.play(VGroup(card_title, rule, part).animate.scale(1.05), run_time=3.2, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["01"])
