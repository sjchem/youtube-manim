# What Does a Function Actually Do? — continuous narration

Each scene below is a continuous voiceover. Only the prose beneath each scene heading is spoken. Separate plain-text copies are in `assets/audio/scripts/`. Visual directions and edit notes live in `animation_plan.md`.

The picture targets 19:34, including the end card. These are editorial timing targets, not measured ElevenLabs speech durations. Generate one file per scene, listen for pronunciation and pauses, then align paragraph boundaries to the corresponding visual beats. Do not read the headings or timestamps aloud.

## Scene 01 — The universal translator

The mathematics of calculus, the equations of physics, and the neural networks behind AI all build on one idea. The function.

Symbols aside, watch what happens. Something goes in. A rule acts on it. Something comes out. For each specified input, one determined output.

Calculus, physics, statistics, machine learning, and AI all build on this idea.

A coin and a selection enter a working vending machine. Out comes your drink.

Ten degrees Celsius enters a converter. Fifty degrees Fahrenheit comes out.

An image enters a fixed neural network. In this example, it returns a ninety-eight percent cat score.

Different inputs. Different rules. The same structure. We will turn it into numbers, a table, and a graph. Later, we will connect machines, and even ask when we can run them backwards.

So, what does a function actually do?

## Scene 02 — Input, rule, output

This machine doubles whatever enters. Nothing is hidden. Its entire job is to multiply the input by two.

One goes in. Two comes out. Three goes in. Six comes out. Before the next number arrives, make a prediction. What should happen to five? Ten. Each answer follows from the same rule.

Keep a record of those inputs and outputs, and we get a table. The table records examples. The rule covers every allowed input.

Now let's give the rule a name. Call it f. Mathematicians write, f of x equals two x. This is the machine written in symbols.

The letter f names the rule. The letter x stands for the input. And f of x names the output for that input. For our doubling machine, that output equals two times x.

The parentheses tell us which input we are using. F of x does not mean f times x. It means the output of f when the input is x. The multiplication belongs to the rule on the other side of the equals sign.

So f of three asks what this machine gives back when three goes in. Replace x with three. Two times three is six. The box, the table, and the notation all agree. But there is one promise every function must keep.

## Scene 03 — Exactly one output

Watch the doubling rule one input at a time. One goes to two. Two goes to four. Three goes to six. Each row records one input and its answer. Every allowed input determines exactly one output. That is the promise a function keeps.

Focus on two. Four is its answer. Now add seven as another answer. Which output should we use?

That is not a function of the input we specified. One input has two outputs. Each allowed input must determine exactly one output. A real device may seem inconsistent because we left out an input, such as its settings or state.

Now consider a different rule: square the input. Negative two, multiplied by negative two, gives four. Positive two, multiplied by positive two, also gives four.

Is that a problem? No. Follow either input separately: each has exactly one answer. Different inputs may share an output. An individual input cannot split.

That shared answer will matter when we try to run the machine backwards. For now, keep the promise in mind: each allowed input determines exactly one output. But which inputs are we allowed to use?

## Scene 04 — Domain and range

Consider the area of a circle. Give the rule a radius, and it gives you an area. The area is pi times the radius squared. One radius determines one area.

Watch the circle grow. The gold dot tracks the radius. The green dot tracks the area on a separate scale. Doubling the radius makes the area four times as large. The output can change differently from the input.

Now try a radius of negative three metres. The algebra could square negative three, but a negative length does not describe a physical radius. For this model, it is not an allowed input.

The allowed inputs form the domain. Here we allow zero and every positive radius, with zero representing the limiting case of zero area.

The outputs actually reached form the range. Every area we produce is nonnegative. And every nonnegative area can be reached by choosing a suitable radius. So the range is zero and everything above it too.

The domain belongs to the function, along with the rule. Change the allowed inputs, and the outputs you can reach may change as well. That will help us later with inverses. For now, let's keep a record of the machine's answers and turn that record into a picture.

## Scene 05 — From machine to graph

Bring back the squaring machine. This time, allow every real number as an input. We will start with just five examples.

Negative two gives four. Negative one gives one. Zero gives zero. One gives one. Two gives four. Each journey becomes a row in our table.

Now look closely at one row. It contains two pieces of information: what went in, and what came out. We can write those as an ordered pair. Input first. Output second. So two going to four becomes the pair, two comma four.

Give those pairs a place on a coordinate plane. The horizontal direction records the input. The vertical direction records the output. Negative two and four means two units left and four units up. Negative one and one means one left and one up. Zero and zero sits at the origin. The positive inputs land to the right.

Now test inputs between our original five. More dots appear. The squaring rule also works for fractions and decimals, so the pattern keeps filling in.

Five dots alone would not tell us the whole rule. We can draw this smooth curve because we know the rule for every input between them. And the graph continues beyond our viewing window.

A graph is a picture of all the allowed input and output pairs. Every point says: this input gives this output. The machine, the table, and the curve describe the same relationship. That means the one-output promise should be visible in the graph itself.

## Scene 06 — The vertical line test

A vertical line holds the horizontal coordinate fixed. Wherever it meets our graph, it finds an output for that input.

Slide the line across the parabola. One crossing. One answer. At every input we inspect, the machine keeps its promise.

Now replace the parabola with this circle. Run the same scanner across it. In the middle, the line crosses twice. At x equals zero, the circle has a point at y equals two, and another at y equals negative two.

One input. Two different outputs. So the whole circle cannot be the graph of y as a function of x. Its upper and lower halves can each be graphed as separate functions.

This is the vertical line test: scan the graph and count intersections. Every vertical line may meet it at most once. No crossing means the input lies outside the domain. Two crossings mean one input has two outputs. Now that we can read a graph, let's see how editing the rule changes its shape.

## Scene 07 — Change the rule, change the shape

Return to the squaring rule and leave a grey copy of its graph behind. That copy gives us a reference for every change.

First, add two to every output. An answer of zero becomes two. An answer of one becomes three. The input stays where it was, while every output moves two units up. So the whole parabola rises. Reset it before the next experiment.

Now subtract two inside the function. We write f of x minus two. This changes what enters the original machine. It is tempting to expect a move to the left. Watch the lowest point instead.

The original machine gives its smallest output when it receives zero. The modified machine receives x minus two. To make that zero, x must equal two. So the new lowest point sits two units to the right.

Try another landmark. The old input one produced one. The new external input three sends one into the squaring machine, so it also produces one. Every old output now occurs two input units farther right. That explains the direction of the shift.

Reset again, and double every output. Follow the point whose input is one. Its output used to be one. Now it is two. The input stays fixed while the point moves vertically. Every output doubles, creating a vertical stretch. Multiplying the outputs by one half would compress the graph instead.

Finally, change the sign of every output. Positive heights become negative heights. The point at zero stays put. The graph reflects across the horizontal axis.

Upward shift. Rightward shift. Stretch. Reflection. Each movement follows from an operation on the inputs or outputs. We can even build these operations as separate machines. What happens when we connect them?

## Scene 08 — Connected machines

Here are two machines. The first adds two. Call it f. The second squares its input. Call it g. We will connect them so the first output becomes the second input.

Start with x. After the first machine, we have x plus two. That entire result enters the squaring machine. So the final output is x plus two, all squared.

We write this as g of f of x. Read the expression from the inside out. F acts first, then g acts on what f produced. This is composition.

Try a number. Three enters the first machine and becomes five. Five enters the second and becomes twenty-five. One journey, with an intermediate answer in the middle.

Now swap the machines. The squaring machine acts first. X becomes x squared. Then the other machine adds two, giving x squared plus two.

Test three again. Three becomes nine. Nine becomes eleven. Twenty-five in the first arrangement. Eleven in the second. The parts and starting input stayed the same, but the order changed the result.

The graphs connect this to our previous experiment. Adding two before squaring shifts this parabola left. Adding two afterwards shifts it up. Some pairs of functions do give the same result in either order, but we cannot assume that.

The small circle between g and f is another way to write composition: f first, then g. A connected machine also needs the first output to be an allowed input for the next. Now imagine choosing that next machine for a special purpose: undoing the first.

## Scene 09 — Running the machine backwards

Our doubling machine takes five and returns ten. What operation would take that ten back to five?

Divide by two. Send ten through the new machine, and five comes back. We have recovered the original input.

This new rule is the inverse of f. We write f with a small minus one above it, and read that as f inverse. Here, f of x is two x, and f inverse of x is x divided by two.

That notation means undo the function. It does not mean take the reciprocal of its output. For this example, halving x and taking one divided by two x are different operations.

Run f and then its inverse. Whatever input you started with comes back unchanged. The two machines cancel each other's action.

Now put the original rule on a square coordinate grid. Draw the diagonal line, y equals x, as a reference. Watch one point on the doubling graph: one comma two. It records one going in and two coming out.

The inverse reverses that journey. Two goes in and one comes out. Its graph therefore contains two comma one. The coordinates have swapped places.

The same reasoning works for every point. If the original sends a to b, the inverse sends b to a. Input and output exchange roles. On a grid with equal scales, swapping coordinates reflects a point across y equals x.

Reflect the whole line, and the graph of the inverse appears. The geometry follows directly from reversing the relationship. But we recovered five from ten because there was only one possible starting value. What if two different inputs had produced the same output?

## Scene 10 — When the way back is ambiguous

Remember the squaring machine. Positive two and negative two both give four. Going forward, each input still gives one output.

Now reverse the question. If four came out, what went in? Positive two? Negative two? The output does not preserve that distinction. We cannot define an inverse function that recovers every original real input.

The graph shows why. The horizontal line at four meets the parabola twice. It has found two different inputs for the same output. This is the horizontal line test for a one-to-one function: different inputs give different outputs.

We can change the situation by restricting the domain. Allow only zero and positive inputs. Fade away the negative half of the parabola. Now four can only have come from two.

Reflect the remaining half across y equals x. The inverse is the square-root function. It takes a nonnegative number and returns its nonnegative square root. The square root of four is two. Solving the equation x squared equals four still gives both positive and negative two.

An inverse works on the outputs the original function actually reaches. Restricting the inputs has made that return journey unambiguous. So far our graphs have used one numerical input at a time. What would change if one input contained two numbers?

## Scene 11 — One input pair, one height

Start with a curve again. Now tilt the camera. There is another direction available, stretching across the floor. The curve we were looking at is one slice of a larger surface.

Let an input contain two numbers, x and y. Together they form one ordered pair. The rule takes that pair and returns one number, z. We write z equals f of x and y.

Every location on the floor specifies an input pair. The height of the surface there records its output. Hold y fixed, and you see a curve. Allow y to vary as well, and all those slices form a landscape.

Pick one location. Follow the vertical marker to the surface. One input pair determines one height. The definition of a function has stayed the same.

This also gives us a picture of model training. Imagine the two coordinates are adjustable model settings, and height represents a loss: a score we want to reduce. This is an illustrative surface, not measurements from a real model.

The walker changes the settings by taking steps downhill. This method is called gradient descent. On this example, the steps approach a valley. Real training can involve millions of settings, and it is not guaranteed to find the lowest possible valley.

More coordinates make the picture harder to draw, but the relationship remains: an input, a rule, and an output. Let's return to the applications we promised at the beginning.

## Scene 12 — What functions unlock

Keep the same diagram and change its labels. In a model of motion, time is the input and position is the output. Specify the motion and its starting conditions, and each time determines a position.

Calculus asks how that position changes. Differentiation takes a suitable position function and produces a velocity function. A derivative describes local change. Integration lets us accumulate quantities over an interval. Both begin with a relationship between quantities.

In statistics, a probability model can take observed information and return the probability of an event. The outcome itself may be uncertain, while the model assigns one probability to the specified input.

In machine learning, an input can be a list of features. A trained model transforms those features into a prediction. A function can still make inaccurate predictions.

Now look at this feedforward neural network. Each layer applies a function and passes its output to the next. It is the composition diagram we built earlier, extended into a chain. With the model and inference settings fixed, that chain determines the prediction.

Calculus, physics, statistics, machine learning, and AI ask different questions. How does the output change? What can we predict? How should a model's settings change? Functions give us a common language for expressing those relationships. That is why this simple idea opens so many doors.

## Scene 13 — The idea behind the symbols

We began with input, rule, output. Then we named the rule f, the input x, and the output f of x.

A table recorded examples. A graph pictured the pairs. Composition connected rules. An inverse, when it existed, recovered the input from the output.

F of x is just a compact way of describing how one quantity determines another. The symbols let us carry that relationship into more complicated questions.

Whenever the notation feels unfamiliar, return to three questions. What is the input? What rule connects it to the output? And does each allowed input determine exactly one output?

Input. Rule. Output. That is a function.

## Scene 14 — Closing card

Thanks for watching. If this helped functions make sense, subscribe for more visual physics and mathematics. Stay curious, and keep asking what the symbols are telling you.
