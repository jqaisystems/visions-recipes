# R58 · Casting

**Style:** a shadow sculpture: one lattice of small blocks that looks like a tangle from every side, carved so that each level lamp throws a different exact word onto its own wall. RESEARCH, DRAFT and REVIEW from the same blocks, then PUBLISH from a fourth lamp while the lattice rebuilds itself.
Every block and every lamp is worked out from the time alone. No footage and no 3D engine.
**Made for:** AI Agent Architecture, a service: it designs multi-agent systems where each agent has one role, its own memory and skills and clear handoff rules, around a shared memory, with a human looped in, and recommends a simpler pipeline when one is enough.
**Length:** 40 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (carving, table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 40-second 1920x1080 film in HyperFrames for AI Agent Architecture, a service that designs multi-agent systems where each agent has one role, its own memory and skills and clear handoff rules, typically 2 to 6 agents around a shared memory, run on a schedule, on a trigger or on request, with a human looped in, built so a new agent should take hours, not weeks, and a simpler pipeline recommended when one is enough. Make it a shadow sculpture in code: one lattice of small blocks that looks like a tangle from every side, carved so that each lamp throws a different exact word onto its own wall.
Carve it in Python first. Draw each word as a mask, RESEARCH, DRAFT and REVIEW, then PUBLISH for a fourth lamp. Keep the lamps level, at 0°, 45°, 90° and 135° around the lattice, so every shadow shares the height axis: that's what makes it solvable. The solid is where every mask, pushed along its own lamp's line, says yes. Thin it one block at a time, in a seeded order, for as long as every shadow stays exactly the same. Carve a second lattice for four lamps, thinning first the blocks the three-lamp lattice lacks, and repair any pixel nothing can cast with one block where it only thickens a letter's edge.
Draw every block instanced in WebGL2 with softly bevelled edges, and every lamp as a parallel beam with its own shadow map, all four in one depth texture array, onto plaster walls set square to each lamp, with 4x antialiasing. Work out every block and every lamp from the time alone. One table holds the lamps, the turn, the rebuild, the collapse, the camera and the captions, and drives both the film and the score, at 96 bpm. An "AI AGENT ARCHITECTURE · DEMO SYSTEM" label stays on screen. The score is composed in code, dry and wooden: a relay clack and a hum on its own note for each lamp, so they make a chord, knocks for blocks sliding, a plucked run for each handoff.
One system: a dark room and the lattice turning slowly, meaning nothing. It settles square the moment the first lamp clicks on. "ONE SYSTEM."
One role each: three lamps light in turn, and RESEARCH, DRAFT and REVIEW land on three walls from the same blocks. "EVERY AGENT HAS ONE ROLE."
One shared memory: the camera moves into each lamp's line and the tangle locks into its word, while the blocks more than one shadow needs glow warm. "ONE SHARED MEMORY."
Handoffs: each lamp in turn at full, and a thin teal line runs along the walls from one word to the next. "ON A SCHEDULE · ON A TRIGGER · ON REQUEST". "EACH HANDS ITS WORK ON." Then a head and shoulders steps into REVIEW's light and its shadow stands beside the word. "A HUMAN SIGNS OFF."
A new agent: a fourth lamp swings in, and the lattice rebuilds itself block by block until PUBLISH lands on a fourth wall. "A NEW AGENT." "ADD ONE IN HOURS, NOT WEEKS."
The honest turn: every block slides into one plain cube, and one lamp throws one plain square. "IF ONE PROMPT IS ENOUGH," "I'LL SAY SO." Then back out to four words. "YOU OWN ALL OF IT."
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Agent Architecture", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The system is a demo. Name no tools or models, and claim no prices and no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made of a shadow sculpture in code: one lattice of small blocks, carved so that each level lamp throws a different exact word onto its own wall. Carve it from {your_words}, one per lamp, keeping only the blocks some shadow needs. Draw the blocks instanced with a real shadow map for every lamp, and work out everything from the time alone. Light the lamps one by one, move the camera into each lamp's line so the tangle locks into its word, add {one_more_word} with a new lamp while the lattice rebuilds itself, then collapse it all to {one_plain_shape}, and end with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code that is dry and wooden.
```

Ideas:

- A team film: one sculpture that casts each person's name from their own side of the table.
- A brand with three products: the same object casts each product's name, then collapses to the logo's simplest shape.
- A museum title: one object casts PAST, PRESENT and FUTURE onto three gallery walls.
- A wedding: one sculpture that casts both names, and the date from a third lamp.

## How it's built

1. **The tangle.** A lattice of pale blocks turns in a dark room and means nothing, then settles square as the first lamp clicks on.
2. **Three words.** Three lamps light in turn and RESEARCH, DRAFT and REVIEW land on three walls, from the same blocks.
3. **The proof.** The camera moves into each lamp's line and the tangle locks into its word, while shared blocks glow warm.
4. **Handoffs.** Each lamp in turn, a teal line running along the walls from word to word, then a head and shoulders steps into REVIEW's light.
5. **A fourth lamp.** A new lamp swings in and the lattice rebuilds itself block by block until PUBLISH lands.
6. **One block.** Every block slides into one plain cube that casts one plain square, then back out to four words.

## Gotchas worth knowing

- A lamp overhead throwing a word on the floor makes the carving unsolvable. Keep every lamp level, so all the shadows share the height axis.
- A diagonal word reaches past where the level lamps' words end. Set the diagonal words narrower, so every letter sits where all the lamps can reach.
- A fourth word can leave a few pixels nothing can cast. Repair each with one block placed where its stray shadow only thickens another letter's edge.
- A cube seen corner on casts a shadow about 1.4 blocks wide, so the diagonal words come out a touch bolder than their masks.
- Walls behind the camera block the proof shots. Build only the walls the lamps face and keep the camera on the lamp side.
- The portrait cut can't be a crop: open the lens a little, back the camera off along its own line so the walls still fit across, and break the captions onto two lines.
