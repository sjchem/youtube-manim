"""Chapter 17 — mystery solved: bond order two, two unpaired electrons, and the
pour explained.

The diagram, counts and bond order come from ``mo_models.fill("O2")``. The
spin picture is ``physics_models.spin_angles`` (aligned with a jitter in a
field, random without one); the pours are ``physics_models.pour`` for a
paramagnetic and a diamagnetic liquid. The magnet's pull acts on molecules
that each carry two parallel unpaired spins; without the field the spins
point every which way.
"""

from manim_scenes.common import *
from manim_scenes.cryogenic_lab import CryogenicPour
from manim_scenes.scene_14_fill_nitrogen import PANEL_X, valence_diagram

SPIN_COUNT = 6


class Scene17MysterySolved(Scene):
    def construct(self) -> None:
        play_scene(self)


class SpinSwarm(VGroup):
    """A few O2 molecules, each with one arrow for its pair of parallel spins."""

    def __init__(self, center, count: int = SPIN_COUNT) -> None:
        super().__init__()
        self.angles = np.zeros(count)
        self.items = []
        c = np.asarray(center, dtype=float)
        for i in range(count):
            spot = c + np.array([(i % 3 - 1) * 1.45, (0.7 if i < 3 else -0.75), 0])
            atoms = VGroup()
            icon_stage = Stage()
            for side in (-1, 1):
                atom = Ball(spot + side * RIGHT * 0.2, 0.17, cfg.ELEMENT_COLORS["O"])
                atom.place(icon_stage, np.eye(3), 1.0)
                atoms.add(atom.mob)
            arrow = spin_arrow(1, cfg.UNPAIRED, 0.75).move_to(spot)
            self.items.append((spot, arrow))
            self.add(atoms, arrow)
        self.base = [a.copy() for _, a in self.items]

    def set_angles(self, angles) -> None:
        self.angles = np.asarray(angles, dtype=float)
        for (spot, arrow), base, angle in zip(self.items, self.base, self.angles):
            arrow.become(base.copy().rotate(float(angle), about_point=spot))

    def turn_to(self, angles, **kwargs) -> Param:
        return Param(self, lambda: self.angles.copy(), self.set_angles, np.asarray(angles, dtype=float), mode="vector",
                     **kwargs)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "Mystery solved")
    o2 = mo.fill("O2")

    # --- 1. Bonding electrons: eight -----------------------------------------------------------------------------------------
    diagram = valence_diagram(o2.diagram.kind, "O")
    arrows = diagram.electrons_for(o2)
    dismiss_opening_title(scene, t, head, at=1.0)
    scene.play(FadeIn(diagram), LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.05), run_time=1.6)
    bonding = VGroup(*[a for a, p in zip(arrows, o2.electrons) if o2.diagram.level(p.level).bonding])
    anti = VGroup(*[a for a, p in zip(arrows, o2.electrons) if not o2.diagram.level(p.level).bonding])
    nb = chip(f"bonding: {o2.bonding}", cfg.BONDING, cfg.FONT["body"]).move_to([PANEL_X, 2.6, 0])
    scene.play(Indicate(bonding, color=cfg.GREEN, scale_factor=1.25), FadeIn(nb), run_time=1.6)

    # --- 2. Antibonding: four -------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    na = chip(f"antibonding: {o2.antibonding}", cfg.ANTIBONDING, cfg.FONT["body"]).move_to([PANEL_X, 1.5, 0])
    fit_width(na, 4.3)
    scene.play(Indicate(anti, color=cfg.ANTIBONDING, scale_factor=1.25), FadeIn(na), run_time=1.6)

    # --- 3. Bond order two ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    numbers = bond_order_numbers(o2.bonding, o2.antibonding, cfg.FONT["title"]).move_to([PANEL_X, 0.1, 0])
    fit_width(numbers, 4.3)
    scene.play(Write(numbers), run_time=1.6)

    # --- 4. A double bond, as the Lewis structure said -----------------------------------------------------------------------------------
    beat(scene, t, 3)
    lewis = LewisDiatomic("O", 2, 2, at=[PANEL_X, -1.75, 0], size=130, spacing=2.2)
    scene.play(Write(lewis), run_time=1.2)
    scene.play(Indicate(lewis.bonds, color=cfg.GREEN, scale_factor=1.2), run_time=1.0)

    # --- 5. Lewis: right bond order, wrong electrons ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[FadeOut(m) for m in (diagram, *arrows, nb, na, numbers)], run_time=0.6)
    scene.play(lewis.animate.move_to([-3.8, 1.6, 0]), run_time=0.7)
    rows_lewis = VGroup(VGroup(check_mark(0.24), txt("bond order 2", cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.3),
                        VGroup(cross_mark(0.22), txt("unpaired electrons", cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.3))
    rows_lewis.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-3.8, -0.9, 0])
    lewis_title = txt("Lewis", cfg.FONT["section"], cfg.MUTED).move_to([-3.8, 3.2, 0])
    scene.play(FadeIn(lewis_title), FadeIn(rows_lewis[0], shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(rows_lewis[1], shift=UP * 0.15), run_time=1.0)

    # --- 6. MO theory: both answers ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    mo_title = txt("Molecular orbitals", cfg.FONT["section"], cfg.CYAN).move_to([3.8, 3.2, 0])
    mini = VGroup(spin_arrow(1, cfg.UNPAIRED, 0.8), spin_arrow(1, cfg.UNPAIRED, 0.8)).arrange(RIGHT, buff=0.5)
    mini.move_to([3.8, 1.6, 0])
    rows_mo = VGroup(VGroup(check_mark(0.24), txt("bond order 2", cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.3),
                     VGroup(check_mark(0.24), txt("2 unpaired electrons", cfg.FONT["body"], cfg.UNPAIRED)).arrange(RIGHT, buff=0.3))
    rows_mo.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.8, -0.9, 0])
    divider = DashedLine([0, 3.4, 0], [0, -2.4, 0], stroke_color=cfg.MUTED, stroke_width=3)
    scene.play(Create(divider), FadeIn(mo_title), FadeIn(mini), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rows_mo], lag_ratio=0.4), run_time=1.4)

    # --- 7. Now the experiment makes sense -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(*[FadeOut(m) for m in (lewis, rows_lewis, lewis_title, mo_title, mini, rows_mo, divider)], run_time=1.0)
    magnet = Electromagnet([2.9, 0.7, 0], scale=1.2)
    pour = CryogenicPour(magnet, drops=90, seed=cfg.SEED + 17, duration=8.0)
    swarm = SpinSwarm([-4.4, 0.4, 0])
    swarm.scale(1.45, about_point=np.array([-4.4, 0.4, 0]))
    swarm.items = [(np.array([-4.4, 0.4, 0]) + (spot - np.array([-4.4, 0.4, 0])) * 1.45, arrow)
                   for spot, arrow in swarm.items]
    swarm.base = [arrow.copy() for _, arrow in swarm.items]
    swarm.set_angles(pm.spin_angles(SPIN_COUNT, False, seed=cfg.SEED))
    swarm_label = txt("each O₂: two parallel spins", cfg.FONT["body"], cfg.UNPAIRED).move_to([-4.4, 2.75, 0])
    fit_width(swarm_label, 6.6)
    scene.play(FadeIn(magnet), FadeIn(pour.flask), FadeIn(swarm), FadeIn(swarm_label), run_time=1.2)

    # --- 8. The field pulls the tiny magnets toward the gap --------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.add(pour)
    scene.play(magnet.field_on(), swarm.turn_to(pm.spin_angles(SPIN_COUNT, True, seed=cfg.SEED)), run_time=1.6)
    pour.run()
    aligned = caption("The field favours alignment and attracts oxygen", cfg.GOLD)
    scene.play(FadeIn(aligned), run_time=0.8)
    narration_wait(scene, 4.0)

    # --- 9. It gathers and hangs in the gap ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    hangs = caption("The liquid gathers and hangs between the poles", cfg.LIQUID_O2)
    scene.play(fade_through(aligned, hangs), run_time=0.8)
    scene.remove(aligned)
    gap_ring = glow_frame(Rectangle(width=1.8, height=1.2).move_to(magnet.gap_center), cfg.GOLD, buff=0.1)
    scene.play(Create(gap_ring), run_time=0.8)

    # --- 10. A response, not a permanent magnet ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    pour.run(False)
    response = caption("A response to the field, not a permanent magnet", cfg.WHITE)
    scene.play(FadeOut(gap_ring), magnet.field.animate.set_stroke(opacity=0), fade_through(hangs, response),
               swarm.turn_to(pm.spin_angles(SPIN_COUNT, False, seed=cfg.SEED + 5)), run_time=1.6)
    scene.remove(hangs)
    # Release the complete glossy bridge, including its meniscus and reflections.
    scene.play(*[part.animate.shift(DOWN * 2.2).set_opacity(0)
                 for part in (pour.drops, pour.bridge, pour.water_line, pour.caustics)],
               pour.jet.animate.set_opacity(0), run_time=1.6, rate_func=rush_into)

    # --- 11. Nitrogen pours straight past ----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(swarm), FadeOut(swarm_label), FadeOut(pour), FadeOut(response), magnet.animate.shift(RIGHT * 1.6),
               run_time=1.0)
    scene.remove(magnet)
    o_magnet = Electromagnet([-3.7, 0.7, 0], scale=1.1)
    n_magnet = Electromagnet([3.7, 0.7, 0], scale=1.1)
    o_pour = CryogenicPour(o_magnet, drops=80, seed=cfg.SEED + 171, duration=7.0)
    n_pour = CryogenicPour(n_magnet, paramagnetic=False, drops=80, seed=cfg.SEED + 172, duration=7.0)
    names = VGroup(formula("O2", cfg.FONT["section"], cfg.LIQUID_O2).move_to([-6.6, 2.4, 0]),
                   formula("N2", cfg.FONT["section"], cfg.LIQUID_N2).move_to([0.8, 2.4, 0]))
    scene.play(FadeIn(o_magnet), FadeIn(n_magnet), FadeIn(o_pour.flask), FadeIn(n_pour.flask), FadeIn(names),
               o_magnet.field_on(), n_magnet.field_on(), run_time=1.2)
    scene.add(o_pour, n_pour)
    scene.bring_to_front(n_magnet)  # Nitrogen falls behind the solid base.
    o_pour.run()
    n_pour.run()

    # --- 12. Same magnet, two liquids, two electrons apart ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    apart = caption("Same magnet. Two liquids. Molecules two electrons apart.", cfg.WHITE)
    scene.play(FadeIn(apart), run_time=0.8)

    # --- 13. Bond order and magnetism, one diagram ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    one = caption("Bond order and magnetism, from one diagram", cfg.GREEN)
    scene.play(fade_through(apart, one), run_time=0.8)
    scene.remove(apart)
    scene.play(Indicate(names, color=cfg.WHITE, scale_factor=1.15), run_time=1.6)

    # --- 14. A fair note on valence bond theory -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    o_pour.run(False)
    n_pour.run(False)
    note = VGroup(txt("Fair note", cfg.FONT["section"], cfg.PURPLE),
                  txt("Advanced valence bond calculations", cfg.FONT["body"], cfg.WHITE),
                  txt("also describe the unpaired electrons.", cfg.FONT["body"], cfg.WHITE),
                  txt("The simple Lewis pairing picture can't.", cfg.FONT["body"], cfg.MUTED)).arrange(DOWN, buff=0.25)
    box = panel(note.width + 0.9, note.height + 0.7, cfg.PURPLE, 0.92).move_to(note)
    scene.play(*[FadeOut(m) for m in (o_magnet, n_magnet, o_pour, n_pour, names, one)], run_time=0.8)
    scene.play(FadeIn(box), FadeIn(note, shift=UP * 0.15), run_time=1.2)

    # --- 15. MO theory makes it natural ----------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    natural = caption("Molecular orbital theory makes it unavoidable", cfg.CYAN)
    scene.play(FadeIn(natural), run_time=0.8)

    # --- 16. One more surprise ---------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    scene.play(FadeOut(box), FadeOut(note), FadeOut(natural), run_time=0.8)
    teaser = VGroup(spin_arrow(1, cfg.UNPAIRED, 0.9), txt("?", 120, cfg.GOLD)).arrange(RIGHT, buff=0.5).move_to([0, 0.5, 0])
    question = caption("What if we take an electron away?", cfg.GOLD)
    scene.play(FadeIn(teaser[0]), FadeIn(question), run_time=0.8)
    scene.play(teaser[0].animate.shift(UP * 1.2).set_opacity(0.3), FadeIn(teaser[1], scale=0.6), run_time=1.4)
    for _ in range(2):
        scene.play(teaser[1].animate.scale(1.15), run_time=2.9, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["17"])
