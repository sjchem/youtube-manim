"""Scene 09 — two cracks in the model. Two of the six purple postulate chips
return: (2) negligible volume, over a glass box of molecules on the left, and
(3) no forces between, over a box on the right.

Left: in ordinary air the molecules fill a few hundredths of a percent of the
space (``pm.molecular_volume_fraction``, b/4 per mole at 1 bar and 300 K).
Then the piston squeezes the box to a quarter of its volume; the molecules are
hard spheres (``pm.HardSphereGas``) and crowd against one another, and chip 2
cracks red.

Right: a dilute gas, molecules far apart. The box is compressed and cooled,
the molecules slow down, and green links join near neighbours. Between the
boxes an inset replays two real encounters computed in the Lennard-Jones
potential (``pm.lj_encounter``): a fast pair passes almost straight; a slow
pair at the same impact parameter is pulled in, swings round and lingers
together (a green link while they are within reach). Chip 3 cracks.

Finally a pressure-temperature map: the ideal gas works at low P and high T
(bottom right); squeezing exposes size (red), cooling exposes attraction (green).
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d, chip_focus, crack, rule_chip
from manim_scenes.kit_d import PairLinks, at_word

BOX_X = 4.7
BOX_Y = -1.2
CHIP_Y = 2.55
INSET = np.array([0.0, -0.9, 0.0])
INSET_SCALE = 0.33           # screen units per molecular diameter (sigma)


class Scene09TwoCracks(Scene):
    def construct(self) -> None:
        play_scene(self)


def encounter(v: float, color: str = cfg.MOLECULE) -> SimpleNamespace:
    """Two molecules replaying ``pm.lj_encounter(v)``; ``clock`` (Knob) is simulation time."""
    times, rel = pm.lj_encounter(v)
    clock = Knob(0.0)

    def at(k: int) -> np.ndarray:
        r = np.array([np.interp(clock.value, times, rel[:, 0]), np.interp(clock.value, times, rel[:, 1])])
        return INSET + np.array([*((-0.5 if k == 0 else 0.5) * r * INSET_SCALE * 2), 0.0])

    def trail(k: int) -> VMobject:
        upto = times <= clock.value
        if upto.sum() < 2:
            return VMobject()
        pts = [INSET + np.array([*((-0.5 if k == 0 else 0.5) * p * INSET_SCALE * 2), 0.0]) for p in rel[upto][::6]]
        pts.append(at(k))
        return polyline(pts, cfg.GOLD, width=3.5, opacity=0.8)

    def link() -> VMobject:
        a, b = at(0), at(1)
        if np.linalg.norm(b - a) > 2.05 * INSET_SCALE * 2:
            return VMobject()
        line = Line(a, b, stroke_color=cfg.ATTRACT, stroke_width=5)
        return VGroup(line.copy().set_stroke(width=14, opacity=0.18), line)

    trails = VGroup(live(VGroup(), lambda: trail(0)), live(VGroup(), lambda: trail(1)))
    pull = live(VGroup(), link)
    balls = VGroup(live(VGroup(), lambda: bead(at(0), color, 0.16)), live(VGroup(), lambda: bead(at(1), color, 0.16)))
    group = VGroup(trails, pull, balls)
    return SimpleNamespace(group=group, clock=clock, end=float(times[-1]), parts=[*trails, pull, *balls])


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "09", TITLES["09"])

    # --- 0. Two postulates return --------------------------------------------------------------------------------------
    chip_v = rule_chip(2, "negligible\nvolume", width=4.3).move_to([-BOX_X, CHIP_Y, 0])
    chip_f = rule_chip(3, "no forces\nbetween", width=4.3).move_to([BOX_X, CHIP_Y, 0])
    left = GasBox((-BOX_X, BOX_Y, 0), half_x=1.2, half_z=0.9, height=2.5, floor=-1.25, lid="piston", zoom=1.12, yaw=-0.45,
                  pitch=0.3, speed=1.4, radius=0.1, spark_axes=(1,),
                  model=pm.HardSphereGas(64, cfg.SEED + 90, 0.1, (2.4, 2.5, 1.8)))
    right = GasBox((BOX_X, BOX_Y, 0), count=56, half_x=1.2, half_z=0.9, height=2.5, floor=-1.25, lid="piston", zoom=1.12,
                   yaw=0.45, pitch=0.3, speed=1.6, radius=0.09, seed=cfg.SEED + 91)
    links = PairLinks(right.cloud, cutoff=0.5)
    right.stage.add_body(links)
    for box in (left, right):
        box.stage.presence = 0.0
        box.stage.refresh()
        scene.add(box.stage)
    scene.play(FadeIn(chip_v, shift=RIGHT * 0.3), FadeIn(chip_f, shift=LEFT * 0.3), left.stage.fade(left.stage, 1.0),
               right.stage.fade(right.stage, 1.0), run_time=1.4)
    play_in(scene, t, 1, *chip_focus(chip_v, False), *chip_focus(chip_f, False), run_time=0.8)

    # --- 1. Negligible volume: true for ordinary air -------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(*chip_focus(chip_v, True), *left.stage.turn(yaw=-0.3), run_time=0.9)
    at_word(scene, t, 1, "air", lead=0.2)
    frac = pm.molecular_volume_fraction()
    head = txt("in air, molecules fill", cfg.FONT["small"], cfg.MUTED)
    value = txt(f"{fx(100 * frac, 2)} %", cfg.FONT["hero"], cfg.WHITE)
    note = txt("of the space", cfg.FONT["small"], cfg.MUTED)
    fill_info = VGroup(head, value, note).arrange(DOWN, buff=0.28).move_to([0, 0.75, 0])
    scale_note = txt("(drawn enlarged)", cfg.FONT["tiny"], cfg.MUTED).move_to([-BOX_X, -3.55, 0])
    scene.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
    scene.play(FadeIn(value, scale=1.2), FadeIn(note), FadeIn(scale_note), run_time=1.0)
    at_word(scene, t, 1, "thousandth", lead=0.4)
    tiny = txt("< 1/1000", cfg.FONT["section"], cfg.GREEN).next_to(fill_info, DOWN, buff=0.3)
    play_in(scene, t, 2, FadeIn(tiny, shift=UP * 0.1), Indicate(value, color=cfg.GREEN, scale_factor=1.08), run_time=1.2)

    # --- 2. Squeeze hard: the molecules' own size matters -----------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(fill_info, tiny)), run_time=0.6)
    scene.play(left.volume_to(0.27, rate_func=smooth), left.stage.zoom_to(1.2), run_time=3.6)
    at_word(scene, t, 2, "size", lead=0.3)
    mark_v, turn_red = crack(chip_v, seed=1)
    crowded = txt("size matters", cfg.FONT["label"], cfg.SIZE).move_to([-BOX_X, -3.55, 0])
    play_in(scene, t, 3, *turn_red, fade_through(scale_note, crowded), run_time=1.2)
    scene.add(mark_v)
    scene.remove(scale_note)

    # --- 3. No attraction: fine while molecules are far apart --------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*chip_focus(chip_f, True), *right.stage.turn(yaw=0.3), right.stage.zoom_to(1.2), run_time=1.0)
    at_word(scene, t, 3, "far", lead=0.2)
    apart = txt("far apart", cfg.FONT["label"], cfg.MOLECULE).move_to([BOX_X, -3.55, 0])
    scene.play(FadeIn(apart, shift=UP * 0.1), right.cloud.tween("radius", 0.13, rate_func=there_and_back), run_time=1.4)
    play_in(scene, t, 4, *right.stage.turn(yaw=0.42), run_time=2.0)

    # --- 4. Closer and colder: attraction shapes the motion -----------------------------------------------------------------
    beat(scene, t, 4)
    back = panel(5.6, 3.0, cfg.MUTED, 0.6).move_to(INSET)
    fast = encounter(pm.LJ_FAST)
    slow = encounter(pm.LJ_SLOW)
    scene.play(right.volume_to(0.5), right.heat_to(110.0),
               set_attr(right.stage, links, "alpha", 1.0), right.stage.zoom_to(1.25), run_time=2.6)
    cold = txt("closer, colder", cfg.FONT["label"], cfg.COLD_COLOR).move_to([BOX_X, -3.55, 0])
    scene.play(fade_through(apart, cold), FadeIn(back), run_time=0.8)
    scene.remove(apart)
    fast_tag = txt("fast", cfg.FONT["small"], cfg.FAST).next_to(back, UP, buff=0.12)
    scene.add(fast.group)
    scene.play(FadeIn(fast_tag), fast.clock.to(fast.group, fast.end, rate_func=linear), run_time=1.1)
    at_word(scene, t, 4, "bend", lead=0.6)
    slow_tag = txt("slow: bends, lingers", cfg.FONT["small"], cfg.ATTRACT).next_to(back, UP, buff=0.12)
    for part in fast.parts:
        part.clear_updaters()
    scene.play(FadeOut(fast.group), fade_through(fast_tag, slow_tag), run_time=0.5)
    scene.remove(fast_tag)
    scene.add(slow.group)
    scene.play(slow.clock.to(slow.group, slow.end, rate_func=linear), run_time=min(5.4, time_left(scene, t, 5) - 1.3))
    mark_f, turn_red_f = crack(chip_f, seed=2)
    play_in(scene, t, 5, *turn_red_f, run_time=1.0)
    scene.add(mark_f)

    # --- 5. Where the ideal gas works: low P, high T -----------------------------------------------------------------------
    beat(scene, t, 5)
    for part in slow.parts:
        part.clear_updaters()
    hide(scene, left.stage, 0.9, FadeOut(VGroup(slow.group, back, slow_tag, crowded, cold)))
    hide(scene, right.stage, 0.5)
    axes = plot_axes((0, 10), (0, 10), x_length=10.5, y_length=4.5, at=[0, -1.3, 0], x_label="T", y_label="P",
                     x_color=cfg.TEMPERATURE, y_color=cfg.PRESSURE)
    ideal = Polygon(axes.c2p(4.5, 0), axes.c2p(10, 0), axes.c2p(10, 5.5), axes.c2p(4.5, 5.5), stroke_width=0,
                    fill_color=cfg.CYAN, fill_opacity=0.16)
    ideal_tag = VGroup(txt("ideal gas works", cfg.FONT["label"], cfg.CYAN), check_mark(0.24, cfg.CYAN)).arrange(RIGHT, buff=0.2)
    ideal_tag.move_to(axes.c2p(7.25, 2.6))
    scene.play(Create(axes), run_time=1.1)
    at_word(scene, t, 5, "works", lead=0.1)
    scene.play(FadeIn(ideal), FadeIn(ideal_tag, shift=UP * 0.1), run_time=1.0)
    at_word(scene, t, 5, "high", nth=2, lead=0.2)
    squeeze = arrow2d(axes.c2p(7.25, 5.7), axes.c2p(7.25, 8.6), cfg.SIZE, width=0.1, tip_len=0.3)
    cool = arrow2d(axes.c2p(4.2, 2.6), axes.c2p(1.6, 2.6), cfg.ATTRACT, width=0.1, tip_len=0.3)
    top = Polygon(axes.c2p(0, 7.2), axes.c2p(10, 7.2), axes.c2p(10, 10), axes.c2p(0, 10), stroke_width=0, fill_color=cfg.SIZE,
                  fill_opacity=0.14)
    side = Polygon(axes.c2p(0, 0), axes.c2p(2.2, 0), axes.c2p(2.2, 10), axes.c2p(0, 10), stroke_width=0, fill_color=cfg.ATTRACT,
                   fill_opacity=0.14)
    scene.play(FadeIn(squeeze, shift=UP * 0.2), FadeIn(cool, shift=LEFT * 0.2), FadeIn(top), FadeIn(side), run_time=1.2)
    at_word(scene, t, 5, "size", lead=0.2)
    size_tag = txt("size", cfg.FONT["section"], cfg.SIZE).move_to(axes.c2p(4.6, 8.6))
    scene.play(FadeIn(size_tag, shift=DOWN * 0.1), Indicate(chip_v.label, color=cfg.WHITE), run_time=0.9)
    at_word(scene, t, 5, "attraction", lead=0.2)
    attr_tag = txt("attraction", cfg.FONT["section"], cfg.ATTRACT).move_to(axes.c2p(2.0, 5.2))
    scene.play(FadeIn(attr_tag, shift=RIGHT * 0.1), Indicate(chip_f.label, color=cfg.WHITE), run_time=0.9)
    finish(scene, t, fill=lambda s: [Indicate(ideal_tag, color=cfg.WHITE, scale_factor=1.05)])
