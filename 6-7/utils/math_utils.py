"""Small exact math helpers used by the animation scenes."""

from __future__ import annotations

from math import gcd, sqrt


CYCLIC_DIGITS = "142857"


def proper_divisors(n: int) -> list[int]:
    """Return the positive proper divisors of n."""

    return [value for value in range(1, n) if n % value == 0]


def is_perfect(n: int) -> bool:
    """Return whether n is a perfect number."""

    return sum(proper_divisors(n)) == n


def polygon_interior_angle(n: int) -> float:
    """Interior angle of a regular n-gon in degrees."""

    return (n - 2) * 180 / n


def cyclic_rotation(k: int, digits: str = CYCLIC_DIGITS) -> str:
    """Return the 1/7 cyclic number multiplied by k for 1 <= k <= 6."""

    if not 1 <= k <= 6:
        raise ValueError("k must be between 1 and 6")
    return str(int(digits) * k).zfill(6)


def long_division_by_7() -> list[tuple[int, int, int]]:
    """Return (remainder in, digit out, remainder out) for 1/7."""

    rows: list[tuple[int, int, int]] = []
    remainder = 1
    for _ in range(6):
        value = remainder * 10
        digit = value // 7
        next_remainder = value % 7
        rows.append((remainder, digit, next_remainder))
        remainder = next_remainder
    return rows


def sum_of_two_squares_pairs(limit: int) -> list[tuple[int, int, int]]:
    """Return nonnegative a, b pairs with a^2 + b^2 <= limit."""

    pairs: list[tuple[int, int, int]] = []
    max_root = int(sqrt(limit))
    for a in range(max_root + 1):
        for b in range(a, max_root + 1):
            value = a * a + b * b
            if value <= limit:
                pairs.append((a, b, value))
    return sorted(pairs, key=lambda item: (item[2], item[0], item[1]))


def are_coprime(a: int, b: int) -> bool:
    """Return whether two integers have greatest common divisor 1."""

    return gcd(a, b) == 1


def factorial(n: int) -> int:
    """Compute n! without importing heavier tools."""

    result = 1
    for value in range(2, n + 1):
        result *= value
    return result
