# R32 · Pinned · concept

**Style (season 4, film 1 of 4): paper cut-out stop motion.** Seasons 1 to 3 were cel-shaded anime, SVG vector and a
raymarched shader. This one looks made by hand on a tabletop and shot frame by frame, all drawn in code on one Canvas
2D:
- **Cut paper, not vectors:** every piece is a cut path with a jittered, slightly torn edge, filled with a paper fibre
  texture generated from noise, in a few stocks (kraft, cream, coloured card, newsprint).
- **A real tabletop light:** each layer sits at a height above the table and casts a soft offset shadow that grows
  with that height, so a piece lifting off the table reads as lifting.
- **Shot on twos:** time is snapped to 12 poses a second, and every piece re-cuts its edge a little on each new pose
  (the "boil" of replaced paper parts), so it moves like stop motion, not like a tween.
- **Pop-up mechanics:** boards rise out of a folding spread like a pop-up book: V-folds and parallel folds worked out
  from the page angle.
- **A multiplane camera:** foreground, set and background layers pan at different rates, with a soft focus on the far
  layers.

Type stays HTML over the canvas, set as if cut from newsprint and card. `paint(t)` draws every frame from one baked
table, so any frame can be seeked.

**Made for:** Etsy to Pinterest (ai.joaoqueiros.com/systems/etsy-to-pinterest), João's internal pipeline that turns Etsy
listings into Pinterest-ready image and video pins. Its own line: "Etsy media in, Pinterest queue out". It has never
had a film.

**The idea:** the pipeline is a craft table. A listing comes in, gets cut into pins, labelled, pinned to the right
board and put on the calendar, while the videos take their own careful path. Everything you see is a step the system
really does.

1. **Listing in (0 to 4 s).** A paper shop listing slides onto the kraft table, João's own Kayak hoodie listing, its real
   photos printed as paper prints ("Kayak Hoodie Graphic Pullover for Outdoor Lovers"). "Etsy media in,"
2. **Media split (4 to 9 s).** The listing's gallery fans out as paper photos. Paper scissors snip out the listing's real size chart
   and colour chart (the system made no pins from them), which flutter off the table. A filmstrip peels away from the photos and slides to one side:
   images one way, video the other.
3. **Cut to pins (9 to 14 s).** Each photo is trimmed by scissors along a dotted line into a tall 2:3 pin. A tag
   unfolds from each with its own title, description and alt text, every one different. "A unique pin for every
   image."
4. **Boards (14 to 19 s).** A spread opens and two boards pop up, "Kayak and Paddle Gear" and "Kayak Life &
   Outdoor Gifts" (the boards these pins really went to). Pins fly over and pushpins press them onto the board each one matches.
5. **Schedule (19 to 24 s).** A week of paper calendar strips slides in, and pins drop into posting slots with gaps
   between them, never two together. A paper clock hand ticks round between checks.
6. **Video queue (24 to 28 s).** The filmstrip folds into a 9:16 frame, gets a cover card, and slides into a folder
   marked "ready_manual". "Video pins stay manual, by design."
7. **Title (28 to 33 s).** "Pinterest queue out." The table clears piece by piece, and the paper settles into the JQ
   AI SYSTEMS logo, flat, never redrawn or recoloured, then "Etsy to Pinterest" and
   ai.joaoqueiros.com/systems/etsy-to-pinterest.

**Score:** composed in code, about 100 bpm, warm and tactile:
- plucked kalimba and muted upright bass over a brushed beat;
- paper slides, scissor snips, pushpin clicks and a calendar flip, all on the beat;
- a clock tick under the schedule;
- a major chord and a bell on the logo.

**Honesty and brand:**
- João's own listing: their design, photos, charts, video and cover, and the pin titles, alt text and boards the
  system wrote (alt text shortened to fit). The model shots are João's mockups, cleared for promo. The schedule
  times are illustrative. No counts, no statuses and no results (the page's "88+" stays out).
- The listing media is not in this repo: add your own (`assets/img/README.md`).
- No Etsy or Pinterest logos, marks or brand colours. The names appear only as the system's own name and line.
- The steps on screen are steps the system really does: import, exclude non-pin images, crop to 2:3, a unique title,
  description and alt text per image, board matching, scheduled slots with gaps, and a separate manual video queue.
- The JQ AI SYSTEMS logo is the official file, placed flat.

**Cuts:** 16:9 and a 9:16 vertical (re-laid out, not cropped). About 33 s.
