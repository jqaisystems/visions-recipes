# R61 · Stacked · concept

**Style:** a shadow sculpture built on camera. A heap of small blocks lies on the floor of a dark room under three lamps, and the walls show only noise. Then the blocks rise and lock into a lattice one row at a time, and because the lamps are level, all three shadows write their words at once, from the bottom up. The lattice rebuilds itself twice, so the walls read three sentences.

**Made for:** the AI Stack Setup & Enablement service (ai.joaoqueiros.com/services/ai-stack-setup). The film sells the service, so it ends with the service link.

**The idea:** the service page's picture of the problem is AI use "scattered across personal accounts and pasted prompts". The heap is that: everything is there, and nothing reads. Setting up the stack is the same blocks put in order, so from every angle the team works from, something clear lands.

**Beats** (39.2 s, 104 bpm):
1. **Scattered:** three lamps click on over a heap of blocks on the floor. The walls show only low, lumpy noise. "SCATTERED ACROSS PERSONAL ACCOUNTS" "AND PASTED PROMPTS."
2. **Installed:** the heap stirs, and the blocks rise and lock into the lattice row by row. On three walls at once, CODE, VIDEO and IMAGE write themselves from the bottom up. The camera looks down each lamp's line in turn, and the blocks line up into each word. "THE RIGHT TOOLS FOR THE WORK."
3. **Configured:** the blocks slide in a wave and the lattice rebuilds: SKILLS, PROMPTS and PLAYBOOK. "SET UP FOR THE WAY YOUR TEAM WORKS."
4. **Onboarding:** three flat heads and shoulders step into the beams, one beside each word. "HANDS-ON. REAL TASKS." "NOT A SLIDESHOW."
5. **Handover:** the figures step out, and a last rebuild leaves YOUR, OWN and STACK. "YOUR ACCOUNTS. YOUR KEYS." "YOURS TO KEEP."
6. **Close:** the logo placed flat, "AI Stack Setup & Enablement", the URL and "A SERVICE · THIS FILM IS CODE".

**Technique:**
- **The carving** (`bake/carve.py`):
  - **Grid and font:** a 104 by 104 by 22 grid in NumPy, the words drawn in Archivo 800, every word at the same letter proportions.
  - **Angles:** the lamps are level, at 0°, 45° and 90°, so every shadow shares the height axis. That makes the carving solvable, and it means each row of the lattice casts the same row of all three words.
  - **Thinning:** each lattice is where all three masks, pushed along the lamps' lines, say yes. It's thinned one block at a time, in a seeded order, for as long as every shadow stays exactly the same.
  - **Results:** all three sets are pixel-exact: CODE / VIDEO / IMAGE keeps 1,505 blocks, SKILLS / PROMPTS / PLAYBOOK 1,472 and YOUR / OWN / STACK 1,396. Narrowing every word a little (`MAXW = 74`) is what made the third set exact.
  - **Matching:** each lattice's blocks are matched to the next one's, in the same row where they can be, so a rebuild slides every block to its next place.
- **The heap and the build:**
  - **The heap:** every block of the first lattice lies in a loose mound on the floor at its own odd angle.
  - **The build:** the lattice is built in 22 rows, a dotted sixteenth apart, taking the top of the heap first and pairing each block with a heap place round the same bearing. Each row's blocks leave raggedly, fly a high arc and lock together.
- **The team:** three flat heads and shoulders. The beams are narrowed, and each figure stands where only its own lamp reaches, so each casts one shadow.
- **The camera:** the wide shots stand high, so the lattice drops below the words and never hides the middle one.
- **Engine:** WebGL2 instanced blocks that can lie at any angle, one 2048 px shadow map per lamp, 4x antialiasing, and every frame worked out from the time alone. One table (`bake/table.py`) drives both the film and the score.
- **Score** (`score/compose.py`):
  - **The lamps:** a heavy switch and a low hum each, swelling as the words complete.
  - **The heap:** a rattle, like a box of blocks shaken once.
  - **The build:** a tuned wooden knock as each row locks, a step higher each time up a D major scale, so the build plays as a rising scale.
  - **The rest:** knocks for the rebuilds landing on struck chords, a soft pluck for each of the team, and one full chord at the close.

**Honesty rules:**
- **Facts come only from the service page:** AI use scattered across personal accounts and pasted prompts; the right tools chosen and installed for the work; each configured with custom skills, prompt libraries and a usage playbook; a hands-on onboarding with real tasks, not a slideshow; everything under the team's own accounts and keys, theirs to keep.
- **Demo content:** the stack is a demo, and the words on the walls are the page's own words.
- **On-screen label:** "AI STACK SETUP & ENABLEMENT · DEMO STACK".
- **Nothing named or claimed:** no model or tool names, no results and no prices.
