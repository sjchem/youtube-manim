# YouTube Package

Everything needed to publish the finished render.

## Title options

1. **Permutations & Combinations Explained Visually**
2. Why a "Combination Lock" Is Named Wrong
3. Permutations vs Combinations — One Question Settles It

Primary recommendation: option 1 for search, with option 2 as the thumbnail
hook line.

## Description

```
A combination lock hides a mathematical question. If the code is 1-2-3, then 3-2-1 will not open
it — same digits, different order, different result. That single observation is
the key distinction between ordered arrangements and unordered groups, and this video
builds both formulas from it, one visual step at a time.

No formula appears before the picture that earns it. We start with addition and
multiplication principles, watch a pool of books shrink into a factorial, build
block and gap methods for restrictions, derive nPr and nCr, divide away swaps
of alike letters, and count diagonals by choosing pairs of vertices.

Chapters
00:00  The combination lock that isn't
01:32  Add alternatives, multiply stages
04:29  Factorials: when every step costs a choice
06:49  Permutations: five runners, three medals
09:29  Why order matters here
10:57  Restricted arrangements: blocks and gaps
13:57  Combinations: dividing the order away
17:12  Quiz: permutation or combination?
18:42  Alike objects and geometrical counting
21:42  Choosing is also leaving behind
23:10  2,598,960 poker hands
24:32  Why 0! = 1
25:18  One question, two answers
26:30  Thanks for watching

The one sentence worth keeping: a combination is a permutation with the
unnecessary order divided away. We also check when repetition is allowed:
four-digit codes with all ten digits available in every slot have 10,000 possibilities.

Every main count is checked in code — including 12 block arrangements, 72 gap
arrangements, 30 arrangements of LEVEL, 9 hexagon diagonals, and 2,598,960
five-card poker hands.

Animated with Manim Community Edition. Source, narration script and the
verification scripts are linked below.
```

## Tags

```
permutations, combinations, nPr, nCr, factorial, combinatorics, counting
principle, multiplication principle, addition principle, block method, gap method,
identical objects, polygon diagonals, geometrical counting, discrete mathematics,
math animation, manim, 3blue1brown style, permutation vs combination, 0
factorial, binomial coefficient, pascal triangle, poker hands, math intuition,
visual mathematics
```

## Thumbnail

Left half: the 3D padlock showing **1 2 3** with a green tick.
Right half: the same lock showing **3 2 1** with a red cross.
Overlaid text, two lines, very large: **SAME DIGITS** / **DIFFERENT RESULT**.
Palette: Oceanic Next — `#041A2F` background, `#FFD166` for the digits,
`#78D98B` and `#FF6B6B` for the verdicts.

Pull the source frame straight from the film:

```
python -m utils.storyboard scene_01 --at 22 --width 1920
```

## Pinned comment

```
The decision rule, in one line: swap two of the things you chose. If the
outcome changed, it's a permutation. If it didn't, it's a combination.

Check repetition too: a code may reuse digits, so its pool need not shrink.

Deliberately left for another video: combinations with repetition, circular
arrangements, derangements, distributions, divisors, and the binomial theorem.
```

## End-screen

* Next: *the binomial theorem*, connected to Pascal's row near 23:30.
* Earlier in this film: the factorial growth near 06:20, for anyone who wants the scale.

## Publication checklist

- [ ] `python -m utils.math_utils` and `python -m utils.counting_models` pass
- [ ] `python -m utils.timing_audit` — every chapter OK
- [ ] `python -m utils.layout_audit` — zero issues
- [ ] `python -m utils.narration_export --check` — valid ranges and current plain-text exports
- [ ] Narration recorded, no chapter "TOO LONG", and phrases checked against visual cues
- [ ] Narration added in the editor or muxed at chapter starts (not loaded automatically)
- [ ] `python main.py render` at 2560 × 1440, 30 FPS
- [ ] Watched once at phone size, checking every equation is legible
- [ ] Chapter timestamps pasted into the description
