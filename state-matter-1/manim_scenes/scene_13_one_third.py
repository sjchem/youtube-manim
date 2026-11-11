"""Scene 13 — why one third? Molecules fly in every direction. Their
velocity arrows, gathered at one point on a 3D stage, end in a fuzzy round
ball: no direction is special. One velocity splits into blue, rose and purple
components, v^2 = v_x^2 + v_y^2 + v_z^2. Bars of the sample's averages
<v_x^2>, <v_y^2>, <v_z^2> (computed from the film's gas) come out equal, so
<v_x^2> = <v^2>/3, and the pressure equation becomes PV = 1/3 N m <v^2>.
"""

from manim_scenes.common import *

GAS = pm.IdealGas(600, cfg.SEED + 13)
SCALE = 1.25                       # stage units per rms speed


class Scene13OneThird(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Why one third?")
    box = GasBox((-3.8, -0.6, 0), count=70, half_x=1.3, half_z=1.0, height=2.5, floor=-1.25, zoom=1.0, yaw=-0.5,
                 pitch=0.3, speed=1.4)
    arrows = [Vector(lambda i=i: box.cloud.position(i), lambda i=i: box.cloud.position(i) + box.cloud.velocity(i) * 0.6,
                     cfg.VELOCITY, width=0.045, tip=0.15) for i in range(0, 70, 7)]
    box.stage.add_overlay(*arrows)
    show(scene, box.stage, 1.0)
    every = txt("every direction", cfg.FONT["section"], cfg.VELOCITY).move_to([3.4, 2.6, 0])
    scene.play(FadeIn(every, shift=DOWN * 0.1), run_time=0.9)
    scene.wait(2.5)

    # --- 2. Gather the arrows at one point: a fuzzy ball ------------------------------------------------------------------------
    beat(scene, t, 1)
    space = Stage((2.6, -0.5, 0), zoom=1.15, yaw=-0.5, pitch=0.35, sway=0.03, spin=0.12)
    axes3 = [Segment(-d * 2.2, d * 2.2, c, width=3, opacity=0.65) for d, c in
             ((np.array([1.0, 0, 0]), cfg.X_COLOR), (np.array([0, 1.0, 0]), cfg.Y_COLOR), (np.array([0, 0, 1.0]), cfg.Z_COLOR))]
    tips = GAS.u * SCALE
    ball = Dots(tips, cfg.VELOCITY, radius=0.045, alpha=0.85)
    fan = [Vector(np.zeros(3), tips[i], cfg.VELOCITY, width=0.03, tip=0.1, glow=False) for i in range(0, 600, 20)]
    space.add_body(*axes3, ball)
    space.add_overlay(*fan)
    ball.presence = 0.0
    for v in fan:
        v.presence = 0.0
    scene.play(FadeOut(every), run_time=0.5)
    show(scene, space, 1.0)
    scene.play(*[space.fade(v, 0.8) for v in fan], run_time=1.6)
    scene.play(space.fade(ball, 1.0), *[space.fade(v, 0.0) for v in fan], run_time=2.0)
    special = txt("no special direction", cfg.FONT["label"], cfg.WHITE).move_to([2.6, 3.0, 0])
    scene.play(FadeIn(special), run_time=0.8)

    # --- 3. Three components: v^2 = v_x^2 + v_y^2 + v_z^2 -----------------------------------------------------------------------
    beat(scene, t, 2)
    v = np.array([1.1, 0.75, 0.6]) * 1.15
    full = Vector(np.zeros(3), v, cfg.VELOCITY, width=0.08, tip=0.25)
    cx = Vector(np.zeros(3), np.array([v[0], 0, 0]), cfg.X_COLOR, width=0.07, tip=0.22)
    cy = Vector(np.array([v[0], 0, 0]), np.array([v[0], v[1], 0]), cfg.Y_COLOR, width=0.07, tip=0.22)
    cz = Vector(np.array([v[0], v[1], 0]), v, cfg.Z_COLOR, width=0.07, tip=0.22)
    for item in (full, cx, cy, cz):
        item.presence = 0.0
    space.add_overlay(full, cx, cy, cz)
    pyth = paint(eq([r"v^2", "=", r"v_x^2", "+", r"v_y^2", "+", r"v_z^2"], cfg.FONT["section"]),
                 {0: cfg.VELOCITY, 2: cfg.X_COLOR, 4: cfg.Y_COLOR, 6: cfg.Z_COLOR}).move_to([2.6, 3.0, 0])
    scene.play(FadeOut(special), box.stage.fade(box.stage, 0.0), space.fade(ball, 0.25), space.glide([-1.6, -0.5, 0]), space.zoom_to(1.35),
               run_time=1.2)
    scene.play(space.fade(full, 1.0), space.set_spin(0.0), run_time=0.9)
    for comp in (cx, cy, cz):
        scene.play(space.fade(comp, 1.0), run_time=0.8)
    pyth.move_to([3.2, 2.9, 0])
    scene.play(Write(pyth), run_time=2.0)
    scene.play(*space.turn(yaw=0.2), run_time=4.0)

    # --- 4. Average over all molecules: three equal averages ----------------------------------------------------------------------
    beat(scene, t, 3)
    ms = GAS.mean_square()
    chart = bar_chart(list(ms), [r"x", "y", "z"], [cfg.X_COLOR, cfg.Y_COLOR, cfg.Z_COLOR], at=[4.2, -0.9, 0], width=4.6,
                      height=2.4, top=0.5, value_labels=[fx(v, 2) for v in ms], bar_width=1.0)
    title = eq(r"\langle v_i^2 \rangle", cfg.FONT["body"], cfg.WHITE).next_to(chart, UP, buff=0.3)
    scene.play(*[space.fade(c, 0.0) for c in (full, cx, cy, cz)], space.fade(ball, 1.0), space.set_spin(0.12), run_time=1.0)
    scene.play(Create(chart.base), FadeIn(chart.names), FadeIn(title), run_time=0.8)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in chart.bars], lag_ratio=0.3), run_time=1.8)
    scene.play(FadeIn(chart.tops), run_time=0.8)

    # --- 5. <v_x^2> = <v^2> / 3 ------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    third = boxed(paint(eq([r"\langle v_x^2\rangle", "=", r"\tfrac{1}{3}", r"\langle v^2\rangle"], cfg.FONT["section"]),
                        {0: cfg.X_COLOR, 2: cfg.LIMIT, 3: cfg.VELOCITY}), cfg.GOLD)
    third.move_to([3.2, 2.9, 0])
    scene.play(fade_through(pyth, third), run_time=1.4)

    # --- 6. One third: three dimensions --------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    dims = txt("3 dimensions → 1/3", cfg.FONT["label"], cfg.LIMIT).next_to(third, DOWN, buff=0.4)
    scene.play(fade_through(title, dims), run_time=0.9)

    # --- 7. PV = 1/3 N m <v^2> -----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    law = paint(eq([r"PV", "=", r"\tfrac{1}{3}", r"N m \langle v^2\rangle"], cfg.FONT["hero"]), {0: cfg.PRESSURE, 2: cfg.LIMIT})
    result = boxed(law, cfg.GOLD).move_to([0, 0.2, 0])
    scene.play(FadeOut(VGroup(chart, dims, third)), space.fade(space, 0.0), run_time=1.0)
    scene.remove(space, box.stage)
    scene.play(FadeIn(result, scale=0.9), run_time=1.6)

    # --- 8. The pressure equation of kinetic theory ----------------------------------------------------------------------------------
    beat(scene, t, 7)
    name = txt("the kinetic theory of gases", cfg.FONT["section"], cfg.GOLD).next_to(result, DOWN, buff=0.6)
    scene.play(FadeIn(name, shift=UP * 0.1), run_time=1.0)
    finish(scene, t, fill=lambda s: [result.frame.animate.set_stroke(opacity=0.5)])
