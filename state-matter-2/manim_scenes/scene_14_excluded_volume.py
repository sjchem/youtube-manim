"""Scene 14 — the space molecules take. A box of ideal points roams its whole
volume; then the points swell into molecules with real size. Two molecules
as translucent hard spheres of diameter d, each with its centre marked (white
and gold): the gold one approaches, touches, and rolls around the first while
its centre traces a gold arc — the centres never come closer than d.

The forbidden sphere around the first molecule (red glass) therefore has
radius d, not d/2: its volume is 8 times the molecule's. A forbidden sphere
belongs to a pair, so each molecule is charged half: 4 times its own volume.
Per mole that is b, and the model approximates the available volume as V − nb.

Finally the meaning of b: two bars (the molecules' own volume, and b, four
times longer), and a gold centre flying among fixed molecules, reflecting off
each red forbidden sphere (``kit_c.ballistic_path``): what matters is where the
centres can go.
"""

from manim_scenes.common import *
from manim_scenes.kit_c import ballistic_path, word_cue

STAGE_AT = (-3.4, -0.45, 0.0)
R = 0.72                       # molecule radius (stage units); diameter d = 2 R
D = 2 * R
A = np.array([-0.85, 0.0, 0.0])
B_START = np.array([2.7, 0.55, 0.4])
COL_X = 4.35


class Scene14ExcludedVolume(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "14", TITLES["14"])

    # --- 0. Ideal points roam everywhere; real molecules have size ---------------------------------------------------------
    box = GasBox(STAGE_AT, count=40, half_x=1.5, half_z=1.1, height=2.6, floor=-1.3, zoom=1.15, yaw=-0.55, pitch=0.3,
                 speed=1.2, radius=0.035, seed=cfg.SEED + 140)
    show(scene, box.stage, 1.0)
    points = txt("ideal: points", cfg.FONT["section"], cfg.LIMIT).move_to([COL_X, 0.9, 0])
    real = txt("real: spheres", cfg.FONT["section"], cfg.MOLECULE).move_to([COL_X, -0.4, 0])
    scene.play(FadeIn(points, shift=LEFT * 0.15), *box.stage.turn(yaw=-0.4), run_time=1.2)
    word_cue(scene, t, 0, "Real", lead=0.2)
    scene.play(box.cloud.tween("radius", 0.17, rate_func=smooth), FadeIn(real, shift=LEFT * 0.15), run_time=2.2)
    play_in(scene, t, 1, *box.stage.turn(yaw=-0.25), run_time=1.6)

    # --- 1. Two hard spheres, diameter d -------------------------------------------------------------------------------------
    beat(scene, t, 1)
    hide(scene, box.stage, 0.8, FadeOut(points), FadeOut(real))
    stage = Stage((-3.0, -0.4, 0.0), zoom=1.65, yaw=-0.35, pitch=0.25, sway=0.03)
    approach, roll = Knob(0.0), Knob(0.0)
    u1 = mu.unit(B_START - A)
    u2 = mu.unit(np.cross(u1, np.array([0.0, 0.0, 1.0])) * -1)

    def b_centre() -> np.ndarray:
        if approach.value < 1.0:
            return B_START + (A + D * u1 - B_START) * approach.value
        th = roll.value
        return A + D * (np.cos(th) * u1 + np.sin(th) * u2)

    sphere_a = glass_sphere(stage, A, R, cfg.MOLECULE, fill_opacity=0.28, rim_opacity=0.9)
    sphere_b = glass_sphere(stage, b_centre, R, cfg.MOLECULE, fill_opacity=0.28, rim_opacity=0.9)
    dot_a = Ball(A, 0.08, cfg.WHITE, layers=10)
    dot_b = Ball(b_centre, 0.09, cfg.GOLD, layers=10)
    stage.add_body(dot_a, dot_b)
    dia = Segment(A - np.array([R, 0, 0]), A + np.array([R, 0, 0]), cfg.WHITE, width=3.5, opacity=0.9)
    dia_tag = Tag(eq("d", cfg.FONT["section"], cfg.WHITE), A + np.array([0, -R, 0]), DOWN * 0.45)
    dia.presence = dia_tag.presence = 0.0
    stage.add_body(dia)
    stage.add_overlay(dia_tag)
    show(scene, stage, 1.0)
    play_in(scene, t, 2, stage.fade(dia, 1.0), stage.fade(dia_tag, 1.0), run_time=1.0)

    # --- 2. They touch but can't overlap: the centres stay at least d apart ------------------------------------------------
    beat(scene, t, 2)
    scene.play(stage.fade(dia, 0.0), stage.fade(dia_tag, 0.0), approach.to(stage, 1.0, rate_func=rush_into), run_time=1.8)
    touch = Circle(radius=0.25, stroke_color=cfg.REPEL, stroke_width=5).move_to(stage.screen_point(A + R * u1))
    scene.play(FadeIn(touch), touch.animate.scale(2.0).set_stroke(opacity=0), run_time=0.6)
    scene.remove(touch)
    gap = Segment(A, b_centre, cfg.GOLD, width=4, opacity=0.95)
    gap_tag = Tag(eq("d", cfg.FONT["section"], cfg.GOLD), lambda: (A + b_centre()) / 2, UP * 0.45 + LEFT * 0.2)
    arc = Curve(lambda: np.array([A + D * (np.cos(p) * u1 + np.sin(p) * u2) for p in np.linspace(0, max(roll.value, 1e-3), 40)]),
                cfg.GOLD, width=4)
    gap.presence = gap_tag.presence = 0.0
    stage.add_body(gap, arc)
    stage.add_overlay(gap_tag)
    word_cue(scene, t, 2, "centre", lead=0.3)
    scene.play(stage.fade(gap, 1.0), stage.fade(gap_tag, 1.0), run_time=0.9)
    rule = VGroup(txt("centres stay", cfg.FONT["label"], cfg.WHITE), eq(r"\ge d", cfg.FONT["title"], cfg.GOLD)).arrange(RIGHT, buff=0.25)
    rule.move_to([COL_X, 2.3, 0])
    scene.play(roll.to(stage, 2.4, rate_func=smooth), FadeIn(rule, shift=DOWN * 0.1), run_time=4.0)
    play_in(scene, t, 3, roll.to(stage, 3.6, rate_func=smooth), run_time=2.0)

    # --- 3. The forbidden sphere has radius d: 8 times the molecule's volume -------------------------------------------------
    beat(scene, t, 3)
    zone = glass_sphere(stage, A, D, cfg.SIZE, presence=0.0, fill_opacity=0.12, ring_opacity=0.35)
    scene.play(*fade_all(stage, zone.parts, 1.0), stage.zoom_to(1.35), run_time=1.6)
    word_cue(scene, t, 3, "radius", lead=0.2)
    radius_tag = chip("radius d, not d/2", cfg.SIZE, cfg.FONT["label"]).move_to([COL_X, 2.55, 0])
    scene.play(fade_through(rule, radius_tag), run_time=0.9)
    scene.remove(rule)
    word_cue(scene, t, 3, "eight", lead=0.3)
    vol = VGroup(eq(r"\frac43\pi d^3", cfg.FONT["label"], cfg.SIZE),
                 eq(r"= 8\times\frac43\pi\left(\frac d2\right)^3", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.25,
                                                                                                        aligned_edge=LEFT)
    vol.move_to([COL_X, 0.65, 0])
    scene.play(Write(vol), run_time=2.0)
    play_in(scene, t, 4, Indicate(vol[1][0][1], color=cfg.GOLD, scale_factor=1.5), run_time=1.0)

    # --- 4. Shared by a pair: 4 times the molecule's own volume each --------------------------------------------------------
    beat(scene, t, 4)
    zone_b = glass_sphere(stage, b_centre, D, cfg.SIZE, presence=0.0, fill_opacity=0.06, ring_opacity=0.2)
    scene.play(*fade_all(stage, zone_b.parts, 0.7), run_time=1.2)
    word_cue(scene, t, 4, "share", lead=0.2)
    share = paint(eq([r"\frac{8v}{2}", "=", "4v"], cfg.FONT["title"]), {0: cfg.SIZE, 2: cfg.GOLD}).move_to([COL_X, -1.95, 0])
    each = txt("per molecule", cfg.FONT["small"], cfg.GOLD).next_to(share, DOWN, buff=0.18)
    scene.play(Write(share), run_time=1.6)
    play_in(scene, t, 5, FadeIn(each, shift=UP * 0.1), Circumscribe(share[2], color=cfg.GOLD), run_time=1.4)

    # --- 5. Per mole: b; the free volume is V − nb ---------------------------------------------------------------------------
    beat(scene, t, 5)
    b_def = paint(eq(["b", "=", "4", "N_A", "v"], cfg.FONT["title"]), {0: cfg.SIZE}).move_to([COL_X, 1.9, 0])
    free = paint(eq([r"V_{\text{available}}", r"\approx", "V", "-", "nb"], cfg.FONT["title"]), {0: cfg.VOLUME, 2: cfg.VOLUME, 4: cfg.SIZE})
    fit_width(free, 6.5)
    free_box = boxed(free, cfg.GOLD, buff=0.22).move_to([COL_X, 0.0, 0])
    scene.play(FadeOut(VGroup(radius_tag, vol, share, each)), stage.zoom_to(1.2), run_time=0.8)
    scene.play(Write(b_def), run_time=1.4)
    word_cue(scene, t, 5, "available", lead=0.3)
    play_in(scene, t, 6, Write(free), Create(free_box.frame), run_time=1.8)

    # --- 6. b is not simply the molecules' volume: what matters is where centres can go --------------------------------------
    beat(scene, t, 6)
    clear(scene, b_def, free, free_box.frame, run_time=0.8, others=[])
    scene.play(b_def.animate.scale(0.75).move_to([COL_X, 2.75, 0]), free.animate.scale(0.75).move_to([COL_X, 1.85, 0]),
               FadeOut(free_box.frame), run_time=0.8)
    # The flight among fixed molecules.
    arena = Stage(STAGE_AT, zoom=1.0, yaw=-0.5, pitch=0.3, spin=0.08, sway=0.02)
    half = 2.1
    rng = np.random.default_rng(cfg.SEED + 141)
    obstacles = np.array([[-1.0, -0.6, 0.4], [0.9, 0.7, -0.5], [0.6, -0.9, 0.9], [-0.7, 1.0, -0.8], [1.2, -0.2, -1.3]])
    r_small = 0.32
    d_small = 2 * r_small
    for o in obstacles:
        stage_ball = Ball(o, r_small, cfg.MOLECULE, layers=18)
        arena.add_body(stage_ball)
        glass_sphere(arena, o, d_small, cfg.SIZE, fill_opacity=0.1, ring_opacity=0.25)
    for a_ in (-1, 1):
        for b_ in (-1, 1):
            for axis in range(3):
                p0 = np.zeros(3)
                p0[(axis + 1) % 3], p0[(axis + 2) % 3] = a_ * half, b_ * half
                p0[axis] = -half
                p1 = p0.copy()
                p1[axis] = half
                arena.add_body(Segment(p0, p1, cfg.GLASS, 2.2, 0.4))
    path = ballistic_path(obstacles, d_small, half - 0.05, [-1.8, 1.6, 1.5], mu.unit([0.8, -0.55, -0.45]) * 1.6, 9.0)
    k = Knob(0.0)
    centre = Ball(lambda: path[int(k.value)], 0.09, cfg.GOLD, layers=10)
    trail = Curve(lambda: path[max(0, int(k.value) - 420):int(k.value) + 1], cfg.GOLD, width=3.5)
    arena.add_body(trail, centre)
    del rng
    show(scene, arena, 0.9)
    bars_y = (-0.4, -1.4)
    own = Rectangle(width=0.9, height=0.5, stroke_width=0, fill_color=cfg.MOLECULE, fill_opacity=0.9)
    bee = Rectangle(width=3.6, height=0.5, stroke_width=0, fill_color=cfg.SIZE, fill_opacity=0.9)
    own.move_to([COL_X - 1.7 + 0.45, bars_y[0], 0])
    bee.move_to([COL_X - 1.7 + 1.8, bars_y[1], 0])
    own_tag = txt("molecules' volume", cfg.FONT["small"], cfg.MOLECULE).next_to(own, RIGHT, buff=0.25)
    bee_tag = eq("b", cfg.FONT["section"], cfg.SIZE).next_to(bee, RIGHT, buff=0.25)
    four = txt("× 4", cfg.FONT["label"], cfg.GOLD).next_to(bee, DOWN, buff=0.2)
    scene.play(GrowFromEdge(own, LEFT), FadeIn(own_tag), k.to(arena, 120, rate_func=linear), run_time=1.2)
    scene.play(GrowFromEdge(bee, LEFT), FadeIn(bee_tag), FadeIn(four), k.to(arena, 360, rate_func=linear), run_time=1.6)
    word_cue(scene, t, 6, "centres", lead=0.3)
    where = txt("where the centres can go", cfg.FONT["label"], cfg.GOLD).move_to([STAGE_AT[0], -3.55, 0])
    scene.play(FadeIn(where, shift=UP * 0.1), k.to(arena, 600, rate_func=linear), run_time=2.0)
    finish(scene, t, arena, fill=lambda s: [k.to(arena, len(path) - 1, rate_func=linear)])
