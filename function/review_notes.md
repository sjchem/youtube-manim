# Structure, narration and visual review

The supplied workspace contained scene source and text assets, but no completed video or voice track at the start of the review. The work therefore reviews the complete authored sequence and the newly rendered silent previews. It does not claim a listening review of an existing voiced edit.

## Editorial judgment

The original teaching order was worth keeping. It repeatedly connects the same machine to mappings, tables, graphs, composition and inverses. Reordering those core chapters would add disruption without improving the explanation. The main structural weakness was the late motivation: the introduction spent too long on a title and four examples before saying what functions unlock.

The current opening is a 66-second Universal Translator sequence. Large calculus expressions appear first, larger physics equations follow, and neural networks/AI appear last against a stronger cyan–violet nebula. These systems collapse into a procedural 3D gateway. Moving gears demonstrate an input determining an output; a vending machine, gauge and fixed image model reuse that action. The gateway then unfolds into a table and graph, followed by the title question. The complete picture now targets 19:34. Applications remain early, at 25–29 seconds, and the later chapters develop the opening's visual promises at a slower teaching pace.

The previous 92-second opening and 20-minute silent cut are preserved under `output/archive/gateway_revision/`. The new gateway, props, title and narration supersede that opening.

## Implemented changes

| Finding | Revision and reason |
|---|---|
| Motivation came after the examples. | Show the five application names beneath the gateway at 25–29 seconds; develop them in scene 12. |
| Long title section slowed the opening. | Put a six-second question card after the action; target 19:34 including the final end card. |
| Voiceover contained stage directions and fragmented cues. | Rewrite all 14 scenes as spoken prose and export individual text files. Keep visual directions separately. |
| Scene durations could disagree with the advertised chapter map. | Pad all remaining frames, include a quantized fade, fail on overruns, and verify actual finished durations in the timing audit. |
| Preview and final CLI used the same frame rate; final resolution was not passed. | Explicit 854×480/15 fps and 2560×1440/30 fps profiles; add `all` and `full` targets. |
| Money alone did not determine a vending-machine output. | Show coin plus selection A and drink A, with the working machine state fixed. |
| Introductory table showed unexplained function notation. | Use Input/Output headers before naming the doubling rule. |
| A red cross could appear to negate the true statement `f(x) ≠ f × x`. | Keep the inequality and remove the cross over it. |
| Scene 02 left old machine arrows behind during notation explanation. | Reuse and remove the original arrows instead of reassigning them each iteration. |
| Area marker secretly divided area by 12 on an unlabelled scale. | Give the area line its own numeric scale and plot the actual area value. |
| Negative radius was described as impossible for the algebra. | Explain that the physical domain excludes it even though the expression can be evaluated. |
| Age-to-height did not specify a unique outcome. | Replace it with temperature conversion. |
| Five samples appeared to justify an arbitrary smooth interpolation. | Explain that the known continuous squaring rule determines the intermediate values; keep samples inside the plotted window and add numbered axes with coordinate guides. |
| Live readouts rebuilt LaTeX repeatedly. | Use `DecimalNumber` for changing radius, area and coordinate values. |
| Function names stayed in their old positions as machines swapped. | Move f and g labels with their corresponding machines. |
| Composition inequality could be read as universal. | Explain that order can matter; final notation gives the general definition of composition. |
| Reversing the whole fork displaced the arrows from their endpoints. | Reverse each arrow in place in the inverse-ambiguity scene. |
| Circle plotting and parabola-to-root reflection used unequal coordinate units. | Use matching x/y unit lengths so a circle appears circular and the reflection matrix truly swaps mathematical coordinates. |
| Chapter 11’s opening curve was unrelated to its subsequent landscape. | Draw the actual y=0 slice of that surface and retain it during the reveal. Use a lighter surface mesh for 480p. |
| Late applications used an unspecified probability and an unhelpful prerequisite ladder. | Show a specified event probability, a differentiation operator, and branches from functions to the applications. |
| The 3D camera could affect following overlays; the end card added another background. | Keep captions fixed through the fade, release camera registrations, restore the flat view and reuse one background. |

## Scene 03 presentation revision

Chapter 03 now uses a plain field, sans-serif headings and three aligned input/output rows. It removes the unrelated rows before adding a second answer to input 2, so the conflict has only two arrows and one short verdict. The squaring example then shows −2 and 2 sharing 4 with the same spacing. A final statement replaces the previous stack of boxed rules and large symbols. Narration and the alignment plan follow this more focused sequence; the chapter remains 88 seconds. Review frames are saved in `output/review/scene03_clean/`.

## Narration decisions

Scene 06 now colours the fixed input `x = 0` gold and the two outputs `y = 2` and `y = −2` green and violet, matching the two intersection markers on the circle. Its former title-only ending is replaced by compact one-crossing and two-crossing diagrams plus the operational rule, “A function passes every vertical line.”

Scene 07 now gives the “left?” prediction a bright gold treatment and colours the `1 → 1` landmark by role: gold input, white arrow and green output. Its title-only ending is replaced by four small reference graphs for upward shift, rightward shift, stretch and reflection.

Scene 08 replaces both flat pipeline pulses with the same procedural shaded sphere, including a surface highlight and two glow layers. The final composition identity uses bright cyan, white and green roles; the graph sits lower so its `y` label does not touch the equation panel.

The script says “each allowed input” and distinguishes range from possible codomain values in the mathematical notes. It explains inverse versus reciprocal, square root versus solving a quadratic, one input pair versus two separate outputs, and an uncertain event versus the probability assigned by a model. It avoids claiming that a function must have a formula, be continuous, or predict accurately. Gradient descent is an illustrative optimisation example, with no claim of guaranteed global convergence.

A viewer who is new to algebra gets numbers and a concrete action first. A more experienced viewer gets the graph, transformation and composition connections. The 3D section extends an established idea without requiring students to learn optimisation mathematics.

## Validation scope

Timing and endpoint layout audits complement visual inspection; neither establishes speech synchronization. Actual cloned-voice audio was not supplied. The README gives the audio placement and duration-check workflow. A final listen-through with that audio remains part of producing the voiced master.


### Checks completed

- Python compilation passed.
- All 14 chapters passed timing checks at 15 and 30 fps. The completed scene lifecycle, including its final hold and fade, was measured.
- A combined `FullVideo` simulation measured exactly 1,174 seconds, found no foreground objects left at chapter boundaries, and confirmed that the 3D camera and fixed overlays were reset.
- The teaching chapters passed endpoint text-layout checks. The new 3D opening also receives a separate cue-frame review because the text audit does not measure depth or camera projection.
- Fourteen plain-text narration exports match the source script: continuous spoken prose per chapter. Actual voice audio was not supplied.
- A short final-resolution render was probed at 2560×1440, 30 fps. This was a format check, not a completed 1440p master.
- The opening has eleven cue-frame stills in `output/review/gateway/`, including the gateway, all three examples, the unfolding table, graph and title. Rendered frames were also inspected for notation, mappings, scales, coordinate plotting, scanners, transformations, composition, inverses and surface reveal. The surface slice is explicitly drawn above the faces so it remains visible.

The per-scene preview files live under `media/videos/<scene>/480p15/`. The assembled silent review cut is `output/function_480p_review.mp4`; the browser gallery is `output/preview_index.html`. The assembly step normalizes small encoder rounding differences so the joined file follows the chapter map. A voiced master still requires generating and aligning the cloned voice as described in README.

## Gateway construction notes

All opening assets are authored in `manim_scenes/gateway_models.py` using core Manim: prisms, extruded shapes, a surface of revolution for the bottle, cylinders, spheres and planar gear outlines. Layered translucent strokes suggest neon glow; no external 3D models or plugin subscription is required. The temperature conversion is 10 × 9/5 + 32 = 50. The network's 98% label is an illustrative prediction score, not measured classifier accuracy. The opening parabola is a preview of the later squaring example.

The procedural geometry follows the [Manim 3D API](https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.html); the initial formula field uses the [SI differential forms of Maxwell's equations](https://sites.science.oregonstate.edu/physics/coursewikis/GSR/book/gsr/maxwell.html).
