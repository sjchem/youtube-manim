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
        ("But lift them off", "[curious]"),
        ("Why? Why don't", "[short pause] [curious]"),
        ("The answer is hidden", "[warmly]"),
    ],
    "02": [
        ("But it is drawn on flat paper.", "[curious]"),
        ("The real molecule does", "[warmly]"),
        ("To predict shape", "[short pause] [thoughtful]"),
    ],
    "03": [
        ("They spread apart", "[thoughtful]"),
        ("A tetrahedron. In this", "[short pause] [warmly]"),
        ("This idea has a name", "[thoughtful]"),
    ],
    "04": [
        ("A triple bond?", "[curious]"),
        ("Chemists write this", "[warmly]"),
        ("And the steric number", "[short pause] [thoughtful]"),
    ],
    "05": [
        ("Spin it any way", "[warmly]"),
        ("Tip it on its edge", "[curious]"),
        ("But four regions cannot", "[short pause] [curious]"),
    ],
    "06": [
        ("Let the regions use", "[warmly]"),
        ("Where does that number", "[curious]"),
        ("Not a number to memorise.", "[short pause] [warmly]"),
    ],
    "07": [
        ("Now for the most important", "[thoughtful]"),
        ("But here is the catch.", "[curious]"),
        ("The lone pair is invisible", "[short pause] [thoughtful]"),
    ],
    "08": [
        ("A word of honesty", "[thoughtful]"),
        ("Now look back", "[warmly]"),
        ("Water has four regions, but", "[short pause] [warmly]"),
    ],
    "09": [
        ("What happens with five", "[curious]"),
        ("That difference between", "[thoughtful]"),
        ("So when lone pairs appear", "[short pause] [curious]"),
    ],
    "10": [
        ("Ninety degree contacts", "[thoughtful]"),
        ("One hundred and eighty degrees, just like", "[warmly]"),
        ("Not four things to memorise.", "[short pause] [warmly]"),
    ],
    "11": [
        ("This time everything", "[warmly]"),
        ("Six regions around sulfur", "[thoughtful]"),
        ("So what happens when lone pairs move", "[short pause] [curious]"),
    ],
    "12": [
        ("Now a second lone pair.", "[curious]"),
        ("How can a molecule", "[short pause] [curious]"),
        ("Because two of its regions", "[warmly]"),
    ],
    "13": [
        ("Here's the trick.", "[warmly]"),
        ("Turn this dial.", "[curious]"),
        ("This is a mathematical model", "[thoughtful]"),
    ],
    "14": [
        ("But here is the beautiful part.", "[short pause] [warmly]"),
        ("With the same s character", "[thoughtful]"),
        ("Two completely different routes", "[warmly]"),
    ],
    "15": [
        ("Let's watch the two pictures", "[warmly]"),
        ("Now ethene", "[curious]"),
        ("So a double bond", "[thoughtful]"),
    ],
    "16": [
        ("It's a useful picture.", "[thoughtful]"),
        ("So keep the two models", "[warmly]"),
        ("Treat them as historical", "[short pause] [thoughtful]"),
    ],
    "17": [
        ("Shape has one more surprise.", "[curious]"),
        ("But water is bent.", "[short pause] [curious]"),
        ("Both have polar bonds", "[warmly]"),
    ],
    "18": [
        ("This time the chain", "[curious]"),
        ("To be fair", "[thoughtful]"),
        ("For these molecules, symmetry", "[warmly]"),
    ],
    "19": [
        ("Your turn.", "[warmly]"),
        ("Take a moment.", "[short pause]"),
        ("You didn't memorise those.", "[short pause] [warmly]"),
    ],
    "20": [
        ("We started with a simple question.", "[thoughtful]"),
        ("But molecules live", "[short pause] [warmly]"),
        ("And that third dimension", "[warmly]"),
    ],
    "21": [
        ("But there's a question", "[curious]"),
        ("Next time:", "[short pause] [warmly]"),
    ],
    "22": [],
}
