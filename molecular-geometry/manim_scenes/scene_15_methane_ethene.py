"""Chapter 15 — where the two pictures meet: methane and ethene.

Methane: VSEPR's four regions hand over to four sp3 hybrids, and four
hydrogen 1s orbitals glide in to overlap them head on (sigma). Ethene is
built from its measured geometry (``molecule_library.ethene``): sp2
hybrids form the sigma framework, the upright p orbitals overlap side by side
above and below the plane (pi). Twisting one end shows why: turned 90
degrees, the p orbitals no longer line up and the pi overlap is lost.
"""

from manim_scenes.common import *

UNITS = 0.56
PM = 2.9 / 134          # ethene drawn with C=C 2.9 screen units long


class Scene15MethaneEthene(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "Methane and ethene")
    alpha3 = om.SP_ALPHA["sp3"]

    # --- 1-2. Methane: VSEPR's four regions ------------------------------------------------------------------------
    stage = Stage([0, -0.3, 0], zoom=1.2, yaw=0.45, pitch=0.3, sway=0.1)
    regions = RegionModel(stage, pm.ideal_directions(4))
    regions.core.presence = 0.0
    regions.glow.presence = 0.0
    carbon = element_ball("C", ORIGIN, scale=0.6)
    stage.add_body(carbon)
    show(scene, stage, 1.0)
    dismiss_opening_title(scene, t, head, at=2.4)
    beat(scene, t, 1)
    vsepr = top_caption("VSEPR: four regions, tetrahedral", cfg.CYAN)
    scene.play(FadeIn(vsepr), stage.set_spin(0.3), run_time=1.2)

    # --- 3. Valence bond picture: four sp3 hybrids pointing the same way --------------------------------------------------
    beat(scene, t, 2)
    hybrids = [Orbital(stage, ORIGIN, d, alpha3, units=UNITS) for d in pm.ideal_directions(4)]
    for h in hybrids:
        h.set_presence(0.0)
    vb = top_caption("Valence bond: four sp³ hybrids", cfg.BLUE)
    scene.play(*[stage.fade(l, 0.0) for l in regions.lobes], *[a for h in hybrids for a in h.fade(1.0)],
               fade_through(vsepr, vb), stage.set_spin(0.20), run_time=1.8)
    scene.remove(vsepr)

    # --- 4. Hydrogen 1s orbitals overlap head on -----------------------------------------------------------------------------
    beat(scene, t, 3)
    reach = om.polar_reach(alpha3) * UNITS
    approach = [2.2]

    def h_spot(d):
        return lambda d=d: mu.unit(d) * reach * (0.95 * approach[0])

    h_balls, h_orbs = [], []
    for d in pm.ideal_directions(4):
        h_orbs.append(hydrogen_orbital(stage, h_spot(d), units=UNITS * 0.95, opacity=0.6))
        ball = element_ball("H", h_spot(d))
        stage.add_body(ball)
        h_balls.append(ball)
    for body in h_orbs + h_balls:
        body.presence = 0.0
    # Settle the view for the incoming hydrogen overlaps after the hybrid reveal.
    scene.play(*[stage.fade(b, 1.0) for b in h_orbs + h_balls], stage.set_spin(0.0), run_time=1.0)
    scene.play(stage.tween(lambda: approach[0], lambda v: approach.__setitem__(0, v), 1.0), run_time=2.6,
               rate_func=smooth)

    # --- 5. Four sigma bonds, all equivalent ---------------------------------------------------------------------------------------
    beat(scene, t, 4)
    glows = [Halo(b, cfg.GOLD, reach=3.2, peak=0.3) for b in h_balls]
    for g in glows:
        g.presence = 0.0
    stage.add_body(*glows)
    four = VGroup(txt("4 ×", cfg.FONT["section"], cfg.WHITE), eq(r"\sigma", cfg.FONT["hero"], cfg.SIGMA_COLOR))
    four.arrange(RIGHT, buff=0.25).move_to([5.0, 0.0, 0])
    scene.play(*[stage.fade(g, 1.0) for g in glows], FadeIn(four, shift=LEFT * 0.2), run_time=1.2)
    scene.play(stage.set_spin(0.35), run_time=1.6)

    # --- 6. Ethene ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, stage, 0.8, FadeOut(vb), FadeOut(four))
    geometry = ml.ethene()
    carbons = geometry["C"] * PM
    hs = geometry["H"] * PM
    twist = [0.0]

    def turned(point_fn):
        """Points on the right-hand CH2 end turn with the twist about the C=C axis."""
        def where():
            p = np.asarray(point_fn(), dtype=float)
            return carbons[1] + mu.rotation_about(RIGHT, twist[0]) @ (p - carbons[1])
        return where

    stage = Stage([0, -0.5, 0], zoom=1.15, yaw=0.0, pitch=0.32, sway=0.1)
    # Lay the molecular plane flat so the p orbitals (along local z) stand upright.
    stage.model = mu.rotation_x(-np.pi / 2)
    c_balls = [element_ball("C", carbons[0], scale=0.85), element_ball("C", turned(lambda: carbons[1]), scale=0.85)]
    h_balls = [element_ball("H", hs[i] if i < 2 else turned(lambda i=i: hs[i])) for i in range(4)]
    rods = [Rod(c_balls[0], c_balls[1], 2)] + [Rod(c_balls[0 if i < 2 else 1], h_balls[i]) for i in range(4)]
    stage.add_body(*rods, *c_balls, *h_balls)
    name = formula(r"\mathrm{C_2H_4}", cfg.FONT["section"]).move_to([0, 3.0, 0])
    show(scene, stage, 1.2, FadeIn(name))

    # --- 7. Three regions per carbon: trigonal planar ---------------------------------------------------------------------------------
    beat(scene, t, 6)
    hch = AngleArc(carbons[0], hs[0] - carbons[0], hs[1] - carbons[0], 0.75,
                   label=degrees_label(gd.BOND_ANGLE_DEG["C2H4"], cfg.FONT["body"]), label_gap=0.7,
                   label_offset=LEFT * 0.5)
    hch.presence = 0.0
    stage.add_overlay(hch)
    planar = caption("Three regions per carbon: trigonal planar", cfg.CYAN)
    scene.play(stage.fade(hch, 1.0), FadeIn(planar), run_time=1.2)
    scene.play(*stage.turn(pitch=1.3), run_time=2.0, rate_func=smooth)
    scene.play(*stage.turn(pitch=0.32), run_time=1.6, rate_func=smooth)

    # --- 8. Each carbon sp2, with one upright p -------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    alpha2 = om.SP_ALPHA["sp2"]
    left_dirs = [RIGHT, hs[0] - carbons[0], hs[1] - carbons[0]]
    right_dirs = [LEFT, hs[2] - carbons[1], hs[3] - carbons[1]]
    sp2 = [Orbital(stage, carbons[0], d, alpha2, units=UNITS * 0.68) for d in left_dirs]
    sp2 += [Orbital(stage, turned(lambda: carbons[1]),
                    (lambda d=d: mu.rotation_about(RIGHT, twist[0]) @ mu.unit(d)), alpha2, units=UNITS * 0.68)
            for d in right_dirs]
    p_up = [p_orbital(stage, carbons[0], OUT, units=UNITS * 0.9, opacity=0.8),
            p_orbital(stage, turned(lambda: carbons[1]), lambda: mu.rotation_about(RIGHT, twist[0]) @ OUT,
                      units=UNITS * 0.9, opacity=0.8)]
    for orb in sp2 + p_up:
        orb.set_presence(0.0)
    sigma_cc = Rod(c_balls[0], c_balls[1], order=1)
    sigma_cc.presence = 0.0
    stage.add_body(sigma_cc)
    tag = caption("sp² in the plane · p above and below", cfg.BLUE)
    # Give each carbon its own turn. Six hybrid orbitals plus two p orbitals
    # at once hid the bond framework and the direction of each lobe.
    scene.play(stage.fade(hch, 0.0), stage.fade(rods[0], 0.0), stage.fade(sigma_cc, 1.0),
               *[a for o in sp2[:3] for a in o.fade(0.75)], fade_through(planar, tag),
               *stage.turn(yaw=0.18, pitch=0.72), run_time=1.2)
    scene.remove(planar)
    scene.wait(0.8)  # Give the first carbon a readable, settled view.
    scene.play(*[a for o in sp2[:3] for a in o.fade(0.0)], run_time=0.4)
    scene.play(*[a for o in sp2[3:] for a in o.fade(0.75)], run_time=0.9)
    scene.wait(0.8)  # Match the time given to the second carbon.
    scene.play(*[a for o in sp2[3:] for a in o.fade(0.0)], run_time=0.4)
    scene.play(*[a for o in p_up for a in o.fade(1.0)],
               *stage.turn(yaw=0.0, pitch=0.32), run_time=1.2)

    # --- 9. The sigma framework ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    sigma_tag = VGroup(eq(r"\sigma", cfg.FONT["hero"], cfg.SIGMA_COLOR), txt("framework", cfg.FONT["body"], cfg.SIGMA_COLOR))
    sigma_tag.arrange(RIGHT, buff=0.3).move_to([-4.6, 2.3, 0])
    scene.play(*[a for o in p_up for a in o.fade(0.3)],
               *[a for o in sp2 for a in o.fade(0.0)], FadeIn(sigma_tag), run_time=1.2)
    scene.play(*stage.turn(yaw=0.5), run_time=2.4, rate_func=there_and_back)

    # --- 10. Side-by-side p overlap: the pi bond ---------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    lift = 0.62
    pi_lobes = [Lobe(lambda s=s: carbons[0] + OUT * s * lift + LEFT * 0.25, RIGHT, 2.8, 0.36, cfg.PI_COLOR,
                     start=0.0, body_opacity=0.4) for s in (1, -1)]
    for lobe in pi_lobes:
        lobe.presence = 0.0
    stage.add_body(*pi_lobes)
    pi_tag = VGroup(eq(r"\pi", cfg.FONT["hero"], cfg.PI_COLOR), txt("bond", cfg.FONT["body"], cfg.PI_COLOR))
    pi_tag.arrange(RIGHT, buff=0.3).move_to([4.6, 2.3, 0])
    scene.play(*[a for o in sp2 for a in o.fade(0.0)], *[a for o in p_up for a in o.fade(0.35)], run_time=1.2)
    scene.play(*[stage.fade(l, 1.0) for l in pi_lobes], FadeIn(pi_tag), *stage.turn(pitch=0.22), run_time=1.6)

    # --- 11. sigma + pi; pi needs parallel p orbitals ---------------------------------------------------------------------------------------
    beat(scene, t, 10)
    double = caption("Double bond = σ + π", cfg.WHITE)
    scene.play(fade_through(tag, double), run_time=0.9)
    scene.remove(tag)
    scene.play(stage.tween(lambda: twist[0], lambda v: twist.__setitem__(0, v), np.pi / 2),
               *[stage.fade(l, 0.0) for l in pi_lobes],
               *[a for o in p_up for a in o.fade(0.8)], *stage.turn(pitch=0.35), run_time=2.2, rate_func=smooth)
    scene.play(stage.tween(lambda: twist[0], lambda v: twist.__setitem__(0, v), 0.0),
               *[stage.fade(l, 1.0) for l in pi_lobes],
               *[a for o in p_up for a in o.fade(0.35)], run_time=2.2, rate_func=smooth)
    scene.play(Indicate(pi_tag, color=cfg.WHITE, scale_factor=1.06), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
