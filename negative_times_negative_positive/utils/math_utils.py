"""Small mathematical helpers used by the scenes and scripts."""

from __future__ import annotations


def sign_product(a: float, b: float) -> float:
    """Return a * b with ordinary signed-number arithmetic."""
    return a * b


def multiplication_pattern(multiplier: int, multiplicand: int, start: int, end: int) -> list[dict[str, int]]:
    """Generate rows for n * multiplicand while n runs from start to end."""
    step = 1 if end >= start else -1
    return [
        {"multiplier": n, "multiplicand": multiplicand, "product": n * multiplicand}
        for n in range(start, end + step, step)
    ]


def distributive_negative_proof(a: int, b: int) -> dict[str, int | str]:
    """Return the key values in (-a)(b + -b) = (-a)b + (-a)(-b)."""
    left_factor = -abs(a)
    positive_b = abs(b)
    known = left_factor * positive_b
    unknown = -known
    return {
        "left_factor": left_factor,
        "positive_b": positive_b,
        "negative_b": -positive_b,
        "known_product": known,
        "unknown_product": unknown,
        "whole_expression": f"{left_factor}({positive_b}+{-positive_b})",
    }


def format_signed_number(n: int | float) -> str:
    """Format numbers with an explicit plus sign for positives."""
    if n > 0:
        return f"+{int(n) if float(n).is_integer() else n}"
    return str(int(n) if float(n).is_integer() else n)


def generate_number_line_ticks(start: int, end: int, step: int = 1) -> list[int]:
    """Generate evenly spaced integer ticks for a number line."""
    if step == 0:
        raise ValueError("step must not be zero")
    direction = 1 if end >= start else -1
    signed_step = abs(step) * direction
    return list(range(start, end + direction, signed_step))
