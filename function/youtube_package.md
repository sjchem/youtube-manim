# YouTube package

## Title options

1. **What Does a Function Actually Do?** *(primary)*
2. Functions, Explained Visually — Input, Rule, Output
3. f(x) Is Not Multiplication — What a Function Really Means

## Description

```
A number goes in. A rule acts on it. Another number comes out.

That is the entire idea behind functions — and it is the floor that calculus,
physics, statistics and machine learning are all built on. This video builds
that idea visually, from a vending machine to a neural network, building the meaning before teaching the notation.

We go from a machine, to numbers flowing through it, to a table, to ordered
pairs, to a graph, to transformations, to machines wired in series, to running
one backwards — each step motivated by the picture before it.

Chapters
00:00  The universal translator
01:06  Input, rule, output
02:41  Why one input gives one output
04:09  Domain and range
05:31  How a function becomes a graph
07:16  The vertical line test
08:21  Change the rule, change the shape
10:26  Machines in a pipeline (composition)
12:11  Running the machine backward (inverses)
14:06  When there is no way back
15:26  Two inputs, one output
17:01  Why functions matter
18:29  Input, rule, output
19:19  Thanks for watching

A note on the two metaphors used: the "machine" is a picture of the assignment
x ↦ f(x), not a physical claim. And the landscape in the 3D chapter is an
invented surface — but the behaviour it shows, gradient descent on a real
function of a model's parameters, is an illustration of one common optimisation method; real training need not find the global minimum.

Made with Manim Community Edition.
Source: https://github.com/sjchem/youtube-manim

#mathematics #functions #calculus #manim #3blue1brown #machinelearning
```

## Tags

`functions`, `what is a function`, `function notation`, `f(x)`, `domain and range`,
`vertical line test`, `function transformations`, `composition of functions`,
`inverse functions`, `square root`, `graphs`, `calculus`, `precalculus`,
`machine learning intuition`, `gradient descent`, `manim`, `math animation`,
`visual mathematics`

## Thumbnail

- Deep Oceanic background `#041A2F`.
- Centre: the glowing cyan machine box, a **gold** `x` entering from the left and
  a **green** `f(x)` leaving on the right — a recreation of the final scene’s symbol diagram.
- Overlay, upper left, two lines of heavy white type:
  `f(x)` / `IS NOT ×`
- Lower right corner: a small parabola in cyan, so the maths is legible at
  thumbnail size without any extra words.
- Keep all type inside the central 80% — the chapter list crops the right edge on
  mobile.

Grab the source frame with:

```bash
ffmpeg -ss 12 -i media/videos/scene_13_finale/480p15/Scene13Finale.mp4 -frames:v 1 output/thumbnail-source.png
```

## Pinned comment

```
The one line worth taking away: f(x) is not f times x. It is a name for what
the rule f gives back when you hand it x. Everything in the video — graphs,
composition, inverses — is a consequence of that single sentence.

What should the next one be: derivatives, or vectors?
```

## Shorts / clip candidates

| Clip | Source | Why it stands alone |
|---|---|---|
| 05:31 – 07:16 | chapter 05 | table → pairs → dots → parabola |
| 08:21 – 10:26 | chapter 07 | output shifts, input shifts, stretch and reflection |
| 12:11 – 14:06 | chapter 09 | coordinate swap motivates inverse reflection |
| 14:06 – 15:26 | chapter 10 | why squaring needs a restricted domain to be inverted |

## End screen

- Suggested next: *Visual Calculus — From Limits to Derivatives* (`calculus-1/`),
  which opens exactly where this one closes.
- Subscribe element bottom-right, over the card from chapter 14.
