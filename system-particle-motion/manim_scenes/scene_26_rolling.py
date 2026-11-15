"""Scene 26 — rolling: translation plus rotation. A wheel rolls along a 3D
road without slipping (spin = -x / R, so speed v_cm = R |omega| exactly). It pauses
and four rim points get arrows: gold translation (all v_cm), cyan rotation
(tangent, size R omega = v_cm), then white sums: 2 v_cm at the top, zero at
the contact point (ringed red), diagonal at the sides. It rolls on, and one
gold rim bead draws its cycloid: stopping at every touch, racing at the top.
"""

from manim_scenes.common import *

R = 1.35
X0 = -4.7
CYCLOID_START_X = 0.0
CYCLOID_END_X = 4.7
V_LEN = 1.25                  # screen length of v_cm


def material_point(x: float) -> np.ndarray:
    """The same marked point on the outer rim, including its visible front-face offset."""
    a = -np.pi / 2 - (x - X0) / R
    return np.array([x + R * np.cos(a), R + R * np.sin(a), 0.375])


class Scene26Rolling(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "26", "Rolling: translation plus rotation")
    stage = Stage((0.0, -2.0, 0.0), zoom=1.15, yaw=-0.12, pitch=0.16, sway=0.015)
    road = Grid((0, 0, 0), (1, 0, 0), (0, 0, 1), (-8.0, 8.0), (-1.4, 1.4), step=0.5, major=4, color=cfg.GRID, opacity=0.35,
                fill="#1B2A38", fill_opacity=0.6)
    stage.add_body(road)
    x = Knob(X0)

    def centre() -> np.ndarray:
        return np.array([x.value, R, 0.0])

    def spin() -> float:
        return -(x.value - X0) / R

    drum = Drum(centre, R, 0.3, cfg.DISC_BODY, spin=spin, stripe=cfg.DISC_STRIPE, sectors=8)
    bead = Ball(lambda: material_point(x.value), 0.13, cfg.GOLD, layers=14)
    bead.bias = 50.0
    stage.add_body(drum, bead)
    show(scene, stage, 0.8)
    scene.play(x.to(stage, -2.0, rate_func=rate_functions.ease_out_sine), run_time=3.2)

    # --- 2. Translation + rotation -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    move = Vector(lambda: centre() + np.array([0, 0, 0.4]), lambda: centre() + np.array([V_LEN, 0, 0.4]), cfg.VELOCITY,
                  width=0.09, tip=0.28)
    hidden(move)
    stage.add_overlay(move)
    curl = turn_arrow_3d(stage, lambda: centre() + np.array([0, 0, 0.45]), (0, 0, 1), R * 0.62, np.radians(120),
                         -np.radians(250), cfg.OMEGA, width=5)
    hidden(*curl.parts)
    eqn = VGroup(txt("rolling", cfg.FONT["section"], cfg.TORQUE), txt("=", cfg.FONT["section"], cfg.WHITE),
                 txt("translation", cfg.FONT["section"], cfg.VELOCITY), txt("+", cfg.FONT["section"], cfg.WHITE),
                 txt("rotation", cfg.FONT["section"], cfg.OMEGA)).arrange(RIGHT, buff=0.3).move_to(UP * 3.1)
    fit_width(eqn, 13.0)
    scene.play(stage.fade(move, 1.0), FadeIn(eqn[2]), run_time=0.8)
    scene.play(*[stage.fade(p, 1.0) for p in curl.parts], FadeIn(eqn[3:]), run_time=0.8)
    scene.play(FadeIn(eqn[:2]), x.to(stage, CYCLOID_START_X, rate_func=linear), run_time=2.2)

    # --- 3. No slipping: v_cm = R omega ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    contact = Tag(Circle(radius=0.22, stroke_color=cfg.WARNING, stroke_width=5), lambda: np.array([x.value, 0.0, 0.3]))
    contact.presence = 0.0
    stage.add_overlay(contact)
    no_slip = eq(r"v_{\mathrm{cm}} = R\,|\omega|", cfg.FONT["title"], cfg.WHITE)
    no_slip_box = boxed(no_slip, cfg.RESULT).move_to([0, 1.9, 0])
    scene.play(stage.fade(contact, 1.0), run_time=0.6)
    skid = caption("no slip: contact-point velocity = 0", cfg.WARNING, cfg.FONT["small"])
    scene.play(FadeIn(skid), run_time=0.7)
    scene.play(Write(no_slip), run_time=1.4)
    scene.play(Create(no_slip_box.frame), run_time=0.6)

    # --- 4. Translation arrows -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(eqn), FadeOut(skid), run_time=0.3)
    scene.play(*[stage.fade(p, 0.0) for p in curl.parts], stage.fade(move, 0.0),
               VGroup(no_slip_box, no_slip).animate.scale(0.7).move_to([-5.2, 3.2, 0]), run_time=0.5)
    angles = [np.pi / 2, 0.0, -np.pi / 2, np.pi]

    def rim(a: float) -> np.ndarray:
        return centre() + R * np.array([np.cos(a), np.sin(a), 0.0]) + np.array([0, 0, 0.35])

    def v_rot(a: float) -> np.ndarray:
        return V_LEN * np.array([np.sin(a), -np.cos(a), 0.0])

    trans = [Vector(lambda a=a: rim(a), lambda a=a: rim(a) + np.array([V_LEN, 0, 0]), cfg.VELOCITY, width=0.07, tip=0.24)
             for a in angles]
    rot = [Vector(lambda a=a: rim(a), lambda a=a: rim(a) + v_rot(a), cfg.OMEGA, width=0.07, tip=0.24) for a in angles]
    total = [Vector(lambda a=a: rim(a), lambda a=a: rim(a) + np.array([V_LEN, 0, 0]) + v_rot(a), cfg.WHITE, width=0.09, tip=0.3)
             for a in angles]
    hidden(*trans, *rot, *total)
    stage.add_overlay(*trans, *rot, *total)
    legend = VGroup(txt("translation: v_cm everywhere", cfg.FONT["small"], cfg.VELOCITY),
                    txt("rotation: R ω, along the rim", cfg.FONT["small"], cfg.OMEGA),
                    txt("sum", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([4.6, 2.9, 0])
    scene.play(*[stage.fade(v, 1.0) for v in trans], FadeIn(legend[0]), run_time=1.0)

    # --- 5. Rotation arrows --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[stage.fade(v, 1.0) for v in rot], FadeIn(legend[1]), run_time=1.0)
    equal = eq(r"R\,|\omega| = v_{\mathrm{cm}}", cfg.FONT["body"], cfg.OMEGA).move_to([-2.0, 2.1, 0])
    scene.play(FadeIn(equal), run_time=0.8)

    # --- 6. Add them: top 2 v_cm -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[stage.fade(v, 0.0) for v in trans + rot], *[stage.fade(v, 1.0) for v in total], FadeIn(legend[2]),
               FadeOut(equal), run_time=1.2)
    top_lab = Tag(eq(r"2\,v_{\mathrm{cm}}", cfg.FONT["section"], cfg.WHITE), lambda: rim(np.pi / 2) + np.array([2 * V_LEN, 0, 0]),
                  RIGHT * 0.75)
    top_lab.presence = 0.0
    stage.add_overlay(top_lab)
    scene.play(stage.fade(top_lab, 1.0), run_time=0.8)
    twice = caption("top speed: twice the centre's speed", cfg.WHITE)
    scene.play(FadeIn(twice), run_time=0.6)

    # --- 7. Bottom: zero ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    zero = Tag(eq("0", cfg.FONT["section"], cfg.WARNING), lambda: rim(-np.pi / 2), DOWN * 0.6 + RIGHT * 0.5)
    zero.presence = 0.0
    stage.add_overlay(zero)
    rest = caption("the contact point: momentarily at rest", cfg.WARNING)
    scene.play(stage.fade(zero, 1.0), fade_through(twice, rest), run_time=0.9)

    # --- 8. Roll on: the cycloid ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(*[stage.fade(v, 0.0) for v in trans + rot + total], stage.fade(top_lab, 0.0), stage.fade(zero, 0.0),
               stage.fade(contact, 0.0), FadeOut(legend), run_time=0.6)
    start_x = x.value
    trail = Curve(lambda: np.array([material_point(xx)
                                    for xx in np.linspace(start_x, max(x.value, start_x + 1e-3), 90)]),
                  cfg.GOLD, width=4)
    trail.bias = 45.0
    stage.add_body(trail)
    cyc = caption("one rim point traces a cycloid", cfg.GOLD)
    scene.play(fade_through(rest, cyc), x.to(stage, CYCLOID_END_X, rate_func=linear), run_time=8.0)
    finish(scene, t, stage)
