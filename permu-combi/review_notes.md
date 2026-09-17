# Review and revision notes

The original twelve-scene structure had a strong teaching sequence: a concrete
mystery, a reusable counting method, a change in what counts as an outcome,
and a large application. The main weaknesses were narration continuity,
pacing within scenes, and a few mathematical qualifications. The revision
keeps the Oceanic theme and existing 3D scenes. A later curriculum expansion
added two chapters; tightening the interactive quiz brought the final runtime
to 26:45.

## What changed

- **A connected story.** The race participants become the science-team
  candidates. Each spoken ending introduces the next question. The finale
  returns to the opening lock beside a team and performs the same swap in both.
- **Continuous narration.** All fourteen scenes now have one spoken passage.
  The exported text files contain no headings,
  timestamps or production directions. Estimated scene rates are 117–145 words
  per minute before allowing for pauses; the quiz needs silent countdowns.
- **Honest timing.** The old combinations narration included lines marked
  13:16 and 13:27 although the chapter ended at 13:07. Some other late lines
  also left implausibly little speaking time. The revised master uses chapter
  ranges, with a separate visual cue table for recording and editing. Export
  validation rejects incorrect ranges, duplicate chapters and inline timecodes.
- **Motion that follows the explanation.** Books are selected at 19, 31, 43
  and 55 seconds; medal choices begin at 27, 42 and 57 seconds. These steps
  previously completed much earlier, followed by long holds. The recap's
  three columns now arrive separately; larger fractions improve readability.
- **Repetition is explicit.** A PIN is an ordered code, but the no-repeat
  permutation formula does not generally count PINs. A repeated digit now
  appears visually, with `10^4 = 10,000` under the stated all-digits-allowed
  assumption, including leading zero. The final recap states the scope of the
  factorial formulas.
- **Other mathematical corrections.** Twelve factorial is 479,001,600,
  *nearly* half a billion; its on-screen caption previously said it exceeded
  half a billion. The growth bar now identifies its compressed logarithmic
  scale. The multiplication principle requires equal branch counts, not
  statistical independence. Zero factorial is described as a consistent
  definition with an empty-arrangement interpretation.
- **Class 10–11 extension.** The choices chapter now contrasts the addition and
  multiplication principles. New scenes derive block and gap methods, the
  repeated-object formula through LEVEL, and polygon diagonals through vertex
  combinations. The full film now has fourteen chapters, with the recognition
  quiz reduced to three compact comparisons.

The permutation convention is consistent with
[OpenStax's treatment of ordered lists without repeated objects](https://openstax.org/books/contemporary-mathematics/pages/7-2-permutations).
The project remains in Manim Community Edition, which matches its existing
scene code and the local Oceanic theme.

## Review scope

This is a source, narration and generated-preview review. There was no finished
movie or recorded narration in the project to watch. Storyboards were inspected
for the factorial, combinations, quiz and finale scenes. Automated layout
checks inspect text bounds at animation endpoints; they cannot prove that
intermediate motion or 3D projections are free of occlusion. Actual voice
recordings must still be aligned to the cue windows. The README explains that
placing audio files in the asset directory does not automatically mix them
into the current render.

No full 2K render was made. Preview individual chapters with the sequential
commands in `README.md`; Scene 14 is the final subscribe card.

## Validation

- Python compilation, scene listing, exact arithmetic and counting-model checks passed.
- All fourteen scene budgets are covered by the timing audit; revised scenes
  are also checked at the final 30 fps rate.
- All fourteen scenes are covered by the automated endpoint text-layout audit; final
  layout changes were checked again and inspected as rendered stills.
- Narration exports match the master, chapter ranges match the animation
  budgets, and checks rejected deliberately malformed ranges and timecodes.
- The all-digits-allowed PIN total was independently checked by enumerating
  all four-digit sequences.

The storyboard previews demonstrate the revised visuals. There is no recorded
voice track, so speech synchronization remains an editing step rather than a
verified result.
