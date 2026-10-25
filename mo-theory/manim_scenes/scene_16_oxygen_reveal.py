"""Chapter 16 — the reveal: oxygen's twelve Lewis electrons fly into its
molecular orbitals, and the last two land unpaired in pi*.

Each Lewis dot is carried to the slot ``mo_models.fill("O2")`` assigns, in
Aufbau order; Hund's rule (in the model) sends the twelfth electron to the
second pi* orbital with its spin parallel. The closing 3D shot is the pair of
computed pi* orbitals, each holding one of those electrons.
"""

from manim_scenes.common import *
from manim_scenes.scene_14_fill_nitrogen import counter, valence_diagram

DIAGRAM_AT = np.array([1.35, -0.15, 0])
LEWIS_AT = np.array([-5.45, 1.6, 0])


class Scene16OxygenReveal(Scene):
    def construct(self) -> None:
        play_scene(self)


def bar_magnet(height: float = 0.62) -> VGroup:
    """A tiny bar magnet pointing up: red north on top, blue south below."""
    north = Rectangle(width=0.2, height=height / 2, stroke_width=0, fill_color=cfg.RED, fill_opacity=1)
    south = Rectangle(width=0.2, height=height / 2, stroke_width=0, fill_color=cfg.BLUE, fill_opacity=1)
    return VGroup(north, south).arrange(DOWN, buff=0)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "Oxygen: where are they?")
    o2 = mo.fill("O2")
    total = o2.species.electrons

    # --- 1. Back to the mystery --------------------------------------------------------------------------------------------
    lewis = LewisDiatomic("O", 2, 2, at=[0, 0.3, 0], size=210, spacing=3.4)
    scene.play(Write(lewis), run_time=1.6)
    dismiss_opening_title(scene, t, head, at=2.6)

    # --- 2. Twelve valence electrons, all paired ----------------------------------------------------------------------------
    beat(scene, t, 1)
    twelve = txt(f"{total} valence electrons, all paired", cfg.FONT["body"], cfg.WHITE).move_to([0, -2.4, 0])
    scene.play(Indicate(lewis.bonds, color=cfg.WHITE, scale_factor=1.15), run_time=1.0)
    scene.play(LaggedStart(*[Indicate(pair, color=cfg.CYAN, scale_factor=1.4) for pair in lewis.lone], lag_ratio=0.2),
               FadeIn(twelve), run_time=2.0)

    # --- 3. The magnet disagrees: move the electrons where they belong ------------------------------------------------------------
    beat(scene, t, 2)
    diagram = valence_diagram(o2.diagram.kind, "O", center=DIAGRAM_AT, ao_x=3.1)
    magnet_says = caption("The magnet says otherwise", cfg.GOLD)
    scene.play(fade_through(twelve, magnet_says), run_time=0.8)
    scene.remove(twelve)
    scene.play(lewis.animate.scale(0.5).move_to(LEWIS_AT), run_time=1.0)
    scene.play(FadeIn(diagram), run_time=0.8)

    # --- 4. Oxygen's ordering ----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    order = glow_frame(VGroup(diagram.level_group("s2p", links=False), diagram.level_group("p2p", links=False)), cfg.GOLD,
                       buff=0.14)
    order_word = caption("Oxygen's ordering: sigma 2p below the pi pair", cfg.GOLD)
    scene.play(Create(order), fade_through(magnet_says, order_word), run_time=1.0)
    scene.remove(magnet_says)
    scene.play(FadeOut(order), run_time=0.8)

    # --- 5. Let them in: the bond lines become electrons ------------------------------------------------------------------------------
    beat(scene, t, 4)
    bond_dots = lewis.bond_dots()
    scene.play(ReplacementTransform(lewis.bonds, bond_dots), FadeOut(order_word), run_time=1.0)
    dots = lewis.electron_dots(bond_dots)
    anims, arrows = fly_electrons(diagram, dots, o2, arc=-0.8)
    tally = counter(0, total).move_to([-5.45, -0.15, 0])
    tally_word = txt("placed", cfg.FONT["small"], cfg.MUTED).next_to(tally, DOWN, buff=0.2)
    scene.play(FadeIn(tally), FadeIn(tally_word), run_time=0.6)

    def advance(lo: int, hi: int, run_time: float = 1.8) -> None:
        scene.play(*anims[lo:hi], Transform(tally, counter(hi, total).move_to(tally)), run_time=run_time, lag_ratio=0.3)

    # --- 6. sigma 2s, sigma* 2s ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    advance(0, 2)
    advance(2, 4)

    # --- 7. sigma 2p -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    advance(4, 6, 1.4)

    # --- 8. The pi pair: ten so far ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    advance(6, 10, 2.2)
    same_ten = caption("Ten so far: the same ten as nitrogen", cfg.WHITE)
    scene.play(FadeIn(same_ten), run_time=0.6)

    # --- 9. Two left: the next level up is the pi* pair --------------------------------------------------------------------------------------
    beat(scene, t, 8)
    star_box = diagram.highlight("p2p*", cfg.GOLD)
    two_left = caption("Two left. Next level up: the pi* pair", cfg.GOLD)
    scene.play(fade_through(same_ten, two_left), Create(star_box), run_time=1.0)
    scene.remove(same_ten)
    scene.play(Indicate(VGroup(*dots[10:]), color=cfg.GOLD, scale_factor=1.6), run_time=1.2)

    # --- 10. Two degenerate orbitals, two electrons: Hund ------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    hund = VGroup(txt("Hund's rule:", cfg.FONT["body"], cfg.GOLD), txt("spread out,", cfg.FONT["small"], cfg.WHITE),
                  txt("spins parallel", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.12).move_to([-5.4, -2.25, 0])
    scene.play(FadeIn(hund, shift=UP * 0.15), FadeOut(two_left), run_time=1.0)

    # --- 11. The first goes into the first pi* orbital -------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    advance(10, 11, 1.6)

    # --- 12. The second does not pair: it takes the other orbital, spin parallel --------------------------------------------------------------------------
    beat(scene, t, 11)
    last = o2.electrons[11]
    hover = spin_arrow(-1, cfg.RED).move_to(diagram.slot(last.level, 0, -1) + UP * 1.0)
    scene.play(ReplacementTransform(dots[11], hover, path_arc=-0.6), run_time=1.4)
    scene.play(hover.animate.move_to(diagram.slot(last.level, 0, -1) + UP * 0.35), run_time=0.8)
    refuse = cross_mark(0.22).move_to(hover)
    scene.play(Create(refuse), run_time=0.5)
    scene.play(FadeOut(refuse), ReplacementTransform(hover, arrows[11], path_arc=0.5),
               Transform(tally, counter(total, total).move_to(tally)), run_time=1.6)
    scene.play(FadeOut(star_box), run_time=0.6)

    # --- 13. There they are -----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    lonely = [arrows[i] for i, p in enumerate(o2.electrons) if p in set(o2.unpaired_placements())]
    others = [a for a in arrows if a not in lonely]
    glows = VGroup(*[halo(0.55, cfg.GOLD, layers=6, peak_opacity=0.3).move_to(a) for a in lonely])
    scene.add(glows, *lonely)
    scene.play(diagram.animate.set_opacity(0.22), *[a.animate.set_opacity(0.22) for a in others], FadeOut(tally),
               FadeOut(tally_word), FadeOut(hund), FadeOut(lewis.letters), FadeOut(lewis.lone), FadeIn(glows), run_time=1.6)
    scene.play(*[a.animate.scale(1.35) for a in lonely], run_time=1.2)

    # --- 14. Two unpaired electrons in two pi* orbitals --------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    found = result_label(f"{o2.unpaired} unpaired\nelectrons", cfg.UNPAIRED, cfg.FONT["title"])
    found.move_to([-5.2, 0.9, 0])
    where = eq(r"\text{in } \pi^{*}_{2p}", cfg.FONT["section"], cfg.ANTIBONDING).next_to(found, DOWN, buff=0.35)
    anti_word = txt("antibonding", cfg.FONT["body"], cfg.ANTIBONDING).next_to(where, DOWN, buff=0.2)
    scene.play(FadeIn(found, scale=1.1), run_time=1.2)
    scene.play(FadeIn(where), FadeIn(anti_word), run_time=1.0)

    # --- 15. Two parallel spins: two tiny magnets ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    magnets = VGroup(*[bar_magnet().next_to(a, RIGHT, buff=0.15) for a in lonely])
    scene.play(LaggedStart(*[GrowFromCenter(m) for m in magnets], lag_ratio=0.4), run_time=1.4)
    same_way = caption("Two tiny magnets, pointing the same way", cfg.GOLD)
    scene.play(FadeIn(same_way), run_time=0.8)

    # --- 16. Paramagnetic: predicted ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    star_group = VGroup(glows, *lonely, magnets)
    scene.play(FadeOut(diagram), *[FadeOut(a) for a in others], FadeOut(found), FadeOut(where), FadeOut(anti_word),
               FadeOut(same_way), star_group.animate.scale(1.6).move_to([0, 1.6, 0]), run_time=1.2)
    para = result_label("PARAMAGNETIC", cfg.PARAMAGNETIC, cfg.FONT["hero"]).move_to([0, -0.5, 0])
    scene.play(FadeIn(para, scale=1.2), run_time=1.2)
    predicted = caption("Predicted by molecular orbital theory", cfg.GREEN)
    scene.play(FadeIn(predicted), run_time=0.8)

    # --- 17. The two pi* orbitals in 3D -----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 16)
    everything = [m for m in scene.mobjects if not getattr(m, "_is_project_background", False)]
    scene.play(*[FadeOut(m) for m in everything], run_time=1.0)
    scene.remove(*everything)
    stages = []
    for kind, x, pitch in (("py", -3.9, 0.3), ("pz", 3.9, 0.8)):
        st = Stage([x, -0.2, 0], zoom=0.5, yaw=0.45, pitch=pitch, sway=0.25)
        cloud = MOCloud(st, om.MOSpec(kind, -1.0, om.R_P), opacity=0.62)
        stage_nuclei(st, cloud)
        tag = Tag(VGroup(halo(0.55, cfg.GOLD, layers=5, peak_opacity=0.3), spin_arrow(1, cfg.UNPAIRED, 0.8)),
                  np.zeros(3), offset=np.array([0.0, -2.45, 0.0]))
        st.add_overlay(tag)
        stages.append(st)
    show(scene, stages[0], 1.0)
    show(scene, stages[1], 1.0)
    titles = VGroup(eq(r"\pi^{*}_{2p}", cfg.FONT["title"], cfg.ANTIBONDING).move_to([-3.9, 3.2, 0]),
                    eq(r"\pi^{*}_{2p}", cfg.FONT["title"], cfg.ANTIBONDING).move_to([3.9, 3.2, 0]))
    scene.play(FadeIn(titles), run_time=0.8)
    each = caption("Two pi* orbitals at right angles, one electron each", cfg.GOLD)
    scene.play(FadeIn(each), run_time=0.8)

    # --- 18. Lewis can't show them; the waves can't hide them -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 17)
    final = caption("Lewis couldn't show them. The waves can't hide them.", cfg.WHITE)
    scene.play(fade_through(each, final), run_time=1.0)
    scene.remove(each)
    scene.play(stages[1].rock(RIGHT, PI / 2), run_time=3.0, rate_func=there_and_back)
    scene.play(*stages[0].turn(yaw=1.2), *stages[1].turn(yaw=1.2), run_time=6.0, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
