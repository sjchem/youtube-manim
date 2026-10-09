# Animation plan — Why Does Pascal's Triangle Know Algebra?

13 chapters, 21:23. Every chapter is a `play_scene(scene)` function timed to the
beats in `narration.py`; the full film plays them in order. Colour is meaning:
**a = blue, b = rose, coefficients = gold, confirmed = green, brute force =
orange, general/limit = purple, guides = muted.**

| # | Start | Length | Chapter | Core visual |
|---|------|------|---------|-------------|
| 01 | 00:00 | 64 s | Title card and the mystery | Bright "Binomial Theorem" title with "Pascal's Triangle & Combinations" and $(a+b)^5$; the card holds until 00:03.4, then its expression moves into the mystery. Six gold "?" coefficients; brute force doubles 2→4→8→16→32 raw products (orange counter), which collapse onto 1, 5, 10, 10, 5, 1; a triangle built by addition shows the same row; five choice machines flicker as the teaser. |
| 02 | 01:04 | 96 s | Start small | $(a+b)^0$, $(a+b)^1$; a square of side $a+b$ splits into $a^2$, two $ab$ rectangles and $b^2$; one rectangle rotates onto the other, both slide together into $2ab$; the algebra shows the four products $aa, ab, ba, bb$ as choice lists, and $ab$/$ba$ merge — "a coefficient counts the ways". |
| 03 | 02:40 | 102 s | The cube (3D) | A cube of edge $a+b$ is cut on three planes into eight lit blocks, exploded, named ($a^3$, slabs $a^2b$, beams $ab^2$, $b^3$), sorted into 1·3·3·1 on a front-facing shelf; three direction machines (x, y, z) show "three slabs = three ways to choose which direction gets the b"; $2\times2\times2 = 8$. |
| 04 | 04:22 | 115 s | The triangle builds itself | Expansions for $n = 0..5$ stack with aligned equals signs; the letters fade and the coefficients settle into Pascal's triangle (terms with an unwritten 1 morph into "1"); addition-rule arrows; then $(a+b)^5 = (a+b)^4(a+b)$: the "×a" copy stays, the "×b" copy slides one column, columns add to row 5. |
| 05 | 06:17 | 128 s | Five choice machines | Brackets morph into machines with an a-door and a b-door; $aabab$ drops out as a choice list and multiplies to $a^3b^2$; $2^5 = 32$; all 32 lists, then sorted by number of b's into a histogram of piles 1, 5, 10, 10, 5, 1; pile sizes become coefficients; $1+5+10+10+5+1 = 32 = 2^5$. |
| 06 | 08:25 | 131 s | Combinations | Two b's fix a list ("the rest is forced"); machines with index tags light every pair, building a 4+3+2+1 staircase of ten lists; ten copies collapse into a boxed $10a^3b^2$; $5\times4$ ordered picks, "2→4" and "4→2" give the same list, $20/2 = 10 = \binom52$; general $n$ machines; $\binom nk = n!/(k!(n-k)!)$ in purple; all six $\binom5k$ evaluate to the row. |
| 07 | 10:36 | 99 s | The binomial theorem | The formula arrives with a glow; each symbol is braced in turn ("k brackets say b", "the rest say a", "ways to pick which ones", "collect every k") while five machines act it out; "choose · count · collect"; test at $n=5$ column by column; the middle term of $(a+b)^{10}$ is $252a^5b^5$. |
| 08 | 12:15 | 101 s | Opposite exponents | Exponent rows (blue 5→0, rose 0→5) under the expansion; a five-cell list flips one a to b at a time while a gold frame steps along the expansion; $(5-k)+k = 5$; the coefficient row reverses by swapping mirror partners; "2 say b / 3 say a"; $\binom52 = \binom53$, then $\binom nk = \binom n{n-k}$; $(1+1)^5 = 32$. |
| 09 | 13:56 | 111 s | Why Pascal's rule works | The ten lists; the last cell of each glows; they split into "last says b" (4 = $\binom41$) and "last says a" (6 = $\binom42$); 4 + 6 = 10; general in/out branch on the newest item; $\binom nk = \binom{n-1}{k-1}+\binom{n-1}k$; tied to chapter 4's ×a / ×b copies with a machine. |
| 10 | 15:47 | 110 s | Paths | The triangle becomes a maze of nodes; left step a (blue), right step b (rose); a glowing ball walks $abaab$ while its list builds; ten routes into the 10 are drawn one by one with a live tally; every node fills with its route count; the 4 via the upper-left and 6 via the upper-right; "Pascal's triangle ↔ combinations ↔ binomial coefficients". |
| 11 | 17:37 | 116 s | Coin flips (3D) | A coin flips; heads left, tails right; a Galton board drops 64 seeded balls (1, 10, 19, 22, 11, 1); $(H+T)^5$, the 32 sequences, the ten with two tails, $P = 10/32 \approx 0.31$; row 5 lifts out of the triangle as lit 3D columns; sample vs exact bars (64, then 1,024 scaled); rows for 10 and 20 flips approach a purple bell curve. |
| 12 | 19:33 | 100 s | The final payoff | Five machines count $\binom5k$ for each k, powers attach, the expansion assembles in a green frame; the chain expand → choose → count → stack, rooted in "one counting structure"; $(10+1)^4 = 11^4 = 14641$ spells row 4, and row 5's tens carry; the theorem with "ways to choose" as the closing frame. |
| 13 | 21:13 | 10 s | Subscribe | The channel card (THANK YOU FOR WATCHING / SUBSCRIBE / Stay curious.) over a halo, with row 5 in gold beneath. |

## Recurring objects (all in `manim_scenes/common.py`)

- `ChoiceMachine` / `machine_row` — a bracket as a two-door machine; `machine.animate.choose("b")`.
- `choice_list` — a row of letter cells (outlined blue a, filled rose b; equally sized glyphs; H/T for coins).
- `expansion_tex`, `term_tex`, `colored_tex` — coloured LaTeX whose terms and coefficients are addressable.
- `pascal_triangle`, `pascal_point`, `path_line`, `bounce_path` — the triangle, routes and bounces.
- `coin`, `bar_set`, `block` — coins, histogram bars and lit 3D boxes.
- `heading`, `caption`, `chip`, `glow_frame`, `halo` — type and emphasis, sized for phones.

Keep captions to a short phrase; narration carries the explanation. Supporting
equations and door labels retain 80% opacity during emphasis, with bright blue,
rose and secondary text. The probability comparison labels gold as expected
counts, and the closing $11^5$ shot shows carrying with an arrow.

## 3D chapters

03 (the cube) and 11 (the lifted histogram) use `ThreeDScene` cameras. Captions
are pinned with `hud()`, and text in those chapters is faded in rather than
morphed from 3D objects (a morph into fixed-in-frame text leaves world-space
copies behind). Every chapter resets the camera on exit, so the full film can
mix flat and 3D chapters freely.
