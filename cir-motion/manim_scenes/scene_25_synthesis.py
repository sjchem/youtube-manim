"""Scene 25 — one chain of reasoning. The opening question returns with a
constant-speed particle; then the chain builds: changing direction ->
changing velocity -> acceleration -> net force, toward the centre. The
reference particle's five descriptions are tiled round it (4 m/s, 2 rad/s,
pi s, 8 m/s^2, 16 N); the three providers of the inward force return from
scene 16; and the film closes where it began, on a 3D track, with the car's
velocity and acceleration arrows turning together.
"""

from manim_scenes.common import *
from manim_scenes.scene_16_centripetal_force import job_panel


class Scene25Synthesis(Scene):
    def construct(self) -> None:
        play_scene(self)


def link(body: str, color: str) -> VGroup:
    return chip(body, color, cfg.FONT["small"])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "25", "One chain of reasoning")
    view = CircleView([0, -0.9, 0], 1.8, P, kv=1.0 / P.v)
    v = view.arrow("v", width=0.09)
    question = txt("accelerate without getting faster?", cfg.FONT["section"], cfg.WHITE).move_to([0, 2.2, 0])
    fit_width(question, 12.6)
    scene.play(FadeIn(head, shift=DOWN * 0.18), FadeIn(VGroup(view.ring, view.hub, view.ball)), run_time=0.8)
    scene.add(v)
    scene.play(FadeIn(question, shift=UP * 0.1), v.grow_in(run_time=0.6), view.run(0.4, 1.0), run_time=1.0)
    scene.play(view.run(1.6, 3.6), run_time=3.6)

    # --- 2. Yes: acceleration is changing velocity ----------------------------------------------------------------------------
    beat(scene, t, 1)
    yes = result_label("Yes.", cfg.GOLD, cfg.FONT["hero"]).move_to([-4.6, 2.2, 0])
    meaning = eq(r"\vec a = \frac{d\vec v}{dt}", cfg.FONT["section"], cfg.ACCEL).move_to([4.4, 2.2, 0])
    a = view.arrow("a", width=0.09)
    scene.add(a)
    scene.play(FadeOut(head), fade_through(question, yes), a.grow_in(run_time=1.0), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)
    scene.play(FadeIn(meaning), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)
    scene.play(view.run(view.clock.value + 1.6, 4.0), run_time=4.0)

    # --- 3. Changing direction -> changing velocity -> acceleration -------------------------------------------------------------------
    beat(scene, t, 2)
    for m in (view.ball, v, a):
        m.clear_updaters()
    clear(scene, run_time=0.6)
    chain = VGroup(link("changing direction", cfg.VELOCITY), txt("⇒", cfg.FONT["section"], cfg.WHITE),
                   link("changing velocity", cfg.VELOCITY), txt("⇒", cfg.FONT["section"], cfg.WHITE),
                   link("acceleration", cfg.ACCEL)).arrange(RIGHT, buff=0.3)
    fit_width(chain, 13.6)
    chain.move_to([0, 1.2, 0])
    for k in (0, 2, 4):
        scene.play(*[FadeIn(chain[j], shift=RIGHT * 0.1) for j in range(max(k - 1, 0), k + 1)], run_time=0.8)
        scene.wait(0.8)

    # --- 4. ... -> net force, toward the centre ------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    force = VGroup(txt("⇒", cfg.FONT["section"], cfg.WHITE), link("net force", cfg.FORCE)).arrange(RIGHT, buff=0.3)
    force.next_to(chain, DOWN, buff=0.6).align_to(chain, RIGHT)
    centre = txt("uniform motion: inward", cfg.FONT["label"], cfg.WHITE).next_to(force, DOWN, buff=0.5)
    newton = eq(r"\vec F_{\text{net}} = m\vec a", cfg.FONT["body"], cfg.FORCE).next_to(force, LEFT, buff=0.8)
    scene.play(FadeIn(force, shift=RIGHT * 0.1), FadeIn(newton), run_time=1.0)
    scene.play(FadeIn(centre, shift=UP * 0.1), run_time=0.8)

    # --- 5. One particle, many descriptions --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    clear(scene, run_time=0.6)
    ref = CircleView([-3.4, -0.5, 0], 2.2, P, kv=1.0 / P.v, ka=1.3 / P.accel)
    arrows = [ref.arrow("v", width=0.09), ref.arrow("a", width=0.09)]
    scene.add(ref.ring, ref.hub, ref.ball, *arrows)
    scene.play(FadeIn(VGroup(ref.ring, ref.hub, ref.ball)), *[x.grow_in(run_time=0.7) for x in arrows], run_time=0.7)
    tiles = VGroup(scalar_tile("speed", rf"{V}\ \mathrm{{m/s}}", cfg.VELOCITY),
                   scalar_tile("angular speed", rf"{OMEGA}\ \mathrm{{rad/s}}", cfg.ANGLE),
                   scalar_tile("period", r"\pi\ \mathrm{s}", cfg.WHITE),
                   scalar_tile("acceleration", rf"{AC}\ \mathrm{{m/s^2}}", cfg.ACCEL),
                   scalar_tile("inward force", rf"{FC}\ \mathrm{{N}}", cfg.FORCE),
                   scalar_tile("mass · radius", rf"{MASS}\ \mathrm{{kg}} \cdot {R_M}\ \mathrm{{m}}", cfg.MUTED))
    tiles.arrange_in_grid(3, 2, buff=0.3).move_to([3.4, -0.2, 0])
    for tile in tiles:
        scene.play(FadeIn(tile, shift=UP * 0.1), ref.run(ref.clock.value + 0.35, 1.0), run_time=1.0)
    one = result_label("one motion, many descriptions", cfg.GOLD, cfg.FONT["label"]).move_to([0, 3.3, 0])
    scene.play(FadeIn(one), ref.run(ref.clock.value + 0.3, 0.8), run_time=0.8)
    scene.play(ref.run(ref.clock.value + 2.2, 7.0), run_time=7.0)

    # --- 6. String, curve, orbit: the same reasoning --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    for m in (ref.ball, *arrows):
        m.clear_updaters()
    clear(scene, run_time=0.6)
    panels = [job_panel(x, kind) for x, kind in zip((-4.7, 0.0, 4.7), ("tension", "friction", "gravity"))]
    scene.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in panels], lag_ratio=0.3), run_time=2.0)
    reasoning = result_label("different forces, the same reasoning", cfg.FORCE, cfg.FONT["label"]).move_to([0, 2.4, 0])
    scene.play(FadeIn(reasoning, shift=DOWN * 0.1), run_time=0.8)
    scene.wait(3.0)

    # --- 7. Direction matters ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    clear(scene, run_time=0.6)
    matters = VGroup(txt("not speed alone:", cfg.FONT["section"], cfg.WHITE), txt("direction matters", cfg.FONT["hero"], cfg.GOLD)).arrange(DOWN, buff=0.3)
    scene.play(FadeIn(matters[0], shift=UP * 0.1), run_time=0.7)
    scene.play(FadeIn(matters[1], scale=0.95), run_time=1.0)

    # --- 8. Back on the track: the power of thinking in vectors --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    stage = field_stage((0.0, -1.0, 0), zoom=1.35, pitch=0.78, yaw=-0.3, half=4.2, spin=0.0)
    track = Band(ring_points(ORIGIN, 2.4, 160), 0.32, cfg.ROAD, edge=cfg.MUTED, centre_line=cfg.WHITE)
    stage.add_body(track)
    car = Circuit(stage, P, R=2.4, body="car", color=cfg.CAR, car_length=0.62, kv=1.1 / P.v, ka=1.0 / P.accel, phase=-np.pi / 2)
    for kind in ("v", "a"):
        car.add_arrow(kind, width=0.08, lift=0.28, presence=1.0)
    scene.play(FadeOut(matters), run_time=0.6)
    show(scene, stage, 1.0)
    vectors = txt("thinking in vectors", cfg.FONT["title"], cfg.GOLD).move_to([0, 3.3, 0])
    scene.play(FadeIn(vectors, shift=DOWN * 0.1), car.run(car.t + 0.4, 1.2), run_time=1.2)
    scene.play(car.run(car.t + 3.0, 9.0), *stage.turn(yaw=0.3, run_time=9.0), run_time=9.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["25"])
