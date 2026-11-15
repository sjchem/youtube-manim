"""Scene 09 — the cross product. On a turning 3D stage a rod is pinned at a
pivot and a force arrow rotates at its tip: the turning depends on where and
in which direction. The rod becomes vector A and the force vector B, lying in
a horizontal plane. Their parallelogram fills with purple; its area is
A B sin(theta). A x B rises perpendicular to the plane; a curled cyan arrow
from A toward B and the "thumb" show the right-hand rule. The angle sweeps:
at 90 degrees the parallelogram and cross product peak; at 0 and 180 both vanish.
Finally B x A appears, pointing straight down: -A x B.
"""

from manim_scenes.common import *

A_LEN, B_LEN = 2.6, 2.0
C_SCALE = 0.42              # screen length of A x B per unit area


class Scene09CrossProduct(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "09", "The cross product")
    stage = Stage((1.2, -1.35, 0.0), zoom=1.1, yaw=-0.55, pitch=0.42, sway=0.04)
    theta = Knob(np.radians(55))
    O = np.zeros(3)

    def A() -> np.ndarray:
        return np.array([A_LEN, 0.0, 0.0])

    def B() -> np.ndarray:
        return B_LEN * np.array([np.cos(theta.value), 0.0, -np.sin(theta.value)])

    def C() -> np.ndarray:
        return np.cross(A(), B()) * C_SCALE

    plane = Grid((0.4, 0.0, -0.6), (1, 0, 0), (0, 0, 1), (-3.2, 3.2), (-2.6, 2.6), step=0.5, major=4, color=cfg.GRID,
                 opacity=0.35, fill=cfg.PANEL_2, fill_opacity=0.35)
    stage.add_body(plane)

    # --- 1. Where a force acts, and which way ---------------------------------------------------------------------
    pivot = Ball(O, 0.14, cfg.STEEL, layers=12)
    tip = Ball(A(), 0.08, cfg.STEEL, layers=8)
    rod = Rod(pivot, tip, width=16, dark="#4A5A68", light="#DCE6EE")
    push_dir = Knob(np.radians(120))
    force = Vector(A, lambda: A() + 1.6 * np.array([np.cos(push_dir.value), 0.0, -np.sin(push_dir.value)]), cfg.FORCE,
                   width=0.09, tip=0.3)
    stage.add_body(rod, pivot, tip)
    stage.add_overlay(force)
    show(scene, stage, 1.0)
    chips = VGroup(chip("where it acts", cfg.POSITION), chip("which way it points", cfg.FORCE)).arrange(RIGHT, buff=0.8)
    chips.move_to(UP * 3.0)
    scene.play(FadeIn(chips[0], shift=DOWN * 0.1), run_time=0.7)
    scene.play(push_dir.to(stage, np.radians(20)), FadeIn(chips[1], shift=DOWN * 0.1), run_time=2.0)
    scene.play(push_dir.to(stage, np.radians(90)), *stage.turn(yaw=-0.3), run_time=2.0)

    # --- 2. A new product ------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    name = result_label("the cross product", cfg.TORQUE, cfg.FONT["section"]).move_to(UP * 3.0)
    scene.play(fade_through(chips, name), run_time=1.0)

    # --- 3. A and B, angle theta ---------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    vA = Vector(O, A, cfg.CYAN, width=0.09, tip=0.3)
    vB = Vector(O, B, cfg.GOLD, width=0.09, tip=0.3)
    labA = Tag(eq(r"\vec A", cfg.FONT["section"], cfg.CYAN), lambda: A() * 1.08, DOWN * 0.35 + RIGHT * 0.25)
    labB = Tag(eq(r"\vec B", cfg.FONT["section"], cfg.GOLD), lambda: B() * 1.12, UP * 0.5 + RIGHT * 0.2)
    arc = Curve(lambda: np.array([0.7 * np.array([np.cos(a), 0, -np.sin(a)]) for a in np.linspace(0, theta.value, 24)]),
                cfg.ANGLE, width=4)
    arc.bias = 1.0
    th = Tag(eq(r"\theta", cfg.FONT["body"], cfg.ANGLE), lambda: 1.05 * np.array([np.cos(theta.value / 2), 0, -np.sin(theta.value / 2)]), DOWN * 0.45)
    hidden(vA, vB, labA, labB, arc, th)
    stage.add_body(arc)
    stage.add_overlay(vA, vB, labA, labB, th)
    scene.play(stage.fade(rod, 0.0), stage.fade(tip, 0.0), stage.fade(force, 0.0), stage.fade(pivot, 0.0),
               stage.fade(vA, 1.0), stage.fade(labA, 1.0), run_time=1.0)
    scene.play(stage.fade(vB, 1.0), stage.fade(labB, 1.0), run_time=0.8)
    scene.play(stage.fade(arc, 1.0), stage.fade(th, 1.0), run_time=0.8)
    AxB = eq(r"\vec A \times \vec B", cfg.FONT["title"], cfg.TORQUE).move_to([-4.6, 2.9, 0])
    scene.play(FadeOut(name), Write(AxB), run_time=1.2)

    # --- 4. Magnitude: the parallelogram's area ------------------------------------------------------------------------------------
    beat(scene, t, 3)
    gram = Face(lambda: [O, A(), A() + B(), B()], cfg.TORQUE, opacity=0.32, edge_opacity=0.8)
    gram.bias = -50
    gram.presence = 0.0
    stage.add_body(gram)
    mag = eq(r"|\vec A \times \vec B| = AB\sin\theta", cfg.FONT["section"], cfg.WHITE)
    mag.next_to(AxB, DOWN, buff=0.4).align_to(AxB, LEFT)
    area = txt("= the parallelogram's area", cfg.FONT["small"], cfg.TORQUE).next_to(mag, DOWN, buff=0.2).align_to(mag, LEFT)
    scene.play(stage.fade(gram, 1.0), Write(mag), run_time=1.6)
    scene.play(FadeIn(area), run_time=0.7)

    # --- 5. Direction: perpendicular to both --------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    vC = Vector(O, C, cfg.TORQUE, width=0.1, tip=0.32)
    labC = Tag(eq(r"\vec A\times\vec B", cfg.FONT["body"], cfg.TORQUE), C, RIGHT * 1.0 + UP * 0.2)
    square = Curve(lambda: np.array([[0.3, 0, 0], [0.3, 0.3, 0], [0, 0.3, 0]]), cfg.WHITE, width=3, glow=False)
    square.bias = 2.0
    hidden(vC, labC, square)
    stage.add_body(square)
    stage.add_overlay(vC, labC)
    scene.play(stage.fade(vC, 1.0), run_time=1.0)
    scene.play(stage.fade(labC, 1.0), stage.fade(square, 1.0), *stage.turn(yaw=-0.75, pitch=0.3), run_time=2.0)

    # --- 6. Right-hand rule -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    curl = turn_arrow_3d(stage, lambda: np.array([0.0, 0.35, 0.0]), (0, 1, 0), 0.85, np.pi / 2, theta.value,
                         cfg.ANGLE, width=6)   # right-handed about +y: from A (+x) toward B
    hidden(*curl.parts)
    rhr = VGroup(txt("right hand:", cfg.FONT["small"], cfg.MUTED),
                 txt("curl A → B", cfg.FONT["small"], cfg.ANGLE),
                 txt("thumb: A × B", cfg.FONT["small"], cfg.TORQUE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    rhr.move_to([4.7, 2.7, 0])
    scene.play(FadeOut(area), *[stage.fade(p, 1.0) for p in curl.parts], run_time=1.2)
    scene.play(FadeIn(rhr, shift=LEFT * 0.15, lag_ratio=0.3), run_time=1.6)
    scene.play(*stage.turn(yaw=-0.35, pitch=0.5), run_time=2.6)

    # --- 7. Perpendicular: the biggest ------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(*[stage.fade(p, 0.0) for p in curl.parts], FadeOut(rhr), run_time=0.6)
    value = readout(r"\sin\theta =", lambda: float(np.sin(theta.value)), 2, "", cfg.ANGLE, size=46).move_to([4.6, 2.9, 0])
    scene.play(FadeIn(value), run_time=0.5)
    scene.play(theta.to(stage, np.radians(90)), run_time=2.0)
    biggest = eq(r"\theta = 90^\circ:\ |\vec A\times\vec B| = AB", cfg.FONT["body"], cfg.BALANCED).move_to([4.2, -3.3, 0])
    scene.play(FadeIn(biggest), run_time=0.8)

    # --- 8. Parallel: zero ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(theta.to(stage, 0.0), FadeOut(biggest), stage.fade(labC, 0.0), stage.fade(th, 0.0), stage.fade(square, 0.0), run_time=2.6)
    zero = eq(r"\theta = 0^\circ,\ 180^\circ:\ \vec A\times\vec B = 0", cfg.FONT["body"], cfg.WARNING).move_to([4.2, -3.3, 0])
    fit_width(zero, 7.0)
    scene.play(FadeIn(zero), run_time=0.8)
    scene.play(theta.to(stage, np.pi), run_time=1.5)

    # --- 9. Order matters ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(theta.to(stage, np.radians(65)), FadeOut(zero), FadeOut(value), stage.fade(square, 1.0),
               run_time=1.6)
    scene.play(stage.fade(labC, 1.0), stage.fade(th, 1.0), run_time=0.4)
    vD = Vector(O, lambda: -C(), cfg.ROSE, width=0.1, tip=0.32)
    labD = Tag(eq(r"\vec B\times\vec A", cfg.FONT["body"], cfg.ROSE), lambda: -C(), RIGHT * 1.0)
    hidden(vD, labD)
    stage.add_overlay(vD, labD)
    scene.play(stage.fade(vD, 1.0), stage.fade(labD, 1.0), *stage.turn(pitch=0.22), run_time=1.4)
    anti = eq(r"\vec B\times\vec A = -\,\vec A\times\vec B", cfg.FONT["section"], cfg.WHITE)
    anti_box = boxed(anti, cfg.RESULT).move_to([-4.3, -3.3, 0])
    scene.play(Write(anti), run_time=1.4)
    scene.play(Create(anti_box.frame), run_time=0.6)

    # --- 10. Exactly what rotation needs ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    needs = VGroup(chip("perpendicular direction", cfg.TORQUE), chip("sine of the angle", cfg.ANGLE)).arrange(RIGHT, buff=0.6)
    needs.move_to([4.0, 2.9, 0])
    fit_width(needs, 7.4)
    scene.play(FadeIn(needs, shift=DOWN * 0.1, lag_ratio=0.3), run_time=1.2)
    finish(scene, t, stage)
