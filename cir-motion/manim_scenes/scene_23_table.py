"""Scene 23 — speed, direction, or both? The brief's comparison table, one
row per beat, each with a small live icon: a straight line at constant
velocity, a straight line speeding up, uniform circular motion, and
circular motion speeding up. Columns: tangential and radial acceleration,
then what changes (nothing, speed, direction, both). One principle closes
it: a = dv/dt.
"""

from manim_scenes.common import *

ROWS_Y = (1.75, 0.65, -0.45, -1.55)
X_ICON, X_NAME, X_AT, X_AR, X_CHANGE = -6.0, -4.95, 0.95, 2.75, 5.3
LOOP = 2.4                                  # seconds per icon loop


class Scene23Table(Scene):
    def construct(self) -> None:
        play_scene(self)


def icon(kind: str, y: float, tick: Knob) -> VGroup:
    """A tiny live picture of one kind of motion, looping every LOOP seconds."""
    centre = np.array([X_ICON, y, 0])
    group = VGroup()
    if kind.startswith("line"):
        group.add(Line(centre + LEFT * 0.7, centre + RIGHT * 0.7, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6))
        accel = kind == "line speeding"

        def where():
            s = tick.value % LOOP / LOOP
            return centre + RIGHT * (-0.65 + 1.3 * (s * s if accel else s))

        def speed():
            s = tick.value % LOOP / LOOP
            return 0.25 + 0.55 * s if accel else 0.45

        dot = bead(where(), cfg.BALL, 0.08)
        dot.add_updater(lambda m: m.move_to(where()))
        group.add(VecArrow(where, lambda: where() + RIGHT * speed(), cfg.VELOCITY, width=0.05, tip_len=0.14), dot)
    else:
        ring = Circle(radius=0.45, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6).move_to(centre)
        accel = kind == "circle speeding"

        def angle():
            s = tick.value % LOOP
            return 1.6 * s + (0.9 * s * s if accel else 0.0)

        def where():
            a = angle()
            return centre + 0.45 * np.array([np.cos(a), np.sin(a), 0])

        def vel():
            s = tick.value % LOOP
            w = 1.6 + (1.8 * s if accel else 0.0)
            a = angle()
            return np.array([-np.sin(a), np.cos(a), 0]) * 0.075 * w

        dot = bead(where(), cfg.BALL, 0.08)
        dot.add_updater(lambda m: m.move_to(where()))
        group.add(ring, VecArrow(where, lambda: where() + vel(), cfg.VELOCITY, width=0.05, tip_len=0.14), dot)
    return group


def cell(latex: str, color: str, x: float, y: float) -> MathTex:
    return eq(latex, cfg.FONT["body"], color).move_to([x, y, 0])


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "23", "Speed, direction, or both?")
    tick = Knob(0.0)
    header = VGroup(txt("motion", cfg.FONT["small"], cfg.MUTED).move_to([X_NAME, 2.75, 0], aligned_edge=LEFT),
                    eq(r"a_t", cfg.FONT["body"], cfg.TANGENTIAL).move_to([X_AT, 2.75, 0]),
                    eq(r"a_r", cfg.FONT["body"], cfg.ACCEL).move_to([X_AR, 2.75, 0]))
    rule = Line([-6.9, 2.3, 0], [6.9, 2.3, 0], stroke_color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5)
    scene.play(FadeIn(header), Create(rule), run_time=0.8)
    scene.play(FadeOut(head), tick.to(header, tick.value + 1.6, run_time=1.6, rate_func=linear), run_time=1.6)

    rows = [("line steady", "straight, constant velocity", "0", "0", "nothing"),
            ("line speeding", "straight, changing speed", r"\neq 0", "0", "speed"),
            ("circle steady", "uniform circular", "0", r"\neq 0", "direction"),
            ("circle speeding", "circular, changing speed", r"\neq 0", r"\neq 0", "both")]
    changes = VGroup()
    for k, (kind, name, at, ar, change) in enumerate(rows):
        beat(scene, t, k + 1)
        y = ROWS_Y[k]
        pic = icon(kind, y, tick)
        label = txt(name, cfg.FONT["small"], cfg.WHITE).move_to([X_NAME, y, 0], aligned_edge=LEFT)
        values = VGroup(cell(at, cfg.TANGENTIAL if at != "0" else cfg.MUTED, X_AT, y),
                        cell(ar, cfg.ACCEL if ar != "0" else cfg.MUTED, X_AR, y))
        changes.add(txt(change, cfg.FONT["small"], cfg.GOLD).move_to([X_CHANGE, y, 0]))
        scene.play(FadeIn(pic), FadeIn(label, shift=RIGHT * 0.1), tick.to(header, tick.value + 1.0, run_time=1.0, rate_func=linear),
                   run_time=1.0)
        scene.play(FadeIn(values, shift=UP * 0.05), tick.to(header, tick.value + 0.8, run_time=0.8, rate_func=linear), run_time=0.8)
        hold = SCRIPT["23"][k + 2][0] - (float(scene.time) - t)      # run the icons right up to the next cue
        scene.play(tick.to(header, tick.value + hold, run_time=hold, rate_func=linear), run_time=hold)

    # --- 6. Speed, direction, or both ------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    change_head = txt("changes", cfg.FONT["small"], cfg.GOLD).move_to([X_CHANGE, 2.75, 0])
    scene.play(FadeIn(change_head), LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in changes], lag_ratio=0.25),
               tick.to(header, tick.value + 2.0, run_time=2.0, rate_func=linear), run_time=2.0)
    scene.play(tick.to(header, tick.value + 5.5, run_time=5.5, rate_func=linear), run_time=5.5)

    # --- 7. One principle: a = dv/dt -------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    principle = paint(eq([r"\vec a", "=", r"d\vec v/dt"], cfg.FONT["section"]), {0: cfg.ACCEL, 2: cfg.VELOCITY})
    principle.move_to([0, -2.6, 0])
    framed = boxed(principle, cfg.RESULT, 0.16)
    scene.play(Write(principle), tick.to(header, tick.value + 1.4, run_time=1.4, rate_func=linear), run_time=1.4)
    scene.play(FadeIn(framed[0]), tick.to(header, tick.value + 0.7, run_time=0.7, rate_func=linear), run_time=0.7)
    scene.play(tick.to(header, tick.value + 5.0, run_time=5.0, rate_func=linear), run_time=5.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["23"])
