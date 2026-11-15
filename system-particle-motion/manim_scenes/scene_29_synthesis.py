"""Scene 29 — translation and rotation, side by side. The opening 3D shot
returns: one green push slides a box, swings a door and rolls a cylinder.
Then the film's answer, one idea at a time: the centre of mass carries the
translation (F = M a_cm); torque r x F and moment of inertia sum m r^2 carry
the turning. A two-column table fills pair by pair — x/theta, v/omega,
a/alpha, F = M a / tau = I alpha, p = M v / L = I omega, kinetic energies,
work, and the two conservation laws. Three gold chips name what geometry
adds; the three-line core message; and the three props move once more.
"""

from manim_scenes.common import *

PSI0 = -0.6


class Scene29Synthesis(Scene):
    def construct(self) -> None:
        play_scene(self)


def props_stage(scene: Scene) -> tuple[Stage, Knob]:
    """The opening shot in miniature: box on ice, door, cylinder. One knob drives all three pushes."""
    stage = Stage((0.0, -2.1, 0.0), zoom=1.15, yaw=-0.3, pitch=0.3, sway=0.02)
    floor(stage, 0.0, reach=7.0, opacity=0.2)
    go = Knob(0.0)
    hinge = np.array([-1.0, 0.0, 0.0])
    frame = mu.rotation_y(PSI0)
    pose = lambda: mu.rotation_y(PSI0 + 1.2 * go.value)  # noqa: E731
    ice = Face([[-6.4, 0.01, -1.1], [-2.4, 0.01, -1.1], [-2.4, 0.01, 1.1], [-6.4, 0.01, 1.1]], cfg.ICE, opacity=0.2,
               edge_opacity=0.5)
    ice.bias = -500
    box = Block(lambda: np.array([-5.0 + 2.2 * go.value, 0.36, 0.0]), (0.9, 0.72, 0.8), "#C98A4B")
    door = Block(lambda: hinge + pose() @ np.array([0.85, 1.35, 0.0]), (1.7, 2.7, 0.09), cfg.WOOD, pose=pose)
    post = Block(hinge + frame @ np.array([-0.08, 1.4, 0.0]), (0.12, 2.8, 0.2), cfg.WOOD_DARK, pose=lambda: frame)
    cyl = Drum(lambda: np.array([2.5 + 1.8 * go.value, 0.55, 0.0]), 0.55, 0.55, cfg.DISC_BODY,
               spin=lambda: -1.8 * go.value / 0.55, stripe=cfg.DISC_STRIPE, sectors=6)
    stage.add_body(ice, box, post, door, cyl)
    pushes = [Vector(lambda: np.array([-5.0 + 2.2 * go.value - 1.75, 0.36, 0.0]), lambda: np.array([-5.0 + 2.2 * go.value - 0.47, 0.36, 0.0]),
                     cfg.FORCE, width=0.1, tip=0.3),
              Vector(lambda: hinge + pose() @ np.array([1.52, 1.2, 1.3]), lambda: hinge + pose() @ np.array([1.52, 1.2, 0.07]),
                     cfg.FORCE, width=0.1, tip=0.3),
              Vector(lambda: np.array([2.5 + 1.8 * go.value - 1.85, 0.55, 0.0]), lambda: np.array([2.5 + 1.8 * go.value - 0.57, 0.55, 0.0]),
                     cfg.FORCE, width=0.1, tip=0.3)]
    stage.add_overlay(*pushes)
    stage.pushes = pushes
    return stage, go


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "29", "Translation and rotation, side by side")
    stage, go = props_stage(scene)
    show(scene, stage, 1.0)
    scene.play(go.to(stage, 1.0, rate_func=rate_functions.ease_out_sine), *[stage.fade(p, 0.0) for p in stage.pushes],
               run_time=3.0)
    q = VGroup(txt("A push.", cfg.FONT["section"], cfg.FORCE), txt("Three motions. Why?", cfg.FONT["section"], cfg.WHITE))
    q.arrange(RIGHT, buff=0.4).move_to(UP * 3.0)
    scene.play(FadeIn(q, shift=DOWN * 0.15), run_time=1.0)

    # --- 2. The centre of mass carries the translation ---------------------------------------------------------------------
    beat(scene, t, 1)
    hide(scene, stage, 0.8, FadeOut(q))
    ideas = VGroup(
        VGroup(com_target(0.24, glow=False), eq(r"\vec F_{\text{ext}} = M\vec a_{\mathrm{cm}}", cfg.FONT["section"], cfg.WHITE)).arrange(RIGHT, buff=0.4),
        VGroup(eq(r"\vec\tau = \vec r\times\vec F", cfg.FONT["section"], cfg.TORQUE),
               eq(r"I = \sum m r_\perp^2", cfg.FONT["section"], cfg.INERTIA)).arrange(RIGHT, buff=1.0),
    ).arrange(DOWN, buff=0.6).move_to(UP * 0.6)
    scene.play(FadeIn(ideas[0], shift=UP * 0.15), run_time=1.0)
    carries = caption("the centre of mass carries the translation", cfg.WHITE)
    scene.play(FadeIn(carries), run_time=0.6)

    # --- 3. Torque and moment of inertia carry the turning ------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeIn(ideas[1][0], shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(ideas[1][1], shift=UP * 0.15), run_time=1.0)
    turning = caption("where a force acts, and where the mass sits, decide the turning", cfg.TORQUE, cfg.FONT["small"])
    scene.play(fade_through(carries, turning), run_time=0.8)

    # --- 4. The table ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(ideas), FadeOut(turning), run_time=0.6)
    heads = VGroup(txt("translation", cfg.FONT["body"], cfg.VELOCITY), txt("rotation (fixed axis)", cfg.FONT["body"], cfg.ANGLE))
    pairs = [(r"x,\ v,\ a", r"\theta,\ \omega,\ \alpha"), (r"F = M a", r"\tau = I\alpha"), (r"p = M v", r"L = I\omega"),
             (r"K = \tfrac12 M v^2", r"K = \tfrac12 I\omega^2"), (r"W = \textstyle\int F_x\,dx", r"W = \textstyle\int \tau\,d\theta"),
             (r"F_{\text{ext}} = 0:\ p\ \text{conserved}", r"\tau_{\text{ext}} = 0:\ L\ \text{conserved}")]
    rows = VGroup()
    for left, right in pairs:
        rows.add(VGroup(eq(left, cfg.FONT["body"], cfg.VELOCITY), eq(right, cfg.FONT["body"], cfg.ANGLE)))
    ys = np.linspace(2.0, -3.0, len(pairs))
    for row, y in zip(rows, ys):
        for item in row:
            fit_width(item, 6.4)
        row[0].move_to([-3.6, y, 0])
        row[1].move_to([3.6, y, 0])
    heads[0].move_to([-3.6, 3.05, 0])
    heads[1].move_to([3.6, 3.05, 0])
    rule = Line([0, 2.7, 0], [0, -3.5, 0], stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5)
    scene.play(FadeIn(heads), Create(rule), run_time=0.8)
    for row in rows[:4]:
        scene.play(FadeIn(row[0], shift=RIGHT * 0.1), run_time=0.7)
        scene.play(FadeIn(row[1], shift=RIGHT * 0.12), run_time=1.1)

    # --- 5. Work and conservation -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    for row in rows[4:]:
        scene.play(FadeIn(row[0], shift=RIGHT * 0.1), run_time=0.6)
        scene.play(FadeIn(row[1], shift=RIGHT * 0.12), run_time=1.0)
    scene.play(Create(glow_frame(rows[5], cfg.BALANCED, buff=0.15)), run_time=0.8)

    # --- 6. Geometry joins the story ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[FadeOut(m) for m in scene.mobjects if not getattr(m, "_is_project_background", False)], run_time=0.8)
    same_laws = txt("Newton's laws · energy · momentum", cfg.FONT["body"], cfg.MUTED).move_to(UP * 2.6)
    geometry = VGroup(chip("where the force acts", cfg.TORQUE), chip("where the mass sits", cfg.INERTIA),
                      chip("which axis it turns about", cfg.ANGLE)).arrange(DOWN, buff=0.4).move_to(DOWN * 0.4)
    plus = txt("+ geometry", cfg.FONT["section"], cfg.RESULT).move_to(UP * 1.5)
    scene.play(FadeIn(same_laws), run_time=0.8)
    scene.play(FadeIn(plus, scale=1.1), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in geometry], lag_ratio=0.4), run_time=2.0)

    # --- 7. The core message ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(same_laws, plus, geometry)), run_time=0.6)
    core = VGroup(txt("Net force changes the centre-of-mass motion.", cfg.FONT["section"], cfg.FORCE),
                  txt("Torques change the rotation.", cfg.FONT["section"], cfg.TORQUE),
                  txt("Moment of inertia links shape to spin.", cfg.FONT["section"], cfg.INERTIA)).arrange(DOWN, buff=0.45)
    fit_width(core, 13.4)
    core.move_to(UP * 0.2)
    for line in core:
        scene.play(FadeIn(line, shift=UP * 0.15), run_time=0.9)

    # --- 8. Push a box, a door, a cylinder: now you know why ------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(core.animate.scale(0.6).move_to(UP * 3.0), run_time=0.8)
    stage2, go2 = props_stage(scene)
    show(scene, stage2, 0.8)
    scene.play(go2.to(stage2, 1.0, rate_func=rate_functions.ease_out_sine), *[stage2.fade(p, 0.0) for p in stage2.pushes],
               run_time=3.2)
    why = caption("not only how things move, but why", cfg.RESULT)
    scene.play(FadeIn(why), run_time=0.8)
    finish(scene, t, stage2)
