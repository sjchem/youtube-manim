"""Narration source: continuous spoken prose, cut into visual beats.

Each beat is ``(spoken text, visual hold in seconds)``. A beat's window is the
time its words take at ``PACE`` words per second (a little slower than the
narrator's natural ~2.86 words per second, so the voice never races the
picture), plus the hold: extra seconds for a 3D move, a derivation step, a
live simulation or a prediction countdown. Beat start times and scene lengths
are *derived* from these windows, so ``config.SCENE_DURATIONS`` always
matches the script.

Scenes hold on a beat with ``common.beat(scene, t, i)``. Export joins the prose
for a voice recording and writes cue sheets separately
(``python -m utils.narration_export``).

Every number spoken here is checked against the model by
``python -m utils.rotation_data`` — change a value in
``utils/physics_models.py`` and the check names the line that no longer agrees.

Spelling for the cloned voice: numbers are written out in words, symbols as
they are read aloud ("tau equals I alpha", "r cross F", "x c m").
"""

from __future__ import annotations

import re

PACE = 2.65           # words per second used to size each beat's window
TRANSITION = 0.55     # closing fade of every scene, seconds
# Holds below are written as relative weights; this one factor tunes the whole
# film toward the brief's 140-150 words per finished minute while keeping
# every live demo, derivation step and countdown a real visual pause.
HOLD_SCALE = 0.7
MIN_HOLD = 0.6
_WORD = re.compile(r"[A-Za-z0-9']+")


def words(line: str) -> int:
    return len(_WORD.findall(line))


TITLES: dict[str, str] = {}
SCRIPT: dict[str, list[tuple[float, str]]] = {}
HOLDS: dict[str, list[float]] = {}
DURATIONS: dict[str, float] = {}


def _scene(key: str, title: str, beats: list[tuple[str, float]]) -> None:
    TITLES[key] = title
    t = 0.0
    out: list[tuple[float, str]] = []
    holds = []
    for text, weight in beats:
        hold = max(MIN_HOLD, round(weight * HOLD_SCALE, 2))
        holds.append(hold)
        out.append((round(t, 1), text))
        t = round(t, 1) + words(text) / PACE + hold
    SCRIPT[key] = out
    HOLDS[key] = holds
    DURATIONS[key] = round(t + TRANSITION, 1)


# ---------------------------------------------------------------------------
# Chapter 1 — From particles to extended bodies
# ---------------------------------------------------------------------------

_scene("01", "One push, three motions", [
    ("Push a box across smooth ice, and it slides. Every part of it moves together, in a straight line.", 1.4),
    ("Now give the same push to a door. It doesn't slide at all. It swings around its hinges.", 1.4),
    ("Give it to a cylinder on a floor with enough grip, and something stranger happens. It rolls: it moves forward, and it spins, at the same time.", 1.6),
    ("Same push. Three completely different motions.", 1.6),
    ("In the last episode, we followed a single particle around a circle. But a door is not a particle. Neither is a wheel, or a spinning top. They have size and shape. They are made of countless particles, all moving together.", 1.2),
    ("So why can the same force make one object move in a straight line, another rotate, and a third do both?", 1.8),
    ("To answer that, we need four new ideas: the centre of mass, torque, moment of inertia, and angular momentum.", 1.0),
    ("This is System of Particles and Rotational Motion.", 4.2),
])

_scene("02", "From particles to rigid bodies", [
    ("When we throw a ball, we usually treat it as a point. A point has mass, but no size. To trace the ball's path through the air, that is often all we need.", 1.2),
    ("But try that with a spinning wheel. A point near the axle sweeps a tiny circle. A point on the rim travels much farther, in the same time. One dot can't describe both.", 1.6),
    ("So we treat the wheel as an extended body: many particles, at many different positions.", 0.8),
    ("And we make one simplifying assumption. The distance between any two particles never changes. The body doesn't stretch, bend or squash. We call it a rigid body.", 1.6),
    ("Real materials do deform a little. But when that deformation is tiny, the rigid model works remarkably well.", 0.8),
    ("A rigid body can move in three ways. In pure translation, every particle has the same velocity. The body shifts, but never turns.", 1.4),
    ("In fixed-axis rotation, points away from the axis move on circles. Points on the axis stay still. Farther out means faster.", 1.4),
    ("And in rolling, it does both at once.", 1.6),
    ("So to describe an extended body, knowing where it is isn't enough. We also need to know how it is turned, and how that is changing. Let's start with the first part. Where is it?", 1.4),
])

# ---------------------------------------------------------------------------
# Chapter 2 — Centre of mass
# ---------------------------------------------------------------------------

_scene("03", "Two masses, one balance point", [
    ("Take two particles on a light rod. Where would you hold the rod, so that it balances?", 1.8),
    ("If the masses are equal, the answer is easy: exactly halfway between them.", 1.4),
    ("Now make one of them three times heavier. Hold the rod at the middle, and it tips. The balance point has moved toward the heavier mass.", 1.8),
    ("In uniform gravity, the balance point is the centre of mass. For two particles on a line, it's a weighted average of their positions.", 1.0),
    ("x c m equals m one x one, plus m two x two, all divided by m one plus m two.", 2.2),
    ("Each position is weighted by its mass. A heavier particle pulls the average toward itself.", 1.0),
    ("Let's try it. A two kilogram mass sits at zero. A six kilogram mass sits at four metres.", 1.4),
    ("Two times zero, plus six times four, is twenty-four. Divide by the total mass, eight kilograms, and the centre of mass is at three metres.", 2.2),
    ("One metre from the heavy mass, three metres from the light one. The distances are in the inverse ratio of the masses.", 1.8),
])

_scene("04", "Where is the centre of mass?", [
    ("Is the centre of mass always at the geometric centre of an object?", 1.4),
    ("For a uniform, symmetric body, it is. A uniform sphere, a uniform disc, a uniform straight rod: their centres of mass sit right at their centres.", 1.6),
    ("Symmetry does the work. For every bit of mass on one side, there is a matching bit on the other.", 1.2),
    ("But spread the mass unevenly, like a hammer with a heavy iron head, and the centre of mass shifts toward the heavy end.", 1.6),
    ("It can even lie where there is no material at all. A uniform ring has its centre of mass at the centre of the hole, in empty space.", 2.0),
    ("So the centre of mass isn't decided by geometry alone. It's decided by how the mass is distributed.", 1.2),
    ("Now toss the hammer. It tumbles in a complicated way. But watch only the centre of mass. Ignoring air resistance, it traces a smooth parabola, just like a thrown ball.", 3.0),
    ("Hold on to that. It's a clue to why the centre of mass matters so much.", 1.2),
])

_scene("05", "Many particles, one point", [
    ("Real objects contain far more than two particles. So let's scale up.", 0.8),
    ("Give each particle a mass, m i, and a position vector, r i, measured from an origin.", 1.4),
    ("The total mass, capital M, is the sum of all the masses.", 0.8),
    ("The centre of mass is the mass-weighted average of all the position vectors. R c m equals one over M, times the sum of m i r i.", 2.4),
    ("Each particle pulls the average toward itself, in proportion to its mass.", 1.2),
    ("This one vector equation is really three equations: x, y and z, each a weighted average on its own.", 1.8),
    ("And it doesn't matter where we put the origin. Move it, and every position vector changes. But the centre of mass stays at the same physical point.", 2.0),
    ("A real solid contains an enormous number of atoms. So instead of counting them, we treat the mass as smoothly spread out.", 1.4),
    ("Each tiny piece of mass, d m, sits at its own position r. The sum becomes an integral. R c m equals one over M, times the integral of r d m.", 2.4),
    ("From two beads to a solid body, it's the same idea. But the real power of the centre of mass appears when things start to move.", 1.4),
])

# ---------------------------------------------------------------------------
# Chapter 3 — Motion of the centre of mass and linear momentum
# ---------------------------------------------------------------------------

_scene("06", "Internal forces cancel", [
    ("Here are five particles, joined by springs. Each one pushes and pulls on its neighbours.", 1.4),
    ("Forces between particles of the system are internal forces. Forces from outside the system are external forces.", 1.2),
    ("Look at the internal forces. They come in pairs. If one particle pulls on another, the other pulls back, equally hard, in the opposite direction. That's Newton's third law.", 2.0),
    ("Now write Newton's second law for every particle. m i a i equals the net force on it.", 1.4),
    ("Add them all up. On the right, we get all the external forces, plus all the internal forces.", 1.2),
    ("But the internal forces come in equal and opposite pairs. In the sum, every pair cancels.", 1.8),
    ("And on the left, the sum of m i a i is exactly the total mass times the acceleration of the centre of mass.", 1.2),
    ("So the net external force equals M times a c m.", 2.4),
    ("Let's test it. Push on just one particle, with a steady force. The springs stretch, the cluster wobbles and turns. But the centre of mass accelerates smoothly, in a straight line, as if all the mass sat at that one point.", 4.0),
    ("One caution. This law tells us how the centre of mass moves. It doesn't say the point of application is irrelevant. Push somewhere else, and the body turns differently. That's the job of torque, which is coming soon.", 1.8),
])

_scene("07", "The exploding firework", [
    ("Here's a dramatic test. A firework shell is launched. Ignoring air resistance, it follows a parabola.", 1.8),
    ("At the top, it bursts. Fragments fly in every direction.", 2.4),
    ("The burst forces are internal. They push the fragments apart, but in equal and opposite pairs.", 1.2),
    ("The only external force is still gravity, the same total pull as before. So the centre of mass of all the fragments carries on along the original parabola, as if nothing had happened.", 3.2),
    ("That holds until a fragment hits the ground. Then the ground pushes on it, a new external force, and the centre of mass leaves the parabola.", 2.4),
    ("Internal forces can rearrange a system. Only external forces can change the motion of its centre of mass.", 1.8),
])

_scene("08", "The momentum of a system", [
    ("The total linear momentum of a system is the sum of the momenta of its particles. P equals the sum of m i v i.", 1.2),
    ("Take the time derivative of the centre of mass equation, and that same sum appears: it equals M times v c m. The total momentum is just the total mass, moving with the centre of mass.", 1.8),
    ("And Newton's second law for the whole system becomes: d P by d t equals the net external force.", 1.2),
    ("So if the net external force is zero, the total momentum stays constant. That's conservation of linear momentum.", 1.2),
    ("Let's see it on a frictionless track. A two kilogram cart moves right at three metres per second. A three kilogram cart moves left at one metre per second.", 1.4),
    ("Taking right as positive, the total momentum is two times three, plus three times minus one. That's three kilogram metres per second.", 1.8),
    ("Divide by the total mass, five kilograms. The centre of mass moves right at zero point six metres per second.", 1.8),
    ("Now they collide. The bumper pushes the carts apart, and their velocities change completely.", 3.2),
    ("But the centre of mass doesn't even flinch. It keeps gliding at zero point six metres per second, because the collision forces are internal.", 2.4),
])

# ---------------------------------------------------------------------------
# Chapter 4 — Vector product
# ---------------------------------------------------------------------------

_scene("09", "The cross product", [
    ("So far, adding and scaling vectors has been enough. But rotation needs a new tool. A force can turn things, and the turning depends on where the force acts, and in which direction.", 1.2),
    ("To capture that, we need a new way to multiply two vectors: the cross product.", 0.8),
    ("Take two vectors, A and B, with an angle theta between them. Their cross product, A cross B, is a new vector.", 1.6),
    ("Its magnitude is A B sine theta. That's the area of the parallelogram the two vectors span.", 1.8),
    ("For a nonzero cross product, its direction is perpendicular to both vectors, standing out of their plane.", 1.8),
    ("Which way out? Use your right hand. Curl your fingers from the first vector toward the second, through the smaller angle. Your thumb points along A cross B.", 2.4),
    ("Watch the angle. When the vectors are perpendicular, the parallelogram is largest, and so is the cross product: A times B.", 1.8),
    ("Close the angle, and the parallelogram flattens. Parallel vectors give zero. Turn one directly opposite to the other, and the cross product is also zero.", 1.8),
    ("And order matters. B cross A points the opposite way. B cross A equals minus A cross B.", 2.0),
    ("A perpendicular direction, and the sine of the angle. These two features are exactly what we need to describe rotation.", 1.2),
])

_scene("10", "Angular velocity as a vector", [
    ("In episode two, we met angular velocity, omega: how fast an angle changes.", 1.0),
    ("For rotation about a fixed axis, omega can also be a vector. It points along the axis.", 1.4),
    ("Curl the fingers of your right hand the way the body turns. Your thumb points along omega. Spin it the other way, and omega flips.", 2.6),
    ("Now pick a point on the rotating body, at position r, measured from a point on the axis. Its velocity is omega cross r.", 1.6),
    ("The cross product gives the right direction automatically: tangent to that point's circle.", 1.8),
    ("And it gives the right size: omega times the point's perpendicular distance from the axis. That's the same v equals r omega from episode two.", 1.8),
    ("Every particle of a rigid body shares the same omega. But their velocities differ. A particle twice as far from the axis moves twice as fast.", 2.4),
    ("So the cross product links position, velocity and rotation. Next, it will link force and rotation.", 1.2),
])

# ---------------------------------------------------------------------------
# Chapter 5 — Torque and equilibrium
# ---------------------------------------------------------------------------

_scene("11", "Torque: why doors have handles", [
    ("Why is a door easier to open at the handle than near its hinges?", 1.2),
    ("Push near the handle, and the door swings easily. Push with the same force near the hinges, and it barely moves.", 2.4),
    ("The turning effect of a force is called torque, or moment of force. And it depends on more than the force alone.", 1.0),
    ("Torque is r cross F. Here r is the position of the point where the force acts, measured from the axis, and F is the force.", 1.8),
    ("Its size is r F sine theta, where theta is the angle between r and F.", 1.8),
    ("There's another way to see it. Extend the force into a line, its line of action. The perpendicular distance from the axis to that line is the lever arm. Torque equals F times the lever arm.", 2.4),
    ("Push straight toward the hinge, and the line of action passes right through the axis. The lever arm is zero. That push cannot start the door turning from rest.", 2.0),
    ("Let's put numbers on it. Push perpendicular to the door with twenty newtons, zero point eight metres from the hinges. The torque is twenty times zero point eight: sixteen newton metres.", 1.8),
    ("Same push, only zero point two metres from the hinges: four newton metres. The same force gives four times less torque, because the lever arm is four times shorter.", 2.2),
])

_scene("12", "A couple: turning without moving", [
    ("Can the net force on an object be zero, and yet it still starts to turn?", 1.4),
    ("Apply two equal forces, in opposite directions, along two different parallel lines.", 1.4),
    ("Add them as vectors, and they cancel. The net force is zero, so the centre of mass doesn't accelerate.", 1.8),
    ("But both forces turn the bar the same way. Their torques add. The bar starts to spin, right where it is.", 2.6),
    ("This pair is called a couple. If the lines of action are a distance d apart, the torque of the couple is F times d, about any point you choose.", 2.0),
    ("You apply a couple every time you turn a steering wheel, or twist open a jar lid.", 1.8),
    ("So zero net force doesn't mean nothing happens. To describe a rigid body completely, we need both force and torque.", 1.8),
])

_scene("13", "Equilibrium: the balanced seesaw", [
    ("When is a rigid body in mechanical equilibrium? It needs two separate conditions.", 1.0),
    ("First, translational equilibrium. The external forces must add up to zero, so the centre of mass doesn't accelerate.", 1.4),
    ("Second, rotational equilibrium. For our rigid bodies about a fixed axis, zero net torque about that axis means zero angular acceleration.", 1.4),
    ("Equilibrium doesn't have to mean rest. A gliding body can have zero net force. A symmetric disc can spin steadily with zero net torque. If a body starts at rest and both conditions hold, it stays at rest. That's static equilibrium.", 1.6),
    ("Here's a seesaw. A child weighing one hundred newtons sits two metres to the left of the pivot.", 1.2),
    ("On the right, a heavier child, two hundred newtons, sits just one metre from the pivot.", 1.4),
    ("Left side: one hundred times two, two hundred newton metres, counterclockwise. Right side: two hundred times one, two hundred newton metres, clockwise.", 1.8),
    ("Taking counterclockwise as positive, the net torque is two hundred minus two hundred: zero. The torques balance.", 1.8),
    ("But balancing torques isn't the whole story. The children push down with three hundred newtons in total. If the seesaw's own weight is negligible, the pivot must push up with three hundred newtons.", 1.8),
    ("Three hundred up, minus one hundred, minus two hundred: zero. Forces balance, and torques balance. That's mechanical equilibrium.", 1.8),
    ("Move the lighter child a little closer to the pivot, and the torques no longer balance. The seesaw tips.", 3.0),
])

# ---------------------------------------------------------------------------
# Chapter 6 — Moment of inertia
# ---------------------------------------------------------------------------

_scene("14", "Why mass isn't enough", [
    ("In linear motion, mass measures how hard it is to change an object's velocity. Same force, bigger mass, smaller acceleration.", 1.2),
    ("Rotation adds a twist. Here are a thin ring and a solid disc, with the same mass and the same radius.", 1.4),
    ("Apply the same torque to both. The disc spins up faster. The ring resists more.", 3.0),
    ("Why? In the ring, all the mass sits at the rim. In the disc, much of it lies close to the axis.", 1.6),
    ("Resistance to changes in rotation is measured by the moment of inertia, I. For particles, I equals the sum of m i, times r i perpendicular, squared.", 1.8),
    ("Here r perpendicular is each particle's distance from the axis. For a continuous body, the sum becomes the integral of r squared d m. The unit is the kilogram metre squared.", 1.6),
    ("Notice the square. Mass far from the axis counts much more than mass close in.", 1.4),
    ("Take two one kilogram masses on a light rod, each one metre from the axis. I equals one times one squared, plus one times one squared: two kilogram metres squared.", 1.8),
    ("Now slide both masses out to two metres. I equals one times four, plus one times four: eight kilogram metres squared.", 2.0),
    ("The mass hasn't changed at all. But the moment of inertia is four times larger. Apply the same torque, and the spread-out version picks up speed four times more slowly.", 3.0),
])

_scene("15", "A gallery of shapes", [
    ("Moment of inertia depends on three things: the shape of the body, how its mass is distributed, and which axis it turns about.", 1.2),
    ("A thin ring, about its central axis: M R squared. Every bit of its mass is at distance R.", 1.8),
    ("A uniform solid disc: one half M R squared. A solid cylinder about its long axis: also one half M R squared. Its length doesn't change the answer.", 2.0),
    ("A uniform solid sphere, about a diameter: two fifths M R squared. A thin spherical shell: two thirds M R squared.", 2.0),
    ("A thin uniform rod of length L, about its middle: one twelfth M L squared. About one end: one third M L squared.", 2.0),
    ("Line up the round bodies by how far their mass sits from the axis, and the pattern is clear. The more mass near the rim, the larger the moment of inertia.", 2.0),
    ("Compare the ring and the disc. With equal mass and radius, the ring's moment of inertia is twice the disc's. Its mass lies farther from the axis, on average.", 2.2),
    ("How much mass matters. But where the mass sits can matter just as much.", 1.8),
])

_scene("16", "Radius of gyration", [
    ("Sometimes we want to sum up a whole mass distribution with a single length.", 1.0),
    ("Imagine gathering all of a body's mass into a thin ring around the axis, at a distance k. Choose k so the moment of inertia stays the same. That distance is the radius of gyration.", 2.4),
    ("I equals M k squared. So k equals the square root of I over M.", 1.8),
    ("For a thin ring, the mass is already at the rim. k equals R.", 1.4),
    ("For a solid disc, I is one half M R squared. So k is R over root two: about zero point seven one R.", 2.4),
    ("The mass isn't really there. The radius of gyration is a bookkeeping distance. But it tells you at a glance that the disc's mass sits closer to the axis than the ring's.", 1.8),
])

_scene("17", "Two axis theorems", [
    ("Calculating a moment of inertia from scratch can take serious integration. Fortunately, two theorems often save the work.", 1.0),
    ("First, the parallel axis theorem. If you know the moment of inertia about an axis through the centre of mass, you can find it about any parallel axis.", 1.4),
    ("I equals I c m plus M d squared, where d is the distance between the two axes.", 1.8),
    ("Take a uniform rod. About its centre, I is one twelfth M L squared. Now move the axis to one end, a distance L over two away.", 1.8),
    ("Add M times L over two, squared: one quarter M L squared. One twelfth plus one quarter is one third. So about the end, I is one third M L squared, just as the table said.", 2.6),
    ("Notice that among parallel axes, the one through the centre of mass always gives the smallest moment of inertia. Shift the axis anywhere, and you only add M d squared.", 1.8),
    ("Second, the perpendicular axis theorem. It works only for flat, planar bodies.", 1.0),
    ("Use perpendicular x and y axes in the lamina, and a z axis through their common intersection. Then I z equals I x plus I y.", 1.8),
    ("For a uniform disc, I z is one half M R squared. By symmetry, I x equals I y. So each is one quarter M R squared: the moment of inertia about a diameter.", 2.6),
    ("Two simple theorems, and one big lesson. Moment of inertia depends on which axis you choose.", 1.4),
])

# ---------------------------------------------------------------------------
# Chapter 7 — Rotational kinematics
# ---------------------------------------------------------------------------

_scene("18", "Rotation's equations of motion", [
    ("Now that we know what resists rotation, let's predict the rotation itself.", 0.8),
    ("For straight-line motion, we track position, velocity and acceleration. For rotation about a fixed axis, each one has a partner.", 1.4),
    ("Position x becomes the angle theta. Velocity v becomes angular velocity omega, the rate of change of theta. Acceleration a becomes angular acceleration alpha, the rate of change of omega.", 2.4),
    ("And time is still just time.", 1.0),
    ("When angular acceleration is constant, angular velocity changes by alpha t. Add that change to the initial spin: omega equals omega zero plus alpha t.", 2.0),
    ("The angle reached is theta zero, plus omega zero t, plus one half alpha t squared. The initial spin and the acceleration each contribute to the angle turned.", 2.0),
    ("The third equation links speed and angle without time: omega squared equals omega zero squared, plus two alpha times theta minus theta zero.", 2.4),
    ("Same structure, new symbols. Everything you know about uniformly accelerated motion now works for rotation.", 1.4),
])

_scene("19", "A wheel spins up", [
    ("Let's use them. A wheel starts from rest, and speeds up with a constant angular acceleration of two radians per second squared.", 1.2),
    ("How fast is it turning after four seconds? And how far has it turned?", 1.4),
    ("Watch it for four seconds.", 5.0),
    ("Omega equals zero, plus two times four: eight radians per second.", 1.8),
    ("The angle turned is zero, plus one half, times two, times four squared: sixteen radians.", 1.8),
    ("One revolution is two pi radians. So sixteen radians is sixteen divided by two pi: about two point five five revolutions.", 2.2),
    ("Not quite three full turns. The counter agrees.", 2.0),
])

_scene("20", "One spin, many motions", [
    ("In fixed-axis rotation, every particle shares the same omega and alpha. But do they share the same linear motion?", 1.2),
    ("No. A particle at perpendicular distance r from the axis moves with speed r omega. Farther out means faster.", 1.6),
    ("When the spin speeds up, each particle also gains speed along its path. That's the tangential acceleration: a t equals r alpha.", 1.8),
    ("And because each particle moves on a circle, it also needs an inward, radial acceleration: a r equals r omega squared.", 1.8),
    ("The tangential part changes the speed. The radial part changes the direction.", 1.6),
    ("The two parts are perpendicular. Add them as vectors. Their magnitudes form a right triangle, so Pythagoras gives the total acceleration.", 2.2),
    ("As the wheel spins faster, the radial part grows like omega squared, and soon dominates.", 3.0),
    ("One rigid body, one omega. But each particle has its own speed and its own acceleration, set by its distance from the axis.", 1.8),
])

# ---------------------------------------------------------------------------
# Chapter 8 — Rotational dynamics
# ---------------------------------------------------------------------------

_scene("21", "Newton's second law for rotation", [
    ("Now we can connect torque and moment of inertia.", 0.8),
    ("Focus on one particle of a rotating body, at distance r from the axis. Only the tangential part of the force on it can change its speed around the circle.", 1.4),
    ("Newton's second law along the tangent: F t equals m a t. And a t is r alpha. So F t equals m r alpha.", 2.0),
    ("Multiply both sides by r. On the left, r F t is the torque on that particle. On the right, m r squared alpha.", 2.0),
    ("Now add over every particle. They all share the same alpha, so it comes out of the sum.", 1.4),
    ("On the right, the sum of m r squared is the moment of inertia. On the left, the torques of our central internal forces cancel, leaving the net external torque about the fixed axis.", 1.8),
    ("Tau net equals I alpha. Newton's second law for a rigid body about a fixed axis, with constant moment of inertia.", 2.4),
    ("Torque plays the role of force. Moment of inertia plays the role of mass. Angular acceleration plays the role of acceleration.", 1.8),
    ("Bigger torque, faster spin-up. Bigger moment of inertia, slower spin-up. Alpha equals tau over I.", 1.8),
])

_scene("22", "Spinning up a disc", [
    ("Let's try it on a real object. A uniform solid disc, with mass four kilograms and radius zero point five metres, turns on a frictionless axle through its centre.", 1.4),
    ("Its moment of inertia is one half M R squared: one half, times four, times zero point five squared. That's zero point five kilogram metres squared.", 2.4),
    ("A string wrapped around the rim pulls with a steady two newtons. At a radius of zero point five metres, that's a net torque of one newton metre.", 1.6),
    ("Alpha equals tau over I: one divided by zero point five. Two radians per second squared.", 1.8),
    ("That's exactly the angular acceleration of our spinning wheel. So after four seconds, this disc is also turning at eight radians per second, having swept through sixteen radians. Dynamics gives us alpha. Kinematics does the rest.", 3.0),
])

_scene("23", "Rotational energy and work", [
    ("A spinning disc isn't going anywhere. Its centre stays put. Yet it clearly carries energy. Where is it?", 1.4),
    ("In its particles. Every particle is moving, and each has kinetic energy, one half m i v i squared.", 1.4),
    ("For rotation about a fixed axis, v i equals r i omega. So each particle has one half m i r i squared omega squared.", 2.0),
    ("Add them up. Omega is the same for all of them, so it comes out of the sum, and what's left inside is the sum of m r squared: the moment of inertia.", 1.8),
    ("K rot equals one half I omega squared. The rotational partner of one half M v squared.", 2.4),
    ("Back to our disc. I is zero point five, and after four seconds, omega is eight. So K equals one half, times zero point five, times eight squared: sixteen joules.", 2.4),
    ("Where did those sixteen joules come from? From the work done by the torque.", 1.0),
    ("A force does work through a distance. A torque does work through an angle. For a constant torque, W equals tau times delta theta.", 1.8),
    ("One newton metre, through sixteen radians: sixteen joules. Exactly the kinetic energy gained, starting from rest.", 2.4),
    ("For a torque that changes, W is the integral of tau d theta. And the rate of doing work, the power, is P equals tau omega. That's the language of motors, turbines and flywheels.", 1.8),
    ("The work-energy principle also governs rotation. The motion is angular, but work still measures energy transferred.", 1.4),
])

# ---------------------------------------------------------------------------
# Chapter 9 — Angular momentum and its conservation
# ---------------------------------------------------------------------------

_scene("24", "Angular momentum", [
    ("Linear momentum, m v, describes translation. What describes rotation?", 1.0),
    ("Choose an origin fixed in an inertial frame. A particle's angular momentum about it is L equals r cross p: position cross momentum.", 1.4),
    ("Its size is r p sine theta. Like torque, it's momentum times a lever arm.", 1.8),
    ("Even a particle moving in a straight line has angular momentum about a point beside its path. And if no force acts, the lever arm stays the same, so L stays constant.", 2.4),
    ("For a particle moving on a circle around the origin, the velocity is perpendicular to the radius. So L equals m r v. And since v equals r omega, L equals m r squared omega.", 2.2),
    ("Now a rigid body. Add up m r squared omega for all its particles, and we get I omega. For a body turning about a fixed symmetry axis, L equals I omega, pointing along the axis.", 2.0),
    ("For a general body on a fixed axis, only the component of L along that axis equals I omega. The full vector can tilt. The bearings then supply a sideways torque to keep the axis fixed.", 2.0),
    ("About that same fixed origin, the net external torque equals the rate of change of total angular momentum, when internal torques cancel. Tau equals d L by d t.", 2.0),
    ("Along a fixed axis, with I constant, the rate of change of axial angular momentum is I alpha. So tau equals I alpha follows.", 1.4),
    ("Force changes linear momentum. Torque changes angular momentum.", 2.0),
])

_scene("25", "The spinning skater", [
    ("If the net external torque is zero, then d L by d t is zero, and angular momentum stays constant. This is conservation of angular momentum.", 1.4),
    ("For rotation about a fixed symmetry axis, I omega stays constant. Make I smaller, and omega must grow.", 1.4),
    ("Here's a skater, spinning with arms stretched out. Moment of inertia: four kilogram metres squared. Angular speed: two radians per second.", 1.8),
    ("Angular momentum: four times two, eight kilogram metres squared per second.", 1.4),
    ("Now the skater pulls their arms in. The moment of inertia drops to two.", 3.4),
    ("The ice is nearly frictionless, so the external torque about the vertical axis is negligible. L stays at eight. So omega becomes eight over two: four radians per second. The spin doubles.", 2.4),
    ("But here's a puzzle. Before, the kinetic energy was one half, times four, times two squared: eight joules. After, one half, times two, times four squared: sixteen joules.", 2.4),
    ("The energy doubled. Where did the extra eight joules come from?", 1.8),
    ("From the skater. Replay the pull. Muscles pull inward while the arms move inward, doing positive work. Chemical energy becomes kinetic energy.", 1.8),
    ("Those internal forces redistribute angular momentum within the skater. Its total stays constant, while internal work changes the kinetic energy.", 1.6),
    ("Angular momentum conserved. Kinetic energy not. Two different conservation questions, with two different answers.", 2.4),
])

# ---------------------------------------------------------------------------
# Chapter 10 — Rolling motion
# ---------------------------------------------------------------------------

_scene("26", "Rolling: translation plus rotation", [
    ("Now let's put everything together. A wheel rolling along a road.", 1.0),
    ("Its centre moves forward. At the same time, the wheel turns about its centre. Rolling is translation plus rotation.", 1.4),
    ("Rolling without slipping means the wheel doesn't skid. The contact point has zero velocity relative to the ground. Using speeds, that links the motions: v c m equals R times the magnitude of omega.", 2.0),
    ("Let's build the velocity of each point. Translation gives every point the same forward velocity, v c m.", 1.8),
    ("Rotation about the centre adds a velocity tangent to the rim, of size R omega, which equals v c m.", 1.8),
    ("Add them. At the top, both point forward: two v c m. The top of the wheel moves twice as fast as its centre.", 2.0),
    ("At the bottom, they cancel. The contact point is momentarily at rest.", 1.8),
    ("Momentarily. A moment later, a new point touches the ground. Follow one point on the rim, and it traces a cycloid: stopping dead at every touch, racing at the top.", 3.6),
])

_scene("27", "The energy of rolling", [
    ("So a rolling body carries two kinds of kinetic energy.", 0.8),
    ("Its centre of mass moves: one half M v c m squared. And it rotates about its centre of mass: one half I c m omega squared.", 2.0),
    ("Rolling without slipping, omega equals v c m over R. Substitute, and factor out one half M v c m squared.", 2.0),
    ("K equals one half M v c m squared, times one plus I c m over M R squared.", 2.4),
    ("That bracket decides how the energy is shared. For a solid cylinder, I over M R squared is one half, so one third of its kinetic energy is rotation. For a ring, it's one, so half of its energy is rotation.", 2.8),
    ("Same mass, same radius, same speed, but different shares of energy. That has a surprising consequence on a slope.", 1.4),
])

_scene("28", "The race down the ramp", [
    ("A solid cylinder and a thin ring, with the same mass and the same radius, are released together at the top of a ramp. Both roll without slipping. Which reaches the bottom first?", 1.4),
    ("Pause, and make your prediction.", 3.6),
    ("Here's the race.", 5.0),
    ("The cylinder wins, clearly.", 1.0),
    ("Energy explains why. Both lose the same potential energy. But the ring must put half its kinetic energy into spinning, the cylinder only a third. So the cylinder has more left over for moving forward.", 1.8),
    ("Static friction supplies the turning torque. With enough grip, it prevents slipping and does no work at the stationary contact point. The acceleration is g sine beta, divided by one plus I c m over M R squared.", 2.0),
    ("For the cylinder: two thirds g sine beta. For the ring: one half g sine beta. On this thirty degree ramp, that's about three point two seven, versus two point four five metres per second squared.", 2.4),
    ("And a block sliding down a frictionless ramp, with no rotation at all, would beat them both, at g sine beta: four point nine metres per second squared.", 2.4),
    ("Mass and radius cancel out. The distribution of mass decides the race. Centre of mass, torque, moment of inertia and energy, all on one ramp.", 2.0),
])

# ---------------------------------------------------------------------------
# Chapter 11 — Scientific synthesis
# ---------------------------------------------------------------------------

_scene("29", "Translation and rotation, side by side", [
    ("We began with one question. Why can the same force make one object move in a straight line, another rotate, and a third do both?", 1.2),
    ("The centre of mass carries the translation. Its motion obeys F equals M a c m, whatever happens inside.", 1.4),
    ("The turning effect depends on where a force acts: torque, r cross F. And rotation is resisted by moment of inertia, set by where the mass sits.", 1.4),
    ("Then everything followed a familiar pattern. Theta, omega and alpha mirror x, v and a. Tau equals I alpha mirrors F equals M a. L equals I omega mirrors p equals M v. One half I omega squared mirrors one half M v squared.", 2.6),
    ("Work accumulates through distance or angle. With zero net external force, linear momentum is conserved. With zero net external torque, total angular momentum is conserved.", 1.8),
    ("Newton's laws didn't change. Energy is still energy. Momentum still matters. But once objects have size and shape, geometry joins the story: where the force acts, where the mass sits, and which axis it turns about.", 1.8),
    ("Forces decide how the centre of mass moves. Torques decide how the rotation changes. And moment of inertia connects the body's shape to its spin.", 2.2),
    ("Push a box on ice, and it slides. Hinges let a door turn. With enough grip, a cylinder rolls. The forces, supports and mass distribution explain each motion. Physics isn't only about how things move. It's about why they move the way they do.", 3.4),
])

_scene("30", "Stay curious", [
    ("Thanks for watching. Stay curious.", 4.4),
])
