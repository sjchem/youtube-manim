"""Scene 08 — the rules of the ideal gas. One 3D glass box of gas sits in the
middle of the frame; the six postulates of the kinetic molecular theory arrive
one per beat as numbered purple chips (purple: idealised assumptions), three
in a column on each side, and each switches on its own effect in the box.
(1) A dozen molecules multiply into a crowd, while a live trace of their
pushes on the walls (wall hits per molecule, from the model) settles from a
sputter into a steady average. (2) The fat molecules shrink to near-points:
the box is almost empty. (3) One molecule is followed in gold; with no forces
it flies dead straight between wall bounces. (4) The gas is released from one
corner and fills the turning box. (5) Wall hits flash orange while an inset
replays one elastic collision of two equal molecules (``pm.COLLISION``): their
kinetic-energy bars trade, the total bar never moves. (6) A heater warms the
gas, a thermometer climbs and the velocity arrows lengthen. Finally the six
chips feed PV = nRT, which appears in a gold box above the gas.
"""

from manim_scenes.common import *
from manim_scenes.kit_a import Bouncers, arrow2d, chip_focus, rule_chip

RULES = [
    "huge\nnumbers",
    "negligible\nvolume",
    "no forces\nbetween",
    "random\nmotion",
    "elastic\ncollisions",
    None,                     # <K> proportional to T (an equation)
]
COUNT = 140
START = 12
BIG, SMALL = 0.12, 0.042
FOLLOW = 23
CHIP_W = 4.1
COL_X = (-5.02, 5.02)
ROW_Y = (1.95, 0.5, -0.95)
SLOT = np.array([0.0, 2.3, 0.0])          # caption slot above the box


class Scene08KmtRules(Scene):
    def construct(self) -> None:
        play_scene(self)


def make_chips() -> list[VGroup]:
    chips = []
    for k, body in enumerate(RULES):
        if body is None:
            body = paint(eq([r"\langle K\rangle", r"\propto", "T"], cfg.FONT["small"]), {0: cfg.GOLD, 2: cfg.TEMPERATURE})
        c = rule_chip(k + 1, body, width=CHIP_W)
        c.move_to([COL_X[k // 3], ROW_Y[k % 3], 0])
        chips.append(c)
    return chips


def wall_trace(box: GasBox, axes: Axes, window: float = 0.5, span: float = 4.0):
    """A strip chart of the wall hits per molecule (normalised so the long-run mean sits at 1)."""
    gas, ch = box.gas, box.chamber
    samples: list[tuple[float, float]] = []

    def per_molecule_rate() -> float:
        active = gas.active
        mean_abs = np.abs(gas.u[active]).mean(axis=0) if active.any() else np.full(3, 0.46)
        return float(box.cloud.speed * box.cloud.heat * np.sum(mean_abs / ch.extent()))

    def sample() -> None:
        now = box.cloud.time
        if samples and now - samples[-1][0] < 1e-3:
            return
        n = max(box.cloud.active_count(), 1)
        value = box.cloud.hit_rate(window) / (n * per_molecule_rate())
        samples.append((now, float(np.clip(value, 0.0, 2.4))))
        while samples and samples[0][0] < now - span - 0.5:
            samples.pop(0)

    def draw() -> VMobject:
        if len(samples) < 2:
            return VMobject()
        now = samples[-1][0]
        pts = [axes.c2p(span - (now - t), v) for t, v in samples if now - t <= span]
        if len(pts) < 2:
            return VMobject()
        line = polyline(pts, cfg.PRESSURE, width=4)
        return VGroup(line.copy().set_stroke(width=11, opacity=0.15), line)

    return sample, draw


def collision_inset(at) -> SimpleNamespace:
    """Two equal molecules meet (pm.COLLISION); their kinetic-energy bars trade, the total holds."""
    at = np.asarray(at, dtype=float)
    back = panel(4.1, 2.2, cfg.MUTED, 0.86).move_to(at)
    arena = at + np.array([-0.95, -0.22, 0])
    (v1, v2), (w1, w2) = pm.COLLISION.before, pm.COLLISION.after
    n = pm.COLLISION.normal
    r = 0.15
    s = Knob(-1.0)
    reach = 0.5

    def where(k: int) -> np.ndarray:
        side = -1 if k == 0 else 1
        contact = np.array([*(side * n * r), 0.0])
        v = (v1, v2)[k] if s.value < 0 else (w1, w2)[k]
        return arena + contact + np.array([*(v * s.value * reach), 0.0])

    a = bead(where(0), cfg.GOLD, r)
    b = bead(where(1), cfg.MOLECULE, r)
    a.add_updater(lambda m: m.move_to(where(0)))
    b.add_updater(lambda m: m.move_to(where(1)))
    ke_before = 0.5 * np.array([v1 @ v1, v2 @ v2])
    ke_after = 0.5 * np.array([w1 @ w1, w2 @ w2])
    total = float(ke_before.sum())
    base_y = at[1] - 0.62
    top_h = 0.95
    xs = at[0] + np.array([0.42, 0.9, 1.45])

    def bars() -> VGroup:
        ke = ke_before if s.value < 0 else ke_after
        group = VGroup()
        for x, value, color, w in zip(xs, (*ke, total), (cfg.GOLD, cfg.MOLECULE, cfg.WHITE), (0.3, 0.3, 0.36)):
            h = max(top_h * value / total, 0.02)
            group.add(Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color,
                                fill_opacity=0.8).move_to([x, base_y + h / 2, 0]))
        return group

    shown = live(VGroup(), bars)
    floor = Line([xs[0] - 0.28, base_y, 0], [xs[2] + 0.3, base_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    names = VGroup(txt("A", cfg.FONT["tiny"], cfg.GOLD), txt("B", cfg.FONT["tiny"], cfg.MOLECULE),
                   txt("total", cfg.FONT["tiny"], cfg.WHITE))
    for name, x in zip(names, xs):
        name.next_to([x, base_y, 0], DOWN, buff=0.12)
    names[2].shift(RIGHT * 0.06)
    title = txt("kinetic energy", cfg.FONT["tiny"], cfg.MUTED).move_to([at[0], at[1] + 0.78, 0])
    tags = VGroup(txt("A", cfg.FONT["tiny"], cfg.GOLD), txt("B", cfg.FONT["tiny"], cfg.MOLECULE))
    tags[0].add_updater(lambda m: m.next_to(where(0), LEFT, buff=0.1))
    tags[1].add_updater(lambda m: m.next_to(where(1), RIGHT, buff=0.1))
    flash = Circle(radius=0.3, stroke_color=cfg.WHITE, stroke_width=5, fill_opacity=0).move_to(arena)
    group = VGroup(back, floor, shown, names, title, a, b, tags)
    return SimpleNamespace(group=group, s=s, a=a, b=b, flash=flash, arena=arena, parts=[shown, a, b, *tags])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", TITLES["08"])
    box = GasBox((0.0, -1.0, 0), count=COUNT, active=START, half_x=1.4, half_z=1.0, height=2.6, floor=-1.3,
                 heater=True, zoom=1.36, yaw=-0.5, pitch=0.3, speed=1.5, radius=BIG, trail=3.2, spark_size=1.3)
    plate, glow, coil = box.parts[-3:]
    plate.presence = 0.0
    show(scene, box.stage, 1.2)
    kmt = txt("kinetic molecular theory", cfg.FONT["section"], cfg.LIMIT).move_to([0, 3.42, 0])
    scene.play(*box.stage.turn(yaw=-0.42), run_time=2.0)
    scene.play(FadeIn(kmt, shift=DOWN * 0.15), *box.stage.turn(yaw=-0.36), run_time=1.2)
    scene.play(Circumscribe(kmt, color=cfg.LIMIT, buff=0.15), *box.stage.turn(yaw=-0.3), run_time=1.6)
    play_in(scene, t, 1, *box.stage.turn(yaw=-0.22), run_time=2.4)

    chips = make_chips()
    caption = None

    def introduce(k: int, words: str | None, color: str, extra=()) -> None:
        nonlocal caption
        new = None
        if words:
            new = txt(words, cfg.FONT["label"], color)
            fit_width(new, 5.2)
            new.move_to(SLOT)
        anims = [FadeIn(chips[k], shift=(RIGHT if k < 3 else LEFT) * 0.3), *chip_focus(chips[k], True)]
        if k:
            anims += chip_focus(chips[k - 1], False)
        if caption is not None and new is not None:
            anims.append(fade_through(caption, new))
        elif caption is not None:
            anims.append(FadeOut(caption))
        elif new is not None:
            anims.append(FadeIn(new, shift=DOWN * 0.1))
        scene.play(*anims, *extra, run_time=0.9)
        if caption is not None:
            scene.remove(caption)
        caption = new

    # --- 1. Huge numbers: properties are statistical averages ------------------------------------------------------------
    beat(scene, t, 1)
    axes = plot_axes((0, 4.0), (0, 2.4), x_length=3.3, y_length=1.45, at=[-5.15, -2.75, 0], x_label="t", y_label="P",
                     y_color=cfg.PRESSURE, label_size=cfg.FONT["small"])
    mean_line = DashedLine(axes.c2p(0, 1), axes.c2p(4.0, 1), stroke_color=cfg.MUTED, stroke_width=2.5, dash_length=0.1)
    sample, draw = wall_trace(box, axes)
    box.stage.bodies.insert(0, Ticker(sample))
    trace = live(VMobject(), draw)
    introduce(0, None, cfg.WHITE, [FadeOut(kmt), FadeIn(axes), FadeIn(mean_line)])
    scene.add(trace)
    scene.play(*box.stage.turn(yaw=-0.3), run_time=1.6)
    on = Knob(START)
    seen = {"n": START}

    def multiply() -> None:
        k = int(on.value)
        for i in range(seen["n"], k):
            box.gas.active[i] = True
            box.cloud.born[i] = box.cloud.time
        seen["n"] = max(seen["n"], k)

    box.stage.bodies.insert(0, Ticker(multiply))
    scene.play(on.to(box.stage, COUNT, run_time=3.0, rate_func=rush_into), run_time=3.0)
    avg = txt("steady average", cfg.FONT["label"], cfg.PRESSURE)
    fit_width(avg, 5.2)
    avg.move_to(SLOT)
    caption = avg
    scene.play(FadeIn(avg, shift=DOWN * 0.1), *box.stage.turn(yaw=-0.42), run_time=1.0)
    play_in(scene, t, 2, *box.stage.turn(yaw=-0.5), run_time=1.6)

    # --- 2. Negligible volume: mostly empty space ---------------------------------------------------------------------------
    beat(scene, t, 2)
    introduce(1, "mostly empty space", cfg.WHITE, [FadeOut(VGroup(axes, mean_line, trace))])
    trace.clear_updaters()
    scene.play(box.cloud.tween("radius", SMALL, run_time=3.0), box.stage.zoom_to(1.46, run_time=3.0),
               *box.stage.turn(yaw=-0.62, run_time=3.0), run_time=3.0)
    play_in(scene, t, 3, *box.stage.turn(yaw=-0.48), box.stage.zoom_to(1.36), run_time=4.6)

    # --- 3. No forces: straight lines between collisions ----------------------------------------------------------------------
    beat(scene, t, 3)
    box.cloud.follow = FOLLOW
    box.cloud.follow_alpha = 0.0
    box.cloud.history = []
    introduce(2, "straight lines", cfg.GOLD, [box.cloud.tween("follow_alpha", 1.0), box.cloud.tween("alpha", 0.3)])
    scene.play(box.cloud.tween("radius", 0.05, run_time=1.0), run_time=1.0)
    play_in(scene, t, 4, *box.stage.turn(yaw=-0.3), run_time=6.8)

    # --- 4. Random motion: a gas fills its container ---------------------------------------------------------------------------
    beat(scene, t, 4)
    introduce(3, "fills the container", cfg.MOLECULE, [box.cloud.tween("follow_alpha", 0.0), box.cloud.tween("alpha", 0.0)])
    box.cloud.follow = None
    rng = np.random.default_rng(cfg.SEED + 81)
    act = np.nonzero(box.gas.active)[0]
    box.gas.phase[act] = np.column_stack([rng.uniform(0.0, 0.2, len(act)), rng.uniform(0.82, 1.0, len(act)),
                                          rng.uniform(0.82, 1.0, len(act))])
    box.cloud.born[act] = box.cloud.time
    box.cloud.alpha = 1.0
    scene.play(*box.stage.turn(yaw=0.35, run_time=5.6, rate_func=smooth), run_time=5.6)
    play_in(scene, t, 5, *box.stage.turn(yaw=0.42), run_time=0.6)

    # --- 5. Elastic collisions: energy passes, the total is conserved --------------------------------------------------------
    beat(scene, t, 5)
    inset = collision_inset([5.02, -2.72, 0])
    introduce(4, "total KE conserved", cfg.WHITE, [box.cloud.tween("spark", 1.6), FadeIn(inset.group)])
    for _ in range(2):
        scene.play(inset.s.to(inset.a, 0.0, run_time=1.4, rate_func=linear), *box.stage.turn(yaw=0.3, run_time=1.4),
                   run_time=1.4)
        flash = inset.flash.copy()
        scene.play(inset.s.to(inset.a, 1.0, run_time=1.5, rate_func=linear), FadeOut(flash, scale=2.0, run_time=0.6),
                   *box.stage.turn(yaw=0.18, run_time=1.5), run_time=1.5)
        scene.remove(flash)
        if _ == 0:
            scene.play(inset.s.to(inset.a, -1.0, run_time=0.01), run_time=0.2)
            scene.play(*box.stage.turn(yaw=0.1), run_time=0.9)
    play_in(scene, t, 6, *box.stage.turn(yaw=0.0), run_time=1.6)

    # --- 6. <K> depends only on T: heat it ------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    for m in inset.parts:
        m.clear_updaters()
    therm = Thermo(box.kelvin, [5.0, -2.55, 0], low=200, high=700, height=1.45)
    therm.remove(therm.readout, therm.unit)
    therm.shift(UP * (-1.85 - therm.get_top()[1]))
    arrows = []
    for i in (5, 40, 77):
        arrow = Vector(lambda i=i: box.cloud.position(i), lambda i=i: box.cloud.position(i) + box.cloud.velocity(i) * 0.42,
                       cfg.VELOCITY, width=0.05, tip=0.17)
        arrow.presence = 0.0
        arrows.append(arrow)
    box.stage.add_overlay(*arrows)
    introduce(5, "hotter → faster", cfg.TEMPERATURE,
              [FadeOut(inset.group), box.cloud.tween("spark", 1.0), box.stage.fade(plate, 1.0),
               *[box.stage.fade(a, 1.0) for a in arrows]])
    scene.play(FadeIn(therm, shift=UP * 0.2), *box.heater_on(1.0), run_time=0.8)
    scene.play(box.heat_to(620, run_time=4.0), box.cloud.tween("warmth", 0.5, run_time=4.0),
               *box.stage.turn(yaw=-0.2, run_time=4.0), run_time=4.0)
    play_in(scene, t, 7, *box.stage.turn(yaw=-0.28), run_time=1.0)

    # --- 7. Together: PV = nRT -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    law = paint(eq(["P", "V", "=", "n", "R", "T"], 62), {0: cfg.PRESSURE, 1: cfg.VOLUME, 3: cfg.AMOUNT, 5: cfg.TEMPERATURE})
    law.move_to(SLOT + UP * 0.05)
    framed = boxed(law, cfg.GOLD, buff=0.24)
    feeds = VGroup()
    for k, c in enumerate(chips):
        side = RIGHT if k < 3 else LEFT
        start_pt = c.pill.get_edge_center(side)
        end_pt = framed.frame.get_edge_center(-side) + DOWN * (0.18 * (1 - k % 3))
        feeds.add(Line(start_pt, end_pt, stroke_color=cfg.GOLD, stroke_width=3, stroke_opacity=0.7))
    scene.play(FadeOut(caption), *[a for c in chips for a in chip_focus(c, True)], *[box.stage.fade(a, 0.0) for a in arrows],
               run_time=0.8)
    scene.remove(caption)
    scene.play(LaggedStart(*[Create(f) for f in feeds], lag_ratio=0.12), run_time=1.4)
    scene.play(Write(law), Create(framed.frame), FadeOut(feeds), run_time=1.6)
    scene.play(box.heat_to(pm.ROOM_T, run_time=2.4), box.cloud.tween("warmth", 0.0, run_time=2.4), *box.heater_on(0.0, run_time=2.4),
               *[a for c in chips for a in chip_focus(c, False)], run_time=2.4)
    finish(scene, t, box.stage)
