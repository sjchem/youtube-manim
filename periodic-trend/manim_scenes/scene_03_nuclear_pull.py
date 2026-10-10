"""The pull of the nucleus: charge and distance, then what a cloud really shows.

The bar heights are Coulomb's law (``pm.coulomb_pull``): doubling the charge
doubles the bar; doubling the distance quarters it. The planetary orbit is
drawn only to be crossed out.
"""

from manim_scenes.common import *

NUCLEUS_AT = np.array([-3.4, 0.2, 0])
NEAR = 2.2                         # screen distance of the electron at "r"
BAR_X = 4.6
BAR_BASE = -2.3
BAR_UNIT = 1.6                     # screen height of the pull of charge 1 at distance r


class Scene03NuclearPull(Scene):
    def construct(self) -> None:
        play_scene(self)


def pull_bar(charge: float, distance: float) -> Rectangle:
    height = BAR_UNIT * pm.coulomb_pull(charge, distance)
    bar = Rectangle(width=0.9, height=max(height, 0.02), stroke_width=0, fill_color=cfg.PULL_COLOR, fill_opacity=0.9)
    return bar.move_to([BAR_X, BAR_BASE + height / 2, 0])


def tug_arrow(electron: Mobject, charge: float, distance: float) -> Arrow:
    start = electron.get_center()
    end = start + (NUCLEUS_AT - start) / np.linalg.norm(NUCLEUS_AT - start) * 1.1
    strength = pm.coulomb_pull(charge, distance)
    return Arrow(start + LEFT * 0.18, end, buff=0, color=cfg.PULL_COLOR, stroke_width=3 + 5 * strength,
                 tip_length=0.18 + 0.08 * strength, max_tip_length_to_length_ratio=0.5,
                 max_stroke_width_to_length_ratio=30)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "03", "The pull of the nucleus")

    # --- 1. Positive nucleus, negative electron ---------------------------------------
    core = nucleus_core("+1", 0.42).move_to(NUCLEUS_AT)
    electron = glow_dot(NUCLEUS_AT + RIGHT * NEAR, 0.16)
    minus = txt("−", cfg.FONT["title"], cfg.CYAN).next_to(electron, UP, buff=0.18)
    plus = txt("positive", cfg.FONT["small"], cfg.RED).next_to(core, DOWN, buff=0.45)
    neg = txt("negative", cfg.FONT["small"], cfg.CYAN).next_to(electron, DOWN, buff=0.45)
    scene.play(FadeIn(core, scale=0.6), FadeIn(plus, shift=UP * 0.15), run_time=1.0)
    scene.play(FadeIn(electron, scale=0.5), FadeIn(minus), FadeIn(neg, shift=UP * 0.15), run_time=1.0)

    # --- 2. Opposites attract --------------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    arrow = tug_arrow(electron, 1, 1)
    scene.play(GrowArrow(arrow), run_time=0.9)
    scene.play(electron.animate(rate_func=there_and_back).shift(LEFT * 0.35), run_time=1.2)
    attract = chip("opposite charges attract", cfg.GOLD, cfg.FONT["small"]).move_to([-1.3, 2.6, 0])
    scene.play(FadeIn(attract, shift=DOWN * 0.15), run_time=0.7)

    # --- 3. Two dials: charge and distance --------------------------------------------------
    beat(scene, t, 2)
    axis = Line([BAR_X - 0.9, BAR_BASE, 0], [BAR_X + 0.9, BAR_BASE, 0], stroke_color=cfg.MUTED, stroke_width=3)
    bar = pull_bar(1, 1)
    bar_name = txt("pull", cfg.FONT["label"], cfg.GOLD).next_to(axis, DOWN, buff=0.25)
    one = chip("1   charge", cfg.ORANGE, cfg.FONT["small"]).move_to([-1.3, 2.6, 0])
    scene.play(*fade_labels(attract, one), Create(axis), GrowFromEdge(bar, DOWN),
               FadeIn(bar_name), FadeOut(plus), FadeOut(neg), run_time=1.0)

    # --- 4. Twice the charge, twice the pull --------------------------------------------------
    beat(scene, t, 3)
    stronger = nucleus_core("+2", 0.5).move_to(NUCLEUS_AT)
    double = pull_bar(2, 1)
    new_arrow = tug_arrow(electron, 2, 1)
    scene.play(FadeThrough(core, stronger), Transform(bar, double), Transform(arrow, new_arrow), run_time=1.4)
    core = stronger
    times_two = eq(r"\times 2", cfg.FONT["section"], cfg.GOLD).next_to(bar, LEFT, buff=0.3)
    scene.play(FadeIn(times_two, scale=1.3), run_time=0.6)
    scene.play(electron.animate(rate_func=there_and_back).shift(LEFT * 0.45), run_time=1.2)

    # --- 5. Distance ---------------------------------------------------------------------------
    beat(scene, t, 4)
    two = chip("2   distance", cfg.CYAN, cfg.FONT["small"]).move_to([-1.3, 2.6, 0])
    back = nucleus_core("+1", 0.42).move_to(NUCLEUS_AT)
    scene.play(*fade_labels(one, two), FadeThrough(core, back),
               Transform(bar, pull_bar(1, 1)), Transform(arrow, tug_arrow(electron, 1, 1)), FadeOut(times_two),
               run_time=1.0)
    core = back
    near_mark = DashedLine(NUCLEUS_AT + DOWN * 1.35, NUCLEUS_AT + RIGHT * NEAR + DOWN * 1.35, stroke_color=cfg.MUTED,
                           stroke_width=3, dash_length=0.1)
    near_tag = eq("r", cfg.FONT["label"], cfg.CYAN).next_to(near_mark, DOWN, buff=0.15)
    scene.play(Create(near_mark), FadeIn(near_tag), run_time=0.8)
    scene.play(electron.animate.shift(RIGHT * NEAR), minus.animate.shift(RIGHT * NEAR), FadeOut(arrow), run_time=1.6)

    # --- 6. Double the distance, a quarter of the pull -------------------------------------------
    beat(scene, t, 5)
    far_mark = DashedLine(NUCLEUS_AT + DOWN * 1.95, NUCLEUS_AT + RIGHT * 2 * NEAR + DOWN * 1.95, stroke_color=cfg.CYAN,
                          stroke_width=3, dash_length=0.1)
    far_tag = eq("2r", cfg.FONT["label"], cfg.CYAN).next_to(far_mark, DOWN, buff=0.15)
    arrow = tug_arrow(electron, 1, 2)
    scene.play(Create(far_mark), FadeIn(far_tag), GrowArrow(arrow), Transform(bar, pull_bar(1, 2)), run_time=1.4)
    quarter = eq(r"\times \tfrac{1}{4}", cfg.FONT["section"], cfg.GOLD).next_to(bar, LEFT, buff=0.3).shift(UP * 0.3)
    scene.play(FadeIn(quarter, scale=1.3), run_time=0.6)

    # --- 7. The law, as an object ------------------------------------------------------------------
    beat(scene, t, 6)
    law = eq(r"\text{pull} \;\propto\; \frac{Z}{r^{2}}", 64, cfg.WHITE)
    law.move_to([0.2, 0.2, 0])
    holder = glow_frame(law, cfg.WHITE, buff=0.3)
    scene.play(FadeOut(VGroup(core, electron, minus, arrow, near_mark, near_tag, far_mark, far_tag, two, quarter)),
               FadeOut(VGroup(bar, axis, bar_name)), run_time=0.8)
    scene.play(Write(law), Create(holder), run_time=1.6)
    notes = VGroup(txt("Z: charge of the nucleus", cfg.FONT["small"], cfg.ORANGE),
                   txt("r: distance to the electron", cfg.FONT["small"], cfg.CYAN)).arrange(DOWN, buff=0.22)
    notes.next_to(holder, DOWN, buff=0.45)
    scene.play(FadeIn(notes, shift=UP * 0.15), run_time=0.8)

    # --- 8. Not planets on orbits --------------------------------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "Clouds, not orbits")
    scene.play(FadeOut(VGroup(law, holder, notes)), run_time=0.6)
    orbit_at = np.array([-3.6, 0.0, 0])
    sun = nucleus_core("+", 0.3).move_to(orbit_at)
    ring = Circle(radius=1.8, stroke_color=cfg.MUTED, stroke_width=3).move_to(orbit_at)
    planet = glow_dot(orbit_at + RIGHT * 1.8, 0.13)
    scene.play(FadeIn(sun), Create(ring), FadeIn(planet), run_time=1.0)
    scene.play(MoveAlongPath(planet, ring), run_time=1.6, rate_func=linear)
    wrong = cross_mark(1.1, cfg.RED).move_to(orbit_at)
    scene.play(Create(wrong), run_time=0.6)

    # --- 9. Likely and rare ---------------------------------------------------------------------------
    beat(scene, t, 8)
    cloud_at = np.array([3.4, 0.0, 0])
    atom = Atom(2.0, cloud_at, charge="+", count=520, seed=21, nucleus_radius=0.28, glow=0.2)
    scene.play(FadeIn(atom, scale=0.7), VGroup(sun, ring, planet, wrong).animate.set_opacity(0.3), run_time=1.4)
    dense = txt("dense: likely", cfg.FONT["small"], cfg.WHITE).move_to(cloud_at + np.array([-0.3, 2.95, 0]))
    dense_line = Line(dense.get_bottom() + DOWN * 0.08, cloud_at + UP * 0.45, stroke_color=cfg.WHITE, stroke_width=2.5)
    faint = txt("faint: rare", cfg.FONT["small"], cfg.MUTED).move_to(cloud_at + np.array([2.2, -2.75, 0]))
    faint_line = Line(faint.get_top() + UP * 0.08, cloud_at + np.array([1.85, -1.55, 0]), stroke_color=cfg.MUTED,
                      stroke_width=2.5)
    scene.play(Create(dense_line), FadeIn(dense), run_time=0.8)
    scene.play(Create(faint_line), FadeIn(faint), run_time=0.8)

    # --- 10. No hard edge: a contour holds most of the cloud --------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(sun, ring, planet, wrong)), FadeOut(VGroup(dense, dense_line, faint, faint_line)),
               run_time=0.7)
    scene.play(Glide(atom, [-2.2, 0.0, 0]), run_time=1.0)
    contour = DashedVMobject(Circle(radius=2.0, stroke_color=cfg.WHITE, stroke_width=3.5), num_dashes=56)
    contour.move_to(atom.center_point())
    scene.play(Create(contour), run_time=1.2)
    holds = VGroup(txt("Display contour", cfg.FONT["body"], cfg.WHITE),
                   txt("Cloud continues beyond it", cfg.FONT["small"], cfg.CYAN)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    holds.move_to([3.6, 0.9, 0])
    wall = chip('No hard boundary', cfg.GOLD, cfg.FONT["label"]).move_to([3.6, -1.0, 0])
    scene.play(FadeIn(holds, shift=LEFT * 0.2), run_time=0.8)
    scene.play(FadeIn(wall, scale=1.1), run_time=0.8)
    scene.play(Indicate(contour, color=cfg.GOLD, scale_factor=1.03), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
