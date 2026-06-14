"""Small mathematical helpers used by the animation scenes."""

from __future__ import annotations

from fractions import Fraction
from functools import reduce
from operator import mul
from typing import Iterable


def require_nonzero_base(base: int | float) -> None:
    """Raise an explicit error when a zero base would break the zero-power rule."""

    if base == 0:
        raise ValueError("The zero-power rule in this project assumes a nonzero base.")


def power_sequence(base: int, highest: int, lowest: int = 0) -> list[tuple[int, int | Fraction]]:
    """Return descending exponent/value pairs for a positive integer base."""

    require_nonzero_base(base)
    sequence: list[tuple[int, int | Fraction]] = []
    for exponent in range(highest, lowest - 1, -1):
        if exponent >= 0:
            value: int | Fraction = base**exponent
        else:
            value = Fraction(1, base ** abs(exponent))
        sequence.append((exponent, value))
    return sequence


def exponential_points(base: int, x_values: Iterable[int]) -> list[tuple[int, int | Fraction]]:
    """Return points from y = base^x, keeping negative exponents exact."""

    return [(x, base**x if x >= 0 else Fraction(1, base ** abs(x))) for x in x_values]


def empty_product(factors: Iterable[int | float]) -> int | float:
    """The product over no factors is the multiplicative identity: 1."""

    return reduce(mul, factors, 1)


def latex_fraction(value: int | Fraction) -> str:
    """Convert an integer or Fraction into a compact LaTeX fragment."""

    if isinstance(value, Fraction):
        return rf"\frac{{{value.numerator}}}{{{value.denominator}}}"
    return str(value)
