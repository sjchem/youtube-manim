# Animation Plan — Statistics for ML · Part 1 · Chapter 1

Total target: ~7 min 15 sec

---

## Scene 01 — Series Opening  (~55 s)
**Narrative arc**: A universe of data comes alive; the course is revealed.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–8s | Data rain — noise + signal dots appear | LaggedStart FadeIn for ~85 dots |
| P2 | 8–16s | True sine curve emerges from the dots | Create(ParametricFunction) + glow |
| P3 | 16–28s | Data dims; course title card reveals | Write title lines; glow underline |
| P4 | 28–42s | Series roadmap: 4-part grid | LaggedStart FadeIn boxes |
| P5 | 42–50s | Part 1 spotlighted; Chapter 1 title | Indicate + scale; YOU ARE HERE |
| P6 | 50–55s | Main question posed | Write question; transition |

**Key objects**: Dot (cyan + muted), ParametricFunction, RoundedRectangle, Text (hero 76pt)

---

## Scene 02 — The Uncertain World  (~47 s)
**Narrative arc**: Reality has a true signal; we only see noisy observations.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–10s | Green sine wave appears (hidden truth) | Animate stroke opacity 0→0.9 |
| P2 | 10–25s | Orange noise dots scatter around curve | LaggedStart FadeIn 55 dots |
| P3 | 25–36s | Uncertainty error bars + ML noise labels | GrowFromCenter error bars; FadeIn tags |
| P4 | 36–44s | True curve dims; purple "?" fades in | animate fill opacity; FadeIn ? |
| P5 | 44–47s | "Statistics gives us the tools" | FadeIn text top; curve returns |

**Key objects**: ParametricFunction (green), Dot (orange), error bars (Line), Text "?"

---

## Scene 03 — Signal vs Noise  (~50 s)
**Narrative arc**: Statistical smoothing extracts signal; residuals = noise.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–14s | Axes + noisy scatter (70 orange dots) | Create axes; LaggedStart dots |
| P2 | 14–28s | Smoothed mean line appears | Create smooth VMobject + glow |
| P3 | 28–41s | Residual lines + residual formula | LaggedStart Create lines; Write formula |
| P4 | 41–50s | Labels SIGNAL/NOISE + equation | FadeIn labels; Write equation |

**Key objects**: Axes, Dot, VMobject (smooth), Line (residuals)
**Equation**: Data = Signal + Noise

---

## Scene 04 — Population vs Sample  (~49 s)
**Narrative arc**: We reason about the whole from a small measured part.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–13s | 200 muted population dots | LaggedStart FadeIn |
| P2 | 13–26s | 25 cyan sample dots highlighted | Dim population; FadeIn sample |
| P3 | 26–38s | μ and x̄ dashed vertical lines | Create lines + MathTex labels |
| P4 | 38–49s | CI bracket + ML test-set note | Create CI bars; FadeIn note |

**Key objects**: Dot (muted + cyan), DashedLine, MathTex (μ, x̄)

---

## Scene 05 — Patterns & Prediction  (~56 s)
**Narrative arc**: Statistics finds the pattern; probability wraps it in uncertainty.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–13s | Scatter 18 data points on axes | Create axes; LaggedStart dots |
| P2 | 13–26s | Regression line drawn | Create Line + glow |
| P3 | 26–38s | Confidence band appears for average trend | FadeIn polygon + boundary curves |
| P4 | 38–56s | Wider prediction interval + new purple dot → prediction ŷ | FadeIn outer band; Move dot; dashed lines; ŷ label |

**Key objects**: Axes, Dot, Line (regression), Polygon (band), Arrow
**Equation**: ŷ symbol

---

## Scene 06 — Overfitting  (~58 s)
**Narrative arc**: Memorising data ≠ learning; statistics tells us the difference.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–12s | 10 cyan training dots on axes | Create axes; LaggedStart dots |
| P2 | 12–24s | Good linear fit (green) drawn | Create Line + glow |
| P3 | 24–39s | Overfit polynomial (red) + training error note | Create VMobject; FadeIn note |
| P4 | 39–53s | New purple test dot; arrows show gap; test error note | GrowArrow green ✓ / red ✗; FadeIn note |
| P5 | 53–58s | Final caption | FadeIn caption |

**Key objects**: Dot, Line (green), VMobject (red wiggly), Arrow, Text ✓ ✗

---

## Scene 07 — Bias-Variance Tradeoff  (~55 s)
**Narrative arc**: Dartboard metaphor makes bias and variance tangible.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–16s | 4 dartboards + labels appear | LaggedStart FadeIn boards + labels |
| P2 | 16–38s | Darts thrown at each board | LaggedStart GrowFromCenter dots |
| P3 | 38–46s | Ideal quadrant highlighted | Halo circle; Indicate |
| P4 | 46–55s | Expected Test Error = Bias² + Variance + Noise | Write equation top |

**Key objects**: Circle (concentric rings), Dot (darts), Text equation

---

## Scene 08 — Statistics: The Thinking Layer  (~53 s)
**Narrative arc**: Statistics is not separate from ML — it is the reasoning layer beneath.

| Phase | Duration | Visual | Animation |
|-------|----------|--------|-----------|
| P1 | 0–14s | 4-stage pipeline boxes + arrows | LaggedStart FadeIn; animate arrows |
| P2 | 14–22s | Statistics box pulsed/indicated | Indicate; stroke width animates |
| P3 | 22–42s | 6 tool bubbles fan out from Stats box | LaggedStart FadeIn bubbles + lines |
| P4 | 42–53s | Synthesis: "Statistics is how machines learn" | Write text top |

**Key objects**: RoundedRectangle, Arrow, Circle (bubbles), Text

---

## Scene 09 — Subscribe Card  (~12 s)
**Objects**: Text cards (THANK YOU / SUBSCRIBE / tagline)
**Animation**: FadeIn staggered; Indicate subscribe

---

## Shared Visual Language
- **Cyan** = signal, model, statistics layer
- **Green** = correct, generalisation, truth
- **Orange** = observations, raw data, uncertainty
- **Red** = error, overfitting, noise residuals
- **Purple** = new/unseen data, limits, prediction targets
- **Gold** = highlight, sample mean, CI, subscribe
- **Muted grey** = background structures, population
