"""Scene 20 — horizontal motion. On the 3D field the ball's floor shadow
(blue) carries the blue v_x arrow, which never changes. A strobe drops a
shadow mark every quarter second: equally spaced. Marks at 1 s and 2 s sit
at x(1) = 14.14 m and x(2) = 28.28 m, from ``physics_models.REFERENCE``.
"""

from manim_scenes.common import *


class Scene20Horizontal(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "20", "Horizontal motion")
    stage, flight = projectile_stage(pitch=0.42)
    flight.add_shadows(floor=True)
    vx_floor = Vector(lambda: flight.world(flight.t) * np.array([1, 0, 1]) + np.array([0, 0.02, 0]),
                      lambda: flight.world(flight.t) * np.array([1, 0, 1]) + np.array([P.vx * flight.k, 0.02, 0]),
                      cfg.X_COLOR, width=0.08, tip=0.24)
    vx_floor.presence = 0.0
    stage.add_overlay(vx_floor)
    show(scene, stage, 1.0)

    # --- 2. No sideways force: a_x = 0, v_x never changes ---------------------------------------------------------------
    beat(scene, t, 1)
    ax = paint(eq([r"a_x", "=", "0"], cfg.FONT["section"]), {0: cfg.X_COLOR}).move_to([-7.3, 3.45, 0], aligned_edge=LEFT)
    scene.play(Write(ax), run_time=1.0)
    scene.play(stage.fade(vx_floor, 1.0), run_time=0.5)
    scene.play(flight.realtime(speed=0.5))

    # --- 3. v_x = v0 cos(theta), all the way ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    vx_eq = paint(eq([r"v_x", "=", r"v_0\cos\theta"], cfg.FONT["section"]), {0: cfg.X_COLOR, 2: cfg.X_COLOR}).next_to(ax, DOWN, buff=0.3).align_to(ax, LEFT)
    scene.play(Write(vx_eq), run_time=1.2)
    rewind(scene, flight, 0.6)
    scene.play(flight.realtime(speed=0.8))

    # --- 4. x = v0 cos(theta) t ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    x_eq = paint(eq([r"x", "=", r"v_0\cos\theta\ t"], cfg.FONT["section"]), {0: cfg.X_COLOR, 2: cfg.X_COLOR}).next_to(vx_eq, DOWN, buff=0.3).align_to(ax, LEFT)
    scene.play(Write(x_eq), run_time=1.4)
    scene.play(Indicate(x_eq, color=cfg.X_COLOR, scale_factor=1.05), run_time=1.0)

    # --- 5. The floor shadow, strobed: equally spaced ------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    times = np.arange(0.0, P.flight_time + 1e-6, 0.25)
    marks = []
    for when in times:
        disc = Disc(flight.world(float(when)) * np.array([1, 0, 1]) + np.array([0, 0.015, 0]), 0.13, cfg.X_COLOR, opacity=0.8)
        disc.presence = 0.0
        marks.append(disc)
    stage.add_body(*marks)
    rewind(scene, flight, 0.6)

    def strobe(m, dt):
        for when, disc in zip(times, marks):
            if flight.t >= when - 1e-6:
                disc.presence = 1.0

    stage.add_updater(strobe)
    scene.play(flight.realtime(speed=0.6))
    equal = txt("equal spacing", cfg.FONT["label"], cfg.X_COLOR).move_to([3.8, 2.6, 0])
    scene.play(FadeIn(equal), run_time=0.6)

    # --- 6. x = 14.14 t -----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    stage.remove_updater(strobe)
    numbers = paint(eq([r"x", r"\approx", rf"{VX}\,t"], cfg.FONT["section"]), {0: cfg.X_COLOR, 2: cfg.X_COLOR}).next_to(x_eq, DOWN, buff=0.35).align_to(ax, LEFT)
    scene.play(Write(numbers), FadeOut(equal), run_time=1.2)

    # --- 7. After one second ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    tags = []
    for second in (1, 2):
        where = flight.world(float(second)) * np.array([1, 0, 1])
        tag = Tag(VGroup(txt(f"{second} s", cfg.FONT["small"], cfg.WHITE),
                         eq(rf"{md.fixed(float(P.x(second)), 2)}\ \mathrm{{m}}", cfg.FONT["small"], cfg.X_COLOR)).arrange(DOWN, buff=0.1),
                  where, DOWN * 0.75)
        tag.presence = 0.0
        tags.append(tag)
    stage.add_overlay(*tags)
    ring1 = Disc(flight.world(1.0) * np.array([1, 0, 1]) + np.array([0, 0.02, 0]), 0.26, cfg.WHITE, opacity=0.0, stroke=cfg.WHITE)
    stage.add_body(ring1)
    scene.play(stage.fade(tags[0], 1.0), run_time=0.8)
    scene.play(Indicate(numbers, color=cfg.X_COLOR, scale_factor=1.05), run_time=1.0)

    # --- 8. After two seconds: equal distances in equal times ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    ring2 = Disc(flight.world(2.0) * np.array([1, 0, 1]) + np.array([0, 0.02, 0]), 0.26, cfg.WHITE, opacity=0.0, stroke=cfg.WHITE)
    stage.add_body(ring2)
    scene.play(stage.fade(tags[1], 1.0), run_time=0.8)
    same = txt('Δx = vₓΔt', cfg.FONT["label"], cfg.WHITE).move_to([3.4, 2.6, 0])
    scene.play(FadeIn(same), run_time=0.8)

    # --- 9. Gravity pulls straight down: no sideways part -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(same), *[stage.fade(m, 0.0) for m in (*tags, ring1, ring2)], run_time=0.6)
    g_arrow = flight.add_arrow("g", cfg.ACCEL, width=0.09)
    rewind(scene, flight, 0.6)
    scene.play(stage.fade(g_arrow, 1.0), run_time=0.5)
    straight = txt('aₓ = 0', cfg.FONT["label"], cfg.ACCEL).move_to([3.4, 2.6, 0])
    scene.play(FadeIn(straight), flight.realtime(speed=0.5), run_time=P.flight_time / 0.5)

    # --- 10. Uniform and predictable ---------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    uniform = result_label('vₓ = constant', cfg.X_COLOR, cfg.FONT["section"]).move_to([3.4, 2.6, 0])
    scene.play(fade_through(straight, uniform), run_time=0.8)
    scene.play(Indicate(VGroup(ax, vx_eq, x_eq), color=cfg.X_COLOR, scale_factor=1.03), run_time=1.2)

    # --- 11. The vertical motion is different -------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    vy_arrow = flight.add_arrow("vy", cfg.Y_COLOR, width=0.08)
    rewind(scene, flight, 0.6)
    nxt = txt('Vertical motion', cfg.FONT["section"], cfg.Y_COLOR).move_to([3.0, 2.6, 0])
    scene.play(fade_through(uniform, nxt), stage.fade(vy_arrow, 1.0), stage.fade(g_arrow, 0.0), run_time=0.8)
    scene.play(flight.realtime(speed=0.5))
    scene.wait(1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["20"])
