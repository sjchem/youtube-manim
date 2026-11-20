"""Scene 02 — the road ahead. A glowing path winds across the frame through
five numbered stops, and a gold molecule travels along it as each stop is
named. Every stop gets a small picture drawn from the film's own grammar:

1. speeds — a gold Maxwell-Boltzmann curve (``pm.maxwell_pdf``) over a cyan histogram;
2. assumptions — two molecules: a red forbidden circle (size) and a green link (attraction);
3. repairs — a tiny Z-against-P plot: dashed purple ideal line, a green dip, a red rise;
4. the critical point — the coexistence dome (``pm.binodal``) with a purple point on top;
5. liquids — a deep-blue drop over a rippling surface.

The last beat sends the molecule along the whole path while every picture
pulses in turn: the same molecules, only the conditions change.
"""

from manim_scenes.common import *
from manim_scenes.kit_d import at_word

NODE_X = (-5.6, -2.8, 0.0, 2.8, 5.6)
NODE_Y = (-0.75, -0.3, -0.75, -0.3, -0.75)
ICON_Y = 1.45
ICON_SCALE = 1.32
LABEL_Y = (-1.65, -2.35)
LABELS = ("speeds", "assumptions", "repairs", "critical point", "liquids")
COLORS = (cfg.GOLD, cfg.RED, cfg.GREEN, cfg.PURPLE, cfg.LIQUID_EDGE)


class Scene02Roadmap(Scene):
    def construct(self) -> None:
        play_scene(self)


# ----------------------------------------------------------------------------
# The five pictures (each about 1.8 wide, 1.2 tall, centred on the origin)
# ----------------------------------------------------------------------------


def icon_speeds() -> VGroup:
    s = np.linspace(0, 2.6, 60)
    f = pm.maxwell_pdf(s)
    w, h = 1.9, 1.15
    pts = [np.array([x / 2.6 * w - w / 2, y / f.max() * h - h / 2, 0]) for x, y in zip(s, f)]
    rng = np.random.default_rng(cfg.SEED + 20)
    samples = np.linalg.norm(rng.normal(scale=1 / np.sqrt(3), size=(400, 3)), axis=1)
    edges = np.linspace(0, 2.6, 14)
    counts, _ = np.histogram(samples, edges)
    dens = counts / (len(samples) * (edges[1] - edges[0])) / f.max()
    bars = VGroup(*[Rectangle(width=w / 13 * 0.86, height=max(d * h, 0.02), stroke_width=0, fill_color=cfg.MOLECULE,
                              fill_opacity=0.45).move_to([((a + b) / 2) / 2.6 * w - w / 2, -h / 2 + d * h / 2, 0])
                    for a, b, d in zip(edges[:-1], edges[1:], dens)])
    curve = polyline(pts, cfg.GOLD, width=5)
    base = Line([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], stroke_color=cfg.MUTED, stroke_width=3)
    return VGroup(bars, curve.copy().set_stroke(width=14, opacity=0.18), curve, base)


def icon_assumptions() -> VGroup:
    a = bead([-0.5, -0.05, 0], cfg.MOLECULE, 0.2, glow=0.6)
    b = bead([0.62, 0.15, 0], cfg.MOLECULE, 0.2, glow=0.6)
    zone = DashedVMobject(Circle(radius=0.44, stroke_color=cfg.RED, stroke_width=4).move_to(a), num_dashes=16)
    link = Line(a.get_center(), b.get_center(), stroke_color=cfg.GREEN, stroke_width=5)
    glow = link.copy().set_stroke(width=14, opacity=0.2)
    return VGroup(zone, glow, link, a, b)


def icon_repairs() -> VGroup:
    w, h = 1.9, 1.2
    one = DashedLine([-w / 2, 0, 0], [w / 2, 0, 0], stroke_color=cfg.PURPLE, stroke_width=3, dash_length=0.1)
    xs = np.linspace(0, 1, 40)
    z = 1 - 1.4 * xs * np.exp(-4 * xs) * 2.2 + 0.9 * xs ** 2.2
    pts = [np.array([x * w - w / 2, (zz - 1) * h * 0.9, 0]) for x, zz in zip(xs, z)]
    low = [p for p, zz in zip(pts, z) if zz <= 1.0]
    high = [p for p, zz in zip(pts, z) if zz >= 1.0 and p[0] > 0]
    green = polyline(low, cfg.GREEN, width=5)
    red = polyline([low[-1], *high], cfg.RED, width=5)
    axis = VGroup(Line([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], stroke_color=cfg.MUTED, stroke_width=3),
                  Line([-w / 2, -h / 2, 0], [-w / 2, h / 2, 0], stroke_color=cfg.MUTED, stroke_width=3))
    z_tag = eq("Z", cfg.FONT["tiny"], cfg.GOLD).next_to(axis[1], LEFT, buff=0.08).shift(UP * 0.35)
    return VGroup(axis, one, green, red, z_tag)


def icon_critical() -> VGroup:
    dome = pm.binodal(40, 0.62)
    w, h = 1.9, 1.15
    v = np.log(dome[:, 0])
    vmin, vmax = v.min(), v.max()
    p = dome[:, 1]
    pts = [np.array([(a - vmin) / (vmax - vmin) * w - w / 2, (b - p.min()) / (1 - p.min()) * h - h / 2, 0])
           for a, b in zip(v, p)]
    fill = Polygon(*pts, stroke_width=0, fill_color=cfg.COEXIST, fill_opacity=0.35)
    edge = polyline(pts, cfg.LIQUID_EDGE, width=4)
    top = glow_dot(pts[len(pts) // 2], cfg.PURPLE, radius=0.11)
    return VGroup(fill, edge, top)


def icon_liquid() -> VGroup:
    t = np.linspace(0, 2 * np.pi, 80)
    pts = [np.array([0.5 * np.sin(a) * np.sin(a / 2), 0.62 * np.cos(a) + 0.18, 0]) for a in t]
    drop = Polygon(*pts, stroke_color=cfg.LIQUID_EDGE, stroke_width=3, fill_color=cfg.LIQUID, fill_opacity=0.85)
    shine = Arc(radius=0.22, start_angle=2.1, angle=1.0, stroke_color=cfg.WHITE, stroke_width=4).move_to([-0.17, -0.02, 0])
    ripples = VGroup(*[Ellipse(width=0.9 + 0.5 * k, height=0.16 + 0.06 * k, stroke_color=cfg.LIQUID_EDGE, stroke_width=3,
                               stroke_opacity=0.8 - 0.25 * k).move_to([0, -0.6, 0]) for k in range(3)])
    return VGroup(ripples, drop, shine)


# ----------------------------------------------------------------------------


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "02", TITLES["02"])

    # The winding path through five stops.
    knots = [np.array([-7.2, -0.55, 0])] + [np.array([x, y, 0]) for x, y in zip(NODE_X, NODE_Y)] + [np.array([7.2, -0.55, 0])]
    spline = VMobject().set_points_smoothly(knots)
    pts = np.array([spline.point_from_proportion(a) for a in np.linspace(0, 1, 400)])
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    arc /= arc[-1]
    stops = [float(arc[np.argmin(np.linalg.norm(pts - np.array([x, y, 0]), axis=1))]) for x, y in zip(NODE_X, NODE_Y)]

    def along(s: float) -> np.ndarray:
        return np.array([np.interp(s, arc, pts[:, 0]), np.interp(s, arc, pts[:, 1]), 0.0])

    road = polyline(pts, cfg.CYAN, width=5, opacity=0.75)
    road_glow = road.copy().set_stroke(width=16, opacity=0.12)
    lit = Knob(0.0)
    trail = live(VMobject(), lambda: polyline([along(s) for s in np.linspace(0, max(lit.value, 1e-3), 120)], cfg.GOLD,
                                              width=7) if lit.value > 0.005 else VMobject())
    nodes = VGroup()
    for k, (x, y) in enumerate(zip(NODE_X, NODE_Y)):
        ring = Circle(radius=0.36, stroke_color=COLORS[k], stroke_width=4, fill_color=cfg.PANEL, fill_opacity=1)
        num = txt(str(k + 1), cfg.FONT["tiny"], cfg.WHITE).move_to(ring)
        nodes.add(VGroup(ring, num).move_to([x, y, 0]))
    ride = Knob(0.0)
    traveller = live(VGroup(), lambda: glow_dot(along(ride.value), cfg.GOLD, radius=0.13, reach=3.6))

    scene.play(Create(road_glow), Create(road), run_time=1.3)
    scene.add(trail)
    play_in(scene, t, 1, LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.15), run_time=1.0)

    icons = [icon_speeds(), icon_assumptions(), icon_repairs(), icon_critical(), icon_liquid()]
    labels = []
    for k, (icon, word) in enumerate(zip(icons, LABELS)):
        icon.scale(ICON_SCALE).move_to([NODE_X[k], ICON_Y, 0])
        label = txt(word, cfg.FONT["label"], COLORS[k])
        label.move_to([NODE_X[k], LABEL_Y[k % 2], 0])
        labels.append(label)
    stems = [DashedLine(nodes[k].get_top(), icons[k].get_bottom() + DOWN * 0.08, stroke_color=COLORS[k], stroke_width=2.5,
                        stroke_opacity=0.6, dash_length=0.08) for k in range(5)]

    def arrive(k: int, run_time: float = 1.2) -> None:
        if k == 0:
            scene.add(traveller)
        scene.play(lit.to(trail, stops[k], rate_func=smooth), ride.to(traveller, stops[k], rate_func=smooth), nodes[k][0].animate.set_fill(COLORS[k], opacity=0.35),
                   run_time=run_time)
        scene.play(Create(stems[k]), FadeIn(icons[k], shift=UP * 0.2, scale=0.85), FadeIn(labels[k], shift=UP * 0.1),
                   run_time=1.0)

    # --- 1. Speeds -------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    arrive(0)
    at_word(scene, t, 1, "speed", lead=0.2)
    many = txt("not one speed", cfg.FONT["small"], cfg.GOLD).move_to([NODE_X[0] + 0.6, 3.05, 0])
    scene.play(Indicate(icons[0][2], color=cfg.WHITE, scale_factor=1.12), FadeIn(many, shift=DOWN * 0.1), run_time=1.2)
    play_in(scene, t, 2, FadeOut(many), run_time=0.8)

    # --- 2. The assumptions, and the two that fail first -------------------------------------------------------------
    beat(scene, t, 2)
    arrive(1)
    at_word(scene, t, 2, "size", lead=0.2)
    size = txt("size", cfg.FONT["small"], cfg.RED)
    pull = txt("attraction", cfg.FONT["small"], cfg.GREEN)
    VGroup(size, pull).arrange(RIGHT, buff=0.4).move_to([NODE_X[1], 3.05, 0])
    scene.play(FadeIn(size, shift=DOWN * 0.1), Indicate(icons[1][0], color=cfg.WHITE, scale_factor=1.15), run_time=0.9)
    at_word(scene, t, 2, "attraction", lead=0.2)
    scene.play(FadeIn(pull, shift=DOWN * 0.1), Indicate(icons[1][2], color=cfg.WHITE, scale_factor=1.15), run_time=0.9)
    play_in(scene, t, 3, FadeOut(size), FadeOut(pull), run_time=0.8)

    # --- 3. Repair the equation, measure the departure ---------------------------------------------------------------
    beat(scene, t, 3)
    arrive(2)
    at_word(scene, t, 3, "measure", lead=0.2)
    scene.play(Create(icons[2][2].copy().set_stroke(cfg.WHITE, width=8, opacity=0.5), remover=True),
               Indicate(icons[2][3], color=cfg.WHITE, scale_factor=1.1), run_time=1.2)

    # --- 4. The boundary, and the point where it disappears ----------------------------------------------------------
    beat(scene, t, 4)
    arrive(3)
    at_word(scene, t, 4, "disappears", lead=0.4)
    peak = icons[3][2]
    ring = Circle(radius=0.3, stroke_color=cfg.PURPLE, stroke_width=5).move_to(peak)
    play_in(scene, t, 5, FadeIn(ring), ring.animate.scale(2.2).set_stroke(opacity=0), icons[3][0].animate.set_fill(opacity=0.08),
            run_time=1.6)
    scene.remove(ring)

    # --- 5. Liquids --------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    arrive(4)
    words = ("evaporate", "surfaces", "flow")
    for w in words:
        at_word(scene, t, 5, w, lead=0.2)
        scene.play(Indicate(icons[4][1], color=cfg.WHITE, scale_factor=1.12), run_time=0.8)

    # --- 6. Same molecules, different conditions ---------------------------------------------------------------------
    beat(scene, t, 6)
    end_s = 1.0
    msg = VGroup(txt("same molecules", cfg.FONT["section"], cfg.GOLD), txt("different conditions", cfg.FONT["label"], cfg.CYAN))
    msg.arrange(DOWN, buff=0.22).move_to([0, -3.62, 0])
    ride.value = 0.0
    scene.play(lit.to(trail, end_s, rate_func=smooth, run_time=3.6), ride.to(traveller, end_s, rate_func=smooth, run_time=3.6),
               LaggedStart(*[Indicate(icon, color=cfg.WHITE, scale_factor=1.1) for icon in icons], lag_ratio=0.55, run_time=3.6),
               FadeIn(msg[0], shift=UP * 0.15, run_time=1.0), run_time=3.6)
    scene.play(FadeIn(msg[1], shift=UP * 0.1), run_time=0.8)
    finish(scene, t, fill=lambda s: [road_glow.animate.set_stroke(cfg.GOLD, width=22, opacity=0.2)])
