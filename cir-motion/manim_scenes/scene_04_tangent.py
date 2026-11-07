"""Scene 04 — which way is it moving? The reference particle circles on a
turning 3D ground (``physics_models.REFERENCE``, played at 0.35x real time
so the eye can follow). The teal position vector runs from the centre; the
gold velocity lies along the dashed tangent, with a right-angle mark: v is
perpendicular to r. Red arrows rule out "inward" and "outward". Then the
particle keeps moving, leaving frozen velocity copies every eighth of a
lap: same speed · turning velocity.
"""

from manim_scenes.common import *

R = 2.5                                  # stage units for the 2 m radius
KV = 1.35 / P.v                          # 4 m/s -> 1.35 stage units
SLOW = 0.35                              # film seconds per model second = 1 / SLOW
LIFT = 0.22


class Scene04Tangent(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "Which way is it moving?")
    stage = field_stage((0.0, -0.9, 0), zoom=1.25, pitch=0.82, yaw=-0.25, half=3.6)
    ring = Curve(ring_curve(ORIGIN, R, 160, h=0.01), cfg.MUTED, width=4, opacity=0.8)
    hub = Ball(np.array([0.0, 0.08, 0.0]), 0.08, cfg.MUTED, layers=10)
    stage.add_body(ring, hub)
    orbit = Circuit(stage, P, R=R, height=LIFT, kv=KV, phase=-0.3)
    show(scene, stage, 1.2)
    scene.play(orbit.run(1.6, 1.6 / SLOW), run_time=1.6 / SLOW)

    # --- 2. Which way does the velocity point? -----------------------------------------------------------------------
    beat(scene, t, 1)
    ask = Tag(eq(r"\vec v\ ?", cfg.FONT["body"], cfg.VELOCITY), lambda: orbit.world(), UP * 0.7 + RIGHT * 0.5)
    ask.presence = 0.0
    stage.add_overlay(ask)
    scene.play(FadeOut(head), stage.fade(ask, 1.0), orbit.run(orbit.t + 0.3, 0.8), run_time=0.8)
    scene.play(orbit.run(orbit.t + 1.9, 1.9 / SLOW), run_time=1.9 / SLOW)

    # --- 3. The position vector from the centre --------------------------------------------------------------------------
    beat(scene, t, 2)
    r_arrow = orbit.add_arrow("r", width=0.075)
    r_tag = Tag(eq(r"\vec r", cfg.FONT["body"], cfg.POSITION), lambda: (orbit.world() + np.array([0, LIFT, 0])) * 0.5,
                UP * 0.42)
    r_tag.presence = 0.0
    stage.add_overlay(r_tag)
    scene.play(stage.fade(ask, 0.0), stage.fade(r_arrow, 1.0), stage.fade(r_tag, 1.0), run_time=0.9)
    scene.play(orbit.run(orbit.t + 1.4, 1.4 / SLOW), run_time=1.4 / SLOW)
    frozen = orbit.t

    # --- 4. Along the tangent ----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    here = orbit.world(frozen)
    along = ground_vec(orbit.view.unit_t(frozen))
    tangent = Segment(here - along * 1.8, here + along * 1.8, cfg.WHITE, width=3, opacity=0.75, dashed=True)
    tangent.presence = 0.0
    stage.add_body(tangent)
    v_arrow = orbit.add_arrow("v", width=0.085)
    t_tag = Tag(txt("tangent", cfg.FONT["small"], cfg.WHITE), here - along * 1.25, UP * 0.5 + LEFT * 0.3)
    t_tag.presence = 0.0
    stage.add_overlay(t_tag)
    scene.play(stage.fade(tangent, 1.0), stage.fade(t_tag, 1.0), run_time=1.0)
    scene.play(stage.fade(v_arrow, 1.0), run_time=0.8)
    v_tag = Tag(eq(r"\vec v", cfg.FONT["body"], cfg.VELOCITY), lambda: orbit.world() + ground_vec(orbit.view.vel(orbit.t) * KV),
                UP * 0.42 + RIGHT * 0.2)
    v_tag.presence = 0.0
    stage.add_overlay(v_tag)
    scene.play(stage.fade(v_tag, 1.0), *stage.turn(yaw=-0.05, run_time=2.5), run_time=2.5)

    # --- 5. Perpendicular to the radius ----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    out = ground_vec(orbit.view.unit_r(frozen))
    size = 0.32
    corner = Curve(np.array([here - out * size, here - out * size + along * size, here + along * size]), cfg.WHITE,
                   width=3.5, glow=False)
    corner.presence = 0.0
    stage.add_body(corner)
    perp = eq([r"\vec v", r"\perp", r"\vec r"], cfg.FONT["title"])
    paint(perp, {0: cfg.VELOCITY, 2: cfg.POSITION}).move_to([4.6, 3.1, 0])
    scene.play(stage.fade(corner, 1.0), run_time=0.8)
    scene.play(Write(perp), run_time=1.2)
    scene.play(*stage.turn(yaw=-0.45, pitch=0.95, run_time=3.0), run_time=3.0)

    # --- 6. Never inward, never outward ----------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    inward = Vector(here, here - out * 1.2, cfg.WARNING, width=0.06, tip=0.22, glow=False)
    outward = Vector(here, here + out * 1.2, cfg.WARNING, width=0.06, tip=0.22, glow=False)
    crosses = [Tag(cross_mark(0.2), here - out * 0.75), Tag(cross_mark(0.2), here + out * 0.75)]
    for item in (inward, outward, *crosses):
        item.presence = 0.0
    stage.add_overlay(inward, outward, *crosses)
    scene.play(stage.fade(inward, 1.0), run_time=0.6)
    scene.play(stage.fade(crosses[0], 1.0), run_time=0.5)
    scene.play(stage.fade(outward, 1.0), run_time=0.6)
    scene.play(stage.fade(crosses[1], 1.0), run_time=0.5)
    scene.wait(3.0)
    scene.play(*[stage.fade(i, 0.0) for i in (inward, outward, *crosses)], Indicate(perp, color=cfg.VELOCITY), run_time=1.2)

    # --- 7. The tangent turns; so does the velocity ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(stage.fade(tangent, 0.0), stage.fade(t_tag, 0.0), stage.fade(corner, 0.0), stage.fade(r_tag, 0.0),
               stage.fade(v_tag, 0.0), run_time=0.6)
    ghosts = []
    step = P.period / 8
    for k in range(4):
        scene.play(orbit.run(orbit.t + step, step / SLOW), run_time=step / SLOW)
        p = orbit.world()
        ghost = Vector(p, p + ground_vec(orbit.view.vel(orbit.t) * KV), cfg.VELOCITY, width=0.06, tip=0.22, glow=False)
        ghost.presence = 0.45
        stage.add_overlay(ghost)
        ghosts.append(ghost)
    scene.play(orbit.run(orbit.t + step * 1.5, step * 1.5 / SLOW), *stage.turn(yaw=0.1, run_time=step * 1.5 / SLOW),
               run_time=step * 1.5 / SLOW)
    same = txt("same speed · turning velocity", cfg.FONT["label"], cfg.VELOCITY).move_to([-3.6, 3.3, 0])
    scene.play(FadeIn(same, shift=DOWN * 0.1), run_time=0.7)

    # --- 8. What does turning do to the components? --------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    nxt = VGroup(eq(r"v_x", cfg.FONT["body"], cfg.X_COLOR), eq(r"v_y", cfg.FONT["body"], cfg.Y_COLOR),
                 txt("?", cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.35)
    chipped = on_panel(nxt, cfg.MUTED, 0.25).move_to([-3.6, 2.2, 0])
    scene.play(FadeIn(chipped, shift=UP * 0.1), *[stage.fade(g, 0.0) for g in ghosts],
               orbit.run(orbit.t + 1.2, 1.2), run_time=1.2)
    scene.play(orbit.run(orbit.t + 1.6, 1.6 / SLOW), run_time=1.6 / SLOW)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
