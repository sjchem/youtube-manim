"""Scene 03 — two masses, one balance point. On a 3D stage a light rod carries
two beads and rests on a wedge. With equal beads the wedge balances it at the
middle. The right bead grows to three times the mass: held at the middle the
rod tips; the wedge slides to the new balance point and the centre-of-mass
target follows. The formula is written; the rod becomes the worked example
(2 kg at 0, 6 kg at 4 m): 24 / 8 = 3 m; distances 1 m and 3 m are in the
inverse ratio of the masses.
"""

from manim_scenes.common import *

C = pm.COM_PAIR
S = 1.5                 # screen units per metre along the rod
HALF = (C.x2 - C.x1) / 2 * S
H = 1.05                # height of the rod above the floor


class Scene03TwoMasses(Scene):
    def construct(self) -> None:
        play_scene(self)


def bead_radius(mass: float) -> float:
    return 0.27 * (mass / C.m1) ** (1 / 3)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "03", "Two masses, one balance point")
    stage = Stage((0.0, -1.75, 0.0), zoom=1.55, yaw=-0.2, pitch=0.26, sway=0.03)
    floor(stage, 0.0, reach=6.0, opacity=0.22)
    m1, m2 = Knob(C.m1), Knob(C.m1)                 # start equal
    px, tilt = Knob(-1.4), Knob(0.0)                # wedge position (screen x), rod tilt (rad)

    def on_rod(x: float) -> np.ndarray:
        """Point at rod coordinate x (screen units from the rod's centre)."""
        rel = np.array([x - px.value, 0.0, 0.0])
        return np.array([px.value, H, 0.0]) + mu.rotation_z(tilt.value) @ rel

    def com_x() -> float:
        return (m1.value * -HALF + m2.value * HALF) / (m1.value + m2.value)

    left = Ball(lambda: on_rod(-HALF) + np.array([0, bead_radius(m1.value), 0]), bead_radius(C.m1), cfg.MASS)
    right = Ball(lambda: on_rod(HALF) + np.array([0, bead_radius(m2.value), 0]), bead_radius(C.m1), cfg.MASS)
    right_radius = lambda: bead_radius(m2.value)  # noqa: E731
    left_end = Ball(lambda: on_rod(-HALF), 0.05, cfg.STEEL, layers=6)
    right_end = Ball(lambda: on_rod(HALF), 0.05, cfg.STEEL, layers=6)
    rod = Rod(left_end, right_end, width=9, dark="#4A5A68", light="#DCE6EE")
    wedge = Solid(lambda: prism([[px.value - 0.42, 0.0], [px.value + 0.42, 0.0], [px.value, H - 0.04]], 0.32)[0],
                  prism([[0, 0], [1, 0], [0, 1]], 0.32)[1], cfg.STEEL)
    stage.add_body(wedge, rod, left_end, right_end, left, right)
    target = com_tag(lambda: (m1.value * left.where() + m2.value * right.where()) / (m1.value + m2.value), 0.19)
    target.presence = 0.0
    stage.add_overlay(target)

    def grow_right(m):
        right.radius = right_radius()

    holder = Dot(radius=0.001, fill_opacity=0)
    holder.add_updater(grow_right)
    scene.add(holder)
    show(scene, stage, 1.2)
    question = caption("where would you hold it?", cfg.WHITE)
    scene.play(FadeIn(question), run_time=0.8)
    scene.play(px.to(stage, 1.2, rate_func=there_and_back), tilt.to(stage, 0.0), run_time=3.0)

    # --- 2. Equal masses: halfway ---------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(px.to(stage, 0.0), run_time=1.4)
    half = caption("equal masses: exactly halfway", cfg.BALANCED)
    scene.play(stage.fade(target, 1.0), fade_through(question, half), run_time=1.0)

    # --- 3. Three times heavier: it tips; the balance point moves -------------------------------------------
    beat(scene, t, 2)
    heavier = caption("three times heavier", cfg.MASS)
    scene.play(m2.to(stage, C.m2), fade_through(half, heavier), run_time=1.6)
    scene.play(tilt.to(stage, -0.17, rate_func=rate_functions.ease_in_quad), run_time=1.0)
    tips = caption("held at the middle, it tips", cfg.WARNING)
    scene.play(fade_through(heavier, tips), run_time=0.8)
    scene.wait(0.8)
    scene.play(tilt.to(stage, 0.0), px.to(stage, com_x_value(C.m1, C.m2)), run_time=2.0)
    moved = caption("COM shifts toward the heavier mass", cfg.BALANCED)
    scene.play(fade_through(tips, moved), run_time=0.8)

    # --- 4. The centre of mass: a weighted average ------------------------------------------------------------
    beat(scene, t, 3)
    name = result_label("centre of mass", cfg.WHITE, cfg.FONT["section"]).move_to([0, 2.95, 0])
    scene.play(FadeIn(name, shift=DOWN * 0.15), FadeOut(moved), run_time=1.0)
    avg = caption("a weighted average of positions", cfg.MUTED)
    scene.play(FadeIn(avg), run_time=0.8)

    # --- 5. The formula -------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    formula = eq([r"x_{\mathrm{cm}}", "=", r"{m_1 x_1 + m_2 x_2", r"\over", r"m_1 + m_2}"], cfg.FONT["section"])
    formula[0].set_color(cfg.WHITE)
    formula_box = boxed(formula, cfg.WHITE).move_to([0, 2.55, 0])
    scene.play(FadeOut(name), FadeOut(avg), run_time=0.5)
    scene.play(Write(formula), run_time=2.2)
    scene.play(Create(formula_box.frame), run_time=0.8)

    # --- 6. Each position weighted by its mass -----------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(formula[2].animate.set_color(cfg.MASS), run_time=0.8)
    pull = caption("mass-weighted position", cfg.MASS)
    scene.play(FadeIn(pull), Indicate(formula[2], color=cfg.MASS, scale_factor=1.05), run_time=1.2)

    # --- 7. The worked example on the same rod ---------------------------------------------------------------------------
    beat(scene, t, 6)
    group = VGroup(formula_box, formula)
    scene.play(FadeOut(pull), group.animate.scale(0.72).move_to([-4.3, 3.0, 0]), run_time=1.0)
    kg1 = Tag(txt(f"{fx(C.m1)} kg", cfg.FONT["label"], cfg.MASS), left.where, UP * 0.85)
    kg2 = Tag(txt(f"{fx(C.m2)} kg", cfg.FONT["label"], cfg.MASS), right.where, UP * 1.05)
    x1 = Tag(eq(r"x_1 = " + fx(C.x1), cfg.FONT["label"], cfg.POSITION), lambda: on_rod(-HALF), DOWN * 0.95)
    x2 = Tag(eq(r"x_2 = " + fx(C.x2) + r"\,\mathrm{m}", cfg.FONT["label"], cfg.POSITION), lambda: on_rod(HALF), DOWN * 0.95)
    hidden(kg1, kg2, x1, x2)
    stage.add_overlay(kg1, kg2, x1, x2)
    scene.play(stage.fade(kg1, 1.0), stage.fade(x1, 1.0), run_time=0.9)
    scene.play(stage.fade(kg2, 1.0), stage.fade(x2, 1.0), run_time=0.9)

    # --- 8. 24 / 8 = 3 m ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    steps = VGroup(
        eq(rf"x_{{\mathrm{{cm}}}} = {{{fx(C.m1)}({fx(C.x1)}) + {fx(C.m2)}({fx(C.x2)}) \over {fx(C.m1)} + {fx(C.m2)}}}",
           cfg.FONT["body"]),
        eq(rf"= {{{fx(C.moment)} \over {fx(C.total)}}}", cfg.FONT["body"]),
        eq(rf"= {fx(C.x_cm)}\ \mathrm{{m}}", cfg.FONT["section"], cfg.RESULT),
    ).arrange(RIGHT, buff=0.3)
    fit_width(steps, 9.0)
    steps.move_to([2.6, 3.0, 0])
    scene.play(Write(steps[0]), run_time=2.0)
    scene.play(FadeIn(steps[1], shift=LEFT * 0.15), run_time=1.0)
    scene.play(FadeIn(steps[2], shift=LEFT * 0.15), run_time=1.0)
    result_box = glow_frame(steps[2], cfg.RESULT)
    xc = Tag(eq(rf"x_{{\mathrm{{cm}}}} = {fx(C.x_cm)}\,\mathrm{{m}}", cfg.FONT["label"], cfg.WHITE),
             lambda: on_rod(com_x()), DOWN * 1.0)
    xc.presence = 0.0
    stage.add_overlay(xc)
    scene.play(Create(result_box), stage.fade(xc, 1.0), stage.fade(x2, 0.0), run_time=1.0)

    # --- 9. Inverse ratio ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    lift = np.array([0.0, -0.55, 0.32])
    d_heavy = Segment(lambda: on_rod(com_x()) + lift, lambda: on_rod(HALF) + lift, cfg.POSITION, width=6, opacity=1.0)
    d_light = Segment(lambda: on_rod(-HALF) + lift, lambda: on_rod(com_x()) + lift, cfg.POSITION, width=6, opacity=1.0)
    d1 = Tag(txt(f"{fx(C.x2 - C.x_cm)} m", cfg.FONT["label"], cfg.POSITION),
             lambda: 0.5 * (on_rod(com_x()) + on_rod(HALF)) + lift, DOWN * 0.42)
    d3 = Tag(txt(f"{fx(C.x_cm - C.x1)} m", cfg.FONT["label"], cfg.POSITION),
             lambda: 0.5 * (on_rod(-HALF) + on_rod(com_x())) + lift, DOWN * 0.42)
    for item in (d_heavy, d_light):
        item.bias = 5.0
    hidden(d_heavy, d_light, d1, d3)
    stage.add_body(d_heavy, d_light)
    stage.add_overlay(d1, d3)
    scene.play(stage.fade(x1, 0.0), stage.fade(xc, 0.0), run_time=0.5)
    scene.play(stage.fade(d_heavy, 1.0), stage.fade(d1, 1.0), run_time=0.8)
    scene.play(stage.fade(d_light, 1.0), stage.fade(d3, 1.0), run_time=0.8)
    ratio = eq(rf"{{d_{{\text{{light}}}} \over d_{{\text{{heavy}}}}}} = {{{fx(C.x_cm - C.x1)} \over {fx(C.x2 - C.x_cm)}}}"
               rf" = {{m_2 \over m_1}}", cfg.FONT["body"], cfg.WHITE)
    ratio.move_to(DOWN * 3.6)
    scene.play(Write(ratio), run_time=1.6)
    finish(scene, t, stage)


def com_x_value(a: float, b: float) -> float:
    return (a * -HALF + b * HALF) / (a + b)
