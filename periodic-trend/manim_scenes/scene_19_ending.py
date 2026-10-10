"""Ending: from periodic trends to the next question — why do atoms bond?

The table fades until only sodium and chlorine remain; their tiles become the
film's atoms, the properties the film built connect around them, and the two
atoms drift close enough for their clouds to meet — the opening frame of the
next episode.
"""

from manim_scenes.common import *

PITCH = 0.62
CENTER = DOWN * 0.45
NA_AT = np.array([-3.4, 0.25, 0])
CL_AT = np.array([3.4, 0.25, 0])


class Scene19Ending(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "19")

    # --- 1. Only two atoms remain ------------------------------------------------------------------
    table = periodic_table(pitch=PITCH, center=CENTER)
    scene.play(FadeIn(table), run_time=0.8)
    keep = {11, 17}
    scene.play(*[table.tiles[z].animate.set_opacity(0.08) for z in table.tiles if z not in keep],
               *[Indicate(table.tiles[z], color=cfg.WHITE, scale_factor=1.3) for z in keep], run_time=1.4)
    sodium = Atom(1.75, table.tiles[11].get_center(), charge="+11", core=0.8, count=260, seed=191)
    chlorine = Atom(1.15, table.tiles[17].get_center(), charge="+17", core=0.45, count=380, seed=192)
    sodium.cloud.set_radius(0.05)
    chlorine.cloud.set_radius(0.05)
    scene.play(FadeOut(table), run_time=0.4)
    scene.play(FadeIn(sodium), FadeIn(chlorine), run_time=0.4)
    scene.play(Glide(sodium, NA_AT), Glide(chlorine, CL_AT), *sodium.resize(1.75),
               *chlorine.resize(1.15), run_time=1.0)
    names = VGroup(txt("sodium", cfg.FONT["label"], cfg.BLUE).move_to(NA_AT + DOWN * 2.45),
                   txt("chlorine", cfg.FONT["label"], cfg.GREEN).move_to(CL_AT + DOWN * 2.45))
    scene.play(FadeIn(names), run_time=0.6)

    # --- 2. Not just what they are: how they behave ----------------------------------------------------
    beat(scene, t, 1)
    what = txt("what the elements are", cfg.FONT["body"], cfg.MUTED)
    how = txt("how they behave", cfg.FONT["body"], cfg.GOLD)
    line = VGroup(what, eq(r"\rightarrow", cfg.FONT["body"]), how).arrange(RIGHT, buff=0.35).move_to([0, 3.0, 0])
    fit_width(line, 13.4)
    scene.play(FadeIn(what, shift=DOWN * 0.1), run_time=0.7)
    scene.play(FadeIn(line[1]), FadeIn(how, shift=LEFT * 0.2), run_time=0.9)

    # --- 3. The patterns are connected ------------------------------------------------------------------
    beat(scene, t, 2)
    words = (("size", cfg.CYAN), ("ionization", cfg.GOLD), ("electronegativity", cfg.CYAN), ("reactivity", cfg.ORANGE))
    nodes = VGroup(*[chip(word, colour, cfg.FONT["small"]) for word, colour in words])
    spots = ([0, 1.55, 0], [0, 0.45, 0], [0, -0.65, 0], [0, -1.75, 0])
    for node, spot in zip(nodes, spots):
        node.move_to(spot)
    links = VGroup()
    for node in nodes:
        for atom_at in (NA_AT, CL_AT):
            side = node.get_left() if atom_at[0] < 0 else node.get_right()
            links.add(Line(atom_at + (side - atom_at) / np.linalg.norm(side - atom_at) * 1.3, side,
                           stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.6))
    scene.play(FadeOut(line), LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes], lag_ratio=0.25), run_time=1.6)
    scene.play(Create(links), run_time=1.4)
    scene.play(LaggedStart(*[Indicate(n, color=cfg.WHITE, scale_factor=1.05) for n in nodes], lag_ratio=0.2), run_time=1.6)

    # --- 4. Close enough to interact ---------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(nodes, links, names)), run_time=0.7)
    scene.play(Glide(sodium, [-1.55, 0.25, 0]), Glide(chlorine, [1.4, 0.25, 0]), run_time=2.4, rate_func=smooth)
    meet = BondCloud([-1.55, 0.25, 0], [1.4, 0.25, 0], count=220, seed=193, width=0.55, glow=0.22, lean=0.4)
    scene.play(FadeIn(meet), run_time=1.0)

    # --- 5. Why do atoms bond at all? -----------------------------------------------------------------------
    beat(scene, t, 4)
    question = Text("Why do atoms bond at all?", font=cfg.TITLE_FONT, weight=BOLD, font_size=64, color=cfg.GOLD)
    question.set_stroke("#351F05", width=3, opacity=0.8, background=True)
    fit_width(question, 13.4)
    question.move_to([0, 2.95, 0])
    scene.play(Write(question), run_time=1.6)

    # --- 6. Next episode ----------------------------------------------------------------------------------------
    beat(scene, t, 5)
    next_card = VGroup(txt("NEXT", cfg.FONT["small"], cfg.MUTED),
                       txt("Chemical Bonding, Explained Visually", cfg.FONT["section"], cfg.CYAN)).arrange(DOWN, buff=0.15)
    fit_width(next_card, 13.4)
    next_card.move_to([0, -3.1, 0])
    rule = Line(LEFT * 4.6, RIGHT * 4.6, stroke_color=cfg.CYAN, stroke_width=3).next_to(next_card, UP, buff=0.22)
    scene.play(Create(rule), FadeIn(next_card, shift=UP * 0.15), run_time=1.2)
    scene.play(Indicate(next_card[1], color=cfg.WHITE, scale_factor=1.04), run_time=1.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["19"])
