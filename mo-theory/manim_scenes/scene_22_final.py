"""Chapter 22 — synthesis: from wave functions to observable chemistry.

Every picture here is one the film has already computed: the hanging liquid
oxygen (``physics_models.pour``), the sigma 1s pair (``orbital_models``), the
filled H2, N2 and O2 diagrams (``mo_models``), and a closing gallery of four
molecular orbitals.
"""

from manim_scenes.common import *
from manim_scenes.cryogenic_lab import CryogenicPour
from manim_scenes.scene_02_two_pictures import series_path
from manim_scenes.scene_20_boron_fluorine import compact


class Scene22Final(Scene):
    def construct(self) -> None:
        play_scene(self)


def compact_1s(key: str, x: float, y: float = 0.3, height: float = 3.2) -> tuple[MODiagram, list[VGroup]]:
    f = mo.fill(key)
    d = MODiagram(f.diagram, center=[x, y, 0], height=height, ao_x=1.0, mo_width=0.62, aos=False, axis=False)
    for label in d.labels.values():
        d.remove(label)
    return d, [arrow.scale(0.85) for arrow in d.electrons_for(f)]


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "22", "From waves to chemistry")

    # --- 1. The puzzle -----------------------------------------------------------------------------------------------------------
    lewis = LewisDiatomic("O", 2, 2, at=[-4.2, 0.6, 0], size=170, spacing=2.8)
    magnet = Electromagnet([3.8, 0.7, 0], scale=1.2)
    pour = CryogenicPour(magnet, drops=90, seed=cfg.SEED + 1, duration=8.0)
    pour.clock = pour.sim.duration + 3.0
    pour.apply_clock()
    # The recap begins after pouring: keep the glossy pool and its cold mist.
    pour.remove(pour.flask, pour.jet, pour.drops)
    pour.mist.remove(*[image for image, _, _, at_lip in pour.mist_specs if at_lip])
    pour.mist_specs = [spec for spec in pour.mist_specs if not spec[3]]
    scene.play(FadeIn(lewis), FadeIn(magnet), FadeIn(pour), magnet.field_on(), run_time=1.6)
    pour.run()
    dismiss_opening_title(scene, t, head, at=2.4)
    puzzle = caption("A double bond — and drawn into a magnet", cfg.WHITE)
    scene.play(FadeIn(puzzle), run_time=0.8)

    # --- 2. Stop tying electrons to fixed pairs --------------------------------------------------------------------------------------
    beat(scene, t, 1)
    pour.clear_updaters()
    scene.play(*[FadeOut(m) for m in (magnet, pour, puzzle)], lewis.animate.move_to([0, 0.4, 0]), run_time=1.0)
    cloud = VGroup(*[Ellipse(width=6.4 * f, height=2.6 * f, stroke_width=0, fill_color=cfg.DENSITY, fill_opacity=0.08)
                     for f in np.linspace(1.0, 0.35, 7)]).move_to([0, 0.4, 0])
    scene.play(FadeIn(cloud), lewis.bonds.animate.set_opacity(0), lewis.lone.animate.set_opacity(0.15), run_time=2.0)

    # --- 3. Atomic waves: bonding and antibonding ----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(lewis), FadeOut(cloud), run_time=0.7)
    left = Stage([-3.9, 0.2, 0], zoom=0.8, yaw=0.3, pitch=0.3, sway=0.25)
    right = Stage([3.9, 0.2, 0], zoom=0.8, yaw=0.3, pitch=0.3, sway=0.25)
    bond = MOCloud(left, om.MOSpec("s", 1.0, 4.4))
    anti = MOCloud(right, om.MOSpec("s", -1.0, 4.4))
    stage_nuclei(left, bond)
    stage_nuclei(right, anti)
    names = VGroup(txt("bonding", cfg.FONT["body"], cfg.BONDING).move_to([-3.9, -2.3, 0]),
                   txt("antibonding", cfg.FONT["body"], cfg.ANTIBONDING).move_to([3.9, -2.3, 0]))
    show(scene, left, 0.6)
    show(scene, right, 0.6)
    scene.play(bond.morph(R=om.R_S), anti.morph(R=om.R_S), FadeIn(names), run_time=3.0, rate_func=smooth)

    # --- 4. Where electrons sit decides everything ---------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    hide(scene, left, 0.5, FadeOut(names))
    hide(scene, right, 0.4)
    trio = []
    for key, x, maker in (("H2", -5.0, compact_1s), ("N2", 0.0, compact), ("O2", 5.0, compact)):
        d, arrs = maker(key, x)
        title = formula(key, cfg.FONT["section"]).move_to([x, 3.4, 0])
        order = txt(f"bond order {md.display_number(mo.bond_order(key))}", cfg.FONT["small"], cfg.GREEN).move_to([x, -2.45, 0])
        trio.append(VGroup(title, d, *arrs, order))
    scene.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in trio], lag_ratio=0.3), run_time=2.0)
    decides = caption("Where electrons sit: bond order, stability, magnetism", cfg.WHITE)
    scene.play(FadeIn(decides), run_time=0.8)

    # --- 5. Oxygen: two unpaired, exactly where Lewis couldn't show them --------------------------------------------------------------------------------
    beat(scene, t, 4)
    o2 = mo.fill("O2")
    oxygen = trio[2]
    lonely = [a for a, p in zip(oxygen[2:-1], o2.electrons) if p in set(o2.unpaired_placements())]
    glows = VGroup(*[halo(0.45, cfg.GOLD, layers=5, peak_opacity=0.32).move_to(a) for a in lonely])
    scene.play(trio[0].animate.set_opacity(0.25), trio[1].animate.set_opacity(0.25), FadeIn(glows), run_time=1.2)
    unpaired = caption("Two unpaired electrons, right where Lewis couldn't show them", cfg.GOLD)
    scene.play(fade_through(decides, unpaired), *[Indicate(a, color=cfg.WHITE, scale_factor=1.4) for a in lonely],
               run_time=1.4)
    scene.remove(decides)

    # --- 6. Shape, energy, occupancy -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[FadeOut(g) for g in trio], FadeOut(glows), FadeOut(unpaired), run_time=0.8)
    words = VGroup(result_label("shape", cfg.CYAN, cfg.FONT["title"]), result_label("energy", cfg.ANTIBONDING, cfg.FONT["title"]),
                   result_label("occupancy", cfg.GOLD, cfg.FONT["title"])).arrange(RIGHT, buff=1.0).move_to([0, 0.4, 0])
    for w in words:
        scene.play(FadeIn(w, shift=UP * 0.2), run_time=0.9)
        narration_wait(scene, 1.2)
    scene.play(Indicate(words[2], color=cfg.WHITE, scale_factor=1.12), run_time=1.2)

    # --- 7. A prediction of quantum mechanics ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    prediction = result_label("Not a mystery: a prediction", cfg.GREEN, cfg.FONT["section"]).move_to([0, -1.6, 0])
    scene.play(FadeIn(prediction, shift=UP * 0.2), run_time=1.0)

    # --- 8. Electron waves hold every molecule together: a gallery -----------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(words), FadeOut(prediction), run_time=0.8)
    specs = ((om.MOSpec("s", 1.0, om.R_S), r"\sigma_{1s}", cfg.BONDING, 0.7),
             (om.MOSpec("s", -1.0, om.R_S), r"\sigma^{*}_{1s}", cfg.ANTIBONDING, 0.7),
             (om.MOSpec("py", 1.0, om.R_P), r"\pi_{2p}", cfg.BONDING, 0.34),
             (om.MOSpec("py", -1.0, om.R_P), r"\pi^{*}_{2p}", cfg.ANTIBONDING, 0.34))
    gallery, labels = [], VGroup()
    for (spec, tex, color, zoom), x in zip(specs, (-5.55, -1.85, 1.85, 5.55)):
        st = Stage([x, 0.4, 0], zoom=zoom, yaw=0.4, pitch=0.35, spin=0.35)
        cloud = MOCloud(st, spec)
        stage_nuclei(st, cloud)
        st.presence = 0.0
        gallery.append(st)
        labels.add(eq(tex, cfg.FONT["section"], color).move_to([x, -1.9, 0]))
    for st in gallery:
        scene.add(st)
    scene.play(*[st.fade(st, 1.0) for st in gallery], LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.2), run_time=1.6)
    held = caption("Every molecule: electron waves spread over the whole molecule", cfg.CYAN)
    scene.play(FadeIn(held), run_time=0.8)

    # --- 9. The series: atomic orbitals to molecular orbitals ----------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    path = series_path(3).move_to([0, 0.3, 0])
    scene.play(*[st.fade(st, 0.0) for st in gallery], FadeOut(labels), FadeOut(held), run_time=1.0)
    for st in gallery:
        scene.remove(st)
    scene.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in path[0]], lag_ratio=0.35), Create(path[1]), run_time=2.4)
    deeper = caption("The same electrons. A deeper picture.", cfg.WHITE)
    scene.play(FadeIn(deeper), Indicate(path[0][3], color=cfg.GOLD, scale_factor=1.1), run_time=1.2)

    # --- 10. Bonds aren't sticks ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(path), FadeOut(deeper), run_time=0.8)
    heroes = []
    for kind, x, pitch in (("py", -3.4, 0.35), ("pz", 3.4, 0.75)):
        hero = Stage([x, 0.95, 0], zoom=0.36, yaw=0.45, pitch=pitch, spin=0.20)
        cloud = MOCloud(hero, om.MOSpec(kind, -1.0, om.R_P), opacity=0.66)
        stage_nuclei(hero, cloud, color=cfg.ELEMENT_COLORS["O"], radius=0.20)
        heroes.append(hero)
    orbital_names = VGroup(
        eq(r"\pi^{*}_{2p_y}", cfg.FONT["body"], cfg.ANTIBONDING).move_to([-3.4, 3.0, 0]),
        eq(r"\pi^{*}_{2p_z}", cfg.FONT["body"], cfg.ANTIBONDING).move_to([3.4, 3.0, 0]),
    )
    line_one = txt("Bonds aren't sticks.", cfg.FONT["title"], cfg.WHITE).move_to([0, -2.1, 0])
    line_two = txt("They're quantum states.", cfg.FONT["title"], cfg.CYAN).move_to([0, -3.05, 0])
    for hero in heroes:
        hero.presence = 0.0
        scene.add(hero)
    scene.play(*[hero.fade(hero, 1.0) for hero in heroes], FadeIn(line_one), FadeIn(orbital_names), run_time=1.2)
    scene.play(FadeIn(line_two, shift=UP * 0.15), run_time=1.0)

    # --- 11. And sometimes, a little magnetic -----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    spins = VGroup(*[VGroup(halo(0.5, cfg.GOLD, layers=5, peak_opacity=0.3), spin_arrow(1, cfg.UNPAIRED, 0.9))
                     for _ in range(2)])
    for mark, x in zip(spins, (-3.4, 3.4)):
        mark.move_to([x, -1.1, 0])
    magnetic = txt("…and sometimes, a little bit magnetic.", cfg.FONT["body"], cfg.GOLD).move_to([0, -3.05, 0])
    scene.play(FadeIn(spins, scale=0.6), fade_through(line_two, magnetic), run_time=1.4)
    scene.remove(line_two)
    for _ in range(6):
        scene.play(spins.animate.scale(1.15), run_time=2.4, rate_func=there_and_back)
    scene.play(*[hero.set_spin(0.12) for hero in heroes], run_time=5.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["22"])
