# R33 · Planner · concept (as built)

**Style (season 4, film 2 of 4): paper cut-out stop motion.** It uses the same engine as R32 Pinned: torn-edge cut paper
with stocks generated from noise, layer shadows from a tabletop light, poses on twos with edge boil, a stepped camera
and multiplane parallax, all on one Canvas 2D, with `paint(t)` drawing every frame from one baked table.

To stop it reading as Pinned again, it changes three things.
- **A different set:** a pale birch desk with a felt-lined desk blotter, a mug of pencils, a stamp pad and a stapler.
  Pinned had a green cutting mat with scissors. The palette moves to navy, mustard, coral and cream, with no teal or
  terracotta lead.
- **Different paper mechanics:** Pinned cut and pinned. This film works by lift-the-flap, a volvelle (a paper wheel),
  an accordion fold, a rubber stamp and a tractor-feed printout. Every paper move is new to the season.
- **Its own camera:** a slow top-down crane over the whole spread, where Pinned used stepped close-ups. It pushes in
  only twice, on the variety check and on the export.

**Made for:** the Social Media Content Calendar (ai.joaoqueiros.com/systems/content-calendar), João's internal system
that plans a month of posts from one brand brief. Its own line is "A month of posts, in 10 minutes." It has never
had a film.

**The idea:** a month of social media built as a paper planner on a desk. One brief goes in. It turns into four
weekly themes, then thirty days of post cards, and then a printout ready to schedule. Every step on the desk is a
step the system really does.

1. **The brief (0 to 4 s).** A paper form slides onto the blotter. Pull tabs slide out one at a time with the brief's
   fields: voice, audience, goals, themes, highlights, frequency per platform. Each tab's value is a word on its own
   paper strip. "One brief in,"
2. **Four themes (4 to 9 s).** A paper volvelle (a wheel on a split pin) turns four clicks, and at each click a
   theme banner unrolls from it like a paper streamer. Each banner has a headline and a one-line rationale. The four
   banners build left to right toward the month's goal. "Four weeks, each with a reason."
3. **Thirty days (9 to 15 s).** An accordion of card unfolds across the desk into a month grid, five rows of
   flaps. The flaps lift on the beat in a wave. Under each one is a small post card with a caption line, hashtags, a
   CTA and a pencil sketch of the suggested visual. Each card has a paper corner colour for its platform:
   Instagram, LinkedIn and Pinterest are named in type only, with no logos or brand colours. "Every platform, in its
   own voice."
4. **Variety check (15 to 21 s).** The camera pushes in. A rubber stamp marked REPEAT HOOK slams onto a card whose
   hook repeats an earlier one. The card crumples and is rolled off the desk, and a new card slides in under the
   flap. A second stamp, SAME CTA, does the same thing. Then a week holding three cards of one format gets one of
   them swapped. "No repeats."
5. **CSV out (21 to 27 s).** The month folds back up. Its cards feed into a paper printer, and a tractor-feed strip
   with sprocket holes scrolls out, printed with one row per post: date, platform, caption, hashtags, CTA, visual.
   "One row per post."
6. **Reviewed (27 to 29 s).** A pencil ticks down the margin of the printout, the human review the system expects
   before scheduling. The strip tears off at the perforation.
7. **Title (29 to 33 s).** The torn strip folds into a paper plane and flies off. A black sheet sweeps the desk, and
   the JQ AI SYSTEMS logo lands flat, never redrawn or recoloured. Then come "Social Media Content Calendar", its
   line and ai.joaoqueiros.com/systems/content-calendar.

**Score:** composed in code, about 108 bpm and brighter than Pinned's:
- marimba, felt piano and a light shaker;
- tab slides, volvelle clicks, a flap riffle, stamp thuds, a crumple and the printer's chatter, all on the beat;
- the paper plane's whoosh into a major chord and a bell on the logo.

**Honesty and brand:**
- **The brand in the brief.** I recommend running the system for real on João's own brand. The best choice is JQ
  VISIONS, with a month launching the recipe library, so every theme, caption, hashtag and CTA on screen is real
  output, shortened to fit and never rewritten. This needs João to point me to the system's folder, or to send a
  CSV it made. The fallback is a sample brief marked "sample brief, illustrative" in the concept card and the recipe
  copy. **As built:** no system output was found on disk, so the film uses the fallback: a sample JQ VISIONS brief
  launching the recipe library, labelled "JQ VISIONS · sample brief" on the form and illustrative in the copy. The
  bake checks the sample against the system's own rules (no hook or CTA twice, never three posts of one format in a
  week).
- **Facts used on screen:** 30 days, four weekly themes with a rationale each, three platforms, one row per post, and
  a human review before scheduling. These are how it works, not results.
- **Kept off screen:** "4h → 10m", "under 15 minutes" and any other time or volume claim. The tagline "A month of
  posts, in 10 minutes." is the system's own line, and João decides whether the end card uses it. Without it, the end
  card reads "One brief in, a month of posts out." **As built:** the end card uses "One brief in, a month of posts
  out"; the tagline stays off screen and out of the social copy.
- **Third-party names:** no Instagram, LinkedIn, Pinterest, Buffer, Later or Notion logos or colours. The platform
  names appear as type only.
- The JQ AI SYSTEMS logo is the official file, placed flat.

**Cuts:** 16:9, plus a 9:16 vertical re-laid out for portrait, not cropped. About 33 s. **As built** (33.3 s at 108
bpm): in the vertical the theme banners stack under the volvelle, the month stands on end with a column per week and a
row per weekday, the accordion opens sideways, the banners shrink to the heads of the week columns, the folded month
turns on its side into the printer, and the printer sits low so the whole CSV stands in frame
(`videos/planner-vertical`).

**Stack:** HyperFrames 0.8.184 · Canvas 2D · GSAP · Python (table, score). The film forks R32's engine:
`piece()`, the stocks, the light, the boil and `camAt`.
