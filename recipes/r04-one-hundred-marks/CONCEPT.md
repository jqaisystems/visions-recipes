# R04 · One Hundred Marks, One Line · concept card (approved by João 2026-10-22: Marks book, traced silhouettes, 100 marks, pipeline-only source, JQ mark ending)

**Style (reusable):** One Line. A single stroke never lifts off the page: it closes into the outline of one
mark, then slides straight into the next, a hundred times, faster and faster, and finally settles on one.
Anyone can swap the shapes for their own icons, products, letters or maps.

**Subject:** Marks, the 160-page book of 398 identities (joaoqueiros.com/marks). The page's own numbers:
398 identities, 160 pages, five forms (symbols 126, emblems 98, lettering 81, families 52, monograms 41),
twelve years, 2014 to 2025. Its tagline: "398 identities · 160 pages · one book".

**Why it isn't a repeat:**
- The Marks page already has a 52-second film and a "Drawn, path by path" chapter that redraws five marks
  over their construction guides. R04 doesn't draw strokes in: it is one unbroken outline that changes
  shape, a hundred marks in one breath.
- /code 012 One Line is a teal line travelling through scenes. R04 is a closed contour that morphs in place,
  on paper, in ink.

**Story in one line:** an empty page and a pen line. The line closes into the Digitalift bird, then flows
into the next mark, and the next, a hundred identities in one stroke. It slows, opens, and signs off as the
JQ mark, with "Marks" set beside it.

**Spec:** about 26 s, 16:9 1920×1080, 30 fps. Score composed in code: pencil on paper (a filtered noise
scratch that follows the line's speed), one soft paper tick per mark, rising as the pace quickens, and a
calm piano-like close on the lockup. Same MIT source routine on GitHub.

**Look:** the book itself. A warm paper page (#F7F5F0), one ink line (#151515), small grey captions in the
book's style ("033 · Rancho Monte Alegre · Symbol · page 20"), the "Marks" serif title for the lockup.
A light film after three dark ones (R01 to R03 are all black). Technique: SVG, one `<path>`, every outline
resampled to the same number of points so any mark can morph into any other.

## How the outlines are made (needs your OK)
- There are no vector files for most marks online, only the 640 px images on the Marks page (the six SVGs
  there cover just five client marks plus the JQ mark). So: take each public image, keep the symbol (crop
  off the wordmark), threshold it, close small gaps, and trace its outer edge into one contour. A silhouette,
  not the detailed drawing. Then resample every contour to ~600 points and rotate each one so its start point
  lines up with the previous mark's, which keeps the morph from twisting.
- 100 marks from the symbols, emblems and monograms (they have a strong outer shape; lettering doesn't
  trace well). Chosen by readability as a silhouette, in book order.
- Only marks that are already public on the Marks page. Never the client folders on this machine. Never
  Veriti (035), as the backlog says.

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 3 s | Paper. A pen point draws one horizontal line across the page. | stroke-dashoffset draw |
| 3 to 7 s | The line curls and closes into 002 Digitalift's bird. Hold; caption "002 · Digitalift · Symbol · page 4". | point-matched morph |
| 7 to 17 s | It flows from mark to mark, one every 0.5 s, then quicker, down to about four a second. Caption counts "014 / 100", mark names flick by. | eased morph chain, one path |
| 17 to 21 s | It slows on the last few, then opens and settles into the JQ mark. | slower morph, ease out |
| 21 to 26 s | Lockup: JQ mark, "Marks", "398 identities · 160 pages · one book", joaoqueiros.com/marks. | type fades, one eased drift |

## The source on GitHub (needs your OK)
The client marks are their owners' trademarks, so they can't go in an MIT repo. The zip ships the whole
pipeline (tracer, morph, score) plus the JQ mark and twelve plain demo shapes, and the README says: drop in
your own SVGs or PNGs and run the tracer. The film itself still shows the real marks. This matches the
recipes rule (only your own work in the source).

## Open choices for João
- Subject: the Marks book (recommended).
- Outlines traced from the public images as silhouettes (recommended), or fewer marks (say 40) that I
  trace more carefully.
- Count: 100 marks (recommended, the title promises it), or all symbols and emblems (224) in the same 10 s
  for a blur at the end.
- Source: pipeline + JQ mark + demo shapes, no client marks (recommended).
- Ending: the JQ mark (recommended), or the "Marks" book cover.
