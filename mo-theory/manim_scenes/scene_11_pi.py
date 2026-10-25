"""Chapter 11 — sideways p orbitals: pi and pi*, and why they come in pairs.

The surfaces are phi_A + c phi_B for two parallel 2p orbitals
(``utils.orbital_models``), slid together and then flipped from c = +1 to
c = -1. The second pair, turned 90 degrees about the bond axis, gives an
identical, degenerate set — the pair of pi* orbitals that will hold oxygen's
unpaired electrons.
"""

from manim_scenes.common import *
from manim_scenes.scene_10_sigma_p import MORPH_STEP, phase_tag, recessed_plane

STAGE_AT = np.array([-2.4, -0.2, 0])
PANEL_X = 5.0
FAR = 13.0


class Scene11Pi(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "11", "Pi orbitals come in pairs")
    units = P_UNITS

    # --- 1. Two p orbitals side by side ----------------------------------------------------------------------------------
    stage = Stage(STAGE_AT, zoom=0.64, yaw=0.0, pitch=0.25, sway=0.3)
    pi = MOCloud(stage, om.MOSpec("py", 1.0, FAR), step=MORPH_STEP)
    stage_nuclei(stage, pi)
    stage.add_body(Segment(np.array([-8.0, 0, 0]), np.array([8.0, 0, 0]), cfg.GOLD, 2.6, 0.6, dashed=True))
    tops = [phase_tag(stage, lambda s=s: np.array([s * pi.spec.R / 2 * units + 1.3, 3.3, 0.0]), 1) for s in (-1, 1)]
    show(scene, stage, 1.4)
    dismiss_opening_title(scene, t, head, at=2.4)
    scene.play(*[stage.fade(x, 1.0) for x in tops], run_time=0.8)
    parallel = caption("Side by side, at right angles to the bond axis", cfg.WHITE)
    scene.play(FadeIn(parallel), run_time=0.8)

    # --- 2. In phase: upper and lower lobes merge: pi ---------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(pi.morph(R=om.R_P), *[stage.fade(x, 0.0) for x in tops], FadeOut(parallel), run_time=4.6, rate_func=smooth)
    pi.step = None
    name = eq(r"\pi_{2p}", cfg.FONT["hero"], cfg.BONDING).move_to([PANEL_X, 2.6, 0])
    scene.play(Write(name), run_time=1.0)

    # --- 3. Nothing on the axis; a nodal plane through both nuclei ----------------------------------------------------------------
    beat(scene, t, 2)
    flat = recessed_plane(stage, "y", size=8.5)
    scene.play(stage.fade(flat, 1.0), *stage.turn(yaw=0.5, pitch=0.42), run_time=2.0)
    above = caption("Clouds above and below; a node through the axis", cfg.WHITE)
    scene.play(FadeIn(above), run_time=0.8)
    scene.play(*stage.turn(yaw=-0.4, pitch=0.3), run_time=4.0, rate_func=smooth)

    # --- 4. Out of phase: pi star ------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    pi.step = MORPH_STEP
    scene.play(pi.morph(c=-1.0), FadeOut(above), run_time=3.6, rate_func=smooth)
    pi.step = None
    cut = recessed_plane(stage, "x", size=6.0)
    star = eq(r"\pi^{*}_{2p}", cfg.FONT["hero"], cfg.ANTIBONDING).move_to(name)
    scene.play(stage.fade(cut, 1.0), Transform(name, star), run_time=1.2)
    second = caption("A second node, between the nuclei", cfg.ANTIBONDING)
    scene.play(FadeIn(second), run_time=0.6)

    # --- 5. Sideways overlap: a smaller split than head-on -------------------------------------------------------------------------------
    beat(scene, t, 4)
    sig = mini_split([PANEL_X - 1.35, -0.2, 0], drop=1.25, rise=1.6, bonding_tex=r"\sigma", antibonding_tex=r"\sigma^{*}",
                     half_width=1.0, line=0.5, size=cfg.FONT["body"])
    pis = mini_split([PANEL_X + 1.45, -0.2, 0], drop=0.6, rise=0.8, bonding_tex=r"\pi", antibonding_tex=r"\pi^{*}",
                     half_width=1.0, line=0.5, size=cfg.FONT["body"])
    scene.play(FadeOut(name), FadeOut(second), run_time=0.6)
    scene.play(FadeIn(sig), run_time=1.0)
    scene.play(FadeIn(pis), run_time=1.0)
    less = caption("Sideways overlap is weaker: pi splits less than sigma", cfg.WHITE)
    scene.play(FadeIn(less), run_time=0.6)

    # --- 6. The second sideways p orbital, turned ninety degrees ---------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(sig), FadeOut(pis), FadeOut(less), run_time=0.6)
    hide(scene, stage, 0.8)
    left = Stage([-3.9, 0.25, 0], zoom=0.5, yaw=0.45, pitch=0.35, sway=0.2)
    right = Stage([3.9, 0.25, 0], zoom=0.5, yaw=0.45, pitch=0.75, sway=0.2)
    pi_y = MOCloud(left, om.MOSpec("py", 1.0, om.R_P))
    pi_z = MOCloud(right, om.MOSpec("pz", 1.0, om.R_P))
    for st, cloud in ((left, pi_y), (right, pi_z)):
        stage_nuclei(st, cloud)
        st.add_body(Segment(np.array([-7.5, 0, 0]), np.array([7.5, 0, 0]), cfg.GOLD, 2.4, 0.6, dashed=True))
    show(scene, left, 0.8)
    turned = caption("Each atom has a second sideways p orbital, turned 90°", cfg.WHITE)
    show(scene, right, 1.0, FadeIn(turned))
    names = VGroup(eq(r"\pi_{2p}", cfg.FONT["section"], cfg.BONDING).move_to([-3.9, 2.95, 0]),
                   eq(r"\pi_{2p}", cfg.FONT["section"], cfg.BONDING).move_to([3.9, 2.95, 0]))
    scene.play(FadeIn(names), run_time=0.8)

    # --- 7. The same shape, rotated about the axis -----------------------------------------------------------------------------------------
    beat(scene, t, 6)
    rotated = caption("Same shape, rotated a quarter turn about the bond axis", cfg.CYAN)
    scene.play(fade_through(turned, rotated), run_time=0.8)
    scene.remove(turned)
    scene.play(right.rock(RIGHT, -PI / 2), run_time=2.4, rate_func=smooth)
    scene.play(right.rock(RIGHT, PI / 2), run_time=2.4, rate_func=smooth)

    # --- 8. Same energy: degenerate -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    pair = mini_split([0, -1.25, 0], drop=0.6, rise=0.8, bonding_tex=r"\pi_{2p}\ \pi_{2p}", antibonding_tex=r"\pi^{*}_{2p}\ \pi^{*}_{2p}",
                      count=2, half_width=2.6, line=0.75, size=cfg.FONT["body"])
    scene.play(FadeOut(rotated), left.glide([-4.4, 1.0, 0]), right.glide([4.4, 1.0, 0]), names[0].animate.move_to([-4.4, 3.4, 0]),
               names[1].animate.move_to([4.4, 3.4, 0]), run_time=1.0)
    scene.play(Create(pair.ao), Create(pair.links[:2]), FadeIn(pair.bond), FadeIn(pair.labels[0]), run_time=1.4)
    degenerate = result_label("degenerate: same energy", cfg.GREEN, cfg.FONT["body"]).move_to([0, -3.55, 0])
    scene.play(FadeIn(degenerate, shift=UP * 0.15), run_time=0.8)

    # --- 9. And two pi stars ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7 + 1)
    stars = VGroup(eq(r"\pi^{*}_{2p}", cfg.FONT["section"], cfg.ANTIBONDING).move_to(names[0]),
                   eq(r"\pi^{*}_{2p}", cfg.FONT["section"], cfg.ANTIBONDING).move_to(names[1]))
    pi_y.step = pi_z.step = MORPH_STEP
    scene.play(pi_y.morph(c=-1.0), pi_z.morph(c=-1.0), Transform(names, stars), run_time=3.0, rate_func=smooth)
    pi_y.step = pi_z.step = None
    scene.play(Create(pair.links[2:]), FadeIn(pair.anti), FadeIn(pair.labels[1]), run_time=1.4)

    # --- 10. Keep your eye on the pi star pair ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    spotlight = glow_frame(VGroup(pair.anti, pair.labels[1]), cfg.GOLD, buff=0.15)
    secret = caption("Oxygen's secret hides here", cfg.GOLD)
    scene.play(Create(spotlight), fade_through(degenerate, secret), run_time=1.2)
    scene.remove(degenerate)
    scene.play(Indicate(pair.anti, color=cfg.GOLD, scale_factor=1.15), run_time=1.4)

    # --- 11. Six p orbitals in, six molecular orbitals out --------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    tally = VGroup(*[eq(tex, cfg.FONT["section"], color) for tex, color in (
        (r"\sigma", cfg.BONDING), (r"\sigma^{*}", cfg.ANTIBONDING), (r"\pi", cfg.BONDING), (r"\pi", cfg.BONDING),
        (r"\pi^{*}", cfg.ANTIBONDING), (r"\pi^{*}", cfg.ANTIBONDING))]).arrange(RIGHT, buff=0.55)
    count = eq(r"6 \rightarrow 6", cfg.FONT["title"], cfg.GREEN)
    row = VGroup(tally, count).arrange(RIGHT, buff=1.0).move_to([0, -3.3, 0])
    scene.play(FadeOut(secret), FadeOut(spotlight), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in tally], lag_ratio=0.2), run_time=1.6)
    scene.play(Write(count), run_time=0.8)
    scene.play(*left.turn(yaw=1.2), *right.turn(yaw=1.2), run_time=5.5, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["11"])
