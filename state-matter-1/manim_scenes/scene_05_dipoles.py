"""Scene 05 — permanent dipoles. A 3D hydrogen chloride molecule: chlorine
pulls the shared electrons (a soft cloud gathers on Cl), leaving delta-minus
on Cl and delta-plus on H. Two molecules take three poses, and a live meter
reads the dipole-dipole energy from ``physics_models.dipole_energy``: head to
tail -2, side by side antiparallel -1, head to head +2 (units of
mu^2 / 4 pi eps0 r^3). Then they tumble through a seeded Metropolis walk
(``tumbling_dipoles``): the plain average of all orientations is zero, but the
running mean of the thermally sampled energy settles below zero — the Keesom
attraction, measured — and it falls as -1/r^6.
"""

from manim_scenes.common import *

SEP = 1.7                      # half the distance between the molecules (stage units)
H_ARM, CL_ARM = 0.5, 0.36       # atom distances from the molecule's centre, along the dipole


class Scene05Dipoles(Scene):
    def construct(self) -> None:
        play_scene(self)


class HCl:
    """One hydrogen chloride on a stage. ``m`` is the dipole direction (from the
    delta-minus Cl toward the delta-plus H); tween it with ``aim``."""

    def __init__(self, stage: Stage, centre, m=(1.0, 0.0, 0.0)) -> None:
        self.stage, self.c, self.m = stage, np.asarray(centre, dtype=float), mu.unit(m)
        self.h = Ball(lambda: self.c + self.m * H_ARM, 0.2, cfg.ATOM["H"], label="H")
        self.cl = Ball(lambda: self.c - self.m * CL_ARM, 0.4, cfg.ATOM["Cl"], label="Cl")
        self.rod = Rod(self.h, self.cl, width=15)
        self.cloud = Halo(self.cl, cfg.CLOUD, reach=1.9, peak=0.22)
        self.cloud.presence = 0.0
        # Labels sit beyond each atom along the molecule's own axis, so they never cross the bond.
        self.minus = Tag(txt("δ−", 34, cfg.DELTA_MINUS), lambda: self.c - self.m * (CL_ARM + 0.68))
        self.plus = Tag(txt("δ+", 34, cfg.DELTA_PLUS), lambda: self.c + self.m * (H_ARM + 0.5))
        for tag in (self.minus, self.plus):
            tag.presence = 0.0
        self.parts = [self.rod, self.h, self.cl]
        stage.add_body(self.cloud, *self.parts)
        stage.add_overlay(self.minus, self.plus)

    def aim(self, direction, **kwargs) -> Param:
        return Param(self.stage, lambda: self.m, lambda v: setattr(self, "m", mu.unit(v)), mu.unit(direction),
                     mode="direction", **kwargs)


class EnergyMeter(VGroup):
    """A vertical bar from zero: green and downward when attractive, red and upward when repulsive."""

    def __init__(self, value: Callable[[], float], at, *, unit: float = 0.75, span: float = 2.2) -> None:
        super().__init__()
        self.value, self.unit = value, unit
        self.zero = Line(LEFT * 0.7, RIGHT * 0.7, stroke_color=cfg.WHITE, stroke_width=3).move_to(at)
        rail = Line(UP * span, DOWN * span, stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5).move_to(at)
        self.bar = Rectangle(width=0.7, height=0.1, stroke_width=0, fill_opacity=0.9)
        self.symbol = eq("U", cfg.FONT["label"], cfg.WHITE).next_to(rail, UP, buff=0.15)
        self.attract = txt("attract", cfg.FONT["tiny"], cfg.ATTRACT).next_to(rail, DOWN, buff=0.15)
        self.repel = txt("repel", cfg.FONT["tiny"], cfg.REPEL).next_to(self.symbol, RIGHT, buff=0.35)
        self.add(rail, self.bar, self.zero, self.symbol, self.attract, self.repel)
        self.bar.add_updater(lambda m: self._fit())
        self._fit()

    def _fit(self) -> None:
        u = float(self.value())
        h = max(abs(u) * self.unit, 0.03)
        self.bar.stretch_to_fit_height(h)
        self.bar.move_to(self.zero.get_center() + UP * (np.sign(u) * h / 2))
        self.bar.set_fill(cfg.REPEL if u > 0 else cfg.ATTRACT)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Permanent dipoles")
    stage = Stage((-1.2, -0.3, 0), zoom=1.55, yaw=0.0, pitch=0.22, sway=0.035)
    one = HCl(stage, (0.0, 0.0, 0.0))
    show(scene, stage, 1.0)
    pulls = txt("Cl pulls the shared electrons", cfg.FONT["label"], cfg.WHITE).move_to([3.6, 2.4, 0])
    fit_width(pulls, 7.2)
    scene.play(FadeIn(pulls), stage.fade(one.cloud, 1.0), run_time=1.4)
    scene.play(*stage.turn(yaw=0.5), run_time=4.0)

    # --- 2. A permanent dipole --------------------------------------------------------------------------------------
    beat(scene, t, 1)
    permanent = result_label("permanent dipole", cfg.GOLD, cfg.FONT["section"]).move_to([3.6, 2.4, 0])
    scene.play(fade_through(pulls, permanent), stage.fade(one.minus, 1.0), stage.fade(one.plus, 1.0), run_time=1.2)
    scene.play(*stage.turn(yaw=0.0), run_time=3.0)

    # --- 3. Two molecules: orientation matters --------------------------------------------------------------------------
    beat(scene, t, 2)
    sep = np.array([1.0, 0.0, 0.0])
    two = HCl(stage, (SEP, 0.0, 0.0))
    meter = EnergyMeter(lambda: pm.dipole_energy(one.m, two.m, sep), [5.6, -0.3, 0])
    for p in (*two.parts, two.minus, two.plus):
        p.presence = 0.0
    scene.play(FadeOut(permanent), Param(stage, lambda: one.c, lambda v: setattr(one, "c", np.asarray(v)), np.array([-SEP, 0, 0]),
                                         mode="vector"), stage.fade(one.cloud, 0.0), run_time=1.2)
    scene.play(*[stage.fade(p, 1.0) for p in (*two.parts, two.minus, two.plus)], FadeIn(meter), run_time=1.0)

    # --- 4. Head to tail: attract ------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    pose_name = txt("head to tail", cfg.FONT["label"], cfg.ATTRACT).move_to([-1.2, 2.7, 0])
    scene.play(FadeIn(pose_name), run_time=0.6)
    scene.play(Indicate(meter.bar, color=cfg.ATTRACT), run_time=1.2)

    # --- 5. Side by side, opposite: attract, more weakly ---------------------------------------------------------------------
    beat(scene, t, 4)
    side = txt("side by side, opposite", cfg.FONT["label"], cfg.ATTRACT).move_to([-1.2, 2.7, 0])
    scene.play(one.aim((0, 1, 0)), two.aim((0, -1, 0)), fade_through(pose_name, side), run_time=1.6)
    scene.wait(1.5)

    # --- 6. Head to head: repel -----------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    clash = txt("head to head", cfg.FONT["label"], cfg.REPEL).move_to([-1.2, 2.7, 0])
    scene.play(one.aim((1, 0, 0)), two.aim((-1, 0, 0)), fade_through(side, clash), run_time=1.6)
    scene.play(Indicate(meter.bar, color=cfg.REPEL), run_time=1.2)

    # --- 7. Fixed orientations: U ~ 1/r^3, sign set by angles; an energy, not a force -------------------------------------
    beat(scene, t, 6)
    law = eq(r"U \propto \frac{1}{r^3}", cfg.FONT["section"], cfg.WHITE).move_to([-4.0, 2.75, 0])
    note = VGroup(txt("sign depends on the angles", cfg.FONT["small"], cfg.GOLD),
                  txt("an energy, not a force", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.22)
    note.next_to(law, DOWN, buff=0.35)
    tags = (one.minus, one.plus, two.minus, two.plus)       # introduced already; keep the law's notes clear of them
    scene.play(FadeOut(clash), Write(law), *[stage.fade(tag, 0.0) for tag in tags], run_time=1.2)
    scene.play(FadeIn(note[0]), one.aim((1, 0, 0)), two.aim((1, 0, 0)), run_time=1.6)
    scene.play(FadeIn(note[1]), one.aim((0, 1, 0)), two.aim((0, 1, 0)), run_time=1.6)
    scene.play(one.aim((1, 0, 0)), two.aim((-1, 0, 0)), run_time=1.6)

    # --- 8. Tumbling: equally likely orientations would cancel ----------------------------------------------------------------
    beat(scene, t, 7)
    m1s, m2s, energies = pm.tumbling_dipoles()
    frame = Knob(0.0)
    count = len(energies)

    def sample(series: np.ndarray) -> np.ndarray:
        k = float(np.clip(frame.value, 0, count - 1.001))
        i = int(k)
        return series[i] * (1 - (k - i)) + series[i + 1] * (k - i)

    one.m, two.m = mu.unit(m1s[0]), mu.unit(m2s[0])
    stage.add_updater(lambda m: (setattr(one, "m", mu.unit(sample(m1s))), setattr(two, "m", mu.unit(sample(m2s)))), index=0)
    axes = plot_axes((0, count), (-0.5, 0.5), x_length=6.0, y_length=4.0, at=[3.4, -0.6, 0], x_label=r"\text{time}",
                     y_label=r"\langle U \rangle", y_color=cfg.ATTRACT)
    zero = DashedLine(axes.c2p(0, 0), axes.c2p(count, 0), stroke_color=cfg.WHITE, stroke_width=2.5, dash_length=0.14)
    equal = txt("all orientations equal: 0", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.c2p(count * 0.60, 0), UP, buff=0.36)
    # Keep the zero-reference label readable as the faint instantaneous trace passes.
    equal.add_background_rectangle(color=cfg.BG, opacity=0.96, buff=0.08)
    equal.set_z_index(5)
    running = np.cumsum(energies) / np.arange(1, count + 1)

    def trace() -> VMobject:
        k = int(np.clip(frame.value, 2, count - 1))
        step = max(1, k // 160)
        return polyline([axes.c2p(i, running[i]) for i in range(0, k, step)] + [axes.c2p(k, running[k])], cfg.ATTRACT, 6)

    def raw() -> VMobject:
        k = int(np.clip(frame.value, 2, count - 1))
        lo = max(0, k - 140)
        return polyline([axes.c2p(i, energies[i]) for i in range(lo, k)], cfg.MUTED, 2, 0.45)

    mean_line = live(VMobject(), trace)
    jitter = live(VMobject(), raw)
    scene.play(FadeOut(VGroup(law, note, meter)), stage.glide([-4.0, -0.3, 0]), stage.zoom_to(1.15),
               *[stage.fade(tag, 0.0) for tag in (one.minus, one.plus, two.minus, two.plus)],
               *stage.turn(pitch=0.45), run_time=1.2)
    scene.play(Create(axes), Create(zero), FadeIn(equal), run_time=1.2)
    scene.add(jitter)
    scene.play(frame.to(stage, 220, run_time=5.5, rate_func=linear), run_time=5.5)

    # --- 9. Attractive poses are visited more: the average is attractive -----------------------------------------------------
    beat(scene, t, 8)
    measured = txt("thermal average", cfg.FONT["small"], cfg.ATTRACT).move_to([3.0, 2.25, 0])
    scene.add(mean_line)
    scene.play(FadeIn(measured), frame.to(stage, 520, run_time=6.0, rate_func=linear), run_time=6.0)
    scene.play(frame.to(stage, 680, run_time=4.0, rate_func=linear), run_time=4.0)

    # --- 10. And it falls as -1/r^6 ---------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    keesom = boxed(eq(r"\langle U \rangle \propto -\frac{1}{r^6}", cfg.FONT["body"], cfg.ATTRACT), cfg.ATTRACT)
    keesom.move_to([3.6, 2.6, 0])
    scene.play(fade_through(measured, keesom), frame.to(stage, 760, run_time=1.4, rate_func=linear), run_time=1.4)
    scene.play(frame.to(stage, count - 1, run_time=6.0, rate_func=linear), run_time=6.0)
    finish(scene, t, stage)
