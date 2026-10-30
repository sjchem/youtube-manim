"""Scene 20 — the concentration map: the opening glass returns at the centre
and every measure becomes a node wired to it, in its own colour, with the
two bridges between them (density, the reaction's z). Then one question,
and the title over the turning solution as the camera pulls back.
"""

from manim_scenes.common import *

BASE = np.array([0.0, -2.75, 0.0])
NODES = [
    ("molarity", "mol per L of solution", cfg.VOLUME, (-5.1, 2.05)),
    ("molality", "mol per kg of solvent", cfg.SOLVENT_MASS, (5.1, 2.05)),
    ("mole fraction", "share of all the moles", cfg.AMOUNT, (-5.25, -0.55)),
    ("mass percent", "share of all the mass", cfg.SOLUTION_MASS, (5.25, -0.55)),
    ("normality", "eq/L for a stated reaction", cfg.EQUIVALENT, (-4.9, -3.05)),
    ("ppm · ppb", "tiny ratios, stated basis", cfg.GOLD, (4.9, -3.05)),
]


class Scene20Finale(Scene):
    def construct(self) -> None:
        play_scene(self)


def node(name: str, what: str, color: str, at) -> VGroup:
    title = txt(name, cfg.FONT["body"], color)
    sub = txt(what, cfg.FONT["tiny"], cfg.WHITE)
    body = VGroup(title, sub).arrange(DOWN, buff=0.1)
    box = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.36, corner_radius=0.2, stroke_color=color,
                           stroke_width=3, fill_color=cfg.PANEL, fill_opacity=0.9)
    group = VGroup(box, body.move_to(box)).move_to([at[0], at[1], 0])
    group.box = box
    return group


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "20")
    stage, glass, swarm = solution_stage(BASE, zoom=1.15, solvent=500, solute=5, seed=1, solute_radius=0.12)
    swarm.solute_glow = 1.0
    show(scene, stage, 1.4)
    question = result_label("How concentrated is it?", cfg.WHITE, cfg.FONT["section"]).move_to([0, 2.9, 0])
    scene.play(FadeIn(question, shift=DOWN * 0.15), run_time=1.0)

    # --- 2. Every number has a meaning ----------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(glass.set_glow(0.6), set_attr(stage, swarm, "solute_glow", 1.6), run_time=1.2)

    nodes = [node(*spec[:3], spec[3]) for spec in NODES]
    centre = np.array([0.0, -1.5, 0.0])
    wires = [glow_line(centre + (n.get_center() - centre) * 0.28, n.box.get_edge_center(RIGHT if n.get_x() < 0 else LEFT),
                       spec[2], 2.0) for n, spec in zip(nodes, NODES)]

    def reveal(indices, *extra):
        scene.play(*[Create(wires[i]) for i in indices], *[FadeIn(nodes[i], scale=0.9) for i in indices], *extra, run_time=1.2)

    # --- 3. Molarity and molality ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(question), run_time=0.4)
    reveal([0], glass.set_glow(1.0))
    reveal([1], glass.set_glow(0.0), set_attr(stage, swarm, "solvent_glow", 1.0))

    # --- 4. Mole fraction and mass percent ------------------------------------------------------------------------------
    beat(scene, t, 3)
    reveal([2], set_attr(stage, swarm, "solvent_glow", 0.0))
    reveal([3])

    # --- 5. Normality and ppm ---------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    reveal([4])
    reveal([5])

    # --- 6. One system, connected --------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    density = glow_line(nodes[0].box.get_right(), nodes[1].box.get_left(), cfg.SOLUTION_MASS, 2.2)
    density_tag = txt("density", cfg.FONT["small"], cfg.SOLUTION_MASS).next_to(density, UP, buff=0.12)
    feq_tag = eq(r"= c \times z", cfg.FONT["small"], cfg.EQUIVALENT).next_to(nodes[4], UP, buff=0.15)
    scene.play(Create(density), FadeIn(density_tag), run_time=1.0)
    scene.play(FadeIn(feq_tag, shift=LEFT * 0.15), Indicate(nodes[4].box, color=cfg.EQUIVALENT), run_time=1.0)
    scene.play(LaggedStart(*[Indicate(n.box, color=cfg.WHITE, scale_factor=1.04) for n in nodes], lag_ratio=0.12),
               run_time=2.0)

    # --- 7. Don't memorise: ask one question --------------------------------------------------------------------------------
    beat(scene, t, 6)
    web = VGroup(*nodes, *wires, density, density_tag, feq_tag)
    scene.play(FadeOut(web), run_time=1.0)
    ask = txt("Don't memorise. Ask one question.", cfg.FONT["body"], cfg.CYAN).move_to([0, 2.9, 0])
    scene.play(FadeIn(ask, shift=DOWN * 0.15), run_time=0.9)

    # --- 8. What are we actually comparing? -------------------------------------------------------------------------------------
    beat(scene, t, 7)
    big = result_label("What are we actually comparing?", cfg.GOLD, cfg.FONT["title"]).move_to([0, 2.85, 0])
    fit_width(big, 13.6)
    scene.play(fade_through(ask, big), stage.zoom_to(1.25), stage.glide([0.0, -3.1, 0.0]), run_time=1.2)
    scene.remove(ask)
    scene.play(Indicate(big, color=cfg.WHITE, scale_factor=1.04), run_time=1.0)

    # --- 9. Title over the solution as we pull back ----------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(big), stage.zoom_to(3.0), stage.glide([0.0, -3.8, 0.0]), run_time=1.6)
    veil = Rectangle(width=16.5, height=9.5, stroke_width=0, fill_color=cfg.BG, fill_opacity=0.0)
    scene.add(veil)
    card = title_card("CONCENTRATION", "Explained Visually").move_to([0, 0.4, 0])
    scene.play(veil.animate.set_fill(opacity=0.45), FadeIn(card, shift=UP * 0.2), run_time=1.4)
    scene.play(stage.zoom_to(1.6), stage.glide([0.0, -3.2, 0.0]), veil.animate.set_fill(opacity=0.3),
               card.animate.scale(1.04), run_time=9.2, rate_func=smooth)
    end_scene(scene, t, cfg.SCENE_DURATIONS["20"])
