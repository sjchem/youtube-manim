# Verification of the expanded explanation

Target: senior secondary / introductory university chemistry.

The user's current nineteen-chapter structure is preserved: 35:20 and 4,839 spoken words.
Narration is edited in narration_script.md; all nineteen chapter exports and the full export match.

## Implemented

- Chapter 3 distinguishes the school shell-capacity rule from Bohr's one-electron model.
- Chapter 5 shows amplitudes at both openings and individual detections without an invented trajectory.
  A fresh path-detector run removes interference while retaining the same diffraction envelope.
- Chapter 7 shows separate position and tangent momentum vectors, with momentum units.
- Chapter 9 limits the cat analogy to statistical sampling.
- Chapter 11 links a density slice, radial curve, spherical boundary and live enclosed probability.
  It also connects radial/angular node counts to the displayed 2s and 2p examples.
- Chapter 12 connects angular families to L², magnetic states to Lz and spin to Sz.
- Chapters 13 and 17 distinguish penetration from zero inner probability, and filling guides from fixed energies.
- Narration, science notes, beat plan, architecture and README are synchronized.
  All nineteen 480p commands and all nineteen 2K commands still occupy their respective copy blocks.
  Stale chapter imports in the preview utilities are corrected.

## Validation

- Scientific invariants pass, including independent integration of the displayed 1s wave function
  and reconstruction of coherent/incoherent slit intensities from complex amplitudes.
- All narration windows and speaking rates pass; exports match.
- Updated standalone chapters pass timing, endpoint text bounds, text collisions and cleanup checks.
- Chapters 08–19 also pass continuously in one fresh scene, including the orbital-to-filling transitions.
- Source compilation and documented preview imports pass.
- Final 480p/15fps motion previews were rendered and selected frames inspected:
  double-slit chapter, approximately 90.0 s; radial worked example, approximately 28.3 s.

The complete 01–19 audit was attempted twice. One process terminated with exit 143;
the diagnostic retry completed through chapter 08 and then exited 139.
The fresh 08–19 continuation passes, but this is not a successful single-process full-film audit.
No complete 2K film or newly recorded narration audio was rendered.

## Review artifacts

- [Double-slit motion](../../output/depth_motion/videos/scene_05_one_at_a_time/480p15/Scene05OneAtATime.mp4)
- [Radial probability motion](../../output/depth_motion/videos/depth_preview/480p15/RadialProbabilityReview.mp4)
- [Double-slit frame](../../output/depth_motion/double_slit_frame.png)
- [Radial probability frame](../../output/depth_motion/radial_probability_frame.png)
- [Final revised chapter audit](../../output/depth_audit_final/audit.json)
- [Final slit/radial pacing audit](../../output/depth_last_layout/audit.json)
- [Continuous chapters 08–19 audit](../../output/depth_tail_continuity/audit.json)
