"""Scene 05 — why so few are slow. Fourteen molecules carry gold velocity
arrows; their tails slide to one common point, and the tips become the first
dots of a round 3D cloud in velocity space (1500 seeded Maxwellian velocity
vectors on a slowly turning stage, with v_x, v_y, v_z axes). A gold arrow from
the centre to one tip is that molecule's speed u. A translucent gold shell of
radius u then counts the tips inside it — they light up gold and a live number
reads the count — while, on the right, a gold curve of "tips in the shell"
grows with the shell. Near the centre the shell is tiny and nearly empty
(slow molecules are rare); as it grows its area 4πu² gathers more; far out the
cloud fades faster than the shell grows and the count falls. Two dashed
factors, the rising shell area (blue) and the fading cloud (purple), multiply
into the gold Maxwell-Boltzmann curve, and the full formula is written with
its u² and exponential factors framed in the same colours.
"""

from manim_scenes.common import *
from manim_scenes.kit_c import live_number
from manim_scenes.kit_d import Trace, at_word

N = 1500
RMS = 1.6                        # stage units: rms speed of the cloud
SIGMA = RMS / np.sqrt(3)
SHELL = 0.09                     # half-thickness of the counting shell
ARROWS = 14
STAGE_AT = (-3.55, -0.25, 0.0)
U_MAX = 3.6
Y_TOP = 0.8
SHELL_COLOR = cfg.BLUE
CLOUD_FADE = cfg.LIMIT


class Scene05VelocitySpace(Scene):
    def construct(self) -> None:
        play_scene(self)


def cloud_points() -> np.ndarray:
    rng = np.random.default_rng(cfg.SEED + 50)
    return rng.normal(scale=SIGMA, size=(N, 3))


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "05", TITLES["05"])
    pts = cloud_points()
    radii = np.linalg.norm(pts, axis=1)
    stage = Stage(STAGE_AT, zoom=0.98, yaw=-0.6, pitch=0.32, sway=0.03)

    # --- 0. Molecules with velocity arrows; the tails slide to one point ------------------------------------------------
    rng = np.random.default_rng(cfg.SEED + 51)
    homes = rng.uniform(-1.0, 1.0, size=(ARROWS, 3)) * np.array([2.3, 1.7, 1.6])
    tips = pts[:ARROWS]
    slide = Knob(0.0)
    balls, vectors = [], []
    for k in range(ARROWS):
        tail = (lambda k=k: homes[k] * (1 - slide.value))
        balls.append(Ball(tail, 0.1, cfg.MOLECULE, layers=12))
        vectors.append(Vector(tail, lambda k=k, tail=tail: tail() + tips[k], cfg.VELOCITY, width=0.05, tip=0.17))
    stage.add_body(*balls)
    stage.add_overlay(*vectors)
    show(scene, stage, 1.2)
    at_word(scene, t, 0, "tail", lead=0.3)
    origin = Ball(np.zeros(3), 0.07, cfg.WHITE, layers=10)
    origin.presence = 0.0
    stage.add_body(origin)
    scene.play(stage.fade(origin, 1.0), run_time=0.5)
    scene.play(slide.to(stage, 1.0, rate_func=smooth), *stage.turn(yaw=-0.4), run_time=3.0)
    play_in(scene, t, 1, *fade_all(stage, balls, 0.0), run_time=0.8)

    # --- 1. Tips form a round cloud, densest at the centre -----------------------------------------------------------------
    beat(scene, t, 1)
    first = Dots(tips, cfg.GOLD, radius=0.06)
    first.presence = 0.0
    cloud = Dots(pts, cfg.MOLECULE, radius=0.034, alpha=0.75)
    cloud.presence = 0.0
    stage.add_body(cloud, first)
    axes3 = axis_triad(stage, (0, 0, 0), [(2.6, 0, 0), (0, 2.6, 0), (0, 0, 2.6)], [cfg.MUTED] * 3,
                       ["v_x", "v_y", "v_z"], width=2.5, label_size=cfg.FONT["small"])
    for part in axes3.parts:
        part.presence = 0.0
    scene.play(stage.fade(first, 1.0), *fade_all(stage, vectors, 0.0), run_time=1.0)
    at_word(scene, t, 1, "cloud", lead=0.3)
    scene.play(stage.fade(cloud, 1.0), *fade_all(stage, axes3.parts, 1.0), stage.zoom_to(1.05), run_time=2.0)
    vs_tag = txt("velocity space", cfg.FONT["label"], cfg.MUTED)
    vs_tag.move_to([-7.3 + vs_tag.width / 2, 3.1, 0])
    scene.play(FadeIn(vs_tag, shift=DOWN * 0.1), stage.fade(first, 0.0), run_time=0.9)
    at_word(scene, t, 1, "round", lead=0.2)
    scene.play(stage.set_spin(0.16), run_time=1.0)
    at_word(scene, t, 1, "densest", lead=0.3)
    core = Halo(origin, cfg.WHITE, reach=15.0, peak=0.22)
    core.presence = 0.0
    stage.add_body(core)
    scene.play(stage.fade(core, 1.0), run_time=1.0)
    play_in(scene, t, 2, stage.fade(core, 0.0), run_time=1.6)

    # --- 2. Speed = distance of a tip from the centre; count tips in a thin shell ---------------------------------------
    beat(scene, t, 2)
    pick = int(np.argmin(np.abs(radii - 1.45)))
    speed_arrow = Vector(np.zeros(3), pts[pick], cfg.GOLD, width=0.07, tip=0.22)
    speed_arrow.presence = 0.0
    u_tag = Tag(eq("u", cfg.FONT["section"], cfg.GOLD), pts[pick] * 0.55, UP * 0.42)
    u_tag.presence = 0.0
    stage.add_overlay(speed_arrow, u_tag)
    scene.play(stage.fade(speed_arrow, 1.0), stage.fade(u_tag, 1.0), *fade_all(stage, axes3.tags, 0.0), run_time=1.0)
    at_word(scene, t, 2, "count", lead=0.3)
    r_shell = Knob(0.05)
    shell = glass_sphere(stage, np.zeros(3), lambda: r_shell.value, cfg.GOLD, presence=0.0, fill_opacity=0.07,
                         ring_opacity=0.22)
    lit = Dots(lambda: pts[np.abs(radii - r_shell.value) < SHELL], cfg.GOLD, radius=0.055)
    lit.presence = 0.0
    stage.add_body(lit)

    def in_shell() -> int:
        return int(np.count_nonzero(np.abs(radii - r_shell.value) < SHELL))

    count_head = txt("tips in shell", cfg.FONT["small"], cfg.GOLD).move_to([STAGE_AT[0] - 0.7, -3.35, 0])
    count = live_number(in_shell, lambda m: m.next_to(count_head, RIGHT, buff=0.3), 46, cfg.WHITE)
    scene.add(count)
    scene.play(*fade_all(stage, shell.parts, 1.0), stage.fade(lit, 1.0), cloud_alpha(stage, cloud, 0.45),
               stage.fade(speed_arrow, 0.0), stage.fade(u_tag, 0.0), *fade_all(stage, axes3.tags, 1.0), FadeIn(count_head), set_attr(count, count, "alpha", 1.0),
               run_time=1.4)
    axes = plot_axes((0, U_MAX), (0, Y_TOP), x_length=5.0, y_length=3.7, at=[4.15, -0.2, 0], x_label="u", y_label="n",
                     x_color=cfg.VELOCITY, x_ticks=(1, 2, 3))
    axes.labels[1].become(txt("tips", cfg.FONT["small"], cfg.GOLD).next_to(axes.y_axis.get_end(), UP, buff=0.12))
    us = np.linspace(0.0, U_MAX, 200)
    mb = pm.maxwell_pdf(us, RMS)
    trace = Trace(axes, us, mb, cfg.GOLD, start=0.05)
    scene.play(Create(axes), run_time=1.2)
    scene.add(trace.curve, trace.bead)
    at_word(scene, t, 2, "shell", lead=0.6)
    play_in(scene, t, 3, r_shell.to(stage, 1.45, rate_func=smooth), trace.grow(1.45, rate_func=smooth), run_time=2.4)

    # --- 3. Near the centre the shell is tiny: very slow molecules are rare ----------------------------------------------
    beat(scene, t, 3)
    scene.play(r_shell.to(stage, 0.32, rate_func=smooth), trace.end.to(trace.curve, 0.32, rate_func=smooth), stage.zoom_to(1.25),
               run_time=3.0)
    at_word(scene, t, 3, "rare", lead=0.6)
    rare = txt("slow: rare", cfg.FONT["label"], cfg.SLOW).move_to(axes.c2p(0.95, 0.68))
    scene.play(FadeIn(rare, shift=DOWN * 0.1), Indicate(count, color=cfg.GOLD, scale_factor=1.2), run_time=1.2)
    play_in(scene, t, 4, stage.zoom_to(1.05), run_time=1.6)

    # --- 4. Bigger shell: area 4 pi u^2 gathers more tips -----------------------------------------------------------------
    beat(scene, t, 4)
    area = eq(r"4\pi u^2", cfg.FONT["section"], SHELL_COLOR).move_to([STAGE_AT[0] + 2.4, 2.45, 0])
    scene.play(FadeIn(area, shift=DOWN * 0.1), FadeOut(rare), run_time=0.8)
    scene.play(r_shell.to(stage, 1.31, rate_func=smooth), trace.grow(1.31, rate_func=smooth), run_time=4.4)
    play_in(scene, t, 5, Indicate(area, color=cfg.WHITE, scale_factor=1.15), run_time=1.2)

    # --- 5. Far out the cloud fades faster than the shell grows -------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(r_shell.to(stage, 3.25, rate_func=smooth), trace.grow(3.25, rate_func=smooth), stage.zoom_to(0.9), run_time=5.0)
    play_in(scene, t, 6, *fade_all(stage, shell.parts, 0.0), stage.fade(lit, 0.0), cloud_alpha(stage, cloud, 0.75),
            set_attr(count, count, "alpha", 0.0), FadeOut(count_head), trace.fade_bead(0.0), FadeOut(area), run_time=1.2)

    # --- 6. Growing shell x fading cloud = Maxwell-Boltzmann ------------------------------------------------------------------
    beat(scene, t, 6)
    grow_f = curve_on(axes, lambda u: 0.06 * u * u, 0, 3.6, SHELL_COLOR, width=4, glow=False)
    fade_f = curve_on(axes, lambda u: 0.74 * float(np.exp(-u * u / (2 * SIGMA ** 2))), 0, U_MAX, CLOUD_FADE, width=4, glow=False)
    grow_d = DashedVMobject(grow_f.core, num_dashes=30)
    fade_d = DashedVMobject(fade_f.core, num_dashes=30)
    product = VGroup(eq(r"4\pi u^2", cfg.FONT["label"], SHELL_COLOR), eq(r"\times", cfg.FONT["label"], cfg.WHITE),
                     txt("fading cloud", cfg.FONT["small"], CLOUD_FADE), eq("=", cfg.FONT["label"], cfg.WHITE),
                     eq("f(u)", cfg.FONT["label"], cfg.GOLD)).arrange(RIGHT, buff=0.18)
    product.move_to([4.15, 2.75, 0])
    scene.play(Create(grow_d), FadeIn(product[0]), run_time=1.2)
    scene.play(Create(fade_d), FadeIn(product[1:3]), run_time=1.2)
    at_word(scene, t, 6, "Maxwell", lead=0.3)
    scene.play(FadeIn(product[3:]), Indicate(trace.curve, color=cfg.WHITE, scale_factor=1.02), run_time=1.2)
    mb_name = txt("Maxwell–Boltzmann", cfg.FONT["small"], cfg.GOLD).move_to(axes.c2p(2.55, 0.76))
    play_in(scene, t, 7, FadeIn(mb_name, shift=UP * 0.1), run_time=1.0)

    # --- 7. The formula: a u^2 from the shell, an exponential that makes high energy rare ------------------------------------
    beat(scene, t, 7)
    formula = eq([r"f(u)", "=", r"4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}", r"u^2", r"e^{-mu^2/(2k_BT)}"], cfg.FONT["body"] - 2)
    paint(formula, {0: cfg.GOLD, 3: SHELL_COLOR, 4: CLOUD_FADE})
    # Leave room for both factor frames, including their soft outer glows.
    # Shift horizontally to preserve the equation's shared mathematical baseline.
    formula[3:].shift(RIGHT * 0.25)
    formula[4].shift(RIGHT * 0.60)
    formula.move_to([0.0, -3.3, 0])
    back = panel(formula.width + 0.7, formula.height + 0.45, cfg.MUTED, 0.92).move_to(formula)
    scene.play(FadeIn(back), Write(formula), stage.glide([STAGE_AT[0], 0.35, 0]), FadeOut(vs_tag), run_time=2.0)
    at_word(scene, t, 7, "squared", lead=0.3)
    f_shell = glow_frame(formula[3], SHELL_COLOR, buff=0.1)
    scene.play(Create(f_shell), Indicate(grow_d, color=cfg.WHITE), run_time=1.0)
    at_word(scene, t, 7, "exponential", lead=0.3)
    f_fade = glow_frame(formula[4], CLOUD_FADE, buff=0.1)
    scene.play(Create(f_fade), Indicate(fade_d, color=cfg.WHITE), run_time=1.0)
    at_word(scene, t, 7, "shape", lead=0.3)
    shape = boxed(txt("the shape matters", cfg.FONT["label"], cfg.GOLD), cfg.GOLD, buff=0.16).move_to([4.15, 2.75, 0])
    scene.play(fade_through(product, shape), run_time=1.0)
    scene.remove(product)
    finish(scene, t, stage)


def cloud_alpha(stage: Stage, cloud: Dots, value: float, **kwargs) -> Param:
    return set_attr(stage, cloud, "alpha", value, **kwargs)
