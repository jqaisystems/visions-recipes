# R64 · Gist

**Style:** string art in code: 5,184 nails land scattered, straighten onto a grid and take their theme's colour, then one thread winds BRIEF only along passes that stay inside the letters, holds its last pass for a reviewer, and joins a wall of earlier days.
Every frame is worked out from the time alone. No footage, no images: the word is set in code.
**Made for:** AI News Curator, a research briefing workflow: useful signals from newsletters, releases, docs updates and saved links become consistent records, grouped by topic and date, and the latest useful items become one short daily brief. A person decides what each one becomes, and nothing is published automatically.
**Length:** 40 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · GSAP · Python (winding, table and score) · NumPy · SciPy · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 40-second 1920x1080 film in HyperFrames for AI News Curator, my research briefing workflow. Useful signals arrive from newsletters, releases, social posts, saved links, docs updates and community notes, and sit in tabs until they're forgotten. The workflow turns each one into a consistent record, groups them by topic and date, and makes the latest useful items into one short daily brief. A person decides what each one becomes, nothing is published automatically, and the archive is kept by day, month and topic. Make it string art in code: a dark board full of nails, and one thread that only takes passes that stay inside a letter, so a word comes out of crossing straight lines like a hand-made string-art sign.
Wind it in Python first. Set BRIEF large on a jittered grid of 5,184 nails. A pass may only run between nails near a letter's edge and must stay inside the letter for its whole length. From the nail it is on, the thread takes the pass that covers the most bare letter; when nothing is worth winding from there, it runs behind the board to the best pass left. Hold back the longest of the last sixty passes and move it to the end, with hidden jumps behind the board, so the thread stays one run. Split the board into six theme patches with ragged borders.
Draw it in WebGL2: instanced nails with round heads on a dark board, the thread as instanced lit ribbons, one low key light with a shadow map. Work out every frame from the time alone. One table holds the nails, the passes, the camera and the captions, and drives both the film and the score, at 96 bpm. An "AI NEWS CURATOR · DEMO BOARD" label stays on screen. The score is composed in code, strings and wood: a tap for every nail, and a pluck for every pass, its pitch set by its length like a real string, kept in D major pentatonic.
Scattered: from low across the board, nails land in eight waves at random angles and well off their places, a few with small source-type tags: NEWSLETTER, RELEASE, DOCS UPDATE, SAVED LINK, COMMUNITY NOTE, SOCIAL POST, never a link or a headline. "USEFUL SIGNALS ARRIVE FROM EVERYWHERE." "AND SIT IN TABS UNTIL THEY'RE FORGOTTEN."
Every link a record: a ripple from the centre lifts every nail, carries it to its place on one grid and taps it in. "EVERY LINK BECOMES A RECORD."
Topic and date: a band of light crosses the board and each head takes its theme's colour, coral, amber, teal, sage, sky or violet, with no labels. "GROUPED BY TOPIC AND DATE."
The brief: the thread ties on and the camera follows its tip as it winds BRIEF, slowly and then in a rush, while the rest of the board stays bare. "THE LATEST USEFUL ITEMS," "IN ONE SHORT DAILY BRIEF."
A person decides: the thread stops one pass short, its end hanging loose. A dashed amber line marks the pass still to be laid and its nail glows. A reviewer's lamp crosses, and only then is the last pass pulled into place, with one pluck. "A PERSON DECIDES WHAT EACH ONE BECOMES." "NOTHING IS PUBLISHED AUTOMATICALLY."
The archive: the camera pulls back to a wall of fifteen boards, three weeks of weekdays under MON to FRI, today's marked TODAY, each wound and in its own colours. "KEPT BY DAY, MONTH AND TOPIC." "RESEARCH STARTS FROM MEMORY, NOT OLD TABS."
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI News Curator", the URL and "RESEARCH BRIEFING WORKFLOW · THIS FILM IS CODE".
Take facts only from the case study. The board is a demo: no real links, headlines or sources. Name no tools and claim no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made as string art in code: a dark board of {nails} nails that land scattered and straighten onto a grid, then one thread that winds {your_word} out of straight lines, each pass chosen in Python to stay inside a letter and cover the most bare letter. Hold the last pass back until {your_moment}, then pull back to {your_wall}, and end with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where every pass is a pluck pitched by its length.
```

Ideas:

- A shop's daily special wound on a board of its regulars, the last pass laid when the chef says so.
- A team's weekly update: the board holds every ticket, and the thread winds the one word that sums up the week.
- A portfolio intro: your name wound out of a board of all your projects, then the camera pulls back to the years before.
- A product launch: the board is every piece of feedback, and the thread winds the product's name from the few that shaped it.

## How it's built

1. **Scattered.** Nails land in waves at every angle, a few tagged with a source type.
2. **Every link a record.** A ripple lifts every nail onto one grid and taps it in.
3. **Topic and date.** A band of light crosses the board and each head takes its theme's colour.
4. **The brief.** The thread winds BRIEF, slowly then in a rush, and the rest of the board stays bare.
5. **A person decides.** The last pass waits, marked in amber, until a reviewer's lamp crosses. Only then is it laid.
6. **The archive.** The camera pulls back to a wall of earlier days, today's marked TODAY.
7. **The mark.** The logo, the system and the link, flat on dark.

## Gotchas worth knowing

- Test that a pass stays inside the letter along its whole length, not just at its ends, or the thread cuts across the counters of B and R.
- Only offer passes between nails near a letter's edge. Nails deep inside a letter make short passes that fill it with clutter and never trace its shape.
- The pass held for the reviewer has to read from across the board. The last pass the winding happens to choose is often tiny, so pick a long one and move it to the end with hidden jumps behind the board.
- A board that is just big enough shows its edge in a low raking shot. Draw it far larger than the nails until the camera pulls back to the wall.
- A shadow map sized for one board turns to mush on a wall of fifteen. Widen its extent and move its centre with the camera.
- The portrait cut can't be a crop: pull the camera back until the whole word fits the width, and turn the wall so the weekdays run down the frame.
