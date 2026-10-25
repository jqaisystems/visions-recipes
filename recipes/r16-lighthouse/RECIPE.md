# R16 · Lighthouse

**Style:** lead generation as a lighthouse at night, filmed like a luxury watch commercial. A sweeping beam that is
the search, boats that are prospects, a sea that mirrors everything, and a harbour that is the pipeline.
**Made for:** AI Lead Generation & Outreach (ai.joaoqueiros.com/services/lead-generation).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom and reflector) · GSAP · Python (table, word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Lead Generation & Outreach service: a lighthouse at night,
Three.js with bloom, a sea that reflects everything (a TSL reflector), warm lamps, teal #00BFB4 accents.
A red and white striped lighthouse on dark rocks, a brass lantern room with a turning glass lens, a low moon, a
stone quay, and 44 small boats scattered on the sea, each with a lamp on its mast.
Open on a macro through the lantern glass: the lamp flickers on and the lens starts to turn, with a foghorn.
Source: the beam sweeps across the sea and every boat it passes lights up; the HUD reads "ideal customer · design
studios, 10 to 50 people". Enrich: the beam stops on three boats and a card rises beside each ("Posted about a
rebrand", "Opened a second office", "Hiring a designer"). Score: the camera rises to a top view and the beam sweeps
again; a score from 0 to 100 appears over every boat; the cold ones fade and the six hot ones (85+) turn amber and
head for shore. Draft: a panel types a first message to the best one, "Ana · design studio · fit 96", and a cursor
pulls a brass SEND lever; a spark flies from the lighthouse to her boat. Harbour: the hot boats moor at the quay and
their lights rise into the word "found" above it, mirrored in the water. End on "AI Lead Generation & Outreach",
"Your next clients, found and scored for you." and the URL. Station titles wipe on bottom left.
Technique: one seeded table baked in Python holds the beam's path and every boat (where it is, when the beam first
finds it, when it is scored, its score); the film and the score both read it. The beam is two additive cones that end
where they meet the water and fade as the camera nears them.
Score: compose it in code from the same table: the sea's wash and a slow night pad, a filament hum and a foghorn, a
sonar ping for every boat found, ticking digits and a warm bell for every hot lead, typing, a lever's ratchet and
clunk, a rush as the message flies, a shimmer as the lights rise, harbour bells into one last chord.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: {search} as a lighthouse at night,
Three.js with bloom and a sea that reflects everything, {accent} accents.
The beam is {the_search}; the boats are {the_candidates}; the harbour is {the_destination}.
Source: the beam sweeps and every boat it passes lights up. Enrich: it stops on three and a card rises beside each:
{card_1}, {card_2}, {card_3}. Score: every boat gets a number; the best turn for shore. {human_moment}.
Then the best boats moor and their lights rise into the word "{word}", mirrored in the water.
End on {title}, {line} and {url}. One baked table drives the picture and a score composed in code.
```

Ideas: a recruiter's search for candidates; a buyer comparing suppliers; a fund scanning startups; a reader finding
the right sources.

## How it's built

1. **One table.** `bake/boats.py` seeds 44 boats and the beam's path, then works out when the beam first passes each
   boat and when it passes again to score it. The film reads `assets/boats.js` and the score reads `bake/boats.json`,
   so every ping lands on the boat that lights up.
2. **A sea that mirrors.** The water is a gently moving surface with a TSL reflector under it, nudged by the surface
   normals, so the boats, the lighthouse, the beam and the word all reflect.
3. **A beam you can see.** Two additive cones, brightest at the lamp and thicker toward their middle, scaled every
   frame to end where the beam meets the water. A narrow spotlight on the same line really lights the boats.
4. **Scores over the sea.** Each score is HTML, placed every frame by projecting the boat to the screen, and counted
   up as the beam passes. The cold ones fade; the hot ones stay amber.
5. **Lights into a word.** Several hundred points are sampled from the outlines of "found"; each light leaves a hot boat on
   an arc and lands on its point above the quay, and the reflector does the rest.

## Gotchas worth knowing

- A cone of light seen from inside is a grey wall: end it at the water and fade it as the camera nears its axis.
- A shiny sea under a spotlight blooms into a white blob: a rougher sea gives a soft pool of light, and the reflector
  keeps the sparkle.
- Keep the floating scores off the HUD and the panels, and give them a dark pill so they stay readable over bright
  water.
- With a mirror sea, place the end card below the word's reflection, not on top of it.
