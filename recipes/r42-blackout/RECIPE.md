# R42 · Blackout

**Style:** ink feedback (season 6, film 2). Wet ink and water in one WebGL2 feedback buffer over a paper fibre texture,
restarted from clean paper at fixed anchors so any frame can be rebuilt. Crisp type on a 2D layer above.
**Made for:** Codex Control Center, a local-first dashboard that keeps the metadata and not the words.
**Length:** 33.6 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.6-second 1920x1080 film in HyperFrames for Codex Control Center, a local-first dashboard that keeps
the metadata of a session and not its words, as blackout poetry. Make it dynamic motion design, a showreel piece. One WebGL2
feedback buffer holds ink and water over a paper fibre texture: water carries ink along the fibres, so edges feather like ink
on newsprint. The page restarts from clean paper at fixed anchors and replays forward, so any frame is rebuilt the same way.
Crisp type sits on a 2D layer above. 100 bpm, 56 beats. Newsprint bone #EDE8DC, printing ink #0C0C0E, and one vermilion
#E8341C kept for the stamps. Archivo condensed at 900, JetBrains Mono for the log, no gradients or glow, a score composed in
code. Every log line, path and token is fictional.
The log: a dense demo session log races up the page: prompts, full paths, raw output, a fake token.
Blackout: on the half beat, wet bars slam over each private line in six bursts. They bleed through the fibres and join until the
page is black, leaving only times, event types and tool names on islands of bare paper. "METADATA ONLY."
Observe: the survivors assemble a dashboard with activity, usage, readiness and workspace labels instead of paths, marked DEMO
DATA. "NO API KEY TO OBSERVE."
Approve: task cards queue. A vermilion APPROVE stamp slams onto one, moving with the card, and its splash ripples through the wet
page. The task runs in a read-only sandbox. A full-access card arrives and gets stamped BLOCKED. "NOTHING RUNS UNTIL YOU SAY SO."
The wash: water sweeps the page, private words cut out of the ink melt as it reaches them, and the black rinses back to bone.
"CHECKED BEFORE IT'S PUBLIC."
Close: one drop blooms to fill the frame, then the logo placed flat, never redrawn or recoloured, with "Codex Control Center", the
URL and "Open source · MIT". Use "Codex" only in the system's name. Take facts only from the case study, don't imply the check
guarantees safety, and claim no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose promise is {the_promise}, as
blackout poetry. One WebGL2 feedback buffer holds ink and water over a paper fibre texture, restarted from clean paper at fixed
anchors so any frame can be rebuilt. Fill the page with {the_dense_document}, using fictional text only. On the beat, wet bars slam
over {what_gets_removed} and bleed together until only {what_survives} is left on islands of bare paper. Turn the survivors into
{the_result}, stamp {the_decision} in {one_accent_colour} with a splash that ripples the wet page, wash the page back to {your_paper},
and end on {your_mark}, placed flat, with {line} and {url}. Crisp type above the ink, at {bpm} bpm, with a score composed in code: a
wet slap per bar and a long soak into a sub drop.
```

Ideas:

- A legal redaction tool: a contract floods until only the clauses you need are left on bare paper.
- A newsletter that cuts the noise: a day's headlines soak away until one line stays.
- A poet's own launch: real blackout poems made from their own drafts, in their own paper and ink.
- A data removal service: a profile page floods and rinses clean, with the stamp as the final act.

## How it's built

1. **A page full of secrets.** The log is dense and readable on purpose: prompts, paths, output, a fake token. All of it is invented in one table script, the same one the bars read from.
2. **Wet bars.** Each burst adds ink and water along a row. The water spreads first and the ink follows along the fibres, so the bars creep sideways and join.
3. **The soak.** Bars become a flooded page in one long move, with a descending sound into a sub drop. It's the film's big change, and nothing cuts.
4. **What survives.** Times, event types and tool names stay on islands of bare paper, the way a real blackout poem leaves its words.
5. **Survivors become the UI.** Those same labels slide into the dashboard, so the data and the interface are visibly one thing.
6. **The stamp.** The APPROVE stamp lands on the card and moves with it. Its splash lands on the wet page below, and the ripple bends everything, type included.
7. **The refusal.** BLOCKED lands with a dull thud on a full-access card, and that task never runs.
8. **The wash.** Water sweeps the buffer so the ink actually lifts. The private words are cut out of the ink, so they melt as it arrives.

## Gotchas worth knowing

- Without a fibre texture, a bleed is just a soft edge. The direction has to come from the paper.
- Feedback has history and a renderer seeks. Without anchors, a frame depends on how you got there, and a re-render won't match.
- Leave words as islands of paper with black type. Bone letters cut out of the ink read as a graphic, not as what the ink left behind.
- Keep one accent colour for the stamps alone, or they stop being the event.
- A wash that clears on a straight line is a wipe. It has to move the ink in the buffer.
