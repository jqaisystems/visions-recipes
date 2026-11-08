# R52 · Same Sand

**Style:** sand animation on a lightbox, in code. The sand is 240,000 grains, matched from one picture to the next by sliced optimal transport and then exactly along a Hilbert curve,
added into one WebGL2 height texture and lit from below, so thin sand breaks into grains and thick sand stops the light. Every frame is worked out from the time alone. No footage and no 3D engine.
**Made for:** AI Content Systems, a service: content pipelines that take a brief and draft it in your voice, for your review, where the client keeps the code, the prompts and the voice document.
**Length:** 36.25 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 36.25-second 1920x1080 film in HyperFrames for AI Content Systems, a service that builds content pipelines which take a brief and draft it in your voice. Make it a sand animation on a lightbox, in code, where every picture is the same sand: a sand animator never brings in new sand for the next picture, they push the same sand into a new shape.
The sand is grains: 200,000 dark ones poured first and 40,000 terracotta ones poured later for the voice, and after that no grain is added or taken away. Draw each picture once on a canvas as blocks of sand, lines cut into them and lines of sand on the bare table, and sample it as grain positions. Match the grains to each new picture with sliced optimal transport, 22 directions, then match the result to exact spots along a Hilbert curve. Each grain travels the transport path, a little late or early and on a gentle curve, and hops to its exact spot at the end, landing on a downbeat. Add every grain into one RG16F height texture as a soft point, red for all the sand and green for the terracotta, and light it from below: test each grain against the thickness so thin sand breaks into single grains and thick sand stops the light, with a low lamp on the slopes that finds the terracotta. Work every frame out from the time alone. One table holds every picture and flow and drives both the film and the score, at 96 bpm. A "AI CONTENT SYSTEMS · DEMO BRIEF" label stays on screen. The score is composed in code in D minor: Karplus-Strong plucked strings, a hand drum, noise for every flow and a soft pad that breathes in under it.
Light on: black, a click, the table lights up amber, and a stream of dark grains builds one pile.
One brief: the pile flows into a card with "BRIEF" and four lines cut into it, under "ONE BRIEF." in sand.
In your voice: terracotta grains pour onto the card, and the next flow pulls them through it. "IN YOUR VOICE."
Anti-patterns out: "IN TODAY'S FAST-PACED WORLD..." forms in sand, a line of sand strikes it through, and it flows back into the card. "ANTI-PATTERNS OUT."
Every format: a post, an email, a caption reading "SPRING MENU, BAKED THIS MORNING." and a carousel of five, each a different shape and each landing on a downbeat. "ONE BRIEF. EVERY FORMAT." "NOT COPY-PASTED."
Four languages: one line cut into a band of sand, "SAME VOICE.", "MESMA VOZ.", "MÊME VOIX.", "MISMA VOZ.", the same four notes a register higher each time.
The review: three drafts, "DRAFTS FOR YOUR REVIEW." The only hand in the film, a black silhouette, ticks two and strikes the third, pushing grains aside into ridges, and the struck draft flows back out rewritten.
A month: a calendar fills row by row out of one shrinking pile. "A MONTH AT A TIME."
Yours: the sand gathers into a document beside "THE VOICE. THE PROMPTS. THE CODE. YOURS." The light clicks off.
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Content Systems", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The brand, the brief and the drafts are demos. Say drafts for your review, never that nothing can publish without a person. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} sand animation on a lightbox in HyperFrames for {product}, in code. Pour {how_many} grains into one pile, then {tinted_grains} in {tint_colour} for {what_the_tint_means}, and after that never add or take one away: every picture is the same grains flowing into a new shape. Draw each picture as blocks of sand, lines cut into them and lines of sand, and sample it as grain positions. Match the grains to it with sliced optimal transport and then exactly along a Hilbert curve, and land each flow on a downbeat. Flow from {your_first_picture} into {your_shapes}, then {your_turn}. Light it from below so thin sand breaks into grains and thick sand stops the light. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where every flow is sand you can hear.
```

Ideas:

- A translation agency: one paragraph flows through ten languages, and the same grains carry it across.
- A recipe site: one pile of flour becomes a loaf, a cake and a pizza, without adding any.
- A design system: one set of grains reshaped into a button, a card and a page, all one material.
- A newsletter: one story flows into a headline, a post and an email, with the key point in tinted grains through each.

## How it's built

1. **The pour.** A click, a flicker, then amber. A thin stream of dark grains lands in one spot and rolls out into a cone, the later grains further out.
2. **Same sand, new shape.** The pile flows into a card with the brief cut into it. Each grain is a little late or early and travels on a gentle curve, so the sand moves as a cloud and never as a dissolve.
3. **The voice.** 40,000 terracotta grains pour onto the card, and the next flow pulls them through it. From here on the voice can be followed through every shape.
4. **The stock phrase.** IN TODAY'S FAST-PACED WORLD... forms in sand, a line of sand strikes it through, and it flows back into the card.
5. **Every format.** A post, an email, a caption and a carousel, each landing on a downbeat. The landing is exact because every grain has its own spot in the picture.
6. **Four languages.** One line cut into a band of sand, in four languages. Only the letters move, and the band and the voice stay where they are.
7. **The review.** The fingertip ticks two drafts and strikes the third. Its marks push grains aside into ridges, and the struck draft flows back out rewritten.
8. **A month, then yours.** A calendar fills row by row out of one shrinking pile, and the sand gathers into a document beside THE VOICE. THE PROMPTS. THE CODE. YOURS.

## Gotchas worth knowing

- Moving a height field along a pressure flow looks like the obvious way, and it isn't: with a capped speed the sand pinches into blobs, and without one it turns into a dissolve. Grains are what make it read as sand.
- Sliced optimal transport gets the grains into the right shape but not onto the fine detail, so cut lines and words come out soft. Match the result to exact sample points along a Hilbert curve and hop there at the end.
- Hop to the exact spot too early and the Hilbert curve's blocks show through as a maze. Travel the transport path first, and keep the last hop short and late.
- Every picture needs about the same area of sand, or the thickness jumps between scenes. Words alone don't hold enough sand, so cut them into blocks or set them beside one.
- The grain barely compresses. A constant-quality encode came out at 55 MB for 36 seconds, so encode the web copy at a fixed bitrate in two passes.
