"""Chapter 02 — Lewis structures are flat; methane is not.

A quick callback to Part 1 (the energy valley, sigma and pi overlap), then the
Lewis vocabulary, then methane drawn as the flat cross a Lewis structure
suggests. The 3D model takes over at the same positions, turns edge-on (the
cross collapses to a line), and the four bonds lift into a tetrahedron while
a live arc reads the angle going from 90 to 109.5 degrees.
"""

from manim_scenes.common import *

CENTER = np.array([0.0, 0.2, 0.0])
LEWIS_BOND = 2.3
# A tetrahedron that grows straight out of the flat cross: the left/right pair
# tilts toward the viewer, the up/down pair tilts away (cos = -1/3 between all).
A, B = np.sqrt(2 / 3), np.sqrt(1 / 3)
TETRA_FROM_CROSS = [np.array(v) for v in ([A, 0, B], [0, A, -B], [-A, 0, B], [0, -A, -B])]


class Scene02LewisIsFlat(Scene):
    def construct(self) -> None:
        play_scene(self)


def energy_valley(width: float = 3.6, height: float = 2.2) -> VGroup:
    """A schematic Morse-shaped energy curve with the gold ball at its bottom."""
    xs = np.linspace(0.32, 3.2, 120)
    ys = (1 - np.exp(-1.9 * (xs - 0.9))) ** 2 - 1
    pts = [np.array([x / 3.2 * width - width / 2, max(min(y, 0.9), -1.0) * height / 1.9, 0]) for x, y in zip(xs, ys)]
    curve = VMobject(stroke_color=cfg.GOLD, stroke_width=6).set_points_smoothly(pts)
    bottom = pts[int(np.argmin([p[1] for p in pts]))]
    ball = VGroup(Circle(radius=0.17, stroke_width=0, fill_color=cfg.GOLD, fill_opacity=1),
                  Circle(radius=0.07, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.7).shift(UL * 0.05))
    ball.move_to(bottom + UP * 0.17)
    return VGroup(curve, ball)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "Lewis structures are flat")

    # --- 1. Last time: bonds lower the energy; orbitals overlap -------------------------------------
    valley = energy_valley().move_to([-4.8, 0.5, 0])
    sigma_stage = Stage([0, 0.4, 0], zoom=1.35, pitch=0.25, sway=0.2)
    for x in (-0.55, 0.55):
        hydrogen_orbital(sigma_stage, [x, 0, 0], units=0.62, opacity=0.6)
        sigma_stage.add_body(element_ball("H", [x, 0, 0], scale=0.7))
    pi_stage = Stage([4.8, 0.4, 0], zoom=1.3, yaw=0.35, pitch=0.2, sway=0.2)
    for x in (-0.55, 0.55):
        p_orbital(pi_stage, [x, 0, 0], [0, 1, 0], units=0.38, opacity=0.7)
        pi_stage.add_body(element_ball("C", [x, 0, 0], scale=0.55, label=False))
    tags = VGroup(chip("lower energy", cfg.GOLD, cfg.FONT["label"]).move_to([-4.8, -1.9, 0]),
                  eq_chip(r"\sigma", cfg.SIGMA_COLOR, cfg.FONT["body"]).move_to([0, -1.9, 0]),
                  eq_chip(r"\pi", cfg.PI_COLOR, cfg.FONT["body"]).move_to([4.8, -1.9, 0]))
    recap = caption("Last time: why atoms bond", cfg.CYAN)
    scene.play(Create(valley[0]), FadeIn(valley[1], scale=0.5), FadeIn(recap), run_time=1.6)
    show(scene, sigma_stage, 1.0, FadeIn(tags[0]))
    show(scene, pi_stage, 1.0, FadeIn(tags[1:]))
    dismiss_opening_title(scene, t, head)
    scene.play(valley[1].animate.shift(UP * 0.02), run_time=1.0)

    # --- 2. The Lewis vocabulary ---------------------------------------------------------------------------
    beat(scene, t, 1)
    hide(scene, sigma_stage, 0.6, FadeOut(valley), FadeOut(tags), FadeOut(recap))
    hide(scene, pi_stage, 0.4)
    water = Lewis("O", [("H", 200, 1), ("H", 340, 1)], central_lone=[60, 120], at=[0, 0.6, 0], bond=2.6)
    scene.play(Write(water), run_time=1.6)
    notes = VGroup(
        txt("atom", cfg.FONT["body"], cfg.WHITE).next_to(water.ligand_symbols[0], DOWN, buff=0.5),
        txt("shared pair", cfg.FONT["body"], cfg.CYAN).next_to(water.bond_lines[1], DOWN, buff=0.9),
        txt("lone pair", cfg.FONT["body"], cfg.PURPLE).next_to(water.lone_dots, UP, buff=0.4),
    )
    for note, target in zip(notes, (water.ligand_symbols[0], water.bond_lines[1], water.lone_dots)):
        scene.play(FadeIn(note, shift=UP * 0.1), Indicate(target, color=note.get_color(), scale_factor=1.25),
                   run_time=1.1)

    # --- 3. Methane, drawn as a flat cross -----------------------------------------------------------------
    beat(scene, t, 2)
    methane = Lewis("C", [("H", 0, 1), ("H", 90, 1), ("H", 180, 1), ("H", 270, 1)], at=CENTER, bond=LEWIS_BOND,
                    size=100, ligand_size=84)
    name = formula("CH4", cfg.FONT["section"]).move_to([5.2, 2.5, 0])
    scene.play(FadeOut(water), FadeOut(notes), run_time=0.7)
    scene.play(Write(methane), FadeIn(name), run_time=1.8)

    # --- 4. Excellent bookkeeping --------------------------------------------------------------------------------
    beat(scene, t, 3)
    books = VGroup(chip("4 bonds", cfg.CYAN), chip("8 electrons", cfg.CYAN)).arrange(DOWN, buff=0.25)
    books.move_to([-4.9, 0.2, 0])
    scene.play(LaggedStart(*[Indicate(b, color=cfg.CYAN, scale_factor=1.3) for b in methane.bond_lines],
                           lag_ratio=0.25), FadeIn(books[0], shift=RIGHT * 0.2), run_time=1.8)
    scene.play(FadeIn(books[1], shift=RIGHT * 0.2), run_time=0.8)

    # --- 5. Is it really flat, ninety degrees apart? --------------------------------------------------------------
    beat(scene, t, 4)
    corners = VGroup()
    for angle in (45, 135, 225, 315):
        d = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0])
        square = Square(side_length=0.3, stroke_color=cfg.GOLD, stroke_width=4).rotate(np.radians(angle - 45))
        corners.add(square.move_to(CENTER + d * 0.82))
    ninety = degrees_label(90, cfg.FONT["section"]).move_to(CENTER + np.array([1.55, 1.5, 0]))
    flat = caption("Flat, with bonds 90° apart?", cfg.GOLD)
    scene.play(FadeOut(books), LaggedStart(*[Create(c) for c in corners], lag_ratio=0.2), FadeIn(ninety),
               FadeIn(flat), run_time=1.8)

    # --- 6. Turn the flat version on its side ------------------------------------------------------------------------
    beat(scene, t, 5)
    stage = Stage(CENTER, zoom=1.0)
    model = MoleculeModel(stage, ml.molecule("CH4"), bond=LEWIS_BOND, labels=True)
    for i, d in enumerate((RIGHT, UP, LEFT, DOWN)):
        model.dirs[i] = d.astype(float)
    stage.presence = 0.0
    stage.refresh()
    scene.add(stage)
    scene.play(FadeOut(methane), FadeOut(corners), FadeOut(ninety), stage.fade(stage, 1.0), run_time=1.2)
    edge = caption("Edge on, a flat cross is just a line", cfg.WHITE)
    swap(scene, flat, edge)
    scene.play(*stage.turn(pitch=np.pi / 2 - 0.02), run_time=2.4, rate_func=smooth)
    scene.play(Wiggle(edge, scale_value=1.04), run_time=1.0)

    # --- 7. The real molecule spreads into 3D ----------------------------------------------------------------------------
    beat(scene, t, 6)
    arc = model.arc(0, 1, radius=1.15, live=True, label_gap=0.6, size=cfg.FONT["body"])
    scene.play(*stage.turn(yaw=0.45, pitch=0.42), run_time=1.8, rate_func=smooth)
    scene.play(stage.fade(arc, 1.0), FadeOut(edge), run_time=0.6)
    stage.sway = 0.15
    scene.play(*[model.aim(i, d) for i, d in enumerate(TETRA_FROM_CROSS)], run_time=3.6, rate_func=smooth)

    # --- 8. A tetrahedron, 109.5 degrees ------------------------------------------------------------------------------------
    beat(scene, t, 7)
    faces = [Face([model._site_point(a), model._site_point(b), model._site_point(c)], cfg.CYAN, 0.08, 0.4)
             for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))]
    for face in faces:
        face.presence = 0.0
    stage.add_body(*faces)
    wider = caption("Tetrahedron · wider than 90°", cfg.GOLD)
    scene.play(*[stage.fade(f, 1.0) for f in faces], FadeIn(wider), run_time=1.4)
    scene.play(stage.set_spin(0.35), run_time=1.0)
    scene.play(Indicate(wider, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)

    # --- 9. Connections versus shape -----------------------------------------------------------------------------------------
    beat(scene, t, 8)
    small = Lewis("C", [("H", 0, 1), ("H", 90, 1), ("H", 180, 1), ("H", 270, 1)], at=[-4.4, 0.3, 0], bond=1.5,
                  size=72, ligand_size=60)
    labels = VGroup(chip("connections", cfg.WHITE, cfg.FONT["label"]).move_to([-4.4, -2.3, 0]),
                    chip("shape", cfg.GREEN, cfg.FONT["label"]).move_to([2.6, -2.75, 0]))
    scene.play(FadeOut(wider), *[stage.fade(f, 0.0) for f in faces], stage.glide([2.6, 0.25, 0]),
               FadeIn(small), FadeIn(labels[0]), run_time=1.4)
    scene.play(FadeIn(labels[1], scale=1.1), run_time=0.8)

    # --- 10. Electrons take up space ----------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    space = caption("Electrons take up space", cfg.CYAN)
    scene.play(FadeOut(small), FadeOut(labels), FadeOut(name), stage.glide(CENTER), stage.zoom_to(1.05),
               stage.fade(arc, 0.0), run_time=1.4)
    scene.play(*model.fade("domains", 1.0), FadeIn(space), run_time=2.0)
    scene.play(stage.set_spin(0.2), run_time=1.5)
    scene.play(*stage.turn(pitch=0.22), run_time=2.6, rate_func=smooth)
    scene.play(Indicate(space, color=cfg.WHITE, scale_factor=1.04), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
