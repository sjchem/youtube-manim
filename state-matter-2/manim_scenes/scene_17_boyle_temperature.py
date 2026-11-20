"""Scene 17 — the Boyle temperature. The compressibility factor of a van der
Waals fluid (``pm.z_reduced``) is built as a 3D surface over reduced pressure
and reduced temperature on a slowly turning stage, each patch coloured green
below Z = 1, white at 1 and red above (``kit_d.z_color``), with a translucent
purple Z = 1 plane. A gold slice at one temperature runs across the surface
and is mirrored live in a 2D inset of Z against pressure.

Near the critical temperature the slice dips deep. Warming it, the dip gets
shallower; at T_B = 27/8 T_c (``pm.VDW_BOYLE_REDUCED``, the van der Waals
Boyle temperature) the slice leaves Z = 1 flat; above it, Z rises from the
start. Measured Boyle temperatures (``pm.BOYLE_T``) are marked on a kelvin
scale with room temperature: nitrogen about 327 K, helium about 23 K. Finally
the warning: on the Boyle slice, at a moderate pressure, the attraction and size
terms are both large — two long arrows that nearly cancel (12 % and 11 %).
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d
from manim_scenes.kit_d import at_word, z_color

PR_MAX = 6.0
TR_LOW, TR_HIGH = 1.05, 6.0
T_BOYLE = pm.VDW_BOYLE_REDUCED
STAGE_AT = (-3.0, 0.15, 0.0)
INSET_AT = [4.55, -0.15, 0]


class Scene17BoyleTemperature(Scene):
    def construct(self) -> None:
        play_scene(self)


def X(pr: float) -> float:
    return pr / PR_MAX * 4.8 - 2.4


def Dz(tr: float) -> float:
    return 1.7 - (tr - TR_LOW) / (TR_HIGH - TR_LOW) * 3.4     # hotter slices recede into the screen


def Y(z: float) -> float:
    return (z - 1.0) * 3.2


def point(pr: float, tr: float) -> np.ndarray:
    return np.array([X(pr), Y(pm.z_reduced(pr, tr)), Dz(tr)])


def terms_reduced(pr: float, tr: float) -> tuple[float, float]:
    """(size push, attraction pull) of the reduced van der Waals fluid at (pr, tr): a = 3, b = 1/3, R = 8/3."""
    z = pm.z_reduced(pr, tr)
    v = z * (8 / 3) * tr / pr
    return (1 / 3) / (v - 1 / 3), 3 / ((8 / 3) * tr * v)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "17", TITLES["17"])
    stage = Stage(STAGE_AT, zoom=1.2, yaw=-0.55, pitch=0.42, spin=0.0, sway=0.03)

    # --- 0. The surface Z(P, T) --------------------------------------------------------------------------------------
    prs = np.linspace(0.0, PR_MAX, 15)
    trs = np.linspace(TR_LOW, TR_HIGH, 12)
    faces = surface_faces(point, prs, trs, lambda p, q: z_color(pm.z_reduced(p, q), low=0.5, high=0.25), opacity=0.55,
                          edge_opacity=0.25)
    for f in faces:
        f.presence = 0.0
    stage.add_body(*faces)
    plane = Face([np.array([X(0), 0, Dz(TR_LOW)]), np.array([X(PR_MAX), 0, Dz(TR_LOW)]), np.array([X(PR_MAX), 0, Dz(TR_HIGH)]),
                  np.array([X(0), 0, Dz(TR_HIGH)])], cfg.LIMIT, opacity=0.1, edge_opacity=0.7)
    plane.presence = 0.0
    stage.add_body(plane)
    origin = np.array([X(0), Y(0.35), Dz(TR_LOW)])
    triad = axis_triad(stage, origin, [origin + [5.2, 0, 0], origin + [0, 3.4, 0], origin + [0, 0, -3.9]],
                       [cfg.PRESSURE, cfg.GOLD, cfg.TEMPERATURE], ["P", "Z", "T"], width=3.0, label_size=cfg.FONT["section"],
                       offsets=[(0.1, 0.55, 0), (0, 0, 0), (-0.55, 0.2, 0)])
    triad.segments[2].bias = -500.0  # temperature axis belongs behind the surface
    show(scene, stage, 1.0)
    at_word(scene, t, 0, "surface", lead=0.4)
    # The staggered faces share one live stage; keep its projection updating
    # throughout the reveal so the surface fades in instead of popping at the end.
    scene.play(LaggedStart(*[stage.fade(f, 1.0) for f in faces], lag_ratio=0.012,
                           suspend_mobject_updating=False), stage.turn(yaw=-0.4)[0], run_time=3.0)
    play_in(scene, t, 1, stage.fade(plane, 1.0), stage.set_spin(0.012), run_time=1.6)

    # --- 1. Near T_c the slice dips deep -------------------------------------------------------------------------------
    beat(scene, t, 1)
    tr = Knob(1.1)
    samples = np.linspace(0.02, PR_MAX, 48)
    slice_curve = Curve(lambda: np.array([point(p, tr.value) + np.array([0, 0.03, 0]) for p in samples]), cfg.GOLD, width=6)
    slice_curve.presence = 0.0
    stage.add_body(slice_curve)
    slice_curve.bias = 50.0
    axes = plot_axes((0, PR_MAX), (0.3, 1.2), x_length=4.6, y_length=3.8, at=INSET_AT, x_label="P", y_label="Z",
                     x_color=cfg.PRESSURE, y_color=cfg.GOLD, y_ticks=(0.6, 1.0))
    one = DashedLine(axes.c2p(0, 1), axes.c2p(PR_MAX, 1), stroke_color=cfg.LIMIT, stroke_width=3.5, dash_length=0.12)
    inset = live(VGroup(), lambda: polyline([axes.c2p(p, pm.z_reduced(p, tr.value)) for p in samples], cfg.GOLD, width=6))
    t_read = live(VGroup(), lambda: VGroup(eq("T =", cfg.FONT["label"], cfg.TEMPERATURE),
                                           txt(f"{fx(tr.value, 2)} T", cfg.FONT["section"], cfg.WHITE),
                                           eq("_c", cfg.FONT["label"], cfg.WHITE))
                  .arrange(RIGHT, buff=0.12, aligned_edge=DOWN).move_to([INSET_AT[0], 2.55, 0]))
    scene.add(inset, t_read)
    scene.play(stage.fade(slice_curve, 1.0), Create(axes), Create(one), FadeIn(inset), FadeIn(t_read), run_time=1.6)
    at_word(scene, t, 1, "deep", lead=0.3)
    dip = txt("attraction has time", cfg.FONT["small"], cfg.ATTRACT).move_to(axes.c2p(3.4, 0.38))
    play_in(scene, t, 2, FadeIn(dip, shift=UP * 0.1), run_time=1.0)

    # --- 2. Warm it: the dip gets shallower ------------------------------------------------------------------------------
    beat(scene, t, 2)
    play_in(scene, t, 3, tr.to(inset, 2.2, rate_func=smooth), FadeOut(dip), run_time=3.8)

    # --- 3. The Boyle temperature: flat at Z = 1 ---------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(tr.to(inset, T_BOYLE, rate_func=smooth), run_time=3.4)
    at_word(scene, t, 3, "flat", lead=0.3)
    tangent = Line(axes.c2p(0, 1), axes.c2p(2.4, 1), stroke_color=cfg.WHITE, stroke_width=8, stroke_opacity=0.6)
    scene.play(Create(tangent), Indicate(t_read, color=cfg.GOLD, scale_factor=1.06), run_time=1.2)
    at_word(scene, t, 3, "Boyle", lead=0.3)
    boyle = result_label("Boyle temperature", cfg.LIMIT, cfg.FONT["label"]).move_to([INSET_AT[0], -2.75, 0])
    tb = eq(r"T_B=\tfrac{27}{8}\,T_c", cfg.FONT["label"], cfg.WHITE).next_to(boyle, DOWN, buff=0.2)
    play_in(scene, t, 4, FadeIn(boyle, shift=UP * 0.1), FadeIn(tb, shift=UP * 0.1), run_time=1.2)

    # --- 4. Above it, size wins from the start ----------------------------------------------------------------------------
    beat(scene, t, 4)
    play_in(scene, t, 5, tr.to(inset, 4.8, rate_func=smooth), FadeOut(tangent), run_time=3.6)

    # --- 5. Measured Boyle temperatures ---------------------------------------------------------------------------------------
    beat(scene, t, 5)
    inset.clear_updaters()
    t_read.clear_updaters()
    scene.play(FadeOut(VGroup(axes, one, inset, t_read, boyle, tb)), tr.to(stage, T_BOYLE), run_time=1.0)
    line = Line([1.7, -0.6, 0], [7.2, -0.6, 0], stroke_color=cfg.MUTED, stroke_width=4)

    def kx(kelvin: float) -> float:
        return 1.7 + kelvin / 400 * 5.5

    ticks = VGroup(*[VGroup(Line([kx(k), -0.7, 0], [kx(k), -0.5, 0], stroke_color=cfg.MUTED, stroke_width=3),
                            txt(str(k), cfg.FONT["tiny"], cfg.MUTED).move_to([kx(k), -1.0, 0])) for k in (0, 100, 200, 300, 400)])
    decorative(ticks)
    unit = txt("K", cfg.FONT["small"], cfg.MUTED).move_to([7.45, -0.6, 0])
    room = DashedLine([kx(pm.ROOM_T), -0.6, 0], [kx(pm.ROOM_T), 1.9, 0], stroke_color=cfg.GOLD, stroke_width=3, dash_length=0.1)
    room_tag = txt("room", cfg.FONT["small"], cfg.GOLD).next_to(room, UP, buff=0.1)
    title = txt("measured Boyle temperatures", cfg.FONT["small"], cfg.LIMIT).move_to([4.45, 3.15, 0])
    scene.play(Create(line), FadeIn(ticks), FadeIn(unit), FadeIn(title), run_time=1.2)
    scene.play(Create(room), FadeIn(room_tag), run_time=0.8)
    at_word(scene, t, 5, "nitrogen", lead=0.4)
    n2 = pm.BOYLE_T["N2"]
    n2_dot = glow_dot([kx(n2), -0.6, 0], cfg.GAS_COLORS["N2"], radius=0.12)
    n2_tag = VGroup(txt("N₂", cfg.FONT["label"], cfg.GAS_COLORS["N2"]), txt(f"{fx(n2, 0)} K", cfg.FONT["small"], cfg.WHITE))
    n2_tag.arrange(DOWN, buff=0.08).move_to([kx(n2) + 0.15, 0.55, 0])
    scene.play(FadeIn(n2_dot, scale=1.5), FadeIn(n2_tag, shift=DOWN * 0.1), run_time=1.0)
    at_word(scene, t, 5, "helium", lead=0.3)
    he = pm.BOYLE_T["He"]
    he_dot = glow_dot([kx(he), -0.6, 0], cfg.GAS_COLORS["He"], radius=0.12)
    he_tag = VGroup(txt("He", cfg.FONT["label"], cfg.GAS_COLORS["He"]), txt(f"{fx(he, 0)} K", cfg.FONT["small"], cfg.WHITE))
    he_tag.arrange(DOWN, buff=0.08).move_to([kx(he) + 0.2, 0.55, 0])
    scene.play(FadeIn(he_dot, scale=1.5), FadeIn(he_tag, shift=DOWN * 0.1), run_time=1.0)
    at_word(scene, t, 5, "far", lead=0.3)
    gap = arrow2d([kx(he) + 0.15, -1.55, 0], [kx(pm.ROOM_T) - 0.1, -1.55, 0], cfg.SIZE, width=0.09, tip_len=0.26)
    rises = txt("He: Z rises from the start", cfg.FONT["small"], cfg.SIZE).move_to([4.45, -2.15, 0])
    play_in(scene, t, 6, FadeIn(gap, shift=RIGHT * 0.2), FadeIn(rises, shift=UP * 0.1), run_time=1.2)

    # --- 6. Z = 1 is not "no interactions": the two terms cancel ---------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(line, ticks, unit, room, room_tag, title, n2_dot, n2_tag, he_dot, he_tag, gap, rises)),
               stage.set_spin(0.0), run_time=0.9)
    p_star = 3.0
    push, pull = terms_reduced(p_star, T_BOYLE)
    spot = point(p_star, T_BOYLE) + np.array([0, 0.03, 0])
    bead_ = Ball(spot, 0.13, cfg.WHITE, layers=12)
    up_v = Vector(spot, spot + np.array([0, push * 9.0, 0]), cfg.SIZE, width=0.11, tip=0.3)
    down_v = Vector(spot, spot - np.array([0, pull * 9.0, 0]), cfg.ATTRACT, width=0.11, tip=0.3)
    for b in (bead_,):
        b.presence = 0.0
        b.bias = 100.0
    up_v.presence = down_v.presence = 0.0
    stage.add_body(bead_)
    stage.add_overlay(up_v, down_v)
    scene.play(stage.fade(bead_, 1.0), run_time=0.6)
    at_word(scene, t, 6, "strong", lead=0.3)
    labels = VGroup(txt(f"size: +{fx(100 * push, 0)} %", cfg.FONT["label"], cfg.SIZE),
                    txt(f"attraction: −{fx(100 * pull, 0)} %", cfg.FONT["label"], cfg.ATTRACT))
    labels.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.5, 0.9, 0])
    scene.play(stage.fade(up_v, 1.0), stage.fade(down_v, 1.0), FadeIn(labels, shift=LEFT * 0.15), run_time=1.2)
    at_word(scene, t, 6, "cancel", lead=0.3)
    verdict = boxed(eq(r"Z \approx 1", cfg.FONT["title"], cfg.WHITE), cfg.GOLD, buff=0.2).move_to([4.5, -1.0, 0])
    sub = txt("by cancellation", cfg.FONT["label"], cfg.GOLD).next_to(verdict, DOWN, buff=0.22)
    scene.play(FadeIn(verdict, shift=UP * 0.1), FadeIn(sub), run_time=1.0)
    finish(scene, t, stage, drift=0.15)
