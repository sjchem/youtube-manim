# Expanded explanation: teaching and reference notes

Audience: senior secondary / introductory university chemistry. Keep the user's 19 chapters and 35:20 windows.
The supplied transcript for [A Brief Guide to Quantum Model of Atom](https://www.youtube.com/watch?v=-4-TJMhGlX8)
was used to identify useful teaching questions, not as text to copy or as a source for all scientific claims.
The video itself was not played during this review.

## Questions answered by the revised visuals

1. **How can one electron show interference?** The source and screen register separate events.
   Pulses at both openings illustrate amplitude contributions, without inventing a measured route.
   Adding amplitudes before squaring produces a cross term. A detector that leaves distinguishable
   path records removes that term. The fresh recorded pattern retains the same single-slit envelope.
   A person's awareness is not part of this calculation.
2. **Does uncertainty prohibit knowing anything about position and momentum together?**
   No: corresponding components have statistical spreads whose product is bounded.
   Radius and speed alone are not exact position and momentum vectors.
3. **Where is hydrogen 1s most concentrated?** Point density is greatest at the nucleus.
   The radial probability density peaks at a0 because a spherical shell contributes a volume factor.
   Integrating the normalized radial density gives 32.332% inside a0 and 90% inside 2.66116 a0.
   The displayed circle is a section through that sphere; its disk is not the integrated volume.
4. **What do the quantum numbers measure?** In the nonrelativistic hydrogen model,
   L² = l(l+1) hbar² and Lz = ml hbar. For 2pz, L² = 2 hbar² while Lz = 0.
   An s state has zero orbital angular momentum, unlike Bohr's circulating ground-state electron.
   Spin projections are Sz = ms hbar = ±hbar/2.
5. **Where do the capacities come from?** Sum 2l+1 spatial states over a shell to obtain n²;
   two spin states and Pauli exclusion give maximum capacity 2n². Capacity is not an occupancy order.
6. **Why does 4s appear before 3d for potassium?** Madelung ordering is a guide.
   The ground configuration minimizes total energy; relative orbital energies change with occupancy and ionization.

## Approximation and analogy boundaries

- Ring closure recovers Bohr quantization in a constrained ring model, not the full 3D hydrogen angular-momentum rule.
- The double-slit profile uses equal Gaussian far-field amplitudes in schematic coordinates.
  With coherence c, intensity is g(y)[1+c cos(2ky)]. It is normalized when sampling detections.
  Changing c modifies the cross term, not the assumed envelope.
- A cat-photo histogram illustrates repeated sampling only. It does not imply an electron follows an unknown classical path.
- Hydrogen radial curves illustrate penetration. Their radii are not calibrated many-electron orbitals.
  The 3d tail has small, nonzero inner probability.
- Radial and angular node counts for these hydrogen states are n−l−1 and l.
  Real px/py and most named d orbitals combine magnetic eigenstates; do not assign each a literal ml value.

## Primary educational references

- [Feynman Lectures III, chapter 1](https://www.feynmanlectures.caltech.edu/III_01.html):
  individual detections, amplitudes, interference and path detection.
- [OpenStax: Heisenberg uncertainty](https://openstax.org/books/university-physics-volume-3/pages/7-2-the-heisenberg-uncertainty-principle):
  wave packets and statistical position/momentum spreads.
- [OpenStax: hydrogen atom](https://openstax.org/books/university-physics-volume-3/pages/8-1-the-hydrogen-atom):
  normalized wave functions, radial probability and angular-momentum quantum numbers.
- [OpenStax: development of quantum theory](https://openstax.org/books/chemistry-2e/pages/6-3-development-of-quantum-theory):
  orbitals and quantum labels.
- [OpenStax: electron configurations](https://openstax.org/books/chemistry-2e/pages/6-4-electronic-structure-of-atoms-electron-configurations):
  exclusion, filling and exceptions.

The probability values above are calculated in utils/quantum_examples.py and checked independently
against integration of the actual radial wave function by utils/audit.py.
