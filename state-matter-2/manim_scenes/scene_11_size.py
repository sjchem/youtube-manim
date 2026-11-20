"""Scene 11 — size crowds the space. Two glass boxes turn side by side, each
holding the same sixty molecules with the same speeds (the same temperature):
on the left an ideal gas of points, on the right hard spheres with real size
(``CollidingSpheres``, a ``pm.HardSphereGas`` that reports contacts), which
throw a small red flash whenever two of them bounce apart. Only hits on the
piston and the floor spark (orange), and a pair of live bars between the boxes
counts exactly those hits per second (a 3-second running window). Dilute, the
bars nearly match. Both pistons then squeeze the gas to three tenths of its
volume. Under each box a "free room" bar tracks the room left for motion: the
box's volume for points; for the spheres the van der Waals estimate V − N b,
whose red part (the molecules' excluded volume, fixed) eats an ever larger
share as the box shrinks. The hard-sphere box's bar climbs far above the point
gas's: more hits, higher pressure. The scene closes on P_real > P_ideal, a
positive deviation, in red.
"""

from manim_scenes.common import *
from manim_scenes.kit_c import CollidingSpheres, ContactFlashes, bar_meter, live_number, word_cue

N = 60
R_SPHERE = 0.12                      # stage units: the right box's molecules have real size
R_POINT = 0.045                      # the left box's "points" (drawn small, no size in the model)
HX, HZ, H, FLOOR = 1.2, 0.9, 2.6, -1.3
SPEED = 1.7
SEED = cfg.SEED + 110
SQUEEZE_1, SQUEEZE_2 = 0.6, 0.3      # volume ratios after the two squeezes
WINDOW = 3.0                         # seconds of hits averaged by each bar
BAR_H = 3.2
BASE_Y = -2.5
ROOM_LEN = 3.0
ROOM_Y = -3.55


class Scene11Size(Scene):
    def construct(self) -> None:
        play_scene(self)


def excluded_fraction() -> float:
    """N b / V0 with b = 4 x one sphere's volume (the van der Waals estimate of the room the spheres take)."""
    b = pm.EXCLUDED_PER_MOLECULE * 4 / 3 * np.pi * R_SPHERE ** 3
    return N * b / (2 * HX * H * 2 * HZ)


def room_bar(box: GasBox, left: float, blocked: float) -> VGroup:
    """A free-room bar: a rail as long as the full volume, a blue fill for the free room and
    (``blocked`` > 0) a red block for the molecules' excluded volume, which never shrinks."""
    rail = RoundedRectangle(width=ROOM_LEN + 0.16, height=0.5, corner_radius=0.1, stroke_color=cfg.MUTED,
                            stroke_width=2, stroke_opacity=0.6, fill_color=cfg.PANEL, fill_opacity=0.8)
    rail.move_to([left + ROOM_LEN / 2, ROOM_Y, 0])
    free = Rectangle(width=1, height=0.34, stroke_width=0, fill_color=cfg.VOLUME, fill_opacity=0.9)
    taken = Rectangle(width=1, height=0.34, stroke_width=0, fill_color=cfg.SIZE, fill_opacity=0.95)
    group = VGroup(rail, free, taken)

    def fit(m):
        v = box.chamber.volume_ratio()
        w_free = max((v - blocked) * ROOM_LEN, 0.02)
        free.stretch_to_fit_width(w_free).move_to([left + w_free / 2, ROOM_Y, 0])
        w_taken = max(blocked * ROOM_LEN, 0.001)
        taken.stretch_to_fit_width(w_taken).move_to([left + w_free + w_taken / 2, ROOM_Y, 0])
        taken.set_opacity(0.95 if blocked > 0 else 0.0)

    group.add_updater(fit)
    fit(group)
    group.free, group.taken, group.rail = free, taken, rail
    return group


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "11", TITLES["11"])

    # --- 0. Two boxes, the same molecules: points on the left, real spheres on the right ---------------------------------
    kw = dict(count=N, seed=SEED, half_x=HX, half_z=HZ, height=H, floor=FLOOR, lid="piston", zoom=0.9, pitch=0.3,
              speed=SPEED, spark_axes=(1,), sway=0.03)
    ideal = GasBox((-4.25, -0.45, 0), yaw=-0.42, radius=R_POINT, **kw)
    real = GasBox((4.25, -0.45, 0), yaw=0.42, radius=R_SPHERE,
                  model=CollidingSpheres(N, SEED, R_SPHERE, (2 * HX, H, 2 * HZ)), **kw)
    bumps = ContactFlashes(real)
    bumps.presence = 0.0
    real.stage.add_overlay(bumps)
    scene.add(ideal.stage, real.stage)
    for stage in (ideal.stage, real.stage):
        stage.presence = 0.0
    scene.play(ideal.stage.fade(ideal.stage, 1.0), real.stage.fade(real.stage, 1.0), run_time=1.4)
    play_in(scene, t, 1, *ideal.stage.turn(yaw=-0.5), *real.stage.turn(yaw=0.5), run_time=time_left(scene, t, 1))

    # --- 1. Same number, same temperature; points vs molecules with size that bounce off one another --------------------
    beat(scene, t, 1)
    same = chip("same N · same T", cfg.WHITE, cfg.FONT["small"]).move_to([0, 2.75, 0])
    left_tag = txt("ideal: points", cfg.FONT["label"], cfg.MOLECULE).move_to([-4.3, 2.75, 0])
    right_tag = txt("real: with size", cfg.FONT["label"], cfg.SIZE).move_to([4.3, 2.75, 0])
    scene.play(FadeIn(same, shift=DOWN * 0.15), run_time=1.0)
    scene.play(Indicate(same.label, color=cfg.GOLD, scale_factor=1.08), run_time=1.2)
    word_cue(scene, t, 1, "left")
    scene.play(FadeIn(left_tag, shift=DOWN * 0.15), ideal.cloud.tween("radius", R_POINT * 1.8, rate_func=there_and_back),
               run_time=1.4)
    word_cue(scene, t, 1, "right")
    scene.play(FadeIn(right_tag, shift=DOWN * 0.15), real.stage.zoom_to(1.02), run_time=1.4)
    word_cue(scene, t, 1, "bounce")
    scene.play(real.stage.fade(bumps, 1.0), run_time=0.8)
    play_in(scene, t, 2, real.stage.zoom_to(0.9), *ideal.stage.turn(yaw=-0.62), *real.stage.turn(yaw=0.62), run_time=3.0)

    # --- 2. Dilute: the hits on piston and floor nearly match --------------------------------------------------------------
    beat(scene, t, 2)
    top = 2.75 * float(np.abs(ideal.gas.u[:, 1]).sum()) * SPEED / (H * SQUEEZE_2)
    rate_i = lambda: ideal.cloud.hit_rate(WINDOW, axis=1)
    rate_r = lambda: real.cloud.hit_rate(WINDOW, axis=1)
    bar_i = bar_meter(rate_i, [-0.55, BASE_Y, 0], cfg.MOLECULE, top=top, height=BAR_H)
    bar_r = bar_meter(rate_r, [0.55, BASE_Y, 0], cfg.SIZE, top=top, height=BAR_H)
    base = Line([-1.25, BASE_Y, 0], [1.25, BASE_Y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    hits_title = txt("hits / s", cfg.FONT["label"], cfg.IMPULSE).move_to([0, 1.75, 0])
    num_i = live_number(lambda: bar_i.level.value, lambda m: m.next_to(bar_i.tip(), UP, buff=0.14), 36, cfg.MOLECULE)
    num_r = live_number(lambda: bar_r.level.value, lambda m: m.next_to(bar_r.tip(), UP, buff=0.14), 36, cfg.SIZE)
    scene.add(num_i, num_r)
    scene.play(Create(base), FadeIn(bar_i), FadeIn(bar_r), FadeIn(hits_title, shift=DOWN * 0.1),
               set_attr(num_i, num_i, "alpha", 1.0), set_attr(num_r, num_r, "alpha", 1.0), run_time=1.2)
    word_cue(scene, t, 2, "alike")
    alike = eq(r"\approx", cfg.FONT["section"], cfg.WHITE)
    alike.add_updater(lambda m: m.move_to([0, max(bar_i.tip()[1], bar_r.tip()[1]) + 0.95, 0]))
    dilute = chip("dilute", cfg.MOLECULE, cfg.FONT["small"]).move_to([0, ROOM_Y, 0])
    scene.play(FadeIn(alike, scale=0.8), FadeIn(dilute, shift=UP * 0.1), run_time=1.0)
    word_cue(scene, t, 2, "small")
    scene.play(*ideal.stage.turn(yaw=-0.42), *real.stage.turn(yaw=0.42), real.stage.zoom_to(1.0),
               run_time=2.4, rate_func=there_and_back)
    play_in(scene, t, 3, Indicate(dilute.label, color=cfg.WHITE, scale_factor=1.06), run_time=1.2)

    # --- 3. Squeeze both boxes --------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    alike.clear_updaters()
    scene.play(ideal.volume_to(SQUEEZE_1), real.volume_to(SQUEEZE_1), FadeOut(alike), FadeOut(same),
               run_time=3.6, rate_func=smooth)

    # --- 4. Each sphere's bulk blocks room: the free room shrinks faster than the box --------------------------------------
    beat(scene, t, 4)
    room_i = room_bar(ideal, -4.25 - ROOM_LEN / 2, 0.0)
    room_r = room_bar(real, 4.25 - ROOM_LEN / 2, excluded_fraction())
    room_tag = txt("free room", cfg.FONT["label"], cfg.VOLUME).move_to([0, ROOM_Y, 0])
    scene.play(FadeOut(dilute), run_time=0.4)
    scene.play(FadeIn(room_i), FadeIn(room_r), FadeIn(room_tag, shift=UP * 0.1), run_time=0.8)
    word_cue(scene, t, 4, "blocks")
    scene.play(Indicate(room_r.taken, color=cfg.WHITE, scale_factor=1.25), real.stage.zoom_to(1.05), run_time=1.4)
    word_cue(scene, t, 4, "free")
    scene.play(ideal.volume_to(SQUEEZE_2), real.volume_to(SQUEEZE_2), real.stage.zoom_to(0.95), run_time=4.8,
               rate_func=smooth)
    play_in(scene, t, 5, Indicate(room_r.free, color=cfg.WHITE, scale_factor=1.15),
            Indicate(room_i.free, color=cfg.WHITE, scale_factor=1.15), run_time=1.4)

    # --- 5. Less room: back to the walls more often; count the hits ---------------------------------------------------------
    beat(scene, t, 5)
    scene.play(ideal.cloud.tween("spark", 1.6), real.cloud.tween("spark", 1.6), *ideal.stage.turn(yaw=-0.5),
               *real.stage.turn(yaw=0.5), run_time=2.4)
    word_cue(scene, t, 5, "count")
    scene.play(Circumscribe(VGroup(bar_r, num_r), color=cfg.SIZE, buff=0.14), run_time=1.6)
    word_cue(scene, t, 5, "pressure")
    more = txt("more hits → higher P", cfg.FONT["label"], cfg.WHITE).move_to([0, 3.4, 0])
    more[-1].set_color(cfg.PRESSURE)
    scene.play(FadeIn(more, shift=DOWN * 0.12), run_time=1.0)
    play_in(scene, t, 6, *ideal.stage.turn(yaw=-0.6), *real.stage.turn(yaw=0.6), run_time=3.0)

    # --- 6. Size and repulsion dominate: P_real > P_ideal, a positive deviation ------------------------------------------------
    beat(scene, t, 6)
    law = eq(r"P_{\text{real}} > P_{\text{ideal}}", cfg.FONT["section"], cfg.SIZE)
    kind = txt("positive deviation", cfg.FONT["label"], cfg.SIZE)
    verdict = VGroup(law, kind).arrange(DOWN, buff=0.2)
    framed = boxed(verdict, cfg.SIZE, buff=0.2).move_to([0, 3.1, 0])
    scene.play(FadeOut(more), FadeOut(hits_title), run_time=0.4)
    scene.play(FadeIn(framed.body, shift=DOWN * 0.15), run_time=0.8)
    scene.play(Create(framed.frame), run_time=1.0)
    finish(scene, t, real.stage, fill=lambda s: ideal.stage.turn(yaw=ideal.stage.yaw - 0.22 * s / 4))
