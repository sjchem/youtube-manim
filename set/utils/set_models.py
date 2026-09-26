"""Reference set examples and operation helpers for the visual lesson.

Scenes use these definitions for the number and pizza challenges. Choreography
also contains explicit labels and positions, so changing an example requires
reviewing the matching animation and narration. De Morgan's laws are evaluated
independently on both sides by de_morgan_report.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import chain

# ---------------------------------------------------------------------------
# Core operations, written out rather than delegated, so the names in the film
# and the names in the code are the same names.
# ---------------------------------------------------------------------------


def union(a: Iterable[str], b: Iterable[str]) -> set[str]:
    """A ∪ B — every element in A, in B, or in both."""
    return {item for item in chain(a, b)}


def intersection(a: Iterable[str], b: Iterable[str]) -> set[str]:
    """A ∩ B — only the elements that pass both rules."""
    b_set = set(b)
    return {item for item in a if item in b_set}


def complement(universe: Iterable[str], a: Iterable[str]) -> set[str]:
    """Aᶜ — everything in the universe that is not in A."""
    a_set = set(a)
    return {item for item in universe if item not in a_set}


def difference(a: Iterable[str], b: Iterable[str]) -> set[str]:
    """A \\ B — in A, but refused by B."""
    b_set = set(b)
    return {item for item in a if item not in b_set}


def is_subset(a: Iterable[str], b: Iterable[str]) -> bool:
    """A ⊆ B — true exactly when no counterexample exists."""
    return counterexample(a, b) is None


def counterexample(a: Iterable[str], b: Iterable[str]) -> str | None:
    """The first element of A that is not in B — what the subset scanner hunts.

    ``None`` means the scan found nothing, which is the whole content of
    ``A ⊆ B``. For an empty A there is nothing to scan, so the answer is
    vacuously ``None``: that is why ∅ is a subset of every set.
    """
    b_set = set(b)
    for item in a:
        if item not in b_set:
            return item
    return None


def cardinality(a: Iterable[str]) -> int:
    """|A| — how many distinct memberships the set holds."""
    return len(set(a))


# ---------------------------------------------------------------------------
# The film's worked examples
# ---------------------------------------------------------------------------

FRUIT_BOARD = ("apple", "banana", "pizza", "strawberry", "carrot", "grapes")
FRUIT = ("apple", "banana", "strawberry", "grapes")

ANIMALS = ("cat", "tiger", "dog", "whale", "chicken", "duck", "platypus", "snake")
MAMMALS = ("cat", "tiger", "dog", "whale", "platypus")
CATS = ("cat", "tiger")
EGG_LAYERS = ("chicken", "duck", "platypus", "snake")

NUMBER_UNIVERSE = tuple(str(n) for n in range(1, 11))
PRIMES = ("2", "3", "5", "7")
EVENS = ("2", "4", "6", "8", "10")

TOPPINGS = (
    "mozzarella", "ricotta", "bacon", "sausage",
    "mushroom", "olive", "onion", "pepper",
)
DAIRY = ("mozzarella", "ricotta")
MEAT = ("bacon", "sausage")


@dataclass(frozen=True)
class Example:
    """One universe with two rules inside it — the film's recurring setup."""

    universe: tuple[str, ...]
    a: tuple[str, ...]
    b: tuple[str, ...]
    a_label: str
    b_label: str
    universe_label: str

    def only_a(self) -> set[str]:
        return difference(self.a, self.b)

    def only_b(self) -> set[str]:
        return difference(self.b, self.a)

    def both(self) -> set[str]:
        return intersection(self.a, self.b)

    def neither(self) -> set[str]:
        return complement(self.universe, union(self.a, self.b))


ANIMAL_EXAMPLE = Example(
    universe=ANIMALS, a=MAMMALS, b=EGG_LAYERS,
    a_label="MAMMALS", b_label="EGG-LAYERS", universe_label="ANIMALS",
)
NUMBER_EXAMPLE = Example(
    universe=NUMBER_UNIVERSE, a=PRIMES, b=EVENS,
    a_label="PRIME", b_label="EVEN", universe_label="1 … 10",
)
PIZZA_EXAMPLE = Example(
    universe=TOPPINGS, a=DAIRY, b=MEAT,
    a_label="DAIRY", b_label="MEAT", universe_label="TOPPINGS",
)


# ---------------------------------------------------------------------------
# De Morgan, verified on the film's own examples
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DeMorganReport:
    """Both sides of both laws, on one concrete universe."""

    not_a_or_b: set[str]        # (A ∪ B)ᶜ
    not_a_and_not_b: set[str]   # Aᶜ ∩ Bᶜ
    not_a_and_b: set[str]       # (A ∩ B)ᶜ
    not_a_or_not_b: set[str]    # Aᶜ ∪ Bᶜ

    @property
    def first_law_holds(self) -> bool:
        return self.not_a_or_b == self.not_a_and_not_b

    @property
    def second_law_holds(self) -> bool:
        return self.not_a_and_b == self.not_a_or_not_b


def de_morgan_report(example: Example) -> DeMorganReport:
    """Evaluate all four regions independently, then compare them."""
    a_c = complement(example.universe, example.a)
    b_c = complement(example.universe, example.b)
    return DeMorganReport(
        not_a_or_b=complement(example.universe, union(example.a, example.b)),
        not_a_and_not_b=intersection(a_c, b_c),
        not_a_and_b=complement(example.universe, intersection(example.a, example.b)),
        not_a_or_not_b=union(a_c, b_c),
    )


def de_morgan_holds_everywhere() -> bool:
    """True when both laws survive every worked example in the film."""
    return all(
        de_morgan_report(example).first_law_holds and de_morgan_report(example).second_law_holds
        for example in (ANIMAL_EXAMPLE, NUMBER_EXAMPLE, PIZZA_EXAMPLE)
    )


def truth_table_rows() -> list[tuple[bool, bool, bool, bool]]:
    """¬(p ∨ q) against (¬p) ∧ (¬q): the logic twin of the first law."""
    rows = []
    for p in (True, False):
        for q in (True, False):
            rows.append((p, q, not (p or q), (not p) and (not q)))
    return rows
