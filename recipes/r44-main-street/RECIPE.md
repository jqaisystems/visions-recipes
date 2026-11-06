# R44 · Main Street

**Style:** a tilt-shift miniature town. Hand-written WebGL2: instanced buildings, one moving sun with a real shadow map, a
tilt-shift final pass and motion across 8 sub-frames, all computed from the beat. Flat labels and the mark sit on a 2D layer above.
**Made for:** the AI Client Acquisition System, two internal tools that find and score businesses and write an email for a person to approve or reject.
**Length:** 32 s · 1920×1080 · 30 fps, with a 9:16 cut built on its own portrait town.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for the AI Client Acquisition System, two internal tools that find businesses,
score them from 0 to 100 with a written reason and draft an email for a person to approve. Make it dynamic motion design, a showreel
piece, in daylight and full colour. The funnel happens to a miniature town of exactly 500 fictional businesses, shot like a tilt-shift
model, in hand-written WebGL2: instanced buildings with gable roofs and windows, trees, one sun with a 4096 shadow map, a tilt-shift
final pass, ACES and motion across 8 sub-frames, with everything computed from the beat. One Python table holds the town, the scores
and the words. 120 bpm, 64 beats. Coral #EE4A2B, gold #F5B21F, bone #FBF5E4, ink #14111A, Archivo at 900, JetBrains Mono for labels. A
score composed in code in C: each business plays one marimba note as it's found, then plucked bass, hand claps and glockenspiel.
All businesses, scores and emails are fictional and labelled DEMO DATA.
One van: macro on an orange van in an empty town. "500 COLD RESULTS." The first five shops open on the first five notes.
The search: shops bounce up around the van and outwards from the plaza as the camera lifts to the whole town.
Words: SEARCH and SCORE rise from the ground as thousands of tiny blocks, casting real shadows, with "BY INDUSTRY AND LOCATION" and "0 TO 100, WITH A WRITTEN REASON".
Scores: a low flight along the streets with a rolling score tag on every roof.
The drop: one held breath, then a shockwave through the ground, debris, buildings sinking and night falling at once. "BELOW 40: FILTERED OUT". 30 buildings stay lit and throw beacons. A giant gold "30", "QUALIFIED, OUT OF 500".
One business: sunrise on TIDAL BAKERY with a queue outside, 87 / 100, "NO WEBSITE. SOCIAL PAGE ONLY.", labelled fictional.
The flip: the town turns coral and ink. "SOMETHING SPECIFIC ABOUT THEM."
The draft: paper labelled "DRAFT · NOT SENT · DEMO TEXT" beside the street. APPROVE on the bakery; REJECT on a neighbour, which sinks. "YOU DECIDE WHAT GOES OUT."
Never twice: new shops open while six contacted buildings sit dark inside rings. "NO PROSPECT EMAILED TWICE."
Close: the sun sets, the town sinks from the edges inwards, and the logo lands flat, never redrawn or recoloured, with the system's name, the URL and "INTERNAL SYSTEM · DEMO DATA".
Take facts only from the case study. Claim no replies, clients or revenue, and don't imply it's for sale or that emails send themselves.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose story is {the_story}, set in a living miniature {place}
shot like a tilt-shift model. Use instanced 3D {buildings_or_objects} in hand-written WebGL2, one sun moving through {times_of_day} with real
shadows, a tilt-shift final pass and motion across sub-frames, all computed from the beat. Keep one table for the {things} and let each play
one note as it appears, so {the_process} is the tune. Build {your_big_words} from thousands of tiny blocks standing in the streets. Hold one
breath, then send a shockwave through the ground for {the_big_change}. Fly in on {one_example}, show {the_decision}, and end on {your_mark},
placed flat, with {line} and {url}, at {bpm} bpm with a score composed in code.
```

Ideas:

- A courier app: parcels as vans crossing a miniature city, and each delivery a note in the tune.
- A property portal: a model town where only the homes matching your search stay lit at night.
- A local election: a town of real scale with results rising from the streets, block by block.
- A city's own festival: venues opening as the band plays, each stage a note, the night falling on the drop.

## How it's built

1. **Five shops, five notes.** The first shops are picked by where the van will be when each note plays, so a tiny street gets to be a melody before the town arrives.
2. **The search has a body.** Shops open as the van passes and outwards from the plaza, whichever comes first, with an overshooting bounce on the sixteenth.
3. **Words that cast shadows.** SEARCH is thousands of tiny blocks of uneven height, standing in the streets under the same sun as everything else.
4. **Scores on the roofs.** A low flight with a tag pinned to each roof by projecting its position every frame. Tags too far away to read are dropped.
5. **The drop.** One held breath, then a pulse through the ground lifts the streets as it passes, filtered buildings tip and sink, debris flies and the sun moves to night.
6. **30 beacons.** The survivors stand taller with lit windows, and each throws a beam of pure light into the sky, so a very small thing can be seen from the top of a town.
7. **A place to care about.** One bakery with an awning, parked cars, trees and a queue that shuffles, labelled fictional, so a lead is suddenly somewhere you could go.
8. **A person decides.** APPROVE lights on the bakery, REJECT sinks its neighbour, and a word the size of the town says who chose.

## Gotchas worth knowing

- Fog that looks lovely at street level turns every wide shot to milk. Start it beyond your widest camera.
- A long lens means a long way back. Work out the distance from the width you need, or the words will run off the frame.
- Check your words against their ground. Bone on sunny streets vanished, and ink held.
- Check how long a word stays finished, not when it starts. A wave of blocks can use up a whole line's hold.
- Plan for what stands in front of your hero. Random houses and trees will end up between the camera and the bakery.
