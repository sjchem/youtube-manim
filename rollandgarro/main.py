from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from manim import *

try:
    from manim_physics import *  # noqa: F401,F403
except Exception:
    # The project does not require manim-physics at runtime. It is listed as
    # optional because these scenes are more stable as deterministic 2D Manim.
    pass


config.background_color = "#070A12"
config.frame_width = 16
config.frame_height = 9


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BACKGROUND = "#070A12"
DEEP_NAVY = "#0B1020"
OFF_WHITE = "#F3EFE2"
GOLD = "#F5C542"
CLAY = "#B84A2A"
CLAY_DARK = "#73321F"
CLAY_LIGHT = "#E06B3E"
CLAY_OPENING = "#D75A32"
HARD_COURT = "#277A83"
HARD_COURT_DARK = "#155056"
GRASS = "#2C6B3F"
BALL = "#D8FF39"
BALL_DARK = "#8EB321"
GRAVITY_COLOR = WHITE
DRAG_COLOR = "#FF4C4C"
MAGNUS_COLOR = "#40DFFF"
FRICTION_COLOR = "#FF9B25"
VELOCITY_COLOR = "#FFE45C"
SPIN_COLOR = "#C891FF"

G = 9.81
RHO_AIR = 1.225
BALL_RADIUS_M = 0.0335
BALL_MASS_KG = 0.057
CD = 0.55
MAGNUS_K = 1.15e-4
CLAY_FRICTION = 0.78
HARD_FRICTION = 0.55
E_CLAY = 0.76
E_HARD = 0.82


@dataclass(frozen=True)
class SurfaceModel:
    name: str
    color: str
    alpha: float
    beta: float
    gamma: float
    e: float
    friction: float
    dust: int


SURFACES = {
    "hard": SurfaceModel("Hard court", HARD_COURT, 0.82, 0.72, 0.05, E_HARD, HARD_FRICTION, 8),
    "clay": SurfaceModel("Red clay", CLAY, 0.58, 0.58, 0.14, E_CLAY, CLAY_FRICTION, 40),
    "grass": SurfaceModel("Grass", GRASS, 0.88, 0.66, 0.03, 0.72, 0.42, 5),
}


# ---------------------------------------------------------------------------
# Physics models
# ---------------------------------------------------------------------------


def drag_force(v: np.ndarray, cd: float = CD) -> np.ndarray:
    """Quadratic drag: always points opposite velocity."""
    v = np.array(v, dtype=float)
    speed = np.linalg.norm(v)
    area = math.pi * BALL_RADIUS_M**2
    return -0.5 * RHO_AIR * cd * area * speed * v


def magnus_force(v: np.ndarray, omega: np.ndarray, k: float = MAGNUS_K) -> np.ndarray:
    """Simplified Magnus lift. In this 2D visual, omega is a 3D spin vector."""
    v3 = np.array([v[0], v[1], 0.0], dtype=float)
    omega3 = np.array(omega, dtype=float)
    return k * np.cross(omega3, v3)[:2]


def simple_projectile_path(v0=(27.0, 8.0), y0=1.0, duration=1.15, dt=0.02) -> np.ndarray:
    pts = []
    x, y = 0.0, y0
    vx, vy = v0
    for _ in np.arange(0, duration, dt):
        pts.append([x, y])
        vy -= G * dt
        x += vx * dt
        y = max(0.0, y + vy * dt)
    return np.array(pts)


def spin_projectile_path(
    v0=(27.0, 8.0),
    omega_z=-160.0,
    y0=1.0,
    duration=1.15,
    dt=0.02,
    drag_scale=1.0,
    magnus_scale=1.0,
) -> np.ndarray:
    """Integrate a plausible ball path with drag and Magnus force."""
    position = np.array([0.0, y0], dtype=float)
    velocity = np.array(v0, dtype=float)
    points = []
    for _ in np.arange(0, duration, dt):
        points.append(position.copy())
        fg = np.array([0.0, -BALL_MASS_KG * G])
        fd = drag_scale * drag_force(velocity)
        fm = magnus_scale * magnus_force(velocity, np.array([0.0, 0.0, omega_z]))
        acceleration = (fg + fd + fm) / BALL_MASS_KG
        velocity += acceleration * dt
        position += velocity * dt
        if position[1] < 0:
            position[1] = 0
            break
    return np.array(points)


def bounce_model(v_in: np.ndarray, omega_in: float, surface_type: str = "clay") -> tuple[np.ndarray, float]:
    """Visual bounce model separating normal restitution and tangential grip."""
    surface = SURFACES[surface_type]
    vx, vy = float(v_in[0]), float(v_in[1])
    v_after = np.array([surface.alpha * vx, -surface.e * vy])
    omega_after = surface.beta * omega_in + surface.gamma * vx
    return v_after, omega_after


def friction_impulse_visual_model(surface_type: str) -> float:
    return SURFACES[surface_type].friction


def speed_loss_comparison(vx=24.0) -> dict[str, float]:
    return {
        "hard": vx * SURFACES["hard"].alpha,
        "clay": vx * SURFACES["clay"].alpha,
        "grass": vx * SURFACES["grass"].alpha,
    }


def trajectory_with_spin(
    omega_z: float,
    origin=LEFT * 6 + DOWN * 2.5,
    x_scale=0.20,
    y_scale=0.55,
    v0=(28.0, 8.0),
    duration=1.2,
) -> list[np.ndarray]:
    pts = spin_projectile_path(v0=v0, omega_z=omega_z, duration=duration)
    return [origin + RIGHT * (p[0] * x_scale) + UP * (p[1] * y_scale) for p in pts]


# ---------------------------------------------------------------------------
# Visual helpers
# ---------------------------------------------------------------------------


def create_tennis_ball(radius=0.22, label=False) -> VGroup:
    core = Circle(radius=radius, color=BALL_DARK, fill_color=BALL, fill_opacity=1, stroke_width=2)
    glow = Circle(radius=radius * 1.08, color=BALL, fill_opacity=0.14, stroke_opacity=0)
    seam1 = Arc(radius=radius * 0.72, start_angle=-1.2, angle=2.4, color=OFF_WHITE, stroke_width=3)
    seam1.shift(LEFT * radius * 0.24)
    seam2 = Arc(radius=radius * 0.72, start_angle=PI - 1.2, angle=2.4, color=OFF_WHITE, stroke_width=3)
    seam2.shift(RIGHT * radius * 0.24)
    ball = VGroup(glow, core, seam1, seam2)
    if label:
        ball.add(Text("spin", font_size=18, color=OFF_WHITE).next_to(core, DOWN, buff=0.08))
    return ball


def create_court_surface(
    width=7.0,
    height=1.8,
    surface_type="clay",
    label=True,
    texture=True,
) -> VGroup:
    surface = SURFACES[surface_type]
    rect = Rectangle(width=width, height=height, fill_color=surface.color, fill_opacity=1, stroke_width=0)
    top_line = Line(rect.get_left() + UP * height / 2, rect.get_right() + UP * height / 2, color=OFF_WHITE, stroke_width=3)
    group = VGroup(rect, top_line)
    if texture:
        rng = random.Random(22 if surface_type == "clay" else 9)
        dots = VGroup()
        for _ in range(75 if surface_type == "clay" else 36):
            x = rng.uniform(-width / 2 + 0.1, width / 2 - 0.1)
            y = rng.uniform(-height / 2 + 0.08, height / 2 - 0.08)
            color = CLAY_LIGHT if surface_type == "clay" else "#3AA0A8"
            dots.add(Dot([x, y, 0], radius=rng.uniform(0.006, 0.017), color=color, fill_opacity=rng.uniform(0.25, 0.65)))
        group.add(dots)
    if label:
        group.add(Text(surface.name.upper(), font_size=28, color=OFF_WHITE, weight=BOLD).move_to(rect.get_center()))
    return group


def create_force_arrow(start, vector, color, label, scale=1.0) -> VGroup:
    arr = Arrow(start, start + np.array(vector) * scale, buff=0, color=color, stroke_width=6, max_tip_length_to_length_ratio=0.22)
    text = Text(label, font_size=24, color=color, weight=BOLD).next_to(arr.get_end(), UP, buff=0.08)
    return VGroup(arr, text)


def create_velocity_vector(start, vector, label="v") -> VGroup:
    return create_force_arrow(start, vector, VELOCITY_COLOR, label, scale=1.0)


def create_spin_indicator(radius=0.42, direction="topspin", color=SPIN_COLOR) -> VGroup:
    angle = -1.35 * TAU if direction == "topspin" else 1.35 * TAU
    arc = Arc(radius=radius, start_angle=0.25 * PI, angle=angle, color=color, stroke_width=5)
    tip = Triangle(color=color, fill_opacity=1).scale(0.08)
    tip.move_to(arc.point_from_proportion(1.0))
    tip.rotate(-PI / 3 if direction == "topspin" else PI / 3)
    return VGroup(arc, tip)


def create_dust_particles(center, count=34, radius=0.75, color=CLAY_LIGHT, seed=4) -> VGroup:
    rng = random.Random(seed)
    particles = VGroup()
    for _ in range(count):
        angle = rng.uniform(0.05 * PI, 0.95 * PI)
        dist = rng.uniform(radius * 0.25, radius)
        p = Dot(center, radius=rng.uniform(0.012, 0.032), color=color, fill_opacity=rng.uniform(0.55, 0.95))
        p.target = p.copy().shift(np.array([math.cos(angle), math.sin(angle), 0]) * dist)
        particles.add(p)
    return particles


def create_equation_box(lines: Iterable[str], title: str | None = None, width=6.0) -> VGroup:
    texts = VGroup(*[Text(line, font_size=28, color=OFF_WHITE) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    if title:
        heading = Text(title, font_size=24, color=GOLD, weight=BOLD)
        texts = VGroup(heading, texts).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    box = RoundedRectangle(corner_radius=0.08, width=width, height=texts.height + 0.6, color=OFF_WHITE, stroke_opacity=0.35, fill_color=DEEP_NAVY, fill_opacity=0.78)
    texts.move_to(box.get_center())
    return VGroup(box, texts)


def create_title_card(title: str, subtitle: str | None = None) -> VGroup:
    main = Text(title, font_size=52, color=OFF_WHITE, weight=BOLD)
    if subtitle:
        sub = Text(subtitle, font_size=25, color=GOLD)
        return VGroup(main, sub).arrange(DOWN, buff=0.25)
    return VGroup(main)


def create_split_screen(left_label="HARD COURT", right_label="RED CLAY") -> VGroup:
    left = create_court_surface(width=7.7, height=5.6, surface_type="hard", label=False).shift(LEFT * 4)
    right = create_court_surface(width=7.7, height=5.6, surface_type="clay", label=False).shift(RIGHT * 4)
    right[0].set_fill(CLAY_OPENING, opacity=1)
    divider = Line(UP * 4.5, DOWN * 4.5, color=OFF_WHITE, stroke_opacity=0.35)
    labels = VGroup(
        Text(left_label, font_size=32, color=OFF_WHITE, weight=BOLD).to_edge(UP).shift(LEFT * 4),
        Text(right_label, font_size=32, color=OFF_WHITE, weight=BOLD).to_edge(UP).shift(RIGHT * 4),
    )
    return VGroup(left, right, divider, labels)


def path_mobject(points, color=BALL, stroke_width=5) -> VMobject:
    path = VMobject(color=color, stroke_width=stroke_width)
    path.set_points_smoothly(points)
    return path


class RedClayScene(Scene):
    """Shared background and title utilities."""

    def add_cinematic_background(self):
        bg = Rectangle(width=16.4, height=9.4, fill_color=BACKGROUND, fill_opacity=1, stroke_width=0)
        glow = Circle(radius=5.2, color=CLAY, fill_opacity=0.06, stroke_opacity=0).shift(DOWN * 2 + RIGHT * 3)
        self.add(bg, glow)

    def chapter_title(self, title: str, subtitle: str | None = None):
        card = create_title_card(title, subtitle)
        self.play(FadeIn(card, shift=UP * 0.25), run_time=1.1)
        self.wait(0.9)
        self.play(FadeOut(card, shift=UP * 0.25), run_time=0.8)

    def pad_scene_to(self, start_time: float, target_duration: float):
        """Hold the completed visual long enough for narration pacing."""
        remaining = target_duration - (self.time - start_time)
        if remaining > 0:
            self.wait(remaining)


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------


class OpeningHookScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        question = Text("Same shot. Same speed. Same spin.", font_size=44, color=OFF_WHITE, weight=BOLD)
        self.play(FadeIn(question), run_time=0.8)
        self.wait(0.45)
        self.play(question.animate.to_edge(UP), run_time=0.7)

        split = create_split_screen()
        split.shift(DOWN * 0.15)
        self.play(FadeIn(split), run_time=0.9)

        hard_ball = create_tennis_ball(0.18).move_to(LEFT * 6.7 + DOWN * 1.0)
        clay_ball = create_tennis_ball(0.18).move_to(RIGHT * 1.3 + DOWN * 1.0)
        hard_path = path_mobject([
            LEFT * 6.7 + DOWN * 1.0,
            LEFT * 5.2 + DOWN * 0.1,
            LEFT * 3.7 + DOWN * 1.15,
            LEFT * 2.2 + DOWN * 0.75,
            LEFT * 0.8 + DOWN * 0.45,
        ], color=VELOCITY_COLOR)
        clay_path = path_mobject([
            RIGHT * 1.3 + DOWN * 1.0,
            RIGHT * 2.7 + DOWN * 0.1,
            RIGHT * 4.0 + DOWN * 1.15,
            RIGHT * 4.9 + UP * 0.55,
            RIGHT * 5.7 + UP * 1.45,
        ], color=BALL)
        self.play(Create(hard_path), MoveAlongPath(hard_ball, hard_path), Rotate(hard_ball, -TAU * 1.6), run_time=1.8)
        self.play(Create(clay_path), MoveAlongPath(clay_ball, clay_path), Rotate(clay_ball, -TAU * 2.4), run_time=1.8)

        impact = RIGHT * 4.0 + DOWN * 1.15
        dust = create_dust_particles(impact, count=48, radius=1.2, seed=10)
        self.play(LaggedStart(*[MoveToTarget(p) for p in dust], lag_ratio=0.02), FadeIn(dust), run_time=0.8)

        title = create_title_card("The Hidden Science", "of Red Clay Tennis").move_to(ORIGIN)
        plate = Rectangle(width=16, height=9, fill_color=BACKGROUND, fill_opacity=0.72, stroke_width=0)
        self.play(FadeIn(plate), FadeIn(title, scale=1.05), run_time=0.8)
        self.wait(0.6)


class AirForcesScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        self.chapter_title("Journey One", "the ball moves through air")

        ball = create_tennis_ball(0.34).move_to(LEFT * 1.2)
        spin = create_spin_indicator(0.66).move_to(ball)
        river = VGroup()
        for y in np.linspace(-2.5, 2.5, 8):
            line = DashedLine(LEFT * 7 + UP * y, RIGHT * 7 + UP * (y + 0.25 * math.sin(y)), color="#2E5D80", stroke_opacity=0.45)
            river.add(line)
        self.play(LaggedStart(*[Create(line) for line in river], lag_ratio=0.05), FadeIn(ball), run_time=1.0)
        self.play(Create(spin), Rotate(ball, -TAU * 1.2), run_time=1.0)

        center = ball.get_center()
        arrows = VGroup(
            create_force_arrow(center, DOWN * 1.35, GRAVITY_COLOR, "gravity"),
            create_force_arrow(center, LEFT * 1.45, DRAG_COLOR, "drag"),
            create_force_arrow(center, DOWN * 0.9 + RIGHT * 0.45, MAGNUS_COLOR, "Magnus"),
            create_velocity_vector(center, RIGHT * 1.55 + UP * 0.4, "velocity"),
        )
        self.play(LaggedStart(*[GrowArrow(a[0]) for a in arrows], lag_ratio=0.16), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(a[1]) for a in arrows], lag_ratio=0.12), run_time=0.6)

        note = Text("Spin turns the air into a steering force.", font_size=34, color=GOLD).to_edge(DOWN)
        self.play(Write(note), run_time=0.8)
        self.wait(0.8)


class SpinTrajectoryScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        title = Text("Topspin dips. Backspin floats.", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.7)

        base = Line(LEFT * 6.7 + DOWN * 2.55, RIGHT * 6.7 + DOWN * 2.55, color=OFF_WHITE, stroke_opacity=0.35)
        net = VGroup(
            Line(DOWN * 2.55, DOWN * 1.15, color=OFF_WHITE, stroke_width=4),
            DashedLine(DOWN * 2.50, DOWN * 1.20, color=OFF_WHITE, dash_length=0.12),
        )
        self.play(Create(base), Create(net), run_time=0.7)

        topspin_pts = trajectory_with_spin(omega_z=-230, v0=(29, 9), duration=1.25)
        flat_pts = trajectory_with_spin(omega_z=0, v0=(29, 9), duration=1.25)
        slice_pts = trajectory_with_spin(omega_z=150, v0=(29, 9), duration=1.25)
        top_path = path_mobject(topspin_pts, color=BALL, stroke_width=6)
        flat_path = path_mobject(flat_pts, color=OFF_WHITE, stroke_width=3).set_opacity(0.55)
        slice_path = path_mobject(slice_pts, color=MAGNUS_COLOR, stroke_width=5)

        top_label = Text("topspin", font_size=26, color=BALL).next_to(top_path, DOWN, buff=0.15)
        slice_label = Text("backspin / slice", font_size=26, color=MAGNUS_COLOR).next_to(slice_path, UP, buff=0.15)
        flat_label = Text("same launch speed", font_size=24, color=OFF_WHITE).move_to(RIGHT * 2 + DOWN * 0.3)
        ball = create_tennis_ball(0.18).move_to(topspin_pts[0])

        self.play(Create(flat_path), FadeIn(flat_label), run_time=0.8)
        self.play(Create(slice_path), FadeIn(slice_label), run_time=1.1)
        self.play(Create(top_path), MoveAlongPath(ball, top_path), Rotate(ball, -TAU * 2.2), FadeIn(top_label), run_time=1.5)

        insight = Text("The shot is already changing before it touches the court.", font_size=31, color=GOLD).to_edge(DOWN)
        self.play(FadeIn(insight, shift=UP * 0.2), run_time=0.7)
        self.wait(0.7)


class EquationBuildScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        title = Text("A visual model of flight", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.6)

        ball = create_tennis_ball(0.26).move_to(LEFT * 4.7 + UP * 0.4)
        equation = create_equation_box(
            [
                "m dv/dt = F_g + F_d + F_M",
                "F_g = m g",
                "F_d = -1/2 rho C_d A |v| v",
                "F_M ~= S (omega x v)",
            ],
            title="Flight forces",
            width=7.1,
        ).move_to(RIGHT * 2.4 + UP * 0.5)
        self.play(FadeIn(ball), FadeIn(equation), run_time=0.9)

        arrows = VGroup(
            create_force_arrow(ball.get_center(), DOWN * 1.0, GRAVITY_COLOR, "F_g"),
            create_force_arrow(ball.get_center(), LEFT * 1.0, DRAG_COLOR, "F_d"),
            create_force_arrow(ball.get_center(), DOWN * 0.75 + RIGHT * 0.35, MAGNUS_COLOR, "F_M"),
        )
        self.play(LaggedStart(*[GrowArrow(a[0]) for a in arrows], lag_ratio=0.2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(a[1]) for a in arrows], lag_ratio=0.15), run_time=0.5)

        terms = VGroup(
            Text("mass resists change", font_size=24, color=OFF_WHITE),
            Text("drag steals speed", font_size=24, color=DRAG_COLOR),
            Text("spin bends the path", font_size=24, color=MAGNUS_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(DOWN).shift(LEFT * 0.5)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in terms], lag_ratio=0.2), run_time=1.0)

        curve = path_mobject(trajectory_with_spin(-210, origin=LEFT * 6.2 + DOWN * 2.2, x_scale=0.19, y_scale=0.42), color=BALL)
        self.play(Create(curve), run_time=1.1)
        self.wait(0.7)


class BouncePhysicsScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        title = Text("Journey Two: the collision", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.6)

        hard = create_court_surface(width=6.7, height=1.4, surface_type="hard", label=False).shift(LEFT * 4 + DOWN * 2.7)
        clay = create_court_surface(width=6.7, height=1.4, surface_type="clay", label=False).shift(RIGHT * 4 + DOWN * 2.7)
        labels = VGroup(
            Text("Hard court: skids forward", font_size=25, color=OFF_WHITE).next_to(hard, UP, buff=0.2),
            Text("Clay: grips, slows, kicks", font_size=25, color=GOLD).next_to(clay, UP, buff=0.2),
        )
        self.play(FadeIn(hard), FadeIn(clay), FadeIn(labels), run_time=0.8)

        incoming_left = path_mobject([LEFT * 6.6 + UP * 2.0, LEFT * 5.4 + UP * 0.5, LEFT * 4.4 + DOWN * 2.0], VELOCITY_COLOR)
        outgoing_left = path_mobject([LEFT * 4.4 + DOWN * 2.0, LEFT * 3.0 + DOWN * 1.35, LEFT * 1.3 + DOWN * 1.15], HARD_COURT)
        incoming_right = path_mobject([RIGHT * 1.4 + UP * 2.0, RIGHT * 2.6 + UP * 0.5, RIGHT * 3.6 + DOWN * 2.0], VELOCITY_COLOR)
        outgoing_right = path_mobject([RIGHT * 3.6 + DOWN * 2.0, RIGHT * 4.4 + DOWN * 0.6, RIGHT * 5.2 + UP * 0.75], BALL)
        self.play(Create(incoming_left), Create(incoming_right), run_time=0.9)

        dust = create_dust_particles(RIGHT * 3.6 + DOWN * 2.0, count=48, radius=1.1, seed=18)
        self.play(Create(outgoing_left), Create(outgoing_right), FadeIn(dust), LaggedStart(*[MoveToTarget(p) for p in dust], lag_ratio=0.015), run_time=1.2)

        eq = create_equation_box(
            [
                "e = v_after_normal / v_before_normal",
                "v_x_after = alpha v_x_before",
                "omega_after = beta omega + gamma v_x",
            ],
            title="Bounce model",
            width=6.5,
        ).to_edge(LEFT).shift(UP * 0.3)
        self.play(FadeIn(eq, shift=RIGHT * 0.2), run_time=0.8)

        friction = create_force_arrow(RIGHT * 3.6 + DOWN * 1.9, LEFT * 1.1, FRICTION_COLOR, "friction impulse")
        self.play(GrowArrow(friction[0]), FadeIn(friction[1]), run_time=0.8)
        self.wait(0.7)


class ClayFrictionScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        title = Text("Why topspin becomes heavier on clay", font_size=40, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.6)

        surface = create_court_surface(width=13.5, height=1.25, surface_type="clay", label=False).to_edge(DOWN, buff=0.7)
        ball = create_tennis_ball(0.26).move_to(LEFT * 5.4 + UP * 1.6)
        spin = create_spin_indicator(0.55, "topspin").move_to(ball)
        path_in = path_mobject([LEFT * 5.4 + UP * 1.6, LEFT * 3.8 + DOWN * 0.3, LEFT * 2.5 + DOWN * 2.25], VELOCITY_COLOR)
        path_out = path_mobject([LEFT * 2.5 + DOWN * 2.25, LEFT * 1.5 + DOWN * 0.2, LEFT * 0.5 + UP * 1.8], BALL)
        self.play(FadeIn(surface), FadeIn(ball), Create(spin), run_time=0.8)
        self.play(Create(path_in), MoveAlongPath(ball, path_in), Rotate(ball, -TAU * 1.8), run_time=1.1)

        contact = LEFT * 2.5 + DOWN * 2.25
        dust = create_dust_particles(contact, count=56, radius=1.3, seed=28)
        arrows = VGroup(
            create_force_arrow(contact + UP * 0.25, LEFT * 0.95, FRICTION_COLOR, "grip"),
            create_force_arrow(contact + UP * 0.15, UP * 1.1, MAGNUS_COLOR, "kick"),
        )
        self.play(FadeIn(dust), LaggedStart(*[MoveToTarget(p) for p in dust], lag_ratio=0.012), run_time=0.65)
        self.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]), GrowArrow(arrows[1][0]), FadeIn(arrows[1][1]), run_time=0.7)
        self.play(Create(path_out), MoveAlongPath(ball, path_out), Rotate(ball, -TAU * 2.3), run_time=1.2)

        shoulder = DashedLine(RIGHT * 0.4 + UP * 0.95, RIGHT * 6.2 + UP * 0.95, color=GOLD, stroke_opacity=0.8)
        note = Text("shoulder-height contact", font_size=25, color=GOLD).next_to(shoulder, UP, buff=0.1)
        player = VGroup(Line(RIGHT * 5.6 + DOWN * 2.25, RIGHT * 5.6 + UP * 0.55, color=OFF_WHITE), Circle(radius=0.18, color=OFF_WHITE).move_to(RIGHT * 5.6 + UP * 0.8))
        self.play(Create(player), Create(shoulder), FadeIn(note), run_time=0.9)
        self.wait(0.7)


class RallyGeometryScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        title = Text("On clay, time becomes tactics", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.6)

        court = Rectangle(width=10, height=5.2, color=OFF_WHITE, stroke_width=3, fill_color=CLAY_DARK, fill_opacity=0.75)
        center = Line(UP * 2.6, DOWN * 2.6, color=OFF_WHITE, stroke_width=2)
        service1 = Line(LEFT * 5 + UP * 1.15, RIGHT * 5 + UP * 1.15, color=OFF_WHITE, stroke_width=2)
        service2 = Line(LEFT * 5 + DOWN * 1.15, RIGHT * 5 + DOWN * 1.15, color=OFF_WHITE, stroke_width=2)
        net = Line(LEFT * 5, RIGHT * 5, color=OFF_WHITE, stroke_width=4)
        geometry = VGroup(court, center, service1, service2, net).shift(DOWN * 0.1)
        self.play(Create(geometry), run_time=1.0)

        p1 = Dot(LEFT * 3.6 + DOWN * 2.0, radius=0.13, color=BALL)
        p2 = Dot(RIGHT * 3.6 + UP * 1.8, radius=0.13, color=MAGNUS_COLOR)
        slide = Line(RIGHT * 4.5 + UP * 1.8, RIGHT * 3.6 + UP * 1.8, color=FRICTION_COLOR, stroke_width=7)
        self.play(FadeIn(p1), FadeIn(p2), Create(slide), run_time=0.7)

        rally_paths = VGroup(
            CurvedArrow(LEFT * 3.6 + DOWN * 2.0, RIGHT * 3.5 + UP * 2.1, angle=-TAU / 5, color=BALL),
            CurvedArrow(RIGHT * 3.5 + UP * 2.1, LEFT * 4.1 + UP * 1.8, angle=-TAU / 5, color=MAGNUS_COLOR),
            CurvedArrow(LEFT * 4.1 + UP * 1.8, RIGHT * 2.7 + DOWN * 2.1, angle=TAU / 6, color=BALL),
            CurvedArrow(RIGHT * 2.7 + DOWN * 2.1, LEFT * 0.7 + DOWN * 0.35, angle=TAU / 7, color=GOLD),
        )
        labels = VGroup(
            Text("heavy topspin", font_size=23, color=BALL).move_to(LEFT * 1.4 + UP * 2.75),
            Text("wide angle", font_size=23, color=MAGNUS_COLOR).move_to(LEFT * 3.7 + UP * 2.25),
            Text("drop shot", font_size=23, color=GOLD).move_to(RIGHT * 1.6 + DOWN * 0.65),
        )
        self.play(LaggedStart(*[Create(a) for a in rally_paths], lag_ratio=0.35), run_time=2.0)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.16), run_time=0.8)

        clock = Text("+ time", font_size=34, color=GOLD, weight=BOLD).to_edge(RIGHT).shift(UP * 2.4)
        endurance = Text("+ endurance", font_size=34, color=OFF_WHITE, weight=BOLD).next_to(clock, DOWN, aligned_edge=LEFT, buff=0.25)
        patience = Text("+ patience", font_size=34, color=OFF_WHITE, weight=BOLD).next_to(endurance, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(clock), FadeIn(endurance), FadeIn(patience), run_time=0.9)
        self.wait(0.7)


class LivingClayCourtScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        title = Text("The court is a living variable", font_size=42, color=OFF_WHITE, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title), run_time=0.6)

        panels = VGroup()
        for name, color, x in [
            ("wet / compact", "#8F3926", -4.6),
            ("ideal / grippy", CLAY, 0.0),
            ("dry / loose", "#D66A37", 4.6),
        ]:
            panel = RoundedRectangle(corner_radius=0.08, width=4.0, height=4.6, fill_color=color, fill_opacity=0.95, stroke_color=OFF_WHITE, stroke_opacity=0.25)
            label = Text(name, font_size=27, color=OFF_WHITE, weight=BOLD).next_to(panel, UP, buff=0.22)
            rng = random.Random(int((x + 6) * 100))
            specks = VGroup(*[
                Dot(panel.get_center() + RIGHT * rng.uniform(-1.75, 1.75) + UP * rng.uniform(-1.9, 1.9), radius=rng.uniform(0.006, 0.022), color=CLAY_LIGHT, fill_opacity=rng.uniform(0.25, 0.8))
                for _ in range(70)
            ])
            panels.add(VGroup(panel, label, specks).shift(RIGHT * x + DOWN * 0.25))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in panels], lag_ratio=0.15), run_time=1.1)

        notes = VGroup(
            Text("moisture changes density", font_size=25, color=GOLD),
            Text("rolling changes smoothness", font_size=25, color=OFF_WHITE),
            Text("wear creates loose particles", font_size=25, color=CLAY_LIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in notes], lag_ratio=0.18), run_time=1.0)

        mini_ball = create_tennis_ball(0.14).move_to(panels[0][0].get_center() + UP * 1.4)
        paths = [
            path_mobject([panels[i][0].get_center() + UP * 1.4, panels[i][0].get_center() + DOWN * 1.2], color=VELOCITY_COLOR, stroke_width=4)
            for i in range(3)
        ]
        self.play(FadeIn(mini_ball), run_time=0.3)
        for path in paths:
            ball_copy = mini_ball.copy().move_to(path.get_start())
            self.add(ball_copy)
            self.play(Create(path), MoveAlongPath(ball_copy, path), run_time=0.55)
            self.remove(ball_copy)
        self.wait(0.7)


class FinalSummaryScene(RedClayScene):
    def construct(self):
        self.add_cinematic_background()
        words = VGroup(
            Text("AIR", font_size=54, color=MAGNUS_COLOR, weight=BOLD),
            Text("SPIN", font_size=54, color=SPIN_COLOR, weight=BOLD),
            Text("FRICTION", font_size=54, color=FRICTION_COLOR, weight=BOLD),
            Text("CLAY", font_size=54, color=CLAY_LIGHT, weight=BOLD),
        ).arrange(RIGHT, buff=0.55)
        self.play(LaggedStart(*[FadeIn(w, scale=1.08) for w in words], lag_ratio=0.15), run_time=1.2)
        self.wait(0.4)

        line1 = Text("Air shapes the flight.", font_size=35, color=OFF_WHITE)
        line2 = Text("Clay rewrites the bounce.", font_size=35, color=GOLD)
        takeaway = VGroup(line1, line2).arrange(DOWN, buff=0.25).move_to(DOWN * 0.9)
        self.play(words.animate.to_edge(UP), FadeIn(takeaway), run_time=0.9)

        final = create_title_card("The Hidden Science", "of Red Clay Tennis").move_to(ORIGIN)
        self.play(FadeOut(takeaway), FadeTransform(words, final), run_time=1.1)
        cta = Text("What surface should we explain next?", font_size=28, color=OFF_WHITE).to_edge(DOWN)
        self.play(FadeIn(cta), run_time=0.6)
        self.wait(0.8)


SCENE_TIMELINE = [
    (OpeningHookScene, 28),
    (AirForcesScene, 30),
    (SpinTrajectoryScene, 30),
    (EquationBuildScene, 30),
    (BouncePhysicsScene, 30),
    (ClayFrictionScene, 30),
    (RallyGeometryScene, 28),
    (LivingClayCourtScene, 28),
    (FinalSummaryScene, 24),
]


class PreviewCompositeScene(RedClayScene):
    """Fast one-command render for checking all chapters together."""

    def construct(self):
        for scene_cls, _target_duration in SCENE_TIMELINE:
            scene_cls.construct(self)
            self.play(FadeOut(*self.mobjects), run_time=0.35)


class FinalCompositeScene(RedClayScene):
    """Narration-paced full render, targeted at roughly 4.5 minutes."""

    def construct(self):
        for scene_cls, target_duration in SCENE_TIMELINE:
            start_time = self.time
            scene_cls.construct(self)
            elapsed = self.time - start_time
            remaining = max(0, target_duration - elapsed)
            if remaining > 0:
                self.wait(remaining)
            self.play(FadeOut(*self.mobjects), run_time=0.35)
