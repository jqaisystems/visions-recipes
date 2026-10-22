# R03 · Signal from Noise

**Style:** thousands of small fragments behave like iron filings. A field switches on and they turn, line up and
gather around the poles that matter, and the strongest few are pulled out into one reviewed list.
**Made for:** AI News Curator, JQ AI SYSTEMS (ai.joaoqueiros.com/systems/ai-news-curator).
**Length:** 26 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · HTML · Canvas 2D · GSAP (one clock) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames for AI News Curator, my research briefing workflow.
Story: about 6,000 short fragments drift as noise, a few labelled only with source types (github · release,
newsletter, docs update, saved link, community note, social post). "Scattered signals," types over them.
Then a field switches on: every fragment turns to face it and slides onto the field lines of two magnets,
like iron filings. The field splits into six alternating poles, one per real theme (AI tooling, Coding
workflows, Design systems, Automation patterns, Public GitHub work, Client research), and the filings flow
into them, turning teal near each pole. The brightest fragment of each theme flies to the centre and becomes
one row of a "Daily brief" card. A gate line scans down the card and gives each row its review outcome
(public content, private research, client context, archived note), then "Nothing is published
automatically." The field settles into archive rows by day. End on "Scattered signals, daily briefings."
and the case study URL. The status line names the real steps: import, normalize, classify, brief, review, archive.
Technique: Canvas 2D only. Trace the field lines once at load from point charges (E = q r / |r|^2), give every
fragment a noise state, a dipole state, a six-pole state and an archive state, and blend between them with
seeded per-fragment delays. One painter computes every frame from time; no simulation state.
Brand: #111110 background, #F5F5F0 bone, #00A89D teal, iron grey #6E6E68, Geist, Geist Mono, Instrument Serif.
Score: compose it in code with numpy: metallic grains for the filings, a thunk and a magnetic hum when the
field switches on, a struck tone per theme, a pop per row, a scan for the review gate, from the same timing table.
Public-safe: no real links, no headlines, no sources.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames.
{n} fragments labelled {fragment_labels} drift as noise while "{opening_line}" types.
A field switches on and they line up like iron filings, then gather around {k} poles: {pole_names}.
The strongest fragment of each pole flies into {summary_object}, which {review_step}.
The rest settles into {archive_shape}. Close on {final_line}.
Canvas 2D, field lines traced once, every fragment blended between states from time.
Palette: {palette}. Fonts: {fonts}. Score composed in code with metallic grains, synced to the picture.
```

Ideas: support tickets gathering around product areas into a weekly triage, job applications sorting into a
shortlist, customer feedback clustering into a roadmap, photos from a shoot filing themselves into a selects board.

## How it's built

1. **Field lines, traced once.** Two charges, then six with alternating signs. From each charge, 30 to 46 lines
   are traced with a midpoint step along the field and stopped at another charge or the frame edge. Every
   fragment takes one point on one line.
2. **Four states per fragment.** Noise (seeded sines), dipole, six poles, archive. The painter blends position and
   angle between them with per-fragment delays, so the alignment ripples outwards from the centre. Angles blend
   modulo π, because a filing has no head or tail.
3. **6,000 lines in a few strokes.** Each fragment's colour and alpha are rounded into one of about 120 buckets,
   and each bucket is one path and one stroke, so a frame costs a few canvas calls.
4. **Signal leaves the field.** The six brightest fragments are drawn as a teal streak from their pole and become
   HTML rows on the card, which the review gate then tags.
5. **Sound from the same clock.** Metallic grains whose density follows the alignment, a hum that opens as the
   field turns on, struck tones for the themes and a scan for the gate, all generated in Python.

## Gotchas worth knowing

- A canvas draws text with whatever font is loaded at that moment. Load the web font and repaint once it is ready.
- Flex rows in a table-like card shrink their columns unevenly when the content is too wide. Set `flex: none` on
  the cells and size the row for its longest label.
- Seeded randomness (mulberry32) instead of `Math.random()`, or every render scatters the filings differently.
