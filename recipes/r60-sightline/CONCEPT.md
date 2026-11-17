# R60 · Sightline · concept

**Style:** a shadow sculpture with one moving lamp. A lattice of small blocks stands on a plinth, and a lamp on a curved rail travels round it. The lamp's shadow on a long curved wall is noise almost the whole way, and at three exact angles it snaps into a crisp word. The lattice rebuilds itself twice, so three sweeps read three sentences.

**Made for:** the AI Consulting & Roadmapping service (ai.joaoqueiros.com/services/consulting). The film sells the service, so it ends with the service link.

**The idea:** a business looks like a tangle from most angles. The consulting work is finding the few angles where it reads clearly. The lamp is the point of view, the rail is the engagement, and each exact angle is a finding.

**Beats** (40.8 s, 100 bpm):
1. **A tangle:** a dark room, a pale lattice on a plinth, a lamp on a curved rail. The lamp slides and the shadow on the wall churns. "FROM MOST ANGLES, A TANGLE."
2. **The question:** over the lamp's shoulder, the shadow lands on WHERE, then DOES, then AI FIT?, each word snapping sharp as the lamp reaches its angle. "WHERE DOES AI FIT IN YOUR BUSINESS?"
3. **The work:** the blocks slide in a wave and AI FIT? becomes AUDIT ("WHERE THE HOURS ACTUALLY GO."). The lamp sweeps back: RANK ("SCORED BY PAYOFF, RISK AND COST."), then PLAN ("A PHASED PLAN YOU CAN EXECUTE.").
4. **The roadmap:** a second rebuild turns PLAN into FIRST. On the third sweep FIRST, SECOND and THIRD land, and each one stays on the wall in teal over a line with a tick every 7.5°. "WHAT TO BUILD FIRST, SECOND AND THIRD." "A PHASED PLAN · 3 TO 12 MONTHS".
5. **The honest stop:** the lamp goes on to an angle where nothing reads and stops. The shadow stays noise. "SOMETIMES THE ANSWER IS: DON'T BUILD IT."
6. **Direction:** the three marks on the wall light together. "NO CODE. JUST DIRECTION."
7. **Close:** the logo placed flat, "AI Consulting & Roadmapping", the URL and "A SERVICE · THIS FILM IS CODE".

**Technique:**
- **The carving** (`bake/carve.py`):
  - **Grid and font:** a 104 by 104 by 22 grid in NumPy, the words drawn in Archivo 800, every word at the same letter proportions.
  - **Angles:** the lamp is level and the words sit at 0°, 45° and 90°, so every shadow shares the height axis. That's what makes the carving solvable.
  - **Thinning:** the solid is where all three masks, pushed along the lamp's line, say yes. It's thinned one block at a time, in a seeded order, for as long as every shadow stays exactly the same.
  - **Results:** WHERE / DOES / AI FIT? keeps 1,598 blocks with one stray edge pixel on WHERE. AUDIT / RANK / PLAN (1,586) and FIRST / SECOND / THIRD (1,649) are pixel-exact.
  - **Matching:** each lattice's blocks are matched to the next one's, in the same row where they can be, so a rebuild slides every block to its next place. 1,661 blocks in all.
- **The lamp:**
  - **Motion:** one parallel beam whose angle follows the time. It leaves each angle quickly and comes into the next slowly, so each word gathers over about half a second.
  - **Shutter:** it's taken at four instants across a shutter of one and a half frames, each with its own 2048 px shadow map, so the shadow smears while the lamp moves and is sharp when it stops.
- **The rebuilds:** they run as a wave across the lamp's line, so the word on the wall changes from one end to the other.
- **The room:** one curved plaster wall, drawn only from the inside, a brass rail with a teal mark at each station, and a plinth whose shadow is a bar under every word. The last three words are kept as a texture on the wall.
- **Engine:** WebGL2 instanced blocks with 4x antialiasing, every frame worked out from the time alone. One table (`bake/table.py`) drives both the film and the score.
- **Score** (`score/compose.py`):
  - **The rail:** a rumble that follows the lamp's speed.
  - **The shadow:** a hiss that narrows onto a note as each word gathers, then a struck note and a wooden snap as it lands, so each sweep plays three notes.
  - **The rest:** knocks for the rebuilds, a tick for each mark the lamp crosses on the roadmap, two low notes that don't agree at the stop, and one full chord at the close.

**Honesty rules:**
- **Facts come only from the service page:** a workflow audit of where time goes, an opportunity map scored by time savings, cost, risk and strategic value, a ranked priority list, a phased plan of 3 to 12 months of what to build first, second and third, no code, just direction, and an honest answer when AI isn't a good fit.
- **Demo content:** the roadmap is a demo, and the words on the wall are the page's own words.
- **On-screen label:** "AI CONSULTING & ROADMAPPING · DEMO ROADMAP".
- **Nothing named or claimed:** no model or tool names, no results and no prices.
