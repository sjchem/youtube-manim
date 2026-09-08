# Animation and narration alignment plan

Picture target: **19:34**, 14 chapters. See `config.py` for durations and README for per-scene 480p and 1440p commands. Prose for voice generation lives in `narration_script.md`; directions belong here.

## Story structure

The video asks one evolving question: **What does the machine do?** Numbers reveal its rule; arrows reveal its promise; a table becomes a graph; editing the rule moves that graph; connecting machines creates composition; undoing a machine motivates inverses. A second input coordinate then expands the picture into 3D. The ending fulfils the opening promise by returning to the opening applications.

The first 30 seconds establish the question and the reason to care. The middle earns the notation through examples. The final minute makes the emotional point: **f(x) is a compact description of how one quantity determines another.**

## Opening: local time within scene 01

| Time | Picture | Narration anchor |
|---|---|---|
| 00–04 s | Large MATHEMATICS title, CALCULUS subtitle and four oversized calculus expressions against a stronger cyan/violet nebula. | “The mathematics of calculus…” |
| 04–07 s | Large PHYSICS title and Maxwell equations in three spacious rows; calculus recedes into the nebula. | “…the equations of physics…” |
| 07–10 s | NEURAL NETWORKS and ARTIFICIAL INTELLIGENCE appear last, with pulsing nodes over the earlier mathematics. | “…and the neural networks behind AI…” |
| 10–15 s | The three systems spiral into one point; a glowing 3D gateway emerges and rotates. | “…all build on one idea. The function.” |
| 15–25 s | Flat input/output slots appear. A rough solid enters; internal gears turn; a smooth sphere exits. | “Symbols aside, watch what happens…” |
| 25–30 s | Five applications light up beneath the same machine. | “Calculus, physics, statistics…” |
| 30–36 s | The gateway becomes a neon vending machine. Coin enters, selection A lights, a modelled bottle drops and moves to the output. | “A coin and a selection…” |
| 36–42 s | A mechanical gauge absorbs 10°C; its gears and needle spin; 50°F emerges. | “Ten degrees Celsius…” |
| 42–48 s | A pixel image enters a layered 3D network; pulses travel to an illustrative 98% CAT score. | “An image enters a fixed neural network…” |
| 48–51 s | The gateway returns; its glass panels fold outward and a small x/y table appears. | “Different inputs. Different rules…” |
| 51–57 s | The frame expands into a coordinate grid; its internal core becomes P(x,y), tracing a parabola. | “We will turn it into numbers, a table, and a graph.” |
| 57–60 s | Hold the graph, then clear it for the title. | “Later, we will connect machines…” |
| 60–66 s | Three-line title: WHAT DOES A / FUNCTION / ACTUALLY DO? Input → Rule → Output underneath. | “So, what does a function actually do?” |

The first minute is a visual promise; chapters 02 and 05 teach the table and graph construction at a slower pace. The rough-shape example illustrates a rule that smooths a shape; functions in general need not simplify their inputs. The cat percentage is a sample prediction score, not a measured accuracy or a claim about a real model. The illustrated vending example assumes a working, stocked machine with its state fixed.

Scene 01 uses core Manim procedural 3D geometry. No downloaded models, paid service, or additional plugin is needed. Soft layered strokes suggest glow in Cairo; this is a stylized mathematical render. `python -m utils.opening_review` regenerates eleven cue-frame stills in `output/review/gateway/` without encoding a complete clip. The front-facing camera keeps text readable; object rotations reveal actual depth, and the camera returns to its standard position before scene 02.

These anchors are picture cues. The continuous narration has not yet been synthesized; align its paragraph starts with these cues after generating the cloned voice. Leave a short pause before the last question.

## Chapter handoffs and visual beats

| Scene and start | Visual sequence | Spoken handoff to the next scene |
|---|---|---|
| 01 · 00:00 | Symbol nebula → 3D gateway → action → applications → three machines → unfolding graph → title. | “So, what does a function actually do?” |
| 02 · 01:06 | ×2 machine; 1→2, 3→6, predict 5→10; Input/Output table; name f; identify rule/input/output with compact, shaded annotation arrows; evaluate f(3). | “There is one promise every function must keep.” |
| 03 · 02:41 | Clean aligned rows, 1→2 / 2→4 / 3→6; remove unrelated rows before isolating the 2→4/7 split; then contrast −2 and 2 sharing 4. | “Which inputs are we allowed to use?” |
| 04 · 04:09 | Radius and area change together; separate labelled number-line scales; reject negative physical radius; highlight domain and range. | “Turn that record into a picture.” |
| 05 · 05:31 | Reuse squaring machine; each result enters a table; rows become pairs; pairs fly to plotted points; more samples fill in; continuous rule becomes curve. | “The one-output promise should be visible in the graph itself.” |
| 06 · 07:16 | Vertical scanner on parabola; scanner on radius-two circle; expose (0,2) and (0,−2) in distinct bright colours; finish with one-crossing and two-crossing comparison panels. | “See how editing the rule changes its shape.” |
| 07 · 08:21 | Grey reference parabola; +2 outside; −2 inside with a brighter prediction prompt; bright input/output landmark; output doubling; sign reflection; finish with four compact before/after graph cards. | “What happens when we connect them?” |
| 08 · 10:26 | +2 then square with a shaded glowing 3D pulse; 3→5→25; physically swap boxes and their names; repeat the 3D pulse; 3→9→11; compare graphs; reveal bright role-coloured composition notation above the lowered graph. | “Undoing the first.” |
| 09 · 12:11 | ×2 forward and ÷2 back; inverse notation and reciprocal distinction; (1,2) becomes (2,1); reflect graph across y=x on equal scales. | “What if two different inputs had produced the same output?” |
| 10 · 14:06 | Both signs reach 4; reverse each arrow in place; horizontal line catches both inputs; remove negative domain; reflect surviving curve into √x. | “What would change if one input contained two numbers?” |
| 11 · 15:26 | Front view of the actual y=0 slice; camera tilts; reveal surface; lift one floor point to its output height; illustrative descent path; restore camera. | “Return to the applications we promised at the beginning.” |
| 12 · 17:01 | Same machine relabelled for position, differentiation, event probability and prediction; feedforward layer chain recalls composition; return to the opening applications. | “Functions give us a common language…” |
| 13 · 18:29 | Words become x→f→f(x); graph/composition/inverse memory cards; final word diagram. | “That is a function.” |
| 14 · 19:19 | Short closing card; space for an editor's end-screen elements. | Brief invitation, then finish at 19:34. |

Handoffs use the same visual vocabulary and spoken question across a short fade. These are conceptual continuations, not a claim that every chapter shares a persistent mobject across the cut.

## Pacing and accessibility

- Give viewers time to predict the doubling output before ten appears. Leave a breath before the rightward shift and before the inverse ambiguity is resolved.
- Keep input gold, rule cyan and output green; also identify roles through position, words and arrows. Red marks a conflict, not a different kind of number.
- Use the original graph as a reference during transformations. The vertex explains horizontal shifts; the tracked point explains vertical stretching.
- Do not suggest that five table rows uniquely determine a smooth function. Narration states that the known squaring rule supplies the in-between points.
- In 3D, keep explanatory text fixed to the screen. The white curve is an exact slice of the displayed surface, not an unrelated parabola. Camera movement reveals an additional coordinate instead of decorating a flat explanation.
- The landscape is illustrative. Descent on it does not establish that real neural-network training finds a global minimum.
- Generate voice audio first and compare each paragraph with its visual beat. Word counts are planning estimates. Adjust pauses and holds after listening; do not stretch every spoken line to fill a scene.

## Final editorial viewing pass

Watch the opening through the first concrete example, the complete table-to-graph transition, the right-shift reasoning, both inverse reflections, and the 3D-to-2D return. Check the complete cut once with voice at normal speed. Confirm readability on a small screen and let a beginner explain one input-output example back to you before publication.

## Scene 03: clean presentation revision

Use a plain background, sans-serif headings, large values and thin arrows. Show a single relationship at a time when explaining a conflict. There are no set ovals, giant crosses, moving bubbles or stacked warning captions in this chapter.

| Local time | Picture | Narration anchor |
|---|---|---|
| 00–20 s | Three evenly spaced horizontal input/output rows, then “A function.” | “Watch the doubling rule…” |
| 20–24 s | Remove the first and third rows; centre 2→4. | “Focus on two.” |
| 24–29 s | Move 4 upward and add 7 below it; the isolated input now has two red arrows. | “Now add seven…” |
| 29–36 s | One short verdict below the fork: “Not a function.” | “That is not a function…” |
| 36–45 s | Replace that verdict with the precise one-output promise. | “…we left out an input…” |
| 45–60 s | Squaring example: −2 and 2 independently reach 4. | “Now consider a different rule…” |
| 60–70 s | “Still a function”; keep the two converging paths visible. | “Follow either input separately…” |
| 70–88 s | Clear the diagram, state the promise once, then ask which inputs are allowed. | “That shared answer will matter…” |
