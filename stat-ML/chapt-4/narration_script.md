# Narration Script - Chapter 4: Probability Basics Every ML Learner Must Know

Total planned runtime: ~11-12 minutes. Timestamps are approximate and align with
`config.SCENE_DURATIONS`.

**Manim feature policy:** Scenes 01-09 should be built as Manim animations. Core Manim is the
default so the project stays render-safe. Scene 10 stays a simple closing card.

---

## Scene 01 - Uncertainty (0:00 - 1:08)

The real world is messy. Emails can look suspicious without being spam. Medical symptoms can
point to more than one condition. A photo can be blurry, cropped, or taken in bad light.

So here is the main question: how can machine learning make predictions when the world is
uncertain, noisy, and incomplete?

A model never sees the whole real world. It sees data: examples, patterns, measurements, and
signals. Because the evidence is incomplete, the answer is usually not absolute truth. It is a
probability.

Here is an email. The model reads the words, the links, the sender, and the formatting. And
instead of saying, "this is definitely spam," it says:

`P(spam | email features) = 0.95`

That number is the doorway into this chapter. Machine learning is not only trying to be right.
It is trying to measure how likely something is, given what it knows.

**Manim feature:** Noisy evidence becomes an email, passes through a small ML model, and becomes
a filled probability bar. The chapter title appears at the end of the scene.

## Scene 02 - Probability as a Function (1:08 - 2:22)

Now we give that number a name.

Probability is a function. It takes an event and assigns a number to it.

`P(A)`

Here, `A` is an event, and `P(A)` is the probability of that event.

For example:

`P(Rain) = 0.30`

means there is a thirty percent chance of rain.

Every probability must live between zero and one:

`0 <= P(A) <= 1`

And the probability of the whole sample space is one:

`P(Omega) = 1`

That means something in the set of all possible outcomes must happen.

One very useful rule follows immediately: the complement rule.

`P(A^c) = 1 - P(A)`

So if:

`P(Spam) = 0.95`

then:

`P(Not Spam) = 0.05`

This is already the beginning of binary classification: one class and its complement.

**Manim feature:** Show `P(A)`, the bounds `0 <= P(A) <= 1`, `P(Omega)=1`, a rain marker at
`0.30`, then a spam/not-spam complement pair.

## Scene 03 - Addition & Multiplication Rules (2:22 - 3:38)

Once we can assign probability to one event, the next question is: what happens when we combine
events?

For "A or B", we use the addition rule:

`P(A union B) = P(A) + P(B) - P(A intersection B)`

The subtraction matters because the overlap gets counted twice.

Imagine a customer who might buy coffee, cake, or both. The probability of buying at least one
is the coffee probability plus the cake probability, minus the overlap where both are true.

For events happening together in sequence, we use the multiplication rule:

`P(A intersection B) = P(B | A) P(A)`

Read it as: the probability of A and B together equals the probability of A, times the
probability of B after A is already true.

This is the bridge to Bayes' theorem.

**Manim feature:** First show overlapping coffee/cake circles for the addition rule. Then
replace them with a small disease-to-positive-test probability tree for the multiplication rule.

## Scene 04 - Conditional Probability (3:38 - 4:58)

Now the vertical bar becomes important.

`P(A | B)`

means the probability of A, given B.

Mathematically, conditional probability is:

`P(A | B) = P(A intersection B) / P(B)`

This says: once B is known to be true, shrink the world down to B. Inside that smaller world,
ask how much also belongs to A.

That is exactly what a spam filter does. It does not ask only:

`P(spam)`

It asks:

`P(spam | email features)`

When the email contains "free", many links, and an unknown sender, the model updates its belief:

`P(spam | email features) = 0.95`

Conditional probability is the mathematical version of "given the evidence."

**Manim feature:** Use a Venn diagram to show `B` as the restricted world and `A intersection B`
as the overlap. Then transition to the email feature chips and posterior spam probability.

## Scene 05 - Bayes' Theorem (4:58 - 6:08)

Bayes' theorem should not feel magical. It comes directly from conditional probability.

Start with:

`P(H | E) = P(H intersection E) / P(E)`

Here, `H` is a hypothesis, like "the patient has the disease." `E` is evidence, like a positive
test.

Now rewrite the joint probability using the multiplication rule:

`P(H intersection E) = P(E | H) P(H)`

Substitute that into the first equation:

`P(H | E) = P(E | H) P(H) / P(E)`

That is Bayes' theorem.

It says: start with a prior belief, measure how likely the evidence is under that belief, then
normalize by how common the evidence is overall.

This is how probability updates when new evidence appears.

**Manim feature:** Show a prior-to-evidence-to-updated-belief flow, then reveal the three-line
Bayes derivation step by step.

## Scene 06 - Random Variables, Distributions & Expected Value (6:08 - 7:24)

So far, probability has been attached to events. Machine learning also needs variables.

A random variable turns uncertain outcomes into values.

For a coin:

`X = 1` for heads

`X = 0` for tails

In machine learning, features and labels can be treated as random variables.

A probability distribution tells us how probability is spread across possible values.

For a die, the distribution is discrete: each outcome from one to six has probability one-sixth.

For measurements like height, noise, or prediction error, the distribution may be continuous.
One famous continuous shape is the normal distribution, or bell curve.

Another powerful idea is expected value:

`E[X] = sum over x of x P(x)`

It means the long-run average. For a fair die, the expected value is three point five.

This idea will matter later when we talk about loss functions and optimization.

**Manim feature:** Map coin outcomes to a random variable, show a fair-die discrete
distribution, show a bell curve, then reveal the expected-value formula.

## Scene 07 - Joint, Marginal & Independence (7:24 - 8:46)

Real machine learning data usually has many variables at once.

Joint probability keeps variables together:

`P(A, B)`

For example: the probability that a user clicks and buys.

A probability table lets us see those combinations as cells.

Marginal probability zooms out:

`P(A) = sum over b of P(A, B=b)`

That means we sum across the other variable and keep only the one we care about.

This also gives us a clean definition of independence.

If A and B are independent:

`P(A, B) = P(A) P(B)`

But in machine learning, features are often not independent:

`P(A, B) != P(A) P(B)`

Income and education, symptoms and disease, words and spam labels - useful signals are often
connected.

**Manim feature:** Use a joint probability table, highlight one cell, sum one row into a
marginal, then show the independence equality and the usual ML inequality.

## Scene 08 - The ML Prediction Formula (8:46 - 10:04)

Now the whole chapter connects to supervised machine learning.

Most supervised models can be viewed as estimating:

`P(y | x)`

Here, `x` is what the model observes: features, pixels, symptoms, transaction details, or email
content.

And `y` is what the model predicts: spam, cat, fraud, disease, or any class label.

Examples:

`P(Spam | Email)`

`P(Cat | Pixels)`

`P(Fraud | Transaction)`

`P(Disease | Symptoms)`

The model is not seeing the whole world. It is using the evidence in `x` to estimate the
probability of `y`.

That is why probability is not a side topic in machine learning. It is often the shape of the
prediction itself.

**Manim feature:** Animate `x = features` through a model into `P(y | x)`, then show four
concrete ML examples.

## Scene 09 - Synthesis & Next Chapter Bridge (10:04 - 11:14)

Now the chain is complete.

Probability starts with events:

`P(A)`

Then we learn complements, addition, multiplication, conditional probability, and Bayes'
theorem.

Random variables let us attach probability to values. Distributions show how probability is
spread. Expected value summarizes the long-run average.

Joint and marginal probability help us work with many variables at once. Independence tells us
when variables do, or do not, carry information about each other.

And machine learning brings the whole chain together as:

`P(y | x)`

Based on the data I have seen, this outcome is more likely than that one.

That is the language of uncertainty in machine learning.

And it leads directly to the next chapter: probability distributions, the patterns behind data.

**Manim feature:** Show the full probability chain as connected nodes, then transition into bell
and skewed distribution curves for the next chapter.

## Scene 10 - Subscribe (11:14 - 11:42)

Thank you for watching. In the next chapter, we will look deeper at probability distributions:
the patterns behind data, and why those shapes matter for machine learning.

Stay curious, and keep building your ML foundations.
