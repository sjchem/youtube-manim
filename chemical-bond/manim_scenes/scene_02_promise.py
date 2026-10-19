"""The promise: from Part 4's periodic trends to one principle for every bond.

The table is assembled from the filling model (``utils.physics_models``),
exactly as in the periodic-table films. Sodium's ionization energy and
chlorine's electron affinity come from ``utils.bond_data``. The three
memorised bond types are crossed out and replaced by three ingredients and a
single inequality, which the rest of the film keeps returning to.
"""

from manim_scenes.common import *

PITCH = 0.68
TABLE_AT = DOWN * 0.45


class Scene02Promise(Scene):
    def construct(self) -> None:
        play_scene(self)


def valley_sketch(width: float = 4.4, depth: float = 1.3, color: str = cfg.ENERGY) -> VGroup:
    """A small, unlabelled energy valley (the film's recurring icon)."""
    axes = Axes(x_range=[0, 320, 100], y_range=[-500, 400, 200], x_length=width, y_length=depth * 2.2,
                tips=False, axis_config={"stroke_color": cfg.MUTED, "stroke_width": 2, "include_ticks": False})
    depth_kj, r_e, a = H2
    start_r = bm.morse_inverse(380, depth_kj, r_e, a)
    curve = axes.plot(lambda r: float(bm.morse(r, depth_kj, r_e, a)), x_range=[start_r, 320, 1], color=color,
                      stroke_width=6, use_smoothing=False)
    under = curve.copy().set_stroke(color, width=18, opacity=0.15)
    group = VGroup(axes, under, curve)
    group.axes, group.curve = axes, curve
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "Last time: periodic trends")

    # --- 1. The table from the last film ---------------------------------------------------------------
    table = periodic_table(pitch=PITCH, center=TABLE_AT)
    columns = sorted({pm.position(z)[1] for z in table.tiles})
    waves = [AnimationGroup(*[FadeIn(table.tiles[z], shift=DOWN * 0.15) for z in table.tiles if pm.position(z)[1] == c])
             for c in columns]
    scene.play(LaggedStart(*waves, lag_ratio=0.08), run_time=2.2)
    na, cl = table.tiles[pm.z_of("Na")], table.tiles[pm.z_of("Cl")]
    scene.play(*[table.tiles[z].animate.set_opacity(0.14) for z in table.tiles if z not in (11, 17)],
               na.animate.scale(1.35), cl.animate.scale(1.35), run_time=1.4)
    frames = VGroup(glow_frame(na, cfg.CATION, buff=0.06), glow_frame(cl, cfg.ANION, buff=0.06))
    scene.play(Create(frames), run_time=0.8)
    dismiss_opening_title(scene, t, head)

    # --- 2. Sodium lets go; chlorine takes ---------------------------------------------------------------
    beat(scene, t, 1)
    gives = VGroup(txt("electron out", cfg.FONT["small"], cfg.WHITE),
                   txt(f"costs {bd.IONIZATION_KJ['Na']} kJ/mol", cfg.FONT["small"], cfg.REQUIRED)).arrange(DOWN, buff=0.12)
    gives.move_to([-1.8, 2.75, 0])
    takes = VGroup(txt("electron in", cfg.FONT["small"], cfg.WHITE),
                   txt(f"releases {bd.ELECTRON_AFFINITY_KJ['Cl']} kJ/mol", cfg.FONT["small"], cfg.RELEASED)).arrange(DOWN, buff=0.12)
    takes.move_to([4.2, 2.75, 0])
    link_na = Line(gives.get_bottom() + DOWN * 0.08, na.get_top() + UP * 0.08, stroke_color=cfg.CATION, stroke_width=3)
    link_cl = Line(takes.get_bottom() + DOWN * 0.08, cl.get_top() + UP * 0.08, stroke_color=cfg.ANION, stroke_width=3)
    scene.play(*[table.tiles[z].animate.set_opacity(0.04) for z in table.tiles if z not in (11, 17)],
               FadeIn(gives, shift=DOWN * 0.1), Create(link_na), run_time=0.9)
    leaving = glow_dot(na.get_center(), 0.12)
    scene.play(FadeIn(leaving, scale=0.5), leaving.animate.shift(UP * 0.9 + RIGHT * 0.5), run_time=1.0)
    scene.play(FadeIn(takes, shift=DOWN * 0.1), Create(link_cl), run_time=0.9)
    arriving = glow_dot(cl.get_center() + UP * 0.9 + LEFT * 0.5, 0.12)
    scene.play(FadeOut(leaving), FadeIn(arriving), arriving.animate.move_to(cl.get_center()), run_time=1.0)
    scene.play(FadeOut(arriving, scale=0.4), Indicate(cl, color=cfg.WHITE, scale_factor=1.15), run_time=0.8)

    # --- 3. What happens when they meet? -------------------------------------------------------------------
    beat(scene, t, 2)
    sodium = Atom(1.25, [-3.6, 0.1, 0], charge="Na", core=0.55, count=260, core_count=150, seed=21, glow=0.12)
    chlorine = Atom(0.95, [3.6, 0.1, 0], charge="Cl", core=0.45, count=360, core_count=140, seed=22, glow=0.18)
    for atom in (sodium, chlorine):
        atom.cloud.set_radius(0.05)
        if atom.core:
            atom.core.set_radius(0.03)
    scene.play(FadeOut(VGroup(gives, takes, link_na, link_cl, frames)),
               *[table.tiles[z].animate.set_opacity(0) for z in table.tiles], run_time=0.8)
    scene.remove(table)
    scene.add(sodium, chlorine)
    scene.play(*sodium.resize(1.25, 0.55), *chlorine.resize(0.95, 0.45), run_time=1.0)
    meet = txt("?", 120, cfg.GOLD).move_to([0, 0.1, 0])
    scene.play(sodium.glide([-2.6, 0.1, 0]), chlorine.glide([2.6, 0.1, 0]), FadeIn(meet, scale=0.5), run_time=1.6)

    # --- 4. Three boxes of rules -------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(meet), FadeOut(sodium, scale=0.7), FadeOut(chlorine, scale=0.7), run_time=0.7)
    names = ("covalent", "ionic", "metallic")
    colours = (cfg.CYAN, cfg.CATION, cfg.METAL_CORE)
    cards = VGroup()
    for name, colour in zip(names, colours):
        box = panel(3.9, 3.0, colour, 0.85)
        title = txt(name, cfg.FONT["body"], colour).move_to(box.get_top() + DOWN * 0.55)
        rules = VGroup(*[Line(LEFT * 1.25, RIGHT * (1.25 - 0.35 * k), stroke_color=cfg.MUTED, stroke_width=6,
                              stroke_opacity=0.7) for k in range(3)]).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        rules.next_to(title, DOWN, buff=0.45)
        cards.add(VGroup(box, title, rules))
    cards.arrange(RIGHT, buff=0.55).move_to([0, 0.2, 0])
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.25), run_time=1.5)
    memorise = txt("Three separate rules?", cfg.FONT["body"], cfg.MUTED).move_to([0, -2.55, 0])
    scene.play(FadeIn(memorise, shift=UP * 0.1), run_time=0.7)
    strikes = VGroup(*[strike(c[2], cfg.REPEL) for c in cards])
    scene.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.2), run_time=1.0)

    # --- 5. Build them from three ingredients ---------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(cards, strikes, memorise), shift=DOWN * 0.2), run_time=0.7)
    nucleus = nucleus_core("+", 0.42)
    electron = glow_dot(ORIGIN, 0.2)
    energy_icon = valley_sketch(2.6, 0.75)
    tokens = VGroup(
        VGroup(nucleus, txt("nuclei", cfg.FONT["label"], cfg.NUCLEUS_COLOR)).arrange(DOWN, buff=0.5),
        VGroup(electron, txt("electrons", cfg.FONT["label"], cfg.CYAN)).arrange(DOWN, buff=0.5),
        VGroup(energy_icon, txt("energy", cfg.FONT["label"], cfg.ENERGY)).arrange(DOWN, buff=0.25),
    )
    plus = [eq("+", cfg.FONT["title"], cfg.MUTED) for _ in range(2)]
    row = VGroup(tokens[0], plus[0], tokens[1], plus[1], tokens[2]).arrange(RIGHT, buff=0.7).move_to([0, 0.3, 0])
    for token in tokens:
        token[1].align_to(tokens[2][1], DOWN)
    for index, item in enumerate((tokens[0], plus[0], tokens[1], plus[1], tokens[2])):
        scene.play(FadeIn(item, shift=UP * 0.2, scale=0.9), run_time=0.55)

    # --- 6. The one idea --------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(row.animate.scale(0.62).move_to([0, 2.55, 0]), run_time=1.0)
    rule = eq(r"E_{\text{together}} \;<\; E_{\text{apart}}", 64, cfg.WHITE).move_to([0, 0.75, 0])
    rule[0][0].set_color(cfg.ENERGY)
    scene.play(Write(rule), run_time=1.6)
    frame = glow_frame(rule, cfg.ENERGY, buff=0.25)
    scene.play(Create(frame), run_time=0.8)
    valley = valley_sketch(5.2, 1.0).move_to([0, -2.15, 0])
    scene.play(Create(valley.curve), FadeIn(valley[1]), FadeIn(valley.axes), run_time=1.4)
    marble = glow_dot(valley.axes.c2p(300, float(bm.morse(300, *H2))), 0.14, cfg.ENERGY)
    path = valley.axes.plot(lambda r: float(bm.morse(r, *H2)), x_range=[H2[1], 300, 1]).reverse_points()
    scene.play(FadeIn(marble, scale=0.5), run_time=0.4)
    scene.play(MoveAlongPath(marble, path), run_time=2.2, rate_func=rush_into)
    scene.play(Flash(marble, color=cfg.ENERGY, line_length=0.3, num_lines=10), run_time=0.8)
    apart = txt("apart", cfg.FONT["small"], cfg.MUTED).next_to(valley.axes.c2p(300, 0), UP, buff=0.2)
    together = txt("together", cfg.FONT["small"], cfg.RELEASED).next_to(valley.axes.c2p(H2[1], -H2[0]), RIGHT, buff=0.45)
    scene.play(FadeIn(apart, shift=DOWN * 0.1), run_time=0.7)
    scene.play(FadeIn(together, shift=LEFT * 0.1), Indicate(rule[0][:9], color=cfg.RELEASED, scale_factor=1.05), run_time=1.2)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
