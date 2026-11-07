"""Sparse ElevenLabs v3/v4 delivery cues, separate from the spoken science.

Each anchor must occur exactly once in its scene. Cues sit at sentence starts
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
        ("Nothing has changed on", "[short pause] [curious]"),
        ("So here's the surprising", "[short pause] [emphasized]"),
        ("Why does that happen?", "[short pause] [curious]"),
        ("This is Circular Motion.", "[pause] [warmly]"),
    ],
    "02": [
        ("Physics uses a more", "[short pause]"),
        ("That's the key idea", "[pause] [emphasized]"),
    ],
    "03": [
        ("How much has the", "[short pause] [curious]"),
        ("The speed didn't change", "[short pause] [emphasized]"),
    ],
    "04": [
        ("But which way does", "[short pause] [curious]"),
        ("Let's see what that", "[pause] [warmly]"),
    ],
    "05": [
        ("Now add time as", "[short pause] [curious]"),
        ("But the magnitude doesn't.", "[short pause] [emphasized]"),
    ],
    "06": [
        ("Yet you were moving", "[short pause]"),
        ("Which brings us to", "[pause] [warmly]"),
    ],
    "07": [
        ("If the velocity arrows", "[curious]"),
        ("Shrink the time interval.", "[short pause] [curious]"),
        ("A perpendicular acceleration turns", "[pause] [warmly]"),
    ],
    "08": [
        ("Here's a lovely way", "[short pause] [warmly]"),
        ("Watch the ratio as", "[short pause] [curious]"),
    ],
    "09": [
        ("Take the limit of", "[short pause] [emphasized]"),
        ("There's a second way", "[pause] [curious]"),
        ("And the particle's speed", "[pause] [warmly]"),
    ],
    "10": [
        ("Speed enters squared.", "[short pause] [emphasized]"),
        ("Why? On a wider", "[short pause] [curious]"),
    ],
    "11": [
        ("If the acceleration points", "[curious]"),
        ("Coast, nudge, coast, nudge.", "[short pause]"),
        ("Circular motion isn't an", "[pause] [warmly]"),
    ],
    "12": [
        ("Measure it in radians.", "[short pause]"),
        ("And if we keep", "[pause] [curious]"),
    ],
    "13": [
        ("How quickly does an", "[curious]"),
        ("Here's what that means.", "[short pause] [warmly]"),
        ("That outer point is", "[pause] [warmly]"),
    ],
    "14": [
        ("Back to our particle.", "[pause] [warmly]"),
        ("Angular speed, period, frequency", "[pause] [emphasized]"),
    ],
    "15": [
        ("But that doesn't mean", "[short pause] [emphasized]"),
        ("Keep that distinction in", "[pause] [warmly]"),
    ],
    "16": [
        ("What causes it?", "[short pause] [curious]"),
        ("Now the most important", "[pause] [emphasized]"),
        ("Different forces. The same", "[pause] [warmly]"),
    ],
    "17": [
        ("Now, suppose the string", "[pause] [curious]"),
        ("Many people expect it", "[short pause]"),
        ("The ball never needed", "[pause] [warmly]"),
    ],
    "18": [
        ("Take a curve of", "[pause]"),
        ("At twenty metres per", "[short pause] [emphasized]"),
        ("This is an idealized", "[pause] [calm]"),
    ],
    "19": [
        ("So what keeps it", "[short pause] [curious]"),
        ("Fire it fast enough,", "[short pause] [emphasized]"),
        ("Gravity up there is", "[short pause]"),
    ],
    "20": [
        ("If the force is", "[short pause] [curious]"),
        ("Now ride along inside", "[pause]"),
        ("Circular motion needs a", "[pause] [warmly]"),
    ],
    "21": [
        ("But what if the", "[short pause] [curious]"),
    ],
    "22": [
        ("But its speed is", "[short pause]"),
        ("Our particle again.", "[pause] [warmly]"),
        ("One part turns the", "[pause] [warmly]"),
    ],
    "23": [
        ("These aren't different definitions.", "[pause] [emphasized]"),
    ],
    "24": [
        ("Time to test your", "[warmly]"),
        ("Two. An object goes", "[pause]"),
        ("Three. A particle on", "[pause]"),
        ("Four. A satellite moves", "[pause]"),
        ("Five. Can the angular", "[pause]"),
        ("If a question surprised", "[pause] [warmly]"),
    ],
    "25": [
        ("We began with a", "[short pause] [curious]"),
        ("The answer is yes.", "[short pause] [emphasized]"),
        ("Once we understand how", "[pause] [warmly]"),
    ],
    "26": [
        ("Thanks for watching. Stay", "[pause] [warmly]"),
    ],
}
