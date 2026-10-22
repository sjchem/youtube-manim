"""Chapter 16 — two models, one molecule: what hybridization does and doesn't say.

Ammonia and water shown with clear bond skeletons and compact purple
lone-pair hybrid lobes. The lobes clear before angles are compared.
Ideal sp3 would give 109.5 degrees; the measured
angles (``geometry_data``) are smaller, so hybrid labels do not produce the
angles. Then the two models side by side, and a note that sp3d / sp3d2 are
historical textbook labels rather than literal d-orbital explanations.
"""

from manim_scenes.common import *

UNITS = 0.30


class Scene16TwoModels(Scene):
    def construct(self) -> None:
        play_scene(self)


def hybrid_picture(key: str, at) -> tuple[Stage, MoleculeModel, list[Orbital]]:
    """Keep the bond skeleton clear; use only compact lone-pair hybrid lobes."""
    spec = ml.molecule(key)
    # A shallow pyramid view keeps ammonia's third hydrogen below nitrogen,
    # away from its lone pair. Water uses the familiar bent orientation.
    orient = np.eye(3) if key == "NH3" else bisect_down(spec.sites[2].direction, spec.sites[3].direction)
    stage = Stage(at, zoom=1.05, yaw=0.45, pitch=0.12, sway=0.12)
    model = MoleculeModel(stage, spec, orient=orient, lone_pairs=False, bond=2.2)
    lone_hybrids = []
    for i in model.lone():
        orbital = Orbital(stage, ORIGIN, model._dir(i), om.SP_ALPHA["sp3"], units=UNITS,
                          plus=cfg.LONE_PAIR_COLOR, opacity=0.50)
        # Full hybrid sets were shown in the preceding scene. Here only the
        # large lone-pair lobes are needed; small back lobes obscure N and O.
        orbital.minus.presence = 0.0
        lone_hybrids.append(orbital)
    stage.presence = 0.0
    stage.refresh()
    return stage, model, lone_hybrids


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "Two models, one molecule")

    # --- 1. Ammonia and water, the sp3 way ---------------------------------------------------------------------------
    pictures = [hybrid_picture(key, [x, 0.95, 0]) for key, x in (("NH3", -3.8), ("H2O", 3.8))]
    names = VGroup(*[VGroup(formula(key, cfg.FONT["section"]), eq(r"sp^3", cfg.FONT["body"], cfg.BLUE)).arrange(RIGHT, buff=0.4)
                     .move_to([x, -1.75, 0]) for key, x in (("NH3", -3.8), ("H2O", 3.8))])
    for stage, _, _ in pictures:
        scene.add(stage)
    scene.play(*[s.fade(s, 1.0) for s, _, _ in pictures], FadeIn(names), run_time=1.4)
    dismiss_opening_title(scene, t, head)

    # --- 2. Useful, not the whole story --------------------------------------------------------------------------------
    beat(scene, t, 1)
    useful = caption("A useful picture. Not the whole story.", cfg.WHITE)
    scene.play(FadeIn(useful), run_time=0.9)

    # --- 3. Ideal sp3 vs measured ----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    # One shared benchmark leaves both molecule labels and measured angles
    # a clear area below the structures.
    ideal = VGroup(txt(f"ideal sp³: {pm.TETRAHEDRAL_DEG:.1f}°", cfg.FONT["body"], cfg.MUTED)
                   .move_to([0, 3.25, 0]))
    arcs = []
    for (stage, model, _), key in zip(pictures, ("NH3", "H2O")):
        arc = model.arc(2, 3, radius=1.0, label=degrees_label(gd.BOND_ANGLE_DEG[key], cfg.FONT["body"]),
                        label_gap=0.5)
        arcs.append((stage, arc))
    # Clear all orbital surfaces and settle each measured bond pair face-on.
    # This is an angle comparison, so the atoms and gold arcs take priority.
    settle = []
    for stage, model, lone_hybrids in pictures:
        stage.sway = 0.0
        settle += [stage.fade(orbital.plus, 0.0) for orbital in lone_hybrids]
        settle += [stage.align(bisect_down(model.dirs[2], model.dirs[3])),
                   *stage.turn(yaw=0.0, pitch=0.0)]
    scene.play(FadeOut(useful), FadeIn(ideal), *settle, run_time=0.9)
    scene.play(*[stage.fade(arc, 1.0) for stage, arc in arcs], run_time=1.2)
    strikes = VGroup(*[Line(i.get_left() + LEFT * 0.05, i.get_right() + RIGHT * 0.05, stroke_color=cfg.RED, stroke_width=6)
                       for i in ideal])
    scene.play(Create(strikes), run_time=0.9)
    labels_note = caption("Hybrid labels don't produce the measured angles", cfg.GOLD)
    scene.play(FadeIn(labels_note), run_time=0.8)

    # --- 4. Water's real orbitals are more nuanced --------------------------------------------------------------------------
    beat(scene, t, 3)
    nuanced = caption("Water's real orbitals: not four identical hybrids", cfg.WHITE)
    scene.play(fade_through(labels_note, nuanced), Indicate(names[1], color=cfg.GOLD, scale_factor=1.05), run_time=1.2)
    scene.remove(labels_note)

    # --- 5-6. Two models, two jobs ----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    for stage, _, _ in pictures:
        stage.clear_updaters()
    scene.play(*[FadeOut(s) for s, _, _ in pictures], FadeOut(VGroup(names, ideal, strikes, nuanced)), run_time=0.9)
    for stage, _, _ in pictures:
        scene.remove(stage)
    heads = VGroup(txt("VSEPR", cfg.FONT["section"], cfg.CYAN), txt("Hybridization", cfg.FONT["section"], cfg.BLUE))
    left_rows = VGroup(*[txt(s, cfg.FONT["body"], cfg.WHITE) for s in
                         ("predicts shape", "bonds + lone pairs")])
    right_rows = VGroup(*[txt(s, cfg.FONT["body"], cfg.WHITE) for s in
                          ("describes orbitals", "σ overlap + p for π")])
    for col, x in ((VGroup(heads[0], *left_rows), -3.7), (VGroup(heads[1], *right_rows), 3.7)):
        col.arrange(DOWN, buff=0.45).move_to([x, 0.6, 0])
    divider = Line([0, 2.6, 0], [0, -1.6, 0], stroke_color=cfg.MUTED, stroke_width=3)
    scene.play(FadeIn(heads[0], shift=DOWN * 0.1), Create(divider), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in left_rows], lag_ratio=0.35), run_time=2.0)
    beat(scene, t, 5)
    scene.play(FadeIn(heads[1], shift=DOWN * 0.1), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.15) for r in right_rows], lag_ratio=0.35), run_time=2.0)

    # --- 7. sp3d and sp3d2: textbook labels ---------------------------------------------------------------------------------------
    beat(scene, t, 6)
    table = VGroup(heads, left_rows, right_rows, divider)
    scene.play(table.animate.move_to([0, 1.3, 0]), run_time=1.0)
    old = VGroup(VGroup(eq(r"sp^3d", cfg.FONT["section"], cfg.MUTED), txt("5 regions", cfg.FONT["body"], cfg.MUTED)),
                 VGroup(eq(r"sp^3d^2", cfg.FONT["section"], cfg.MUTED), txt("6 regions", cfg.FONT["body"], cfg.MUTED)))
    for row in old:
        row.arrange(RIGHT, buff=0.5)
    old.arrange(RIGHT, buff=1.6).move_to([0, -1.75, 0])
    scene.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in old], lag_ratio=0.4), run_time=1.6)

    # --- 8. Historical labels; d orbitals play a minor part --------------------------------------------------------------------------
    beat(scene, t, 7)
    tag = chip("historical textbook labels", cfg.MUTED, cfg.FONT["label"]).move_to([0, -2.75, 0])
    minor = caption("Modern calculations: d orbitals play only a minor part", cfg.WHITE)
    scene.play(FadeIn(tag, shift=UP * 0.1), run_time=0.9)
    scene.play(FadeIn(minor), Indicate(old, color=cfg.WHITE, scale_factor=1.03), run_time=1.4)
    scene.play(Indicate(heads[0], color=cfg.WHITE, scale_factor=1.06), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
