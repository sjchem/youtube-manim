"""Scene 28 — the race down the ramp. A 3D ramp at 30 degrees, 3 m long.
A solid cylinder and a thin copper ring (same mass, same radius) wait at the
top in two lanes. A 3-2-1 countdown for the viewer's prediction, then the
race in slow motion: each body's distance along the slope is 1/2 a t^2 with
a = g sin(beta) / (1 + I / M R^2) from ``physics_models.INCLINE``, and each
spins at s / R (rolling without slipping). The cylinder wins. Energy shares,
the acceleration law and the numbers (3.27 vs 2.45 m/s^2) follow. Then the
race is re-run with a frictionless sliding block in a middle lane: it wins
at g sin(beta) = 4.9 m/s^2. The near-lane cylinder and far-lane ring
have unique turning markers; the ramp and finish line draw behind the racers.
The ramp moves left for the energy and acceleration explanations; the final
race freezes when the sliding block reaches the finish.
"""

from manim_scenes.common import *

INC = pm.INCLINE
S = 2.0                                  # screen units per metre along the slope
R = 0.42
BETA = np.radians(INC.beta_deg)
DOWN_SLOPE = np.array([np.cos(BETA), -np.sin(BETA), 0.0])
NORMAL = np.array([np.sin(BETA), np.cos(BETA), 0.0])
TOP = np.array([-3.0, INC.length * S * np.sin(BETA), 0.0])
LANES = {"cylinder": 1.55, "block": 0.0, "ring": -1.55}
RAMP_HALF_WIDTH = 2.2
# Every racer lies above the ramp; whole-object depth sorting must not hide a far lane.
RAMP_BIAS, GUIDE_BIAS, FINISH_BIAS = -100.0, -60.0, -50.0
SLOW = INC.time(1.0) / 4.0               # physics seconds per film second


def distance_at(coefficient: float, seconds: float) -> float:
    """Distance along the ramp, stopped at the finish line (stage units)."""
    elapsed = float(np.clip(seconds, 0.0, INC.time(coefficient)))
    return 0.5 * INC.accel(coefficient) * elapsed * elapsed * S


def race_centre(coefficient: float, seconds: float, lane: float, lift: float = R) -> np.ndarray:
    return TOP + DOWN_SLOPE * distance_at(coefficient, seconds) + NORMAL * lift + np.array([0.0, 0.0, lane])


def rolling_spin(coefficient: float, seconds: float) -> float:
    """Clockwise spin paired with downhill translation: omega = -v / R."""
    return -distance_at(coefficient, seconds) / R


class Scene28Race(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "28", "The race down the ramp")
    stage = Stage((0.0, -2.35, 0.0), zoom=1.05, yaw=-0.5, pitch=0.28, sway=0.015)
    floor(stage, 0.0, reach=7.5, opacity=0.2)
    clock = Knob(0.0)

    def centre(c: float, lane: float, lift: float) -> np.ndarray:
        return race_centre(c, clock.value, lane, lift)

    bottom = TOP + DOWN_SLOPE * INC.length * S
    ramp_v, ramp_f = prism([[TOP[0] - 0.4, 0.0], [bottom[0], 0.0], [TOP[0], TOP[1]]], RAMP_HALF_WIDTH)
    ramp = Solid(ramp_v, ramp_f, "#3A5068", bias=RAMP_BIAS)
    finish_line = Segment(bottom + np.array([0, 0.02, -RAMP_HALF_WIDTH]), bottom + np.array([0, 0.02, RAMP_HALF_WIDTH]), cfg.GOLD, width=5, opacity=1.0)
    finish_line.bias = FINISH_BIAS
    lanes = [Segment(TOP + NORMAL * 0.015 + np.array([0.0, 0.0, lane]),
                     bottom + NORMAL * 0.015 + np.array([0.0, 0.0, lane]),
                     cfg.MUTED, width=1.8, opacity=0.35, dashed=True) for lane in LANES.values()]
    for guide in lanes:
        guide.bias = GUIDE_BIAS
    c_cyl, c_ring = float(pm.shape("cylinder").coefficient), float(pm.shape("ring").coefficient)
    cyl = Drum(lambda: centre(c_cyl, LANES["cylinder"], R), R, 0.32, cfg.DISC_BODY, spin=lambda: rolling_spin(c_cyl, clock.value),
               stripe=cfg.DISC_STRIPE, sectors=6)
    ring = Hoop(lambda: centre(c_ring, LANES["ring"], R), R, cfg.RING_BODY, spin=lambda: rolling_spin(c_ring, clock.value), width=14)
    block = Block(lambda: centre(0.0, LANES["block"], 0.3), (0.6, 0.6, 0.6), "#C98A4B", pose=lambda: mu.rotation_z(-BETA))
    block.presence = 0.0
    stage.add_body(ramp, *lanes, finish_line, cyl, ring, block)
    cyl_marker = rim_marker(stage, cyl, np.pi / 2, cfg.GOLD, fraction=0.82, radius=0.055)
    ring_marker = Ball(lambda: ring.point(np.pi / 2) + np.array([0.0, 0.0, 0.03]), 0.045, cfg.GOLD, layers=10)
    ring_marker.bias = 50.0
    stage.add_body(ring_marker)
    show(scene, stage, 1.0)
    names = [Tag(txt("solid cylinder", cfg.FONT["small"], cfg.DISC_STRIPE), lambda: centre(c_cyl, LANES["cylinder"], R), UP * 0.85 + LEFT * 0.8),
             Tag(txt("thin ring", cfg.FONT["small"], cfg.RING_BODY), lambda: centre(c_ring, LANES["ring"], R), UP * 0.85 + RIGHT * 0.8)]
    angle_tag = Tag(eq(rf"\beta = {fx(INC.beta_deg)}^\circ", cfg.FONT["body"], cfg.ANGLE),
                    TOP + DOWN_SLOPE * (INC.length * S * 0.35) + np.array([0.0, -0.95, RAMP_HALF_WIDTH + 0.02]),
                    DOWN * 0.1 + LEFT * 0.25)
    hidden(*names, angle_tag)
    stage.add_overlay(*names, angle_tag)
    scene.play(*[stage.fade(n, 1.0) for n in names], stage.fade(angle_tag, 1.0), run_time=0.9)
    same = caption("same M · same R · rolling without slipping", cfg.WHITE, cfg.FONT["small"])
    scene.play(FadeIn(same), run_time=0.6)
    which = result_label("which reaches the bottom first?", cfg.WHITE, cfg.FONT["body"]).move_to(UP * 3.1)
    scene.play(FadeIn(which), run_time=0.8)

    # --- 2. Predict --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(same), run_time=0.3)
    countdown(scene, [5.6, 1.8, 0], 3)

    # --- 3. The race ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    slow = chip("slow motion", cfg.MUTED, cfg.FONT["tiny"]).move_to([-6.1, 3.3, 0])
    scene.play(FadeIn(slow), *[stage.fade(n, 0.0) for n in names], run_time=0.3)
    scene.play(clock.to(stage, INC.time(c_cyl), rate_func=linear), run_time=INC.time(c_cyl) / SLOW)

    # --- 4. The cylinder wins ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    win = result_label("the cylinder wins", cfg.RESULT, cfg.FONT["section"])
    scene.play(fade_through(which, win.move_to(UP * 3.1)), run_time=0.8)
    # First show the cylinder at the line with the ring still uphill, then let the ring finish.
    scene.play(clock.to(stage, INC.time(c_ring), rate_func=linear),
               run_time=(INC.time(c_ring) - INC.time(c_cyl)) / SLOW)

    # --- 5. Energy shares --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(stage.glide((-3.65, -1.9, 0.0)), stage.zoom_to(0.82), run_time=1.0)
    shares = VGroup(eq(rf"\text{{ring: }} {share_tex('ring')}\ \text{{of }}K\ \text{{spinning}}", cfg.FONT["body"], cfg.RING_BODY),
                    eq(rf"\text{{cylinder: }} {share_tex('cylinder')}\ \text{{of }}K\ \text{{spinning}}", cfg.FONT["body"],
                       cfg.DISC_STRIPE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.1, 1.3, 0])
    fit_width(shares, 6.5)
    same_pe = caption("both lose the same potential energy", cfg.ENERGY)
    scene.play(FadeIn(same_pe), run_time=0.6)
    scene.play(FadeIn(shares[0], shift=LEFT * 0.1), run_time=0.8)
    scene.play(FadeIn(shares[1], shift=LEFT * 0.1), run_time=0.8)
    more = caption("the cylinder keeps more for moving forward", cfg.DISC_STRIPE)
    scene.play(fade_through(same_pe, more), run_time=0.8)

    # --- 6. The law -----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    law = eq(r"a_{\mathrm{cm}} = {g\sin\beta \over 1 + I_{\mathrm{cm}}/MR^2}", cfg.FONT["section"], cfg.WHITE)
    fit_width(law, 6.3)
    law_box = boxed(law, cfg.RESULT).move_to([4.1, 2.85, 0])
    scene.play(FadeOut(VGroup(win, shares, more)), run_time=0.5)
    scene.play(Write(law), run_time=1.1)
    scene.play(Create(law_box.frame), run_time=0.6)
    contact = lambda: centre(c_cyl, LANES["cylinder"], R) - NORMAL * R
    friction = Vector(contact, lambda: contact() - DOWN_SLOPE * 1.05, cfg.FORCE, width=0.07, tip=0.22)
    friction_label = Tag(eq("f_s", cfg.FONT["body"], cfg.FORCE), lambda: contact() - DOWN_SLOPE * 1.05, UP * 0.3)
    hidden(friction, friction_label)
    stage.add_overlay(friction, friction_label)
    scene.play(stage.fade(friction, 1.0), stage.fade(friction_label, 1.0), run_time=0.8)

    # --- 7. 2/3 vs 1/2 g sin beta: 3.27 vs 2.45 ----------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    rows = VGroup(
        eq(rf"\text{{cylinder: }}\tfrac23 g\sin\beta \approx {fx(INC.a_cylinder, 2)}\ \mathrm{{m/s^2}}", cfg.FONT["body"], cfg.DISC_STRIPE),
        eq(rf"\text{{ring: }}\tfrac12 g\sin\beta \approx {fx(INC.a_ring, 2)}\ \mathrm{{m/s^2}}", cfg.FONT["body"], cfg.RING_BODY),
    ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    fit_width(rows, 6.4)
    rows.move_to([4.1, 0.65, 0])
    scene.play(Write(rows[0]), run_time=1.4)
    scene.play(Write(rows[1]), run_time=1.4)

    # --- 8. A frictionless sliding block beats both ------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    racers = (cyl, ring, cyl_marker, ring_marker)
    scene.play(stage.fade(friction, 0.0), stage.fade(friction_label, 0.0),
               *[stage.fade(body, 0.0) for body in racers], run_time=0.3)
    # Reset while hidden, so a new race does not look like uphill sliding.
    clock.value = 0.0
    stage.refresh()
    scene.play(*[stage.fade(body, 1.0) for body in (*racers, block)], run_time=0.5)
    block_row = eq(rf"\text{{sliding block: }} g\sin\beta = {fx(INC.a_block, 1)}\ \mathrm{{m/s^2}}", cfg.FONT["body"], "#E3A869")
    fit_width(block_row, 6.4)
    block_row.next_to(rows, DOWN, buff=0.45).align_to(rows, LEFT)
    no_spin = caption("block lane: frictionless sliding", "#E3A869", cfg.FONT["small"])
    scene.play(FadeIn(no_spin), Write(block_row), run_time=1.4)
    # Freeze at the block's finish: the cylinder and ring are visibly still uphill.
    scene.play(clock.to(stage, INC.time(0.0), rate_func=linear), run_time=INC.time(0.0) / SLOW)

    # --- 9. Distribution decides --------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    decides = caption("mass distribution decides the race", cfg.RESULT)
    scene.play(fade_through(no_spin, decides), run_time=0.9)
    finish(scene, t, stage)


def share_tex(key: str) -> str:
    """The rotational share of a rolling body's kinetic energy, c / (1 + c), as LaTeX."""
    c = pm.shape(key).coefficient
    return ftex(c / (1 + c))
