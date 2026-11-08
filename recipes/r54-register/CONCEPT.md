# R54 · Register · concept

**Style:** print, in code. Every frame is four plates of ink, cyan, magenta, yellow and black, each screened into round dots at its own angle (15°, 75°, 0° and 45°, as on a press) and overprinted on paper. Nothing is a flat colour: a gradient is dots growing, a green is cyan dots over yellow, and black type is a solid plate. The plates can drift out of register, and that drift is the story.

**Made for:** the AI Research & Briefing Systems service (ai.joaoqueiros.com/services/research-briefing). Its first film is R18 Loom. This film sells the service, so it ends with the service link.

**The idea:** out of register, the world is noise. The system pulls it into register: sharp, aligned, printed, on schedule.

**Why it's a wow:** it's a motion design showreel in one material. A camera pull-back out of a single cyan dot, the plates snapping into register on the beat, slammed kinetic type over tiles wiped in from four sides, a black-only key plate scene, a roller wiping the noise away, a whip down to a running press web that slows to a stop, a briefing that prints colour by colour, sheets dealt onto the days, the plates fanning apart into their separations, and an ink flood into the end card.

**Beats** (37 s, 120 bpm):
1. **Out of one dot.** The film opens inside a single cyan dot, pulls back through the halftone of a yellow disc to "YOUR SOURCES.", with the plates out of register; they lock with a clack.
2. **Everything at once.** Six source tiles (a page, a feed, a site, a news page, a magnifier, a chart) slam in on the beat, each wiped in from a side, under "NEWS." "SITES." "FEEDS." "COMPETITORS." Then the tiles drift, the plates slide apart and the noise rises.
3. **The key plate.** Everything collapses. Black ink only: the knowledge document drawn line by line. "BRIEFED ON YOUR FIELD." "IT READS THIS FIRST."
4. **The roller.** Colour comes back as noise. A black roller crosses the sheet and wipes it clean; what's left (the page, the magnifier and the chart) locks into register one plate at a time, on three clacks. "ONLY WHAT MATTERS." "WHAT CHANGED, AND WHY."
5. **The press.** A whip down to the press: the web runs and slows to a stop on the briefing, which prints line by line, each source tile building plate by plate. "IN YOUR FORMAT." "IN YOUR VOICE."
6. **On schedule.** The briefing flies to the first of a grid of days. Daily, a sheet is dealt onto every day; weekly, one heavier sheet. "DAILY" "OR WEEKLY." "ON YOUR RHYTHM."
7. **Yours.** A folder. "THE CODE. THE PROMPTS." "THE KNOWLEDGE DOCUMENT. YOURS." The plates fan apart into their separations, black ink floods the sheet, and the logo is placed flat with "AI Research & Briefing Systems", the URL and "A SERVICE · THIS FILM IS CODE".

**Sound:** composed in code, a printing press at 120 bpm: the press is the kick, paper is the hats, a bass line in D minor, a hit on every slam, a clack of metal on every lock, air on the whips, a rumble that crosses the stereo field under the roller, static under the noise, a stamp and a bell for each line of the briefing, a flick for each sheet dealt.

**Honesty rules:** facts only from the service page; the sources, the field and the briefing are fictional (a safety standard, a rival's service page, two tenders), with "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING" on screen; no third-party names or logos (the sources are plain shapes); no results, prices, build times or warranty; the case study is never referenced, so there's no named weekday or time.

**How it's built:** each frame is drawn twice in Canvas 2D as ink coverage (cyan, magenta and yellow as red, green and blue in one canvas, black in another, knockouts cut back to paper on both), then one WebGL2 shader screens each plate, shifts it by its registration offset and multiplies the four inks over paper with a little mottle and dot gain. The dot grid is fixed to the paper, so the camera can dive into a single dot. The noise is dots of random sizes in cells they don't belong to, cleared behind the roller.

**Generated, not in the repo:** `assets/table.js`, `assets/bgm/score.wav`, renders.
