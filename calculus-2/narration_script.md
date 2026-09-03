# Continuous Narration — Visual Calculus: From Derivatives to Integrals (Part 2)

Target delivery: curious, cinematic, and unhurried, generally between 95 and 105 words per minute. Concept-heavy reveals may slow slightly so students can read the equations. Generate one voice file from each chapter block and fit it to the listed chapter window without adding silence. Do not synthesize the Markdown headings. Every block hands the thought directly to the next chapter — do not add an artificial ending pause to clips 01–13.

## Scene 01 — Velocity Becomes Distance — 0:00–1:29 — Voice Clip 01

A car pulls away, and a simple question follows it down the road: how far did it go?

If the car holds a constant twenty metres per second for five seconds, the answer is easy: twenty times five, one hundred metres. Look at that on a velocity-time graph, and something clicks — that one hundred is exactly the area of the rectangle sitting under the velocity line.

Distance is the area under a velocity graph. Simple, while the speed stays flat.

But now let the speed wander — rising, dipping, rising again, never resting on one value. The flat rectangle is gone; a curve sits in its place. So here is the real question this episode has to answer: if the speed changes at every single instant, what is the distance now? This is Visual Calculus, Part Two — From Derivatives to Integrals.

## Scene 02 — Rectangles Become the Integral — 1:29–2:53 — Voice Clip 02

Start crude. Cut the time axis into just four strips, and stack a rectangle on each one, using the velocity at its left edge. Add the four little areas together, and you get a rough estimate of distance — visibly rough, because each rectangle either overshoots or undershoots the true curve beneath it.

So use more rectangles. Ten. Fifty. Two hundred. Watch each one thin, watch the gaps between rectangle and curve disappear, watch the jagged staircase smooth itself into the curve it was always approximating.

That limit — infinitely many, infinitely thin rectangles — is what we now name with new notation: the integral of f of x, dx, from a to b. Not a mysterious symbol. Just a sum, taken to its limit: the integral is the sum of infinitely many tiny pieces.

## Scene 03 — What dx Really Means — 2:53–3:49 — Voice Clip 03

That dx in the integral is not decoration. Pull out one rectangle, and look at it closely. Its width is dx. Its height is f of x. Multiply them, and its sliver of area is dA equals f of x, dx.

Now picture thousands of these slivers, standing shoulder to shoulder, filling the entire region beneath the curve. The integral is nothing more than an instruction: add up every one of those f of x, dx slivers, from a all the way to b. Once you see the strip, the notation stops being abstract — it becomes a picture you can see.

## Scene 04 — The Fundamental Theorem, Revealed — 3:49–5:41 — Voice Clip 04

Here is the idea the entire subject turns on. Define a running total: A of x, the area collected under f, from some fixed start out to a moving point x. As x slides right, the shaded region grows, and a matching point traces a second curve underneath — the accumulation function itself.

Watch their connection in real time. Where f is lower, A climbs gently. Where f is taller, A steepens. The lower curve is recording the area above it, moment by moment.

Now nudge x forward by one tiny dx. The sliver of area just added is almost exactly a thin rectangle: dA is approximately f of x, dx. Divide both sides by dx, and something remarkable falls out: dA over dx is approximately f of x. Let dx shrink to nothing, and the approximation becomes exact: A prime of x equals f of x.

That shrinking orange strip is the bridge between a local height and a growing total.

That is the Fundamental Theorem of Calculus. The height of one graph controls exactly how fast the accumulated area of the other graph grows.

## Scene 05 — f(x) = x, and a Loop That Closes — 5:41–6:46 — Voice Clip 05

Test that idea on the simplest curve: f of x equals x. The region under this line, from zero out to x, is just a triangle — base x, height x. Its area is one half, base times height, which becomes one half, x times x: A of x equals x squared over two.

Differentiate that area function, and watch what happens: the two comes down, the exponent drops by one, and every trace of the one half cancels away, leaving exactly x. The loop closes on itself — x becomes x squared over two, and x squared over two differentiates straight back into x. Once you have seen that circle complete itself, the Fundamental Theorem is impossible to forget.

## Scene 06 — A Derivative Is a New Function — 6:46–7:57 — Voice Clip 06

Before we go further into integrals, one more look at what a derivative truly is. Take f of x equals x squared, and slide a tangent line along it point by point. At each stop, read off its slope, and plot that single number on a second graph beneath.

At x equals minus two, minus one, zero, one, two, the slopes read minus four, minus two, zero, two, four. Those five points do not scatter randomly — they line up perfectly straight, tracing f prime of x equals two x.

A derivative was never just one slope at one point. It is an entire new function, describing how the original curve is changing everywhere at once.

## Scene 07 — Maxima and Minima — 7:57–8:53 — Voice Clip 07

Send a point walking across a hill-shaped curve. On the way up, the tangent tilts upward: f prime of x is positive. At the very top, the tangent goes flat: f prime of x equals zero. Coming down the other side, the tangent tilts downward: f prime of x is negative.

Watch the derivative graph underneath the whole time, and the pattern is unmistakable: it crosses zero at exactly the same instant the curve above hits its peak. A maximum, or a minimum, is simply the place where change switches direction.

## Scene 08 — The Fenced-Garden Optimization — 8:53–10:29 — Voice Clip 08

Here is that idea put to real use. Imagine fencing a rectangular garden beside a river, with the river standing in for one whole side — free of charge. One hundred metres of fencing remain for the other three sides. Call the width x; the two matching sides use two x of fencing, leaving y equals one hundred minus two x for the side opposite the river. The area becomes A of x equals x, times one hundred minus two x.

Make the garden very narrow, and the area is small. Make it very wide, and the area shrinks right back down. Somewhere between those extremes, the area reaches a peak. Differentiate: A prime of x equals one hundred minus four x. Set that derivative to zero, and solve: x equals twenty-five.

That is the real power of a derivative — not decoration, but the tool that finds exactly where improvement stops and decline begins.

## Scene 09 — Reversing the Derivative, and the Mystery of +C — 10:29–11:43 — Voice Clip 09

Now flip the question around. Suppose velocity is known: v of t equals two t. Can position be rebuilt from it alone? Integrate: s of t equals the integral of two t, dt, which works out to t squared, plus C.

That plus C is not a technicality to memorize — watch three curves at once: t squared minus two, t squared, and t squared plus three. Every one of them has the exact same slope at every matching x-value; only their height differs. Differentiating a curve throws away information about where it started vertically, and no amount of integrating can recover that missing starting height on its own — only one more piece of information, an initial condition, can pin it back down.

## Scene 10 — Substitution as New Coordinates — 11:43–12:53 — Voice Clip 10

Consider the integral of two x, cosine of x squared, dx. Notice that x squared sitting inside the cosine — rename it. Let u equal x squared; then du equals two x, dx. Swap both pieces in, and the integral collapses into something plain: the integral of cosine u, du.

Watch the x-axis itself stretch unevenly into a new u-axis: equal steps in x land as unequal steps in u, because squaring distorts the spacing. That very distortion is exactly what du accounts for. Substitution is not a trick pulled from nowhere — it is simply changing coordinates so the underlying structure turns simple again.

The points move, but more importantly, the spacing between them changes.

## Scene 11 — Integration by Parts, Geometrically — 12:53–14:08 — Voice Clip 11

Picture a rectangle with sides u and v; its area is u v. Now let both sides grow by a small amount at once. The rectangle gains a strip along the top, with area u dv, and a strip along the side, with area v du — plus one tiny leftover corner, du dv, that shrinks away faster than the rest and can be ignored.

That growing rectangle says exactly this: d of u v equals u dv plus v du. Rearrange it — u dv equals d of u v, minus v du — and integrate both sides: the integral of u dv equals u v, minus the integral of v du. Not a formula to memorize. A rectangle, rearranged.

## Scene 12 — Area Between Curves — 14:08–15:09 — Voice Clip 12

Two curves, f of x on top and g of x below, trap a region between them. At any x, the vertical gap separating them is f of x minus g of x. Slice that gap into a strip of width dx, and its area is approximately f of x minus g of x, times dx.

Add hundreds of these thin vertical strips, and they fill the entire region: A equals the integral, from a to b, of f of x minus g of x, dx. Complicated shapes become simple the moment they are sliced thin enough.

## Scene 13 — The Deep Connection and Final Revelation — 15:09–17:19 — Voice Clip 13

One motion, watched two ways at once. Differentiate position, s of t, and the tangent's slope traces out velocity, v of t. Integrate velocity, and the accumulating area beneath it traces out the change in position. Position, differentiated, becomes velocity. Velocity, integrated, becomes position change. Two directions, one underlying motion.

At every instant, the moving tangent and the filling area are describing the same journey from opposite directions.

That is the Fundamental Theorem of Calculus, stated in full. The derivative of the accumulation of f, from a to x, equals f of x itself. And the integral of f, from a to b, equals F of b minus F of a, wherever F prime equals f.

Derivatives look at change locally — they zoom into the infinitely small. Integrals rebuild the whole from those tiny local changes — they add infinitely many small pieces back together. Changing motion led to a derivative; a derivative led to optimization; optimization led to tiny pieces; tiny pieces led to accumulation; accumulation led to an integral; and the integral led back to the Fundamental Theorem, closing the circle. Two sides of the same idea, from start to finish. In the next video, I am going to explain the next step — from integrals to differential equations.

## Scene 14 — Subscribe — 17:19–17:34 — Voice Clip 14

Thank you for watching. Stay curious — and keep following where the mathematics leads next.
