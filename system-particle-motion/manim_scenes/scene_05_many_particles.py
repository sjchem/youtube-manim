"""Scene 05 — many particles, one point. Eleven beads of unequal mass hang in
a turning 3D frame with x, y, z axes. One bead is labelled m_i with its teal
position vector r_i; the total mass and the vector formula follow. Every
position vector appears, then the white R_cm and the centre-of-mass target.
One bead is made heavier and the target slides toward it. Dashed drops give
the three coordinates. The origin is moved: every vector swings, the target
does not. The beads multiply into a smooth solid and one gold element dm with
its r leads to the integral.
"""

from manim_scenes.common import *

MASSES, POSITIONS = pm.particle_cloud()
ORIGIN_3D = np.array([-2.2, -1.6, -0.6])
BOOSTED = int(np.argmax(POSITIONS[:, 0]))       # the bead we make heavier: the right-most one
SHOWN = int(np.argmax(POSITIONS[:, 1]))         # the bead we label m_i, r_i: the top one


class Scene05ManyParticles(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Many particles, one point")
    stage = Stage((2.5, -0.3, 0.0), zoom=1.0, yaw=-0.45, pitch=0.28, sway=0.05)
    boost = Knob(1.0)
    origin = Knob(0.0)                                 # 0: first origin; 1: the moved origin
    moved_to = ORIGIN_3D + np.array([2.4, 0.6, 0.6])

    def o() -> np.ndarray:
        return ORIGIN_3D + (moved_to - ORIGIN_3D) * origin.value

    def masses() -> np.ndarray:
        m = MASSES.copy()
        m[BOOSTED] *= boost.value
        return m

    def com() -> np.ndarray:
        return pm.com(masses(), POSITIONS)

    axes = []
    for d, color, name, length in ((np.array([1, 0, 0]), cfg.X_COLOR, "x", 3.0), (np.array([0, 1, 0]), cfg.Y_COLOR, "y", 3.0),
                                   (np.array([0, 0, 1]), cfg.Z_COLOR, "z", 1.6)):
        axes.append(Segment(lambda d=d: o() - d * 0.2, lambda d=d, n=length: o() + d * n, color, width=3, opacity=0.7))
        axes.append(Tag(eq(name, cfg.FONT["label"], color), lambda d=d, n=length: o() + d * (n + 0.25)))
    origin_dot = Tag(glow_dot(ORIGIN, cfg.WHITE, 0.07), o)
    o_label = Tag(eq("O", cfg.FONT["label"], cfg.WHITE), o, LEFT * 0.7 + UP * 0.25)
    beads = []
    for k, (m, p) in enumerate(zip(MASSES, POSITIONS)):
        radius = lambda k=k: 0.11 + 0.045 * masses()[k]  # noqa: E731
        bead = Ball(p, 0.11 + 0.045 * m, cfg.MASS)
        beads.append((bead, radius))
    stage.add_body(*[a for a in axes if not isinstance(a, Tag)], *[b for b, _ in beads])
    stage.add_overlay(*[a for a in axes if isinstance(a, Tag)], origin_dot, o_label)

    def resize(_m):
        for bead, radius in beads:
            bead.radius = radius()

    holder = Dot(radius=0.001, fill_opacity=0)
    holder.add_updater(resize)
    scene.add(holder)
    show(scene, stage, 1.2)
    scene.play(*stage.turn(yaw=-0.25), run_time=2.4)

    # --- 2. One particle: m_i at r_i --------------------------------------------------------------------------------
    beat(scene, t, 1)
    r_i = Vector(o, POSITIONS[SHOWN], cfg.POSITION, width=0.06, tip=0.24)
    r_lab = Tag(eq(r"\vec r_i", cfg.FONT["body"], cfg.POSITION), lambda: 0.5 * (o() + POSITIONS[SHOWN]), LEFT * 0.45)
    m_lab = Tag(eq("m_i", cfg.FONT["body"], cfg.MASS), POSITIONS[SHOWN], UR * 0.45)
    hidden(r_i, r_lab, m_lab)
    stage.add_overlay(r_i, r_lab, m_lab)
    scene.play(stage.fade(m_lab, 1.0), run_time=0.8)
    scene.play(stage.fade(r_i, 1.0), stage.fade(r_lab, 1.0), run_time=1.0)

    # --- 3. Total mass ---------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    total = eq(r"M = \sum_i m_i", cfg.FONT["section"], cfg.MASS).move_to([-4.7, 3.1, 0])
    scene.play(Write(total), run_time=1.4)

    # --- 4. R_cm = (1/M) sum m_i r_i -----------------------------------------------------------------------------------------
    beat(scene, t, 3)
    formula = eq(r"\vec R_{\mathrm{cm}} = {1 \over M} \sum_i m_i \vec r_i", cfg.FONT["section"], cfg.WHITE)
    formula_box = boxed(formula, cfg.WHITE).move_to([-4.5, 0.8, 0])
    scene.play(Write(formula), run_time=2.0)
    scene.play(Create(formula_box.frame), run_time=0.7)
    all_r = [Vector(o, p, cfg.POSITION, width=0.03, tip=0.16) for k, p in enumerate(POSITIONS) if k != SHOWN]
    hidden(*all_r)
    stage.add_overlay(*all_r)
    scene.play(*[stage.fade(v, 0.55) for v in all_r], stage.fade(r_lab, 0.0), stage.fade(m_lab, 0.0), run_time=1.2)
    R_cm = Vector(o, com, cfg.WHITE, width=0.08, tip=0.3)
    target = com_tag(com, 0.2)
    R_lab = Tag(eq(r"\vec R_{\mathrm{cm}}", cfg.FONT["body"], cfg.WHITE), lambda: 0.55 * (o() + com()), DR * 0.5)
    hidden(R_cm, target, R_lab)
    stage.add_overlay(R_cm, target, R_lab)
    scene.play(stage.fade(R_cm, 1.0), stage.fade(target, 1.0), stage.fade(R_lab, 1.0),
               *[stage.fade(v, 0.25) for v in all_r + [r_i]], run_time=1.4)

    # --- 5. Heavier pulls harder ---------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    pull = caption("greater mass → COM shifts", cfg.MASS)
    scene.play(FadeIn(pull), run_time=0.6)
    scene.play(boost.to(stage, 3.0), run_time=1.6)
    scene.play(boost.to(stage, 1.0), run_time=1.4)

    # --- 6. Three components ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    comps = VGroup(*[eq(rf"{c}_{{\mathrm{{cm}}}} = {{\sum m_i {c}_i \over M}}", cfg.FONT["body"], col)
                     for c, col in (("x", cfg.X_COLOR), ("y", cfg.Y_COLOR), ("z", cfg.Z_COLOR))])
    comps.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    fit_inside(comps, 5.6, 3.0)
    comps.move_to([-4.6, -1.85, 0])
    drops = []
    for axis_k, color in ((0, cfg.X_COLOR), (1, cfg.Y_COLOR), (2, cfg.Z_COLOR)):
        def foot(axis_k=axis_k):
            v = np.zeros(3)
            v[axis_k] = (com() - o())[axis_k]
            return o() + v
        drops.append(Segment(com, foot, color, width=3, opacity=0.9, dashed=True))
    hidden(*drops)
    stage.add_body(*drops)
    scene.play(FadeOut(pull), run_time=0.4)
    for k in range(3):
        scene.play(FadeIn(comps[k], shift=RIGHT * 0.15), stage.fade(drops[k], 1.0), run_time=0.8)

    # --- 7. Move the origin: the centre of mass stays put ----------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(*[stage.fade(d, 0.0) for d in drops], FadeOut(comps), *[stage.fade(v, 0.55) for v in all_r + [r_i]], run_time=0.8)
    same_point = caption("new origin · same physical COM", cfg.WHITE)
    scene.play(FadeIn(same_point), run_time=0.6)
    scene.play(origin.to(stage, 1.0), run_time=3.0)
    scene.play(Indicate(formula, color=cfg.GOLD, scale_factor=1.03), run_time=1.0)
    scene.play(origin.to(stage, 0.0), run_time=2.0)

    # --- 8. A solid: mass smoothly spread -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    rng = np.random.default_rng(cfg.SEED + 5)
    blob = rng.normal(size=(420, 3))
    blob /= np.linalg.norm(blob, axis=1, keepdims=True)
    blob *= rng.random((420, 1)) ** (1 / 3)
    blob = blob * np.array([1.9, 1.3, 1.4]) + com()
    solid = Dots(blob, cfg.MASS, radius=0.055, alpha=0.9)
    solid.presence = 0.0
    stage.add_body(solid)
    smooth_spread = caption("continuous mass distribution", cfg.MASS)
    scene.play(fade_through(same_point, smooth_spread), *[stage.fade(v, 0.0) for v in all_r + [r_i]],
               *[stage.fade(b, 0.0) for b, _ in beads], stage.fade(solid, 1.0), run_time=2.0)

    # --- 9. The integral --------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    element_at = com() + np.array([1.2, 0.7, 0.4])
    element = Ball(element_at, 0.12, cfg.GOLD, layers=14)
    element.bias = 50
    dm_lab = Tag(eq("dm", cfg.FONT["body"], cfg.GOLD), element_at, UR * 0.42)
    r_el = Vector(o, element_at, cfg.POSITION, width=0.06, tip=0.24)
    r_el_lab = Tag(eq(r"\vec r", cfg.FONT["body"], cfg.POSITION), lambda: 0.5 * (o() + element_at), UL * 0.4)
    hidden(element, dm_lab, r_el, r_el_lab)
    stage.add_body(element)
    stage.add_overlay(r_el, dm_lab, r_el_lab)
    scene.play(stage.fade(element, 1.0), stage.fade(dm_lab, 1.0), run_time=0.9)
    scene.play(stage.fade(r_el, 1.0), stage.fade(r_el_lab, 1.0), run_time=0.9)
    integral = eq(r"\vec R_{\mathrm{cm}} = {1 \over M} \int \vec r\, dm", cfg.FONT["section"], cfg.WHITE)
    integral_box = boxed(integral, cfg.RESULT).move_to([-4.5, -1.7, 0])
    sum_to_int = Arrow(formula_box.get_bottom(), integral_box.get_top(), buff=0.15, stroke_color=cfg.MUTED, stroke_width=4)
    scene.play(GrowArrow(sum_to_int), FadeOut(smooth_spread), run_time=0.8)
    scene.play(Write(integral), run_time=1.6)
    scene.play(Create(integral_box.frame), run_time=0.8)

    # --- 10. Same idea; next, motion -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    nxt = caption("now: what happens when things move?", cfg.CYAN)
    scene.play(FadeIn(nxt), stage.fade(o_label, 0.0), *[stage.fade(a, 0.0) for a in axes if isinstance(a, Tag)],
               *stage.turn(yaw=stage.yaw + 0.5), run_time=2.0)
    finish(scene, t, stage)
