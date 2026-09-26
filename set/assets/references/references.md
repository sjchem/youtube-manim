# References

Sources consulted for the mathematics and for the one biological claim the film
makes. Page-level pointers are to the definitions and results the film actually
uses, not to the books in general.

## Set theory

* **Halmos, P. R. (1960). _Naive Set Theory_. Springer.**
  §1–§4. Extensionality, the empty set, and the subset relation. The film's
  treatment of `∅ ⊆ A` as a vacuous truth — no counterexample exists, therefore
  the claim holds — follows Halmos's framing rather than treating it as a
  convention.

* **Enderton, H. B. (1977). _Elements of Set Theory_. Academic Press.**
  Chapter 2. The algebra of sets, including formal proofs of both De Morgan
  laws by two-way membership argument. This is the proof `concept_summary.md`
  reproduces in outline, and the reason the film is careful to call its own
  picture argument a picture argument.

* **Velleman, D. J. (2019). _How to Prove It_, 3rd ed. Cambridge.**
  Chapter 1. The propositional De Morgan laws, ¬(p ∨ q) ≡ (¬p) ∧ (¬q) and
  ¬(p ∧ q) ≡ (¬p) ∨ (¬q), and their relationship to the set-theoretic versions.
  Chapter 10 of the film makes exactly this bridge.

* **Venn, J. (1880). "On the diagrammatic and mechanical representation of
  propositions and reasonings." _Philosophical Magazine_ 10(59), 1–18.**
  The original paper. Venn's own point — that the diagram represents the
  logical relations between the propositions, not the objects — is the point
  chapter 5 makes when the circles move.

## Biology checked for this revision

* [Australian Museum: Platypus](https://australian.museum/learn/animals/mammals/platypus/).
  Confirms that platypuses are egg-laying mammals.
* [Australian Museum: Reptiles](https://australian.museum/learn/animals/reptiles/).
  Reproduction includes egg-laying and live birth. The film therefore describes
  its snake card as an egg-laying snake, rather than generalising to all snakes.

## Tooling

* **Manim Community Edition 0.21.0 (installed for this review)** — <https://docs.manim.community/>
  `ThreeDScene`, `Prism`, `Cylinder`, and the boolean operations
  (`Union`, `Intersection`, `Difference`) that produce every region mask in
  this film.
