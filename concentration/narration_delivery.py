"""Sparse ElevenLabs v3/v4 delivery cues, separate from the spoken science.

Each anchor must occur exactly once in its scene. Put cues at sentence starts
so regenerated scripts keep continuous prose and never split a technical term.
Bracketed directions are performance suggestions, not exact timing controls.
See https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
"""

from __future__ import annotations

# Shared opening delivery keeps the cloned narrator consistent across clips.
OPENING_TAG = "[warm, conversational delivery]"

# Unique text anchors make a script edit fail visibly if a cue needs updating.
DELIVERY_CUES: dict[str, list[tuple[str, str]]] = {
    "01": [
        ("Now, a question.", "[pause] [curious]"),
        ("Four different numbers.", "[short pause]"),
        ("So which one is right?", "[pause] [curious]"),
        ("All of them.", "[short pause] [warmly]"),
        ("So let's stop memorising,", "[short pause] [warmly]"),
    ],
    "02": [
        ("But chemistry happens", "[short pause]"),
        ("Ten times more mass", "[pause] [curious]"),
    ],
    "03": [
        ("Mix them, and you don't get", "[short pause] [curious]"),
        ("Nothing leaked.", "[short pause] [thoughtful]"),
        ("Most concentration measures", "[pause] [warmly]"),
    ],
    "04": [
        ("Now the denominator.", "[short pause]"),
        ("Zero point five two four moles per litre.", "[pause] [warmly]"),
        ("What does it mean physically?", "[short pause] [curious]"),
        ("Notice the word in the denominator again.", "[pause] [thoughtful]"),
    ],
    "05": [
        ("Here's the tempting way:", "[short pause] [playful]"),
        ("But the glucose takes up room.", "[short pause] [thoughtful]"),
        ("There's one catch", "[pause] [curious]"),
        ("We have a way to measure", "[short pause] [thoughtful]"),
    ],
    "06": [
        ("Now switch that off.", "[short pause]"),
        ("Watch the formula change.", "[pause] [curious]"),
        ("The difference isn't in the glucose.", "[short pause] [thoughtful]"),
        ("Volume doesn't make that promise.", "[short pause] [curious]"),
    ],
    "07": [
        ("Dissolved glucose dilutes the water,", "[thoughtful]"),
        ("Why molality here,", "[pause] [curious]"),
        ("Which brings us to an experiment.", "[pause] [curious]"),
    ],
    "08": [
        ("Now warm it gently,", "[short pause]"),
        ("Look at the meters.", "[pause] [curious]"),
        ("And molality?", "[short pause]"),
        ("We haven't removed any glucose.", "[long pause] [thoughtful]"),
        ("Same glucose. Same water.", "[pause] [warmly]"),
    ],
    "09": [
        ("But when temperature changes,", "[short pause] [thoughtful]"),
        ("And here's a detail worth seeing.", "[pause] [curious]"),
        ("Close is not the same.", "[short pause] [thoughtful]"),
    ],
    "10": [
        ("Here's the catch.", "[pause] [curious]"),
        ("But the molecule doesn't decide", "[short pause] [thoughtful]"),
        ("Historically, normality was everywhere", "[pause]"),
        ("So let's run the experiment both ways.", "[short pause] [warmly]"),
    ],
    "11": [
        ("On the right, twice as much base.", "[short pause]"),
        ("These labels describe the original acid stock,", "[pause] [curious]"),
        ("And that second question", "[short pause] [thoughtful]"),
        ("Now let's leave reactions behind,", "[pause] [warmly]"),
    ],
    "12": [
        ("What are the chances it's glucose?", "[short pause] [curious]"),
        ("Pick one.", "[short pause] [playful]"),
        ("Repeat independent picks,", "[pause]"),
        ("Notice the bottom of the fraction.", "[short pause] [thoughtful]"),
    ],
    "13": [
        ("Add the two together.", "[short pause]"),
        ("That's no accident.", "[short pause] [warmly]"),
        ("Tiny here.", "[pause] [thoughtful]"),
    ],
    "14": [
        ("Not by itself.", "[short pause] [thoughtful]"),
        ("The second kind mixes", "[pause]"),
        ("Same solution.", "[short pause] [thoughtful]"),
        ("So whenever you see a percent,", "[short pause] [warmly]"),
    ],
    "15": [
        ("Remember: ethanol and water shrink", "[short pause] [thoughtful]"),
        ("One more relative", "[pause]"),
        ("Compare it with molarity.", "[short pause] [curious]"),
    ],
    "16": [
        ("Here's one gold particle.", "[pause] [softly]"),
        ("Zoom in.", "[short pause] [softly]"),
        ("If one second were your gold dot,", "[pause] [curious]"),
        ("But that's an approximation", "[short pause] [thoughtful]"),
        ("Tiny ratios, but the same question", "[pause] [warmly]"),
    ],
    "17": [
        ("That bridge is density.", "[short pause] [warmly]"),
        ("Total mass minus glucose mass leaves solvent:", "[short pause]"),
        ("Don't memorise it.", "[pause] [thoughtful]"),
    ],
    "18": [
        ("But watch them.", "[short pause] [softly]"),
        ("That equation isn't a rule to memorise.", "[pause] [thoughtful]"),
        ("Five times the volume,", "[short pause] [warmly]"),
    ],
    "19": [
        ("Time to test yourself.", "[playful]"),
        ("That does not fix the final solution volume.", "[long pause]"),
        ("Different denominators:", "[long pause]"),
        ("Only if both protons react.", "[long pause]"),
        ("That's a mole ratio.", "[long pause]"),
        ("Only roughly,", "[long pause]"),
        ("Five traps, and one escape route:", "[pause] [warmly]"),
    ],
    "20": [
        ("Now every number has a meaning", "[short pause] [warmly]"),
        ("So next time you meet", "[pause] [thoughtful]"),
        ("What are we actually comparing?", "[short pause] [softly]"),
        ("Once you can see that,", "[pause] [warmly]"),
    ],
    "21": [],
}
