"""Chapter 14 — filling nitrogen's diagram, ten electrons, bond order three.

Every arrow starts on its own atom (``mo_models.atomic_placements``) and flies
to the slot ``mo_models.fill("N2")`` gives it, in Aufbau order; the counts,
configuration and bond order are read from that filling.
"""

from manim_scenes.common import *

DIAGRAM_AT = np.array([-2.15, -0.15, 0])
PANEL_X = 5.45


class Scene14FillNitrogen(Scene):
    def construct(self) -> None:
        play_scene(self)


def valence_diagram(kind: str, symbol: str, *, center=DIAGRAM_AT, height: float = 5.9, ao_x: float = 3.45) -> MODiagram:
    """The valence diagram used by the filling chapters (14-21)."""
    return MODiagram(mo.diagram(kind), center=center, height=height, ao_x=ao_x, mo_width=0.82, ao_width=0.58, gap=0.24,
                     atoms=(symbol, symbol))


def atom_sources(diagram: MODiagram, per_atom: int) -> list[VGroup]:
    """Each atom's valence electrons on its own levels, interleaved left/right
    so the two atoms contribute evenly as the molecule fills."""
    left = diagram.atom_electrons(per_atom, "L")
    right = diagram.atom_electrons(per_atom, "R")
    return [arrow for pair in zip(left, right) for arrow in pair]


def counter(n: int, total: int) -> MathTex:
    return eq(rf"{n}\,/\,{total}", cfg.FONT["section"], cfg.GREEN if n == total else cfg.WHITE)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "Filling nitrogen")
    filling = mo.fill("N2")
    per_atom = mo.VALENCE_ELECTRONS["N"]
    total = filling.species.electrons

    # --- 1. Five plus five ------------------------------------------------------------------------------------------------
    diagram = valence_diagram(filling.diagram.kind, "N")
    sources = atom_sources(diagram, per_atom)
    dismiss_opening_title(scene, t, head, at=1.2)
    scene.play(FadeIn(diagram), run_time=1.2)
    scene.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in sources], lag_ratio=0.08), run_time=1.6)
    sum_tex = eq([rf"{per_atom}", "+", rf"{per_atom}", "=", rf"{total}"], cfg.FONT["title"]).move_to([PANEL_X, 2.6, 0])
    sum_tex[-1].set_color(cfg.GOLD)
    scene.play(Write(sum_tex), run_time=1.2)

    # --- 2. Nitrogen's ordering --------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    order = glow_frame(VGroup(diagram.level_group("p2p", links=False), diagram.level_group("s2p", links=False)), cfg.GOLD,
                       buff=0.14)
    order_word = txt("pi below sigma", cfg.FONT["small"], cfg.GOLD).move_to([PANEL_X, 1.4, 0])
    scene.play(Create(order), FadeIn(order_word), run_time=1.0)
    scene.play(FadeOut(order), run_time=0.6)

    # --- 3-7. Fill from the bottom ---------------------------------------------------------------------------------------------
    anims, arrows = fly_electrons(diagram, sources, filling, unpaired_gold=False)
    tally = counter(0, total).move_to([PANEL_X, 0.2, 0])
    placed_word = txt("placed", cfg.FONT["small"], cfg.MUTED).next_to(tally, DOWN, buff=0.32)
    scene.play(FadeIn(tally), FadeIn(placed_word), run_time=0.6)
    steps = [(2, 0, 2), (3, 2, 4), (4, 4, 6), (5, 6, 8), (6, 8, 10)]
    notes = {3: caption("So far, bonding and antibonding cancel", cfg.ANTIBONDING),
             4: caption("Hund's rule: one in each, spins parallel", cfg.GOLD)}
    shown_note = None
    for index, lo, hi in steps:
        beat(scene, t, index)
        new_tally = counter(hi, total).move_to(tally)
        extra = []
        if shown_note is not None:
            extra.append(FadeOut(shown_note))
        scene.play(*anims[lo:hi], Transform(tally, new_tally), *extra, run_time=1.8, lag_ratio=0.25)
        shown_note = None
        if index in notes:
            shown_note = notes[index]
            scene.play(FadeIn(shown_note), run_time=0.6)

    # --- 8. Ten electrons placed ----------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    done = check_mark(0.3).next_to(tally, RIGHT, buff=0.3)
    scene.play(Create(done), Indicate(tally, color=cfg.GREEN, scale_factor=1.15), run_time=1.0)

    # --- 9. The configuration -------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    config = eq(filling.configuration_tex(), cfg.FONT["body"])
    for part, level in zip(config, [lv for lv in filling.diagram.ordered() if sum(filling.occupancy()[lv.key])]):
        part.set_color(cfg.BONDING if level.bonding else cfg.ANTIBONDING)
    fit_width(config, 13.6)
    config.move_to([0, -3.65, 0])
    scene.play(Write(config), run_time=2.4)

    # --- 10. Every occupied orbital holds a pair -------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    pairs = VGroup(*[check_mark(0.14).next_to(diagram.levels[key], LEFT if key.startswith("s") else RIGHT, buff=0.12)
                     .shift(LEFT * 0.0) for key, counts in filling.occupancy().items() if sum(counts)])
    no_lone = txt("no electron alone", cfg.FONT["small"], cfg.GREEN).move_to([PANEL_X, -1.3, 0])
    scene.play(LaggedStart(*[Create(c) for c in pairs], lag_ratio=0.15), FadeIn(no_lone), run_time=1.6)

    # --- 11. Count bonding and antibonding ----------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(pairs), FadeOut(no_lone), FadeOut(sum_tex), FadeOut(order_word), FadeOut(tally), FadeOut(done),
               FadeOut(placed_word), run_time=0.8)
    bonding = VGroup(*[a for a, p in zip(arrows, filling.electrons) if filling.diagram.level(p.level).bonding])
    anti = VGroup(*[a for a, p in zip(arrows, filling.electrons) if not filling.diagram.level(p.level).bonding])
    nb = chip(f"bonding: {filling.bonding}", cfg.BONDING, cfg.FONT["body"]).move_to([PANEL_X, 2.5, 0])
    na = chip(f"antibonding: {filling.antibonding}", cfg.ANTIBONDING, cfg.FONT["body"]).move_to([PANEL_X, 1.4, 0])
    fit_width(na, 4.3)
    scene.play(Indicate(bonding, color=cfg.GREEN, scale_factor=1.2), FadeIn(nb), run_time=1.4)
    scene.play(Indicate(anti, color=cfg.ANTIBONDING, scale_factor=1.2), FadeIn(na), run_time=1.4)

    # --- 12. Bond order three ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    numbers = bond_order_numbers(filling.bonding, filling.antibonding, cfg.FONT["title"]).move_to([PANEL_X, -0.2, 0])
    fit_width(numbers, 4.3)
    scene.play(Write(numbers), run_time=1.6)

    # --- 13. A triple bond: N≡N -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    lewis = LewisDiatomic("N", 3, 1, at=[PANEL_X, -1.95, 0], size=120, spacing=2.3).scale(0.85)
    scene.play(Write(lewis), run_time=1.4)
    scene.play(Indicate(lewis.bonds, color=cfg.GREEN, scale_factor=1.15), Indicate(numbers[-1], color=cfg.GREEN), run_time=1.4)
    scene.play(lewis.animate.scale(1.12), run_time=4.6, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
