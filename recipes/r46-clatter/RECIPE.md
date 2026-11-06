# R46 · Clatter

**Style:** a physical split-flap wall. 30,000 instanced tiles in WebGL2, each with two halves, a falling flap and box sides,
driven by one schedule of every flap. The same schedule drives the score, so every flap you see is a click you hear.
**Made for:** the AI Client Acquisition System, two internal tools that find and score businesses and write an email for a person to approve or reject.
**Length:** 34.29 s · 1920×1080 · 30 fps, with a 9:16 cut on its own wall of 180 by 190 tiles.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (schedule, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 34.29-second 1920x1080 film in HyperFrames for the AI Client Acquisition System, two internal tools that find businesses,
score them from 0 to 100 with a written reason and draft an email for a person to approve. Make it dynamic motion design, a showreel
piece. The funnel is a physical wall of 300 x 100 split-flap tiles in WebGL2, five boards of 100 rows, so each 60-tile row is one of 500
fictional businesses. Every tile is instanced geometry with two halves, a falling flap and box sides, with 4x multisampling, motion across 4
sub-frames, depth of field, a travelling glint and ACES. One Python schedule writes every flap as an event; only tiles that change will flip.
112 bpm, 64 beats. Dark tiles, bone #F2EEDC, orange #FF5A1F, Archivo at 800 condensed for words made of tiles. Every flap in the schedule is one click in the
score, panned by its column, ringing through tuned resonators. All businesses, towns, scores and emails are fictional and labelled DEMO DATA.
One tile: macro, one flap falls, then "500 COLD RESULTS." is written tile by tile.
The search: rows arrive from the middle out as the camera pulls back to all 500.
Words: SEARCH and SCORE push out of the wall, their tiles still carrying the rows, with their sub-lines.
Scores: a raking camera while every score spins and settles, with a band beside it.
The drop: one held breath, rows below 40 flip away in a shockwave. "BELOW 40: FILTERED OUT". The rest go and 30 stay. "30", "QUALIFIED, OUT OF 500".
One business: macro along TIDAL BAKERY, the 87 and "NO WEBSITE. SOCIAL PAGE ONLY.", labelled fictional.
The flip: an orange shockwave from the score. "SOMETHING SPECIFIC ABOUT THEM."
The draft: the wall types an email labelled "DRAFT · NOT SENT · DEMO TEXT". APPROVE lights up, another row is marked REJECTED and flips away. "YOU DECIDE WHAT GOES OUT."
Never twice: a fresh search crosses the wall and six CONTACTED rows don't change. "NO PROSPECT EMAILED TWICE."
Close: the wall empties towards the first tile, the last flap falls, and the logo lands flat, never redrawn or recoloured, with the system's name, the URL and "INTERNAL SYSTEM · DEMO DATA".
Take facts only from the case study. Claim no replies, clients or revenue, and don't imply it's for sale or that emails send themselves.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose story is {the_story}, set on a physical wall of split-flap
tiles in WebGL2, each one instanced geometry with a falling flap. Keep one schedule of every flap, so only tiles that change will flip, and make
each row {one_record}. Push {your_words} out of the wall with the data still on their tiles, let {the_big_change} cross it as a shockwave after
one held breath, and let the wall type {your_message} itself. Make every flap one click in the score, panned by its column and ringing through
resonators tuned to {your_key}, at {bpm} bpm. End on one last flap and {your_mark}, placed flat, with {line} and {url}.
```

Ideas:

- A rail or airline brand: the departure board itself, rewriting into the campaign line.
- A band's tour film: dates clattering across a station wall, then the album title pushed out of it.
- A finance or data newsroom: a live table that reorders itself into the headline.
- A language school: one sentence flipping through every language it teaches.

## How it's built

1. **One flap.** Macro, one tile, one click. Then a sentence, written tile by tile, each letter a sound.
2. **The search.** Rows arrive from the middle out, on the sixteenth, while the camera pulls back from one tile to all 500 rows.
3. **Words made of the data.** SEARCH is a mask over the wall. Its tiles turn orange and push forward but keep their rows' letters, so the word is made of the businesses.
4. **Scores spin.** A raking camera runs along the wall as every score rolls through random values on a sixteenth and settles, with its band beside it.
5. **The drop.** One held breath, then a wave from the centre flips the rows below 40 to blank, and you hear it cross the speakers.
6. **One business.** Macro along TIDAL BAKERY, then the 87 lands in orange and its written reason types itself below.
7. **A person decides.** The wall types a draft labelled NOT SENT. APPROVE lights, another row is marked REJECTED and flips away, one tile at a time.
8. **What doesn't change.** A fresh search crosses the wall, flipping every row but six. In a film full of movement, the still rows are the message.

## Gotchas worth knowing

- Max-normalising a click track buries the single clicks at -60 dB. Use a density gain, and check each section's level.
- Events are time-sorted, so a later wave will overwrite a word that landed first. Land words after waves have finished.
- A big glint on 30,000 small tiles becomes a blob at distance. Fade it out as the camera pulls back.
- Words have a maximum width: work out what fits at your widest camera before you schedule them.
- A row of random fictional data can still hold a real product name. Search everything you put on screen.
