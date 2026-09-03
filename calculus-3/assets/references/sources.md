# Sources consulted for Part 3

Kept here so the explanations in `narration_script.md` and `concept_summary.md`
can be traced back to something checkable.

## Antiderivatives, +C, and volumes of revolution
- Gilbert Strang, *Calculus*, MIT OpenCourseWare — chapters on antiderivatives
  and on volumes by slicing. Source for the disk method used in Chapter 11.

## Differential equations, slope fields, initial-value problems
- V. I. Arnold, *Ordinary Differential Equations* — the geometric reading of an
  ODE as a direction field, which Chapter 4 is built on.
- M. W. Hirsch, S. Smale, R. L. Devaney, *Differential Equations, Dynamical
  Systems, and an Introduction to Chaos* — equilibria, solution families, and
  the role of an initial condition (Chapters 3, 4, 9).

## Growth, decay, and cooling
- The logistic model in Chapter 13 follows the standard `r y (1 − y/K)` form;
  its closed-form solution is used directly rather than integrated numerically.
- Newton's law of cooling is stated in *Philosophical Transactions of the Royal
  Society* 22 (1701), "Scala graduum caloris". The rate constant used on screen
  (k = 0.05 min⁻¹) is an illustrative value, not a measurement — see the
  "honest limits" section of `concept_summary.md`.

## Mechanics
- Isaac Newton, *Philosophiæ Naturalis Principia Mathematica* (1687) — the
  second law as a statement about how motion changes.
- Robert Hooke, *De Potentia Restitutiva* (1678) — "ut tensio, sic vis", the
  linear restoring force behind Chapter 10.

## The closing montage
- J. C. Maxwell, "A Dynamical Theory of the Electromagnetic Field" (1865).
- E. Schrödinger, "Quantisierung als Eigenwertproblem" (1926).
- The Navier–Stokes equations in the form given by Landau & Lifshitz,
  *Fluid Mechanics*, §15.
- R. T. Q. Chen, Y. Rubanova, J. Bettencourt, D. Duvenaud, "Neural Ordinary
  Differential Equations", NeurIPS 2018 — the `dh/dt = f(h, t; θ)` shown in
  Chapter 14.

## Numerical method
- The classical fourth-order Runge–Kutta step in `utils/math_utils.rk4_step`
  is the standard one; it is used only for the two-body orbit in Chapter 13,
  where no elementary closed form for r(t) exists.
