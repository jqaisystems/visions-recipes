# R46 · Clatter · concept

**Style:** a physical wall of 30,000 split-flap tiles in WebGL2. Each tile is real instanced geometry: two static halves, a falling flap on a hinge and box sides. Multisampled, with motion blur across 4 sub-frames, depth of field, per-tile tilt and a travelling glint.

**Made for:** the AI Client Acquisition System (ai.joaoqueiros.com/systems/ai-prospecting).

**The idea:** the funnel is literal. Five boards of 100 rows make 500 rows, and each row is one fictional business with a name, trade, town, score and status. The tiles are the only type in the film, from one flap in macro to letters pushed out of the wall. The only flat layer is the frame's demo-data label and the logo at the close.

**Sound:** every flap in the schedule is one click at its real time, panned by its column, so a wave crossing the wall crosses the speakers. The harmony is that same clatter ringing through tuned resonators, with a sub, a kick and one held breath under it. Picture and sound read one file, `bake/table.py`.

**Beats** (64 at 112 bpm, 34.3 s):
1. **One tile.** Macro. One flap falls, then "500 COLD RESULTS." is written tile by tile.
2. **The search.** Rows arrive from the middle out as the camera pulls back from macro to all 500.
3. **Words made of the data.** SEARCH and SCORE, with sub-lines, pushed out of the wall, their tiles still carrying the rows.
4. **Scores spin.** A raking camera along the wall while every score rolls and settles, with a band beside it.
5. **The drop.** One held breath. Rows below 40 flip away in a shockwave. "BELOW 40: FILTERED OUT". The rest go, 30 rows stay. "30". "QUALIFIED, OUT OF 500".
6. **One business.** Macro along TIDAL BAKERY, the 87 and the reason, labelled fictional.
7. **The flip.** An orange shockwave from the score: "SOMETHING / SPECIFIC / ABOUT THEM."
8. **The draft.** The wall types an email labelled DRAFT · NOT SENT · DEMO TEXT. APPROVE lights up, another row is marked REJECTED and flips away. "YOU DECIDE WHAT GOES OUT."
9. **Never twice.** A fresh search crosses the wall and the six CONTACTED rows don't change. "NO PROSPECT EMAILED TWICE."
10. **Close.** The wall empties towards the first tile, the last flap falls, and the logo lands flat.

**Honesty rules:** facts only from the case study; below 40 filtered out, 40 to 59 cold, 60 to 79 warm, 80 to 100 strong; 500 to 30 shown as what the funnel does; no replies, clients or revenue claimed; all businesses, scores and emails fictional and labelled demo data; generic labels only; internal system, not implied for sale; a person decides and emails never send themselves.

**Generated, not committed:** `assets/events.js`, `bake/flips.npz`, `assets/bgm/score.wav`. Run `bake/table.py`, then `score/compose.py`.
