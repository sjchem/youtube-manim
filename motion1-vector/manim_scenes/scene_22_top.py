"""Scene 22 — the highest point. The throw slows into a freeze-frame at
t_H = 1.44 s: v_y = 0, but v_x = 14.14 m/s is still there (the slowest
speed of the flight, not zero), and the orange gravity arrow is unchanged.
A 'gravity switched off' ghost leaves the top in a straight line; the real
ball curves down. A four-line checklist closes it.
"""

from manim_scenes.common import *


class Scene22Top(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "22", "The highest point")
    stage, flight = projectile_stage(zoom=1.2, at=(0.35, -1.7, 0))
    show(scene, stage, 0.9)
    trick = txt('vᵧ = ?', cfg.FONT["label"], cfg.MUTED).move_to([0, 3.0, 0])
    scene.play(FadeIn(trick), run_time=0.7)

    # --- 2. Has it stopped at the top? -------------------------------------------------------------------------------------
    beat(scene, t, 1)
    stopped = txt("stopped at the top?", cfg.FONT["section"], cfg.WHITE).move_to([0, 3.0, 0])
    scene.play(fade_through(trick, stopped), run_time=0.7)
    scene.play(flight.fly(P.apex_time, run_time=3.4, rate_func=lambda a: 1 - (1 - a) ** 2))

    # --- 3. Freeze: v_y = 0 -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    top = flight.world(P.apex_time)
    freeze = Disc(top, 0.42, cfg.WHITE, normal=(0, 0, 1), opacity=0.0, stroke=cfg.WHITE)
    stage.add_body(freeze)
    vy_zero = Tag(eq(r"v_y = 0", cfg.FONT["section"], cfg.Y_COLOR), top, UP * 0.85)
    vy_zero.presence = 0.0
    stage.add_overlay(vy_zero)
    scene.play(FadeOut(stopped), stage.fade(vy_zero, 1.0), run_time=0.8)

    # --- 4. But v_x is still 14.14 m/s --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    vx = flight.add_arrow("vx", cfg.X_COLOR, width=0.1)
    scene.play(stage.fade(vx, 1.0), run_time=0.8)
    vx_tag = Tag(eq(rf"v_x \approx {VX}\ \mathrm{{m/s}}", cfg.FONT["body"], cfg.X_COLOR), top + np.array([P.vx * flight.k, 0, 0]),
                 RIGHT * 2.1 + DOWN * 0.1)
    vx_tag.presence = 0.0
    stage.add_overlay(vx_tag)
    scene.play(stage.fade(vx_tag, 1.0), run_time=0.7)

    # --- 5. Still moving: slowest speed, not zero -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    speed = VGroup(txt("speed at the top", cfg.FONT["small"], cfg.MUTED),
                   eq(rf"{md.fixed(P.speed(P.apex_time), 2)}\ \mathrm{{m/s}}", cfg.FONT["title"], cfg.WHITE),
                   txt('vₘᵢₙ > 0', cfg.FONT["small"], cfg.GOLD)).arrange(DOWN, buff=0.2)
    speed.move_to([-4.4, 2.3, 0])
    scene.play(FadeIn(speed[:2], shift=UP * 0.15), run_time=0.9)
    scene.play(FadeIn(speed[2]), run_time=0.7)

    # --- 6. Acceleration still 9.8 m/s^2 down ----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    g_arrow = flight.add_arrow("g", cfg.ACCEL, width=0.1)
    scene.play(stage.fade(g_arrow, 1.0), run_time=0.8)
    g_tag = Tag(eq(rf"a = {G_TEXT}\ \mathrm{{m/s^2}}\ \downarrow", cfg.FONT["body"], cfg.ACCEL), top + np.array([0, -P.g * flight.k * 1.4, 0]),
                DOWN * 0.45 + RIGHT * 1.6)
    g_tag.presence = 0.0
    stage.add_overlay(g_tag)
    scene.play(stage.fade(g_tag, 1.0), run_time=0.7)
    on = txt('aᵧ = −g', cfg.FONT["label"], cfg.ACCEL).move_to([3.6, 3.0, 0])
    scene.play(FadeIn(on), run_time=0.7)

    # --- 7. If it did: a straight line forever -------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    drift = Knob(0.0)
    ghost = Ball(lambda: top + np.array([P.vx * drift.value * flight.s, 0, 0]), flight.radius * 0.9, cfg.BALL, layers=14)
    ghost.presence = 0.5
    line = Curve(lambda: [top, top + np.array([P.vx * max(drift.value, 1e-3) * flight.s, 0, 0])], cfg.MUTED, width=3, dashed=True,
                 glow=False)
    stage.add_body(line, ghost)
    off = txt('g = 0 ?', cfg.FONT["label"], cfg.MUTED).move_to([3.6, 3.0, 0])
    scene.play(fade_through(on, off), *[stage.fade(m, 0.0) for m in (vy_zero, vx_tag, g_tag)], run_time=0.6)
    scene.play(drift.to(stage, 2.6, run_time=2.6, rate_func=linear), flight.fly(run_time=2.6), run_time=2.6)

    # --- 8. Checklist -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    hide(scene, stage, 0.7, FadeOut(VGroup(off, speed)))
    rows = VGroup()
    for name, value in ((r"v_y", "= 0"), (r"v_x", r"\neq 0"), (r"|\vec{v}|", r"\neq 0"), (r"\vec{a}", r"\neq 0")):
        mark = check_mark(0.22, cfg.GREEN)
        color = {r"v_y": cfg.Y_COLOR, r"v_x": cfg.X_COLOR, r"|\vec{v}|": cfg.VELOCITY, r"\vec{a}": cfg.ACCEL}[name]
        rows.add(VGroup(eq([name, value], cfg.FONT["title"], color), mark).arrange(RIGHT, buff=0.5))
    rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.1)
    scene.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.35), run_time=2.4)

    # --- 9. Zero velocity in one direction does not mean zero acceleration -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    lesson = result_label('vᵧ = 0; aᵧ = −g', cfg.GOLD, cfg.FONT["body"]).move_to(DOWN * 3.2)
    scene.play(FadeIn(lesson, shift=UP * 0.15), run_time=1.0)
    scene.play(Indicate(rows[3], color=cfg.ACCEL, scale_factor=1.05), run_time=1.4)
    scene.wait(4.7)
    end_scene(scene, t, cfg.SCENE_DURATIONS["22"])
