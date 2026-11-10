# R57 · Impression · concept

**Style:** the pin screen as a measuring tool. It turns the frame side on, at a steep three-quarter angle, behind a clear acrylic face, so you see the whole length of every steel shaft and not just the heads. It uses the one thing the real toy does best: **the pins remember.** Push something in and they hold its exact shape after it's gone. Push a second shape into that impression and only the pins that don't fit move. Tilt the frame and every pin slides back flat in one wave, under gravity.

**Made for:** the AI Problem-to-Solution Assessment service (ai.joaoqueiros.com/services/ai-tools-assessment). This film sells the service, so it ends with the service link.

**The idea:** take the shape of the problem before you pick the solution. The workflow is pressed in and the pins keep its true shape, snags and all. Each option is then pressed into that same impression, and the pins show exactly where it doesn't fit. Checked, not guessed.

**Why it's a wow:** three moments.
- A shape withdraws and its perfect negative is left standing in thousands of steel shafts.
- The misfit map: an option pressed into the impression, and only the pins it shoves move, lighting amber, so the mismatch is drawn by the metal itself.
- The tilt reset: the whole frame tips and every pin slides back flat in a rolling wave, with a cascade of ticks.

**Beats** (40 s, 96 bpm):
1. **One problem.** A flat field of pins behind acrylic, a cool rim light down the shafts. A lumpy, awkward shape pushes in from behind: one workflow, with its snags. It withdraws and the pins keep it. "ONE PROBLEM." "TAKEN AS IT IS."
2. **The map.** The camera moves along the impression, and it reads as the process as it runs now: raised steps, ridges at each handoff, a deep pit where work waits, a loop where it's redone. Small flat labels: STEPS · HANDOFFS · DELAYS · REWORK. "MAPPED BEFORE ANYTHING IS BOUGHT."
3. **Up to three paths (the showpiece).** Three shapes press into the same impression from the front, one after another: an off-the-shelf tool, a connected workflow, a simpler process change. With each one, the pins that don't fit are shoved and glow amber, and a panel ticks off PRICE, SETUP, INTEGRATIONS, PRIVACY, MAINTENANCE and REVERSIBILITY. "UP TO THREE PATHS." "CHECKED, NOT GUESSED."
4. **One recommendation.** One shape sits flush. No pin moves, the amber dies away and the sound goes quiet for a beat. Which kind of path it is stays unsaid. "ONE RECOMMENDATION."
5. **The test.** Thirty pins along the edge rise one by one, one per day, then a head and shoulders for the owner and a target for the measure. "A 30-DAY TEST." "AN OWNER. ONE MEASURE OF SUCCESS."
6. **Reset, and the brief.** The frame tilts and every pin slides back flat in one wave. The decision brief then presses up in relief. "WITHIN FIVE BUSINESS DAYS." "NO CODE WRITTEN. NOTHING CONNECTED." The logo is placed flat, with "AI Problem-to-Solution Assessment", the URL and "A SERVICE · THIS FILM IS CODE".

**Sound:** metal, dry and close, as if the frame is on a desk.
- **Pushing in:** a pin moving is a tick, and a shape pushing in is a dense slide of ticks.
- **Fit checks:** a misfit is a scraping cluster pitched by how many pins moved. A clean fit is one soft struck note.
- **The 30 days:** a little rising run of tuned taps.
- **The tilt reset:** the climax, one long cascade like a handful of ball bearings, then a single low chord under the brief.

**Look:**
- **Pins and frame:** brushed steel shafts with domed heads in a dark frame, seen through a clear acrylic face that catches a thin reflection.
- **Light:** one warm key and a cool rim along the shafts.
- **Colour:** amber only for pins that moved during a check. Everything else stays steel.
- **Camera:** a slow push along the impression, never flying over it.
- **Labels:** small flat labels in JetBrains Mono. The one honesty label stays on screen.

**Honesty rules:**
- **Facts come only from the service page:**
  - one business workflow and a 60-minute discovery interview;
  - a map of the current process (steps, tools, handoffs, delays, rework);
  - up to three paths (an off-the-shelf tool, a connected or custom workflow, a simpler process change), compared on price, setup, integrations, permissions, privacy, maintenance, limitations, reversibility and effort, against official sources;
  - one recommendation, a 30-day test plan, an owner and a success criterion;
  - the decision brief within five business days;
  - no accounts connected, no code written, no implementation;
  - "no change" is a valid outcome.
- **On-screen label:** "AI PROBLEM-TO-SOLUTION ASSESSMENT · DEMO WORKFLOW". The workflow and the options are shapes only.
- **No third-party names or logos:** the "tool" shape is a plain form, not a product.
- **No prices, no savings, no results:** the page itself says it won't promise savings before a baseline exists. The case study on the page is never referenced.

**How it's built:**
- **Pins:** 11,520 pins (144 by 80, 10 units apart), each a real steel shaft and domed head, drawn instanced in WebGL2. They're lit by one warm key with a 3072 px shadow map and a cool rim, with 4x MSAA. The acrylic is two clear faces with a fresnel reflection. The frame sits in a stand on a desk.
- **Memory:** the events in the table run in order on every pin, each with a weight that rises once and then stays. "back" pushes pins out to a shape. "front" presses a mould on, and nothing can stay further out than the mould allows. "tilt" and "flat" send every pin home. So any frame renders on its own and the pins still remember.
- **The moulds:** each one is a frosted layer of discs coming down over the heads. Amber is how far a pin was shoved, fading as the problem is pressed back in from behind. The check panel counts the pins each mould moved, live from the same numbers: 1,103 for path 1, 303 for path 2 and 0 for path 3.
- **Which path wins:** path 3 fits, but the film never says which kind of path it is. The three kinds are named once, together, as "A READY-MADE TOOL · A CONNECTED WORKFLOW · A SIMPLER PROCESS".
- **Words:** the captions are flat, along the top, and the map labels follow their pins on screen.
- **Score:** the pin counts the score uses for each mould are written in `score/compose.py`. Change them if the moulds change.
