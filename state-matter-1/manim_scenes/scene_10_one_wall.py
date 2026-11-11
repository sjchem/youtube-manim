"""Scene 10 — one molecule, one wall. A single gold molecule zigzags inside a
3D cube of side L, its trail glowing; one wall is singled out. A 2D close-up
of that wall shows the elastic bounce: the velocity splits into v_x (blue,
toward the wall) and the part along the wall (rose); only v_x reverses. The
momentum along x goes from +m v_x to -m v_x, so the wall receives 2 m v_x,
outward, every hit. For N2 at 300 K (rms ~517 m/s) that is ~4.8e-23 kg m/s.
"""

from manim_scenes.common import *

A = pm.AIR
WALL_X = 2.2
HIT = np.array([WALL_X - 0.24, -0.2, 0.0])
V_IN = np.array([1.6, 0.9, 0.0])


class Scene10OneWall(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "One molecule, one wall")
    box = GasBox((-0.4, -0.45, 0), count=1, seed=cfg.SEED + 10, half_x=1.75, half_z=1.75, height=3.5, floor=-1.75,
                 follow=0, trail=7.0, zoom=1.2, yaw=-0.55, pitch=0.32, speed=2.4, radius=0.1)
    box.gas.u[0] = mu.unit([0.8, 0.45, 0.55]) * 0.95
    show(scene, box.stage, 1.0)
    turn = txt("where does pressure come from?", cfg.FONT["section"], cfg.WHITE).move_to([0, -2.9, 0])
    scene.play(FadeIn(turn, shift=DOWN * 0.1), run_time=0.9)
    scene.wait(2.4)

    # --- 2. One molecule, mass m, in a cube of side L ------------------------------------------------------------------
    beat(scene, t, 1)
    ch = box.chamber
    side = Tag(eq("L", cfg.FONT["section"], cfg.VOLUME), lambda: ch.corner(-1, 0, 1) + np.array([ch.half_x, -0.38, 0.0]))
    mass = Tag(eq("m", cfg.FONT["body"], cfg.FOLLOWED), lambda: box.cloud.position(0), UR * 0.38)
    for item in (side, mass):
        item.presence = 0.0
    box.stage.add_overlay(side, mass)
    scene.play(FadeOut(turn), run_time=0.5)
    scene.play(box.stage.fade(side, 1.0), box.stage.fade(mass, 1.0), run_time=0.8)
    scene.play(*box.stage.turn(yaw=-0.25), run_time=5.5)

    # --- 3. One wall; the perpendicular part of the velocity, v_x -----------------------------------------------------------
    beat(scene, t, 2)
    wall = Face(lambda: [ch.corner(1, 0, -1), ch.corner(1, 0, 1), ch.corner(1, 1, 1), ch.corner(1, 1, -1)], cfg.IMPULSE,
                opacity=0.22, edge_opacity=0.9)
    wall.bias = 2e3
    wall.presence = 0.0
    box.stage.add_body(wall)
    velocity = Vector(lambda: box.cloud.position(0), lambda: box.cloud.position(0) + box.cloud.velocity(0) * 0.55,
                      cfg.VELOCITY, width=0.06, tip=0.2)
    vx = Vector(lambda: box.cloud.position(0),
                lambda: box.cloud.position(0) + np.array([box.cloud.velocity(0)[0] * 0.55, 0, 0]), cfg.X_COLOR, width=0.06, tip=0.2)
    for item in (velocity, vx):
        item.presence = 0.0
    box.stage.add_overlay(velocity, vx)
    scene.play(box.stage.fade(wall, 1.0), box.stage.fade(mass, 0.0), run_time=1.0)
    scene.play(box.stage.fade(velocity, 1.0), run_time=0.8)
    scene.play(box.stage.fade(vx, 1.0), run_time=0.8)
    vx_tag = Tag(eq("v_x", cfg.FONT["body"], cfg.X_COLOR),
                 lambda: box.cloud.position(0) + np.array([box.cloud.velocity(0)[0] * 0.55, 0, 0]), DOWN * 0.42)
    vx_tag.presence = 0.0
    box.stage.add_overlay(vx_tag)
    scene.play(box.stage.fade(vx_tag, 1.0), run_time=0.6)
    scene.wait(3.5)

    # --- 4. A close-up of the bounce: only v_x flips ------------------------------------------------------------------------------
    beat(scene, t, 3)
    s = Knob(-1.0)                       # -1 .. 0: approach; 0 .. 1: rebound

    def velocity_now() -> np.ndarray:
        return V_IN if s.value < 0 else np.array([-V_IN[0], V_IN[1], 0.0])

    def where() -> np.ndarray:
        return HIT + velocity_now() * s.value * 1.6

    slab = Rectangle(width=0.5, height=5.4, stroke_color=cfg.IMPULSE, stroke_width=3, fill_color=cfg.IMPULSE,
                     fill_opacity=0.25).move_to([WALL_X + 0.25, -0.3, 0])
    hatch = VGroup(*[Line([WALL_X + 0.5, y, 0], [WALL_X + 0.85, y + 0.35, 0], stroke_color=cfg.IMPULSE, stroke_width=2,
                          stroke_opacity=0.6) for y in np.linspace(-2.9, 2.0, 12)])
    ball = bead(where(), cfg.FOLLOWED, 0.24, glow=1.0)
    ball.add_updater(lambda m: m.move_to(where()))
    v_arrow = VecArrow(where, lambda: where() + velocity_now() * 1.0, cfg.VELOCITY, width=0.09)
    x_arrow = VecArrow(where, lambda: where() + np.array([velocity_now()[0], 0, 0]) * 1.0, cfg.X_COLOR, width=0.08)
    y_arrow = VecArrow(where, lambda: where() + np.array([0, velocity_now()[1], 0]) * 1.0, cfg.Y_COLOR, width=0.08)
    path_in = DashedLine(HIT - V_IN * 1.6, HIT, stroke_color=cfg.MUTED, stroke_width=2.5, dash_length=0.12)
    path_out = DashedLine(HIT, HIT + np.array([-V_IN[0], V_IN[1], 0]) * 1.6, stroke_color=cfg.MUTED, stroke_width=2.5,
                          dash_length=0.12)
    labels = VGroup(eq(r"\vec v", cfg.FONT["body"], cfg.VELOCITY), eq("v_x", cfg.FONT["body"], cfg.X_COLOR),
                    eq(r"v_\parallel", cfg.FONT["body"], cfg.Y_COLOR)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([5.4, 1.2, 0])
    hide(scene, box.stage, 0.9)
    scene.play(FadeIn(slab), FadeIn(hatch), FadeIn(ball), Create(path_in), run_time=0.9)
    scene.add(v_arrow, x_arrow, y_arrow)
    scene.play(FadeIn(labels), s.to(ball, -0.7, run_time=1.2), run_time=1.2)
    scene.play(s.to(ball, 0.0, run_time=1.6, rate_func=linear), run_time=1.6)
    flash = Circle(radius=0.4, stroke_color=cfg.IMPULSE, stroke_width=6).move_to([WALL_X, HIT[1], 0])
    scene.play(Create(path_out), s.to(ball, 0.6, run_time=1.3, rate_func=linear), FadeOut(flash, scale=2.2), run_time=1.3)
    same = VGroup(txt("speed: same", cfg.FONT["small"], cfg.VELOCITY), txt("along the wall: same", cfg.FONT["small"], cfg.Y_COLOR),
                  txt("v_x: flips", cfg.FONT["small"], cfg.X_COLOR)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-4.6, 2.3, 0])
    scene.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in same], lag_ratio=0.4), run_time=2.0)

    # --- 5. p_x: +m v_x -> -m v_x: a change of 2 m v_x -------------------------------------------------------------------------------
    beat(scene, t, 4)
    steps = VGroup(eq(r"p_x:\ +m v_x \ \longrightarrow\ -m v_x", cfg.FONT["body"], cfg.WHITE),
                   eq(r"|\Delta p_x| = 2 m v_x", cfg.FONT["section"], cfg.IMPULSE)).arrange(DOWN, buff=0.4).move_to([-3.6, -2.2, 0])
    scene.play(FadeOut(same), run_time=0.5)
    scene.play(Write(steps[0]), run_time=1.6)
    scene.play(FadeIn(steps[1], shift=UP * 0.15), run_time=1.2)
    scene.play(s.to(ball, -0.8, run_time=0.01), run_time=0.1)
    scene.play(s.to(ball, 0.0, run_time=1.4, rate_func=linear), run_time=1.4)
    scene.play(s.to(ball, 0.6, run_time=1.2, rate_func=linear), run_time=1.2)

    # --- 6. The wall receives 2 m v_x, outward, every time -------------------------------------------------------------------------
    beat(scene, t, 5)
    push = VecArrow([WALL_X + 0.1, HIT[1], 0], [WALL_X + 1.9, HIT[1], 0], cfg.IMPULSE, width=0.16, tip_len=0.42, live=False)
    push_tag = eq(r"2 m v_x", cfg.FONT["section"], cfg.IMPULSE).next_to(push, RIGHT, buff=0.25)
    frame = glow_frame(steps[1], cfg.IMPULSE)
    scene.play(GrowFromPoint(push, push.get_left()), FadeIn(push_tag, shift=RIGHT * 0.1), run_time=1.2)
    scene.play(Create(frame), run_time=1.0)
    scene.wait(1.5)

    # --- 7. Nitrogen at room temperature: ~500 m/s, ~5e-23 kg m/s -------------------------------------------------------------------
    beat(scene, t, 6)
    numbers = VGroup(eq(rf"v_x \approx {fx(A.nitrogen_rms, 0)}\ \mathrm{{m/s}}", cfg.FONT["body"], cfg.VELOCITY),
                     eq(rf"2 m v_x \approx {sci(A.impulse, 1)}\ \mathrm{{kg\,m/s}}", cfg.FONT["body"], cfg.IMPULSE))
    numbers.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    fit_width(numbers, 6.6)
    numbers.move_to([-3.9, 2.85, 0])
    n2 = txt("N₂ at 300 K", cfg.FONT["label"], cfg.MUTED).next_to(numbers, UP, buff=0.3).align_to(numbers, LEFT)
    scene.play(FadeOut(labels), FadeIn(n2), run_time=0.8)
    scene.play(FadeIn(numbers[0], shift=RIGHT * 0.2), run_time=1.0)
    scene.play(FadeIn(numbers[1], shift=RIGHT * 0.2), run_time=1.2)
    scene.play(s.to(ball, -0.8, run_time=0.01), run_time=0.1)
    scene.play(s.to(ball, 0.6, run_time=2.8, rate_func=linear), run_time=2.8)

    # --- 8. Utterly tiny: how can such pushes add up? ---------------------------------------------------------------------------------
    beat(scene, t, 7)
    tiny = result_label("utterly tiny", cfg.WARNING, cfg.FONT["section"]).move_to([4.6, 2.9, 0])
    scene.play(FadeIn(tiny, scale=1.1), Indicate(numbers[1], color=cfg.WARNING), run_time=1.2)
    scene.play(s.to(ball, -0.8, run_time=0.01), run_time=0.1)
    finish(scene, t, fill=lambda sec: [s.to(ball, 0.6, rate_func=linear)])
