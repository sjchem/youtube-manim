# Concept summary — Beyond Ideal Gases

*How Molecules Become Liquids* · States of Matter, Part 2 · Class 11 Chemistry (NCERT Unit 5, §5.7–5.11)

## The question

Part 1 ended with one elegant equation, PV = nRT. Yet carbon dioxide squeezed at
room temperature turns into a liquid — something particles with no size and no
attraction could never do. Why do real gases depart from the ideal gas
equation, how do the same molecules become a liquid, and what gives liquids
their properties?

## The chain of reasoning

1. **Speeds are distributed, not shared.** Elastic collisions conserve total
   kinetic energy and momentum but hand energy from one molecule to another
   (N₂ at 1 bar and 300 K: billions of collisions per molecule per second).
   Started at one speed, a 2D hard-disk gas relaxes to a steady equilibrium
   distribution: individual motion is unpredictable, the distribution is
   predictable. In 3D, velocity tips form a round cloud densest at the centre;
   counting tips in a thin shell of area 4πu² gives the **Maxwell–Boltzmann**
   speed distribution f(u) ∝ u² e^(−mu²/2k_BT): few slow molecules (the shell is
   tiny), a peak, a long fast tail.
   - u_mp = √(2RT/M) < u_av = √(8RT/πM) < u_rms = √(3RT/M), ratio 1 : 1.128 : 1.225.
     N₂ at 300 K: ≈ 420, ≈ 480, ≈ 520 m/s (M in kg mol⁻¹).
   - ⟨K⟩ = 3/2 k_BT: doubling T (300 → 600 K) multiplies speeds by √2 ≈ 1.41;
     the curve broadens and its peak drops (area stays 1). u ∝ 1/√M: Cl₂
     (≈ 2.5 × heavier) is slower than N₂.
2. **Kinetic molecular theory** lists six assumptions (huge numbers,
   negligible volume, no forces between collisions, random motion, elastic
   collisions, ⟨K⟩ set by T). Two fail first: in air the molecules fill less
   than a thousandth of the space, but squeezed gases crowd; slow, close
   molecules feel each other's attraction. The ideal gas works best at low P
   and high T.
3. **Real gases deviate in two directions.** Attraction (green) lowers the
   pressure — a molecule at the wall is pulled back into the gas — a negative
   deviation, P_real < P_ideal (a mean-field picture). Size and repulsion (red)
   raise it — less free room, more frequent wall hits — a positive deviation.
   Low P: nearly ideal; moderate P: attraction usually wins; very high P: size
   wins. Heating weakens attraction's effect; He and H₂ at room temperature
   show positive deviation over the model pressures shown.
4. **The van der Waals equation** repairs PV = nRT. Nearby pairs grow with the
   square of density (doubling density gives ≈ 4 × the pairs), so
   P_* = P + an²/V², where P_* = nRT/(V − nb) is the same size-corrected gas with attraction switched off. Hard spheres of diameter d exclude a sphere of
   radius d around each other — 8 molecular volumes per pair, **4 per molecule**,
   so b ≈ 4 × the molecules' own volume and V_available ≈ V − nb.
   **(P + an²/V²)(V − nb) = nRT.** 1 mol CO₂ in 1 L at 300 K: ideal ≈ 24.9 bar,
   size correction → ≈ 26.1 bar, attraction −3.6 → ≈ 22.4 bar (≈ 10 % below
   ideal). In 100 L both corrections almost vanish.
5. **Compressibility factor Z = PV/nRT** (= V_real/V_ideal at the same P, T and n).
   Z = 1 satisfies the ideal equation at that state; Z < 1 often indicates attraction dominates, while Z > 1 often indicates crowding and repulsion dominate. At 300 K
   (van der Waals model): CH₄ dips, N₂ dips a little, H₂ and He rise at once.
   At the **Boyle temperature** the curve leaves Z = 1 flat (measured: N₂ ≈ 327 K,
   He ≈ 23 K). Z = 1 can be a cancellation of two strong effects.
6. **Liquefaction and the critical point.** Andrews (1869) squeezed CO₂ at
   constant temperature: gas → a flat coexistence line where liquid and vapour
   share the vessel (squeezing only converts vapour to liquid) → a steep liquid
   branch. The flat stretch shrinks with temperature and vanishes at the
   **critical point**: CO₂ T_c ≈ 304.1 K (≈ 31 °C), P_c ≈ 73.8 bar. In a sealed
   tube the liquid and vapour densities converge and the meniscus vanishes.
   The van der Waals equation itself predicts this: below T_c its isotherms
   wiggle (an unstable branch where squeezing would lower P); Maxwell's
   equal-area line gives the coexistence pressure; T_c = 8a/27Rb (in practice a
   and b are often fitted to measured critical constants). On the P–V–T
   surface the coexistence region is a valley whose two edges meet at the critical
   point; going **around** it (heat, squeeze, cool) turns gas into liquid with
   no droplets and no interface: a **supercritical fluid**, above both T_c and P_c, is one phase.
   Condensation crosses the boundary; the critical point is where it ends.
   Liquefaction needs cooling below T_c plus compression: T_c(CO₂) ≈ 31 °C is
   just above room temperature; T_c(N₂) ≈ 126 K (≈ −150 °C) must be cooled first;
   T_c(NH₃) ≈ 405.5 K (strong attraction, partly hydrogen bonds).
7. **Vapour pressure and boiling.** Liquid molecules share the same energy
   spread; fast ones at the surface escape (evaporation); in a sealed vessel
   vapour builds until condensation matches evaporation — a **dynamic
   equilibrium** at the equilibrium (saturated) vapour pressure, set by the
   liquid and T, not the container. A liquid boils when P_vapour = P_external:
   ether ≈ 35 °C, ethanol ≈ 78 °C, water 100 °C at 1 atm; ≈ 70 °C on Everest
   (≈ 1/3 atm); ≈ 120 °C in a pressure cooker (≈ 2 bar).
8. **Surface tension.** A surface molecule has fewer neighbours than one inside
   and sits at higher energy, so making surface costs work: dW = γ dA
   (γ in N m⁻¹ = J m⁻²; water ≈ 73 mN/m at 20 °C). Free drops become spheres
   (≈ a fifth less area than a cube of equal volume). Water wets glass and
   rises in a capillary; mercury is depressed. γ falls with T and reaches zero
   at the critical point (water ≈ 374 °C).
9. **Viscosity.** Between a still plate and a sliding plate a liquid flows in
   layers (laminar flow) with a velocity gradient du/dz; momentum carried
   between layers and intermolecular attraction resist sliding:
   F/A = η du/dz (Newtonian liquids; η in Pa s). Honey can be thousands of
   times more viscous than water; warming lowers viscosity (water at 100 °C:
   less than a third of its 20 °C value). Glass is an amorphous solid, not a
   slow liquid. Honey is a concentrated sugar solution; the polymer-chain picture is a separate example, not a molecular model of honey.
10. **Synthesis.** Real molecules move at many speeds, attract one another and
    take up space. Far apart and fast, those details fade and PV = nRT works;
    squeezed or slowed, they decide everything — deviations, liquefaction,
    the critical point, evaporation, drops and flow. The molecules never
    change; how fast they move, how closely they are packed and how strongly
    they interact does.

## Models, simplifications and metaphors (named on screen or in narration)

- **2D hard-disk model** (scene 04): a real simulation of 240 elastic disks, all
  starting at one speed. Labelled 2D; its equilibrium curve is the 2D one, not
  the 3D Maxwell–Boltzmann curve.
- **Velocity-space cloud** (scene 05): 3D sample from the equilibrium Gaussian;
  the shell is a counting device, not a physical object.
- **Gas boxes**: point molecules (ideal) or **hard spheres** (scenes 03, 09, 11:
  real elastic sphere collisions, live); speeds scaled to be watchable.
- **Attraction at the wall** (scene 10): the single-tug picture is a teaching
  simplification of a mean-field average, said so in the narration.
- **Van der Waals model** for Z curves, isotherms, Andrews' plateau and the
  3D P–V–T surface, always called a model; the drawn cylinder's height is
  proportional to the model's volume; the liquid's molecules are schematic.
- **Liquid snapshot** (scene 25): a schematic disordered packing.
- **Falling balls** (scene 28): speeds illustrative, not to scale.

## Additional review clarifications

The attraction correction uses a size-corrected reference pressure P_*;
it must not be equated to nRT/V while b is nonzero. V − nb is the van der Waals
free-volume approximation. The model critical temperature depends on a/b.

Vapour pressure is independent of vessel size only while liquid and vapour
coexist at equilibrium. Escape needs suitable energy, direction and local
molecular surroundings; the highlighted speed tail is schematic. Water's
saturation-pressure plot uses IAPWS SR1-86(1992), continuously through its
critical endpoint. Sealing a vessel does not forbid boiling or bubbles.
A two-sided soap film has F = 2γL; one interface has force γ per unit edge length.
