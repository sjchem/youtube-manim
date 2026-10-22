"""Chapter 03 — electron regions push apart, and find the arrangements themselves.

Every motion of the lobes here is a real relaxation path from
``physics_models.relax``: unit vectors on a sphere under a 1/d repulsion,
following the gradient flow. Two regions open to 180 degrees, three to 120,
and a fourth dropped onto the flattened triangle folds it into a tetrahedron.
The energy plot is the computed total repulsion along a path from a seeded
random start, so the curve on screen is the curve the model actually follows.
"""

from manim_scenes.common import *

CENTER = np.array([-0.2, -0.3, 0.0])


class Scene03RegionsRepel(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "03", "Electron regions push apart")

    # --- 1. A central atom; bonds and lone pairs are both regions ------------------------------------
    stage = Stage(CENTER, zoom=1.25, pitch=0.12, sway=0.1)
    regions = RegionModel(stage, np.zeros((0, 3)))
    show(scene, stage, 1.0)
    legend = VGroup(
        VGroup(Ellipse(width=0.9, height=0.42, stroke_color=cfg.CYAN, stroke_width=3, fill_color=cfg.CYAN,
                       fill_opacity=0.3), txt("bond", cfg.FONT["body"], cfg.CYAN)).arrange(RIGHT, buff=0.3),
        VGroup(Ellipse(width=0.8, height=0.55, stroke_color=cfg.PURPLE, stroke_width=3, fill_color=cfg.PURPLE,
                       fill_opacity=0.3), txt("lone pair", cfg.FONT["body"], cfg.PURPLE)).arrange(RIGHT, buff=0.3),
    ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([-5.2, 1.0, 0])
    both = txt("= one region each", cfg.FONT["body"], cfg.WHITE).next_to(legend, DOWN, buff=0.45)
    dismiss_opening_title(scene, t, head, at=2.4)
    scene.play(FadeIn(legend[0], shift=RIGHT * 0.2), run_time=0.9)
    scene.play(FadeIn(legend[1], shift=RIGHT * 0.2), run_time=0.9)
    scene.play(FadeIn(both), run_time=0.8)

    # --- 2. Two regions, squeezed together ------------------------------------------------------------------
    beat(scene, t, 1)
    first = regions.add_region(pm.RELAXATION_STARTS[2][0])
    second = regions.add_region(pm.RELAXATION_STARTS[2][1])
    repel = caption("Regions repel", cfg.RED)
    scene.play(regions.grow(first), regions.grow(second), FadeOut(legend), FadeOut(both), FadeIn(repel),
               run_time=1.6)
    push = Vector(regions.tip(0, 1.08), regions.tip(1, 1.08), cfg.RED, width=0.07, tip=0.22)
    push_back = Vector(regions.tip(1, 1.08), regions.tip(0, 1.08), cfg.RED, width=0.07, tip=0.22)
    for arrow in (push, push_back):
        arrow.presence = 0.0
        stage.add_overlay(arrow)
    scene.play(stage.fade(push, 1.0), stage.fade(push_back, 1.0), run_time=0.8)
    scene.play(*stage.turn(yaw=0.25), run_time=2.2, rate_func=there_and_back)

    # --- 3. They open to 180 degrees ----------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(regions.play_path(pm.settle(regions.dirs)), stage.fade(push, 0.0), stage.fade(push_back, 0.0),
               run_time=2.8, rate_func=smooth)
    line_arc = regions.arc(0, 1, radius=1.05, label=degrees_label(180, cfg.FONT["body"]), label_gap=0.55)
    scene.play(stage.fade(line_arc, 1.0), FadeOut(repel), run_time=0.9)
    two_cap = caption("Two regions: linear", cfg.GREEN)
    scene.play(FadeIn(two_cap), run_time=0.7)

    # --- 4. A third region ------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    third = regions.add_region(UP)
    scene.play(regions.grow(third), stage.fade(line_arc, 0.0), FadeOut(two_cap), run_time=1.4)
    scene.play(regions.play_path(pm.settle(regions.dirs)), run_time=3.0, rate_func=smooth)

    # --- 5. 120 degrees, one flat plane -------------------------------------------------------------------------------
    beat(scene, t, 4)
    arcs = [regions.arc(i, j, radius=1.0, label=degrees_label(120, cfg.FONT["label"]), label_gap=0.5)
            for i, j in ((2, 0), (0, 1), (1, 2))]
    planar = caption("Three regions: trigonal planar", cfg.GREEN)
    scene.play(*[stage.fade(a, 1.0) for a in arcs], FadeIn(planar), run_time=1.2)
    scene.play(*stage.turn(yaw=0.5), run_time=2.4, rate_func=there_and_back)

    # --- 6. Lay the triangle flat; drop a fourth on top ------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[stage.fade(a, 0.0) for a in arcs], FadeOut(planar), run_time=0.6)
    scene.play(regions.rigid_turn(mu.rotation_x(-np.pi / 2)), *stage.turn(pitch=0.42, yaw=0.3), run_time=2.2,
               rate_func=smooth)
    fourth = regions.add_region(UP)
    scene.play(regions.grow(fourth), run_time=1.2)

    # --- 7. The umbrella closes ----------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    umbrella = caption("The three fold down", cfg.CYAN)
    scene.play(FadeIn(umbrella), run_time=0.5)
    scene.play(regions.play_path(pm.settle(regions.dirs)), run_time=4.0, rate_func=smooth)
    tetra_arc = regions.arc(3, 0, radius=1.0, label=degrees_label(round(pm.TETRAHEDRAL_DEG, 1), cfg.FONT["body"]),
                            label_gap=0.85)
    scene.play(stage.fade(tetra_arc, 1.0), run_time=0.8)

    # --- 8. A tetrahedron, found by the repulsion ---------------------------------------------------------------------------
    beat(scene, t, 7)
    faces = [Face([regions.tip(a), regions.tip(b), regions.tip(c)], cfg.CYAN, 0.07, 0.45)
             for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))]
    for face in faces:
        face.presence = 0.0
    stage.add_body(*faces)
    tetra = caption("Four regions: tetrahedral", cfg.GREEN)
    scene.play(*[stage.fade(f, 1.0) for f in faces], stage.fade(tetra_arc, 0.0), fade_through(umbrella, tetra),
               run_time=1.2)
    scene.remove(umbrella)
    scene.play(stage.set_spin(0.45), run_time=1.0)
    scene.play(Indicate(tetra, color=cfg.WHITE, scale_factor=1.05), run_time=1.4)

    # --- 9. A computer model: points on a sphere that repel -------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(*[stage.fade(f, 0.0) for f in faces], stage.set_spin(0.0), stage.glide([-3.4, 0.0, 0]),
               stage.zoom_to(1.0), FadeOut(tetra), run_time=1.2)
    rng = np.random.default_rng(cfg.SEED)
    scrambled = np.array([mu.unit(v) for v in rng.normal(size=(4, 3))])
    scene.play(*[regions.aim(i, d) for i, d in enumerate(scrambled)], run_time=1.0)
    path = pm.settle(regions.dirs, count=160)
    energies = np.array([pm.repulsion_energy(frame) for frame in path])
    box = (np.array([1.6, -1.6, 0]), np.array([6.6, 1.9, 0]))
    xs = np.linspace(box[0][0], box[1][0], len(path))
    ys = mu.linear_map(energies, (energies.min(), energies.max()), (box[0][1] + 0.3, box[1][1] - 0.2))
    axes = VGroup(Line(box[0], [box[0][0], box[1][1], 0], stroke_color=cfg.MUTED, stroke_width=3),
                  Line(box[0], [box[1][0], box[0][1], 0], stroke_color=cfg.MUTED, stroke_width=3))
    curve = VMobject(stroke_color=cfg.GOLD, stroke_width=6).set_points_smoothly(
        [np.array([x, y, 0]) for x, y in zip(xs, ys)])
    y_label = txt("total repulsion", cfg.FONT["small"], cfg.GOLD).next_to(axes[0], UP, buff=0.2).align_to(axes[0], LEFT)
    x_label = txt("settling", cfg.FONT["small"], cfg.MUTED).next_to(axes[1], DOWN, buff=0.2)
    model_note = caption("A model: points on a sphere that repel", cfg.WHITE)
    scene.play(Create(axes), FadeIn(y_label), FadeIn(x_label), FadeIn(model_note), run_time=1.0)
    scene.play(regions.play_path(path, rate_func=linear), Create(curve, rate_func=linear), run_time=4.0)
    lowest = Dot(curve.get_end(), radius=0.11, color=cfg.GOLD)
    scene.play(FadeIn(lowest, scale=0.4), Flash(lowest, color=cfg.GOLD), run_time=0.8)

    # --- 10. VSEPR --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    words = VGroup(*[txt(w, cfg.FONT["section"], cfg.WHITE) for w in ("Valence", "Shell", "Electron", "Pair", "Repulsion")])
    words.arrange(RIGHT, buff=0.32).move_to([0, 0.2, 0])
    fit_width(words, 13.6)
    for word in words:
        word[0].set_color(cfg.GOLD)
    acronym = txt("VSEPR", cfg.FONT["hero"], cfg.GOLD).move_to([0, -1.6, 0])
    hide(scene, stage, 0.8, FadeOut(axes), FadeOut(curve), FadeOut(lowest), FadeOut(y_label), FadeOut(x_label),
         FadeOut(model_note))
    scene.play(LaggedStart(*[FadeIn(w, shift=UP * 0.15) for w in words], lag_ratio=0.18), run_time=1.6)
    scene.play(Indicate(VGroup(*[w[0] for w in words]), color=cfg.WHITE, scale_factor=1.25), run_time=0.8)
    scene.play(FadeIn(acronym, shift=UP * 0.2), run_time=0.6)

    # --- 11. Count the regions; the arrangement follows -------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(words), run_time=0.4)
    scene.play(acronym.animate.scale(0.6).move_to([0, 3.3, 0]), run_time=0.6)
    trio = VGroup()
    names = ("linear", "trigonal planar", "tetrahedral")
    stages = []
    for k, n in enumerate((2, 3, 4)):
        x = (k - 1) * 4.7
        small = Stage([x, 0.45, 0], zoom=0.9, yaw=0.15 if n == 2 else 0.4, pitch=0.3, spin=0.25 if n > 2 else 0.0, sway=0.2)
        RegionModel(small, pm.ideal_directions(n))
        stages.append(small)
        trio.add(VGroup(txt(str(n), cfg.FONT["section"], cfg.WHITE), shape_name(names[k], size=cfg.FONT["body"]))
                 .arrange(DOWN, buff=0.28).move_to([x, -2.5, 0]))
    for small in stages:
        small.presence = 0.0
        scene.add(small)
    scene.play(*[s.fade(s, 1.0) for s in stages], LaggedStart(*[FadeIn(g, shift=UP * 0.15) for g in trio],
                                                               lag_ratio=0.3), run_time=2.0)
    scene.play(LaggedStart(*[Indicate(g[1], color=cfg.WHITE, scale_factor=1.06) for g in trio], lag_ratio=0.35),
               run_time=2.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
