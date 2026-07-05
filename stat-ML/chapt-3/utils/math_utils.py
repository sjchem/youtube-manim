"""Small deterministic statistics helpers used by the scenes and docs."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def modes(values: Sequence[float]) -> list[float]:
    counts = Counter(values)
    top = max(counts.values())
    return sorted(value for value, count in counts.items() if count == top)


def variance(values: Sequence[float], sample: bool = False) -> float:
    center = mean(values)
    denominator = len(values) - 1 if sample else len(values)
    return sum((value - center) ** 2 for value in values) / denominator


def standard_deviation(values: Sequence[float], sample: bool = False) -> float:
    return math.sqrt(variance(values, sample=sample))


def percentile(values: Sequence[float], percent: float) -> float:
    """Linear-interpolated percentile for percent in [0, 100]."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (percent / 100) * (len(ordered) - 1)
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return ordered[int(rank)]
    weight = rank - low
    return ordered[low] * (1 - weight) + ordered[high] * weight


def covariance(xs: Sequence[float], ys: Sequence[float], sample: bool = False) -> float:
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    mx = mean(xs)
    my = mean(ys)
    denominator = len(xs) - 1 if sample else len(xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denominator


def correlation(xs: Sequence[float], ys: Sequence[float]) -> float:
    sx = standard_deviation(xs)
    sy = standard_deviation(ys)
    if sx == 0 or sy == 0:
        raise ValueError("correlation is undefined when either variable has zero standard deviation")
    return covariance(xs, ys) / (sx * sy)
