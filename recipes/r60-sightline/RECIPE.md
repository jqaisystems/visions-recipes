# R60 · Sightline

**Style:** a shadow sculpture with one moving lamp: a lattice of small blocks whose shadow is noise from almost every angle, carved so it snaps into a word at exactly three, and rebuilt twice so three sweeps read three sentences.
Every frame is worked out from the time alone. No footage: every word is a real shadow.
**Made for:** AI Consulting & Roadmapping, a service: a workflow audit of where the hours go, an opportunity map scored by time saved, cost, risk and strategic value, a ranked priority list and a phased plan of 3 to 12 months of what to build first, second and third. No code, just direction.
**Length:** 40.8 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (carving, table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 41-second 1920x1080 film in HyperFrames for AI Consulting & Roadmapping, a service that maps where AI fits in a business before anything is built: a workflow audit of where the hours go, an opportunity map scored by time saved, cost, risk and strategic value, a ranked priority list, and a phased plan of 3 to 12 months showing what to build first, second and third. No code, just direction, and an honest answer when AI isn't a good fit. Make it a shadow sculpture in code with one moving lamp: a lattice of small blocks whose shadow is noise from almost every angle, carved so it snaps into a word at exactly three.
Carve it in Python first, three times. Draw each word as a mask at the same letter proportions: WHERE, DOES and AI FIT?; AUDIT, RANK and PLAN; FIRST, SECOND and THIRD. Keep the lamp level, and use 0°, 45° and 90°, so every shadow shares the height axis. The solid is where all three masks, pushed along the lamp's line, say yes. Thin it one block at a time, in a seeded order, for as long as every shadow stays exactly the same, and repair any pixel nothing can cast with one block where it only thickens a letter's edge. Match each lattice's blocks to the next one's, in the same row where they can be, so a rebuild slides every block to its next place.
Draw every block instanced in WebGL2 with softly bevelled edges, and the lamp as a parallel beam on a curved brass rail, throwing its shadow onto one long curved plaster wall. Take the lamp at four instants across a shutter of one and a half frames, each with its own shadow map, so the shadow smears while the lamp moves and is sharp when it stops, and ease it out of each angle fast and into the next slowly, so each word gathers. Work out the lamp and every block from the time alone. One table holds the lamp's moves, the stations, the rebuilds, the marks, the camera and the captions, and drives both the film and the score, at 100 bpm. An "AI CONSULTING & ROADMAPPING · DEMO ROADMAP" label stays on screen. The score is composed in code, dry and wooden: a rumble that follows the lamp's speed, a hiss that narrows onto a note as each word gathers, and a struck note and a wooden snap as it lands.
A tangle: a dark room, a pale lattice on a plinth, a lamp on a curved rail. The lamp slides and the shadow on the wall churns. "FROM MOST ANGLES, A TANGLE."
The question: over the lamp's shoulder, the shadow lands on WHERE, then DOES, then AI FIT? as the lamp passes each angle. "WHERE DOES AI FIT IN YOUR BUSINESS?"
The work: the blocks slide in a wave and AI FIT? becomes AUDIT. "WHERE THE HOURS ACTUALLY GO." The lamp sweeps back: RANK, "SCORED BY PAYOFF, RISK AND COST.", then PLAN, "A PHASED PLAN YOU CAN EXECUTE."
The roadmap: a second rebuild turns PLAN into FIRST. On the third sweep FIRST, SECOND and THIRD land, and each stays on the wall in teal over a line with a tick every 7.5°. "WHAT TO BUILD FIRST," "SECOND" "AND THIRD." "A PHASED PLAN · 3 TO 12 MONTHS".
The honest stop: the lamp goes on to an angle where nothing reads and stops. The shadow stays noise. "SOMETIMES THE ANSWER IS:" "DON'T BUILD IT."
Direction: the three marks on the wall light together. "NO CODE. JUST DIRECTION."
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Consulting & Roadmapping", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The roadmap is a demo. Name no tools or models, and claim no prices and no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made of a shadow sculpture in code with one moving lamp: a lattice of small blocks carved so that its shadow is noise from almost every angle and snaps into a word at exactly three, 0°, 45° and 90°. Carve one lattice for each sentence, {your_sentences}, three words each, and rebuild between them by sliding every block to its next place. Run the lamp along a rail, take its shadow across the shutter so it smears while it moves and is sharp when it stops, keep {your_last_words} on the wall, then stop the lamp at {an_angle_where_nothing_reads}, and end with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where a hiss narrows onto a note as each word lands.
```

Ideas:

- A product launch: one sculpture that reads THINK / MAKE / SHIP as the lamp travels, then rebuilds into the product's name.
- A countdown: three lattices for THREE / TWO / ONE, each rebuild one step closer.
- A manifesto: three sentences of three words, with the last sentence kept on the wall.
- A gallery title: the artist's name, the show's name and the dates, each found from a different angle in the same room.

## How it's built

1. **A tangle.** A lamp on a curved rail slides round a lattice of blocks, and the shadow on the wall churns.
2. **The question.** Over the lamp's shoulder, the shadow snaps into WHERE, then DOES, then AI FIT?, one at each angle.
3. **The work.** The blocks slide in a wave and AI FIT? becomes AUDIT; the lamp sweeps back through RANK and PLAN.
4. **The roadmap.** PLAN rebuilds into FIRST, and on the third sweep FIRST, SECOND and THIRD land and stay on the wall in teal.
5. **The honest stop.** The lamp goes on to an angle where nothing reads and stops. The shadow stays noise.
6. **Direction.** The three marks light together: no code, just direction.

## Gotchas worth knowing

- A short word alone on a wall can fill in its own gaps: FIT? by itself lost the gap in its question mark. Move a word across, AI FIT?, until every counter stays open.
- Three words at 0°, 45° and 90° carve exactly, as long as every word is set at the same letter proportions and the diagonal word is measured in half diagonals.
- A shadow map taken at one instant makes a moving lamp's shadow jump. Take it at a few instants across the shutter and average them, and the shadow smears while it moves and lands sharp.
- A rebuild that moves blocks in random order turns the word into noise all at once. Run it as a wave across the lamp's line, and the word changes from one end to the other.
- An honest stop next to the last word lets the noise sit on top of it. Stop the lamp well past it, where no word was ever carved.
- The portrait cut can't be a crop: stand further back and higher over the lamp's shoulder, so the lamp, the lattice and the word stack down the frame, and break the captions onto two lines.
