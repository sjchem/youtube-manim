"""Experiment 2: walk down group 1 (3D).

Atoms are translucent lit spheres on one shared scale (NCERT radii), each
with one equatorial ring per occupied shell, so a new shell is something you
can count. The camera only tilts about the horizontal axis (theta fixed), so
screen x stays world x and the pinned labels stay under their spheres. The
chapter ends by taking the spheres away: an atom has no surface, and a radius
is half the distance between bonded nuclei.
"""

from manim_scenes.common import *

GROUP_1 = ("Li", "Na", "K", "Rb", "Cs")
HALOGENS = ("F", "Cl", "Br", "I")
SCALE = 0.0062
HALOGEN_SCALE = 0.0105            # the halogens are smaller: drawn larger, and labelled so
GAP = 0.32
NAME_Y = -2.55
VALUE_Y = -3.25
TILT = 64 * DEGREES


class Scene06RadiusDown(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def radius_of(symbol: str, scale: float = SCALE) -> float:
    return ed.ATOMIC_RADII_PM[symbol] * scale


def row_xs(symbols, scale: float = SCALE) -> list[float]:
    radii = [radius_of(s, scale) for s in symbols]
    width = sum(2 * r for r in radii) + GAP * (len(radii) - 1)
    x, xs = -width / 2, []
    for r in radii:
        xs.append(x + r)
        x += 2 * r + GAP
    return xs


def shell_atom(symbol: str, x: float, scale: float = SCALE) -> VGroup:
    """A translucent sphere with one ring per occupied shell (schematic spacing)."""
    r = radius_of(symbol, scale)
    colour = block_color(pm.z_of(symbol))
    sphere = Sphere(radius=r, resolution=(10, 20)).move_to([x, 0, 0])
    sphere.set_fill(colour, opacity=0.38).set_stroke(width=0)
    shells = pm.outer_shell(pm.z_of(symbol))
    rings = VGroup(*[Circle(radius=r * (k + 1) / shells, stroke_color=cfg.WHITE if k == shells - 1 else cfg.CORE_COLOR,
                            stroke_width=3 if k == shells - 1 else 2, stroke_opacity=0.9).move_to([x, 0, 0])
                     for k in range(shells)])
    core = Sphere(radius=0.09, resolution=(6, 12)).move_to([x, 0, 0]).set_fill(cfg.NUCLEUS_COLOR, 1).set_stroke(width=0)
    atom = VGroup(rings, core, sphere)
    atom.sphere, atom.rings = sphere, rings
    return atom


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "06", "Experiment 2: down group 1")

    xs = row_xs(GROUP_1)
    atoms = [shell_atom(s, x) for s, x in zip(GROUP_1, xs)]
    names = [txt(s, cfg.FONT["section"], cfg.BLUE).move_to([x, NAME_Y, 0]) for s, x in zip(GROUP_1, xs)]
    hud(scene, *names)
    scene.play(FadeIn(atoms[0], scale=0.6), FadeIn(names[0], shift=UP * 0.15), run_time=1.2)

    # --- Sodium: a whole new shell --------------------------------------------------------
    head = dismiss_opening_title(scene, t, head)
    beat(scene, t, 1)
    scene.play(FadeIn(atoms[1], scale=0.6), FadeIn(names[1], shift=UP * 0.15), run_time=1.2)
    config_na = eq(r"[\mathrm{Ne}]\,3s^{1}", cfg.FONT["label"], cfg.CYAN).move_to([0, 2.9, 0])
    hud(scene, config_na)
    scene.play(FadeIn(config_na, shift=DOWN * 0.15), run_time=0.8)
    scene.play(LaggedStart(*[Indicate(ring, color=cfg.GOLD, scale_factor=1.0) for ring in atoms[1].rings],
                           lag_ratio=0.3), run_time=1.6)

    # --- Potassium, rubidium, caesium -------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(config_na), run_time=0.4)
    for atom, name in zip(atoms[2:], names[2:]):
        scene.play(FadeIn(atom, scale=0.6), FadeIn(name, shift=UP * 0.15), run_time=1.4)

    # --- Tilt: count the shells -------------------------------------------------------------
    beat(scene, t, 3)
    farther = caption('New shell → farther out', cfg.CYAN, cfg.FONT["small"], y=2.95)
    hud(scene, farther)
    move_camera(scene, phi=TILT, theta=-PI / 2, run_time=2.6)
    scene.play(FadeIn(farther, shift=DOWN * 0.15), run_time=0.7)
    scene.play(LaggedStart(*[Indicate(a.rings[-1], color=cfg.GOLD, scale_factor=1.0) for a in atoms], lag_ratio=0.2),
               run_time=2.0)

    # --- The numbers ---------------------------------------------------------------------------
    beat(scene, t, 4)
    values = [txt(f"{ed.ATOMIC_RADII_PM[s]} pm", cfg.FONT["small"], cfg.WHITE).move_to([x, VALUE_Y, 0])
              for s, x in zip(GROUP_1, xs)]
    hud(scene, *values)
    for value in values:
        scene.play(FadeIn(value, shift=UP * 0.15), run_time=0.75)

    beat(scene, t, 5)
    ratio = ed.ATOMIC_RADII_PM["Cs"] / ed.ATOMIC_RADII_PM["Li"]
    times = chip(f"caesium ≈ {ratio:.1f} × lithium", cfg.GOLD, cfg.FONT["label"]).move_to([0, 2.95, 0])
    hud(scene, times)
    scene.play(*fade_labels(farther, times), run_time=0.8)
    scene.play(Indicate(atoms[-1].sphere, color=cfg.WHITE, scale_factor=1.04), run_time=1.4)

    # --- The halogens tell the same story -----------------------------------------------------
    beat(scene, t, 6)
    hxs = row_xs(HALOGENS, HALOGEN_SCALE)
    halogens = [shell_atom(s, x, HALOGEN_SCALE) for s, x in zip(HALOGENS, hxs)]
    h_names = [txt(s, cfg.FONT["section"], cfg.GREEN).move_to([x, NAME_Y, 0]) for s, x in zip(HALOGENS, hxs)]
    h_values = [txt(f"{ed.ATOMIC_RADII_PM[s]} pm", cfg.FONT["small"], cfg.WHITE).move_to([x, VALUE_Y, 0])
                for s, x in zip(HALOGENS, hxs)]
    hud(scene, *h_names, *h_values)
    head = swap_heading(scene, head, "Down group 17: the halogens")
    scene.play(FadeOut(VGroup(*atoms)), FadeOut(VGroup(*names, *values, times)), run_time=0.8)
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(a, scale=0.6), FadeIn(n), FadeIn(v))
                             for a, n, v in zip(halogens, h_names, h_values)], lag_ratio=0.35), run_time=2.6)
    zoomed = txt(f"drawn {HALOGEN_SCALE / SCALE:.1f}× larger than group 1", cfg.FONT["tiny"], cfg.MUTED)
    zoomed.move_to([0, 2.95, 0])
    hud(scene, zoomed)
    scene.play(FadeIn(zoomed), run_time=0.6)

    # --- No hard surface -----------------------------------------------------------------------------
    beat(scene, t, 7)
    head = swap_heading(scene, head, "A picture, not a surface")
    scene.play(FadeOut(VGroup(*halogens)), FadeOut(VGroup(*h_names, *h_values, zoomed)), run_time=0.8)
    move_camera(scene, phi=0, theta=-PI / 2, run_time=1.6)
    cloud = Atom(1.7, [-3.9, 0.1, 0], charge="+3", core=0.42, count=480, seed=61, glow=0.22)
    scene.play(FadeIn(cloud, scale=0.7), run_time=1.0)
    thins = txt("thins out gradually", cfg.FONT["small"], cfg.CYAN).move_to([-3.9, -2.75, 0])
    hud(scene, thins)
    scene.play(FadeIn(thins, shift=UP * 0.15), run_time=0.7)

    beat(scene, t, 8)
    left_at, right_at = np.array([1.75, 0.1, 0]), np.array([4.75, 0.1, 0])
    pair = VGroup(ElectronCloud(1.75, left_at, count=260, seed=62, glow=0.16),
                  ElectronCloud(1.75, right_at, count=260, seed=63, glow=0.16))
    nuclei = VGroup(nucleus_core(None, 0.18).move_to(left_at), nucleus_core(None, 0.18).move_to(right_at))
    scene.play(FadeIn(pair), FadeIn(nuclei), run_time=1.0)
    span = DoubleArrow(left_at + DOWN * 2.15, right_at + DOWN * 2.15, buff=0, color=cfg.WHITE, stroke_width=4,
                       tip_length=0.2)
    d_tag = eq("d", cfg.FONT["label"], cfg.WHITE).next_to(span, DOWN, buff=0.15)
    ticks = VGroup(DashedLine(left_at, left_at + DOWN * 2.15, stroke_color=cfg.MUTED, stroke_width=2),
                   DashedLine(right_at, right_at + DOWN * 2.15, stroke_color=cfg.MUTED, stroke_width=2))
    rule = eq(r"r = \frac{d}{2}", cfg.FONT["section"], cfg.GOLD).move_to([3.25, 2.45, 0])
    hud(scene, d_tag, rule)
    scene.play(Create(ticks), GrowFromCenter(span), FadeIn(d_tag), run_time=1.0)
    scene.play(Write(rule), run_time=1.0)
    measure = txt('Radius from bond length', cfg.FONT["small"], cfg.WHITE).move_to([3.25, -3.75, 0])
    hud(scene, measure)
    scene.play(FadeIn(measure, shift=UP * 0.15), run_time=0.7)

    # --- The verdict -----------------------------------------------------------------------------
    beat(scene, t, 9)
    head = swap_heading(scene, head, "Two directions, two winners")
    scene.play(FadeOut(VGroup(cloud, thins, pair, nuclei, span, d_tag, ticks, rule, measure)), run_time=0.8)
    verdict = VGroup(
        VGroup(txt("Across a period", cfg.FONT["body"], cfg.WHITE), txt("nuclear pull wins", cfg.FONT["body"], cfg.GOLD))
        .arrange(DOWN, buff=0.2),
        VGroup(txt("Down a group", cfg.FONT["body"], cfg.WHITE), txt("shells + shielding win", cfg.FONT["body"], cfg.CYAN))
        .arrange(DOWN, buff=0.2),
    ).arrange(RIGHT, buff=1.6).move_to([0, 0.3, 0])
    hud(scene, verdict)
    scene.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in verdict], lag_ratio=0.4), run_time=1.6)

    # --- Teaser: lose an electron ---------------------------------------------------------------------
    beat(scene, t, 10)
    sodium = Atom(1.3, [0, -2.2, 0], charge="+11", core=0.7, count=300, seed=64, nucleus_radius=0.26)
    scene.play(verdict.animate.shift(UP * 1.0), FadeIn(sodium, scale=0.6), run_time=0.9)
    leaving, path = escape_electron(sodium.center_point() + np.array([1.0, 0.6, 0]), np.array([6.8, -0.6, 0]))
    scene.play(FadeIn(leaving, scale=0.4), run_time=0.3)
    scene.play(MoveAlongPath(leaving, path), run_time=1.4, rate_func=rush_into)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
