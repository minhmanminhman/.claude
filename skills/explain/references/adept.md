# ADEPT: principles and worked examples

Source: Kalid Azad, BetterExplained. [ADEPT method](https://betterexplained.com/articles/adept-method/), [learning-to-learn cheatsheet](https://betterexplained.com/cheatsheet/).

## The principles behind the acronym

**Cat, not DNA.** Three definitions of "cat": furry thing with claws that purrs; descendant species sharing traits; the sequence `ACATACATACAT`. The last is precise. It is not what you teach a child. Math education hands out DNA first. So does most technical documentation.
Source: [Developing Your Intuition For Math](https://betterexplained.com/articles/developing-your-intuition-for-math/).

**Work around the circle.** Picture the idea at a centre, surrounded by its facts. Enter at whichever corner is reachable, then work around until you reach the formal definition. There is no single correct entrance.

**Pencil, then ink.** Lee Ames' *Draw 50 Animals* teaches drawing by penciling ovals and rectangles first. The scaffolding is the lesson; the ink is the result. Premature rigour causes three specific harms: fear ("what if I'm wrong?"), tracing (mimicking steps without reasoning), and the illusion that the field advanced "linearly and unwaveringly."
Source: [Pencil, Then Ink](https://betterexplained.com/articles/learning-to-learn-pencil-then-ink/).

**Be the cartoonist.** A cartoonist sees the emotion and amplifies it. A photorealist copies the shading and misses the person. "Technically correct and real-life-ily horrible" is the failure mode. Oversimplify strategically - a limited but accurate understanding is a foothold.
Source: [Think like a cartoonist](https://betterexplained.com/articles/math-cartoonist/).

**Analogies are rafts.** All models are wrong, some are useful. An analogy is scaffolding to be discarded after crossing. Experts call analogies useless because they have already crossed. Ground each one in something the learner already deeply owns - the brain is an association machine.
Source: [Embrace Analogies](https://betterexplained.com/articles/learning-to-learn-embrace-analogies/).

**The ladder of abstraction.** There is no all-purpose answer like "less detail is better." Move closer or further from the idea until it snaps into focus, the way an eye exam swaps lenses. When stuck, reposition rather than add information.
Source: [Math Abstraction](https://betterexplained.com/articles/learning-to-learn-math-abstraction/).

**Honest learning.** Priority one for any class: do not create hate for the subject. Don't hide the difficulty. Explain why an idea was historically distrusted. Teach as a coach, not an oracle. Respect that not every reader wants mastery - some want appreciation.
Source: [Honest Learning](https://betterexplained.com/articles/honest-learning/).

**Intuition is not optional.** Judge your own understanding by three questions, not by a test score: understandable (aha moment, can I say it simply), memorable (an analogy, diagram, or example that lasts months or years), enjoyable (do I want to come back). Questions provoke more interest than assertions.
Source: [Intuition Isn't Optional](https://betterexplained.com/articles/intuition-isnt-optional/).

## Finding the seed

Three steps for locating the central theme of any idea:

1. **Ask history.** Where was the idea first used? What was the discoverer doing when they needed it? The original motivation is usually the analogy.
2. **Translate the notation.** Convert each equation into plain English through that theme.
3. **Test the theme.** Push it at neighbouring properties. If it explains those too, it is the right seed. If it snaps, find another entrance.

For code, the same three steps read as: what commit introduced this and what broke without it; what does each function *do* in one plain sentence; does that story also explain the module next door.

## Worked examples

### Math, from the source

**Imaginary numbers.**
- A: numbers can move north and south, not only east and west. `i` is a rotation into the second dimension.
- D: the number line with a second axis, an arrow swinging 90 degrees.
- E: four 90-degree turns return you to the start.
- P: "Imaginary numbers seem to point North; four turns gets us pointing in the positive direction again."
- T: `i^2 = -1`, `i = sqrt(-1)`.

**The number e.** Four definitions, one theme - continuous 100% growth.
- Compound interest: e is 100% growth compounded at the smallest possible increment.
- The series `1/0! + 1/1! + ...`: each term is a layer - principal, its interest, the interest earning interest. Personified as Mr. Blue, Mr. Green, Mr. Red.
- The differential equation: your growth rate equals your current amount.
- The natural log as time: at value `a` you have grown for `ln(a)` units of time, so e is where you land after exactly one.

**Fourier transform.** A: filtering a smoothie back into its ingredients. E: decomposing the sequence `(4 0 0 0)` into circular components.

**Pythagorean theorem**, as a rhetorical template worth copying: opens on a pop-culture hook, builds area intuition with a small table before touching the theorem, gives one intuitive proof ("any right triangle splits into two similar right triangles") rather than a mechanical one, then applies it to four unrelated domains - circles, social networks, sorting, kinetic energy - each with a 3-4-5 example. It closes by reframing what the reader already knew rather than adding a new fact.
Source: [Surprising Uses of the Pythagorean Theorem](https://betterexplained.com/articles/surprising-uses-of-the-pythagorean-theorem/).

### Software

**Distributed version control** (the author's own): like sharing changes to a group shopping list with friends. P: check out, check in, branch, share differences.

**Applying the shape to a codebase walkthrough.**
- A: what everyday system does this module behave like? A post office, a turnstile, a waiting room, a ledger.
- D: a box-and-arrow of the actual call path, or the state machine the code implements. Real function names.
- E: one real request or one real input, traced line by line with concrete values, citing `file.py:42`.
- P: one sentence on what the module guarantees to its callers.
- T: the signatures, the invariants, the failure modes, the concurrency assumptions.

The seed for code is the constraint. Ask what breaks if the module disappears. Retry logic exists because the network drops; a lock exists because two writers collided once. Name that event and the design explains itself.

### Quant and finance

The domain is dense with formulas that arrived with their motivation stripped off - prime territory for this method.

- **Volatility.** A: the width of tomorrow's fan of outcomes, not today's direction. D: a price path with a widening cone. E: 16% annual vol on a $100 name is roughly $1 of daily movement, since `16/16 = 1`. P: how far the price typically wanders per unit of time. T: annualised standard deviation of log returns, and the `sqrt(t)` scaling that makes the shortcut work.
- **Order book queue position.** A: a ticket line where new arrivals stand at the back and cancellations leave gaps. D: stacked blocks at one price level with your order marked. E: one order joining behind 5,000 shares, then 3,000 cancel ahead of it. P: how much size must trade before yours does. T: the FIFO matching rule and what a cancel-replace costs.
- **Sharpe ratio.** A: reward per unit of nervousness. E: 8% excess return against 16% vol is 0.5. T: the definition, then the assumptions it quietly makes about the return distribution.

Flag the raft's limit where the money is: volatility as a cone assumes a distribution that fat tails violate. Say it, once.
