"""Chapter 05 — the 2D maps lifted into 3D: sigma 1s and sigma* 1s.

Both surfaces are computed (``utils.orbital_models``): two normalised 1s
orbitals combined in phase or out of phase, drawn at the same |psi| contour
as the nuclei slide together. In phase, the spheres fuse into one cloud; out
of phase they never can, because psi is exactly zero on the mid-plane.
"""

from manim_scenes.common import *

LEFT_AT = np.array([-3.9, -0.35, 0])
RIGHT_AT = np.array([3.9, -0.35, 0])
FAR = 4.4
FORCE_LIFT = 0.65  # Keep force arrows parallel to the bond, clear of nuclei.


class Scene05BondingAntibonding(Scene):
    def construct(self) -> None:
        play_scene(self)


def sign_tag(stage: Stage, cloud: MOCloud, side: int, sign: int, lift: float = 1.75) -> Tag:
    """A big + or - riding above one atom's lobe, coloured by phase."""
    mark = eq("+" if sign > 0 else "-", cfg.FONT["section"], cfg.PHASE_PLUS if sign > 0 else cfg.PHASE_MINUS)
    tag = Tag(mark, lambda: np.array([side * cloud.spec.R / 2 * cloud.units, lift, 0.0]))
    tag.presence = 0.0
    stage.add_overlay(tag)
    return tag


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Bonding and antibonding")

    # --- 1. Lift the maps into 3D: two 1s orbitals, far apart ----------------------------------------------------
    bond_stage = Stage([0, -0.15, 0], zoom=1.45, yaw=0.0, pitch=0.18, spin=0.0)
    bonding = MOCloud(bond_stage, om.MOSpec("s", 1.0, FAR))
    nuclei = stage_nuclei(bond_stage, bonding)
    axis = Segment(np.array([-4.6, 0, 0]), np.array([4.6, 0, 0]), cfg.MUTED, 2.4, 0.5, dashed=True)
    bond_stage.add_body(axis)
    tags = [sign_tag(bond_stage, bonding, -1, 1), sign_tag(bond_stage, bonding, 1, 1)]
    show(scene, bond_stage, 1.4)
    dismiss_opening_title(scene, t, head, at=3.0)

    # --- 2. In phase: bring them close -----------------------------------------------------------------------------
    beat(scene, t, 1)
    in_phase = caption("In phase:  + meets +", cfg.PHASE_PLUS)
    scene.play(*[bond_stage.fade(tag, 1.0) for tag in tags], FadeIn(in_phase), *bond_stage.turn(yaw=0.32, pitch=0.3),
               run_time=1.2)
    scene.play(bonding.morph(R=om.R_S), run_time=5.0, rate_func=smooth)

    # --- 3. One cloud, fattest between the nuclei: sigma 1s ------------------------------------------------------------
    beat(scene, t, 2)
    name = eq(r"\sigma_{1s}", cfg.FONT["hero"], cfg.BONDING).move_to([0, 3.05, 0])
    kind = result_label("bonding", cfg.RESULT, cfg.FONT["body"]).next_to(name, RIGHT, buff=0.5)
    scene.play(*[bond_stage.fade(tag, 0.0) for tag in tags], FadeOut(in_phase), Write(name), run_time=1.2)
    scene.play(FadeIn(kind, shift=LEFT * 0.2), run_time=0.8)
    middle = caption("One cloud, fattest between the nuclei", cfg.CYAN)
    scene.play(FadeIn(middle), *bond_stage.turn(yaw=-0.25, pitch=0.42), run_time=2.6, rate_func=smooth)

    # --- 4. Sigma: the same from every angle around the axis --------------------------------------------------------------
    beat(scene, t, 3)
    turning = caption("Turn it around the bond axis: no change", cfg.WHITE)
    scene.play(fade_through(middle, turning), run_time=0.8)
    scene.remove(middle)
    scene.play(bond_stage.rock(RIGHT, TAU), run_time=6.0, rate_func=smooth)

    # --- 5. Out of phase: a second pair, far apart --------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(turning), FadeOut(kind), name.animate.move_to([LEFT_AT[0], 3.05, 0]).scale(0.75),
               bond_stage.glide(LEFT_AT), bond_stage.zoom_to(1.0), run_time=1.4)
    anti_stage = Stage(RIGHT_AT, zoom=1.0, yaw=0.32, pitch=0.42, spin=0.0)
    anti = MOCloud(anti_stage, om.MOSpec("s", -1.0, FAR))
    stage_nuclei(anti_stage, anti)
    anti_tags = [sign_tag(anti_stage, anti, -1, 1), sign_tag(anti_stage, anti, 1, -1)]
    for tag in anti_tags:
        tag.presence = 1.0
    show(scene, anti_stage, 0.9)
    scene.play(anti.morph(R=om.R_S), run_time=2.0, rate_func=smooth)

    # --- 6. They refuse to merge: a nodal plane ----------------------------------------------------------------------------------------
    beat(scene, t, 5)
    plane = nodal_plane(anti_stage, ORIGIN, "x", size=2.7)
    zero = eq(r"\psi = 0", cfg.FONT["body"], cfg.NODE)
    zero_tag = Tag(zero, np.array([0.0, -2.35, 0.0]))
    zero_tag.presence = 0.0
    anti_stage.add_overlay(zero_tag)
    scene.play(anti_stage.fade(plane, 1.0), anti_stage.fade(zero_tag, 1.0), *[anti_stage.fade(g, 0.0) for g in anti_tags],
               run_time=1.4)
    scene.play(*anti_stage.turn(yaw=0.95, pitch=0.3), run_time=4.0, rate_func=there_and_back)
    scene.play(Indicate(zero, color=cfg.GOLD, scale_factor=1.15), run_time=1.0)

    # --- 7. sigma star 1s ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    star = eq(r"\sigma^{*}_{1s}", cfg.FONT["hero"] * 0.75, cfg.ANTIBONDING).move_to([RIGHT_AT[0], 3.05, 0])
    scene.play(Write(star), run_time=1.0)
    asterisk = glow_frame(star, cfg.ANTIBONDING, buff=0.12)
    anti_word = txt("antibonding", cfg.FONT["body"], cfg.ANTIBONDING).next_to(star, DOWN, buff=0.22)
    scene.play(Create(asterisk), FadeIn(anti_word), run_time=1.0)
    scene.play(FadeOut(asterisk), run_time=0.6)

    # --- 8. Side by side ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    bond_word = txt("bonding", cfg.FONT["body"], cfg.RESULT).next_to(name, DOWN, buff=0.22)
    between = caption("Density between the nuclei  —  or a node between them", cfg.WHITE)
    scene.play(FadeIn(bond_word), FadeIn(between), anti_stage.fade(zero_tag, 0.0), run_time=1.0)
    bond_stage.sway = anti_stage.sway = 0.35
    narration_wait(scene, 2.0)

    # --- 9. Why: density between attracts both nuclei ------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    pulls = []
    for side in (-1, 1):
        end = lambda side=side: np.array([side * bonding.spec.R / 2 * bonding.units, FORCE_LIFT, 0])
        tip = lambda side=side: np.array([side * bonding.spec.R / 2 * bonding.units * 0.25, FORCE_LIFT, 0])
        vec = Vector(end, tip, cfg.GOLD, width=0.1, tip=0.28)
        vec.presence = 0.0
        bond_stage.add_overlay(vec)
        pulls.append(vec)
    plus_tags = []
    for stage, cloud in ((bond_stage, bonding), (anti_stage, anti)):
        for side in (-1, 1):
            tag = Tag(txt("+", cfg.FONT["label"], cfg.GOLD), lambda side=side, c=cloud: np.array(
                [side * c.spec.R / 2 * c.units, -0.55, 0.0]))
            tag.presence = 0.0
            stage.add_overlay(tag)
            plus_tags.append((stage, tag))
    pulled = caption("Both nuclei pulled toward the shared density", cfg.GOLD)
    scene.play(*[stage.fade(tag, 1.0) for stage, tag in plus_tags], fade_through(between, pulled), run_time=1.2)
    scene.remove(between)
    scene.play(*[bond_stage.fade(v, 1.0) for v in pulls], run_time=1.2)
    scene.play(bonding.morph(R=om.R_S * 0.92), run_time=1.6, rate_func=there_and_back)

    # --- 10. Without it, the nuclei face each other ------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    pushes = []
    for side in (-1, 1):
        base = lambda side=side: np.array([side * anti.spec.R / 2 * anti.units, FORCE_LIFT, 0])
        tip = lambda side=side: np.array([side * (anti.spec.R / 2 * anti.units + 1.0), FORCE_LIFT, 0])
        vec = Vector(base, tip, cfg.RED, width=0.1, tip=0.28)
        vec.presence = 0.0
        anti_stage.add_overlay(vec)
        pushes.append(vec)
    exposed = caption("A node separates the lobes: antibonding raises energy", cfg.RED)
    scene.play(*[anti_stage.fade(v, 1.0) for v in pushes], fade_through(pulled, exposed), run_time=1.2)
    scene.remove(pulled)
    scene.play(anti.morph(R=om.R_S * 1.12), run_time=1.8, rate_func=there_and_back)

    # --- 11. Half the story: next, energy ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    energy = caption("Shape is half the story. Next: energy.", cfg.CYAN)
    scene.play(fade_through(exposed, energy), *[bond_stage.fade(v, 0.0) for v in pulls],
               *[anti_stage.fade(v, 0.0) for v in pushes], *[stage.fade(tag, 0.0) for stage, tag in plus_tags],
               run_time=1.2)
    scene.remove(exposed)
    scene.play(*bond_stage.turn(yaw=bond_stage.yaw + 0.6), *anti_stage.turn(yaw=anti_stage.yaw - 0.6), run_time=3.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
