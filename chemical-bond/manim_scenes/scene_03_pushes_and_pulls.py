"""Pushes and pulls: every attraction and repulsion inside two hydrogen atoms.

Electrons start as single glowing beads (a snapshot of where each electron
might be) so the six pairwise interactions can be drawn as lines: four
teal attractions (each electron to each nucleus) and two red repulsions.
Line opacity falls with distance, so interactions between far-apart atoms
fade on their own. When the beads' paths begin to cover both nuclei, the
picture hands over to the shared cloud of chapter 01. The "squeeze" beat
shows confinement raising an electron's energy — the quantum ingredient —
as a meter, not as a computed value.
"""

from manim_scenes.common import *

ROW_Y = 0.45
RADIUS = 1.65


class Scene03PushesAndPulls(Scene):
    def construct(self) -> None:
        play_scene(self)


def wanderer(home: Callable[[], np.ndarray], other: Callable[[], np.ndarray], mix: ValueTracker, phase: float,
             radius: float = RADIUS) -> VGroup:
    """One electron bead: circling its own nucleus, or (mix -> 1) roaming over both."""
    dot = glow_dot(home(), 0.16)
    dot.clock = phase

    def where(clock: float) -> np.ndarray:
        h, o = home(), other()
        own = h + radius * 0.55 * np.array([np.cos(1.7 * clock), 0.8 * np.sin(2.3 * clock), 0])
        mid, half = (h + o) / 2, abs(o[0] - h[0]) / 2
        shared = mid + np.array([(half + 0.45 * radius) * np.cos(1.1 * clock), 0.55 * radius * np.sin(2.2 * clock), 0])
        m = smooth(float(np.clip(mix.get_value(), 0, 1)))
        return own + (shared - own) * m

    def step(m: Mobject, dt: float) -> None:
        m.clock += dt
        m.move_to(where(m.clock))

    dot.add_updater(step)
    return dot


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "03", "Pushes and pulls")

    # --- 1. Two protons, two electrons --------------------------------------------------------------
    gap, mix = ValueTracker(7.2), ValueTracker(0.0)
    centre = np.array([0.0, ROW_Y, 0.0])

    def left() -> np.ndarray:
        return centre + LEFT * gap.get_value() / 2

    def right() -> np.ndarray:
        return centre + RIGHT * gap.get_value() / 2

    cloud = bind_pair(PairCloud(LEFT, RIGHT, RADIUS, count=700, seed=31, glow=0.12, dot_radius=0.034), gap.get_value, centre)
    cloud.set_level(0.28)
    scene.add(cloud)
    nuclei = pair_nuclei(cloud, ("+", "+"), radius=0.34)
    e1 = wanderer(left, right, mix, 0.0)
    e2 = wanderer(right, left, mix, 2.1)
    scene.play(FadeIn(cloud), FadeIn(nuclei, scale=0.6), run_time=1.0)
    scene.play(FadeIn(e1, scale=0.5), FadeIn(e2, scale=0.5), run_time=0.8)
    snapshot = txt("Position samples · no orbits", cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.75, 0])
    scene.play(FadeIn(snapshot), run_time=0.6)
    dismiss_opening_title(scene, t, head)

    # --- 2. Opposite charges attract: four pulls ---------------------------------------------------------
    beat(scene, t, 1)

    def fades(d: float) -> float:
        return float(np.clip(3.2 / max(d, 0.1), 0.1, 1.0))

    pulls = VGroup(
        force_line(e1.get_center, left, cfg.ATTRACT, width=7, strength=fades),
        force_line(e1.get_center, right, cfg.ATTRACT, width=7, strength=fades),
        force_line(e2.get_center, right, cfg.ATTRACT, width=7, strength=fades),
        force_line(e2.get_center, left, cfg.ATTRACT, width=7, strength=fades),
    )
    legend = VGroup(
        VGroup(Line(LEFT * 0.35, RIGHT * 0.35, stroke_color=cfg.ATTRACT, stroke_width=6),
               txt("attraction", cfg.FONT["label"], cfg.ATTRACT)).arrange(RIGHT, buff=0.22),
        VGroup(DashedLine(LEFT * 0.35, RIGHT * 0.35, stroke_color=cfg.REPEL, stroke_width=6, dash_length=0.12),
               txt("repulsion", cfg.FONT["label"], cfg.REPEL)).arrange(RIGHT, buff=0.22),
    ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-5.0, 3.05, 0])
    scene.play(FadeIn(legend[0]), run_time=0.5)
    scene.play(LaggedStart(*[Create(line) for line in pulls], lag_ratio=0.3), run_time=1.8)
    both = txt("Each electron, both nuclei", cfg.FONT["label"], cfg.ATTRACT).move_to([0, -2.5, 0])
    scene.play(FadeIn(both, shift=UP * 0.1), run_time=0.7)

    # --- 3. Like charges repel: two pushes -----------------------------------------------------------------
    beat(scene, t, 2)
    pushes = VGroup(
        force_line(left, right, cfg.REPEL, width=7, dashed=True, buff=0.4, strength=fades),
        force_line(e1.get_center, e2.get_center, cfg.REPEL, width=7, dashed=True, strength=fades),
    )
    scene.play(FadeIn(legend[1]), FadeOut(both), run_time=0.5)
    scene.play(Create(pushes[0]), run_time=0.9)
    scene.play(Create(pushes[1]), run_time=0.9)
    six = txt("Six interactions", cfg.FONT["label"], cfg.WHITE).move_to([0, -2.5, 0])
    scene.play(FadeIn(six, shift=UP * 0.1), run_time=0.7)

    # --- 4. Far apart: each atom keeps to itself -------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(six), track(gap, 11.2), run_time=2.4)
    alone = txt("Far apart: weak interaction", cfg.FONT["label"], cfg.MUTED).move_to([0, -2.5, 0])
    scene.play(FadeIn(alone, shift=UP * 0.1), run_time=0.7)
    scene.play(track(gap, 11.6), run_time=1.6, rate_func=there_and_back)

    # --- 5. Closer: Shared electron density -----------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(alone), track(gap, 3.6), run_time=2.6)
    scene.play(track(mix, 1.0), run_time=2.6)
    roam = txt('Shared electron density', cfg.FONT["label"], cfg.CYAN).move_to([0, -2.5, 0])
    scene.play(FadeIn(roam, shift=UP * 0.1), run_time=0.7)

    # --- 6. Density gathers between the nuclei -----------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(roam), FadeOut(snapshot), cloud.share_to(1.0), cloud.fade_to(1.0),
               *[line_gain(l, 0.0) for l in (*pulls, pushes[1])], e1.animate.set_opacity(0), e2.animate.set_opacity(0),
               track(gap, 2.8), run_time=2.4)
    for mob in (e1, e2, *pulls, pushes[1]):
        mob.clear_updaters()
    scene.remove(e1, e2, *pulls, pushes[1])

    def inward(index: int) -> VMobject:
        arrow = Arrow(ORIGIN, RIGHT, buff=0, color=cfg.ATTRACT, stroke_width=10, max_tip_length_to_length_ratio=0.3)

        def follow_nucleus(m: Mobject) -> None:
            nucleus = cloud.ends[index].get_center()
            towards = 1 if index == 0 else -1
            m.put_start_and_end_on(nucleus + LEFT * towards * 1.9, nucleus + LEFT * towards * 0.5)

        arrow.add_updater(follow_nucleus)
        follow_nucleus(arrow)
        return arrow

    hugs = VGroup(inward(0), inward(1))
    scene.play(GrowArrow(hugs[0]), GrowArrow(hugs[1]), run_time=0.9)
    shared = txt("Attraction draws nuclei together", cfg.FONT["label"], cfg.ATTRACT).move_to([0, -2.5, 0])
    scene.play(FadeIn(shared, shift=UP * 0.1), run_time=0.7)

    # --- 7. Too close: the push wins --------------------------------------------------------------------------
    beat(scene, t, 6)
    pushes[0].clear_updaters()
    scene.remove(pushes[0])
    wall = force_line(left, right, cfg.REPEL, width=5, dashed=False, buff=0.3,
                      thickness=lambda d: float(np.clip(18 / max(d, 0.4), 4, 22)))
    scene.add(wall)
    scene.play(FadeOut(shared), FadeOut(hugs), track(gap, 1.05), run_time=2.4, rate_func=rush_into)

    def outward(index: int) -> VMobject:
        arrow = Arrow(ORIGIN, RIGHT, buff=0, color=cfg.REPEL, stroke_width=11, max_tip_length_to_length_ratio=0.3)

        def follow_nucleus(m: Mobject) -> None:
            nucleus = cloud.ends[index].get_center()
            away = -1 if index == 0 else 1
            m.put_start_and_end_on(nucleus + RIGHT * away * 0.45 + UP * 0.95, nucleus + RIGHT * away * 2.3 + UP * 0.95)

        arrow.add_updater(follow_nucleus)
        follow_nucleus(arrow)
        return arrow

    shoves = VGroup(outward(0), outward(1))
    scene.play(GrowArrow(shoves[0]), GrowArrow(shoves[1]), run_time=0.8)
    wins = txt("Too close: repulsion wins", cfg.FONT["label"], cfg.REPEL).move_to([0, -2.5, 0])
    scene.play(FadeIn(wins, shift=UP * 0.1), Wiggle(shoves, scale_value=1.1), run_time=1.2)

    # --- 8. The quantum twist: squeezing an electron costs energy -------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(wins, shoves)), line_gain(wall, 0.0), track(gap, 2.8), run_time=1.0)
    wall.clear_updaters()
    scene.remove(wall)
    meter_box = RoundedRectangle(width=0.62, height=3.4, corner_radius=0.14, stroke_color=cfg.MUTED, stroke_width=3,
                                 fill_color=cfg.PANEL, fill_opacity=0.9).move_to([5.6, ROW_Y - 0.1, 0])
    level = ValueTracker(0.25)
    fill = Rectangle(width=0.46, height=0.1, stroke_width=0, fill_color=cfg.ENERGY, fill_opacity=0.95)

    def refill(m: Mobject) -> None:
        h = max(3.24 * level.get_value(), 0.02)
        m.stretch_to_fit_height(h).move_to(meter_box.get_bottom() + UP * (0.08 + h / 2))

    fill.add_updater(refill)
    refill(fill)
    meter_label = txt("energy", cfg.FONT["small"], cfg.ENERGY).next_to(meter_box, UP, buff=0.2)
    scene.play(FadeIn(meter_box), FadeIn(fill), FadeIn(meter_label), run_time=0.7)
    squeeze = VGroup(glow_arrow([-4.0, ROW_Y, 0], [-2.4, ROW_Y, 0], cfg.PURPLE, 7),
                     glow_arrow([4.0, ROW_Y, 0], [2.4, ROW_Y, 0], cfg.PURPLE, 7))
    scene.play(*[GrowArrow(s.arrow) for s in squeeze], FadeIn(VGroup(*[s[0] for s in squeeze])), run_time=0.7)
    scene.play(cloud.resize_to(0.7), track(gap, 2.0), track(level, 0.9), run_time=2.0)
    quantum = txt("Confinement costs energy", cfg.FONT["label"], cfg.PURPLE).move_to([0, -2.5, 0])
    scene.play(FadeIn(quantum, shift=UP * 0.1), run_time=0.7)
    scene.play(cloud.resize_to(RADIUS), track(gap, 2.8), track(level, 0.35), FadeOut(squeeze), run_time=1.6)

    # --- 9. Track one number: the total energy -----------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(quantum, legend, meter_box, meter_label)), fill.animate.set_opacity(0), run_time=0.7)
    fill.clear_updaters()
    scene.remove(fill)
    scene.play(track(gap, 5.0), cloud.share_to(0.35), run_time=1.4)
    total = eq(r"E_{\text{total}}", 96, cfg.ENERGY).move_to([0, -2.3, 0])
    glow = decorative(total.copy().set_stroke(cfg.ENERGY, width=16, opacity=0.18))
    scene.play(Write(total), FadeIn(glow), run_time=1.2)
    one_number = txt("Energy of the whole system", cfg.FONT["label"], cfg.WHITE).next_to(total, DOWN, buff=0.3)
    scene.play(FadeIn(one_number, shift=UP * 0.1), run_time=0.7)
    scene.play(Circumscribe(total, color=cfg.ENERGY, fade_out=True), run_time=1.4)
    of_r = eq(r"E(r)", 96, cfg.ENERGY).move_to(total)
    distance = txt("Energy versus distance", cfg.FONT["label"], cfg.WHITE).move_to(one_number)
    scene.play(FadeThrough(total, of_r), FadeOut(glow), FadeThrough(one_number, distance), run_time=1.2)
    scene.play(track(gap, 3.2), run_time=1.6)
    scene.play(track(gap, 5.0), run_time=1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
