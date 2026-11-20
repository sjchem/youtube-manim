"""Scene 04 — from one speed to many. A two-dimensional box of a few hundred
hard disks (``pm.disk_movie``: an exact, seeded event simulation) starts with
every disk at the same speed, each heading its own way: gold arrows of equal
length show it, and every disk wears the same speed colour. A live histogram
on the right, its bars coloured with the same slow-to-fast scale, is a single
spike. Then the disks collide: the spike melts, the colours spread, and the
histogram settles onto the gold two-dimensional equilibrium curve
(``pm.rayleigh_pdf``) and stays there. One disk is ringed in gold; its speed,
marked on the histogram's axis, jumps at every collision while the crowd's
shape barely moves. Finally the caution: this is a 2D model; the dashed purple
3D curve (``pm.maxwell_pdf``) has a different shape.
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d
from manim_scenes.kit_d import at_word

UNIT = 0.18
BOX_AT = np.array([-3.5, -0.1, 0.0])
U_MAX, Y_TOP = 2.6, 1.25
EDGES = np.linspace(0.0, U_MAX, 21)
CLIP = 1.18                  # bars taller than this are clipped (the starting spike)
RATE = 1.1                   # simulation seconds per second of film once collisions start
FOLLOW = 7
ARROW_DISKS = (3, 19, 40, 66, 88, 101, 127, 150, 171, 199, 214, 233)


class Scene04OneSpeed(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "04", TITLES["04"])

    # --- 0. Identical disks, one speed, many directions -----------------------------------------------------------------
    dv = DiskView(BOX_AT, unit=UNIT, follow=FOLLOW)
    rate = Knob(0.0)
    driver = VMobject()
    driver.add_updater(lambda m, dt: setattr(dv.clock, "value", min(dv.clock.value + rate.value * dt, 59.9)))
    scene.add(driver)
    tag2d = chip("2D model", cfg.LIMIT, cfg.FONT["small"]).next_to(dv.frame_box, UP, buff=0.22).align_to(dv.frame_box, LEFT)
    scene.play(FadeIn(dv, scale=0.96), run_time=1.4)
    at_word(scene, t, 0, "two", lead=0.2)
    scene.play(FadeIn(tag2d, shift=DOWN * 0.12), run_time=0.8)
    at_word(scene, t, 0, "same", lead=0.3)
    pos = dv.positions(0.0)
    vel = dv.vel[0]
    arrows = VGroup(*[arrow2d(pos[i], pos[i] + np.array([*vel[i], 0.0]) * 0.62, cfg.VELOCITY, width=0.06, tip_len=0.18)
                      for i in ARROW_DISKS])
    scene.play(LaggedStart(*[FadeIn(a, scale=0.6) for a in arrows], lag_ratio=0.08), run_time=1.6)
    same = txt("every speed equal", cfg.FONT["label"], cfg.GOLD).next_to(dv.frame_box, DOWN, buff=0.28)
    scene.play(FadeIn(same, shift=UP * 0.1), run_time=0.8)
    at_word(scene, t, 0, "direction", lead=0.2)
    play_in(scene, t, 1, LaggedStart(*[Indicate(a, color=cfg.WHITE, scale_factor=1.25) for a in arrows], lag_ratio=0.1),
            run_time=2.2)

    # --- 1. The histogram: a single spike -----------------------------------------------------------------------------------
    beat(scene, t, 1)
    axes = plot_axes((0, U_MAX), (0, Y_TOP), x_length=4.7, y_length=4.3, at=[4.55, -0.45, 0], x_label="u", y_label="f(u)",
                     x_color=cfg.VELOCITY, x_ticks=(1, 2))

    def bars() -> VGroup:
        counts, _ = np.histogram(dv.speeds(), bins=EDGES)
        dens = counts / (len(dv.vel[0]) * (EDGES[1] - EDGES[0]))
        group = VGroup()
        for a, b, d in zip(EDGES[:-1], EDGES[1:], dens):
            if d <= 0:
                continue
            h = min(d, CLIP)
            color = speed_color((a + b) / 2, dv.top_speed)
            group.add(Polygon(axes.c2p(a, 0), axes.c2p(b, 0), axes.c2p(b, h), axes.c2p(a, h), stroke_color=color,
                              stroke_width=1.5, fill_color=color, fill_opacity=0.7 if d > CLIP else 0.55))
        return group

    hist = live(VGroup(), bars)
    count_tag = txt("relative frequency", cfg.FONT["small"], cfg.MUTED).next_to(axes, UP, buff=0.3)
    scene.play(Create(axes), FadeIn(count_tag, shift=DOWN * 0.1), run_time=1.4)
    at_word(scene, t, 1, "spike", lead=0.4)
    scene.add(hist)
    spike_tip = axes.c2p(1.0, CLIP)
    off_scale = arrow2d(spike_tip + DOWN * 0.15, spike_tip + UP * 0.45, cfg.GOLD, width=0.07, tip_len=0.2)
    scene.play(FadeIn(hist, shift=UP * 0.3), run_time=1.0)
    scene.play(FadeIn(off_scale, shift=UP * 0.1), Indicate(same, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)

    # --- 2. Let them collide ---------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(arrows), FadeOut(off_scale), FadeOut(same), rate.to(driver, RATE, rate_func=rush_into), run_time=1.6)
    collide = txt("collisions", cfg.FONT["label"], cfg.IMPULSE).next_to(dv.frame_box, DOWN, buff=0.28)
    play_in(scene, t, 3, FadeIn(collide, shift=UP * 0.1), run_time=0.9)

    # --- 3. The spike melts --------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    at_word(scene, t, 3, "faster", lead=0.1)
    below = axes.c2p(0, 0)[1] - 0.8
    faster = txt("faster →", cfg.FONT["small"], cfg.FAST).move_to([axes.c2p(2.0, 0)[0], below, 0])
    slower = txt("← slower", cfg.FONT["small"], cfg.SLOW).move_to([axes.c2p(0.45, 0)[0], below, 0])
    scene.play(FadeIn(faster, shift=RIGHT * 0.2), run_time=0.8)
    at_word(scene, t, 3, "slower", lead=0.1)
    scene.play(FadeIn(slower, shift=LEFT * 0.2), run_time=0.8)
    play_in(scene, t, 4, Indicate(hist, color=cfg.WHITE, scale_factor=1.03), run_time=1.4)

    # --- 4. The shape stops changing -----------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(faster), FadeOut(slower), run_time=0.7)
    at_word(scene, t, 4, "stops", lead=0.3)
    steady = curve_on(axes, lambda s: float(pm.rayleigh_pdf(s)), 0, U_MAX, cfg.GOLD, width=6)
    steady_tag = txt("steady shape", cfg.FONT["label"], cfg.GOLD).next_to(axes, UP, buff=0.3)
    scene.play(Create(steady), fade_through(count_tag, steady_tag), run_time=1.8)
    scene.remove(count_tag)
    at_word(scene, t, 4, "distribution", lead=0.4)
    play_in(scene, t, 5, Circumscribe(steady, color=cfg.GOLD, buff=0.08), run_time=1.8)

    # --- 5. Follow one particle --------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    marker = live(VGroup(), lambda: VGroup(
        DashedLine(axes.c2p(min(dv.follow_speed(), U_MAX), 0), axes.c2p(min(dv.follow_speed(), U_MAX), Y_TOP * 0.95),
                   stroke_color=cfg.GOLD, stroke_width=3, dash_length=0.1),
        Triangle(stroke_width=0, fill_color=cfg.GOLD, fill_opacity=1).scale(0.13)
        .move_to(axes.c2p(min(dv.follow_speed(), U_MAX), 0) + DOWN * 0.2)))
    u_head = eq("u =", cfg.FONT["label"], cfg.GOLD)
    u_value = DecimalNumber(dv.follow_speed(), num_decimal_places=2, font_size=50, color=cfg.GOLD)
    u_value.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
    readout_row = VGroup(u_head, u_value).arrange(RIGHT, buff=0.2).next_to(dv.frame_box, DOWN, buff=0.25)
    u_value.add_updater(lambda m: m.set_value(dv.follow_speed()))
    scene.play(set_attr(dv, dv, "follow_alpha", 1.0), FadeOut(collide), run_time=0.9)
    scene.add(marker)
    scene.play(FadeIn(marker), FadeIn(readout_row), run_time=0.8)
    at_word(scene, t, 5, "crowd's", lead=0.2)
    play_in(scene, t, 6, Indicate(steady, color=cfg.WHITE, scale_factor=1.03), run_time=1.6)

    # --- 6. Unpredictable individuals, a predictable distribution -------------------------------------------------------------
    beat(scene, t, 6)
    one = txt("individual speeds change", cfg.FONT["small"], cfg.WARNING)
    all_ = txt("a stable distribution", cfg.FONT["small"], cfg.GREEN)
    idea = VGroup(one, all_).arrange(DOWN, buff=0.22)
    idea_box = boxed(idea, cfg.GOLD, buff=0.2).move_to([-3.5, -3.42, 0])
    marker.clear_updaters()
    scene.play(FadeOut(marker), FadeOut(readout_row), set_attr(dv, dv, "follow_alpha", 0.0), run_time=0.7)
    scene.play(FadeIn(one, shift=UP * 0.12), run_time=0.9)
    at_word(scene, t, 6, "distribution", lead=0.3)
    scene.play(FadeIn(all_, shift=UP * 0.12), run_time=0.9)
    play_in(scene, t, 7, Create(idea_box.frame), run_time=1.0)

    # --- 7. A caution: this is 2D; a 3D gas has a different curve -------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(Indicate(tag2d, color=cfg.WHITE, scale_factor=1.15), run_time=1.0)
    at_word(scene, t, 7, "three", lead=0.3)
    curve3d = curve_on(axes, lambda s: float(pm.maxwell_pdf(s)), 0, U_MAX, cfg.LIMIT, width=5)
    dashed3d = VGroup(DashedVMobject(curve3d.core, num_dashes=40, dashed_ratio=0.6))
    tag3d = txt("3D gas", cfg.FONT["label"], cfg.LIMIT).move_to(axes.c2p(2.0, 0.85))
    tag2 = txt("2D", cfg.FONT["label"], cfg.GOLD).move_to(axes.c2p(0.4, 1.08))
    scene.play(Create(dashed3d), FadeIn(tag3d, shift=LEFT * 0.15), FadeIn(tag2, shift=RIGHT * 0.15), run_time=1.8)
    finish(scene, t, fill=lambda s: [Indicate(dashed3d, color=cfg.WHITE, scale_factor=1.02)])
