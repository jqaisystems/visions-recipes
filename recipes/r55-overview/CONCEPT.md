# R55 · Overview · concept

**Style:** a field of 61,440 steel pins (192 by 320) in code, but in 3D and in flight. A camera is in the air: it skims the pins at head height, flies over words as they rise ahead of it, drops into the noise, cranes straight up to a bird's-eye view and dives back down to track along the briefing. Nothing is drawn on top: every word, source and day is pins rising out of the field, steel or brass.

**Made for:** the AI Research & Briefing Systems service (ai.joaoqueiros.com/services/research-briefing), its third film after R18 Loom and R54 Register. This film sells the service, so it ends with the service link.

**The idea:** perspective. From the ground, the sources are noise; from above, they're a briefing. The service is the overview: it reads the field, keeps what matters and writes it up.

**Why it's a wow:** a camera flying through a landscape of real metal, words rising out of the ground as it arrives, ripples running out through the pins from every word that lands, a crane shot that settles the noise from the middle out, brass pins among the steel for what matters, and a final pull-out to the whole field in its frame.

**Beats** (36.4 s, 112 bpm, 68 beats):
1. **Ground level.** Black, then a low lamp comes on over a field of pins at head height. The camera lifts off: "YOUR SOURCES."
2. **The flight.** It flies over "NEWS." "SITES." "FEEDS." "COMPETITORS.", each word rising just ahead of it on the beat with a ripple, the sources (a page, a feed, a site, a magnifier, a chart) rising alongside.
3. **Down here.** It drops low into the noise, the sources slamming up all around: "FROM DOWN HERE," "IT'S ALL NOISE."
4. **From above.** A crane straight up to a bird's-eye view while the noise settles from the middle out: "FROM ABOVE," then the knowledge document rises: "BRIEFED ON YOUR FIELD."
5. **The filter.** The sources pop up around it, everything that doesn't matter drops, and the page, the magnifier and the chart turn brass and slide into a column: "ONLY WHAT MATTERS." "WHAT CHANGED, AND WHY."
6. **Written up.** A dive down to a low angle: "IN YOUR FORMAT.", then the briefing rises line by line next to its brass bullets, and the camera pulls back to read it whole: "IN YOUR VOICE."
7. **On schedule.** A grid of days: daily, the briefing rises on every day in turn; weekly, once, taller and in brass. "DAILY OR WEEKLY." "ON YOUR RHYTHM."
8. **Yours.** A brass folder: "THE CODE. THE PROMPTS." "THE KNOWLEDGE DOCUMENT. YOURS." The camera pulls all the way out to the whole field in its frame, and the lamp goes off. The logo is placed flat, with "AI Research & Briefing Systems", the URL and "A SERVICE · THIS FILM IS CODE".

**Sound:** composed in code, the metal family of the season: pins rising are a wash of tiny ticks as dense as the pins moving. The flight runs on a pulse like a press, every word that lands slams (a knock, a clang of steel and a burst of pins), the camera's dashes are air, the noise is a clatter on the sixteenths, the crane up is one long rising sweep landing on an open chord, brass rings warmer than steel, and the briefing is a tune on struck metal, one note per line.

**Honesty rules:** facts come only from the service page; the sources, the field and the briefing are a demo and a label says so; the sources are shapes with no names; no third-party names or logos; no prices, build times, results or client work; the service page's case study is never referenced, so the schedule is a generic grid of days with no named weekday or time.

**Generated, not in the repo:** `assets/table.js` (the camera per frame, the layers), `assets/bgm/score.wav`, renders, `work/`.

**How it's built:** every pin's height and brass are worked out from the time alone and uploaded as one 192 by 320 texture each frame. One WebGL2 shader traces a ray per pixel through the grid of pins, cell by cell, to the first domed head or shaft, then a second ray back towards the lamp for a soft shadow; heads are lit steel or brass reflecting a dark room with a warm glow, shafts sit in the shade so raised words read by their tops. A second pass adds depth of field focused where the camera looks, a glow on the glints, grain and a vignette. The camera is a smooth spline through keys, each framed on the caption it's looking at, and baked per frame in the table. Words clear the noise a few pins around them so they always read.
