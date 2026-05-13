# Narration Script

## Scene 01 - Hook

What if I told you that winning a tennis point about seventy percent of the time can make you win the entire service game more than ninety percent of the time?

That sounds like probability is giving the server extra credit. But it is not magic. It is the structure of tennis scoring.

Winning a point is not the same thing as winning a game. So where does the extra probability come from?

## Scene 02 - Service Point Probability

To understand the jump, we first calculate the chance of winning one service point.

A serve point has two main routes. The first serve goes in, and the server wins after that first serve. Or the first serve misses, the second serve goes in, and the server wins after the second serve.

For this Zverev example, the first serve lands in seventy-one point two percent of the time. He wins seventy-six point eight percent of those points. When the first serve misses, we assume the second serve lands in, and he wins fifty-four point eight percent of those points.

Multiplying along the branches and adding the routes gives about zero point seven zero four six. So the server wins a single point about seventy point four percent of the time.

## Scene 03 - Bernoulli Trial

Now we model each point as a Bernoulli trial.

The random variable X sub i is one if the server wins the point and zero if the server loses it. The running sum counts server points across the game.

The model is simple on purpose. It treats each point as independent with the same win probability p. Real tennis has momentum, fatigue, and tactics, but this clean model already explains a surprising amount.

## Scene 04 - Paths Before Deuce

Before deuce, there are three ways the server can win quickly.

A love game, four-zero, has probability p to the fourth.

A four-one game must end with a server point. The first four points contain exactly three server wins and one receiver win, so there are four paths. That gives four p to the fourth times one minus p.

A four-two game also ends with a server point. In the first five points, the server needs three wins and the receiver needs two. There are ten such paths, so the term is ten p to the fourth times one minus p squared.

Already, path counting is turning a point edge into a game edge.

## Scene 05 - Deuce Recursion

But tennis has one more twist: deuce.

At deuce, the server can win two points in a row and win the game. That has probability p squared.

The server can lose two points in a row and lose the game. Or the players can split two points, in either order, and return to deuce.

That loop is the key. If q is the probability of eventually winning from deuce, then q equals p squared plus two p times one minus p times q.

Solving the recursion gives q equals p squared divided by p squared plus one minus p squared.

## Scene 06 - Full Formula

Now we assemble the game.

The server can win four-zero, four-one, or four-two. Or the game reaches deuce at three-three after six points, and from there the server wins with the deuce probability.

That gives the full formula for G of p.

When p equals zero point seven zero four, G of p is about zero point nine zero six.

A seventy point four percent point edge compounds into a ninety point six percent game edge.

## Scene 07 - Graph

The graph shows why this feels so dramatic.

The dashed line is what would happen if game probability simply equaled point probability. But tennis scoring bends the curve.

At fifty percent, nothing is amplified. The game is still fifty-fifty.

At sixty percent, the server is already much more likely than sixty percent to hold.

And near seventy percent, the curve climbs into the ninety-percent range.

Small advantages do not stay small when the scoring system rewards repeated success.

## Scene 08 - Zverev Case Study

Now compare the model with the Zverev serving example.

Using first-serve percentage, first-serve points won, and second-serve points won, the estimated point win probability is about seventy point four percent.

The theoretical service-game win probability is about ninety point six percent.

The actual service-game win percentage is about ninety point two percent.

The simple model is not perfect, but it lands remarkably close.

## Scene 09 - Outro

So the story is this.

Tennis points can be modeled as Bernoulli trials. Tennis games are nonlinear probability machines. Deuce creates recursion. And small point-level advantages become huge game-level advantages.

Sports analytics is probability wearing sneakers.
