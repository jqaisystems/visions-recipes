# R53 · Channels

**Style:** sand animation on a lightbox, in code. A sheet of 300,000 grains has five islands raised in it, and every cut a fingertip makes pushes the grains aside into banks.
100,000 more grains are the work, each with its own route, times, lane and speed, running down the channels. Every frame is worked out from the time alone. No footage and no 3D engine.
**Made for:** AI Workflow Integration, a service: an AI decision layer added to the tools a team already uses, without replacing them, where the client keeps the code, the configuration, the documentation and the credentials.
**Length:** 36.25 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 36.25-second 1920x1080 film in HyperFrames for AI Workflow Integration, a service that adds an AI decision layer to the tools a team already uses, without replacing them. Make it a sand animation on a lightbox, in code, where the tools are islands in a sheet of sand and the work between them is grains that run down channels a fingertip has cut.
The table is 300,000 dark grains with five islands raised in it, each a plain shape and never a product: an envelope, a form, a grid, a card and a speech bubble, plus a small figure of a person. Every cut is a segment with a time it is drawn, a time it widens from a thin line into a channel and a time it is smoothed away, and a push shader moves the sheet's grains aside into ridges from the time alone. The work is 100,000 terracotta grains, each with a route, a time it lands in a pile, a time it leaves, a lane and a speed, placed every frame from those numbers. 36,000 more grains carry the captions, flowing between lines by sliced optimal transport. Light it from below, as Hands Off is lit. One table holds the islands, every cut, every stream and every caption, and drives both the film and the score, at 96 bpm. A "AI WORKFLOW INTEGRATION · DEMO WORKFLOW" label stays on screen. The score is composed in code in D minor: Karplus-Strong plucked strings, a hand drum, and a trickle of grain noise for every stream.
Your tools: a click, the table lights up amber, five islands, and terracotta grains piled beside them with nowhere to go, while an old crooked furrow carries a trickle by hand. "YOUR TOOLS." "WORK STUCK BETWEEN THEM."
The map: the fingertip draws every route as a thin line, a ring in the middle, and a tick at the bottom of the table. "THE MAP COMES FIRST." "YOU APPROVE IT."
Connected: the thin lines widen into channels from the sources outwards, the ring opens into a basin, and the piles start to move. "NOTHING REPLACED. JUST CONNECTED."
The decision layer: every stream runs into the basin and leaves split, to the grid, the card and the bubble, and a pulse takes a fork to the person. "ROUTED. SUMMARISED." "TO THE RIGHT PERSON."
When it fails: a ridge falls into the card's channel, the grains back up behind it, a mark opens beside it, and the music stops on one bell. The fingertip clears it and the grains run again. "EVERY RUN LOGGED." "FAILURES ALERT." "NOTHING DROPS SILENTLY."
Shadow run: the old furrow and the new channel run side by side and arrive together, then the fingertip sweeps the old one away. "SHADOW RUN FIRST." "THEN CUTOVER."
Yours: the streams keep running. "THE CODE. THE KEYS. THE DOCS. YOURS." The light clicks off.
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Workflow Integration", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The workflow, the requests and the reply are demos, and the tools are shapes with no names. Say nothing drops silently only about failures alerting. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} sand animation on a lightbox in HyperFrames for {product}, in code. Lay a sheet of {how_many} dark grains with {your_islands} raised in it as plain shapes, and pile {work_grains} grains in {work_colour} beside them for {what_the_work_is}. Have a fingertip draw {your_routes} as thin lines, then widen them into channels that push the sheet's grains aside into ridges, worked out from the time alone. Give every work grain a route, a time it leaves, a lane and a speed, and run the streams through {your_decision_point}, where they split. Show {your_turn}. Light it from below so thin sand breaks into grains and thick sand stops the light. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where every stream is a trickle you can hear.
```

Ideas:

- A delivery company: depots as islands, parcels as grains, and the sorting hub as the basin in the middle.
- A support desk: inboxes as islands, tickets as grains that split by topic and reach the right person.
- A data pipeline: sources at the top, one transform in the middle, and three stores filling at the bottom.
- An events team: one sign-up form whose grains fork to the venue, the caterer and a welcome email.

## How it's built

1. **Islands.** A click and the amber light. Five tools are shapes raised in the sand, and the work is terracotta piled beside them, with only an old crooked furrow carrying a trickle by hand.
2. **The map.** The fingertip draws every route as a thin line, a ring for the decision layer, and a tick at the bottom of the table for the approval.
3. **Cut and opened.** The thin lines widen into channels from the sources outwards, and the sheet's grains are pushed aside into banks. The piles start to move.
4. **The basin.** Every stream runs into the basin in the middle and leaves split. Arriving work spreads onto its tool as a terracotta speckle, so the tools fill up as the film goes on.
5. **The right person.** A pulse of grains takes a fork off the bubble's channel to the small figure of a person.
6. **The failure.** A ridge falls into the card's channel. The grains queue behind it instead of vanishing, a mark opens beside it, and the music stops on one bell until the fingertip clears it.
7. **Shadow run, then cutover.** The old furrow and the new channel carry the same work side by side and arrive together, then the fingertip sweeps the old furrow away.

## Gotchas worth knowing

- Streams of grains on a flat table read as dots on rails. The ridges are what make them read as sand: cut the channel into the sheet first, and let the work run between real banks.
- A fallen ridge drawn as a straight bar across the channel came out as a bow tie. Collapse most of the bank into an elliptical mound instead, and it reads as sand that slipped.
- Work that arrives as one blob looks pasted on. Spread each grain onto its tool with a weight that fades in, so the tools fill up as a speckle.
- A route that passes too close to an island's shape tangles with it. Plan the person's channel after the islands are placed, not before.
- The portrait cut can't be a crop: the routes run left to right. Lay the table out again so the work runs from the top down, with the same timings.
