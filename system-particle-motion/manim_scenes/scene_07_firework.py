"""Scene 07 — the exploding firework. On a 3D stage a shell rises along a
dashed parabola (no air resistance). At the apex it bursts into five
fragments of different mass, thrown apart by internal forces: their momentum
kicks, drawn from the burst point, add to zero. The fragments fly off in 3D
with glowing trails, and the centre-of-mass target of all of them rides the
original parabola, until the first fragment lands: the ground pushes, and the
target leaves the dashed curve.
"""

from manim_scenes.common import *

F = pm.FIREWORK
SC = 0.40                                   # screen units per metre
GROUND = np.array([-5.1, 0.0, 0.0])         # launch point in stage coordinates
FRAG_COLORS = [cfg.GOLD, cfg.ORANGE, cfg.ROSE, cfg.CYAN, cfg.GREEN]


class Scene07Firework(Scene):
    def construct(self) -> None:
        play_scene(self)


def world(p: np.ndarray) -> np.ndarray:
    return GROUND + np.asarray(p) * SC


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "The exploding firework")
    stage = Stage((-0.6, -2.25, 0.0), zoom=1.05, yaw=-0.18, pitch=0.16, sway=0.03)
    floor(stage, 0.0, reach=8.0, opacity=0.24)
    clock = Knob(0.0)
    end_t = 2 * F.v0[1] / pm.G

    path = Curve(np.array([world(pm.shell_position(s)) for s in np.linspace(0, end_t, 80)]), cfg.MUTED, width=3,
                 opacity=0.75, dashed=True, glow=False)
    shell = Ball(lambda: world(pm.shell_position(min(clock.value, F.burst_time))), 0.2, cfg.CORAL)
    rise = Curve(lambda: np.array([world(pm.shell_position(s)) for s in np.linspace(0, min(max(clock.value, 1e-3), F.burst_time), 30)]),
                 cfg.CORAL, width=4)
    stage.add_body(path, rise, shell)
    show(scene, stage, 1.0)
    no_air = caption("ignoring air resistance: a parabola", cfg.MUTED)
    scene.play(FadeIn(no_air), run_time=0.6)
    scene.play(clock.to(stage, F.burst_time - 0.02, rate_func=rate_functions.ease_out_sine), run_time=3.4)

    # --- 2. The burst -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    frags = [Ball(lambda k=k: world(pm.fragment_positions(max(clock.value, F.burst_time))[k]), 0.1 + 0.28 * m,
                  FRAG_COLORS[k]) for k, m in enumerate(F.masses)]

    def trail(k: int):
        def pts():
            now = max(clock.value, F.burst_time + 1e-3)
            return np.array([world(pm.fragment_positions(s)[k]) for s in np.linspace(F.burst_time, now, 30)])
        return pts

    trails = [Curve(trail(k), FRAG_COLORS[k], width=3, opacity=0.7) for k in range(len(F.masses))]
    hidden(*frags, *trails)
    stage.add_body(*trails, *frags)
    burst_at = world(pm.shell_position(F.burst_time))
    flash = Tag(VGroup(*[Circle(radius=r, stroke_width=0, fill_color=cfg.GOLD, fill_opacity=0.12) for r in (0.4, 0.7, 1.0)]),
                burst_at)
    flash.presence = 0.0
    stage.add_overlay(flash)
    scene.play(clock.to(stage, F.burst_time), stage.fade(shell, 0.0), stage.fade(rise, 0.3),
               *[stage.fade(f, 1.0) for f in frags], stage.fade(flash, 1.0), FadeOut(no_air), run_time=0.5)
    scene.play(clock.to(stage, F.burst_time + 0.12, rate_func=linear), *[stage.fade(tr, 1.0) for tr in trails],
               stage.fade(flash, 0.0), run_time=1.2)

    # --- 3. Internal: the kicks add to zero -----------------------------------------------------------------------
    beat(scene, t, 2)
    kicks = pm.fragment_kicks()
    masses = np.asarray(F.masses)
    vectors = [Vector(burst_at, burst_at + masses[k] * kicks[k] * 1.4, FRAG_COLORS[k], width=0.06, tip=0.2)
               for k in range(len(masses))]
    hidden(*vectors)
    stage.add_overlay(*vectors)
    scene.play(*[stage.fade(v, 1.0) for v in vectors], run_time=1.0)
    total = eq(r"\sum_i m_i\,\Delta \vec v_i = 0", cfg.FONT["section"], cfg.FORCE).move_to([4.7, 3.3, 0])
    internal = caption("burst forces are internal: equal and opposite pairs", cfg.FORCE)
    scene.play(Write(total), FadeIn(internal), run_time=1.4)

    # --- 4. The centre rides the parabola -------------------------------------------------------------------------------
    beat(scene, t, 3)
    land = pm.first_landing()
    target = com_tag(lambda: world(pm.fragment_com(clock.value)), 0.2)
    target.presence = 0.0
    stage.add_overlay(target)
    scene.play(*[stage.fade(v, 0.0) for v in vectors], stage.fade(target, 1.0), FadeOut(internal), run_time=0.8)
    gravity = caption("only gravity acts from outside", cfg.WHITE)
    scene.play(FadeIn(gravity), run_time=0.6)
    scene.play(clock.to(stage, land - 0.01, rate_func=linear), *stage.turn(yaw=-0.42, pitch=0.22), run_time=7.0)
    rides = caption("COM follows the original parabola", cfg.WHITE)
    scene.play(fade_through(gravity, rides), set_attr(stage, path, "opacity", 1.0), run_time=1.0)

    # --- 5. The first fragment lands: a new external force ------------------------------------------------------------------
    beat(scene, t, 4)
    ground_push = caption("first impact: an external ground force", cfg.WARNING)
    scene.play(fade_through(rides, ground_push), run_time=0.8)
    scene.play(clock.to(stage, land + 0.55, rate_func=linear), run_time=4.0)
    ring = Circle(radius=0.5, stroke_color=cfg.WARNING, stroke_width=6).move_to(stage.screen_point(pm.fragment_com(clock.value) * SC + GROUND))
    scene.play(Create(ring), run_time=0.5)
    scene.play(FadeOut(ring, scale=1.6), run_time=0.6)

    # --- 6. Summary ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    rule = VGroup(txt("Internal forces rearrange a system.", cfg.FONT["body"], cfg.FORCE),
                  txt("External forces change its centre-of-mass motion.", cfg.FONT["body"], cfg.WHITE)).arrange(DOWN, buff=0.2)
    fit_width(rule, 13.0)
    rule.move_to(UP * 2.9)
    scene.play(fade_through(total, rule), FadeOut(ground_push),
               *[stage.fade(item, 0.35) for item in [path, rise, *trails, *frags]], run_time=1.0)
    finish(scene, t, stage)
