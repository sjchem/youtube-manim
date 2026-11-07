"""Scene 03 — speed is the length of the velocity arrow. Two velocities from
``physics_models``: v1 = 5 i and v2 = 5 j, the same speed, different
vectors. Delta v = v2 - v1 is built tip to tail (reverse v1, add it to v2)
and measured: (-5, 5), |delta v| = 5 root 2 = 7.07 m/s. The speed changed
by nothing; the velocity by more than seven metres per second. The scene
closes on a ring of equal arrows: the same change, happening continuously.
"""

from manim_scenes.common import *

V1, V2 = pm.V1, pm.V2
DV = pm.turn_delta_v()
UNIT = 0.55                       # screen units per m/s on the grid
ORIGIN_PT = np.array([-3.4, -2.25, 0])


class Scene03SpeedVelocity(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "03")
    chapter_open(scene, 2, "Velocity and direction")
    head = heading("Speed vs velocity")
    scene.play(FadeIn(head, shift=DOWN * 0.18), run_time=0.6)

    # --- 2. Speed is the magnitude of velocity --------------------------------------------------------------------
    beat(scene, t, 1)
    kinds = VGroup(VGroup(txt("speed", cfg.FONT["section"], cfg.WHITE), txt("scalar", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.15),
                   VGroup(txt("velocity", cfg.FONT["section"], cfg.VELOCITY), txt("vector", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.15))
    kinds.arrange(RIGHT, buff=2.4).move_to([0, 1.6, 0])
    scene.play(FadeIn(kinds[0], shift=UP * 0.1), run_time=0.7)
    scene.play(FadeIn(kinds[1], shift=UP * 0.1), run_time=0.7)
    relation = paint(eq([r"v", "=", r"|\vec v|"], cfg.FONT["title"]), {0: cfg.WHITE, 2: cfg.VELOCITY}).move_to([0, -0.6, 0])
    scene.play(Write(relation), run_time=1.2)
    tail, tip = np.array([-2.0, -2.6, 0]), np.array([2.0, -2.6, 0])
    sample = VecArrow(tail, tip, cfg.VELOCITY, width=0.1)
    brace = Brace(Line(tail, tip), DOWN, color=cfg.WHITE, buff=0.12)
    scene.add(sample)
    scene.play(sample.grow_in(run_time=0.8), run_time=0.8)
    scene.play(FadeIn(brace), Indicate(relation[2], color=cfg.VELOCITY), run_time=1.0)

    # --- 3. v1 = 5 i ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    clear(scene, run_time=0.6)
    grid = plane((-6, 6), (-1, 6), unit=UNIT, at=ORIGIN_PT, labels=True, faint=0.35)
    pt = lambda x, y: grid.c2p(x, y)  # noqa: E731
    v1 = VecArrow(pt(0, 0), pt(*V1), cfg.VELOCITY, width=0.1)
    v1_tag = eq([r"\vec v_1", "=", rf"{wh(V1[0])}\,\hat\imath"], cfg.FONT["body"], cfg.VELOCITY).next_to(pt(V1[0] / 2, 0), UP, buff=0.3)
    scene.play(FadeIn(grid), run_time=0.8)
    scene.add(v1)
    scene.play(v1.grow_in(run_time=1.0), run_time=1.0)
    scene.play(FadeIn(v1_tag), run_time=0.6)

    # --- 4. v2 = 5 j -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    v2 = VecArrow(pt(0, 0), pt(*V2), cfg.VELOCITY, width=0.1)
    v2_tag = eq([r"\vec v_2", "=", rf"{wh(V2[1])}\,\hat\jmath"], cfg.FONT["body"], cfg.VELOCITY).next_to(pt(*V2), RIGHT, buff=0.3)
    scene.add(v2)
    scene.play(v2.grow_in(run_time=1.0), run_time=1.0)
    scene.play(FadeIn(v2_tag), run_time=0.6)

    # --- 5. Same speed, different vectors ---------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    speeds = eq(rf"|\vec v_1| = |\vec v_2| = {wh(pm.magnitude(V1))}\ \mathrm{{m/s}}", cfg.FONT["body"]).move_to([3.6, 3.05, 0])
    differ = eq(r"\vec v_1 \neq \vec v_2", cfg.FONT["body"], cfg.VELOCITY).next_to(speeds, DOWN, buff=0.4)
    scene.play(FadeOut(head), FadeIn(speeds, shift=DOWN * 0.1), run_time=0.8)
    scene.play(FadeIn(differ, shift=DOWN * 0.1), run_time=0.8)

    # --- 6. delta v = v2 - v1 ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    subtract = paint(eq([r"\Delta\vec v", "=", r"\vec v_2", "-", r"\vec v_1"], cfg.FONT["section"]),
                     {0: cfg.DELTA_V, 2: cfg.VELOCITY, 4: cfg.VELOCITY}).move_to([3.6, 1.35, 0])
    scene.play(FadeOut(differ), run_time=0.4)
    scene.play(Write(subtract), run_time=1.2)

    # --- 7. Reverse v1, add tip to tail: delta v = -5 i + 5 j -----------------------------------------------------------------------------------
    beat(scene, t, 6)
    minus = VecArrow(pt(*V2), pt(*pm.sub(V2, V1)), cfg.VELOCITY, width=0.08, grow=0.0)
    minus.alpha = 0.6
    minus_tag = eq(r"-\vec v_1", cfg.FONT["body"], cfg.VELOCITY).next_to(pt(-V1[0] / 2, V2[1]), UP, buff=0.25)
    scene.add(minus)
    scene.play(minus.grow_in(run_time=1.2), FadeIn(minus_tag), run_time=1.2)
    dv = VecArrow(pt(0, 0), pt(*DV), cfg.DELTA_V, width=0.11)
    scene.add(dv)
    scene.play(dv.grow_in(run_time=1.2), run_time=1.2)
    dv_tag = eq([r"\Delta\vec v", "=", rf"{wh(DV[0])}\,\hat\imath + {wh(DV[1])}\,\hat\jmath"], cfg.FONT["body"], cfg.DELTA_V)
    dv_tag.move_to([3.6, 0.1, 0])
    scene.play(FadeIn(dv_tag, shift=DOWN * 0.1), run_time=0.8)

    # --- 8. |delta v| = sqrt(25 + 25) = 7.07 m/s ------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    legs = VGroup(dashed_path(pt(0, 0), pt(DV[0], 0), cfg.X_COLOR, width=4, opacity=0.9),
                  dashed_path(pt(DV[0], 0), pt(*DV), cfg.Y_COLOR, width=4, opacity=0.9))
    scene.play(Create(legs), run_time=1.0)
    size = eq([r"|\Delta\vec v|", "=", rf"\sqrt{{{wh(DV[0] ** 2)} + {wh(DV[1] ** 2)}}}", r"\approx",
               rf"{fx(pm.magnitude(DV), 2)}\ \mathrm{{m/s}}"], cfg.FONT["body"])
    paint(size, {0: cfg.DELTA_V, 4: cfg.DELTA_V})
    fit_width(size, 6.6)
    size.move_to([3.6, -1.2, 0])
    scene.play(Write(size), run_time=1.6)
    scene.play(FadeIn(boxed(size[4], cfg.RESULT, buff=0.12)[0]), run_time=0.6)

    # --- 9. Speed unchanged; velocity changed by 7 m/s -------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    compare = VGroup(eq(r"\Delta v = 0", cfg.FONT["body"], cfg.WHITE),
                     eq(rf"|\Delta \vec v| \approx {fx(pm.magnitude(DV), 2)}", cfg.FONT["body"], cfg.DELTA_V)).arrange(RIGHT, buff=0.9)
    fit_width(compare, 6.4)
    compare.move_to([3.6, -2.55, 0])
    scene.play(FadeIn(compare[0], shift=UP * 0.1), run_time=0.7)
    scene.play(FadeIn(compare[1], shift=UP * 0.1), Indicate(dv, color=cfg.DELTA_V, scale_factor=1.05), run_time=1.0)

    # --- 10. Continuously, in circular motion --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    clear(scene)
    view = CircleView([0, -0.3, 0], 2.4, P, kv=1.25 / P.v)
    arrows = VGroup(*[view.arrow("v", when=k * P.period / 8, width=0.07, tip_len=0.22, glow=False) for k in range(8)])
    for arrow in arrows:
        arrow.refresh()
    scene.play(FadeIn(view.ring), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.18), run_time=3.0)
    scene.add(view.ball)
    live = view.arrow("v", width=0.1, tip_len=0.28)
    scene.add(live)
    scene.play(FadeOut(arrows), view.run(P.period, 4.5), run_time=4.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
