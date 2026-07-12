"""Small deterministic probability helpers used by the scenes and docs."""

from __future__ import annotations

from collections.abc import Sequence


def is_valid_probability(value: float) -> bool:
    """Check that a value is a legal probability in [0, 1]."""
    return 0.0 <= value <= 1.0


def conditional_probability(joint: float, given: float) -> float:
    """Return P(A | B) = P(A and B) / P(B)."""
    if given <= 0:
        raise ValueError("P(B) must be greater than zero to condition on it")
    return joint / given


def joint_probability(p_a_given_b: float, p_b: float) -> float:
    """Return P(A and B) = P(A | B) * P(B)."""
    return p_a_given_b * p_b


def marginal_probability(joint_row: Sequence[float]) -> float:
    """Sum a row or column of a joint-probability table to get the marginal."""
    return sum(joint_row)


def are_independent(p_a: float, p_b: float, p_a_and_b: float, tolerance: float = 1e-6) -> bool:
    """Check P(A and B) == P(A) * P(B) within a small tolerance."""
    return abs(p_a_and_b - (p_a * p_b)) < tolerance


def bayes_posterior(prior: float, likelihood: float, evidence: float) -> float:
    """Return P(H | E) = P(E | H) * P(H) / P(E)."""
    if evidence <= 0:
        raise ValueError("P(evidence) must be greater than zero")
    return (likelihood * prior) / evidence


def total_evidence(prior: float, likelihood_given_h: float, likelihood_given_not_h: float) -> float:
    """Return P(E) using the law of total probability for a binary hypothesis."""
    return likelihood_given_h * prior + likelihood_given_not_h * (1 - prior)


def normalize_distribution(values: Sequence[float]) -> list[float]:
    """Scale a list of non-negative scores so they sum to one."""
    total = sum(values)
    if total <= 0:
        raise ValueError("values must sum to a positive number")
    return [value / total for value in values]
