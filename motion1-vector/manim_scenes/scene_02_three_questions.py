"""Scene 02 — what it takes to describe motion: position (teal, from the
origin), velocity (gold, along the path) and acceleration (orange, straight
down), all live on the reference flight seen from the side. Then two cars at
the same speed, one east and one north, end up in different places; and the
ball's own speed and direction readouts show that direction is the part that
keeps changing.
"""

from manim_scenes.common import *

GRID_AT = (-1.0, -2.7, 0)


class Scene02ThreeQuestions(Scene):
    def construct(self) -> None:
        play_scene(self)


def question(label: str, answer: str, color: str) -> VGroup:
    q = txt(label, cfg.FONT["small"], cfg.MUTED)
    a = txt(answer, cfg.FONT["body"], color)
    group = VGroup(q, a).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    group.q, group.a = q, a
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "Where, how fast, which way?")
    grid = plane((0, 45), (0, 15), unit=0.178, at=GRID_AT, step=5, faint=0.3)
    flight = SideFlight(grid, k=0.07)
    flight.clock.value = 0.95
    flight._draw_trail(flight.trail)
    flight.ball.move_to(flight.point(0.95))
    scene.play(FadeIn(grid), FadeIn(flight.trail), FadeIn(flight.ball), run_time=1.2)

    asks = VGroup(question("Where is it?", "position", cfg.POSITION),
                  question("How fast, which way?", "velocity", cfg.VELOCITY),
                  question("How is that changing?", "acceleration", cfg.ACCEL)).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
    asks.move_to([-4.9, -0.3, 0])
    r = flight.arrow("r", cfg.POSITION)
    v = flight.arrow("v", cfg.VELOCITY)
    a = flight.arrow("a", cfg.ACCEL)
    origin_dot = glow_dot(grid.c2p(0, 0), cfg.POSITION, 0.07)

    # --- 2. Position -----------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.add(r)
    scene.play(FadeIn(asks[0]), FadeIn(origin_dot), r.grow_in(run_time=1.2), run_time=1.2)

    # --- 3. Velocity -------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.add(v)
    scene.play(FadeIn(asks[1]), v.grow_in(run_time=1.2), run_time=1.2)

    # --- 4. Acceleration ---------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.add(a)
    scene.play(FadeIn(asks[2]), a.grow_in(run_time=1.0), run_time=1.0)
    scene.play(flight.fly(speed=0.5))

    # --- 5. Two cars at ten metres per second -----------------------------------------------------------------------
    beat(scene, t, 4)
    for arrow in (r, v, a):
        arrow.clear_updaters()
    scene.play(FadeOut(VGroup(grid, flight.trail, flight.ball, r, v, a, asks, origin_dot, head)), run_time=0.8)
    home = np.array([-2.6, -2.2, 0])
    roads = VGroup(Line(home + LEFT * 0.6, home + RIGHT * 7.4, stroke_color=cfg.GRAY, stroke_width=36, stroke_opacity=0.35),
                   Line(home + DOWN * 0.6, home + UP * 5.2, stroke_color=cfg.GRAY, stroke_width=36, stroke_opacity=0.35))
    dashes = VGroup(dashed_path(home + RIGHT * 0.4, home + RIGHT * 7.3, cfg.WHITE, 3, 0.5, 0.25),
                    dashed_path(home + UP * 0.4, home + UP * 5.1, cfg.WHITE, 3, 0.5, 0.25))
    east, north = Car(cfg.CYAN), Car(cfg.ROSE)
    pos = Knob(0.0)
    east.add_updater(lambda m: m.set_pose(home + RIGHT * (0.75 + pos.value), 0.0))
    north.add_updater(lambda m: m.set_pose(home + UP * (0.75 + pos.value), PI / 2))
    ve = VecArrow(lambda: east.pose[0] + RIGHT * 0.65, lambda: east.pose[0] + RIGHT * 1.85, cfg.VELOCITY, width=0.09)
    vn = VecArrow(lambda: north.pose[0] + UP * 0.65, lambda: north.pose[0] + UP * 1.85, cfg.VELOCITY, width=0.09)
    rose = compass([-6.2, 2.0, 0])
    gauges = VGroup(Speedometer([5.3, 1.75, 0], value=pm.TWO_CARS, radius=1.0, color=cfg.CYAN),
                    Speedometer([5.3, -1.3, 0], value=pm.TWO_CARS, radius=1.0, color=cfg.ROSE))
    names = VGroup(txt("east", cfg.FONT["small"], cfg.CYAN).next_to(gauges[0], LEFT, buff=0.3),
                   txt("north", cfg.FONT["small"], cfg.ROSE).next_to(gauges[1], LEFT, buff=0.3))
    scene.play(FadeIn(roads), FadeIn(dashes), FadeIn(rose), FadeIn(east), FadeIn(north), run_time=1.0)
    scene.add(ve, vn)
    scene.play(FadeIn(gauges), FadeIn(names), ve.grow_in(run_time=0.8), vn.grow_in(run_time=0.8), run_time=0.8)
    scene.play(pos.to(east, 2.9, run_time=5.0, rate_func=linear))

    # --- 6. Same speed, different velocity --------------------------------------------------------------------------------
    beat(scene, t, 5)
    same = VGroup(txt("same speed", cfg.FONT["label"], cfg.WHITE), eq(r"10\ \mathrm{m/s}", cfg.FONT["label"], cfg.WHITE))
    same.arrange(RIGHT, buff=0.3).move_to([3.0, 3.6, 0])
    differ = txt("different velocities", cfg.FONT["label"], cfg.VELOCITY).move_to([3.0, -3.7, 0])
    gap = dashed_path(east.pose[0], north.pose[0], cfg.GOLD, 3, 0.8)
    scene.play(FadeIn(same, shift=DOWN * 0.15), run_time=0.8)
    scene.play(Create(gap), FadeIn(differ, shift=UP * 0.15), run_time=1.2)

    # --- 7. The ball: speed changes a little, direction all the time -------------------------------------------------------------
    beat(scene, t, 6)
    for mob in (east, north, ve, vn):
        mob.clear_updaters()
    scene.play(FadeOut(VGroup(roads, dashes, rose, east, north, ve, vn, gauges, names, same, differ, gap)), run_time=0.8)
    grid2 = plane((0, 45), (0, 15), unit=0.19, at=(-5.6, -2.5, 0), step=5, faint=0.3)
    side = SideFlight(grid2, k=0.07)
    vv = side.arrow("v", cfg.VELOCITY)
    speed = lambda: float(np.linalg.norm(side.velocity()))  # noqa: E731
    angle = lambda: float(np.degrees(np.arctan2(side.velocity()[1], side.velocity()[0])))  # noqa: E731
    speed_num = DecimalNumber(speed(), num_decimal_places=1, font_size=60, color=cfg.WHITE)
    speed_num.add_updater(lambda m: m.set_value(speed()))
    angle_num = DecimalNumber(angle(), num_decimal_places=0, font_size=60, color=cfg.VELOCITY, include_sign=True)
    angle_num.add_updater(lambda m: m.set_value(angle()))
    rows = VGroup(VGroup(txt("speed", cfg.FONT["small"], cfg.MUTED), speed_num, txt("m/s", cfg.FONT["small"], cfg.MUTED)),
                  VGroup(txt("direction", cfg.FONT["small"], cfg.MUTED), angle_num, txt("°", cfg.FONT["small"], cfg.VELOCITY)))
    for row in rows:
        row.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([4.6, 0.6, 0])
    back = panel(rows.width + 0.8, rows.height + 0.8).move_to(rows)
    scene.add(vv)
    scene.play(FadeIn(grid2), FadeIn(side.trail), FadeIn(side.ball), FadeIn(back), FadeIn(rows),
               vv.grow_in(run_time=0.8), run_time=0.8)
    scene.play(side.fly(speed=0.45))

    # --- 8. Direction matters too ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    matters = result_label('Direction', cfg.GOLD, cfg.FONT["section"]).move_to([0, 3.55, 0])
    scene.play(FadeIn(matters, shift=DOWN * 0.15), Indicate(angle_num, color=cfg.GOLD, scale_factor=1.15), run_time=1.0)
    side.clock.value = 0.0
    scene.play(side.fly(speed=0.6))

    # --- 9. First: quantities with no direction at all --------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    vv.clear_updaters()
    speed_num.clear_updaters()
    angle_num.clear_updaters()
    scene.play(FadeOut(VGroup(grid2, side.trail, side.ball, vv, back, rows)), matters.animate.move_to(UP * 2.6), run_time=1.0)
    next_up = VGroup(txt("magnitude only?", cfg.FONT["section"], cfg.WHITE),
                     txt("scalars", cfg.FONT["title"], cfg.CYAN)).arrange(DOWN, buff=0.3).next_to(matters, DOWN, buff=0.55)
    scene.play(FadeIn(next_up[0], shift=UP * 0.15), run_time=0.9)
    scene.play(FadeIn(next_up[1], scale=0.9), run_time=1.0)
    cards = VGroup(*[scalar_card(name, value, cfg.WHITE, width=3.3) for name, value in pm.SCALARS[:3]])
    cards.arrange(RIGHT, buff=0.45).next_to(next_up, DOWN, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3), run_time=2.2)
    scene.play(Indicate(next_up[1], color=cfg.CYAN, scale_factor=1.08), run_time=1.4)
    scene.wait(1.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
