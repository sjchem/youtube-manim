"""Scene 12 — mole fraction as a population: a turning 3D crowd of exactly
one glucose and one hundred waters (the reference solution's 0.100 : 10.0
mol ratio, scaled down). A ring picks molecules at random; the chance of
glucose is the mole fraction. Picks come from ``config.SEED``.
"""

from manim_scenes.common import *

RX = 3.6
GLUCOSE = 100     # the swarm stores solvent first, so index 100 is the glucose
PICKS = [int(i) for i in np.random.default_rng(cfg.SEED + 12).choice(101, 3, replace=True)]


class Scene12MoleFraction(Scene):
    def construct(self) -> None:
        play_scene(self)


def crowd_stage(at=(-3.75, -0.35, 0), zoom: float = 1.55) -> tuple[Stage, Swarm]:
    stage = Stage(at, zoom=zoom, yaw=0.4, pitch=0.35, spin=0.22, sway=0.08)
    swarm = Swarm(stage, Box(half=2.0), solvent=100, solute=1, seed=cfg.SEED + 12, style="spheres",
                  solvent_radius=0.13, solute_radius=0.19, amplitude=0.09)
    return stage, swarm


def pick_ring(swarm: Swarm, index: int, color: str) -> VMobject:
    return always_redraw(lambda: VGroup(
        Circle(radius=0.44, stroke_color=color, stroke_width=12, stroke_opacity=0.25).move_to(swarm.screen[index]),
        Circle(radius=0.38, stroke_color=color, stroke_width=5).move_to(swarm.screen[index])))


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "Mole fraction: pick a molecule")
    stage, swarm = crowd_stage()
    show(scene, stage, 1.6)
    grab = VGroup(txt("grab one molecule", cfg.FONT["body"], cfg.WHITE),
                  txt("at random", cfg.FONT["body"], cfg.CYAN)).arrange(DOWN, buff=0.15).move_to([RX, 0.6, 0])
    scene.play(FadeIn(grab, shift=LEFT * 0.2), run_time=1.0)

    # --- 2. Chance it's glucose? ----------------------------------------------------------------------------
    beat(scene, t, 1)
    chance = eq(r"P(\text{glucose}) = \,?", cfg.FONT["section"], cfg.GOLD).move_to([RX, 0.6, 0])
    scene.play(fade_through(grab, chance), run_time=1.0)
    scene.remove(grab)

    # --- 3. Not litres, not kilograms: the population -------------------------------------------------------------
    beat(scene, t, 2)
    nots = VGroup(txt("litres", cfg.FONT["label"], cfg.MUTED), txt("kilograms", cfg.FONT["label"], cfg.MUTED))
    nots.arrange(RIGHT, buff=0.8).move_to([RX, 2.3, 0])
    strikes = VGroup(*[strike(n) for n in nots])
    population = txt("only the population", cfg.FONT["body"], cfg.AMOUNT).move_to([RX, -1.0, 0])
    scene.play(FadeIn(nots), run_time=0.7)
    scene.play(Create(strikes), run_time=0.7)
    scene.play(FadeIn(population, shift=UP * 0.15), run_time=0.8)

    # --- 4. 0.100 : 10.0 mol = 1 : 100 --------------------------------------------------------------------------------
    beat(scene, t, 3)
    amounts = eq([rf"{N_SOLUTE}", r"\ :\ ", rf"{N_SOLVENT}\ \mathrm{{mol}}"], cfg.FONT["section"]).move_to([RX, 2.2, 0])
    amounts[0].set_color(cfg.SOLUTE)
    amounts[2].set_color(cfg.SOLVENT)
    ratio = eq([r"1", r"\ :\ ", r"100"], cfg.FONT["title"]).move_to([RX, 0.6, 0])
    ratio[0].set_color(cfg.SOLUTE)
    ratio[2].set_color(cfg.SOLVENT)
    scene.play(FadeOut(VGroup(nots, strikes, population, chance)), run_time=0.6)
    scene.play(Write(amounts), run_time=1.3)
    scene.play(FadeIn(ratio, shift=DOWN * 0.3), run_time=1.3)

    # --- 5. A scaled-down crowd of 101 -------------------------------------------------------------------------------------
    beat(scene, t, 4)
    crowd = VGroup(txt("101 molecules", cfg.FONT["body"], cfg.WHITE),
                   txt("1 glucose · 100 water", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.15)
    crowd.move_to([RX, -1.2, 0])
    scene.play(FadeIn(crowd, shift=UP * 0.15), set_attr(stage, swarm, "r_solute", 0.25), run_time=1.0)
    scene.play(set_attr(stage, swarm, "r_solute", 0.19), run_time=1.0)

    # --- 6. Pick: water, water, water ------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(amounts, ratio, crowd)), run_time=0.5)
    tally = VGroup()
    for k, index in enumerate(PICKS):
        ring = pick_ring(swarm, index, cfg.CYAN)
        scene.add(ring)
        scene.play(FadeIn(ring, scale=1.6), run_time=0.5)
        word = txt("water", cfg.FONT["body"], cfg.SOLVENT).move_to([RX, 2.0 - 1.0 * k, 0])
        tally.add(word)
        scene.play(FadeIn(word, shift=LEFT * 0.2), run_time=0.5)
        narration_wait(scene, 0.6)
        ring.clear_updaters()
        scene.play(FadeOut(ring), run_time=0.4)

    # --- 7. About 101 independent picks on average ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    gold_ring = pick_ring(swarm, GLUCOSE, cfg.GOLD)
    scene.add(gold_ring)
    average = VGroup(txt("about", cfg.FONT["label"], cfg.MUTED),
                     txt(f"{pm.expected_picks(REF.x_solute):.0f} picks", cfg.FONT["section"], cfg.GOLD),
                     txt("per glucose, on average", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.15)
    average.move_to([RX, 0.4, 0])
    scene.play(FadeOut(tally), FadeIn(gold_ring, scale=1.6), run_time=0.5)
    scene.play(FadeIn(average, shift=UP * 0.15), run_time=0.6)

    # --- 8. That chance is the mole fraction ------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    rule = fraction("x_i", "n_i", r"\sum_j n_j", cfg.AMOUNT, cfg.WHITE, cfg.FONT["title"]).move_to([RX, 1.9, 0])
    gold_ring.clear_updaters()
    scene.play(FadeOut(average), FadeOut(gold_ring), run_time=0.4)
    scene.play(Write(rule), run_time=1.3)
    name = txt("mole fraction", cfg.FONT["body"], cfg.AMOUNT).next_to(rule, DOWN, buff=0.35)
    scene.play(FadeIn(name), run_time=0.7)

    # --- 9. Substitute ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    sub = eq([r"x_{\text{glucose}}", "=", r"\frac{", N_SOLUTE, "}{", rf"{N_SOLUTE} + {N_SOLVENT}", "}"], cfg.FONT["section"])
    sub[3].set_color(cfg.SOLUTE)
    sub[5].set_color(cfg.WHITE)
    fit_width(sub, 7.6)
    sub.move_to([RX, -0.35, 0])
    scene.play(FadeOut(name), run_time=0.4)
    scene.play(Write(sub), run_time=1.3)

    # --- 10. 0.00990 -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    answer = boxed(eq(rf"x_{{\text{{glucose}}}} \approx {X_TEXT}", cfg.FONT["section"], cfg.RESULT)).move_to([RX, -2.4, 0])
    scene.play(FadeIn(answer, scale=1.08), run_time=1.0)
    scene.play(Indicate(answer, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)

    # --- 11. The bottom is the total ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    brace = Brace(sub[5], DOWN, color=cfg.GOLD)
    total = txt("the total, glucose included", cfg.FONT["small"], cfg.GOLD).next_to(brace, DOWN, buff=0.12)
    scene.play(FadeOut(answer), run_time=0.4)
    scene.play(GrowFromCenter(brace), FadeIn(total), set_attr(stage, swarm, "solvent_glow", 0.8), run_time=1.0)
    scene.play(set_attr(stage, swarm, "solvent_glow", 0.0), run_time=0.8)

    # --- 12. No units -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    units = eq(r"\frac{\mathrm{mol}}{\mathrm{mol}}", cfg.FONT["section"], cfg.MUTED).move_to([RX - 1.4, -2.4, 0])
    cancel = VGroup(strike(units[0][0:3], cfg.WARNING, 6), strike(units[0][4:7], cfg.WARNING, 6))
    pure = txt("a pure number, 0 to 1", cfg.FONT["small"], cfg.AMOUNT).next_to(units, RIGHT, buff=0.4)
    scene.play(FadeOut(VGroup(brace, total)), run_time=0.4)
    scene.play(FadeIn(units), run_time=0.5)
    scene.play(Create(cancel), FadeIn(pure), run_time=1.0)

    # --- 13. It doesn't care about temperature or volume ---------------------------------------------------------------------------------------
    beat(scene, t, 12)
    indifferent = chip("fixed composition: x stays fixed", cfg.RESULT).move_to([RX, -2.4, 0])
    scene.play(FadeOut(VGroup(units, cancel, pure)), run_time=0.4)
    scene.play(FadeIn(indifferent, shift=UP * 0.15), run_time=0.6)
    scene.play(set_attr(stage, swarm, "speed", 2.4), set_attr(stage, swarm, "amplitude", 0.16), run_time=6.0)
    scene.play(set_attr(stage, swarm, "speed", 1.0), set_attr(stage, swarm, "amplitude", 0.09), run_time=6.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
