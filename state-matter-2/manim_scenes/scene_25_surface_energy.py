"""Scene 25 — the cost of a surface. A water drop wobbles into a bead; the camera
dives into a schematic 3D snapshot of a liquid (``pm.liquid_snapshot``: a
disordered, dense slab whose free surface is at the top) on a turning stage.
The crowd dims; one molecule deep inside lights up gold with green bonds to
every neighbour inside the cut-off that ``pm.neighbour_counts`` uses (a green
glass sphere marks the cut-off) — fourteen in this model. A molecule in the top
layer gets only ten: its sphere is empty above. A panel turns the two counts
into an energy ladder: fewer attractions, higher energy. Then the surface is
stretched: the slab widens and thins into a second snapshot of the same
molecules, gold arrows doing the work, and ten molecules (gold) are pulled up
from inside into the surface while gold beads climb the ladder. The new area
glows at the two ends: dW = γ dA, with γ the work per square metre of new
surface. A 3D wire frame with a sliding bar shows the same γ as a force per
metre of edge (a soap film has two surfaces, so F = 2γL), with its units
N/m = J/m². Bars compare water (≈ 73 mN/m at 20 °C) with ethanol beside a
spinning hydrogen-bonded water pair. Finally the "pulled inward" arrow is
offered as a first picture, the "elastic skin" idea is crossed out, and the
stretched slab relaxes back: a surface costs energy, so a liquid keeps it small.
"""

from inspect import signature

from scipy.optimize import linear_sum_assignment

from manim_scenes.common import *
from manim_scenes.kit_g import *

CUTOFF = signature(pm.neighbour_counts).parameters["cutoff"].default
START = pm.liquid_snapshot(nx=6, ny=4, nz=5).copy()        # the slab at rest
WIDE = pm.liquid_snapshot(nx=8, ny=3, nz=5).copy()         # the same number of molecules, stretched surface
WIDE[:, 1] += START[:, 1].max() - WIDE[:, 1].max()          # the surface stays at the same height
_, _ORDER = linear_sum_assignment(((START[:, None, :] - WIDE[None, :, :]) ** 2).sum(-1))
WIDE = WIDE[_ORDER]                                         # each molecule's place in the stretched slab
COUNTS = pm.neighbour_counts(START)
TOP_START = START[:, 1] > START[:, 1].max() - 0.45
TOP_WIDE = WIDE[:, 1] > WIDE[:, 1].max() - 0.45
PROMOTED = np.nonzero(TOP_WIDE & ~TOP_START)[0]            # pulled up from inside into the surface


def _pick_inner() -> int:
    """The best-surrounded molecule a layer below the middle, left of centre."""
    ys = np.unique(np.round(START[:, 1], 0))
    score = [(-COUNTS[i], abs(START[i, 0] + 0.9) + abs(START[i, 2]) + abs(START[i, 1] - ys[1]), i)
             for i in range(len(START)) if not TOP_START[i]]
    return min(score)[2]


def _pick_surface() -> int:
    top = np.nonzero(TOP_START)[0]
    return int(top[np.argmin(np.abs(START[top, 0] - 1.0) + np.abs(START[top, 2]))])


INNER, SURFACE = _pick_inner(), _pick_surface()


def neighbours(i: int) -> np.ndarray:
    d = np.linalg.norm(START - START[i], axis=1)
    d[i] = np.inf
    return np.nonzero(d < CUTOFF)[0]


NB_INNER, NB_SURFACE = neighbours(INNER), neighbours(SURFACE)
assert len(NB_INNER) == COUNTS[INNER] and len(NB_SURFACE) == COUNTS[SURFACE]


class Scene25SurfaceEnergy(Scene):
    def construct(self) -> None:
        play_scene(self)


class Slab:
    """Molecule centres between the rest and stretched snapshots (``morph`` 0..1), gently jiggling."""

    def __init__(self, stage: Stage) -> None:
        self.stage, self.morph = stage, Knob(0.0)
        rng = np.random.default_rng(cfg.SEED + 25)
        self.phase = rng.uniform(0, 2 * np.pi, START.shape)
        self.omega = rng.uniform(1.6, 3.2, START.shape)
        self._key, self._pts = None, START

    def points(self) -> np.ndarray:
        key = (self.stage.clock, self.morph.value)
        if key != self._key:
            m = smooth(float(np.clip(self.morph.value, 0, 1)))
            wobble = 0.045 * np.sin(self.stage.clock * self.omega + self.phase)
            self._pts = START + (WIDE - START) * m + wobble
            self._key = key
        return self._pts

    def at(self, i: int) -> Callable[[], np.ndarray]:
        return lambda: self.points()[i]

    def half_width(self) -> float:
        m = smooth(float(np.clip(self.morph.value, 0, 1)))
        return float(np.abs(START[:, 0]).max() * (1 - m) + np.abs(WIDE[:, 0]).max() * m) + 0.45

    def bottom(self) -> float:
        m = smooth(float(np.clip(self.morph.value, 0, 1)))
        return float(START[:, 1].min() * (1 - m) + WIDE[:, 1].min() * m) - 0.45


class PivotDots(Dots):
    """The dots on one side (in depth) of a pivot point, so they hide or cover the pivot ball correctly."""

    def __init__(self, points, pivot, color: str, front: bool, radius: float) -> None:
        super().__init__(points, color, radius=radius)
        self.all_points, self.pivot, self.front = points, pivot, front

    def place(self, stage, R, visibility):
        pts = np.asarray(self.all_points(), dtype=float)
        z = (pts @ R.T)[:, 2]
        zp = float((R @ self.pivot())[2])
        self.points = pts[z >= zp] if self.front else pts[z < zp]
        super().place(stage, R, visibility)
        self.depth_key = float(stage.project(self.pivot()[None, :], R)[2][0]) + (0.02 if self.front else -0.02)


def drop_stage() -> tuple[Stage, Knob]:
    """A translucent water bead on a floor, molecules inside, wobbling into shape."""
    stage = Stage((0.0, -0.7, 0.0), zoom=1.05, yaw=-0.3, pitch=0.3, sway=0.04)
    verts, quads = cube_mesh(9)
    unit = verts / np.linalg.norm(verts, axis=1, keepdims=True)
    wob = Knob(0.32)
    radius = 1.75

    def shape() -> np.ndarray:
        w = wob.value * np.cos(6.0 * stage.clock)
        k = np.array([1 + 0.5 * w, 0.9 * (1 - w), 1 + 0.5 * w])
        p = unit * radius * k
        p[:, 1] += radius * 0.9 * (1 - w) - 0.05
        return p

    back = ShadedMesh(shape, quads, cfg.LIQUID_EDGE, opacity=0.34, side="back", key=lambda: -100, edge_opacity=0.0)
    front = ShadedMesh(shape, quads, cfg.LIQUID_EDGE, opacity=0.26, side="front", key=lambda: 100, edge_opacity=0.08,
                       gloss=0.9)
    rng = np.random.default_rng(cfg.SEED + 251)
    inside = []
    while len(inside) < 46:
        p = rng.uniform(-1, 1, 3)
        if np.linalg.norm(p) < 0.82 and all(np.linalg.norm(p - q) > 0.33 for q in inside):
            inside.append(p)
    inside = np.array(inside)
    phase = rng.uniform(0, 2 * np.pi, inside.shape)

    def molecules() -> np.ndarray:
        w = wob.value * np.cos(6.0 * stage.clock)
        k = np.array([1 + 0.5 * w, 0.9 * (1 - w), 1 + 0.5 * w])
        p = (inside + 0.03 * np.sin(2.4 * stage.clock + phase)) * radius * k
        p[:, 1] += radius * 0.9 * (1 - w) - 0.05
        return p

    floor = Grid((0, -0.06, 0), (1, 0, 0), (0, 0, 1), (-3.2, 3.2), (-3.2, 3.2), step=0.4, major=0, color=cfg.GRID,
                 opacity=0.25)
    shadow = Disc(np.array([0.0, -0.05, 0.0]), 1.9, "#000000", normal=(0, 1, 0), opacity=0.35, soft=True, bias=-9e3)
    stage.add_body(floor, shadow, back, SortedDots(molecules, mu.mix(cfg.LIQUID, cfg.WHITE, 0.3), radius=0.17, key=0),
                   front)
    return stage, wob


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "25", TITLES["25"])

    # --- 0. A drop pulls itself into a bead. Look at the molecules ------------------------------------------------------
    drop, wob = drop_stage()
    show(scene, drop, 1.0)
    scene.play(wob.to(drop, 0.02, run_time=2.6, rate_func=smooth), *drop.turn(yaw=0.1), run_time=2.6)

    stage = Stage((-2.5, -0.55, 0), zoom=0.9, yaw=-0.5, pitch=0.42, sway=0.05)
    slab = Slab(stage)
    hw = slab.half_width
    top_y = float(START[:, 1].max()) + 0.42
    depth_z = float(np.abs(START[:, 2]).max()) + 0.45
    surface = Face(lambda: [np.array([-hw(), top_y, -depth_z]), np.array([hw(), top_y, -depth_z]),
                            np.array([hw(), top_y, depth_z]), np.array([-hw(), top_y, depth_z])],
                   cfg.LIQUID_EDGE, opacity=0.1, edge_opacity=0.55)
    surface.bias = 60.0
    sides = [Face(lambda s=s: [np.array([s * hw(), slab.bottom(), -depth_z]), np.array([s * hw(), top_y, -depth_z]),
                               np.array([s * hw(), top_y, depth_z]), np.array([s * hw(), slab.bottom(), depth_z])],
                  cfg.LIQUID, opacity=0.05, edge_opacity=0.12) for s in (-1, 1)]
    for f in sides:
        f.bias = -600.0
    crowd = SortedDots(slab.points, mu.mix(cfg.LIQUID, cfg.WHITE, 0.3), radius=0.3, key=-500.0)
    stage.add_body(*sides, crowd, surface)
    note = txt("schematic snapshot", cfg.FONT["tiny"], cfg.MUTED).move_to([-2.5, -3.75, 0])
    scene.add(stage)
    stage.presence = 0.0
    scene.play(drop.zoom_to(3.2), drop.fade(drop, 0.0), stage.fade(stage, 1.0), FadeIn(note), run_time=1.6)
    drop.clear_updaters()
    scene.remove(drop)
    fill_to(scene, t, 1, *stage.turn(yaw=-0.38))

    # --- 1. Deep inside: neighbours on every side -------------------------------------------------------------------------
    beat(scene, t, 1)
    inner = Ball(slab.at(INNER), 0.36, cfg.GOLD)
    inner_halo = Halo(inner, cfg.GOLD, reach=2.4, peak=0.22)
    inner_nb = [PivotDots(lambda: slab.points()[NB_INNER], slab.at(INNER), cfg.LIQUID_EDGE, front, 0.31)
                for front in (False, True)]
    inner_bonds = [Segment(slab.at(INNER), slab.at(j), cfg.ATTRACT, width=4.5, opacity=0.95) for j in NB_INNER]
    inner_zone = glass_sphere(stage, slab.at(INNER), CUTOFF, cfg.ATTRACT, presence=0.0, fill_opacity=0.07)
    for body in (inner, inner_halo, *inner_nb, *inner_bonds):
        body.presence = 0.0
    stage.add_body(inner_halo, inner, *inner_nb, *inner_bonds)

    def row(name: str, count: int) -> VGroup:
        icon = bead(ORIGIN, cfg.GOLD, 0.17, glow=1.0)
        words = VGroup(txt(name, cfg.FONT["label"], cfg.WHITE),
                       txt(f"{count} neighbours", cfg.FONT["small"], cfg.ATTRACT)).arrange(DOWN, buff=0.12,
                                                                                          aligned_edge=LEFT)
        group = VGroup(icon, words).arrange(RIGHT, buff=0.35)
        group.icon, group.words = icon, words
        return group

    row_in = row("inside", int(COUNTS[INNER])).move_to([4.7, 0.9, 0])
    scene.play(set_attr(stage, crowd, "alpha", 0.32), stage.fade(inner, 1.0), stage.fade(inner_halo, 1.0),
               *[stage.fade(d, 1.0) for d in inner_nb], run_time=1.2)
    scene.play(LaggedStart(*[stage.fade(b, 1.0, run_time=0.5) for b in inner_bonds], lag_ratio=0.12),
               *fade_all(stage, inner_zone.parts, 1.0, run_time=2.2), FadeIn(row_in, shift=LEFT * 0.2), run_time=2.2)
    scene.play(*[stage.fade(b, 0.45, rate_func=there_and_back) for b in inner_bonds], *stage.turn(yaw=0.15),
               run_time=2.6)
    fill_to(scene, t, 2, *stage.turn(yaw=0.4))

    # --- 2. At the surface: nothing above, fewer attractions, higher energy ------------------------------------------------
    beat(scene, t, 2)
    surf = Ball(slab.at(SURFACE), 0.36, cfg.GOLD)
    surf_halo = Halo(surf, cfg.GOLD, reach=2.4, peak=0.22)
    surf_nb = [PivotDots(lambda: slab.points()[NB_SURFACE], slab.at(SURFACE), cfg.LIQUID_EDGE, front, 0.31)
               for front in (False, True)]
    surf_bonds = [Segment(slab.at(SURFACE), slab.at(j), cfg.ATTRACT, width=4.5, opacity=0.95) for j in NB_SURFACE]
    surf_zone = glass_sphere(stage, slab.at(SURFACE), CUTOFF, cfg.ATTRACT, presence=0.0, fill_opacity=0.07)
    for body in (surf, surf_halo, *surf_nb, *surf_bonds):
        body.presence = 0.0
    stage.add_body(surf_halo, surf, *surf_nb, *surf_bonds)
    empty = Tag(txt("empty above", cfg.FONT["small"], cfg.WHITE), lambda: slab.points()[SURFACE] + np.array([0, 1.75, 0]))
    empty.presence = 0.0
    stage.add_overlay(empty)
    row_s = row("surface", int(COUNTS[SURFACE])).move_to([4.7, -0.6, 0])
    row_s.align_to(row_in, LEFT)
    dim_inner = [stage.fade(b, 0.25) for b in inner_bonds] + fade_all(stage, inner_zone.parts, 0.0) + \
                [stage.fade(d, 0.0) for d in inner_nb]
    scene.play(*dim_inner, stage.fade(surf, 1.0), stage.fade(surf_halo, 1.0), *[stage.fade(d, 1.0) for d in surf_nb],
               *stage.turn(yaw=-0.2, pitch=0.3), run_time=1.4)
    scene.play(LaggedStart(*[stage.fade(b, 1.0, run_time=0.5) for b in surf_bonds], lag_ratio=0.14),
               *fade_all(stage, surf_zone.parts, 1.0, run_time=2.0), FadeIn(row_s, shift=LEFT * 0.2), run_time=2.0)
    scene.play(stage.fade(empty, 1.0), run_time=0.8)

    # The two counts become rungs of an energy ladder (fewer attractions: higher energy).
    k = 0.42
    y_in = -2.15
    y_s = y_in + k * (COUNTS[INNER] - COUNTS[SURFACE])
    axis = Arrow([2.75, -2.75, 0], [2.75, 1.55, 0], buff=0, stroke_color=cfg.MUTED, stroke_width=4,
                 max_tip_length_to_length_ratio=0.06)
    axis_label = txt("energy", cfg.FONT["small"], cfg.GOLD).next_to(axis, UP, buff=0.12)
    rung_in = Line([3.05, y_in, 0], [4.05, y_in, 0], stroke_color=cfg.LIQUID_EDGE, stroke_width=5)
    rung_s = Line([3.05, y_s, 0], [4.05, y_s, 0], stroke_color=cfg.LIQUID_EDGE, stroke_width=5)
    scene.play(GrowArrow(axis), FadeIn(axis_label), Create(rung_in), Create(rung_s),
               row_in.icon.animate.move_to(rung_in.get_center() + UP * 0.2),
               row_s.icon.animate.move_to(rung_s.get_center() + UP * 0.2),
               FadeOut(row_in.words), FadeOut(row_s.words), run_time=1.8)
    row_in.words.next_to(rung_in, RIGHT, buff=0.3)       # re-placed while hidden, so the rows never cross
    row_s.words.next_to(rung_s, RIGHT, buff=0.3)
    scene.play(FadeIn(row_in.words, shift=LEFT * 0.1), FadeIn(row_s.words, shift=LEFT * 0.1), run_time=0.5)
    rise = VecArrow(rung_in.get_center() + UP * 0.45, rung_s.get_center() + DOWN * 0.12, cfg.GOLD, width=0.08,
                    tip_len=0.22, live=False)
    scene.play(rise.grow_in(run_time=1.0), Indicate(row_s.icon, color=cfg.GOLD, scale_factor=1.3), run_time=1.0)
    fill_to(scene, t, 3, *stage.turn(yaw=-0.05, pitch=0.38))

    # --- 3. More surface: molecules pulled up from inside. Stretching takes work ---------------------------------------------
    beat(scene, t, 3)
    gold = SortedDots(lambda: slab.points()[PROMOTED], cfg.GOLD, radius=0.32, key=-400.0)
    gold.presence = 0.0
    stage.add_body(gold)
    pulls = [Vector(lambda s=s: np.array([s * (hw() + 0.15), top_y - 0.35, 0.0]),
                    lambda s=s: np.array([s * (hw() + 1.45), top_y - 0.35, 0.0]), cfg.GOLD, width=0.12, tip=0.32)
             for s in (-1, 1)]
    for p in pulls:
        p.presence = 0.0
    stage.add_overlay(*pulls)
    work = Tag(txt("work", cfg.FONT["label"], cfg.GOLD), lambda: np.array([-(hw() + 0.9), top_y + 0.35, 0.0]), UP * 0.3)
    work.presence = 0.0
    stage.add_overlay(work)
    away = [stage.fade(b, 0.0) for b in (*inner_bonds, *surf_bonds, *surf_nb, inner_halo, surf_halo)] + \
        fade_all(stage, surf_zone.parts, 0.0) + [stage.fade(empty, 0.0)]
    scene.play(*away, set_attr(stage, crowd, "alpha", 0.6), stage.glide([-2.0, -0.5, 0]), stage.zoom_to(0.74),
               run_time=1.2)
    scene.play(*[stage.fade(p, 1.0) for p in pulls], stage.fade(work, 1.0), stage.fade(gold, 1.0), run_time=0.9)
    hops = VGroup(*[bead(rung_in.get_center() + UP * 0.2, cfg.GOLD, 0.1, glow=1.0) for _ in range(5)])
    paths = [Line(rung_in.get_center() + UP * 0.2 + RIGHT * (0.3 * (k2 - 2) / 2), rung_s.get_center() + UP * 0.2)
             for k2 in range(5)]
    scene.play(slab.morph.to(stage, 1.0, run_time=5.0, rate_func=linear),
               LaggedStart(*[Succession(FadeIn(h, run_time=0.2), MoveAlongPath(h, p, run_time=1.0),
                                        FadeOut(h, run_time=0.3)) for h, p in zip(hops, paths)], lag_ratio=0.5),
               run_time=5.0)
    scene.remove(hops)
    takes = txt("stretching takes work", cfg.FONT["label"], cfg.GOLD).move_to([-2.0, 2.65, 0])
    scene.play(FadeIn(takes, shift=DOWN * 0.15), run_time=0.8)
    fill_to(scene, t, 4, *stage.turn(yaw=0.12))

    # --- 4. Work per extra square metre: gamma. dW = gamma dA ------------------------------------------------------------------
    beat(scene, t, 4)
    w0 = float(np.abs(START[:, 0]).max()) + 0.45
    strips = [Face(lambda s=s: [np.array([s * w0, top_y + 0.01, -depth_z]), np.array([s * hw(), top_y + 0.01, -depth_z]),
                                np.array([s * hw(), top_y + 0.01, depth_z]), np.array([s * w0, top_y + 0.01, depth_z])],
                   cfg.GOLD, opacity=0.32, edge_opacity=0.9) for s in (-1, 1)]
    for f in strips:
        f.presence = 0.0
        f.bias = 70.0
    stage.add_body(*strips)
    da = Tag(eq("dA", cfg.FONT["label"], cfg.LIQUID_EDGE), lambda: np.array([hw() - 0.5, top_y, depth_z + 0.2]), DOWN * 0.45)
    da.presence = 0.0
    stage.add_overlay(da)
    ladder = VGroup(axis, axis_label, rung_in, rung_s, row_in, row_s, rise)
    scene.play(FadeOut(ladder), FadeOut(takes), *[stage.fade(p, 0.0) for p in pulls], stage.fade(work, 0.0),
               *[stage.fade(f, 1.0) for f in strips], stage.fade(da, 1.0), stage.glide([-2.6, -0.6, 0]), run_time=1.4)
    per = VGroup(eq(r"\gamma", cfg.FONT["section"], cfg.GOLD), txt("= work per m²", cfg.FONT["label"], cfg.WHITE),
                 ).arrange(RIGHT, buff=0.22)
    per2 = txt("of new surface", cfg.FONT["label"], cfg.WHITE).next_to(per, DOWN, buff=0.2).align_to(per[1], LEFT)
    defn = VGroup(per, per2).move_to([4.5, 1.6, 0])
    law = paint(eq(["dW", "=", r"\gamma", r"\,dA"], 80), {2: cfg.GOLD, 3: cfg.LIQUID_EDGE}).move_to([4.5, -0.6, 0])
    frame = glow_frame(law, cfg.GOLD, buff=0.3)
    scene.play(FadeIn(defn, shift=LEFT * 0.2), run_time=1.2)
    scene.play(*[stage.fade(f, 0.45, rate_func=there_and_back) for f in strips], run_time=1.4)
    scene.play(Write(law), run_time=1.6)
    scene.play(Create(frame), Indicate(law[2], color=cfg.GOLD, scale_factor=1.3), run_time=1.2)
    fill_to(scene, t, 5, *stage.turn(yaw=-0.25))

    # --- 5. The same gamma as a force per metre of edge. N/m = J/m^2 ----------------------------------------------------------
    beat(scene, t, 5)
    rig = Stage((-2.7, -0.55, 0), zoom=1.05, yaw=-0.42, pitch=0.16, sway=0.04)
    slide = Knob(0.2)
    left_x, h = -2.4, 1.25
    rails = [Curve(np.array([[left_x, s * h, 0.0], [2.3, s * h, 0.0]]), cfg.STEEL, width=7, glow=False) for s in (-1, 1)]
    back_bar = Curve(np.array([[left_x, -h, 0.0], [left_x, h, 0.0]]), cfg.STEEL, width=9, glow=False)
    bar = Block(lambda: np.array([slide.value, 0.0, 0.0]), (0.14, 2 * h + 0.5, 0.14), cfg.STEEL)
    films = [Face(lambda s=s: [np.array([left_x, -h, s * 0.06]), np.array([slide.value, -h, s * 0.06]),
                               np.array([slide.value, h, s * 0.06]), np.array([left_x, h, s * 0.06])],
                  cfg.LIQUID_EDGE, opacity=0.2, edge_opacity=0.35) for s in (-1, 1)]
    tugs = [Vector(lambda y=y: np.array([slide.value - 0.12, y, 0.0]), lambda y=y: np.array([slide.value - 0.7, y, 0.0]),
                   cfg.GOLD, width=0.06, tip=0.18) for y in np.linspace(-0.95, 0.95, 5)]
    force = Vector(lambda: np.array([slide.value + 0.14, -0.3, 0.0]), lambda: np.array([slide.value + 1.6, -0.3, 0.0]),
                   cfg.ORANGE, width=0.12, tip=0.34)
    f_tag = Tag(eq("F", cfg.FONT["section"], cfg.ORANGE), lambda: np.array([slide.value + 1.0, -0.3, 0.0]), DOWN * 0.45)
    l_tag = Tag(eq("L", cfg.FONT["section"], cfg.WHITE), lambda: np.array([slide.value + 0.15, 0.75, 0.0]), RIGHT * 0.4)
    for item in (*tugs, force, f_tag, l_tag):
        item.presence = 0.0
    rig.add_body(*films, *rails, back_bar, bar)
    rig.add_overlay(*tugs, force, f_tag, l_tag)
    rig.presence = 0.0
    scene.add(rig)
    scene.play(FadeOut(VGroup(defn, frame)), FadeOut(note), run_time=0.4)
    scene.play(stage.fade(stage, 0.0), law.animate.scale(0.6).move_to([4.6, 3.25, 0]),
               *[stage.fade(f, 0.0) for f in strips], stage.fade(da, 0.0), rig.fade(rig, 1.0), run_time=0.8)
    scene.play(slide.to(rig, 1.25, run_time=2.4), rig.fade(force, 1.0), rig.fade(f_tag, 1.0), *rig.turn(yaw=-0.25),
               run_time=2.4)
    scene.play(*[rig.fade(v, 1.0) for v in tugs], rig.fade(l_tag, 1.0), run_time=1.0)
    gam = paint(eq([r"\gamma", "=", r"{F", r"\over", r"2L}"], 72), {0: cfg.GOLD, 2: cfg.ORANGE}).move_to([4.6, 1.3, 0])
    film_note = VGroup(txt("soap film · two interfaces", cfg.FONT["tiny"], cfg.MUTED),
                       paint(eq(["F", "=", r"2\gamma", "L"], cfg.FONT["small"]), {0: cfg.ORANGE, 2: cfg.GOLD}))
    film_note.arrange(DOWN, buff=0.18).move_to([4.6, -0.6, 0])
    units = eq(r"\mathrm{N\,m^{-1}} = \mathrm{J\,m^{-2}}", cfg.FONT["body"]).move_to([4.6, -2.15, 0])
    why = eq(r"(\mathrm{J} = \mathrm{N\,m})", cfg.FONT["tiny"], cfg.MUTED).next_to(units, DOWN, buff=0.22)
    scene.play(Write(gam), run_time=1.4)
    scene.play(FadeIn(film_note, shift=UP * 0.15), *rig.turn(yaw=-0.75, pitch=0.3), run_time=2.0)
    scene.play(Write(units), run_time=1.4)
    scene.play(FadeIn(why), slide.to(rig, 1.55, run_time=1.6), run_time=1.6)
    fill_to(scene, t, 6, *rig.turn(yaw=-0.45, pitch=0.2))

    # --- 6. Water: about 73 mN/m at 20 C, thanks to hydrogen bonds -------------------------------------------------------------
    beat(scene, t, 6)
    hide(scene, rig, 0.9, FadeOut(VGroup(gam, film_note, units, why)))
    water = pm.SURFACE_TENSION_20C["water"]
    ethanol = pm.SURFACE_TENSION_20C["ethanol"]
    chart = bar_chart([water, ethanol], ["water", "ethanol"], [cfg.LIQUID_EDGE, cfg.MUTED], at=[-3.0, -1.0, 0], width=5.2,
                      height=3.6, top=80, value_labels=[f"≈ {fx(water, 0)}", f"≈ {fx(ethanol, 0)}"], bar_width=1.5,
                      name_size=cfg.FONT["label"])
    for tag in chart.tops:
        tag.scale(cfg.FONT["label"] / cfg.FONT["tiny"]).next_to(tag, ORIGIN)
    for tag, bar_ in zip(chart.tops, chart.bars):
        tag.next_to(bar_, UP, buff=0.16)
    unit = txt("mN/m at 20 °C", cfg.FONT["small"], cfg.MUTED).next_to(chart, UP, buff=0.35)
    pair = Stage((3.9, -0.9, 0), zoom=1.6, yaw=0.0, pitch=0.2, sway=0.04, spin=0.35)
    w1 = water_atoms()
    donor_h = w1[1][1]
    acceptor = donor_h + mu.unit(donor_h) * 1.85 * 0.62           # O...H about 1.85 angstrom
    pose = mu.rotation_between([0, 1, 0], -mu.unit(donor_h)) @ mu.rotation_y(0.9)
    first = molecule(pair, w1, [(0, 1), (0, 2)], centre=np.array([-0.35, 0.35, 0.0]))
    second = molecule(pair, [(e, pose @ p) for e, p in water_atoms()], [(0, 1), (0, 2)],
                      centre=np.array([-0.35, 0.35, 0.0]) + acceptor)
    link = Segment(first.balls[1].where, second.balls[0].where, cfg.ATTRACT, width=5, opacity=0.95, dashed=True)
    pair.add_body(link)
    hb = chip("hydrogen bonds", cfg.ATTRACT, cfg.FONT["label"]).move_to([3.9, 1.65, 0])
    scene.play(Create(chart.base), FadeIn(unit), run_time=0.7)
    scene.play(GrowFromEdge(chart.bars[0], DOWN), FadeIn(chart.names[0]), run_time=1.2)
    scene.play(FadeIn(chart.tops[0], scale=1.2), run_time=0.6)
    scene.play(GrowFromEdge(chart.bars[1], DOWN), FadeIn(chart.names[1]), FadeIn(chart.tops[1]), run_time=1.1)
    show(scene, pair, 1.0, FadeIn(hb, shift=DOWN * 0.15))
    scene.play(Indicate(chart.tops[0], color=cfg.GOLD, scale_factor=1.2), *[pair.fade(link, 0.35, rate_func=there_and_back)],
               run_time=1.4)
    fill_to(scene, t, 7)

    # --- 7. "Pulled inward" is a first picture; not an elastic skin: a surface costs energy -------------------------------------
    beat(scene, t, 7)
    hide(scene, pair, 0.9, FadeOut(VGroup(chart, unit, hb)))
    for f in strips:
        f.presence = 0.0
    da.presence = 0.0
    inward = Vector(lambda: slab.points()[SURFACE] + np.array([0, 0.45, 0]),
                    lambda: slab.points()[SURFACE] + np.array([0, -1.05, 0]), cfg.ATTRACT, width=0.12, tip=0.3)
    inward.presence = 0.0
    stage.add_overlay(inward)
    scene.play(stage.fade(stage, 1.0), stage.fade(surf_halo, 1.0), set_attr(stage, crowd, "alpha", 0.55),
               FadeOut(law), stage.glide([-2.4, -0.6, 0]), stage.zoom_to(0.8), run_time=1.2)
    first_pic = VGroup(txt("pulled inward?", cfg.FONT["label"], cfg.ATTRACT),
                       txt("a useful first picture", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.14)
    first_pic.move_to([4.5, 2.2, 0])
    scene.play(stage.fade(inward, 1.0), FadeIn(first_pic, shift=LEFT * 0.2), run_time=1.2)
    scene.play(*[stage.fade(inward, 0.4, rate_func=there_and_back)], *stage.turn(yaw=-0.3), run_time=2.0)
    skin = txt("an elastic skin", cfg.FONT["label"], cfg.WHITE).move_to([4.5, 0.65, 0])
    cross = cross_mark(0.26).next_to(skin, LEFT, buff=0.3)
    line = strike(skin, cfg.RED, width=6)
    scene.play(FadeIn(skin, shift=LEFT * 0.2), run_time=0.8)
    scene.play(Create(line), FadeIn(cross, scale=0.6), skin.animate.set_opacity(0.55), run_time=1.0)
    energy = result_label("a surface costs energy", cfg.GOLD, cfg.FONT["label"]).move_to([4.4, -0.95, 0])
    small = txt("so a liquid keeps it small", cfg.FONT["small"], cfg.WHITE).next_to(energy, DOWN, buff=0.3)
    scene.play(FadeIn(energy, scale=0.95), stage.fade(inward, 0.0), run_time=1.2)
    scene.play(slab.morph.to(stage, 0.0, run_time=4.2, rate_func=linear), stage.fade(gold, 0.0, run_time=4.2),
               stage.glide([-2.6, -0.6, 0]), stage.zoom_to(0.9), FadeIn(small, run_time=1.2), run_time=4.2)
    box = glow_frame(VGroup(energy, small), cfg.GOLD, buff=0.25)
    scene.play(Create(box), run_time=1.0)
    finish(scene, t, stage)
