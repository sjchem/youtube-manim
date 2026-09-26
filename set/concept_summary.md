# Mathematical content

The video introduces finite sets through choices of named ingredients,
animals, and numbers, then states laws valid for arbitrary subsets of a
specified universe. Physical baskets, lunchboxes, and fences are visual models;
sets do not depend on physical position, container size, or a drawn boundary.

| Idea | Example and conclusion |
|---|---|
| Membership | Apple belongs to the fruit set; pizza does not. |
| Order and repetition | Reordering named members changes nothing; repeated “apple” adds no new named element. |
| Subset | Cat family ⊆ mammals ⊆ the animals considered. A dog refutes mammals ⊆ cat family. |
| Empty set | No elements means no counterexample to ∅ ⊆ A. The symbol ∅ is a label, not a member. |
| Overlap | The platypus belongs to mammals and egg-laying kinds. |
| Union | {mushroom, olive} ∪ {olive, pepper} = {mushroom, olive, pepper}. |
| Intersection | The two topping orders share only olive. |
| Cardinality | Among 1…10, primes ∩ evens = {2}; its cardinality is 1. The union has 8 members. |
| Complement | Among six available kitchen toppings, removing mozzarella and ricotta leaves four. If U is restricted to dairy itself, its complement is empty. |
| First De Morgan law | (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ. Exclude dairy or meat; equivalently, require not dairy and not meat. |
| Second De Morgan law | (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ. A toy blocked exactly when red and square may pass when not red or not square. |

All complements in a formula use the same universe. “Or” is inclusive.
“Not both” allows one condition to hold; “neither” allows neither to hold.
A two-circle picture illustrates the laws. The first law’s narration also gives
a two-way arbitrary-element argument, which establishes the identity beyond
the particular drawing. The second is explained through the exact gate rule
and the equivalent membership conditions.

The fruit pictures refer to named elements, not separately identified apples.
“Cats” means the cat family, including the tiger. The snake is explicitly an
egg-laying kind; not every snake species lays eggs. Biology references are
kept in `assets/references/references.md`.

`utils/set_models.py` contains reference examples and operation helpers.
`story_world.py` supplies picture and region geometry. Scene choreography also
contains explicit positions and example labels; changing examples requires
reviewing both the narration and animation.

## The connected rule chain

The displayed mathematics uses a single arbitrary element `x` to make the
rules comparable. Fix a universe `U`. Then `A ⊆ B` means every `x ∈ A` is also
in `B`. The empty set satisfies this condition because it has no members to
violate it. Union changes the membership test to `x ∈ A` **or** `x ∈ B`;
intersection changes it to **and**. Complement means `x ∈ U` **and** `x ∉ A`.
De Morgan's laws follow by applying these tests to each side. Scene 12 revisits
the chain one formula at a time. The symbols are shown after concrete fruit,
animal, topping and toy examples have supplied their meaning.
