# The D: diagrams that degrade gracefully

The claim behind the mandate: roughly half the brain is dedicated to vision processing. Readers retain a scattered diagram long after the derivation is gone. A missing diagram is the most common reason an explainer fails the six-month test.

## Choose the weakest form that still carries the idea

| Medium | Use when | Cost |
|---|---|---|
| Inline SVG in HTML | Position encodes meaning: geometry, overlapping regions, a distribution, a price path, a growth curve | High |
| Mermaid | Structure without geometry: call graphs, state machines, sequences, dependency trees | Low |
| ASCII | Terminal answers, small stacks, before/after pairs, timelines | Lowest |
| A small table | The idea is genuinely non-visual and the shape lives in the data | Lowest |

Say in one line when a concept has no useful picture, then show the data's shape instead. Silence reads as laziness.

## What to draw

Draw the mechanism, not the vocabulary. A box labelled "Auth Service" with an arrow to "Database" teaches nothing the names did not. A diagram showing the token minted at t=0, carried on two requests, and rejected on the third teaches the mechanism.

Rules that hold across all three media:

- **One idea per diagram.** If it needs a legend of six entries, it is two diagrams.
- **Label with the reader's own names.** Real function names, real ticker symbols, real field names.
- **Mark the reader's position.** In a queue, a call stack, or a lifecycle, show where "you" are.
- **Annotate the surprise.** The arrow that goes backwards, the branch nobody expects - call it out on the drawing, not only in the prose.
- **Numbers on the drawing.** A cone of volatility with no axis labels is decoration.

## ASCII that works

Queue position at one price level:

```
price 100.25  [ 5,000 ][ YOU: 300 ][ 1,200 ]
              ^ front                  ^ back
              ---- 5,000 must trade before you ----
```

A call path:

```
handler.py:14  handle_order
   -> validate(order)          # rejects 4 of 5 failure modes here
   -> book.insert(order)       # lock held: ~40us
        -> match()             # may re-enter insert on partial fill
   <- OrderAck
```

## SVG in HTML

Hand-write it. Keep it under ~60 lines, use `viewBox` so it scales, and set `stroke`/`fill` from CSS custom properties so the drawing survives a dark background. Never link an external image - the file must stand alone if it is moved or later published.
