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
        ("Now give the same", "[short pause]"),
        ("Give it to a cylinder", "[short pause] [curious]"),
        ("Same push. Three", "[pause] [emphasized]"),
        ("So why can the same", "[pause] [curious]"),
        ("This is System", "[pause] [warmly]"),
    ],
    "02": [
        ("But try that with", "[short pause] [curious]"),
        ("And we make one", "[short pause]"),
        ("And in rolling,", "[short pause] [emphasized]"),
        ("Let's start with the", "[pause] [warmly]"),
    ],
    "03": [
        ("Now make one of them", "[short pause] [curious]"),
        ("In uniform gravity,", "[short pause] [emphasized]"),
        ("Let's try it.", "[pause]"),
    ],
    "04": [
        ("But spread the mass", "[short pause]"),
        ("It can even lie", "[short pause] [curious]"),
        ("Now toss the hammer.", "[pause] [curious]"),
        ("Hold on to that.", "[short pause] [warmly]"),
    ],
    "05": [
        ("The centre of mass is the mass-weighted", "[short pause] [emphasized]"),
        ("And it doesn't matter", "[short pause] [curious]"),
        ("From two beads", "[pause] [warmly]"),
    ],
    "06": [
        ("Look at the internal", "[short pause]"),
        ("But the internal forces", "[short pause] [emphasized]"),
        ("So the net external", "[pause] [emphasized]"),
        ("Let's test it.", "[pause] [curious]"),
        ("One caution.", "[pause]"),
    ],
    "07": [
        ("At the top, it bursts.", "[short pause] [emphasized]"),
        ("The only external force", "[short pause]"),
        ("That holds until", "[pause]"),
    ],
    "08": [
        ("So if the net external", "[short pause] [emphasized]"),
        ("Let's see it", "[pause]"),
        ("Now they collide.", "[pause] [curious]"),
        ("But the centre of mass doesn't", "[short pause] [emphasized]"),
    ],
    "09": [
        ("To capture that,", "[short pause]"),
        ("Which way out?", "[pause] [curious]"),
        ("And order matters.", "[pause] [emphasized]"),
    ],
    "10": [
        ("Curl the fingers", "[short pause]"),
        ("Now pick a point", "[pause] [curious]"),
        ("Every particle of a rigid", "[short pause] [emphasized]"),
    ],
    "11": [
        ("Push near the handle,", "[short pause]"),
        ("There's another way", "[pause] [curious]"),
        ("Push straight toward", "[short pause] [emphasized]"),
        ("Let's put numbers", "[pause]"),
    ],
    "12": [
        ("Add them as vectors,", "[short pause]"),
        ("But both forces", "[short pause] [emphasized]"),
        ("So zero net force", "[pause] [warmly]"),
    ],
    "13": [
        ("Equilibrium doesn't have", "[pause] [curious]"),
        ("Here's a seesaw.", "[pause]"),
        ("But balancing torques", "[short pause] [emphasized]"),
        ("Move the lighter", "[pause] [curious]"),
    ],
    "14": [
        ("Rotation adds a twist.", "[short pause] [curious]"),
        ("Why? In the ring,", "[short pause]"),
        ("Notice the square.", "[short pause] [emphasized]"),
        ("The mass hasn't changed", "[pause] [emphasized]"),
    ],
    "15": [
        ("Line up the round", "[pause]"),
        ("Compare the ring", "[short pause] [curious]"),
        ("How much mass matters.", "[pause] [warmly]"),
    ],
    "16": [
        ("Imagine gathering", "[short pause] [curious]"),
        ("The mass isn't really", "[pause]"),
    ],
    "17": [
        ("First, the parallel", "[short pause]"),
        ("Notice that among", "[short pause] [curious]"),
        ("Second, the perpendicular", "[pause]"),
        ("Two simple theorems,", "[pause] [warmly]"),
    ],
    "18": [
        ("And time is still", "[short pause]"),
        ("When angular acceleration", "[short pause]"),
        ("Same structure, new", "[pause] [warmly]"),
    ],
    "19": [
        ("How fast is it", "[short pause] [curious]"),
        ("Watch it for four", "[short pause]"),
        ("Not quite three", "[pause] [warmly]"),
    ],
    "20": [
        ("No. A particle", "[short pause] [emphasized]"),
        ("The tangential part", "[short pause]"),
        ("As the wheel spins faster,", "[pause] [curious]"),
    ],
    "21": [
        ("Multiply both sides", "[short pause]"),
        ("Tau net equals", "[pause] [emphasized]"),
        ("Bigger torque,", "[short pause] [warmly]"),
    ],
    "22": [
        ("Alpha equals tau", "[short pause]"),
        ("That's exactly the angular", "[pause] [curious]"),
    ],
    "23": [
        ("In its particles.", "[short pause]"),
        ("K rot equals", "[pause] [emphasized]"),
        ("Where did those", "[pause] [curious]"),
        ("The work-energy principle", "[pause] [warmly]"),
    ],
    "24": [
        ("Even a particle moving", "[short pause] [curious]"),
        ("Now a rigid body.", "[pause]"),
        ("About that same fixed origin,", "[pause] [emphasized]"),
        ("Force changes linear", "[short pause] [warmly]"),
    ],
    "25": [
        ("Here's a skater,", "[pause]"),
        ("Now the skater pulls", "[short pause] [curious]"),
        ("But here's a puzzle.", "[pause] [curious]"),
        ("From the skater.", "[short pause] [emphasized]"),
        ("Angular momentum conserved.", "[pause] [warmly]"),
    ],
    "26": [
        ("Rolling without slipping means", "[short pause]"),
        ("Add them.", "[short pause] [emphasized]"),
        ("Momentarily.", "[pause] [curious]"),
    ],
    "27": [
        ("That bracket decides", "[short pause] [emphasized]"),
        ("Same mass, same radius, same speed", "[pause] [curious]"),
    ],
    "28": [
        ("Pause, and make", "[pause] [curious]"),
        ("Here's the race.", "[short pause] [excited]"),
        ("Energy explains why.", "[pause]"),
        ("Static friction supplies", "[short pause] [emphasized]"),
        ("And a block sliding", "[short pause] [curious]"),
        ("Mass and radius cancel", "[pause] [warmly]"),
    ],
    "29": [
        ("We began with one", "[warmly]"),
        ("Then everything followed", "[short pause]"),
        ("Newton's laws didn't", "[pause] [emphasized]"),
        ("Push a box on ice,", "[pause] [warmly]"),
    ],
    "30": [
        ("Thanks for watching.", "[warmly]"),
    ],
}
