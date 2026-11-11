# R59 · Counter

**Style:** one unbroken zoom: every scene lives inside a counter (the hole in a letter, a knob, a full stop) of the scene before, and the camera spirals down through six of them without a cut, from one prompt into the library inside it.
Every frame is worked out from the time alone. No footage and no cuts.
**Made for:** Prompt Engineering, a service: it builds a voice specification, an anti-pattern library, domain knowledge, a prompt library of 5 to 20 prompts and multi-step chains, as documented, editable files the team owns. Not a magic prompt.
**Length:** 42 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 42-second 1920x1080 film in HyperFrames for Prompt Engineering, a service that builds a prompt library a team owns: a voice specification, an anti-pattern library that catches clichés at prompt level, domain knowledge, a prompt library of 5 to 20 prompts for posts, reports, emails, briefs and summaries, and multi-step chains that draft, critique and rewrite, all documented and editable, and not a magic prompt. Make it one unbroken zoom: every scene lives inside a counter (the hole in a letter, a knob, a full stop) of the scene before, and the camera spirals down through it six times without a cut.
Draw it in Canvas 2D, every frame worked out from the time alone. Place each scene inside its parent's counter, shrunk so its whole frame fits inside the hole and turned by 0°, 90°, -90°, 0°, 180° or -90°. That placement leaves one point where it is: spiral the camera about that point, scaling by the placement's inverse as it turns, so landing in the counter is exactly the next scene at full frame. Find each letter's counter by drawing the glyph big and looking outward from its middle until the ink starts. Start each scene a beat and a half before it lands so the dive shows it turning in, average 12 samples across half a frame's shutter while diving, and punch in a little on each landing. One table holds the beat grid, the dives, the turns and every event, and drives both the film and the score, at 120 bpm. A "PROMPT ENGINEERING · DEMO LIBRARY" label stays on screen. The score is composed in code: a groove in D minor, a riser into each dive, an impact on each landing and a pop as each counter opens.
The prompt: on ink, "WRITE IT IN OUR VOICE." is typed key by key, each letter dropping in, and "OUR VOICE" is underlined. The O of VOICE opens.
A voice spec: on bone, three dials, TONE, RHYTHM and VOCABULARY, turn to PLAIN, SHORT and OURS, and a sample sentence answers them, scrambling from "We leverage seamless synergies." to "We fix it. Then we tell you." The VOCABULARY knob opens.
An anti-pattern library: eight demo clichés fly in and are struck out in red, one every half beat, each tagged CAUGHT. "CAUGHT AT PROMPT LEVEL", and its red full stop opens.
Domain knowledge: on teal, a network grows round one node, with THE VOCABULARY, HOW THE FIELD THINKS and WHAT EXPERT READS LIKE. The centre node opens.
A prompt library: twenty cards are dealt (posts, reports, emails, briefs, summaries) while a count runs from 05 to 20, then flip to "v3 · TESTED". The hole in the 0 of 20 opens.
Multi-step chains: DRAFT, CRITIQUE with red strikes marked CLICHÉ, JARGON and FILLER, then REWRITE: "We fix it. Then we tell you", whose teal full stop opens.
Close: "NOT A MAGIC PROMPT." "A LIBRARY YOU OWN." "DOCUMENTED · EDITABLE · YOURS". Then the logo placed flat, never redrawn or recoloured, with "Prompt Engineering", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The clichés, the sentences and the network labels are demo content. Name no tools or models, and claim no prices and no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made as one unbroken zoom: every scene lives inside a counter of the scene before (the hole in a letter, a dot, a knob), placed shrunk and turned so its whole frame fits the hole, and the camera spirals down about the one point that placement leaves where it is, landing exactly on the next scene at full frame, with no cuts. Open on {your_first_line} with a letter whose hole leads in, then dive through {your_scenes}, one idea each, each with its own motion system, and end with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code that rises into every dive and lands on every arrival.
```

Ideas:

- A product tour: the app icon's hole opens onto the home screen, a button opens onto a feature, a dot opens onto the next.
- A conference title: the O in the event's name opens onto each speaker, and the last dot opens onto the date.
- A brand story: the logo's counter opens onto where it started, and every scene's full stop opens onto the next year.
- A recipe: the O of the dish's name opens onto each step, ending in the hole of a plate.

## How it's built

1. **The prompt.** WRITE IT IN OUR VOICE. is typed key by key, and the O of VOICE opens.
2. **A voice spec.** Three dials turn to PLAIN, SHORT and OURS, and a sample sentence scrambles into plain words. The last knob opens.
3. **Clichés caught.** Eight demo clichés fly in and are struck out in red, one every half beat, and a red full stop opens.
4. **A network.** Domain knowledge grows round one node, and the node opens.
5. **Twenty cards.** Twenty prompts are dealt while the count runs to 20, then flip to tested, and the 0 of 20 opens.
6. **A chain.** Draft, critique, rewrite, and the rewrite's teal full stop opens onto the close.

## Gotchas worth knowing

- A zoom about the counter's centre drifts as it turns. Zoom about the one point the placement leaves where it is, and the landing is exact.
- A child scene that starts when it lands shows an empty colour all the way down. Start each scene a beat and a half early so the dive shows it turning in.
- Shrinking the child to the hole's width lets its corners poke out once it turns. Fit its half diagonal to the hole's smaller radius instead.
- Font metrics don't say where a letter's hole is. Draw the glyph and look outward from its middle until the ink starts.
- A full stop right after a letter gets clipped by the letter when its hole opens. Give the dot more room than type would.
- The portrait cut can't be a crop: re-lay every scene for the tall frame and move each counter with it, because the doors are where the scenes put them.
