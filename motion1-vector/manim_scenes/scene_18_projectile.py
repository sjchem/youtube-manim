"""Scene 18 — what projectile motion is. On the 3D field the reference throw
flies with its orange gravity arrow attached: the same length, the same
direction, rising, at the top and falling (a strobe of five ghost images
carries five identical arrows). The model's assumptions are stated once:
no air, gravity only, g = 9.8 m/s^2 and constant. Then a = -g j: a_x = 0,
a_y = -g, and the two velocity components set off on different paths.
"""

from manim_scenes.common import *


class Scene18Projectile(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "18")
    opener = txt("Projectile motion", cfg.FONT["title"], cfg.WHITE)
    fit_width(opener, 12.4)
    opener.move_to(ORIGIN)
    scene.play(FadeIn(opener, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(0.9)
    scene.play(FadeOut(opener, shift=UP * 0.3), run_time=0.6)
    stage, flight = projectile_stage()
    show(scene, stage, 1.0)

    # --- 2. No air: only gravity after launch -------------------------------------------------------------------------
    beat(scene, t, 1)
    rules = VGroup(chip("no air resistance", cfg.CYAN), chip("only gravity", cfg.ACCEL)).arrange(RIGHT, buff=0.5).move_to(UP * 3.45)
    scene.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.2) for r in rules], lag_ratio=0.4), run_time=1.2)
    g_arrow = flight.add_arrow("g", cfg.ACCEL, width=0.09)
    scene.play(stage.fade(g_arrow, 1.0), run_time=0.5)
    scene.play(flight.realtime(1.6, speed=0.6))

    # --- 3. g = 9.8 m/s^2, the same for everything ----------------------------------------------------------------------------
    beat(scene, t, 2)
    g_val = paint(eq([r"g", r"\approx", rf"{G_TEXT}\ \mathrm{{m/s^2}}"], cfg.FONT["section"]), {0: cfg.ACCEL, 2: cfg.ACCEL})
    g_val.move_to([-7.3, 2.45, 0], aligned_edge=LEFT)
    scene.play(Write(g_val), run_time=1.4)
    scene.play(flight.realtime(speed=0.6))

    # --- 4. Constant: a ball never rises far enough to weaken gravity -----------------------------------------------------------------
    beat(scene, t, 3)
    const = chip("g constant", cfg.ACCEL).next_to(rules, RIGHT, buff=0.5)
    VGroup(rules, const).arrange(RIGHT, buff=0.45).move_to(UP * 3.45)
    scene.play(FadeIn(const, shift=DOWN * 0.2), run_time=0.6)
    rewind(scene, flight)
    scene.play(flight.realtime(speed=0.6))
    height = Tag(txt(f"{H_MAX} m", cfg.FONT["small"], cfg.Y_COLOR), flight.at_metres(P.vx * P.apex_time, P.max_height), UP * 0.5)
    height.presence = 0.0
    stage.add_overlay(height)
    scene.play(stage.fade(height, 1.0), run_time=0.6)
    earth = txt("Earth's radius: 6 400 000 m", cfg.FONT["small"], cfg.MUTED).next_to(g_val, DOWN, buff=0.35).align_to(g_val, LEFT)
    scene.play(FadeIn(earth), run_time=0.6)

    # --- 5. x right, y up: a = -g j ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(earth), stage.fade(height, 0.0), run_time=0.5)
    o = np.array([-2.4, 0.02, 1.9])
    x_axis = Vector(o, o + RIGHT * 1.6, cfg.X_COLOR, width=0.06, tip=0.22)
    y_axis = Vector(o, o + UP * 1.2, cfg.Y_COLOR, width=0.06, tip=0.22)
    x_tag = Tag(eq("x", cfg.FONT["body"], cfg.X_COLOR), o + RIGHT * 1.6, RIGHT * 0.3)
    y_tag = Tag(eq("y", cfg.FONT["body"], cfg.Y_COLOR), o + UP * 1.2, UP * 0.3)
    for m in (x_axis, y_axis, x_tag, y_tag):
        m.presence = 0.0
    stage.add_overlay(x_axis, y_axis, x_tag, y_tag)
    scene.play(*[stage.fade(m, 1.0) for m in (x_axis, y_axis, x_tag, y_tag)], run_time=0.8)
    a_vec = paint(eq([r"\vec{a}", "=", r"-g\,\hat{\jmath}"], cfg.FONT["title"]), {0: cfg.ACCEL, 2: cfg.ACCEL}).next_to(g_val, DOWN, buff=0.45).align_to(g_val, LEFT)
    scene.play(Write(a_vec), run_time=1.4)

    # --- 6. a_x = 0 ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    ax = paint(eq([r"a_x", "=", "0"], cfg.FONT["section"]), {0: cfg.X_COLOR}).move_to([3.4, 2.5, 0], aligned_edge=LEFT)
    scene.play(Write(ax), run_time=1.0)

    # --- 7. a_y = -g --------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    ay = paint(eq([r"a_y", "=", r"-g"], cfg.FONT["section"]), {0: cfg.Y_COLOR, 2: cfg.ACCEL}).next_to(ax, DOWN, buff=0.35).align_to(ax, LEFT)
    scene.play(Write(ay), run_time=1.0)

    # --- 8. The gravity arrow never changes -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(*[stage.fade(m, 0.0) for m in (x_axis, y_axis, x_tag, y_tag)], run_time=0.5)
    times = [P.flight_time * k / 4 for k in range(5)]
    ghosts = flight.add_ghosts(times, alpha=0.5)
    ghost_g = []
    for when in times:
        here = flight.world(when)
        arrow = Vector(here, here + np.array([0, -P.g * flight.k * 1.4, 0]), cfg.ACCEL, width=0.07, tip=0.22)
        arrow.presence = 0.0
        ghost_g.append(arrow)
    stage.add_overlay(*ghost_g)
    rewind(scene, flight, 0.6)
    scene.play(flight.realtime(speed=0.65))
    scene.play(*[stage.fade(a, 0.8) for a in ghost_g], run_time=0.8)
    same = txt('g = constant', cfg.FONT["label"], cfg.ACCEL).move_to([-0.6, 2.5, 0])
    scene.play(FadeIn(same), run_time=0.6)

    # --- 9. Two motions, one clock ----------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(same), *[stage.fade(a, 0.0) for a in ghost_g], *[stage.fade(gh, 0.0) for gh in ghosts],
               stage.fade(g_arrow, 0.0), run_time=0.6)
    vx = flight.add_arrow("vx", cfg.X_COLOR, width=0.08)
    vy = flight.add_arrow("vy", cfg.Y_COLOR, width=0.08)
    rewind(scene, flight, 0.6)
    scene.play(stage.fade(vx, 1.0), stage.fade(vy, 1.0), run_time=0.5)
    steady = txt("steady", cfg.FONT["label"], cfg.X_COLOR).move_to([-0.8, 2.6, 0])
    changing = txt("changing", cfg.FONT["label"], cfg.Y_COLOR).next_to(steady, DOWN, buff=0.3)
    scene.play(FadeIn(steady), FadeIn(changing), run_time=0.6)
    scene.play(flight.realtime(speed=0.5))

    # --- 10. First: split the launch velocity --------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    rewind(scene, flight, 0.6, to=0.02)
    vel = flight.add_arrow("v", cfg.VELOCITY, width=0.1)
    scene.play(stage.fade(vel, 1.0), stage.zoom_to(1.55, run_time=1.6), stage.glide([3.4, -2.0, 0], run_time=1.6), run_time=1.6)
    split = txt('v₀ₓ · v₀ᵧ', cfg.FONT["section"], cfg.GOLD).move_to([0, 3.4, 0])
    scene.play(fade_through(VGroup(rules, const), split), run_time=0.8)
    scene.wait(2.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["18"])
