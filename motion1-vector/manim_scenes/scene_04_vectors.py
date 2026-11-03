"""Scene 04 — vectors. One gold arrow stretches (magnitude) and turns
(direction); five physical vectors point five ways; the notation A-arrow and
|A| is attached to the picture; a first tip-to-tail sum (3 then 4 gives 5,
not 7) shows the addition rule; on a grid the arrow becomes A_x i + A_y j.
Then the car: 20 m/s is a speed, 20 m/s east is a velocity.
"""

from manim_scenes.common import *

BASE = np.array([-3.4, -0.9, 0])


class Scene04Vectors(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "Vectors")
    length, angle = Knob(3.6), Knob(32 * DEGREES)
    tip = lambda: BASE + length.value * np.array([np.cos(angle.value), np.sin(angle.value), 0])  # noqa: E731
    arrow = VecArrow(BASE, tip, cfg.VEC_A, width=0.14, tip_len=0.42)
    scene.add(arrow)
    scene.play(arrow.grow_in(run_time=1.4), run_time=1.4)
    mag = txt("magnitude", cfg.FONT["label"], cfg.WHITE)
    mag.add_updater(lambda m: label_at(m, arrow, side=UP, buff=0.3))
    arc = always_redraw(lambda: angle_arc(BASE, 0, np.degrees(angle.value), 1.1, cfg.MUTED, 4))
    ground = DashedLine(BASE, BASE + RIGHT * 2.0, stroke_color=cfg.MUTED, stroke_width=3)
    direction = txt("direction", cfg.FONT["label"], cfg.MUTED)
    direction.add_updater(lambda m: m.next_to(BASE + RIGHT * 1.25 + UP * 0.32 * np.sign(angle.value + 1e-9), RIGHT, buff=0.2))
    scene.play(FadeIn(mag), run_time=0.7)
    scene.play(Create(ground), Create(arc), FadeIn(direction), run_time=0.9)

    # --- 2. Length = how much; pointing = where --------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(length.to(arrow, 5.2, run_time=1.6))
    scene.play(length.to(arrow, 3.6, run_time=1.2))
    scene.play(angle.to(arrow, 70 * DEGREES, run_time=1.5))
    scene.play(angle.to(arrow, 32 * DEGREES, run_time=1.2))

    # --- 3. Five vectors of physics ------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    examples = VGroup()
    for name, color, deg in (("displacement", cfg.POSITION, 20), ("velocity", cfg.VELOCITY, 60),
                             ("acceleration", cfg.ACCEL, -90), ("force", cfg.ROSE, 160), ("momentum", cfg.PURPLE, 0)):
        label = txt(name, cfg.FONT["tiny"], color)
        d = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
        icon = VecArrow(-d * 0.42, d * 0.42, color, width=0.07, tip_len=0.2, live=False)
        examples.add(VGroup(label, icon).arrange(DOWN, buff=0.18))
    examples.arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to(UP * 2.85)
    scene.play(LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in examples], lag_ratio=0.25), run_time=2.4)

    # --- 4. Notation: A with an arrow ------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    name = eq(r"\vec{A}", cfg.FONT["hero"], cfg.VEC_A).move_to([3.8, 1.2, 0])
    scene.play(FadeOut(mag), Write(name), run_time=1.2)
    note = txt('vector notation', cfg.FONT["small"], cfg.MUTED).next_to(name, DOWN, buff=0.35)
    scene.play(FadeIn(note), run_time=0.8)

    # --- 5. Its magnitude: |A| ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    size = eq([r"|\vec{A}|", r"=\ \text{length}"], cfg.FONT["section"]).next_to(note, DOWN, buff=0.55)
    size[0].set_color(cfg.VEC_A)
    brace = always_redraw(lambda: BraceBetweenPoints(arrow.tail(), arrow.tip(), direction=np.array(
        [np.sin(angle.value), -np.cos(angle.value), 0]), color=cfg.WHITE))
    scene.play(FadeOut(note), Write(size), FadeIn(brace), run_time=1.4)

    # --- 6. Vectors combine arrow after arrow, not number plus number ---------------------------------------------------------------------
    beat(scene, t, 5)
    arrow.clear_updaters()
    for m in (direction,):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(arrow, arc, ground, direction, brace, name, size, examples)), run_time=0.8)
    o = np.array([-2.2, -2.3, 0])
    a_vec = VecArrow(o, o + RIGHT * 3.0, cfg.VEC_A, width=0.12)
    b_vec = VecArrow(o + RIGHT * 3.0, o + RIGHT * 3.0 + UP * 4.0, cfg.VEC_B, width=0.12)
    r_vec = VecArrow(o, o + RIGHT * 3.0 + UP * 4.0, cfg.RESULT, width=0.12)
    a_lab = eq("3", cfg.FONT["body"], cfg.VEC_A).next_to(a_vec, DOWN, buff=0.2)
    b_lab = eq("4", cfg.FONT["body"], cfg.VEC_B).next_to(b_vec, RIGHT, buff=0.25)
    r_lab = eq("5", cfg.FONT["body"], cfg.RESULT).move_to(o + RIGHT * 1.1 + UP * 2.4)
    scene.add(a_vec, b_vec, r_vec)
    scene.play(a_vec.grow_in(run_time=0.9), FadeIn(a_lab), run_time=0.9)
    scene.play(b_vec.grow_in(run_time=0.9), FadeIn(b_lab), run_time=0.9)
    scene.play(r_vec.grow_in(run_time=1.0), FadeIn(r_lab), run_time=1.0)
    wrong = eq(["3 + 4", "=", "7"], cfg.FONT["section"]).move_to([4.2, 1.0, 0])
    right = eq([r"3 \oplus 4", "=", "5"], cfg.FONT["section"]).move_to([4.2, -0.6, 0])
    right[2].set_color(cfg.RESULT)
    scene.play(FadeIn(wrong), run_time=0.7)
    scene.play(Create(strike(wrong)), FadeIn(right), run_time=1.0)
    rule = txt('vector addition', cfg.FONT["label"], cfg.RESULT).next_to(right, DOWN, buff=0.5)
    scene.play(FadeIn(rule), run_time=0.7)

    # --- 7. On a grid: across and up -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    clear(scene, head)
    grid = plane((-1, 7), (-1, 5), unit=0.85, at=(-5.6, -2.9, 0))
    a = vec_on(grid, (0, 0), (4, 3), cfg.VEC_A, width=0.12)
    scene.add(grid, a)
    scene.play(FadeIn(grid), run_time=0.8)
    scene.play(a.grow_in(run_time=1.2), run_time=1.2)
    across = vec_on(grid, (0, 0), (4, 0), cfg.X_COLOR, width=0.09)
    up = vec_on(grid, (4, 0), (4, 3), cfg.Y_COLOR, width=0.09)
    scene.add(across, up)
    across_lab = txt("across", cfg.FONT["small"], cfg.X_COLOR).next_to(grid.c2p(2, 0), DOWN, buff=0.25)
    up_lab = txt("up", cfg.FONT["small"], cfg.Y_COLOR).next_to(grid.c2p(4, 1.5), RIGHT, buff=0.25)
    scene.play(across.grow_in(run_time=1.0), FadeIn(across_lab), run_time=1.0)
    scene.play(up.grow_in(run_time=1.0), FadeIn(up_lab), run_time=1.0)

    # --- 8. A = Ax i + Ay j --------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    form = paint(eq([r"\vec{A}", "=", "A_x", r"\,\hat{\imath}", "+", "A_y", r"\,\hat{\jmath}"], cfg.FONT["title"]),
                 {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    form.move_to([3.6, 1.0, 0])
    scene.play(Write(form), run_time=1.6)
    scene.play(ReplacementTransform(across_lab, eq("A_x", cfg.FONT["body"], cfg.X_COLOR).move_to(across_lab)),
               ReplacementTransform(up_lab, eq("A_y", cfg.FONT["body"], cfg.Y_COLOR).move_to(up_lab)), run_time=1.0)
    two = txt('components', cfg.FONT["label"], cfg.WHITE).next_to(form, DOWN, buff=0.6)
    scene.play(FadeIn(two, shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(form[2:4], color=cfg.X_COLOR), run_time=0.9)
    scene.play(Indicate(form[5:7], color=cfg.Y_COLOR), run_time=0.9)

    # --- 9. Back to the car: 20 m/s is a speed --------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene, head)
    road_y = -0.6
    road = Line([-7.2, road_y, 0], [7.2, road_y, 0], stroke_color=cfg.GRAY, stroke_width=70, stroke_opacity=0.3)
    stripes = dashed_path([-7.0, road_y, 0], [7.0, road_y, 0], cfg.WHITE, 3, 0.5, 0.3)
    car = Car(cfg.CYAN, 1.5)
    x = Knob(-5.0)
    car.add_updater(lambda m: m.set_pose([x.value, road_y, 0], 0.0))
    gauge = Speedometer([-4.6, 2.0, 0], value=pm.CAR_SPEED, radius=1.0, unit_gap=0.5)
    speed_chip = VGroup(txt("speed", cfg.FONT["label"], cfg.CYAN), eq(r"20\ \mathrm{m/s}", cfg.FONT["section"])).arrange(DOWN, buff=0.15)
    speed_chip.move_to([-1.8, 2.1, 0])
    scene.play(FadeIn(road), FadeIn(stripes), FadeIn(car), FadeIn(gauge), run_time=0.8)
    scene.play(FadeIn(speed_chip), x.to(car, -1.0, run_time=3.0, rate_func=linear), run_time=3.0)

    # --- 10. 20 m/s east is a velocity -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    rose = compass([5.8, -2.9, 0], 0.6)
    vel = VecArrow(lambda: car.pose[0] + RIGHT * 0.9, lambda: car.pose[0] + RIGHT * 2.6, cfg.VELOCITY, width=0.12)
    vel_chip = VGroup(txt("velocity", cfg.FONT["label"], cfg.VELOCITY),
                      eq(r"20\ \mathrm{m/s,\ east}", cfg.FONT["section"])).arrange(DOWN, buff=0.15)
    vel_chip.move_to([4.1, 2.1, 0])
    scene.add(vel)
    scene.play(FadeIn(rose), vel.grow_in(run_time=0.9), FadeIn(vel_chip), run_time=0.9)
    scene.play(x.to(car, 2.2, run_time=3.0, rate_func=linear))

    # --- 11. A small difference that changes everything -------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    neq = eq(r"\neq", cfg.FONT["title"], cfg.RED).move_to((speed_chip.get_center() + vel_chip.get_center()) / 2)
    tags = VGroup(txt("scalar", cfg.FONT["small"], cfg.CYAN).next_to(speed_chip, UP, buff=0.25),
                  txt("vector", cfg.FONT["small"], cfg.VELOCITY).next_to(vel_chip, UP, buff=0.25))
    scene.play(FadeOut(head), FadeIn(neq, scale=1.3), FadeIn(tags), run_time=1.0)
    scene.play(x.to(car, 5.6, run_time=3.5, rate_func=linear))

    # --- 12. First: distance vs displacement ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    for m in (car, vel, gauge.needle):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(road, stripes, car, vel, gauge, rose, speed_chip, vel_chip, neq, tags)), run_time=0.8)
    teaser = VGroup(txt("distance", cfg.FONT["title"], cfg.CYAN), txt("vs", cfg.FONT["section"], cfg.MUTED),
                    txt("displacement", cfg.FONT["title"], cfg.POSITION)).arrange(RIGHT, buff=0.45)
    scene.play(LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in teaser], lag_ratio=0.35), run_time=1.6)
    scene.play(Indicate(teaser[2], color=cfg.POSITION, scale_factor=1.08), run_time=1.4)
    scene.wait(4.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
