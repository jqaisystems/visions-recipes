# R51 · Hands Off · concept

**Style (season 8, sand on a lightbox, opens the season):** sand animation made entirely in code, the live art where a performer draws and wipes images in sand on a glowing table. Nothing in the library looks like it: no objects, no type on a backdrop, just shadow and amber light. One hand-written WebGL2 shader treats sand as a height field that light passes through, so thin sand glows and thick sand goes black, with single grains at the edges. Every image is drawn on screen by a stroke that really pushes the sand aside and leaves a ridge.

**Made for:** the AI Automation Systems service (ai.joaoqueiros.com/services/ai-automation). Every service and public system already has a film. This service's only one is R13 Chain Reaction, from the earlier Three.js run, so it's the best place for a second. This film sells a service, so it ends with the service link.

**The idea:** a sand artist has to draw everything by hand, and wipe it, and draw it again. That's the page's "repetitive, high-volume task". So a fingertip draws the same task over and over, then draws the map and the code, and then lifts off the table. The drawing keeps going without it.

**Why it's a wow:** the moment the finger leaves. For twenty seconds the audience has learned that sand only moves when the finger moves it. Then the finger lifts, the table is empty of hands, and the sand carries on drawing itself, faster than any hand could. The light then shifts from amber to night blue, and it's still going.

**Beats** (about 33 s):
1. **Light on.** Black. A click, and the table lights up amber. A stream of sand pours in from above and spreads.
2. **The same task.** A fingertip draws a form in the sand and a box beside it, wipes them with one sweep, and draws them again. Each pass lands on the beat and gets faster, and it's the same drawing every time. "THE SAME TASK." "AGAIN." "AND AGAIN."
3. **Plain English.** The finger slows and writes out the pattern as a line of words in the sand. "IF YOU CAN DESCRIBE IT..."
4. **The map.** One sweep clears the table. The finger draws the workflow as boxes and handoffs, with the handoff points pressed in deep. "MAPPED BEFORE ANY CODE."
5. **The code.** The map collapses into lines of a demo Python script written in sand, line by line. "CUSTOM PYTHON. NOT A TEMPLATE."
6. **Hands off (the showpiece).** The finger presses one last dot, and lifts away. Beat of nothing. Then the sand moves by itself: the same drawing from beat 2 draws and wipes itself on every beat, then twice a beat, until a whole wall of them is running across the table.
7. **Night.** The light cools from amber to blue, as a sun drawn in the sand sinks and a moon comes up. Nothing stops. "ON YOUR SCHEDULE."
8. **Yours.** The sand gathers into a stack of files, then a folder. "EVERY FILE. EVERY PROMPT. YOURS." The light clicks off. The logo is placed flat, with "AI Automation Systems", the URL and "A SERVICE · THIS FILM IS CODE".

**Sound:** composed in code, warm and close: plucked strings, a hand drum, and real-sounding sand made from filtered noise, so every stroke of the finger is audible and shaped to its speed. While the finger works, the music follows it. When it lifts, there's one bar of near silence, and then the rhythm comes back as machine-tight sand on every beat. It should sound nothing like the clay films.

**Look:** near-black sand on an amber lightbox, moving to a deep blue at night, and nothing else. The only other colour is the logo on the end card, which sits flat on dark as it must. Words are carved into the sand by the same stroke engine, not laid over it, so they keep the film's single material. A small flat label stays on screen for honesty.

**Honesty rules:**
- Facts come only from the service page: a repetitive task with a pattern you can describe in plain English; the process mapped before code is written; a purpose-built Python and AI pipeline, not a generic template; optional scheduled runs, with or without supervision; every file, prompt and config handed over, and you own the code, the prompts and the data.
- A label stays on screen: "AI AUTOMATION SYSTEMS · DEMO WORKFLOW". The script shown is fictional. The end card says "A SERVICE · THIS FILM IS CODE".
- No results: no hours saved, no costs, no prices, no delivery times, no client work and no claims about any client. "Hands off" is about the system running on a schedule, never a promise that nobody ever has to check it.
- No third-party names or logos: the model providers and tools on the page stay off screen. Python appears only as the language the page names.

**How the film differs from the first idea:** the sand is a height field on the GPU, run forwards frame by frame, and every mark comes from one stroke table, with or without a finger. The hand is lit dimly by a low lamp, because a pure silhouette vanished against dark sand. The wall is 8 by 4. It starts as a wave, tightens until it lands whole on a downbeat with one big hit, then a wave of redrawing runs through it during the night, so nothing stops. Morning clears the table and the folder and last words are laid down in dark sand on bright, the only inverted scene.

**The look:** the sand has visible relief and a dark ridge beside every stroke, the halo round the lines is small, the table shows through at the edges, and the hand is a true silhouette with the light wrapping its edge.

**Generated, not in the repo:** `assets/table.js`, `assets/bgm/score.wav`, renders.
