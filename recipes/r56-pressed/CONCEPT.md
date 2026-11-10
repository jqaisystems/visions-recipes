# R56 · Pressed · concept

**Style:** the pin-art toy, in code. A wall of about 40,000 steel pins in a frame, lit by one low raking light, and every picture is a relief pressed into it from behind. Nothing is drawn on top: every shape, every word and the end card are pins sliding forward and back, with their own shadows and highlights. The light is part of the look: it travels across the wall, so the same relief reads differently as the shadows swing round.

**Made for:** the AI Research & Briefing Systems service (ai.joaoqueiros.com/services/research-briefing). Its films are R18 Loom, from the early Three.js run, R54 Register, print in code, and R55 Overview, the same steel pins with a camera in flight; this is its fourth. This film sells the service, so it ends with the service link.

**The idea:** the world presses in from every side, and the system decides what leaves a mark. On the wall, the sources are reliefs pushed in all at once until the surface is noise. The service flattens what doesn't matter and presses up only what does, until the wall holds one clean briefing.

**Why it's a wow:** the light on metal. Tens of thousands of pins rising in waves, each casting its own shadow, a raking light sweeping across a relief so it seems to turn in 3D, and words that are physically pushed up out of the wall. Then the whole wall breathes flat in one wave, and only the briefing stays standing.

**Beats** (38 s):
1. **The wall.** Black, then the raking light comes on across a flat wall of pins. A ripple runs through it like a breath. "YOUR SOURCES."
2. **Pressed in from everywhere.** Reliefs push in from behind, one after another and then all at once: a page, a feed, a site, a magnifier, a chart. They overlap until the wall is a field of noise, pins jittering at every height. "NEWS. SITES. FEEDS. COMPETITORS."
3. **What you know.** One structured page is pressed in softly underneath everything, its rows and headings faint but steady: the knowledge document. "BRIEFED ON YOUR FIELD." "IT READS THIS FIRST."
4. **The filter (the showpiece).** A wave sweeps across the wall and flattens the noise, pin by pin. Only a few shapes are left standing, and they slide together into groups. "ONLY WHAT MATTERS." "WHAT CHANGED, AND WHY."
5. **Written up.** The groups melt into lines of relief text, pushed up out of the wall as a short briefing in a house layout: a heading, three tight items, each with its why. The light sweeps across it once so it reads. "IN YOUR FORMAT. IN YOUR VOICE."
6. **On schedule.** The wall becomes a grid of days. The same briefing presses up on its day, again and again, on the beat, while the noise between days stays flat. "ON YOUR RHYTHM."
7. **Yours.** The wall settles. A folder presses up at the edge: "THE CODE. THE PROMPTS. THE KNOWLEDGE DOCUMENT. YOURS." The light slides off the wall. The logo is placed flat, with "AI Research & Briefing Systems", the URL and "A SERVICE · THIS FILM IS CODE".

**Sound:** composed in code from metal. Pins rising are a soft wash of tiny ticks, like rain on a tin roof, whose density follows how many pins are moving. The noise beat is dense and clattering, the filter wave is one long falling sweep of ticks that leaves near silence, and the briefing is a tuned melody on struck metal (a celesta-like tone), one note per line as it rises. A low pulse marks each day in the schedule.

**Look:** dark steel pins with rounded heads in a black frame, one warm raking light and a faint cool fill, real cast shadows from pin to pin, and a shallow depth of field so the far edge of the wall falls soft. Reliefs are shapes only. A small flat label stays on screen for honesty.

**Honesty rules:**
- Facts come only from the service page: monitoring the sources that matter (news, sites, feeds, competitors, your industry); a curation pass on which sources and topics matter; domain knowledge embedded as a structured document the model reads before it reads the news; filtering the noise, grouping what matters and summarising what changed with the why-it-matters; written up in the client's format and voice; delivered on a daily or weekly rhythm; source code, prompts, the knowledge document and documentation handed over, and the client owns it.
- A label stays on screen: "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING". The sources, the field and the briefing are fictional: the briefing is short, readable demo copy about a made-up topic. The end card says "A SERVICE · THIS FILM IS CODE".
- No third-party names or logos: the sources are shapes only, and no news outlet, platform, delivery app or model provider is named or hinted by a logo. The feed relief is a plain set of lines, not a product's icon.
- No results: no hours saved, no prices, no build times, no warranty length and no client work. The service page's case study is never referenced, in the film or the copy, so the schedule beat shows a generic grid of days, not a named weekday or time.

**Generated, not in the repo:** `assets/table.js` (the heights over time), `assets/bgm/score.wav`, renders.

**How it's built:** 36,864 pins (256 by 144, 7.2 px apart), every height worked out from the time alone and drawn in one WebGL2 shader: each pixel finds the frontmost pin, its shaft and domed head in a slight perspective from a camera above the wall, and traces its shadow back towards the lamp through the heads of the pins in between. Raised pins catch more of the lamp, so the reliefs read by light and not by outline. Every picture is a layer drawn once at four samples per pin, with its own timing and its own direction for the pins to follow (left to right, top down, from the middle, or scattered). The kept sources (the page, the magnifier and the chart) slide and shrink to become the bullets of the briefing. The briefing is about a made-up field: a safety standard, a rival's service page and two tenders. The schedule is two weeks of days: daily, the briefing lands on all seven in turn; weekly, on the first day only. 100 bpm, 64 beats, 38.4 s.
