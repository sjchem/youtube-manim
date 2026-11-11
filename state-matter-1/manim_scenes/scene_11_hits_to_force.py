"""Scene 11 — from hits to force. One molecule bounces between two walls a
distance L apart at speed v_x (``physics_models.single_molecule_hits``); a
force-time graph below records a spike at each hit on the right wall, every
2L / v_x. Each spike's area is the impulse 2 m v_x. Spread each spike evenly
over the interval to the next and the rectangles tile into a flat line of
the same total area: the average force. The algebra follows on screen:
2 m v_x / (2L / v_x) = m v_x^2 / L.
"""

from manim_scenes.common import *

LEFT_X, RIGHT_X, LANE_Y = -6.0, -1.0, 2.15
L = RIGHT_X - LEFT_X - 0.36                       # travel between the walls for a ball of radius 0.18
VX = 2 * L / 2.0                                  # one round trip every 2.0 s
SPIKE_W, SPIKE_H = 0.6, 2.3                       # a hit, drawn as a narrow triangle of this width and height
END = 12.6


class Scene11HitsToForce(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "From hits to force")
    clock = Knob(0.0)
    start_phase = 0.4                               # fold coordinate at t = 0
    hits = pm.single_molecule_hits(VX, L, END - 1e-6, start=start_phase)
    gap = float(hits[1] - hits[0])

    def ball_x() -> float:
        return LEFT_X + 0.18 + L * float(pm.fold(start_phase + VX * clock.value / L))

    walls = VGroup(*[Rectangle(width=0.22, height=1.4, stroke_width=0, fill_color=cfg.GLASS, fill_opacity=0.6).move_to([x, LANE_Y, 0])
                     for x in (LEFT_X - 0.11, RIGHT_X + 0.11)])
    walls[1].set_fill(cfg.IMPULSE, opacity=0.7)
    floor = Line([LEFT_X, LANE_Y - 0.7, 0], [RIGHT_X, LANE_Y - 0.7, 0], stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5)
    ball = bead([ball_x(), LANE_Y, 0], cfg.FOLLOWED, 0.18, glow=1.0)
    ball.add_updater(lambda m: m.move_to([ball_x(), LANE_Y, 0]))
    span = VGroup(DoubleArrow([LEFT_X, LANE_Y + 0.95, 0], [RIGHT_X, LANE_Y + 0.95, 0], stroke_color=cfg.VOLUME, stroke_width=3,
                              buff=0, tip_length=0.2), eq("L", cfg.FONT["body"], cfg.VOLUME).move_to([(LEFT_X + RIGHT_X) / 2, LANE_Y + 1.35, 0]))
    axes = plot_axes((0, END), (0, 2.6), x_length=12.4, y_length=2.6, at=[0.0, -1.55, 0], x_label="t", y_label="F",
                     y_color=cfg.IMPULSE)

    def spikes_until(now: float) -> VGroup:
        group = VGroup()
        for h in hits:
            if h - SPIKE_W / 2 > now:
                break
            grow = float(np.clip((now - (h - SPIKE_W / 2)) / SPIKE_W, 0, 1))
            group.add(Polygon(axes.c2p(h - SPIKE_W / 2, 0), axes.c2p(h, SPIKE_H * min(1.0, grow * 2)),
                              axes.c2p(h + SPIKE_W / 2 if grow > 0.5 else h - SPIKE_W / 2 + grow * SPIKE_W, 0),
                              stroke_color=cfg.IMPULSE, stroke_width=2.5, fill_color=cfg.IMPULSE, fill_opacity=0.55))
        return group

    spikes = live(VGroup(), lambda: spikes_until(clock.value))
    scene.play(FadeIn(walls), Create(floor), FadeIn(ball), run_time=1.0)
    asks = VGroup(chip("how big is each push?", cfg.IMPULSE), chip("how often?", cfg.VELOCITY)).arrange(DOWN, buff=0.3,
                                                                                                           aligned_edge=LEFT)
    asks.move_to([3.6, 2.4, 0])
    scene.play(FadeIn(asks[0], shift=LEFT * 0.2), clock.to(ball, 0.8, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(FadeIn(asks[1], shift=LEFT * 0.2), clock.to(ball, 1.8, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(clock.to(ball, 4.0, run_time=2.2, rate_func=linear), run_time=2.2)

    # --- 2. Cross the box and back: 2L at v_x ----------------------------------------------------------------------------------
    beat(scene, t, 1)
    trip = VGroup(Arrow([RIGHT_X - 0.2, LANE_Y - 0.35, 0], [LEFT_X + 0.2, LANE_Y - 0.35, 0], stroke_color=cfg.VELOCITY,
                        stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.06),
                  Arrow([LEFT_X + 0.2, LANE_Y - 0.55, 0], [RIGHT_X - 0.2, LANE_Y - 0.55, 0], stroke_color=cfg.VELOCITY,
                        stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.06))
    two_l = eq(r"2L \text{ at } v_x", cfg.FONT["body"], cfg.VELOCITY).move_to([3.6, 1.0, 0])
    scene.play(FadeIn(span), FadeOut(asks), run_time=0.9)
    scene.play(FadeIn(trip), FadeIn(two_l, shift=LEFT * 0.2), clock.to(ball, 5.0, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(clock.to(ball, 12.5, run_time=9.0, rate_func=linear), run_time=9.0)

    # --- 3. Time between hits: 2L / v_x -------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    dt_eq = eq(r"\Delta t = \frac{2L}{v_x}", cfg.FONT["section"], cfg.WHITE).move_to([3.6, 2.6, 0])
    scene.play(FadeOut(trip), FadeIn(dt_eq, shift=DOWN * 0.1), run_time=1.0)
    clock.value = 0.0
    scene.play(clock.to(ball, 3.0, run_time=3.0, rate_func=linear), run_time=3.0)

    # --- 4. Force against time: a spike at each hit, area 2 m v_x --------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(Create(axes), FadeOut(two_l), run_time=1.0)
    clock.value = 0.0
    scene.add(spikes)
    fast = 1.45                                      # the clock runs a little faster than real time here
    scene.play(clock.to(ball, hits[2] + 0.5, rate_func=linear), run_time=(hits[2] + 0.5) / fast)
    area = eq(r"\text{area} = 2 m v_x", cfg.FONT["label"], cfg.IMPULSE).next_to(axes.c2p(hits[0], SPIKE_H), UR, buff=0.12)
    scene.play(FadeIn(area, shift=DOWN * 0.1), run_time=0.8)
    play_in(scene, t, 4, clock.to(ball, END - 0.1, rate_func=linear), run_time=(END - 0.1 - clock.value) / fast)

    # --- 5. Spread each spike over its interval: a steady force of the same area ------------------------------------------------------
    beat(scene, t, 4)
    spikes.clear_updaters()
    level = SPIKE_H * SPIKE_W / 2 / gap
    blocks = VGroup(*[Polygon(axes.c2p(h, 0), axes.c2p(min(h + gap, END), 0), axes.c2p(min(h + gap, END), level),
                              axes.c2p(h, level), stroke_color=cfg.IMPULSE, stroke_width=2, fill_color=cfg.IMPULSE,
                              fill_opacity=0.55) for h in hits])
    blocks = VGroup(*blocks[:len(spikes)])
    scene.play(FadeOut(area), run_time=0.5)
    scene.play(*[Transform(spike, block) for spike, block in zip(spikes, blocks)], run_time=3.0)
    mean = Line(axes.c2p(hits[0], level), axes.c2p(END, level), stroke_color=cfg.GOLD, stroke_width=6)
    steady = txt("same area, steady force", cfg.FONT["label"], cfg.GOLD).next_to(axes.c2p(END * 0.62, level), UP, buff=0.55)
    scene.play(Create(mean), FadeIn(steady, shift=DOWN * 0.1), run_time=1.4)
    scene.wait(3.0)

    # --- 6. Average force = push / time between pushes -------------------------------------------------------------------------------
    beat(scene, t, 5)
    avg = eq([r"\bar F", "=", r"\frac{2 m v_x}{2L/v_x}"], cfg.FONT["section"], cfg.WHITE)
    avg[0].set_color(cfg.GOLD)
    avg.move_to([3.6, 2.4, 0])
    scene.play(FadeOut(dt_eq), FadeOut(steady), run_time=0.6)
    scene.play(Write(avg), run_time=1.8)
    scene.wait(2.0)

    # --- 7. The twos cancel; v_x moves up: m v_x^2 / L -------------------------------------------------------------------------------
    beat(scene, t, 6)
    result = paint(eq([r"\bar F", "=", r"\frac{m v_x^2}{L}"], cfg.FONT["section"], cfg.WHITE), {0: cfg.GOLD})
    result.move_to([3.6, 2.4, 0])
    slashes = VGroup(cancel(avg[2][0]), cancel(avg[2][6]))
    scene.play(Create(slashes), run_time=1.0)
    scene.wait(0.8)
    scene.play(FadeOut(slashes), fade_through(avg, result), run_time=1.6)
    framed = glow_frame(result, cfg.GOLD)
    scene.play(Create(framed), run_time=1.0)

    # --- 8. Harder and sooner: speed appears squared -----------------------------------------------------------------------------------
    beat(scene, t, 7)
    why = VGroup(eq_chip(r"\text{harder: } \times v_x", cfg.IMPULSE, cfg.FONT["small"]),
                 eq_chip(r"\text{sooner: } \times v_x", cfg.VELOCITY, cfg.FONT["small"])).arrange(RIGHT, buff=0.4).move_to([3.6, 0.75, 0])
    clock.value = 0.0
    scene.play(FadeIn(why[0], shift=UP * 0.1), clock.to(ball, 1.0, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(FadeIn(why[1], shift=UP * 0.1), clock.to(ball, 2.0, run_time=1.0, rate_func=linear), run_time=1.0)
    finish(scene, t, fill=lambda s: [clock.to(ball, 2.0 + s, rate_func=linear)])
