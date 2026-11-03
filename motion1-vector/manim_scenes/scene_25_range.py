"""Scene 25 — the range. Range needs horizontal speed and time aloft:
R = v0 cos(theta) T; substituting T and using 2 sin cos = sin 2theta gives
R = v0^2 sin(2 theta) / g = 40.82 m, which the 3D field then measures with a
ruler: 14.14 m/s for 2.89 s. A shallow (20 degrees) and a steep (70 degrees)
throw at the same speed show the trade-off between speed and time.
"""

from manim_scenes.common import *

SHALLOW, STEEP = pm.Projectile(P.v0, 20.0), pm.Projectile(P.v0, 70.0)


class Scene25Range(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "25", "The range")
    q = txt("How far?", cfg.FONT["hero"], cfg.WHITE).move_to(UP * 0.8)
    scene.play(FadeIn(q, scale=0.95), run_time=0.9)

    # --- 2. Two ingredients: horizontal speed and time aloft ------------------------------------------------------------
    beat(scene, t, 1)
    needs = VGroup(chip("horizontal speed", cfg.X_COLOR, cfg.FONT["body"]), txt("×", cfg.FONT["title"], cfg.WHITE),
                   chip("time in the air", cfg.TIME, cfg.FONT["body"])).arrange(RIGHT, buff=0.5).next_to(q, DOWN, buff=0.8)
    scene.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in needs], lag_ratio=0.35), run_time=1.6)

    # --- 3. R = v0 cos(theta) T --------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(q), FadeOut(needs), run_time=0.6)
    r1 = paint(eq([r"R", "=", r"v_0\cos\theta", r"\cdot", "T"], cfg.FONT["section"]), {0: cfg.GREEN, 2: cfg.X_COLOR, 4: cfg.TIME})
    r1.move_to([0, 2.5, 0])
    scene.play(Write(r1), run_time=1.4)

    # --- 4. Substitute T ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    r2 = paint(eq([r"R", "=", r"v_0\cos\theta", r"\cdot", r"\frac{2v_0\sin\theta}{g}"], cfg.FONT["section"]),
               {0: cfg.GREEN, 2: cfg.X_COLOR, 4: cfg.TIME}).next_to(r1, DOWN, buff=0.5)
    scene.play(FadeIn(r2, shift=DOWN * 0.2), run_time=1.6)

    # --- 5. 2 sin cos = sin 2theta ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    ident = eq(r"2\sin\theta\cos\theta = \sin 2\theta", cfg.FONT["body"], cfg.GOLD).next_to(r2, DOWN, buff=0.5)
    scene.play(Write(ident), run_time=1.6)
    scene.play(Indicate(ident, color=cfg.GOLD, scale_factor=1.06), run_time=1.0)

    # --- 6. R = v0^2 sin 2theta / g -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    r3 = paint(eq([r"R", "=", r"\frac{v_0^2\,\sin 2\theta}{g}"], cfg.FONT["title"]), {0: cfg.GREEN}).next_to(ident, DOWN, buff=0.55)
    box = boxed(r3, cfg.GREEN)
    scene.play(Write(r3), run_time=1.6)
    scene.play(FadeIn(box[0]), run_time=0.6)

    # --- 7. Numbers ------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(r1, r2, ident)), run_time=0.4)
    scene.play(box.animate.move_to([-3.6, 2.4, 0]), run_time=0.5)
    nums = eq([r"R", "=", rf"\frac{{{P.v0:.0f}^2\,\sin 90^\circ}}{{{G_TEXT}}}"], cfg.FONT["section"])
    paint(nums, {0: cfg.GREEN}).move_to([3.4, 2.4, 0])
    scene.play(Write(nums), run_time=1.6)

    # --- 8. About 40.82 m ---------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    ans = eq([r"\approx", rf"{RANGE}\ \mathrm{{m}}"], cfg.FONT["section"], cfg.GREEN).next_to(nums, DOWN, buff=0.3)
    scene.play(FadeIn(ans, scale=1.1), run_time=0.9)

    # --- 9. Check on the field: 14.14 m/s for 2.89 s ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    stage, flight = projectile_stage(at=(0.5, -2.5, 0), zoom=1.15, pitch=0.36)
    start_pt, end_pt = flight.world(0.0), flight.world(P.flight_time)
    grow = Knob(0.0)
    ruler = Curve(lambda: [start_pt + np.array([0, 0.03, 0.6]), start_pt + (end_pt - start_pt) * max(grow.value, 1e-3) + np.array([0, 0.03, 0.6])],
                  cfg.GREEN, width=5)
    ends = [Segment(p + np.array([0, 0.03, 0.35]), p + np.array([0, 0.03, 0.85]), cfg.GREEN, width=4, opacity=1.0) for p in (start_pt, end_pt)]
    stage.add_body(ruler, *ends)
    tag = Tag(eq(rf"{RANGE}\ \mathrm{{m}}", cfg.FONT["body"], cfg.GREEN), (start_pt + end_pt) / 2 + np.array([0, 0, 0.6]), DOWN * 0.45)
    tag.presence = 0.0
    stage.add_overlay(tag)
    show(scene, stage, 0.8)
    product = eq([rf"{VX}\ \mathrm{{m/s}}", r"\times", rf"{T_FLIGHT}\ \mathrm{{s}}"], cfg.FONT["body"])
    paint(product, {0: cfg.X_COLOR, 2: cfg.TIME}).next_to(ans, DOWN, buff=0.35)
    scene.play(flight.realtime(speed=0.6), grow.to(stage, 1.0, run_time=P.flight_time / 0.6, rate_func=linear), FadeIn(product),
               run_time=P.flight_time / 0.6)
    scene.play(stage.fade(tag, 1.0), run_time=0.6)

    # --- 10. Shallow: fast forward, short flight -----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(box, nums, ans, product)), stage.fade(tag, 0.0), stage.fade(ruler, 0.0),
               *[stage.fade(e, 0.0) for e in ends], stage.fade(flight.trail, 0.0), stage.fade(flight.ball, 0.0), run_time=0.6)
    shallow = Flight(stage, SHALLOW, origin=(LAUNCH_X, 0, -0.9), trail_color=cfg.CYAN, color=cfg.CYAN)
    shallow.add_arrow("vx", cfg.X_COLOR, width=0.08, presence=1.0)
    lab = VGroup(txt(f"{SHALLOW.angle:.0f}°", cfg.FONT["label"], cfg.CYAN),
                 txt(f"in the air {md.fixed(SHALLOW.flight_time, 2)} s", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.15)
    lab.move_to([0.0, 2.7, 0])
    scene.play(FadeIn(lab), shallow.realtime(speed=0.45), run_time=SHALLOW.flight_time / 0.45)

    # --- 11. Steep: long flight, slow forward -----------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    steep = Flight(stage, STEEP, origin=(LAUNCH_X, 0, 0.9), trail_color=cfg.PURPLE, color=cfg.PURPLE)
    steep.add_arrow("vx", cfg.X_COLOR, width=0.08, presence=1.0)
    lab2 = VGroup(txt(f"{STEEP.angle:.0f}°", cfg.FONT["label"], cfg.PURPLE),
                  txt(f"in the air {md.fixed(STEEP.flight_time, 2)} s", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.15)
    lab2.move_to([0.0, 2.7, 0])
    scene.play(fade_through(lab, lab2), run_time=0.6)
    scene.play(steep.realtime(speed=1.0), run_time=STEEP.flight_time)

    # --- 12. Which angle wins? -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    wins = result_label("Which angle wins?", cfg.GOLD, cfg.FONT["title"]).move_to(UP * 2.7)
    scene.play(fade_through(lab2, wins), run_time=1.0)
    scene.play(Indicate(wins, color=cfg.GOLD, scale_factor=1.05), run_time=1.4)
    scene.wait(4.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["25"])
