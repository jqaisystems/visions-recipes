# R18 · Loom

**Style:** research and briefing as a Jacquard loom in a black studio, filmed in macro like a watch commercial. Every
source is a thread of light, what you know is the punched card the loom reads first, the threads it doesn't lift fall
away as noise, and the woven cloth is the briefing, on the table every Monday at 09:00.
**Made for:** AI Research & Briefing Systems (ai.joaoqueiros.com/services/research-briefing).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom and a reflector floor) · GSAP · Python (table, word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Research & Briefing Systems service: a Jacquard loom in a
black studio, filmed in macro like a watch commercial, Three.js with bloom, brass and oiled wood, a polished floor
that reflects everything (a TSL reflector), amber threads of light, teal #00BFB4 for the threads that matter and the HUD.
Your sources: 212 threads of light stream in from the dark onto the loom's back beam while made-up headlines flicker
past ("Tender opens for a three-year contract", "Five trends you can't ignore", "We're thrilled to announce…").
What you know: a brass pattern card slides into the Jacquard head and eight rules punch in one hole at a time ("our
market", "our clients", "competitors", "regulation", "tenders", "no press releases", "no duplicates", "always the
why"); a teal scan reads the card, and its cords drop to every thread. Only what matters: the loom runs at 96 bpm, the
shuttle flies, the reed beats every pick in; nine threads lift and turn teal, and the other 203 go slack, turn grey
and fall away. The briefing: the camera rises over the loom and the cloth's type comes through the weave in a teal
sweep: "Three things that matter this week.", three stories, each with a "why it matters" line, each sitting over its
own three teal source threads. On schedule: a double-faced brass clock swings in and strikes Monday 09:00; the cloth is
cut, folded twice and carried to a table by an empty chair. Every Monday: the briefings stack up, and the nine threads
rise and draw the word "briefed" in light. End on "AI Research & Briefing Systems", "Your sources, read for you,
briefed on schedule." and the URL. Station titles wipe on bottom left; a HUD counts the threads read and kept.
Technique: one seeded table baked in Python holds every thread (where it comes from, when it arrives, whether the card
lifts it, when it falls, which story it feeds), the headlines, the rules, every pick of the loom and the three
stories; the film and the score both read it.
Score: compose it in code from the same table: a low warm drone, a soft pluck as each thread arrives, static for the
headlines, a clack and a rising note for every rule punched, a shimmer as the card is read, then the loom as the beat
at 96 bpm (a wooden thunk for every beat-up, a swish for the shuttle, a hook clack on the off-beat) over Am, F, C, G,
muffled drops for the threads that fall, nine notes for the nine that matter, a bell per story, the clock ticking to
09:00 and striking, a soft thud for every Monday, one wide chord under the word.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: {many_inputs} becoming {one_output}, as a
Jacquard loom in a black studio, Three.js with bloom, brass and oiled wood, a reflective floor, {accent} accents.
Every {input} is a thread of light; what the system knows is a punched card it reads first: {rules}.
The loom runs; the threads the card lifts turn {accent}, and the rest fall away as {the_noise}.
The woven cloth becomes {the_output}: "{headline}", with {its_parts}, each over its own threads.
{the_moment} ({a_clock, a_deadline, a_handover}). Then the threads gather into the word "{word}".
End on {title}, {line} and {url}. One baked table drives the picture and a score composed in code.
```

Ideas: support tickets woven into a weekly summary; a team's reports woven into one board update; sensor readings
woven into a morning status; job applications woven into a shortlist.

## How it's built

1. **One table.** `bake/loom.py` holds the 212 threads (start point, arrival, whether the card lifts it, the moment it
   falls, its story), the headlines, the eight rules, every pick of the loom and the three stories. The film reads
   `assets/loom.js` and the score reads `bake/loom.json`, so every note lands on what you see.
2. **Threads as one draw.** Every thread is a 28-point polyline in a single `LineSegments`: 16 points of flight from
   the dark, 12 through the warp. A head and a tail move along it to draw it on; the rejected ones sag on a curve
   driven by the clock, turn grey and fade.
3. **The card.** Nine textures are drawn ahead of time, one per number of holes punched, so a frame just picks one;
   each punch adds a flash and a glow, and a teal line scans the card when it is read.
4. **The weave.** The shed opens by moving the lifted threads' heddle eyes; the shuttle, the weft line and the reed
   are timed to the table's picks, and the cloth grows by one pick at a time.
5. **Cloth with type.** The cloth is a 40 by 60 grid laid out on the CPU by `layCloth`, so it can be woven, cut,
   folded twice and carried. Its texture is the briefing drawn on a canvas, revealed after weaving by a teal sweep.
6. **Threads into a word.** Points sampled from the word's outlines are reached from the nine kept threads, and beads
   ride the lines into "briefed" over the stack of finished briefings.

## Gotchas worth knowing

- A cloth seen from behind the loom needs its triangles wound to face that camera, or the type is on the hidden side.
- Read the briefing from behind the loom, where the type runs left to right; the orbit to get there needs a high
  keyframe to clear the Jacquard head.
- A bright key light and bloom turn a pale cloth into a white blob: keep the cloth's albedo low and the light modest.
- Let a lit object leave the frame before the next light comes up, or it blooms out: the clock leaves before the table
  is lit.
