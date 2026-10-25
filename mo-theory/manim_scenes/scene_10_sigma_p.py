"""Chapter 10 — head-on p orbitals: sigma 2p and sigma* 2p.

All surfaces are computed (``utils.orbital_models``): two 2p orbitals on the
bond axis, each pointing at the other, combined as phi_A + c phi_B. The
nuclei slide together with c = +1, then c slides continuously to -1 — the
viewer watches the shared cloud tear apart into the antibonding orbital.
"""

from manim_scenes.common import *

STAGE_AT = np.array([-2.3, -0.25, 0])
PANEL_X = 5.0
FAR = 13.0
MORPH_STEP = 0.46       # a coarser grid while a surface is changing every frame


class Scene10SigmaP(Scene):
    def construct(self) -> None:
        play_scene(self)


def phase_tag(stage: Stage, point, sign: int, size: int | None = None) -> Tag:
    mark = eq("+" if sign > 0 else "-", size or cfg.FONT["section"], cfg.PHASE_PLUS if sign > 0 else cfg.PHASE_MINUS)
    tag = Tag(mark, point)
    tag.presence = 0.0
    stage.add_overlay(tag)
    return tag


def recessed_plane(stage: Stage, normal: str, size: float) -> Face:
    """Keep the nodal guide behind the translucent density and nuclei."""
    plane = nodal_plane(stage, ORIGIN, normal, size=size, opacity=0.055)
    # Whole-object depth sorting otherwise lets the plane cover a nearer lobe.
    # Its geometric position stays at the node; only the reference layer moves.
    plane.bias = -1e3
    plane.edge_opacity = 0.5
    return plane


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "Sigma from p orbitals")
    units = P_UNITS

    # --- 1. Most of chemistry needs p orbitals ---------------------------------------------------------------------------
    solo = Stage([-1.0, -0.3, 0], zoom=0.78, yaw=0.5, pitch=0.3, spin=0.3)
    p_one = MOCloud(solo, om.MOSpec("py", 1.0, om.R_P, single="A"), origin=RIGHT * om.R_P / 2 * units)
    solo.add_body(Ball(ORIGIN, 0.12, cfg.WHITE))
    show(scene, solo, 1.4)
    dismiss_opening_title(scene, t, head, at=2.6)
    p_word = result_label("a p orbital", cfg.CYAN, cfg.FONT["section"]).move_to([4.6, 2.6, 0])
    scene.play(FadeIn(p_word, shift=DOWN * 0.2), run_time=0.8)

    # --- 2. Two lobes of opposite phase; a node through the nucleus ------------------------------------------------------
    beat(scene, t, 1)
    plus = phase_tag(solo, np.array([2.4, 3.0, 0.0]), 1)
    minus = phase_tag(solo, np.array([2.4, -3.0, 0.0]), -1)
    node = recessed_plane(solo, "y", size=4.2)
    scene.play(solo.fade(plus, 1.0), solo.fade(minus, 1.0), run_time=1.0)
    scene.play(solo.fade(node, 1.0), solo.set_spin(0.12), run_time=1.2)
    node_word = caption("A node through the nucleus: psi = 0", cfg.NODE)
    scene.play(FadeIn(node_word), run_time=0.8)

    # --- 3. Point two straight at each other --------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(p_word), FadeOut(node_word), run_time=0.6)
    hide(scene, solo, 0.8)
    stage = Stage(STAGE_AT, zoom=0.69, yaw=0.0, pitch=0.22, sway=0.3)
    sigma = MOCloud(stage, om.MOSpec("ps", 1.0, FAR), step=MORPH_STEP)
    stage_nuclei(stage, sigma)
    axis = Segment(np.array([-8.0, 0, 0]), np.array([8.0, 0, 0]), cfg.MUTED, 2.4, 0.45, dashed=True)
    stage.add_body(axis)
    facing = [phase_tag(stage, lambda s=s: np.array([s * (sigma.spec.R / 2 - 2.0) * units, 1.9, 0.0]), 1)
              for s in (-1, 1)]
    show(scene, stage, 1.2)
    along = caption("Both along the bond axis, pointing at each other", cfg.WHITE)
    scene.play(FadeIn(along), run_time=0.8)

    # --- 4. Match the phases and bring them together ------------------------------------------------------------------------------
    beat(scene, t, 3)
    match = caption("Facing lobes match:  + meets +", cfg.PHASE_PLUS)
    scene.play(*[stage.fade(f, 1.0) for f in facing], fade_through(along, match), run_time=1.0)
    scene.remove(along)
    scene.play(sigma.morph(R=om.R_P), run_time=5.0, rate_func=smooth)
    sigma.step = None

    # --- 5. One thick cloud between; small opposite lobes behind -------------------------------------------------------------------
    beat(scene, t, 4)
    behind = [phase_tag(stage, np.array([s * (om.R_P / 2 + 3.6) * units, 1.7, 0.0]), -1) for s in (-1, 1)]
    thick = caption("One thick cloud between; small opposite lobes behind", cfg.WHITE)
    scene.play(*[stage.fade(f, 0.0) for f in facing], *[stage.fade(b, 1.0) for b in behind], fade_through(match, thick),
               run_time=1.2)
    scene.remove(match)
    scene.play(*stage.turn(yaw=0.6, pitch=0.35), run_time=3.0, rate_func=smooth)

    # --- 6. sigma 2p: the same from every side ------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    name = eq(r"\sigma_{2p}", cfg.FONT["hero"], cfg.BONDING).move_to([PANEL_X, 2.5, 0])
    scene.play(Write(name), *[stage.fade(b, 0.0) for b in behind], FadeOut(thick), run_time=1.0)
    same = caption("Turn it around the axis: it looks the same. That's sigma.", cfg.CYAN)
    scene.play(FadeIn(same), run_time=0.6)
    scene.play(stage.rock(RIGHT, TAU), run_time=6.0, rate_func=smooth)

    # --- 7. Flip one phase -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    flip = caption("Flip one phase: the facing lobes cancel", cfg.ANTIBONDING)
    scene.play(fade_through(same, flip), run_time=0.8)
    scene.remove(same)
    sigma.step = MORPH_STEP
    scene.play(sigma.morph(c=-1.0), run_time=4.4, rate_func=smooth)
    sigma.step = None

    # --- 8. A node splits the bond: sigma* 2p ----------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    mid = recessed_plane(stage, "x", size=4.6)
    star = eq(r"\sigma^{*}_{2p}", cfg.FONT["hero"], cfg.ANTIBONDING).move_to(name)
    scene.play(stage.fade(mid, 1.0), Transform(name, star), FadeOut(flip), run_time=1.2)
    scene.play(*stage.turn(yaw=0.95, pitch=0.3), run_time=3.0, rate_func=there_and_back)

    # --- 9. Head-on overlap: a big split --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    split = mini_split([PANEL_X, -0.3, 0], drop=1.25, rise=1.6, bonding_tex=r"\sigma_{2p}", antibonding_tex=r"\sigma^{*}_{2p}",
                       half_width=1.9, line=0.7, size=cfg.FONT["body"])
    scene.play(FadeOut(name), run_time=0.6)
    scene.play(Create(split.ao), run_time=0.6)
    scene.play(Create(split.links), FadeIn(split.bond), FadeIn(split.anti), FadeIn(split.labels), run_time=1.4)
    big = caption("Head-on overlap is strong: a big split", cfg.WHITE)
    scene.play(FadeIn(big), run_time=0.6)

    # --- 10. Three p orbitals per atom; only one points along the bond -----------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(split), FadeOut(big), run_time=0.6)
    hide(scene, stage, 0.8)
    colors = {"ps": (cfg.PHASE_PLUS, cfg.PHASE_MINUS), "py": (cfg.PURPLE, mu.shade(cfg.PURPLE, 0.75)),
              "pz": (cfg.TEAL, mu.shade(cfg.TEAL, 0.75))}
    words = {"ps": ("along the bond", cfg.PHASE_PLUS), "py": ("sideways", cfg.PURPLE), "pz": ("sideways", cfg.TEAL)}
    trio, stages, keys = {}, [], VGroup()
    for kind, x in (("ps", -4.8), ("py", 0.0), ("pz", 4.8)):
        mini = Stage([x, 0.1, 0], zoom=0.42, yaw=0.0, pitch=0.25, sway=0.25)
        trio[kind] = MOCloud(mini, om.MOSpec(kind, 1.0, om.R_P, single="A"), origin=RIGHT * om.R_P / 2 * units, slots=1,
                             opacity=0.7, plus=cfg.PHASE_PLUS, minus=cfg.PHASE_MINUS)
        mini.add_body(Ball(ORIGIN, 0.2, cfg.WHITE))
        mini.add_body(Segment(np.array([-6.5, 0, 0]), np.array([6.5, 0, 0]), cfg.GOLD, 3.0, 0.7, dashed=True))
        mini.presence = 0.0
        stages.append(mini)
        keys.add(txt(words[kind][0], cfg.FONT["body"], words[kind][1]).move_to([x, -2.45, 0]))
    axis_key = txt("gold line: the bond axis", cfg.FONT["small"], cfg.GOLD).move_to([0, 2.9, 0])
    for mini in stages:
        scene.add(mini)
        scene.play(mini.fade(mini, 1.0), run_time=0.7)
    three = caption("Three p orbitals per atom, at right angles", cfg.WHITE)
    scene.play(FadeIn(keys, shift=UP * 0.2), FadeIn(three), FadeIn(axis_key), run_time=1.0)

    # --- 11. What about the sideways pair? -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    sideways = caption("What happens to the two that stand side by side?", cfg.GOLD)
    scene.play(stages[0].fade(stages[0], 0.3), keys[0].animate.set_opacity(0.3), fade_through(three, sideways),
               Indicate(keys[1:], color=cfg.GOLD, scale_factor=1.08), run_time=1.4)
    scene.remove(three)
    scene.play(*stages[1].turn(yaw=0.9, pitch=0.4), *stages[2].turn(yaw=0.9, pitch=0.4), run_time=3.5, rate_func=smooth)
    scene.play(*stages[1].turn(yaw=0.0, pitch=0.25), *stages[2].turn(yaw=0.0, pitch=0.25), run_time=3.8, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
