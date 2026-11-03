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
        ('But could you say', "[short pause] [curious]"),
        ('What sets the highest', "[short pause] [curious]"),
        ('This is Vectors and', "[pause] [warmly]"),
    ],
    "02": [
        ('Where is it?', "[short pause] [curious]"),
        ('How fast, and in', "[short pause] [curious]"),
        ("Let's start with the", "[pause] [warmly]"),
    ],
    "03": [
        ('But from that reading', "[short pause] [curious]"),
        ('Direction.', "[pause] [warmly]"),
    ],
    "04": [
        ('And the first place', "[pause] [warmly]"),
    ],
    "05": [
        ('Can you travel a', "[short pause] [curious]"),
        ('Displacement asks a different', "[short pause] [curious]"),
        ('Scalars describe magnitude. Vectors', "[pause] [warmly]"),
    ],
    "06": [
        ('When several movements happen', "[short pause] [curious]"),
        ('But how do we', "[short pause] [curious]"),
    ],
    "07": [
        ('Is there a single', "[short pause] [curious]"),
        ('Next: what does it', "[short pause] [curious]"),
        ('Adding vectors tells us', "[pause] [warmly]"),
    ],
    "08": [
        ('Has the velocity changed?', "[short pause] [curious]"),
        ('Addition gives the combined', "[pause] [warmly]"),
    ],
    "09": [
        ('What happens when we', "[short pause] [curious]"),
        ('But what if we', "[short pause] [curious]"),
        ('Multiplying by a scalar', "[pause] [warmly]"),
    ],
    "10": [
        ('Together they let us', "[pause] [warmly]"),
    ],
    "11": [
        ('How much of it', "[short pause] [curious]"),
        ('And how much points', "[short pause] [curious]"),
        ('So how big is', "[pause] [warmly]"),
    ],
    "12": [
        ('Length and angle, or', "[pause] [warmly]"),
    ],
    "13": [
        ('How do we add', "[short pause] [curious]"),
        ('But first, we need', "[pause] [warmly]"),
    ],
    "14": [
        ('For that, we need', "[pause] [warmly]"),
    ],
    "15": [
        ('Which raises the next', "[short pause] [curious]"),
    ],
    "16": [
        ('So when is something', "[short pause] [curious]"),
        ('Now, can these definitions', "[short pause] [curious]"),
    ],
    "17": [
        ('If we know where', "[short pause] [curious]"),
        ("With that, we're ready", "[short pause] [curious]"),
    ],
    "18": [
        ('Once the ball leaves', "[short pause] [curious]"),
        ('To use them, we', "[pause] [warmly]"),
    ],
    "19": [
        ('One will stay fixed.', "[pause] [warmly]"),
    ],
    "20": [
        ('The vertical motion follows', "[pause] [warmly]"),
    ],
    "21": [
        ('Watch the shadow on', "[curious]"),
        ('Gravity still pulls downward.', "[short pause] [emphasized]"),
        ('Then the shadow falls.', "[short pause]"),
        ('Two independent motions, sharing', "[pause] [warmly]"),
    ],
    "22": [
        ('At the very top', "[short pause] [curious]"),
        ('And the acceleration?', "[short pause] [curious]"),
        ('Zero velocity in one', "[pause] [warmly]"),
    ],
    "23": [
        ('But why exactly that', "[short pause] [curious]"),
        ("Now let's put numbers", "[pause] [warmly]"),
    ],
    "24": [
        ('How long does it', "[short pause] [curious]"),
        ('So the ball rises', "[pause] [warmly]"),
    ],
    "25": [
        ('How far does the', "[short pause] [curious]"),
        ('So which angle wins?', "[short pause] [curious]"),
        ('The range depends on', "[pause] [warmly]"),
    ],
    "26": [
        ("The equations don't just", "[pause] [warmly]"),
    ],
    "27": [
        ('At the top of', "[short pause] [curious]"),
        ('Which lands first?', "[short pause] [curious]"),
        ('If a question surprised', "[pause] [warmly]"),
    ],
    "28": [
        ('We started with a', "[short pause] [curious]"),
        ('What happens when an', "[short pause] [curious]"),
        ('Can it accelerate without', "[pause] [warmly]"),
    ],
    "29": [
        ('Thanks for watching. Stay', "[pause] [warmly]"),
    ],
}
