"""Scene 10 — speed enters squared, the radius underneath. Two circuits on
one 3D ground share one clock (0.4x real time) and one scale (0.75 stage
units per metre; arrows at true magnitude). The right circuit becomes the
doubled speed (``physics_models.DOUBLE_SPEED``: 8 m/s, 32 m/s^2, four times
the orange arrow), then the doubled radius (``DOUBLE_RADIUS``: 4 m, 4 m/s^2,
half). Ghost velocity arrows after equal times show why: on the wider
circle the velocity turns more gently.
"""

from manim_scenes.common import *

S = 0.75
KV = 0.2
KA = 0.045
SLOW = 0.4                      # film plays at 0.4x real time, for every circuit
LEFT_C = ground(-3.7, 0.2)
RIGHT_C = ground(2.5, 0.2)


class Scene10SpeedRadius(Scene):
    def construct(self) -> None:
        play_scene(self)


def circuit(stage: Stage, model, centre, color: str = cfg.BALL) -> Circuit:
    c = Circuit(stage, model, centre=centre, R=model.r * S, height=0.18, kv=KV, ka=KA, phase=-np.pi / 2,
                color=color, radius=0.17)
    for kind in ("v", "a"):
        c.add_arrow(kind, width=0.075, tip=0.24)
    ring = Curve(ring_curve(centre, model.r * S, 140, h=0.01), cfg.MUTED, width=3.5, opacity=0.75)
    stage.add_body(ring)
    c.ring = ring
    return c


def appear(stage: Stage, c: Circuit, value: float, **kwargs) -> list:
    return [stage.fade(item, value, **kwargs) for item in (c.ball, c.ring, *c.arrows.values())]


def go(stage: Stage, pair, seconds: float) -> Param:
    """Advance both circuits by the same model time, at the scene's one film rate."""
    return run_together(stage, pair, seconds, seconds / SLOW)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "Speed and radius")
    stage = field_stage((0.0, -1.2, 0), zoom=1.12, pitch=0.78, yaw=0.0, half=6.0, step=0.75)
    left = circuit(stage, P, LEFT_C)
    right = circuit(stage, P, RIGHT_C)
    show(scene, stage, 1.0)
    law = eq(r"a_c = \frac{v^2}{r}", cfg.FONT["section"], cfg.ACCEL).move_to([0, 2.75, 0])
    scene.play(*appear(stage, left, 1.0, run_time=0.6), *appear(stage, right, 1.0, run_time=0.6), run_time=0.6)
    scene.play(go(stage, [left, right], 0.6 * SLOW * 4), run_time=2.4)

    # --- 2. Double the speed: four times the acceleration ----------------------------------------------------------------
    beat(scene, t, 1)
    fast = circuit(stage, pm.DOUBLE_SPEED, RIGHT_C, cfg.GREEN)
    fast.t = right.t / 2      # same place on the circle (it turns twice as fast)
    for item in (fast.ball, fast.ring, *fast.arrows.values()):
        item.presence = 0.0
    scene.play(FadeOut(head), FadeIn(law), *appear(stage, right, 0.0, run_time=0.8), *appear(stage, fast, 1.0, run_time=0.8), run_time=0.8)
    tags = VGroup(eq(r"2v", cfg.FONT["section"], cfg.VELOCITY), eq(r"\Rightarrow", cfg.FONT["section"]),
                  eq(r"4a", cfg.FONT["section"], cfg.ACCEL)).arrange(RIGHT, buff=0.3).move_to([4.4, 1.85, 0])
    scene.play(FadeIn(tags, shift=DOWN * 0.1), go(stage, [left, fast], 0.5), run_time=1.25)
    scene.play(go(stage, [left, fast], 1.7), run_time=4.25)
    scene.play(go(stage, [left, fast], 1.6), run_time=4)

    # --- 3. 8 m/s would need 32 m/s^2 -----------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    values = VGroup(eq(rf"{V}\ \mathrm{{m/s}} \to {AC}\ \mathrm{{m/s^2}}", cfg.FONT["body"], cfg.WHITE).move_to([-4.4, 1.85, 0]),
                    eq(rf"{wh(pm.DOUBLE_SPEED.v)}\ \mathrm{{m/s}} \to {wh(pm.DOUBLE_SPEED.accel)}\ \mathrm{{m/s^2}}",
                       cfg.FONT["body"], cfg.GREEN).move_to([4.4, 0.85, 0]))
    scene.play(FadeIn(values[0]), go(stage, [left, fast], 0.4), run_time=1)
    scene.play(FadeIn(values[1]), go(stage, [left, fast], 0.4), run_time=1)
    scene.play(go(stage, [left, fast], 3.2), run_time=8.0)

    # --- 4. Double the radius: half the acceleration ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    wide = circuit(stage, pm.DOUBLE_RADIUS, RIGHT_C)
    for item in (wide.ball, wide.ring, *wide.arrows.values()):
        item.presence = 0.0
    wide.t = left.t
    scene.play(*appear(stage, fast, 0.0, run_time=0.8), FadeOut(VGroup(tags, values[1])), run_time=0.8)
    scene.play(*appear(stage, wide, 1.0, run_time=0.8), run_time=0.8)
    half = VGroup(eq(r"2r", cfg.FONT["section"], cfg.POSITION), eq(r"\Rightarrow", cfg.FONT["section"]),
                  eq(r"\tfrac12 a", cfg.FONT["section"], cfg.ACCEL)).arrange(RIGHT, buff=0.3).move_to([4.4, 1.85, 0])
    wide_value = eq(rf"{V}\ \mathrm{{m/s}} \to {wh(pm.DOUBLE_RADIUS.accel)}\ \mathrm{{m/s^2}}", cfg.FONT["body"], cfg.WHITE)
    wide_value.move_to([4.4, 0.75, 0])
    scene.play(FadeIn(half, shift=DOWN * 0.1), go(stage, [left, wide], 0.3), run_time=0.75)
    scene.play(FadeIn(wide_value), go(stage, [left, wide], 0.3), run_time=0.75)
    scene.play(go(stage, [left, wide], 2.6), run_time=6.5)

    # --- 5. Equal times: the wide circle turns the velocity more gently ---------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(half, wide_value, values[0])), run_time=0.5)
    ghosts = []
    step = 0.45
    for _ in range(4):
        for c in (left, wide):
            p = c.world()
            ghost = Vector(p, p + ground_vec(c.view.vel(c.t) * KV), cfg.VELOCITY, width=0.055, tip=0.2, glow=False)
            ghost.presence = 0.5
            stage.add_overlay(ghost)
            ghosts.append(ghost)
        scene.play(run_together(stage, [left, wide], step, step / SLOW), run_time=step / SLOW)
    turned = VGroup(eq(rf"\Delta\theta = {fx(P.angular_speed * step, 2)}\ \text{{rad per step}}", cfg.FONT["small"], cfg.ANGLE).move_to([-4.4, 1.6, 0]),
                    eq(rf"\Delta\theta = {fx(pm.DOUBLE_RADIUS.angular_speed * step, 2)}\ \text{{rad per step}}", cfg.FONT["small"], cfg.ANGLE).move_to([4.4, 1.6, 0]))
    scene.play(FadeIn(turned), run_time=0.8)
    scene.wait(1.6)

    # --- 6. Sharp bend, broad curve -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    names = VGroup(chip("sharp bend", cfg.ACCEL).move_to([-4.4, 0.85, 0]), chip("broad curve", cfg.CYAN).move_to([4.4, 0.85, 0]))
    scene.play(*[stage.fade(g, 0.0) for g in ghosts], FadeIn(names, shift=DOWN * 0.1), run_time=0.8)
    scene.play(go(stage, [left, wide], 2.6), run_time=6.5)

    # --- 7. Fast and tight: the most acceleration -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    rules = VGroup(eq(r"a \propto v^2", cfg.FONT["section"], cfg.VELOCITY), eq(r"a \propto \frac{1}{r}", cfg.FONT["section"], cfg.POSITION))
    rules.arrange(RIGHT, buff=1.2).move_to([0, 2.75, 0])
    scene.play(FadeOut(VGroup(turned, names)), fade_through(law, rules), go(stage, [left, wide], 0.3), run_time=0.75)
    scene.play(go(stage, [left, wide], 1.2), run_time=3)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
