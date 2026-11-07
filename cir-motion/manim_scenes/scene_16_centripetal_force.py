"""Scene 16 — centripetal force. Newton's second law turns the inward
acceleration into an inward net force (green, drawn on the reference
particle beside its orange acceleration): F_c = m v^2 / r = m r omega^2,
2 (4^2) / 2 = 16 N for the 2 kg particle. Then the most important point: it
is a job, not a new force. Three small panels show who does the job:
tension (a ball on a string), friction (a car on a flat curve), gravity (a
satellite) — the same green arrow toward the centre in each.
"""

from manim_scenes.common import *

C = np.array([-3.6, -0.5, 0])
R = 2.3
COL = 3.5
KF = 1.4 / P.force                    # screen units per newton


class Scene16CentripetalForce(Scene):
    def construct(self) -> None:
        play_scene(self)


def job_panel(x: float, kind: str) -> VGroup:
    """A small icon of one way to supply the inward force, with its green arrow."""
    box = panel(4.2, 3.6, cfg.MUTED, 0.55).move_to([x, -1.2, 0])
    centre = box.get_center() + UP * 0.25
    ring = Circle(radius=1.0, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6).move_to(centre)
    where = centre + 1.0 * np.array([np.cos(0.5), np.sin(0.5), 0])
    inward = mu.unit(centre - where)
    parts = VGroup(box, ring)
    if kind == "tension":
        parts.add(Line(centre, where, stroke_color=cfg.WHITE, stroke_width=3), Dot(centre, radius=0.07, color=cfg.MUTED),
                  bead(where, cfg.BALL, 0.16))
        name = "tension"
    elif kind == "friction":
        road = Circle(radius=1.0, stroke_color=cfg.GRAY, stroke_width=18, stroke_opacity=0.5).move_to(centre)
        car = Car(cfg.CAR, 0.5)
        car.set_pose(where, 0.5 + PI / 2)
        parts.add(road, car)
        name = "friction"
    else:
        parts.add(bead(centre, cfg.EARTH, 0.55), bead(where, cfg.WHITE, 0.1))
        name = "gravity"
    parts.add(VecArrow(where, where + inward * 0.75, cfg.FORCE, width=0.08, tip_len=0.22, live=False))
    parts.add(txt(name, cfg.FONT["label"], cfg.FORCE).next_to(box.get_bottom(), UP, buff=0.25))
    return parts


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "16")
    chapter_open(scene, 5, "Centripetal acceleration and force")
    head = heading("Centripetal force")
    view = CircleView(C, R, P, kv=1.0 / P.v, ka=1.4 / P.accel)
    a_arrow = view.arrow("a", width=0.09)
    scene.play(FadeIn(head, shift=DOWN * 0.18), FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), run_time=0.8)
    scene.add(a_arrow)
    scene.play(a_arrow.grow_in(run_time=0.6), run_time=0.6)
    cause = chip("what causes it?", cfg.WHITE).move_to([COL, 2.6, 0])
    scene.play(FadeIn(cause), view.run(1.0, 3.0), run_time=3.0)

    # --- 2. Newton's second law -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    newton = paint(eq([r"\vec F_{\text{net}}", "=", r"m\,\vec a"], cfg.FONT["title"]), {0: cfg.FORCE, 2: cfg.ACCEL}).move_to([COL, 2.6, 0])
    scene.play(FadeOut(head), fade_through(cause, newton), view.run(view.clock.value + 0.5, 1.2), run_time=1.2)
    scene.play(view.run(view.clock.value + 1.0, 3.0), run_time=3.0)

    # --- 3. The net force points to the centre too ------------------------------------------------------------------------------
    beat(scene, t, 2)
    # Drawn beside the acceleration (a small sideways offset) so both arrows stay visible.
    side = lambda: view.unit_t() * 0.16  # noqa: E731
    force = VecArrow(lambda: view.point() + side(), lambda: view.point() + side() + view.acc_radial() * P.m * KF,
                     cfg.FORCE, width=0.1)
    scene.add(force)
    scene.play(force.grow_in(run_time=1.0), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)
    names = VGroup(eq(r"\vec F_{\text{net}}", cfg.FONT["small"], cfg.FORCE), eq(r"\vec a", cfg.FONT["small"], cfg.ACCEL))
    names.arrange(RIGHT, buff=0.6).move_to([-3.6, 3.2, 0])
    both = txt("both toward the centre", cfg.FONT["small"], cfg.WHITE).next_to(newton, DOWN, buff=0.45)
    scene.play(FadeIn(names), FadeIn(both), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)
    scene.play(view.run(view.clock.value + 2.0, 6.0), run_time=6.0)

    # --- 4. F_c = m v^2 / r = m r omega^2 -------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    fc = paint(eq([r"F_c", "=", r"\frac{m v^2}{r}", "=", r"m r \omega^2"], cfg.FONT["section"]), {0: cfg.FORCE}).next_to(newton, DOWN, buff=0.5)
    scene.play(FadeOut(both), view.run(view.clock.value + 0.2, 0.4), run_time=0.4)
    scene.play(Write(fc), view.run(view.clock.value + 0.4, 1.2), run_time=1.2)
    scene.play(FadeIn(boxed(fc, cfg.FORCE)[0]), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)
    scene.play(view.run(view.clock.value + 2.6, 8.0), run_time=8.0)

    # --- 5. 2 (4^2) / 2 = 16 N -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    numbers = eq([r"F_c", "=", rf"\frac{{{MASS}\,({V}^2)}}{{{R_M}}}", "=", rf"{FC}\ \mathrm{{N}}"], cfg.FONT["section"])
    paint(numbers, {0: cfg.FORCE, 4: cfg.FORCE}).next_to(fc, DOWN, buff=0.75)
    mass = eq(rf"m = {MASS}\ \mathrm{{kg}}", cfg.FONT["body"], cfg.WHITE).next_to(numbers, DOWN, buff=0.4)
    scene.play(FadeIn(mass), Write(numbers), view.run(view.clock.value + 0.6, 1.6), run_time=1.6)
    scene.play(FadeIn(boxed(numbers[4], cfg.RESULT, 0.12)[0]), view.run(view.clock.value + 0.3, 0.8), run_time=0.8)
    scene.play(view.run(view.clock.value + 2.6, 8.0), run_time=8.0)

    # --- 6. Not a new kind of force ----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    for m in (a_arrow, force, view.ball):
        m.clear_updaters()
    clear(scene, run_time=0.7)
    myth = chip("a new kind of force", cfg.WARNING, cfg.FONT["section"]).move_to([0, 0.6, 0])
    scene.play(FadeIn(myth, scale=0.95), run_time=0.8)
    cross = strike(myth, width=10)
    scene.play(Create(cross), run_time=0.6)

    # --- 7. A job: the net inward force needed -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    job = VGroup(txt("centripetal force", cfg.FONT["section"], cfg.FORCE),
                 txt("net inward force", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.3)
    fit_width(job, 13.0)
    job.move_to([0, 0.6, 0])
    scene.play(FadeOut(VGroup(myth, cross)), run_time=0.5)
    scene.play(FadeIn(job, shift=UP * 0.1), run_time=1.0)
    real = txt("tension · friction · gravity", cfg.FONT["label"], cfg.WHITE).next_to(job, DOWN, buff=0.6)
    scene.play(FadeIn(real), run_time=0.8)

    # --- 8. Tension, friction, gravity -----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(job.animate.scale(0.75).move_to([0, 3.0, 0]), FadeOut(real), run_time=0.8)
    panels = [job_panel(x, kind) for x, kind in zip((-4.7, 0.0, 4.7), ("tension", "friction", "gravity"))]
    for p in panels:
        scene.play(FadeIn(p, shift=UP * 0.15), run_time=1.0)
        scene.wait(0.8)

    # --- 9. Different forces, the same requirement ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    same = result_label("same requirement", cfg.FORCE, cfg.FONT["label"]).move_to([0, 1.35, 0])
    scene.play(FadeIn(same, shift=DOWN * 0.1), run_time=0.8)
    scene.play(*[Indicate(p[-2], color=cfg.FORCE, scale_factor=1.15) for p in panels], run_time=1.4)
    scene.play(*[Indicate(p[-1], color=cfg.WHITE, scale_factor=1.06) for p in panels], run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
