"""Chapter 06 — two energies: the 1s level splits, and the split grows as the
atoms approach.

The diagram is ``mo_models.diagram("1s")``. The curves are the LCAO energies
of H2+ relative to H + H+ (``physics_models.h2plus_energies``), plotted in eV
against the separation in bohr; they are clipped at the top of the plot, and
the valley is the computed minimum.
"""

from manim_scenes.common import *

PLOT = PlotFrame([-3.6, -0.25, 0], 1.25, 0.72)
R_FAR, R_NEAR = 8.0, 0.95
E_TOP = 4.2


class Scene06TwoEnergies(Scene):
    def construct(self) -> None:
        play_scene(self)


def energy_ev(R, which: int):
    plus, minus = pm.h2plus_energies(np.asarray(R, dtype=float))
    return np.minimum((plus if which > 0 else minus) * pm.HARTREE_EV, E_TOP)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "06", "Two energies")
    dia = mo.diagram("1s")

    # --- 1. Energy axis, atom A and atom B ---------------------------------------------------------------------------------
    diagram = MODiagram(dia, center=[0, -0.2, 0], height=5.2, ao_x=4.2, mo_width=1.3, ao_width=1.1, atoms=("A", "B"))
    scene.play(GrowArrow(diagram.axis[0]), FadeIn(diagram.axis[1]), run_time=0.8)
    dismiss_opening_title(scene, t, head, at=1.6)
    scene.play(FadeIn(diagram.atom_names[0]), Create(diagram.ao_left["1s"]), FadeIn(diagram.ao_labels["1s"][0]),
               run_time=1.0)
    scene.play(FadeIn(diagram.atom_names[1]), Create(diagram.ao_right["1s"]), FadeIn(diagram.ao_labels["1s"][1]),
               run_time=1.0)

    # --- 2. Combine: the level splits in two --------------------------------------------------------------------------------
    beat(scene, t, 1)
    ao_y = diagram.y(dia.ao_level("1s").energy)
    guide = dashed_path([-2.6, ao_y, 0], [2.6, ao_y, 0], cfg.MUTED, 2.0, 0.45)
    starts = {k: diagram.levels[k].copy().set_y(ao_y) for k in ("s1s", "s1s*")}
    scene.play(Create(guide), FadeIn(starts["s1s"]), FadeIn(starts["s1s*"]), run_time=0.8)
    scene.play(ReplacementTransform(starts["s1s"], diagram.levels["s1s"]),
               ReplacementTransform(starts["s1s*"], diagram.levels["s1s*"]),
               Create(diagram.links["s1s"]), Create(diagram.links["s1s*"]), run_time=1.8)

    # --- 3. Bonding drops, antibonding rises -------------------------------------------------------------------------------------
    beat(scene, t, 2)
    drop = glow_arrow([0, ao_y, 0], [0, diagram.y(dia.level("s1s").energy) + 0.1, 0], cfg.GREEN, width=6)
    rise = glow_arrow([0, ao_y, 0], [0, diagram.y(dia.level("s1s*").energy) - 0.1, 0], cfg.ANTIBONDING, width=6)
    scene.play(GrowFromPoint(drop, [0, ao_y, 0]), Write(diagram.labels["s1s"]), run_time=1.2)
    scene.play(GrowFromPoint(rise, [0, ao_y, 0]), Write(diagram.labels["s1s*"]), run_time=1.2)
    words = VGroup(txt("bonding: lower", cfg.FONT["small"], cfg.GREEN).next_to(diagram.labels["s1s"], RIGHT, buff=0.4),
                   txt("antibonding: higher", cfg.FONT["small"], cfg.ANTIBONDING)
                   .next_to(diagram.labels["s1s*"], RIGHT, buff=0.4))
    scene.play(FadeIn(words), run_time=0.8)

    # --- 4. The rise is a little larger than the drop ---------------------------------------------------------------------------------
    beat(scene, t, 3)
    gap_down = dia.ao_level("1s").energy - dia.level("s1s").energy
    gap_up = dia.level("s1s*").energy - dia.ao_level("1s").energy
    ruler = VGroup(
        Line([-0.9, ao_y, 0], [-0.9, diagram.y(dia.level("s1s").energy), 0], stroke_color=cfg.GREEN, stroke_width=10),
        Line([0.9, ao_y, 0], [0.9, diagram.y(dia.level("s1s*").energy), 0], stroke_color=cfg.ANTIBONDING, stroke_width=10),
    )
    compare = eq(r"\text{rise} > \text{drop}", cfg.FONT["section"], cfg.WHITE).move_to([5.0, 0.2, 0])
    scene.play(Create(ruler[0]), run_time=0.8)
    scene.play(Create(ruler[1]), run_time=0.8)
    scene.play(ruler[0].animate.move_to([0.5, ao_y + (ao_y - diagram.y(dia.level("s1s").energy)) / 2, 0]),
               run_time=1.2)
    assert gap_up > gap_down
    scene.play(Write(compare), run_time=1.0)

    # --- 5. Watch the split as the atoms approach ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(ruler), FadeOut(compare), FadeOut(words), FadeOut(drop), FadeOut(rise), FadeOut(guide),
               FadeOut(diagram), run_time=1.0)
    R = ValueTracker(R_FAR)
    x_axis = Arrow(PLOT.point(0.6, 0), PLOT.point(8.4, 0), buff=0, color=cfg.MUTED, stroke_width=4, tip_length=0.22)
    y_axis = Arrow(PLOT.point(0.6, -2.3), PLOT.point(0.6, E_TOP + 0.4), buff=0, color=cfg.MUTED, stroke_width=4,
                   tip_length=0.22)
    r_label = txt("distance", cfg.FONT["small"], cfg.MUTED).next_to(x_axis, DOWN, buff=0.15).align_to(x_axis, RIGHT)
    e_label = eq("E", cfg.FONT["label"], cfg.MUTED).next_to(y_axis.get_end(), LEFT, buff=0.15)
    zero_note = txt("H + H⁺", cfg.FONT["tiny"], cfg.MUTED).next_to(PLOT.point(8.4, 0), UP, buff=0.38)
    zero_note.align_to(x_axis, RIGHT)
    bonding_curve = live(lambda: plain_curve(lambda r: energy_ev(r, 1), (R.get_value(), R_FAR), PLOT, cfg.BONDING))
    anti_curve = live(lambda: plain_curve(lambda r: energy_ev(r, -1), (R.get_value(), R_FAR), PLOT, cfg.ANTIBONDING))
    riders = VGroup(glow_dot(ORIGIN, cfg.BONDING), glow_dot(ORIGIN, cfg.ANTIBONDING))

    def ride(group):
        r = R.get_value()
        group[0].move_to(PLOT.point(r, float(energy_ev(r, 1))))
        group[1].move_to(PLOT.point(r, float(energy_ev(r, -1))))

    riders.add_updater(ride)
    pair = VGroup(nucleus_dot(ORIGIN, cfg.WHITE), nucleus_dot(ORIGIN, cfg.WHITE))

    def spread(group):
        half = R.get_value() * 0.22
        group[0].move_to([1.4 - half, 3.3, 0])
        group[1].move_to([1.4 + half, 3.3, 0])

    pair.add_updater(spread)
    scene.play(GrowArrow(x_axis), GrowArrow(y_axis), FadeIn(r_label), FadeIn(e_label), FadeIn(zero_note), run_time=1.0)
    scene.add(bonding_curve, anti_curve, riders, pair)
    same = caption("Far apart: the same energy", cfg.WHITE)
    scene.play(FadeIn(same), FadeIn(pair), run_time=0.8)

    # --- 6. Closer: a valley and a climb ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    split = caption("Closer: the energies separate", cfg.CYAN)
    scene.play(fade_through(same, split), run_time=0.8)
    scene.remove(same)
    scene.play(R.animate.set_value(R_NEAR), run_time=7.0, rate_func=smooth)

    # --- 7. The valley is a bond ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    r_min, depth = pm.h2plus_minimum()
    scene.play(R.animate.set_value(r_min), run_time=2.0, rate_func=smooth)
    valley = glow_dot(PLOT.point(r_min, -depth), cfg.GOLD, radius=0.12)
    bond_word = result_label("a bond", cfg.GOLD, cfg.FONT["body"]).next_to(valley, DOWN, buff=0.35)
    lower = caption("H₂⁺: lower energy than separated H + H⁺", cfg.GREEN)
    scene.play(FadeIn(valley, scale=0.4), FadeIn(bond_word), fade_through(split, lower), run_time=1.2)
    scene.remove(split)
    scene.play(R.animate.set_value(3.6), run_time=1.8, rate_func=there_and_back)

    # --- 8. The rule for every molecule -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    for mob in (bonding_curve, anti_curve, riders, pair):
        mob.clear_updaters()
    scene.play(*[FadeOut(m) for m in (x_axis, y_axis, r_label, e_label, zero_note, bonding_curve, anti_curve,
                                      riders, pair, valley, bond_word, lower)], run_time=1.0)
    rule_head = result_label("The rule", cfg.GOLD, cfg.FONT["title"]).move_to([0, 2.4, 0])
    scene.play(FadeIn(rule_head, shift=DOWN * 0.2), run_time=0.8)

    # --- 9. Bonding helps, antibonding undoes; which orbitals matter --------------------------------------------------------------------------------------
    beat(scene, t, 8)
    up = VGroup(spin_arrow(1, cfg.BONDING, 0.7), txt("in a bonding orbital: holds the molecule together", cfg.FONT["body"],
                                                     cfg.BONDING)).arrange(RIGHT, buff=0.4)
    down = VGroup(spin_arrow(1, cfg.ANTIBONDING, 0.7), txt("in an antibonding orbital: undoes that help",
                                                           cfg.FONT["body"], cfg.ANTIBONDING)).arrange(RIGHT, buff=0.4)
    rows = VGroup(up, down).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([0, 0.4, 0])
    fit_width(rows, 14.0)
    scene.play(FadeIn(up, shift=RIGHT * 0.2), run_time=1.0)
    narration_wait(scene, 2.0)
    scene.play(FadeIn(down, shift=RIGHT * 0.2), run_time=1.0)
    which = result_label("Not just how many electrons — which orbitals", cfg.GREEN, cfg.FONT["body"]).move_to([0, -2.2, 0])
    narration_wait(scene, 1.4)
    scene.play(FadeIn(which, shift=UP * 0.2), run_time=1.0)
    scene.play(Indicate(which.label, color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    scene.play(VGroup(rule_head, rows, which).animate.scale(1.04), run_time=6.0, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
