# Concept summary — System of Particles & Rotational Motion

**One question:** why can the same force make one object move in a straight
line, another rotate, and a third do both?

**One answer:** forces decide how the *centre of mass* moves; *torques* decide
how the rotation changes; and the *moment of inertia* connects a body's shape
to its spin.

## The chain of ideas

1. **Extended and rigid bodies.** A point particle has mass but no size. Real
   bodies are many particles; a *rigid body* keeps every inter-particle
   distance fixed (|r_i − r_j| = constant) — an idealisation that works when
   deformation is negligible. It can translate, rotate about a fixed axis, or
   both (rolling).
2. **Centre of mass.** The mass-weighted average position:
   x_cm = (m₁x₁ + m₂x₂)/(m₁ + m₂); in general R_cm = (1/M) Σ mᵢrᵢ, or
   (1/M) ∫ r dm for a continuous body. Its physical location does not depend on the choice of
   origin (its coordinate vector does), sits at the centre of uniform symmetric bodies, shifts toward
   concentrated mass, and can lie in empty space (a ring).
   *Worked:* 2 kg at 0, 6 kg at 4 m → x_cm = 24/8 = 3 m.
3. **Motion of the centre of mass.** Summing Newton's second law over all
   particles, internal third-law pairs cancel: F_ext = M a_cm. Total momentum
   P = M v_cm and dP/dt = F_ext, so with no external force P is conserved.
   *Worked:* 2 kg at 3 m/s and 3 kg at −1 m/s → P = 3 kg m/s, v_cm = 0.6 m/s,
   unchanged by their collision. The law describes the centre only; where a
   force acts decides the turning.
4. **The cross product.** |A × B| = AB sin θ (the parallelogram's area),
   direction by the right-hand rule, perpendicular to both;
   B × A = −A × B. Angular velocity is a vector along the axis, and
   v = ω × r gives every particle's velocity (v = ω r⊥).
5. **Torque and equilibrium.** τ = r × F, |τ| = rF sin θ = F d⊥ (lever arm).
   *Worked:* 20 N at 0.8 m → 16 N m; at 0.2 m → 4 N m; aimed at the hinge → 0.
   A couple has zero net force but torque Fd. Equilibrium needs ΣF = 0 *and*
   Στ = 0 (not necessarily rest). *Worked seesaw:* 100 N × 2 m = 200 N × 1 m;
   the pivot supplies 300 N.
6. **Moment of inertia.** I = Σ m r⊥² (or ∫ r⊥² dm), unit kg m²: the
   distance enters squared. *Worked:* two 1 kg masses at 1 m → 2 kg m², at
   2 m → 8 kg m². Standard results (ring MR², disc and cylinder ½MR², sphere
   ⅖MR², shell ⅔MR², rod ¹⁄₁₂ML² about its middle and ⅓ML² about an end) are
   re-derived numerically in `utils/physics_models.py`. Radius of gyration:
   I = Mk² (ring k = R, disc k = R/√2 ≈ 0.71R). Parallel axis
   I = I_cm + Md² (rod: ¹⁄₁₂ + ¼ = ⅓); perpendicular axis I_z = I_x + I_y
   for laminae, with all three axes intersecting at the same point (disc diameter ¼MR²).
7. **Rotational kinematics.** θ, ω = dθ/dt, α = dω/dt mirror x, v, a; for
   constant α: ω = ω₀ + αt, θ = θ₀ + ω₀t + ½αt², ω² = ω₀² + 2α(θ − θ₀).
   *Worked:* from rest at 2 rad/s² for 4 s → 8 rad/s, 16 rad, ≈ 2.55 rev.
   Each particle: v = rω, a_t = rα, a_r = rω², a = √(a_t² + a_r²).
8. **Rotational dynamics, work, energy.** F_t = m r α → τ = m r² α →
   τ_net = Iα for a rigid body about a fixed axis with constant I. *Worked:* a 4 kg, 0.5 m disc: I = 0.5 kg m², τ = 1 N m →
   α = 2 rad/s². K_rot = ½Iω² (from Σ ½ m v²); W = τΔθ for constant torque, or ∫τ dθ; P = τω.
   *Worked:* after 4 s, K = 16 J = W = 1 N m × 16 rad.
9. **Angular momentum.** L = r × p; |L| = rp sin θ (constant for a free
   particle); on a circle L = mr²ω; for a rigid body about a symmetry axis
   L = Iω (in general only the axial component equals Iω).
   About a fixed inertial origin, τ_ext = dL/dt when internal torques cancel;
   with zero net external torque, total L is conserved. *Worked skater:* I 4 → 2,
   ω 2 → 4 rad/s, L = 8; K 8 → 16 J, the extra 8 J being work done by the arms
   (internal forces change K, not L).
10. **Rolling.** Translation + rotation with v_cm = R|ω| (no slipping): the top
    moves at 2v_cm, the contact point is momentarily at rest, a rim point
    traces a cycloid. K = ½Mv²(1 + I/MR²). Down an incline,
    static friction supplies the torque and does no work at the stationary
    ideal contact point; sufficient grip is required. The acceleration is
    a = g sin β/(1 + I/MR²): cylinder ⅔ g sin β ≈ 3.27 m/s², ring ½ g sin β
    ≈ 2.45 m/s² at 30°; a frictionless sliding block 4.9 m/s².
11. **Synthesis.** x, v, a, F, M, p, ½Mv², FΔx ↔ θ, ω, α, τ, I, L, ½Iω², τΔθ;
    momentum conserved without external force ↔ angular momentum conserved
    without external torque.

## Simplifications, models and metaphors (named)

* **Rigid body, point masses, uniform bodies** — idealisations, said aloud.
* **No air resistance** for the tossed hammer and the firework; **frictionless**
  track, axle and ice; **negligible seesaw weight**; **rolling without slipping**
  (static friction does no work).
* **The skater** is a model: a 1 kg m² body plus two 2 kg point-mass arms,
  chosen to reproduce the brief's I = 4 → 2 kg m².
* **Illustrative motion** (no spoken numbers): the spring cluster, the hammer's
  mass split, the scene-20 spin-up (shown in labelled slow motion).
* **"Radius of gyration is a bookkeeping distance"** — the narration says the
  mass is not really there.
* **Coverage:** the major topics in the supplied outline, essential derivations,
  and selected worked examples. This does not claim every NCERT derivation,
  exercise, or a particular year’s examination syllabus.
* **Energy-share bars** in scene 27 show fractions of each body’s own total K.
  At equal M, R and speed, the cylinder and ring have different total energies.
