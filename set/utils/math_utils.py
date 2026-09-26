"""Geometry behind the Venn layouts: where a circle sits, where a card lands.

The film's promise is that the picture and the algebra agree. That only holds
if a card belonging to ``A ∩ B`` is physically inside both circles, so the
seating positions here are computed from the circle geometry rather than
eyeballed. :func:`classify_point` is the inverse check, and the layout audit
uses it to catch a card that drifted into the wrong region.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

Point = np.ndarray


def circle_centres(separation: float, y: float = 0.0) -> tuple[Point, Point]:
    """Centres of the two Venn circles, symmetric about the vertical axis."""
    return (
        np.array([-separation / 2, y, 0.0]),
        np.array([separation / 2, y, 0.0]),
    )


def lens_half_width(radius: float, separation: float) -> float:
    """Half the horizontal extent of the overlap, or 0 when the circles are apart."""
    return max(radius - separation / 2, 0.0)


def lens_half_height(radius: float, separation: float) -> float:
    """Half the vertical extent of the overlap lens."""
    if separation >= 2 * radius:
        return 0.0
    return float(np.sqrt(max(radius**2 - (separation / 2) ** 2, 0.0)))


def overlaps(radius: float, separation: float) -> bool:
    """True when the two equal circles genuinely intersect."""
    return separation < 2 * radius


def ring_seats(
    centre: Sequence[float],
    count: int,
    radius: float,
    *,
    start_angle: float = np.pi / 2,
) -> list[Point]:
    """Evenly spaced seats on a circle of the given radius, starting at the top."""
    origin = np.asarray(centre, dtype=float)
    if count <= 0:
        return []
    if count == 1:
        return [origin.copy()]
    return [
        origin + radius * np.array([
            np.cos(start_angle + 2 * np.pi * index / count),
            np.sin(start_angle + 2 * np.pi * index / count),
            0.0,
        ])
        for index in range(count)
    ]


def stacked_seats(
    centre: Sequence[float],
    count: int,
    *,
    columns: int = 2,
    x_step: float = 0.98,
    y_step: float = 1.02,
) -> list[Point]:
    """A compact block of seats — used inside a circle or inside the lens."""
    origin = np.asarray(centre, dtype=float)
    if count <= 0:
        return []
    columns = max(1, min(columns, count))
    rows = int(np.ceil(count / columns))
    seats: list[Point] = []
    for index in range(count):
        row, column = divmod(index, columns)
        in_row = min(columns, count - row * columns)
        seats.append(
            origin
            + np.array([
                (column - (in_row - 1) / 2) * x_step,
                -(row - (rows - 1) / 2) * y_step,
                0.0,
            ])
        )
    return seats


def seats_only_in(
    centre: Sequence[float],
    other_centre: Sequence[float],
    radius: float,
    count: int,
    *,
    inset: float = 0.52,
) -> list[Point]:
    """Seats inside one circle and safely clear of the other circle.

    The seats are pushed away from the neighbour along the line joining the two
    centres, so a 'only in A' card can never stray into the lens.
    """
    origin = np.asarray(centre, dtype=float)
    away = origin - np.asarray(other_centre, dtype=float)
    norm = np.linalg.norm(away)
    direction = away / norm if norm > 1e-9 else np.array([-1.0, 0.0, 0.0])
    anchor = origin + direction * radius * inset * 0.62
    # A card may carry its name underneath, so the vertical pitch has to clear
    # a card plus its label, not just a card.
    return stacked_seats(anchor, count, columns=1 if count < 3 else 2,
                         x_step=radius * 0.62, y_step=radius * 0.74)


def classify_point(
    point: Sequence[float],
    centre_a: Sequence[float],
    centre_b: Sequence[float],
    radius: float,
) -> str:
    """Name the Venn region a point falls in: 'a', 'b', 'both' or 'neither'."""
    position = np.asarray(point, dtype=float)[:2]
    in_a = np.linalg.norm(position - np.asarray(centre_a, dtype=float)[:2]) <= radius
    in_b = np.linalg.norm(position - np.asarray(centre_b, dtype=float)[:2]) <= radius
    if in_a and in_b:
        return "both"
    if in_a:
        return "a"
    if in_b:
        return "b"
    return "neither"


def scatter_outside(
    count: int,
    centre_a: Sequence[float],
    centre_b: Sequence[float],
    radius: float,
    *,
    box: tuple[float, float] = (11.0, 5.4),
    clearance: float = 0.72,
    seed: int = 20260923,
) -> list[Point]:
    """Seats inside the universe rectangle but outside both circles.

    Rejection sampling with a clearance margin, so a 'neither' card is visibly
    outside, not merely mathematically outside.
    """
    rng = np.random.default_rng(seed)
    half_w, half_h = box[0] / 2, box[1] / 2
    seats: list[Point] = []
    attempts = 0
    while len(seats) < count and attempts < 8000:
        attempts += 1
        candidate = np.array([
            rng.uniform(-half_w, half_w),
            rng.uniform(-half_h, half_h),
            0.0,
        ])
        if classify_point(candidate, centre_a, centre_b, radius + clearance) != "neither":
            continue
        if any(np.linalg.norm(candidate - seat) < 1.35 for seat in seats):
            continue
        seats.append(candidate)
    return seats


def interpolate_points(start: Sequence[float], end: Sequence[float], count: int) -> list[Point]:
    """Sample points along a straight path — used by the scanner beam."""
    first = np.asarray(start, dtype=float)
    last = np.asarray(end, dtype=float)
    if count <= 1:
        return [first.copy()]
    return [first + (last - first) * t for t in np.linspace(0.0, 1.0, count)]
