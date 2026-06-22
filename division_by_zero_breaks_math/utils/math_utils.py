"""Small mathematical helpers used by the scenes and narration."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Iterable


def division_as_inverse_equation(a: float, b: float, c_symbol: str = "c") -> str:
    """Return the reverse-multiplication form of a / b = c."""

    return f"{c_symbol} \\times {b:g} = {a:g}"


def multiply_by_zero(values: Iterable[float]) -> list[float]:
    """Model the information collapse caused by multiplication by zero."""

    return [0.0 for _ in values]


def has_solution_for_division_by_zero(numerator: float) -> bool:
    """Only 0 / 0 has candidates; non-zero / 0 has no solution."""

    return isclose(numerator, 0.0)


def reciprocal_samples() -> list[tuple[float, float]]:
    """Stable points for the 1/x limit animation."""

    xs = [1, 0.5, 0.1, 0.01, -0.1, -0.01]
    return [(x, 1 / x) for x in xs]


@dataclass(frozen=True)
class DivisionByZeroCase:
    expression: str
    reverse_question: str
    result: str
    reason: str


CASES = [
    DivisionByZeroCase(
        expression="6 \\div 0",
        reverse_question="? \\times 0 = 6",
        result="No solution",
        reason="zero multiplication can only produce zero",
    ),
    DivisionByZeroCase(
        expression="0 \\div 0",
        reverse_question="? \\times 0 = 0",
        result="Indeterminate",
        reason="every number is a candidate, so no unique value exists",
    ),
]
