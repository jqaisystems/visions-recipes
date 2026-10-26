# R20 · Cartographer

**Style:** a consulting engagement as a navigator's chart table in a dark study, filmed in macro like a watch
commercial. The business is a map under fog; the audit raises the land where the hours go, the opportunities are pins
scored on payoff, cost and risk, and brass dividers rule the route in phases.
**Made for:** AI Consulting & Roadmapping (ai.joaoqueiros.com/services/consulting).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom) · GSAP · Python (table, word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Consulting & Roadmapping service: a navigator's chart table
in a dark study, filmed in macro like a watch commercial, Three.js with bloom, an oiled wood table under one warm lamp,
a map printed on aged chart paper, brass instruments, teal #00BFB4 for the survey ring, the pins' heads, the route and
the HUD.
Not sure where to start: the lamp comes up over the map of one made-up business, an island with six regions ("Sales",
"Quotes", "Support", "Finance", "Content", "Hiring"), a compass rose, a cartouche "The business, as it runs today" and
"here be guesses" in the sea, all under drifting fog. The HUD asks "where does AI fit?".
The audit: a brass survey ring opens out from the centre with a teal beam turning inside it. Where it passes, the fog
lifts and the land rises as thousands of small paper columns, one per cell of the map, tallest where the hours go,
each column flashing teal as it comes up. No numbers: the heights are relative.
Every opportunity, scored: twelve brass pins with teal heads drop onto the relief, each with a label and three rings
at its foot that settle to its payoff, cost and risk. Four are knocked flat with a bounce and marked "NOT WORTH
BUILDING" (a chatbot for everything, auto-screen CVs, rebuild the books, video at scale).
Ranked: the eight left standing lift off the map and line up on a brass rail along the table's edge, tallest first,
and a paper tag swings in under each with its rank, its name and one reason ("The biggest pile of hours, low risk").
Each leaves a numbered teal marker where it stood.
The route: brass dividers walk the map stride by stride from marker 1, ruling a teal line draped over the relief in
three legs, "First · 0 to 3 months", "Second · 3 to 6 months", "Third · 6 to 12 months"; the camera follows them, and
each phase's pins light up on the rail. A compass needle swings and settles on the first leg.
The roadmap: the relief settles into the paper and the route is printed on it, the line itself lifts off the table,
the paper rolls up into a scroll tied with teal bands and a tag, "Roadmap · Debrief booked", and the floating route
re-forms into the word "mapped" in beads of light. End on "AI Consulting & Roadmapping", "Your business mapped against
what AI can realistically do now, and a phased plan you can actually execute." and the URL. Station titles wipe on
bottom left; a HUD names each stage.
Technique: one seeded table baked in Python holds the film's clock, the coast, the regions and their relative hours,
a height for every land cell, every pin (payoff, cost, risk, rank, reason, when it drops or falls), the three phases
and every stride of the dividers; the film and the score both read it. The relief is one InstancedMesh; the fog is a
TSL shader cleared by the ring's radius. No promised hours, savings or ROI anywhere.
Score: compose it in code from the same table: a lamp hum and a low D drone, a sonar ping on every turn of the beam, a
patter of tiny taps that thickens as the land rises, a pluck for every pin over a 90 bpm pulse (Dm, Bb, F, C), a
muted thud and a bounce for every pin knocked flat, a rising line as the pins rank, a brass step on every stride, a
chord for each phase (D, G, A), compass ticks into a bell, a crackling swish as the paper rolls, and one wide D major
chord under the word.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: {what_is_planned} as a navigator's chart
table in a dark study, Three.js with bloom, one warm lamp, chart paper, brass instruments, {accent} accents. The map
shows {the_territory} with its regions {regions}, under fog. A survey ring lifts the fog and the land rises by
{what_the_height_means}. Pins drop in for {the_candidates}, each scored on {three_measures}; {the_rejects} are knocked
flat as "{reject_label}". The rest line up in rank order with their reasons, and brass dividers rule a route in
{phases}. The map rolls up as {the_deliverable}, tagged "{the_tag}", and the route writes the word "{word}".
End on {title}, {line} and {url}. One baked table drives the picture and a score composed in code.
```

Ideas: a year of marketing campaigns, ranked and phased; which shops to open first in a new city; a training plan for a
new team, quarter by quarter; the order to renovate the rooms of a house.

## How it's built

1. **One table.** `bake/table.py` holds the film's clock, the coast, the six regions and their relative hours, a
   height for every land cell, the twelve pins with their payoff, cost, risk, rank, reason and timing, the three
   phases, the route and every stride of the dividers. The film reads `assets/table.js` and the score reads
   `bake/table.json`, so every step lands on what you see.
2. **The relief.** One `InstancedMesh` of 8,586 boxes, one per land cell. Each frame a column's height is its rest
   height times a back-out ease of how far the survey ring has passed it, and its colour leans teal just behind the
   ring and under the turning beam. The heights are stepped like contour lines.
3. **The fog and the ring.** The fog is two planes whose TSL opacity is a cloud texture times a `smoothstep` on the
   distance from the centre, so it clears exactly where the ring has been. The ring is a torus of radius 1 whose
   vertices are pushed out to the ring's radius in a TSL `positionNode`, so its tube keeps its thickness as it grows.
4. **The pins.** Each is a brass needle and a teal head; it drops on a power ease and settles with a damped bounce.
   The three rings at its foot overshoot and settle on a damped cosine; a pin knocked flat turns about a horizontal
   axis on a bounce ease. The ranked pins fly to the rail on a quadratic Bézier.
5. **The dividers.** The route is baked as a Catmull-Rom curve through the eight stops, lifted just above the tallest
   column under it. Each leg is cut into whole strides: one foot stays planted while the other swings to the next
   stride, and the hinge sits where two legs of fixed length meet. The teal line is a tube revealed with a draw range
   up to the pen.
6. **The roll.** The paper is a strip of 260 rows. Behind the contact line every vertex is wound onto a spiral whose
   radius grows with the paper already rolled, so the scroll thickens as it travels; the printed roadmap fades in on
   the same material before it rolls.
7. **The word.** Points sampled from the word's outlines are each reached from their own place along the route, in
   order, so the line seems to re-form into the letters.

## Gotchas worth knowing

- A white paper relief under bloom turns to mush: keep the lamp low, the columns warm and a little dark, and let the
  bloom catch only the teal.
- Fog drawn as an unlit plane glows on its own in the dark: tie its colour to the lamp, or it reads as a grey wash.
- When the camera follows something that pauses, average its position over a short window, or the camera jerks at
  every stop.
- A Studio preview session can add `data-hf-id` attributes to your `index.html`; check your diff before you commit.
