# R44 · Main Street · concept

**Style:** a living miniature town of exactly 500 fictional businesses in WebGL2, shot as a tilt-shift model. Instanced houses with roofs, windows and trees, real shadows from one sun that travels through a day, a night, a morning and an evening, a screen-space tilt-shift lens and motion blur over 8 sub-frames. It's warm and full of colour, the opposite of the two dark drafts.

**Made for:** the AI Client Acquisition System (ai.joaoqueiros.com/systems/ai-prospecting).

**The idea:** the funnel happens to a place. Each business is a building you can point at, the search is a van driving through town as shops appear, and filtering means the buildings sink into the ground. The big words are built from thousands of tiny blocks standing on the same streets, under the same sun.

**Sound:** marimba, pizzicato bass, hand claps and glockenspiel at 120 bpm in C. Each of the 500 businesses plays one marimba note at the moment it's found, chosen from a pentatonic scale by its distance from the plaza, so the search is the tune. Picture and sound read one file, `bake/table.py`.

**Beats** (64 at 120 bpm, 32 s):
1. **One van.** Macro on an empty town. "500 COLD RESULTS." sits over the road, and the first five shops open on the first five notes.
2. **The search.** Shops spring up from the plaza outwards as the camera lifts to the whole town.
3. **Words made of town.** SEARCH and SCORE rise from the ground in blocks, with their sub-lines.
4. **Scores.** A low flight along the streets with a score tag on every roof.
5. **The drop.** One held breath, then a shockwave through the ground, debris, and night falling in an instant. "BELOW 40: FILTERED OUT". Thirty buildings stay and throw beacons into the sky. "30". "QUALIFIED, OUT OF 500".
6. **One business.** Sunrise over TIDAL BAKERY with a queue outside. 87, "NO WEBSITE. SOCIAL PAGE ONLY.", labelled fictional.
7. **The flip.** The town turns coral and ink: "SOMETHING / SPECIFIC / ABOUT THEM."
8. **The draft.** A sheet of paper labelled DRAFT · NOT SENT · DEMO TEXT beside the street. APPROVE on the bakery, REJECT on a neighbour, which sinks. "YOU DECIDE WHAT GOES OUT."
9. **Never twice.** New shops open across town, and six CONTACTED buildings sit dark inside their rings. "NO PROSPECT EMAILED TWICE."
10. **Close.** The sun sets, the town sinks from the edges inwards, and the logo lands flat.

**Honesty rules:** facts only from the case study; below 40 filtered out, 40 to 59 cold, 60 to 79 warm, 80 to 100 strong; 500 to 30 shown as what the funnel does; no replies, clients or revenue claimed; all businesses, scores and emails fictional and labelled demo data; generic labels only; internal system, not implied for sale; a person decides and emails never send themselves.

**Generated, not committed:** `assets/table.js`, `assets/bgm/score.wav`. Run `bake/table.py`, then `score/compose.py`.
