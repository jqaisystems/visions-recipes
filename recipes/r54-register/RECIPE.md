# R54 · Register

**Style:** print, in code. Every frame is four plates of ink, cyan, magenta, yellow and black, each screened into round halftone dots at its own angle and printed over the others on paper.
The plates drift out of register into noise and lock back into register on the beat. Every frame is worked out from the time alone. No footage and no 3D engine.
**Made for:** AI Research & Briefing Systems, a service: it watches the sources that matter, reads a knowledge document of the client's field first, and writes up what changed, and why, in the client's format and voice, daily or weekly, where the client keeps the code, the prompts and the knowledge document.
**Length:** 37 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 37-second 1920x1080 film in HyperFrames for AI Research & Briefing Systems, a service that watches the sources that matter, filters out the noise and writes up what changed, and why, in the client's format and voice. Make it print, in code: every frame is four plates of ink, cyan, magenta, yellow and black, each screened into round halftone dots at its own angle (15, 75, 0 and 45 degrees) and overprinted on paper, and the plates can drift out of register.
Draw every frame twice in Canvas 2D as ink coverage, cyan, magenta and yellow as red, green and blue in one canvas and black in another, with knockouts cut back to paper on both. One WebGL2 shader screens each plate on a dot grid fixed to the paper, shifts it by its own registration offset, adds a little dot gain and mottle, and multiplies the four inks over paper. Noise is dots of random sizes in cells they don't belong to. One table holds every scene, slam, lock and word, and drives both the film and the score, at 120 bpm. A "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING" label stays on screen. The score is composed in code in D minor, built like a printing press: the press is the kick, paper is the hats, and every lock clacks.
Out of one dot: start inside a single cyan dot and pull back through the halftone of a yellow disc to "YOUR SOURCES.", with the plates out of register until they lock with a clack.
Everything at once: six source tiles (a page, a feed, a site, a news page, a magnifier and a chart, all plain shapes) slam in on the beat, each wiped in from a side, under "NEWS." "SITES." "FEEDS." "COMPETITORS." Then the plates drift apart and the noise rises.
The key plate: everything collapses to black ink only, and the knowledge document draws itself line by line. "BRIEFED ON YOUR FIELD." "IT READS THIS FIRST."
The roller: colour comes back as noise, a black roller crosses the sheet and wipes it clean, and the page, the magnifier and the chart lock into register one plate at a time, on three clacks. "ONLY WHAT MATTERS." "WHAT CHANGED, AND WHY."
The press: whip down to a running web that slows to a stop on the briefing, which prints line by line, each source tile building one ink at a time. "IN YOUR FORMAT." "IN YOUR VOICE."
On schedule: the briefing flies to the first of a grid of days, a sheet is dealt onto every day, then one heavier sheet for weekly. "DAILY" "OR WEEKLY." "ON YOUR RHYTHM."
Yours: a folder. "THE CODE. THE PROMPTS." "THE KNOWLEDGE DOCUMENT. YOURS." The plates fan apart into their separations and black ink floods the sheet.
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Research & Briefing Systems", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The sources, the field and the briefing are demos, and the sources are shapes with no names. Name no weekday or time for the schedule. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, printed in code. Draw every frame as four plates of ink, cyan, magenta, yellow and black, and screen each into halftone dots at its own angle in one shader, on a dot grid fixed to the paper, overprinted on {paper_colour} paper. Let the plates drift out of register for {what_the_noise_is}, and pull them back into register for {what_gets_clear}, each lock on a downbeat. Open inside a single dot and pull back to {your_first_words}. Slam in {your_sources} on the beat, then {your_turn}. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where every lock is a clack you can hear.
```

Ideas:

- A newsletter: every issue printed plate by plate, the headline locking into register on the downbeat.
- A gig poster: the band's name slammed in four inks, out of register until the drop.
- A product launch: the product screened out of a single dot, the features dealt like sheets onto a grid.
- A data report: noisy charts out of register, and the one that matters wiped clean by the roller.

## How it's built

1. **Out of one dot.** The film opens inside one cyan dot and pulls back through the halftone of a yellow disc to the words, with the plates out of register until they lock.
2. **Everything at once.** Six source tiles slam in on the beat, each wiped in from a side, under slammed type. Then the plates slide apart and the noise rises.
3. **The key plate.** Everything collapses to black ink only, and the knowledge document draws itself line by line.
4. **The roller.** A black roller crosses the sheet and wipes the noise away, and the page, the magnifier and the chart lock into register on three clacks.
5. **The press.** A whip down to a running web that slows to a stop on the briefing, which prints line by line, each source tile building one ink at a time.
6. **On schedule.** Sheets are dealt onto a grid of days: one for every day for daily, then one heavier sheet for weekly.
7. **Yours.** A folder, then the plates fan apart into their four colours and black ink floods the sheet into the end card.

## Gotchas worth knowing

- A solid black printed as dots looks grey and weak. Add a little dot gain in the shader so full coverage prints solid and the faintest tints leave no specks.
- A dive into one dot is too fast on a linear zoom: ease it in and out, and zoom on a log scale so the pull-back feels even.
- Headlines clipped on a slot reveal can lose their last letter. Make each slot wider than the longest line, not the frame.
- Mixing plates with normal blending muddies them. Write each ink with 'lighten' into its own channel, and knock out with destination-out on every plate.
- The portrait cut can't be a crop: the tiles, the cards and the days run left to right. Lay them out again in columns and rows, with the same timings.
