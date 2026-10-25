# Concept summary — Molecular Orbital Theory, Explained Visually

*Chemical Bonding · Part 3.* Follows *Chemical Bonding, Explained Visually*
(why atoms bond) and *Molecular Geometry, Explained Visually* (VSEPR and
hybridisation), which ended on the question this film answers.

## The question

Oxygen's Lewis structure, O=O with two lone pairs on each atom, shows every
electron paired. Yet liquid oxygen poured between the poles of a strong magnet
is drawn into the gap and hangs there. That response is the signature of
**unpaired electrons**. Where are they?

## The idea in one paragraph

When atoms come together, their atomic orbitals (AOs) — wave functions with a
sign, or phase — can be combined. In the **LCAO** approximation (linear
combination of atomic orbitals), two AOs give two molecular orbitals (MOs): the
in-phase sum, which piles electron density (|ψ|²) between the nuclei and lies
*lower* in energy (**bonding**), and the out-of-phase difference, which has a
node between the nuclei and lies *higher* (**antibonding**, marked \*). Within a finite basis, N independent basis
orbitals give N independent MO combinations. Head-on overlap of s or p orbitals makes **σ**
orbitals (symmetric about the bond axis); sideways p overlap makes **π**
orbitals, which come in **degenerate pairs**. Electrons fill the MO ladder by
Aufbau, Pauli and Hund's rule, and **bond order = (N_bonding − N_antibonding)/2**.
For second-period homonuclear diatomics there are two orderings: s–p mixing between compatible-symmetry combinations
lifts σ2p above the π pair for B₂, C₂ and N₂, but not for O₂ and F₂. Filling
oxygen's 12 valence electrons puts the last two in the two degenerate **π\***
orbitals, one each with parallel spins: bond order 2 *and* two unpaired
electrons — **paramagnetic**, as the magnet shows.

## Intuition → formal idea, in the film's order

| Step | Intuition (picture) | Formal idea |
|---|---|---|
| Hook | liquid O₂ hangs in a magnet's gap | paramagnetism ⇒ unpaired electrons; Lewis O=O shows none |
| Two pictures | handshake pair vs a cloud over the whole molecule | valence bond (localised) vs molecular orbital (delocalised) models |
| Waves | peaks align → taller; peak meets trough → cancel | superposition; sign = phase |
| LCAO | φA + φB piles up, φA − φB has a node | ψ± ∝ φA ± φB, normalised by 1/√(2 ± 2S); density = \|ψ\|² |
| Counting | 2 tiles in, 2 tiles out; 4 → 4 | N basis functions → N independent MOs (Hückel chain shown) |
| Shapes | one fused cloud vs two lobes with a nodal plane | σ1s, σ\*1s; same contour level, normalised |
| Energies | level splits; antibonding rises more | E± of H₂⁺ in LCAO: valley = bond (1.76 eV LCAO vs 2.79 eV exact) |
| H₂⁺, H₂ | one electron, then a pair | BO = ½, then 1; Pauli: opposite spins |
| He₂ | 2 bonding + 2 antibonding | BO = 0; He₂⁺ BO = ½; real He₂ is dispersion-bound, ~52 Å apart |
| σ / π from p | head-on vs side-by-side; flip the phase | σ2p/σ\*2p, π2p/π\*2p; two degenerate π, two degenerate π\* |
| The diagram | ladder of 8 valence MOs | 8 AOs → 8 MOs; Aufbau, Pauli, Hund |
| Orderings | σ2p crosses the π pair | s–p mixing of same-symmetry σ orbitals; weaker as the 2s–2p gap grows |
| N₂ | ten electrons, all paired | (σ2s)²(σ\*2s)²(π2p)⁴(σ2p)², BO = 3, diamagnetic |
| O₂ | the last two take one π\* each | BO = 2, two unpaired electrons, paramagnetic |
| O₂⁺, O₂⁻, O₂²⁻ | remove/add π\* electrons | BO 2.5, 1.5, 1; bonds lengthen as BO falls; 1, 1, 0 unpaired |
| B₂, F₂, C₂ | predict, then check | B₂: BO 1, paramagnetic; F₂: BO 1, diamagnetic; C₂: BO 2, diamagnetic |

## What the film is careful about (and why)

1. **Colour is phase, not charge.** Blue = ψ > 0, rose = ψ < 0; density is a
   separate cyan picture of |ψ|².
2. **LCAO is an approximation.** The count (N in → N out) is exact within the
   chosen basis; the simple sum/difference orbitals are not exact many-electron
   solutions. Chapter 07 shows the LCAO H₂⁺ valley next to the exact minimum.
3. **Bond order is a model quantity, not an existence test.** He₂ has bond
   order 0, yet an extremely weakly bound helium dimer exists (dispersion,
   ~1 mK, ~52 Å; Grisenti et al. 2000). Bond order also correlates with, but
   does not compute, bond energy (H₂ vs H₂⁺: ~1.7×, not 2×).
4. **Lewis ≠ valence bond theory.** Simple Lewis pairing misses O₂'s unpaired
   electrons; advanced valence bond calculations can describe them.
5. **Para/diamagnetism are responses to an applied field.** Liquid oxygen is
   not a permanent magnet: without the field its spins point every which way.
6. **Schematic energies.** MO diagram spacings are schematic; only the
   orderings are physics. The s–p mixing slider in chapter 13 is a toy map of a
   real trend (measured 2s–2p gaps), and says so on screen.
7. **Ion bond lengths depend on the salt** (superoxide ~128–133 pm), so the
   film shows them with "≈".

## Sources

* OpenStax, *Chemistry 2e*, §8.4 "Molecular Orbital Theory" (orderings, B₂,
  N₂, O₂ magnetism, bond order).
* K. P. Huber and G. Herzberg, *Constants of Diatomic Molecules* (1979), via
  the NIST Chemistry WebBook / CCCBDB: bond lengths and D₀.
* G. L. Miessler, P. J. Fischer and D. A. Tarr, *Inorganic Chemistry*, 5th ed.,
  Table 5.1 (O–O distances in O₂ species) and Table 5.2 (orbital potential
  energies, after Mann, Meek and Allen, JACS 122, 2780 (2000)).
* P. Atkins and J. de Paula, *Physical Chemistry*: LCAO treatment of H₂⁺ (S, j,
  k integrals).
* R. E. Grisenti et al., Phys. Rev. Lett. 85, 2284 (2000): the helium dimer.

All of these values live in `utils/mo_data.py`, and `python -m utils.mo_data`
checks every spoken claim against them and against the MO model.

## Visual model notes

The energy diagrams use schematic spacings, while the measured-length and
dissociation-energy comparisons use the cited data. The hydrogen-ion curve
includes internuclear repulsion and approaches H + H⁺ at large separation.
A node changes the wave function and its energy; it is not a material wall.
The small molecular spin arrows represent occupancy or magnetic moments, not
electron trajectories. Alignment is exaggerated for visibility, and the
magnet pour is an illustration rather than laboratory footage. Density-dot
views use a finite viewing window so their low-probability tails do not cross
labels; that display crop does not change the underlying normalised orbital.
