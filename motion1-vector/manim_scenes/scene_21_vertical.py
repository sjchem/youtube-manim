"""Scene 21 — vertical motion, demonstrated before equations. The
wall shadow (rose) immediately rises, stops and falls, carrying a rose v_y arrow that
shrinks to zero at the top and then grows downward. A live v_y-t graph draws
the straight line v_y = 14.14 - 9.8 t through zero at 1.44 s. Finally all
three — floor shadow, wall shadow and ball — move together, and the gold
velocity arrow is exactly the sum of its blue and rose parts.
"""

from manim_scenes.common import *


class Scene21Vertical(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "21", "Vertical motion")
    stage, flight = projectile_stage(wall=True, yaw=-0.62, pitch=0.3, zoom=1.22, at=(0.4, -1.2, 0))
    flight.add_shadows(floor=True, wall_x=WALL_X)
    flight.floor_shadow.presence = 0.0
    wall_v = Vector(lambda: np.array([WALL_X + 0.02, flight.world(flight.t)[1], 0.0]),
                    lambda: np.array([WALL_X + 0.02, flight.world(flight.t)[1] + float(P.vy(flight.t)) * flight.k, 0.0]),
                    cfg.Y_COLOR, width=0.08, tip=0.24)
    wall_v.presence = 0.0
    wall_v.keep_in_frame = True
    stage.add_overlay(wall_v)
    g_arrow = flight.add_arrow("g", cfg.ACCEL, width=0.09)
    show(scene, stage, 0.8)
    scene.play(stage.fade(wall_v, 1.0), run_time=0.3)
    scene.play(flight.realtime(P.apex_time * 0.8, speed=0.38))

    # Show the motion first: the upward component reaches zero while gravity stays down.
    beat(scene, t, 1)
    scene.play(stage.fade(g_arrow, 1.0), run_time=0.3)
    scene.play(flight.realtime(P.apex_time, speed=0.3))
    apex_zero = eq(r"v_y = 0", cfg.FONT["section"], cfg.Y_COLOR).move_to([4.8, 2.5, 0])
    scene.play(FadeIn(apex_zero), run_time=0.5)

    # Fall immediately; the downward velocity arrow grows as the shadow descends.
    beat(scene, t, 2)
    scene.play(FadeOut(apex_zero), run_time=0.3)
    scene.play(flight.realtime(speed=0.45))

    # One compact equation accompanies the moving velocity graph.
    beat(scene, t, 3)
    scene.play(stage.fade(g_arrow, 0.0), run_time=0.3)
    rewind(scene, flight, 0.6)
    vy_num = paint(eq([r"v_y", r"\approx", VY0, rf"-\,{G_TEXT}\,t"], cfg.FONT["body"]), {0: cfg.Y_COLOR, 2: cfg.Y_COLOR, 3: cfg.ACCEL})
    vy_num.move_to([5.0, 2.9, 0])
    axes = Axes(x_range=(0, 3, 1), y_range=(-16, 16, 8), x_length=3.6, y_length=3.0, tips=False,
                axis_config={"stroke_color": cfg.MUTED, "stroke_width": 2.5}).move_to([5.3, 0.7, 0])
    graph_lab = VGroup(eq("v_y", cfg.FONT["small"], cfg.Y_COLOR).next_to(axes.y_axis.get_top(), LEFT, buff=0.15),
                       eq("t", cfg.FONT["small"], cfg.TIME).next_to(axes.x_axis.get_end(), RIGHT, buff=0.12))
    scene.play(Write(vy_num), FadeIn(axes), FadeIn(graph_lab), run_time=0.8)
    line = always_redraw(lambda: axes.plot(lambda x: float(P.vy(x)), x_range=(0, max(flight.t, 0.01)), color=cfg.Y_COLOR,
                                           stroke_width=5))
    dot = always_redraw(lambda: glow_dot(axes.c2p(flight.t, float(P.vy(flight.t))), cfg.Y_COLOR, 0.07))
    scene.add(line, dot)
    scene.play(flight.realtime(P.apex_time * 0.85, speed=0.45))

    # At the top, zero.
    beat(scene, t, 4)
    scene.play(flight.realtime(P.apex_time, speed=0.45))
    zero = eq(r"v_y = 0", cfg.FONT["body"], cfg.Y_COLOR).next_to(axes.c2p(P.apex_time, 0), UP, buff=0.35)
    scene.play(FadeIn(zero), run_time=0.6)

    # Then negative: falling faster and faster.
    beat(scene, t, 5)
    scene.play(flight.realtime(speed=0.6))

    # Gravity never changed direction.
    beat(scene, t, 6)
    rewind(scene, flight, 0.6)
    scene.play(stage.fade(g_arrow, 1.0), FadeOut(zero), run_time=0.5)
    never = txt('aᵧ = −g', cfg.FONT["label"], cfg.ACCEL).move_to([-1.6, 2.9, 0])
    scene.play(FadeIn(never), flight.realtime(speed=0.55), run_time=P.flight_time / 0.55)

    # Both shadows together.
    beat(scene, t, 7)
    for m in (line, dot):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(never, axes, graph_lab, line, dot, vy_num)), stage.fade(g_arrow, 0.0), run_time=0.6)
    floor_v = Vector(lambda: flight.world(flight.t) * np.array([1, 0, 1]) + np.array([0, 0.02, 0]),
                     lambda: flight.world(flight.t) * np.array([1, 0, 1]) + np.array([P.vx * flight.k, 0.02, 0]),
                     cfg.X_COLOR, width=0.08, tip=0.24)
    floor_v.presence = 0.0
    stage.add_overlay(floor_v)
    rewind(scene, flight, 0.6)
    scene.play(stage.fade(flight.floor_shadow, 1.0), stage.fade(floor_v, 1.0), *stage.turn(yaw=-0.5, pitch=0.38, run_time=1.0),
               run_time=1.0)
    labels = VGroup(txt('x(t)', cfg.FONT["label"], cfg.X_COLOR), txt('y(t)', cfg.FONT["label"], cfg.Y_COLOR))
    labels.arrange(RIGHT, buff=0.8).move_to([0, 2.9, 0])
    scene.play(FadeIn(labels), flight.realtime(speed=0.65), run_time=P.flight_time / 0.65)

    # The ball does both: v = v_x + v_y.
    beat(scene, t, 8)
    for name, color in (("v", cfg.VELOCITY), ("vx", cfg.X_COLOR), ("vy", cfg.Y_COLOR)):
        flight.add_arrow(name, color, width=0.1 if name == "v" else 0.075)
    rewind(scene, flight, 0.6)
    scene.play(*[stage.fade(flight.arrows[n], 1.0) for n in ("v", "vx", "vy")], run_time=0.5)
    vsum = paint(eq([r"\vec{v}", "=", r"v_x\,\hat{\imath}", "+", r"v_y\,\hat{\jmath}"], cfg.FONT["section"]),
                 {0: cfg.VELOCITY, 2: cfg.X_COLOR, 4: cfg.Y_COLOR}).move_to([4.2, 2.3, 0])
    scene.play(FadeOut(labels), run_time=0.4)
    scene.play(Write(vsum), run_time=0.8)
    scene.play(flight.realtime(speed=0.42))

    # Two independent motions, one clock.
    beat(scene, t, 9)
    secret = result_label('t', cfg.GOLD, cfg.FONT["section"]).move_to([-2.4, 2.8, 0])
    rewind(scene, flight, 0.6)
    scene.play(FadeIn(secret, shift=DOWN * 0.15), flight.realtime(speed=0.4), run_time=P.flight_time / 0.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["21"])
