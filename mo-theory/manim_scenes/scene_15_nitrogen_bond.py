"""Chapter 15 — nitrogen's triple bond, and a liquid that ignores the magnet.

The 3D bond is the computed sigma 2p orbital plus the two degenerate pi 2p
orbitals (``utils.orbital_models``). Bond energies and lengths come from
``utils.mo_data``. The pour is ``physics_models.pour`` for a diamagnetic
liquid: its push from the field is far too weak to see, so it falls through.
"""

from manim_scenes.common import *
from manim_scenes.cryogenic_lab import CryogenicPour

STAGE_AT = np.array([-2.2, -0.3, 0])
PANEL_X = 4.9
MAGNET_AT = np.array([3.9, 0.7, 0])


class Scene15NitrogenBond(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "Nitrogen's triple bond")
    n2 = mo.fill("N2")

    # --- 1. Bond order three ---------------------------------------------------------------------------------------------
    lewis = LewisDiatomic("N", 3, 1, at=[0, 0.4, 0])
    order = eq([r"\text{bond order} = ", md.display_number(n2.bond_order)], cfg.FONT["title"]).move_to([0, -1.9, 0])
    order[1].set_color(cfg.GREEN)
    scene.play(Write(lewis), run_time=1.4)
    dismiss_opening_title(scene, t, head, at=2.0)
    scene.play(Write(order), run_time=1.2)

    # --- 2. One sigma, two pi ---------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(lewis), FadeOut(order), run_time=0.8)
    stage = Stage(STAGE_AT, zoom=0.9, yaw=0.35, pitch=0.3, sway=0.25)
    sigma = MOCloud(stage, om.MOSpec("ps", 1.0, om.R_P), opacity=0.68)
    pis = [MOCloud(stage, om.MOSpec(kind, 1.0, om.R_P), opacity=0.56, plus=cfg.PHASE_PLUS, minus=cfg.PHASE_MINUS,
                   presence=0.0) for kind in ("py", "pz")]
    stage_nuclei(stage, sigma)
    show(scene, stage, 1.0)
    parts = VGroup(eq(r"1\ \sigma", cfg.FONT["title"], cfg.BONDING),
                   eq(r"+\ \pi_y", cfg.FONT["title"], cfg.TEAL),
                   eq(r"+\ \pi_z", cfg.FONT["title"], cfg.TEAL))
    parts.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([PANEL_X, 0.6, 0])
    scene.play(FadeIn(parts[0]), run_time=0.6)
    # Inspect each contribution before leaving the others as faint context.
    scene.play(*sigma.fade(0.12), *pis[0].fade(1.0), FadeIn(parts[1]), run_time=1.0)
    scene.play(*pis[0].fade(0.15), *pis[1].fade(1.0), FadeIn(parts[2]), run_time=1.0)
    scene.play(stage.rock(RIGHT, PI), run_time=3.0, rate_func=smooth)

    # --- 3. One of the strongest bonds -----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    hide(scene, stage, 0.8, FadeOut(parts))
    keys = ("B2", "C2", "N2", "O2", "F2")
    rows = [(mo.species(k).tex, md.DISSOCIATION_EV[k], f"{md.DISSOCIATION_EV[k]:.1f} eV",
             cfg.GREEN if k == "N2" else cfg.MUTED) for k in keys]
    strength = compare_bars(rows, max_value=10.0, length=6.4, title="energy to pull the atoms apart", label_width=1.6)
    strength.scale(1.15).move_to([0, 0.2, 0])
    scene.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in strength.bars], lag_ratio=0.25), FadeIn(strength[1]),
               run_time=2.4)
    inert = caption("A strong triple bond helps explain nitrogen's low reactivity", cfg.WHITE)
    scene.play(Indicate(strength.bars[2], color=cfg.GREEN, scale_factor=1.06), FadeIn(inert), run_time=1.4)

    # --- 4. Higher bond order, shorter and stronger --------------------------------------------------------------------------------
    beat(scene, t, 3)
    trio = ("N2", "O2", "F2")
    length_rows = [(mo.species(k).tex + rf"\ \ ({md.display_number(mo.bond_order(k))})", md.BOND_LENGTH_PM[k],
                    f"{md.BOND_LENGTH_PM[k]:.0f} pm", cfg.CYAN) for k in trio]
    lengths = compare_bars(length_rows, max_value=150, length=5.0, title="bond order → bond length", label_width=2.6)
    lengths.scale(1.15).move_to([0, 0.2, 0])
    trend = caption("Higher bond order: usually shorter and stronger", cfg.CYAN)
    scene.play(FadeOut(strength), fade_through(inert, trend), run_time=1.0)
    scene.remove(inert)
    scene.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in lengths.bars], lag_ratio=0.3), FadeIn(lengths[1]),
               run_time=2.0)

    # --- 5. The magnetic question: all paired ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(lengths), FadeOut(trend), run_time=0.8)
    lewis2 = LewisDiatomic("N", 3, 1, at=[-4.4, 0.9, 0], size=150, spacing=2.6)
    predict = VGroup(txt("all electrons paired", cfg.FONT["body"], cfg.WHITE),
                     txt("prediction: not drawn in", cfg.FONT["body"], cfg.DIAMAGNETIC)).arrange(DOWN, buff=0.3)
    predict.move_to([-4.4, -1.3, 0])
    scene.play(FadeIn(lewis2), run_time=0.8)
    scene.play(FadeIn(predict[0]), run_time=0.8)
    scene.play(FadeIn(predict[1]), run_time=0.8)

    # --- 6. Pour liquid nitrogen: it falls straight through ------------------------------------------------------------------------------
    beat(scene, t, 5)
    magnet = Electromagnet(MAGNET_AT, scale=1.2)
    pour = CryogenicPour(magnet, paramagnetic=False, drops=80, seed=cfg.SEED + 15, duration=7.0)
    label = txt("liquid nitrogen", cfg.FONT["small"], cfg.LIQUID_N2).next_to(pour.flask, LEFT, buff=0.3)
    scene.play(FadeIn(magnet), FadeIn(pour.flask), FadeIn(label), magnet.field_on(), run_time=1.2)
    scene.add(pour)
    # The falling stream passes behind the solid magnet base.
    scene.bring_to_front(magnet)
    pour.run()
    through = caption("It falls straight through", cfg.WHITE)
    narration_wait(scene, 1.6)
    scene.play(FadeIn(through), run_time=0.8)

    # --- 7. Diamagnetic: pushed away, too weakly to see -------------------------------------------------------------------------------------
    beat(scene, t, 6)
    dia = result_label("diamagnetic", cfg.DIAMAGNETIC, cfg.FONT["title"]).move_to([-4.4, -1.3, 0])
    weak = fit_width(txt("pushed away, far too weakly to see", cfg.FONT["small"], cfg.MUTED), 6.0).next_to(dia, DOWN, buff=0.3)
    scene.play(fade_through(predict, dia), run_time=1.0)
    scene.remove(predict)
    scene.play(FadeIn(weak), run_time=0.8)

    # --- 8. Nitrogen makes sense; now oxygen -------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    pour.run(False)
    plus_two = eq([r"\mathrm{N_2}:\ " + str(mo.species("N2").electrons), r"\rightarrow",
                   r"\mathrm{O_2}:\ " + str(mo.species("O2").electrons)], cfg.FONT["title"])
    plus_two[2].set_color(cfg.GOLD)
    valence = txt("valence electrons", cfg.FONT["body"], cfg.MUTED)
    plus_two.move_to([0, 0.5, 0])
    valence.next_to(plus_two, DOWN, buff=0.4)
    note = caption("Two more electrons, and the other ordering", cfg.GOLD)
    scene.play(*[FadeOut(m) for m in (magnet, pour, label, lewis2, dia, weak, through)], run_time=1.0)
    scene.play(Write(plus_two), FadeIn(valence), FadeIn(note), run_time=1.6)

    # --- 9. Find the unpaired electrons -------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    find = caption("Where are oxygen's unpaired electrons?", cfg.GOLD)
    scene.play(fade_through(note, find), Indicate(plus_two[2], color=cfg.GOLD, scale_factor=1.2), run_time=1.2)
    scene.remove(note)
    scene.play(plus_two.animate.scale(1.08), run_time=2.0, rate_func=there_and_back)
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
