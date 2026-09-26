# Set Theory — the pizza story

Continuous narration for each scene. Speak only the prose beneath each heading.
The text exports in `assets/audio/scripts/` contain no production directions.

The revised animation is **21:56**, including a 48-second opening. The timing
marks below are visual targets, not measured ElevenLabs speech. Generate one
clip per scene using your own cloned voice, listen, then align the visual cues
to those recordings. Read naturally; do not stretch the voice to fill a scene.
Allow a short thinking pause at each viewer question. Pronounce De Morgan as
“duh MOR-gun”, A as “ay”, and U as “you”.

## 01 · One pizza for two friends — 00:00 → 00:48
Making a pizza is easy, until everyone wants something different. One friend wants no meat. Another wants no dairy. You are making one pizza to share, so which toppings can you use? Take a look before anything moves. The sausage has to go, and so does the cheese. But mushrooms, olives, onions, and peppers pass both requests. Now both friends can enjoy the same pizza. You have just made a mathematical decision: choosing what belongs by following a rule. That is where our story of set theory begins.

## 02 · Pack a fruit basket — 00:48 → 03:07
Before we return to the pizza, let us pack something simpler: a fruit basket. Here are an apple, a banana, a pizza slice, a strawberry, a carrot, and some grapes. We need a clear rule for what goes into the basket. Choose the fruit, and four objects move inside. The pizza and carrot stay outside. The collection we have selected is a set. Its membership is well defined: each object either belongs or does not. Let us call this fruit set A. Curly braces let us list its members. The list tells us what is in the collection without needing to draw a basket every time.

Look at the apple. It belongs to A, so we write apple, followed by the membership symbol, followed by A. That symbol means “is an element of.” The pizza does not belong. A line through the symbol changes the statement to “is not an element of.” These are simply two ways of answering the same question. Now keep the apple, banana, and grapes, and shuffle them around. Did their positions change? Yes. Did the members change? No. The set is still the same.

Repetition is similar. These three apple pictures repeat the same named element, apple. They do not represent three individually identified physical apples. Writing that name several times adds no new member. Apple and banana still give us two distinct elements. A set keeps track of membership, rather than order or repetition. Now write the basket as a set of named elements: A equals apple, banana, strawberry, and grapes in braces. For any object x in our collection, x belongs to A exactly when it passes the fruit rule. But what happens when a whole collection fits inside a larger one?

## 03 · Animal habitats and subsets — 03:07 → 05:04
Imagine a small animal park. Every animal we are considering belongs to the park's collection. Within it, we can select the mammals: the cat, tiger, dog, and whale. Inside the mammals, we can select the cat family, which includes both the domestic cat and the tiger. Every animal in this smallest collection is also in the middle collection and the largest one. That relationship is called being a subset.

To make the nesting easier to see, imagine three open lunchboxes standing in for the three collections. The smallest sits inside the middle one, and both sit inside the largest. Drop our cat into the smallest box. It has landed inside all three at once. The boxes model membership; mathematical sets do not need physical walls.

Now compare the two statements. One cat is an element of the mammals set. The entire cat-family set is a subset of mammals. Membership talks about an element; the subset relation talks about all the elements of a set. Can we reverse the second statement? Is every mammal a cat? The dog settles it. A dog is a mammal and is not a cat. One counterexample is enough to disprove that reversed subset claim. Here is the mathematical chain: the cat family C is a subset of mammals M, and M is a subset of the animal universe U. If x belongs to C, then x must belong to M. That is what the subset symbol promises.

## 04 · The empty lunchbox — 05:04 → 06:18
Our lunchbox contains an apple. Take the apple out, and what is left inside? No members at all. This gives us the empty set, written with the crossed oval. This symbol names the empty set; it is not a member inside it. Now compare the empty collection with a collection of fruit. Is the empty set a subset of the fruit set? To disprove a subset claim, we would need an element of the first set that is missing from the second. But there is nothing inside the empty set to examine. No counterexample can exist. This is why the empty set is a subset of every set. The reason concerns members, not the size of a box. In symbols, the empty set is a subset of A. There exists no x inside the empty set, so there is no member that could break the subset rule.

## 05 · The platypus problem — 06:18 → 07:58
Back at the animal park, we have two properties to organise. One habitat represents mammals. The other represents animals of egg-laying kinds. The dog and whale belong on the mammal side. The chicken and the snake shown here belong on the egg-laying side. Our snake represents an egg-laying kind; not every snake species lays eggs. So far, separate habitats seem to work.

Then the platypus arrives. It is a mammal, and platypuses also lay eggs. Where should it go? Give yourself a moment to decide. Putting it only on one side would hide the other membership. Instead, bring the two boundaries together. Their overlap makes room for both properties, and the platypus can sit inside both without being copied. This is the useful idea behind a Venn diagram. The boundaries show relationships between the rules. The shared region says that both rules are true. Our animal has one identity and two memberships. Now let us take that idea back to two friends choosing their pizza toppings. We can now state the rule without naming an animal. An element x belongs to the intersection of M and E exactly when x belongs to M and belongs to E. The platypus gave us one concrete x.

## 06 · Two pizza orders — 07:58 → 10:21
Our friends have written two topping orders. Order A asks for mushroom and olive. Order B asks for olive and pepper. Suppose we want a shopping list covering either order. We collect mushroom, olive, and pepper. Olive appears on both orders, but it only needs one entry in our set of topping names. This collection is the union of A and B. The cup-shaped symbol means union, and the rule is simple: belonging to either set is enough. Here, “or” includes belonging to both.

Now suppose the friends want a topping they both chose. That is a different question. Imagine checking the topping against two order stations. First it must appear on A, and then it must appear on B. Follow the mushroom. It passes the first station but fails the second, so it is not shared by both orders. Pepper fails the first station, even though it would pass the second. Olive passes both. It is the topping that both friends selected.

This shared collection is the intersection, written with the cap-shaped symbol. Union collects from either order. Intersection keeps only what is common to both. Notice that our symbols describe actions we already understand from shopping and sharing. If two orders had no topping in common, their intersection would be the empty set. That would still be a perfectly meaningful answer. Keep those two questions in mind as we change the objects from ingredients to numbers. Let x stand for any topping. The equation for union says x belongs to A union B exactly when it belongs to A or B, including both. The equation for intersection changes that or to and. These are membership tests that work for any sets, not just these two orders.

## 07 · Ten counters, two rules — 10:21 → 12:02
Here are ten counters, numbered one through ten. That is our universe for this puzzle. We will sort them by two rules: prime and even. A prime is a whole number greater than one with exactly two positive divisors, one and itself. An even number is divisible by two. Three, five, and seven belong on the prime side. Four, six, eight, and ten belong on the even side. One and nine belong to neither. We have left one counter waiting: the number two. Where should it go?

Two is prime, because its positive divisors are one and two. It is also even, so it belongs in the overlap. In fact, every larger even number has two as an additional divisor, which is why two is the only even prime. The intersection is the set containing two. Its cardinality, or number of members, is one. The vertical bars mean that we are counting members. For comparison, the union contains eight distinct numbers. It includes everything that passes either rule, counting two just once. The result can be read in two ways. Prime intersect even contains only two. Prime union even has eight members. The braces tell us which elements belong; the vertical bars tell us how many there are.

## 08 · What remains in the kitchen? — 12:02 → 13:54
Look at the toppings available in this kitchen. Our six choices are mozzarella, ricotta, mushroom, olive, onion, and pepper. This particular collection is our universe. Now select the dairy toppings. Mozzarella and ricotta go together. If we want everything in our universe that is not dairy, we keep the other four. That selection is the complement of the dairy set. We write a small c after the set's name.

The phrase “not dairy” hides a question: among which objects? Let us tilt the kitchen shelf into three dimensions and look beyond it. There may be apples, bananas, and pizza elsewhere, but they were not part of the six toppings we agreed to consider. They do not automatically enter the answer. The universe tells us the collection from which we are choosing. A universe need not be finite, but we must specify it.

Now keep the dairy set unchanged, but restrict the universe to those dairy toppings themselves. What belongs to the universe while being outside the dairy set? Nothing. The complement is now empty, even though the dairy set stayed the same. Complement means not in the selected set, but still in the universe. The general equation makes our shelf precise: the complement of D is U minus D. An element x belongs to the complement only when x is in U and x is not in D. Both conditions matter.

## 09 · Build the shared pizza — 13:54 → 15:42
We are ready to return to our two friends. One asks for no meat; the other asks for no dairy. This time, the available menu has eight toppings. Mozzarella and ricotta are dairy. Bacon and sausage are meat. Mushroom, olive, onion, and pepper are neither. Choose the toppings that meet both friends' requests before we reveal them.

Start with everything we need to exclude. Dairy or meat gives the union of the two unwanted collections. Now keep the rest of the available menu. That means taking the complement of the union. The cheese and meat disappear, leaving four toppings for our pizza: mushroom, olive, onion, and pepper. We removed the combined selection.

There is another way to check the same result. Take a mushroom and ask whether it is outside the dairy set. Yes. Then ask whether it is outside the meat set. Yes again. The other three surviving toppings pass both exclusions too. One route excludes the union. The other keeps both complements’ shared members. These are two recipes for exactly the same selection, which brings us to a famous mathematical law. Call the shareable toppings S. We can calculate S by taking the available menu U and removing dairy union meat. We can also calculate S by intersecting not dairy with not meat. Next, we will prove why those two descriptions always agree.

## 10 · Two recipes, one result — 15:42 → 18:01
The two pizzas have the same toppings, even though we described their selection in different ways. Let us give those recipes a diagram. A and B can now be any two subsets of the same universe. The first recipe begins with their union, everything inside either boundary. Taking the complement of that entire selection leaves the region outside both. That is the complement of A union B.

The second recipe starts with the complement of A, everything in the universe outside A. Then consider the complement of B, everything outside B. To pass both exclusions, an element must belong to both complements. Their intersection selects the region outside both original sets. It is the same region we found with the first recipe.

Imagine cutting those two selections into transparent stencils. We can separate them in space, tilt them, and slide one onto the other. Their shapes line up.

This is De Morgan's first law: the complement of a union equals the intersection of the complements. Neither dairy nor meat means not dairy and not meat. Logic uses the same pattern. Negating the whole statement “p or q” gives “not p and not q.” The whole statement is what the parentheses group together. Finally, follow one arbitrary element x. Being in the complement of A union B means x is outside A and outside B. That is exactly what it means for x to belong to both complements. Since this works for every x in U, the two sets are equal.

## 11 · The toy gate — 18:01 → 19:43
For the second law, imagine a toy gate with one exact rule: block a toy when it is red and square. Here are four toys: red or blue, square or round. Which can pass? The red square is blocked because it meets both conditions. The red ball passes because it is not square. The blue square passes because it is not red. The blue ball passes because it fails both blocking conditions.

To pass the gate, a toy therefore needs to be not red or not square. Either is enough, and satisfying both exclusions is allowed. Now draw red toys as one set and square toys as the other. The blocked region is their intersection. Its complement contains everything except that shared region. The same selection is the union of the two complements: outside the red set or outside the square set. That is De Morgan's second law. Negating “and” gives “or” between the negated conditions. Not both does not mean neither; a toy may still meet one of the original conditions. The same membership test proves the second law. If x is not in the intersection, then x fails membership in R or fails membership in S. So the complement of the intersection equals the union of the complements.

## 12 · One test connects every rule — 19:43 → 21:07
Choose a universe U and imagine testing one object, x, inside it. Every rule in this video asks where that object belongs. A is a subset of B when every x in A also belongs to B. So the subset symbol makes a promise about all of A's members.

For union, x passes when it belongs to A or B. That or includes the overlap. For intersection, x passes only when it belongs to A and B. The picture of two circles was showing these membership tests all along.

For a complement, we must keep the universe in view. The object x belongs to the complement of A when it is in U and is outside A. Now read De Morgan's two laws together. Negating a union gives the intersection of the complements. Negating an intersection gives the union of the complements. In each case, the equation states that the two sides accept exactly the same members. We can return to our pizza knowing what every symbol means.

## 13 · Ready to share — 21:07 → 21:47
Our pizza is ready, and both friends can share it. We began with a familiar question about toppings. Now we can describe the answer precisely: take the available toppings outside dairy and outside meat. The equation records that same decision in two equivalent ways. Sets let us describe what belongs. Intersections show what is shared, and complements tell us what remains within the universe we chose. Those ideas can begin with a pizza and travel almost anywhere.

## 14 · End card — 21:47 → 21:56
Thanks for watching. Subscribe for more visual mathematics, and I will see you in the next video.
