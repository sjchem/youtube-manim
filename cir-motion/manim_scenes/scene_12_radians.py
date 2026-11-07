"""Scene 12 — angles and radians. A ruler measures distance on a line; on a
circle the radius sweeps an angle from a fixed direction. One radian is
built literally: a copy of the radius lifts onto the rim and bends along it.
Then theta = s / r, a full turn is 2 pi radians (six whole radii and a bit
laid round the rim), pi and pi / 2 marked, angular position vs angular
displacement, the counterclockwise-positive convention, and an accumulated
angle counter that reaches 2 pi after one lap although the particle faces
the same way it started.
"""

from manim_scenes.common import *

C = np.array([-3.5, -0.45, 0])
R = 2.3
COL = 3.6


class Scene12Radians(Scene):
    def construct(self) -> None:
        play_scene(self)


def bent_radius(bend: float, start: float = 0.0, length: float = 1.0, n: int = 40) -> np.ndarray:
    """A radius-long segment standing on the rim at angle ``start`` (bend 0), wrapped onto the rim (bend 1)."""
    u = np.linspace(0, length, n)
    base = C + R * np.array([np.cos(start), np.sin(start), 0])
    tangent = np.array([-np.sin(start), np.cos(start), 0])
    straight = base[None, :] + np.outer(u * R, tangent)
    arc = np.array([C + R * np.array([np.cos(start + a), np.sin(start + a), 0]) for a in u])
    return straight * (1 - bend) + arc * bend


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "12")
    chapter_open(scene, 4, "Angular motion")
    head = heading("Angles and radians")
    scene.play(FadeIn(head, shift=DOWN * 0.18), run_time=0.6)
    ruler = NumberLine(x_range=(0, 5, 1), length=5.0, color=cfg.MUTED, include_numbers=False).move_to([COL, 1.6, 0])
    walker = bead(ruler.n2p(0), cfg.BALL, 0.14)
    stretch = Knob(0.0)
    walker.add_updater(lambda m: m.move_to(ruler.n2p(stretch.value) + UP * 0.25))
    span = live(VMobject(), lambda: Line(ruler.n2p(0), ruler.n2p(max(stretch.value, 1e-3)), stroke_color=cfg.CYAN, stroke_width=7))
    dist = txt("distance", cfg.FONT["small"], cfg.CYAN).next_to(ruler, DOWN, buff=0.35)
    scene.play(FadeIn(ruler), FadeIn(walker), run_time=0.6)
    scene.add(span)
    scene.play(stretch.to(walker, 4.0, run_time=2.4), FadeIn(dist), run_time=2.4)

    # --- 2. On a circle: the angle swept from a fixed direction ---------------------------------------------------------------
    beat(scene, t, 1)
    view = CircleView(C, R, P)
    reference = dashed_path(C, C + RIGHT * (R + 0.6), cfg.MUTED, width=3, opacity=0.8)
    sweep = Knob(0.0)
    radius = live(VMobject(), lambda: Line(C, C + R * np.array([np.cos(sweep.value), np.sin(sweep.value), 0]),
                                           stroke_color=cfg.POSITION, stroke_width=5))
    angle = live(VMobject(), lambda: arc_mark(C, 0.65, 0.0, max(sweep.value, 1e-3), cfg.ANGLE))
    theta = eq(r"\theta", cfg.FONT["body"], cfg.ANGLE)
    theta.add_updater(lambda m: m.move_to(C + 1.05 * np.array([np.cos(sweep.value / 2), np.sin(sweep.value / 2), 0])))
    scene.play(FadeOut(head), FadeIn(view.ring), FadeIn(view.hub), Create(reference), run_time=0.8)
    scene.add(radius, angle, theta)
    scene.play(sweep.to(radius, 70 * DEGREES, run_time=2.4), FadeIn(theta), run_time=2.4)
    scene.wait(0.6)

    # --- 3. One radian: the radius laid along the rim ------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(sweep.to(radius, 0.0, run_time=1.0), FadeOut(VGroup(ruler, walker, span, dist)), run_time=1.0)
    for m in (theta, span, walker):
        m.clear_updaters()
    scene.remove(theta)
    lift, bend = Knob(0.0), Knob(0.0)
    copy = live(VMobject(), lambda: VMobject(stroke_color=cfg.POSITION, stroke_width=7).set_points_as_corners(
        list(bent_radius(bend.value) * lift.value + np.array([C + np.array([s * R, 0, 0]) for s in np.linspace(0, 1, 40)])
             * (1 - lift.value))))
    scene.add(copy)
    scene.play(lift.to(copy, 1.0, run_time=1.4), run_time=1.4)
    scene.play(bend.to(copy, 1.0, run_time=1.8), run_time=1.8)
    scene.play(sweep.to(radius, 1.0, run_time=1.0), run_time=1.0)
    one = eq(r"1\ \text{rad} \approx 57.3^\circ", cfg.FONT["section"], cfg.ANGLE).move_to([COL, 2.4, 0])
    scene.play(Write(one), run_time=1.2)

    # --- 4. theta = s / r --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    rule = eq([r"\theta", "=", r"\frac{s}{r}"], cfg.FONT["title"])
    paint(rule, {0: cfg.ANGLE, 2: cfg.CYAN}).move_to([COL, 0.6, 0])
    back = eq(r"s = r\,\theta", cfg.FONT["section"], cfg.CYAN).next_to(rule, DOWN, buff=0.5)
    scene.play(Write(rule), run_time=1.4)
    scene.play(FadeIn(back, shift=UP * 0.1), run_time=0.8)

    # --- 5. A full turn: 2 pi radians -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(one, rule, back)), FadeOut(copy), run_time=0.6)
    copy.clear_updaters()
    colors = [cfg.POSITION, cfg.CYAN]
    pieces = VGroup()
    for k in range(7):
        length = min(1.0, TAU - k)
        piece = VMobject(stroke_color=colors[k % 2], stroke_width=9).set_points_as_corners(list(bent_radius(1.0, k, length)))
        pieces.add(piece)
    scene.play(LaggedStart(*[Create(p) for p in pieces], lag_ratio=0.5), run_time=4.2)
    count = eq(r"2\pi \approx 6.28\ \text{radii}", cfg.FONT["body"], cfg.CYAN).move_to([COL, 2.0, 0])
    full = eq(r"360^\circ = 2\pi\ \text{rad}", cfg.FONT["section"], cfg.WHITE).next_to(count, DOWN, buff=0.5)
    scene.play(FadeIn(count), run_time=0.7)
    scene.play(Write(full), run_time=1.2)

    # --- 6. pi and pi / 2 --------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    more = VGroup(eq(r"180^\circ = \pi\ \text{rad}", cfg.FONT["body"]), eq(r"90^\circ = \tfrac{\pi}{2}\ \text{rad}", cfg.FONT["body"]))
    more.arrange(DOWN, buff=0.4).next_to(full, DOWN, buff=0.5)
    ticks = VGroup(*[Line(C + R * 0.88 * d, C + R * 1.12 * d, stroke_color=cfg.WHITE, stroke_width=4) for d in (UP, LEFT)])
    tick_tags = VGroup(eq(r"\tfrac{\pi}{2}", cfg.FONT["small"]).next_to(C + UP * R * 1.12, UP, buff=0.1),
                       eq(r"\pi", cfg.FONT["small"]).next_to(C + LEFT * R * 1.12, LEFT, buff=0.12))
    scene.play(FadeIn(more[0]), Create(ticks[1]), FadeIn(tick_tags[1]), run_time=0.9)
    scene.play(FadeIn(more[1]), Create(ticks[0]), FadeIn(tick_tags[0]), run_time=0.9)

    # --- 7. Radians tie angle to distance: s = r theta ---------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(count, full, more)), FadeOut(pieces), run_time=0.6)
    tie = eq([r"s", "=", r"r", r"\theta"], cfg.FONT["hero"])
    paint(tie, {0: cfg.CYAN, 2: cfg.POSITION, 3: cfg.ANGLE}).move_to([COL, 1.0, 0])
    framed = boxed(tie, cfg.RESULT, buff=0.3)
    scene.play(Write(tie), run_time=1.2)
    scene.play(FadeIn(framed[0]), sweep.to(radius, 2.2, run_time=1.6), run_time=1.6)

    # --- 8. Angular position vs angular displacement -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(tie, framed[0])), sweep.to(radius, 0.5, run_time=0.8), run_time=0.8)
    initial = Line(C, C + R * np.array([np.cos(0.5), np.sin(0.5), 0]), stroke_color=cfg.MUTED, stroke_width=4)
    theta_i = eq(r"\theta_i", cfg.FONT["small"], cfg.MUTED).move_to(C + (R + 0.4) * np.array([np.cos(0.5), np.sin(0.5), 0]))
    scene.add(initial)
    scene.play(FadeIn(theta_i), run_time=0.5)
    angle.clear_updaters()
    change = live(VMobject(), lambda: arc_mark(C, 0.95, 0.5, max(sweep.value, 0.501), cfg.ANGLE, 6))
    scene.remove(angle)
    scene.add(change)
    scene.play(sweep.to(radius, 2.0, run_time=1.6), run_time=1.6)
    theta_f = eq(r"\theta_f", cfg.FONT["small"], cfg.POSITION).move_to(C + (R + 0.4) * np.array([np.cos(2.0), np.sin(2.0), 0]))
    displacement = paint(eq([r"\Delta\theta", "=", r"\theta_f - \theta_i"], cfg.FONT["section"]), {0: cfg.ANGLE}).move_to([COL, 1.6, 0])
    scene.play(FadeIn(theta_f), Write(displacement), run_time=1.4)

    # --- 9. Counterclockwise positive, clockwise negative -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    signs = VGroup(VGroup(txt("counterclockwise", cfg.FONT["small"], cfg.ANGLE), eq(r"\Delta\theta > 0", cfg.FONT["body"], cfg.ANGLE)).arrange(RIGHT, buff=0.35),
                   VGroup(txt("clockwise", cfg.FONT["small"], cfg.ROSE), eq(r"\Delta\theta < 0", cfg.FONT["body"], cfg.ROSE)).arrange(RIGHT, buff=0.35))
    signs.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(displacement, DOWN, buff=0.6)
    ccw = CurvedArrow(C + R * 1.25 * np.array([np.cos(-0.4), np.sin(-0.4), 0]), C + R * 1.25 * np.array([np.cos(0.3), np.sin(0.3), 0]),
                      angle=0.6, color=cfg.ANGLE, stroke_width=5)
    cw = CurvedArrow(C + R * 1.25 * np.array([np.cos(3.5), np.sin(3.5), 0]), C + R * 1.25 * np.array([np.cos(2.8), np.sin(2.8), 0]),
                     angle=-0.6, color=cfg.ROSE, stroke_width=5)
    scene.play(FadeIn(signs[0]), Create(ccw), run_time=0.8)
    scene.play(FadeIn(signs[1]), Create(cw), run_time=0.8)

    # --- 10. One lap: an angular displacement of 2 pi ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    change.clear_updaters()
    scene.play(FadeOut(VGroup(signs, ccw, cw, initial, theta_i, theta_f, change, displacement, radius, reference,
                              ticks, tick_tags)), run_time=0.7)
    radius.clear_updaters()
    lap = CircleView(C, R, P, phase=0.0)
    r_arrow = lap.arrow("r", width=0.08)
    scene.add(lap.ball, r_arrow)
    scene.play(FadeIn(lap.ball), r_arrow.grow_in(run_time=0.6), run_time=0.6)
    swept = live(VMobject(), lambda: arc_mark(C, 0.7, 0.0, max(lap.theta(), 1e-3), cfg.ANGLE, 6) if lap.theta() < TAU - 1e-3
                 else Circle(radius=0.7, stroke_color=cfg.ANGLE, stroke_width=6).move_to(C))
    readout = number_line(lambda: lap.theta(), 2, "rad", cfg.ANGLE, 60, "Δθ")
    readout.move_to([COL, 1.4, 0])
    scene.add(swept)
    scene.play(FadeIn(readout), run_time=0.5)
    scene.play(lap.run(P.period, 9.0), run_time=9.0)
    readout.clear_updaters()
    two_pi = eq(r"= 2\pi", cfg.FONT["section"], cfg.ANGLE).next_to(readout, DOWN, buff=0.4)
    same_way = txt("same way it started", cfg.FONT["small"], cfg.WHITE).next_to(two_pi, DOWN, buff=0.35)
    scene.play(FadeIn(two_pi), run_time=0.7)
    scene.play(FadeIn(same_way), Indicate(r_arrow, color=cfg.POSITION, scale_factor=1.05), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
