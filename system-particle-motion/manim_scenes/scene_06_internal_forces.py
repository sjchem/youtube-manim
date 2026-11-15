"""Scene 06 — internal forces cancel. Five beads of different mass, joined by
glowing springs, wobble freely (a seeded velocity-Verlet run from
``physics_models``); their centre-of-mass target stays still. One spring
lights up with its third-law pair of green arrows, then every pair. The
derivation builds on the right: m_i a_i = F_i, sum, the internal pairs cancel
(struck out), the sum of m_i a_i is M a_cm, so F_ext = M a_cm (boxed). The
test: a steady green push on one bead only. The cluster stretches, wobbles
and turns as it crosses the screen, while its centre glides along a straight
line in exact step with a lone white point mass M pushed by the same force.
"""

from manim_scenes.common import *

S = 1.9                                       # screen units per metre (the free cluster)
S_TEST = 1.15                                 # the travelling tests need room to cross the screen
FREE_AT = np.array([-3.9, -0.5, 0.0])         # where the free cluster wobbles
PUSH_AT = np.array([-4.2, -0.6, 0.0])         # where the pushed run starts
TEST_SECONDS = 8.5
ARROW_PER_N = 0.42
MASSES = np.asarray(pm.SPRINGS.masses)
EDGES = pm.cluster_edges()


class Scene06InternalForces(Scene):
    def construct(self) -> None:
        play_scene(self)


class ClusterView(VGroup):
    """The spring cluster drawn from a stored run at film time ``clock``."""

    def __init__(self, run, at, clock: Knob, scale: float = S) -> None:
        super().__init__()
        self.sigma = scale            # never self.scale: that would shadow Mobject.scale
        self.times, self.frames, self.pairs = run
        self.at, self.clock = np.asarray(at, dtype=float), clock
        self.springs = VGroup(*[VMobject(stroke_color=cfg.MUTED, stroke_width=3.5, stroke_opacity=0.85) for _ in EDGES])
        size = scale / S
        self.beads = VGroup(*[bead(ORIGIN, cfg.MASS, (0.14 + 0.05 * m) * size, glow=0.6) for m in MASSES])
        self.add(self.springs, self.beads)
        self.add_updater(lambda m: m.refresh())
        self.refresh()

    def _index(self) -> tuple[int, float]:
        k = float(np.clip(self.clock.value / (self.times[1] - self.times[0]), 0, len(self.times) - 1.001))
        return int(k), k - int(k)

    def positions(self) -> np.ndarray:
        i, f = self._index()
        xy = self.frames[i] * (1 - f) + self.frames[i + 1] * f
        return np.column_stack([xy * self.sigma, np.zeros(len(xy))]) + self.at

    def pair_force(self, edge: int) -> np.ndarray:
        i, f = self._index()
        v = self.pairs[i][edge] * (1 - f) + self.pairs[i + 1][edge] * f
        return np.array([v[0], v[1], 0.0])

    def com(self) -> np.ndarray:
        return pm.com(MASSES, self.positions())

    def refresh(self) -> "ClusterView":
        pts = self.positions()
        for spring, (i, j) in zip(self.springs, EDGES):
            spring.set_points_as_corners(zigzag(pts[i], pts[j]))
        for b, p in zip(self.beads, pts):
            b.move_to(p)
        return self


def zigzag(a: np.ndarray, b: np.ndarray, turns: int = 7, amp: float = 0.09) -> list[np.ndarray]:
    d = b - a
    n = np.linalg.norm(d)
    side = np.array([-d[1], d[0], 0.0]) / max(n, 1e-6)
    pts = [a, a + d * 0.15]
    for k in range(turns):
        f = 0.15 + 0.7 * (k + 0.5) / turns
        pts.append(a + d * f + side * amp * (1 if k % 2 else -1))
    pts += [a + d * 0.85, b]
    return pts


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "06", "Internal forces cancel")
    clock = Knob(0.0)
    free = ClusterView(pm.spring_cluster_run(False, 75.0), FREE_AT, clock)
    target = com_target(0.18)
    target.add_updater(lambda m: m.move_to(free.com()))
    scene.play(FadeIn(free), FadeIn(target), run_time=1.2)
    drive(free, clock, 1.0)
    joined = caption("five particles, joined by springs", cfg.WHITE)
    scene.play(FadeIn(joined), run_time=0.8)

    # --- 2. Internal vs external ------------------------------------------------------------------------------
    beat(scene, t, 1)
    legend = VGroup(chip("internal: between particles", cfg.FORCE), chip("external: from outside", cfg.WARNING))
    legend.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.9, 3.0, 0])
    fit_width(legend, 6.6)
    scene.play(FadeOut(joined), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in legend], lag_ratio=0.4), run_time=1.4)

    # --- 3. Third-law pairs ---------------------------------------------------------------------------------------
    beat(scene, t, 2)
    def pair_arrows(edge: int, width: float = 0.07) -> list[VecArrow]:
        i, j = EDGES[edge]
        on_i = VecArrow(lambda: free.positions()[i], lambda: free.positions()[i] + free.pair_force(edge) * ARROW_PER_N,
                        cfg.FORCE, width=width, tip_len=0.2)
        on_j = VecArrow(lambda: free.positions()[j], lambda: free.positions()[j] - free.pair_force(edge) * ARROW_PER_N,
                        cfg.FORCE, width=width, tip_len=0.2)
        return [on_i, on_j]

    first = pair_arrows(0, 0.1)
    free.springs[0].set_stroke(cfg.FORCE, width=5)
    scene.add(*first)
    scene.play(*[a.grow_in(run_time=0.9) for a in first], run_time=0.9)
    third = eq(r"\vec F_{12} = -\vec F_{21}", cfg.FONT["section"], cfg.FORCE).move_to([-3.9, -3.55, 0])
    scene.play(Write(third), run_time=1.4)
    scene.wait(2.0)
    rest = [a for e in range(1, len(EDGES)) for a in pair_arrows(e)]
    scene.add(*rest)
    scene.play(*[a.grow_in(run_time=1.2) for a in rest], run_time=1.2)

    # --- 4. Newton's second law for each particle ---------------------------------------------------------------------
    beat(scene, t, 3)
    rows = VGroup(
        eq(r"m_i \vec a_i = \vec F_i", cfg.FONT["body"]),
        eq([r"\sum_i m_i \vec a_i", "=", r"\sum \vec F_{\text{ext}}", "+", r"\sum \vec F_{\text{int}}"], cfg.FONT["body"]),
        eq([r"M \vec a_{\mathrm{cm}}", "=", r"\sum \vec F_{\text{ext}}"], cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    fit_width(rows, 7.6)
    rows.move_to([3.9, 0.3, 0])
    rows[1][2].set_color(cfg.WARNING)
    rows[1][4].set_color(cfg.FORCE)
    rows[2][2].set_color(cfg.WARNING)
    scene.play(Write(rows[0]), run_time=1.4)

    # --- 5. Sum them ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(Write(rows[1]), run_time=2.0)

    # --- 6. Internal pairs cancel ---------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    slash = cancel(rows[1][4], cfg.FORCE)
    zero = eq("0", cfg.FONT["body"], cfg.FORCE).next_to(rows[1][4], UP, buff=0.3)
    scene.play(Create(slash), FadeIn(zero, shift=DOWN * 0.1), *[a.fade_to(0.25, run_time=1.0) for a in first + rest],
               run_time=1.0)
    pairs_cancel = caption("internal forces cancel in the sum", cfg.FORCE)
    scene.play(fade_through(third, pairs_cancel), run_time=0.8)

    # --- 7. The left side is M a_cm ---------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    brace = Brace(rows[1][0], DOWN, color=cfg.MUTED)
    brace_tag = eq(r"M \vec a_{\mathrm{cm}}", cfg.FONT["label"], cfg.WHITE).next_to(brace, DOWN, buff=0.1)
    scene.play(FadeOut(pairs_cancel), GrowFromCenter(brace), FadeIn(brace_tag), run_time=1.0)
    scene.wait(1.5)
    scene.play(fade_through(VGroup(brace, brace_tag), rows[2]), FadeOut(zero), run_time=1.2)

    # --- 8. The law ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    law = eq(r"\vec F_{\text{ext}} = M \vec a_{\mathrm{cm}}", cfg.FONT["title"], cfg.WHITE)
    law_box = boxed(law, cfg.RESULT).move_to([3.8, 0.3, 0])
    scene.play(FadeOut(rows[:2]), FadeOut(slash), run_time=0.4)
    scene.play(ReplacementTransform(rows[2], law), run_time=0.8)
    scene.play(Create(law_box.frame), run_time=0.8)

    # --- 9. The test: push one particle ---------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    for arrow in first + rest:
        arrow.clear_updaters()
    free.clear_updaters()
    target.clear_updaters()
    scene.play(FadeOut(free), FadeOut(target), FadeOut(legend), *[FadeOut(a) for a in first + rest],
               VGroup(law_box.frame, law).animate.scale(0.62).move_to([4.6, 3.1, 0]), run_time=1.0)
    clock2 = Knob(0.0)
    run = pm.spring_cluster_run(True)
    pushed = ClusterView(run, PUSH_AT, clock2, S_TEST)
    start_com = pushed.com()
    a_cm = np.array([*pm.SPRINGS.a_cm, 0.0]) * S_TEST
    point_mass = glow_dot(start_com, cfg.WHITE, 0.1, reach=2.4)
    point_mass.add_updater(lambda m: m.move_to(start_com + 0.5 * a_cm * clock2.value ** 2 + DOWN * 1.5))
    target2 = com_target(0.18)
    target2.add_updater(lambda m: m.move_to(pushed.com()))
    track = DashedLine(start_com + LEFT * 0.3, start_com + RIGHT * 7.6, stroke_color=cfg.MUTED, stroke_width=2.5,
                       dash_length=0.14)
    lone_track = track.copy().shift(DOWN * 1.5)
    force = VecArrow(lambda: pushed.positions()[pm.SPRINGS.push_on] - np.array([*pm.SPRINGS.force, 0]) * 1.2,
                     lambda: pushed.positions()[pm.SPRINGS.push_on], cfg.WARNING, width=0.11, tip_len=0.3)
    lone_force = VecArrow(lambda: point_mass.get_center() - np.array([*pm.SPRINGS.force, 0]) * 1.2,
                          lambda: point_mass.get_center(), cfg.WARNING, width=0.09, tip_len=0.26)
    m_tag = eq("M", cfg.FONT["label"], cfg.MASS)
    m_tag.add_updater(lambda m: m.next_to(point_mass, DOWN, buff=0.18))
    scene.play(FadeIn(pushed), FadeIn(target2), Create(track), run_time=1.0)
    scene.add(force)
    scene.play(force.grow_in(run_time=0.6), run_time=0.6)
    scene.play(FadeIn(point_mass), FadeIn(m_tag), Create(lone_track), run_time=0.8)
    scene.add(lone_force)
    scene.play(lone_force.grow_in(run_time=0.5), run_time=0.5)
    scene.play(clock2.to(pushed, TEST_SECONDS, rate_func=linear), run_time=TEST_SECONDS)
    same = caption("same external force · same COM acceleration", cfg.WHITE)
    scene.play(FadeIn(same), run_time=0.8)

    # --- 10. A caution: where the force acts decides the turning -------------------------------------------------------------------------------
    beat(scene, t, 9)
    for mob in (pushed, target2, point_mass, m_tag, force, lone_force):
        mob.clear_updaters()
    scene.play(*[FadeOut(m) for m in (same, law_box.frame, law, pushed, target2, point_mass, m_tag, force, lone_force,
                                      track, lone_track)], run_time=0.8)
    notes = VGroup(txt("same push, same centre motion", cfg.FONT["body"], cfg.WHITE),
                   txt("pushed at a different point: a different turn", cfg.FONT["body"], cfg.TORQUE)).arrange(DOWN, buff=0.32)
    fit_width(notes, 13.0)
    notes.move_to(UP * 3.0)
    lanes = (np.array([-4.2, 0.55, 0.0]), np.array([-4.2, -2.35, 0.0]))
    clock3 = Knob(0.0)
    views, targets, pushes = [], [], []
    for lane, bead_k in zip(lanes, (pm.SPRINGS.push_on, 3)):
        view = ClusterView(pm.spring_cluster_run(True, None, bead_k), lane, clock3, S_TEST)
        tgt = com_target(0.16)
        tgt.add_updater(lambda m, v=view: m.move_to(v.com()))
        push = VecArrow(lambda v=view, b=bead_k: v.positions()[b] - np.array([*pm.SPRINGS.force, 0]) * 1.1,
                        lambda v=view, b=bead_k: v.positions()[b], cfg.WARNING, width=0.1, tip_len=0.28)
        views.append(view)
        targets.append(tgt)
        pushes.append(push)
    in_step = DashedLine(UP, DOWN, stroke_color=cfg.WHITE, stroke_width=2.5, dash_length=0.12)
    in_step.add_updater(lambda m: m.put_start_and_end_on(views[0].com(), views[1].com()))
    in_step.update()
    scene.play(FadeIn(notes[0], shift=DOWN * 0.15), *[FadeIn(v) for v in views], *[FadeIn(g) for g in targets], run_time=1.0)
    scene.add(*pushes)
    scene.play(*[p.grow_in(run_time=0.6) for p in pushes], FadeIn(in_step), run_time=0.6)
    scene.play(clock3.to(views[0], 9.5, rate_func=linear), run_time=9.5)
    scene.play(FadeIn(notes[1]), run_time=0.9)
    finish(scene, t)
