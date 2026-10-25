"""Chapter 20 — predicting B2 and F2, then four filled diagrams side by side.

Each diagram uses its element's ordering (``mo_models.ORDERING``) and is filled
by ``mo_models.fill``; the line-up's bond orders and unpaired counts are read
from those fillings.
"""

from manim_scenes.common import *
from manim_scenes.scene_14_fill_nitrogen import PANEL_X, atom_sources, valence_diagram

LINEUP = ("B2", "N2", "O2", "F2")


class Scene20BoronFluorine(Scene):
    def construct(self) -> None:
        play_scene(self)


def compact(key: str, x: float, height: float = 5.0, y: float = 0.45) -> tuple[MODiagram, list[VGroup]]:
    """A small molecular-levels-only diagram, filled, without level labels."""
    f = mo.fill(key)
    d = MODiagram(f.diagram, center=[x, y, 0], height=height, ao_x=1.0, mo_width=0.62, gap=0.16, aos=False, axis=False)
    for label in d.labels.values():
        d.remove(label)
    return d, [arrow.scale(0.85) for arrow in d.electrons_for(f)]


def verdict_rows(f: mo.Filling) -> VGroup:
    color = cfg.PARAMAGNETIC if f.unpaired else cfg.DIAMAGNETIC
    return VGroup(txt(f"bond order {md.display_number(f.bond_order)}", cfg.FONT["body"], cfg.GREEN),
                  txt(f"{f.unpaired} unpaired", cfg.FONT["body"], color),
                  txt(f.magnetism, cfg.FONT["body"], color)).arrange(DOWN, buff=0.22)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "20", "Boron and fluorine")
    b2, f2 = mo.fill("B2"), mo.fill("F2")

    # --- 1. Read molecules nobody showed you ------------------------------------------------------------------------------
    teaser = result_label("Your turn to predict", cfg.GOLD, cfg.FONT["title"]).move_to([0, 0.3, 0])
    scene.play(FadeIn(teaser, scale=1.1), run_time=1.0)
    dismiss_opening_title(scene, t, head, at=2.2)

    # --- 2. Boron: three each, six in total; nitrogen's ordering ---------------------------------------------------------------
    beat(scene, t, 1)
    diagram = valence_diagram(b2.diagram.kind, "B")
    sources = atom_sources(diagram, mo.VALENCE_ELECTRONS["B"])
    name = formula("B2", cfg.FONT["title"]).move_to([PANEL_X, 2.6, 0])
    total = eq([f"{mo.VALENCE_ELECTRONS['B']}+{mo.VALENCE_ELECTRONS['B']}", "=", f"{b2.species.electrons}"],
               cfg.FONT["section"]).move_to([PANEL_X, 1.5, 0])
    scene.play(FadeOut(teaser), run_time=0.5)
    scene.play(FadeIn(diagram), FadeIn(name), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in sources], lag_ratio=0.1), Write(total), run_time=1.6)
    anims, arrows = fly_electrons(diagram, sources, b2)

    # --- 3. Four into the 2s pair; two left ----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(*anims[:2], run_time=1.4)
    scene.play(*anims[2:4], run_time=1.4)
    pi_box = diagram.highlight("p2p", cfg.GOLD)
    scene.play(Create(pi_box), run_time=0.8)

    # --- 4. Hund: one in each, spins parallel ----------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*anims[4:], run_time=1.6)
    scene.play(FadeOut(pi_box), run_time=0.5)

    # --- 5. Bond order one, two unpaired: paramagnetic ---------------------------------------------------------------------------------
    beat(scene, t, 4)
    rows = verdict_rows(b2).move_to([PANEL_X, 0.0, 0])
    fit_width(rows, 4.3)
    scene.play(FadeIn(rows, shift=UP * 0.15), FadeOut(total), run_time=1.0)
    lewis_note = caption("A simple Lewis structure doesn't suggest this", cfg.WHITE)
    scene.play(FadeIn(lewis_note), *[Indicate(a, color=cfg.WHITE, scale_factor=1.3) for a in arrows[4:]], run_time=1.2)

    # --- 6. Fluorine: seven each, fourteen; oxygen's ordering -----------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[FadeOut(m) for m in (diagram, *arrows, name, rows, lewis_note)], run_time=0.8)
    diagram = valence_diagram(f2.diagram.kind, "F")
    sources = atom_sources(diagram, mo.VALENCE_ELECTRONS["F"])
    name = formula("F2", cfg.FONT["title"]).move_to([PANEL_X, 2.6, 0])
    total = eq([f"{mo.VALENCE_ELECTRONS['F']}+{mo.VALENCE_ELECTRONS['F']}", "=", f"{f2.species.electrons}"],
               cfg.FONT["section"]).move_to([PANEL_X, 1.5, 0])
    scene.play(FadeIn(diagram), FadeIn(name), LaggedStart(*[FadeIn(a) for a in sources], lag_ratio=0.05), Write(total),
               run_time=1.6)
    anims, arrows = fly_electrons(diagram, sources, f2)

    # --- 7. Everything oxygen had, then two more ----------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(*anims[:12], run_time=2.2, lag_ratio=0.08)
    scene.play(*anims[12:], run_time=1.2)
    full = diagram.highlight("p2p*", cfg.ANTIBONDING)
    scene.play(Create(full), run_time=0.6)

    # --- 8. Eight bonding, six antibonding: bond order one, diamagnetic ---------------------------------------------------------------------------
    beat(scene, t, 7)
    counts = VGroup(chip(f"bonding: {f2.bonding}", cfg.BONDING), chip(f"antibonding: {f2.antibonding}", cfg.ANTIBONDING))
    counts.arrange(DOWN, buff=0.18).move_to([PANEL_X, 0.9, 0])
    rows = verdict_rows(f2).move_to([PANEL_X, -1.1, 0])
    fit_width(rows, 4.3)
    scene.play(FadeOut(total), FadeOut(full), run_time=0.4)
    scene.play(FadeIn(counts), run_time=0.5)
    scene.play(FadeIn(rows, shift=UP * 0.15), run_time=1.0)

    # --- 9. Line them up ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(*[FadeOut(m) for m in (diagram, *arrows, name, counts, rows)], run_time=0.8)
    xs = (-5.4, -1.8, 1.8, 5.4)
    line = VGroup()
    for key, x in zip(LINEUP, xs):
        f = mo.fill(key)
        d, arrs = compact(key, x)
        title = formula(key, cfg.FONT["section"]).move_to([x, 3.4, 0])
        order = txt(md.display_number(f.bond_order), cfg.FONT["title"], cfg.GREEN).move_to([x, -2.45, 0])
        spins = (VGroup(*[spin_arrow(1, cfg.UNPAIRED, 0.55) for _ in range(f.unpaired)]).arrange(RIGHT, buff=0.2)
                 if f.unpaired else txt("all paired", cfg.FONT["small"], cfg.DIAMAGNETIC)).move_to([x, -3.3, 0])
        column = VGroup(title, d, *arrs, order, spins)
        line.add(column)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in line], lag_ratio=0.3), run_time=2.4)

    # --- 10. Climbs and falls; magnetism on and off --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(*[Indicate(c[-2], color=cfg.WHITE, scale_factor=1.25) for c in line], run_time=1.4)
    scene.play(*[Indicate(c[-1], color=cfg.GOLD, scale_factor=1.25) for c, key in zip(line, LINEUP) if mo.unpaired(key)],
               run_time=1.4)
    narration_wait(scene, 1.0)
    scene.play(line.animate.scale(1.03), run_time=3.6, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["20"])
