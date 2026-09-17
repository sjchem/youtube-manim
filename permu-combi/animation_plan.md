# Animation Plan

Fourteen chapters, 26:45 total. Each chapter is an independent module exposing
`play_scene(scene)`, so it can be previewed alone or chained by `full_video.py`.

## The visual grammar

The film teaches one language in chapter 01 and never breaks it afterwards. A
viewer who learns the pictures can read the mathematics off the screen.

| Picture | Meaning | Helper |
|---|---|---|
| Glowing disc with a name | one object | `common.chip` |
| Cyan disc | still available to be chosen | `cfg.AVAILABLE` |
| Gold disc | chosen, or in flight | `cfg.CHOSEN` |
| Dimmed grey disc | used up, no longer available | `common.dim_chip` |
| Empty rounded square | a position you can fill | `common.slot` |
| Numbered, orange slots | order matters → permutation | `common.slot_row(ranks=...)` |
| One green ring around everything | order does not matter → combination | `common.team_ring` |
| Product built left to right | the count, revealed as the animation earns it | `common.ProductChain` |
| Purple | scale, abstraction, huge numbers | `cfg.ABSTRACT` |
| Red | overcounting, a locked lock, a contradiction | `cfg.WRONG` |

Worked products build progressively. `ProductChain.reveal(scene, i)` exposes
one factor at a time beside the choice that justified it. General formulas and
recap equations appear only after the corresponding visual argument.

## Chapter breakdown

| # | Module | Secs | Start | 3D | What happens |
|---|---|---|---|---|---|
| 01 | `scene_01_lock_paradox` | 92 | 00:00 | ✅ | A real 3D padlock. 1-2-3 opens it; 3-2-1 does not. Digits become letters; ranked slots vs. one ring. Title. |
| 02 | `scene_02_choices_multiply` | 177 | 01:32 | — | Outfit tree and a third stage derive multiplication; mutually exclusive bus/train routes introduce the addition principle: OR adds, AND multiplies. |
| 03 | `scene_03_factorial` | 140 | 04:29 | — | Four books, four ranked slots. The pool visibly shrinks 4→3→2→1 as the product builds. `4! = 24`, then `n!`, then a log-scaled growth bar to `12!`. |
| 04 | `scene_04_permutations` | 160 | 06:49 | ✅ | Five runners, a 3D podium. Gold/silver/bronze filled in turn; `5×4×3 = 60`; the `2×1` tail greyed out and divided away; `nPr` derived. |
| 05 | `scene_05_order_matters` | 88 | 09:29 | — | One swap on the podium demoted one person and promoted another. `ABC ≠ BAC`. All six podiums cycled through the same three slots. |
| 06 | `scene_06_block_gap` | 180 | 10:57 | — | MATH with A and T together becomes three objects plus an internal swap. Three boys create four safe gaps for two distinct girls. Results: 12 and 72. |
| 07 | `scene_07_combinations` | 195 | 13:57 | — | The same count applied to a team gives 60. Six orderings of `ABC` collapse into one ring. `3! = 6` overcount, `60/6 = 10`, all ten teams shown, `nCr` derived. |
| 08 | `scene_08_quiz` | 90 | 17:12 | — | Three compact situations: PIN, pizza, then the same two people with roles versus inside one team. Smaller typography and short timers lead into the swap test. Repeated PIN digits show why reuse gives `10^4`. |
| 09 | `scene_09_alike_geometry` | 180 | 18:42 | — | Invisible L/E swaps turn `5!` into `5!/(2!2!)=30`. A hexagon's vertex pairs become 15 segments; removing six sides leaves nine diagonals; three vertices suggest triangles. |
| 10 | `scene_10_symmetry` | 88 | 21:42 | — | Ten dots; three chosen, seven dimmed; the highlight inverts. `C(10,3) = C(10,7)`. Closes on the symmetric histogram of row 10 with its mirror line. |
| 11 | `scene_11_poker` | 82 | 23:10 | ✅ | Five cards dealt, rearranged, unchanged. `52C5` with factorial cancellation → 2,598,960, then a drifting 3D cloud of ~190 tiny hands. |
| 12 | `scene_12_zero_factorial` | 46 | 24:32 | — | Choosing everybody motivates the consistent definition `0! = 1`; the empty arrangement gives it a counting meaning. |
| 13 | `scene_13_finale` | 72 | 25:18 | — | Three formulas revealed at 0, 7 and 14 seconds. The decision rule and its no-repeat scope, then the opening lock beside a team: the same swap changes only the code. |
| 14 | `scene_14_subscribe` | 15 | 26:30 | — | Final closing and subscribe card. |

## How the 3D chapters behave

Manim's `ThreeDCamera` depth-sorts only mobjects with `shade_in_3d`; every flat
`VMobject` is drawn last, on top. Two consequences shape the props:

* Nothing flat and filled may sit between the camera and a 3D part it is meant
  to reveal — hence the padlock has no painted recess behind its wheels.
* Text is therefore always legible over 3D geometry, which is why the podium
  and poker chapters pin their captions with `add_fixed_in_frame_mobjects`.

A `theta` rotation spins flat text in-plane, so chapters 04 and 11 hold
`theta = -90°` and create depth with `phi` alone. Chapter 01 does rotate
`theta`, but only while every word on screen is fixed in the frame.

Each 3D chapter restores `phi = 0`, `theta = -90°`, zoom, background colour and
its fixed-in-frame registrations before returning, so `full_video.py` can chain
chapters in any order.

## Pacing contract

`common.begin_scene` stamps the start time; `common.cue(scene, started, t)`
holds until second *t* of the chapter and **raises** if the animation has already
run past it; `common.end_scene` pads to the exact target and raises on overrun.
A chapter therefore cannot silently exceed its animation budget. This verifies
scene boundaries, not word-level alignment with a recording.

Verify without rendering a single frame:

```
python -m utils.timing_audit     # every chapter lands on its target second
python -m utils.layout_audit     # no text leaves the frame, no text overlaps
python -m utils.storyboard 6     # still frames of each distinct composition
```

## Continuous narration and recording cues

`narration_script.md` is the spoken master: one connected passage per scene,
with an explicit bridge into the next idea. The exported `scene_XX.txt` files
contain only speech. Record naturally; the windows below indicate where the
corresponding ideas appear. All times in this table are **seconds from the
start of that scene**, not timestamps to read aloud. They are editing guides,
not measured word timings. Pause naturally or retime the animation after
listening to the actual take. Leave each quiz countdown silent.

| Scene | Visual / narration windows |
|---|---|
| 01 | 0–24 introduce and open the lock; 24–38 reverse the code; 38–52 explain ordered codes; 52–65 letter positions; 65–78 team; 78–92 question and wardrobe bridge. |
| 02 | 0–18 wardrobe; 18–50 branches; 50–80 multiplication; 80–112 shoes; 112–145 bus/train alternatives; 145–168 `3+2=5`; 168–177 OR/add versus AND/multiply. |
| 03 | 0–19 books and slots; choices begin at 19, 31, 43, 55; 66–80 product and 24; 80–92 factorial notation; 92–110 general pattern; 110–140 growth and partial-position question. |
| 04 | 0–27 runners and podium; gold, silver and bronze begin at 27, 42, 57; 66–78 total; 78–98 unwanted factorial tail; 98–116 divide by `2!`; 116–140 notation; 140–160 check and swap bridge. |
| 05 | 0–12 read the podium; 12–24 swap; 24–44 changed awards; 44–69 six outcomes; 69–88 who plus where, then remove the roles. |
| 06 | 0–25 form the AT block; 25–53 outside and internal arrangements; 53–78 result; 78–108 arrange boys and reveal four gaps; 108–141 choose gaps and arrange girls; 141–180 result and method summary. |
| 07 | 0–18 same people, new task; 18–44 ordered count; 44–68 six lists; 68–88 collapse into a team; 88–106 equal overcount; 106–116 divide; 116–137 ten teams; 137–166 formulas; 166–195 meaning of the divisors and quiz bridge. |
| 08 | 0–5 invitation; 5–17 compare PINs; 17–28 repeated digit and `10^4`; 28–48 toppings; 48–61 two named roles; 61–76 the same people as one team; 76–90 outcome test and repetition reminder. The countdown is shown before each decision. |
| 09 | 0–34 naive `5!` and identical L swap; 34–68 E swap and division; 68–96 general formula; 96–130 all hexagon segments; 130–157 remove sides; 157–180 diagonals and triangle selection. |
| 10 | 0–26 choose three; 26–40 seven determined; 40–58 invert and compare; 58–66 general identity; 66–88 symmetric row and cards bridge. |
| 11 | 0–20 deck and deal; 20–34 rearrange; 34–42 combination; 42–52 cancellation; 52–60 answer; 60–82 illustrative cloud and empty-case bridge. |
| 12 | 0–14 one way to choose all; 14–20 factorial formula; 20–30 consistent boundary definition; 30–46 empty arrangement and recap bridge. |
| 13 | 0–22 three pictures and formulas; 22–28 connect them; 28–38 order test; 38–46 distinct/no-repeat scope; 46–55 lock/team callback; 55–72 final question and payoff. |
| 14 | 0–15 thank the viewer and close on the subscribe card. |

The storyboard aims for a small number of meaningful visual changes, with
room to understand each one. In particular, the four book choices and three
medal choices now occupy separate explanation windows instead of finishing
early and leaving one completed picture on screen for most of the explanation.
