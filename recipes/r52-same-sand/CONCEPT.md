# R52 · Same Sand · concept

**Style (season 8, sand on a lightbox, film 2 of 3):** the same lightbox as R51 Hands Off, with three things that film never did. The sand is poured in as a falling stream, there are two sands, the near-black sand and a warm tinted one, and the showpiece is the classic sand-animation morph: one picture flowing into the next by itself, with every grain moving and none added or taken away. R51 was about drawing and wiping. This one is about the same material taking a new shape.

**Made for:** the AI Content Systems service (ai.joaoqueiros.com/services/content-systems). Its only recipe film is R17 Prism, from the earlier Three.js run, and R33 Planner covers its live case study, the Social Media Content Calendar. This film sells the service, so it ends with the service link.

**The idea:** one brief, many formats, one voice. A sand animator never brings in new sand for the next picture. They push the same sand into a new shape. That's what the page promises: one brief goes in, and comes out as a post, an email and a caption, each with its own template, not copy-pasted across, and all in the same voice.

**Why it's a wow:** the morphs. Sand that flows from a square post into a long email, then into a short caption line and a row of carousel tiles, without a cut, and you can see the same dark sand and the same tinted streak travelling across the table each time. Then one line changes language four times without a single grain going missing.

**Beats** (about 33 s):
1. **Pour.** Black. A click, and the table lights up amber. A thin stream of sand pours from above and builds one pile. "ONE BRIEF." A small demo brief for a made-up brand is drawn into it.
2. **The voice.** A stream of the tinted sand pours into the pile and gets raked through it. "IN YOUR VOICE." Then pale grains spell out stock phrases ("IN TODAY'S FAST-PACED WORLD...") and a comb drags through and pulls them out. "ANTI-PATTERNS OUT."
3. **Formats (the showpiece).** The pile flows by itself into a square post, then into the long column of an email, then into a short caption, then into a row of five carousel tiles. Each change lands on a downbeat, and each shape is laid out differently. "ONE BRIEF. EVERY FORMAT." "NOT COPY-PASTED."
4. **Languages.** One line of the caption is written out and flows from English into Portuguese, French and Spanish, the tinted streak staying in the same words. "SAME VOICE / MESMA VOZ / MÊME VOIX / MISMA VOZ".
5. **Review.** The music drops. The fingertip from R51 comes back, the only time a hand appears. It taps two drafts to keep them, and drags a line through the third, which melts back into the pile and flows out again rewritten. "DRAFTS FOR YOUR REVIEW."
6. **A month.** The approved drafts flow out into a calendar grid of small tiles, filled square by square on the beat. "A MONTH AT A TIME."
7. **Yours.** The sand gathers back into one pile, then a document: "THE VOICE. THE PROMPTS. THE CODE. YOURS." The light clicks off. The logo is placed flat, with "AI Content Systems", the URL and "A SERVICE · THIS FILM IS CODE".

**Sound:** composed in code, the same family as R51 so the season sounds like one set, plucked strings, hand drum and filtered-noise sand, with a new voice: a soft sustained pad that swells under every morph, so the flows feel like breaths. Each morph has its own pitch rising across the formats, the language change is the melody played four times in four registers, and the review drops to the pluck alone.

**Look:** near-black sand on the amber table, with one tinted sand, a warm terracotta, that stays visible as a streak inside every shape. That streak is the voice, and it's the only colour in the film apart from the logo, which sits flat on dark as it must. Words are part of the sand. A small flat label stays on screen for honesty.

**Honesty rules:**
- Facts come only from the service page: voice calibration and an anti-pattern library built before anything is automated, a pipeline that takes a brief and produces drafts in your voice, separate templates per platform ("not copy-pasted across"), output in English, Portuguese, French or Spanish with the voice kept across translations, drafts for human review with approve, reject or rewrite, a month of content drafted at a time, and source code, prompt library, voice document and documentation handed over.
- A label stays on screen: "AI CONTENT SYSTEMS · DEMO BRIEF". The brand, the brief and every draft are fictional. The end card says "A SERVICE · THIS FILM IS CODE".
- The review beat never claims nothing can ever publish without a person. The page lets publishing be automated for low-risk content if the client chooses, so the film says "drafts for your review", which is the page's default, and the copy says so.
- No results: no engagement numbers, no time saved, no prices, no build times, no client work and no claims about any client.
- No third-party names or logos: platforms are shown only as shapes (a square, a column, a line, a row of tiles), never by name or logo, and the model providers and tools on the page stay off screen.

**Generated, not in the repo:** `assets/table.js`, `assets/bgm/score.wav`, renders.

**How the film differs from the first idea:** the sand is 240,000 grains, not a height field. A first build moved a height field along a pressure flow, and it pinched into blobs or turned into a fade. So now 200,000 dark grains are poured, then 40,000 tinted ones, and no grain is ever added or taken away after that. Each picture is sampled as grain positions. Every grain is matched to the next picture by sliced optimal transport, and then to an exact spot in it along a Hilbert curve, so each flow travels the short way and lands exactly on the beat. The grains are splatted into a height map and lit as in R51. Every frame is worked out from the time alone. The film is 36.25 s at 96 bpm, and the tick, the tick and the strike at the review push grains aside into ridges.
