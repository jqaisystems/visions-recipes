# R58 · Casting · concept

**Style:** one object, many shadows. A hanging lattice of small matte blocks looks like a meaningless tangle from every angle. But each lamp that switches on throws a clean, readable shadow onto its own plaster wall, and each shadow is different. The object is carved in code so that all its shadows are true at once: every block exists only because at least one shadow needs it, and removing any block would break a letter somewhere. The picture is made entirely by what's missing: light.

**Made for:** the AI Agent Architecture service (ai.joaoqueiros.com/services/agent-architecture). The film sells the service, so it ends with the service link.

**The idea:** one system and one shared memory, with each agent casting its own output. The lattice is the shared memory. Each lamp is an agent with one role. The same blocks read as RESEARCH from one side, DRAFT from another and REVIEW from a third. The agents differ only in where they stand and what they look at, and that's the architecture.

**Why it's a wow:** three moments.
- **The reveal:** the camera circles a shapeless tangle, a lamp clicks on, and a crisp word lands on the wall. Then a second lamp, a second word, and it's still the same tangle.
- **The proof:** the camera swings round into the line of each lamp, and the tangle visibly lines up into the letter it casts.
- **The regrow:** a fourth lamp is added, and blocks slide in and out until the same lattice casts four shadows. Adding an agent takes hours, not weeks.

**Beats** (40 s, 96 bpm):
1. **One system.** A dark round room with plaster walls. A lattice of pale blocks hangs on a wire, turning slowly. It means nothing. "ONE SYSTEM."
2. **One role each.** The lamps stand in a ring at the lattice's height, like agents around one table. Lamp 1 clicks on, and RESEARCH falls on the wall opposite. Lamp 2, a quarter turn round, puts DRAFT on its wall. Lamp 3, between them, puts REVIEW on a third. "EVERY AGENT HAS ONE ROLE."
3. **One shared memory.** The camera moves into each lamp's line in turn, and the tangle locks into each word. The blocks warm slightly where every shadow uses them. "ONE SHARED MEMORY."
4. **Handoffs.** The lamps fire in order, research, then draft, then review. A thin beam of light runs from one word to the next along the walls, so each agent's shadow seems to pass work to the next. The schedule ticks past in small labels: ON A SCHEDULE · ON A TRIGGER · ON REQUEST. Then the reviewer's lamp dims and holds, and a small human silhouette steps into the light: "A HUMAN SIGNS OFF."
5. **Add an agent.** A fourth lamp swings in. The lattice rebuilds itself, with blocks sliding out and new ones sliding in, until a fourth word lands on a fourth wall. "ADD ONE IN HOURS, NOT WEEKS."
6. **The honest turn.** Every lamp but one goes out. The tangle collapses into one plain block with one plain shadow. "IF ONE PROMPT IS ENOUGH, I'LL SAY SO."
7. **The end card.** The lamps come back. The logo is placed flat on the back wall, with "AI Agent Architecture", the URL, and "A SERVICE · THIS FILM IS CODE".

**Sound:** it's dry and wooden, like a small room.
- **Lamps:** each lamp is a heavy relay clack followed by a low filament hum, and each agent's lamp hums on its own note. The three notes make a chord as they light.
- **Blocks:** blocks sliding in and out make soft wooden knocks, like a box of dominoes shaken gently.
- **Handoffs:** each handoff is a plucked note travelling along the wall with the beam.
- **The honest turn:** when the lamps go out, the room drops to one hum, and the end card brings the full chord back.

**Look:**
- **The room:** warm plaster walls, a pale floor, and the lattice made of bone-white blocks with softly bevelled edges.
- **Shadows:** real shadows from real lamp positions, sharp near the object and soft further away. Each lamp is a slightly different warm white, so where shadows overlap you see faint coloured fringes.
- **Colour:** the JQ teal only on the handoff beam and the labels.
- **Labels:** small flat labels in JetBrains Mono. The honesty label stays on screen.
- **Camera:** a slow orbit that keeps coming back to each lamp's line, never a fly-through.

**Honesty rules:**
- **Facts come only from the service page:**
  - multi-agent systems where each agent has a role, its own memory scope and skills, with handoff rules;
  - typically 2 to 6 agents;
  - a shared memory layer;
  - scheduled, triggered and on-demand runs;
  - a human looped in;
  - a design document signed off before the build;
  - extending the system "should take hours, not weeks";
  - a simpler pipeline is recommended when multi-agent isn't needed;
  - the client owns everything.
- **On-screen label:** "AI AGENT ARCHITECTURE · DEMO SYSTEM". The three roles (research, draft, review) are the page's own examples.
- **No tool or model names:** the stack list on the page is never shown.
- **No results, no case study:** the case study's numbers are never referenced, and no prices or timescales are promised beyond the page's wording.

**Carving test (done before building):** I ran the carving in NumPy on a 64 by 64 by 16 grid, with the lamps level and set at 0°, 90° and 45° around the lattice.
- **Three lamps work perfectly.** RESEARCH, DRAFT and REVIEW all came out pixel-exact, from about 800 blocks after thinning. The diagonal word has to sit a little narrower (about 60% of its wall) for that.
- **The lamps have to be level.** My first layout used a lamp overhead throwing a word on the floor, and that failed badly. Level lamps share the height axis, and that's what makes the carving solvable.
- **Four lamps didn't quite work at that size.** RESEARCH, DRAFT, REVIEW and PUBLISH lost 2% to 8% of their pixels, so the build raised the grid, narrowed the words and added a repair pass (see below).

**Technique:**
- **The carving:** `bake/carve.py` (NumPy). Each word is rasterised to a mask. The solid is the intersection of the masks extruded along each level lamp's direction. It's then thinned: blocks are removed one at a time, in a seeded order, as long as every shadow stays exactly the same. What's left looks like a tangle and casts perfect shadows. The fourth-lamp state is carved the same way, and the rebuild morphs block by block between the two sets.
- **The table:** `bake/table.py` at 96 bpm holds the lamps, their on and off keys, the camera, the captions and the rebuild order. The score reads the same table.
- **Rendering:** WebGL2 instanced blocks with one shadow map per lamp, shared from Impression's renderer, a plaster shader for the walls, and 4x MSAA. Any frame renders from the time alone.
- **Lamps** are treated as distant, so the light is parallel. **Generated, not committed:** `assets/table.js`, `assets/blocks.js`, `assets/bgm/score.wav` and the renders.

**Build decisions:**
- **The carving** (`bake/carve.py`): a 104 by 104 by 22 grid, in Archivo 800. RESEARCH is cast at 0°, DRAFT at 45°, REVIEW at 90° and PUBLISH at 135°. The diagonal words sit narrower and the level ones slightly narrower too, so the ends of every word are inside the region all lamps reach.
- **Three lamps:** 1,731 blocks, and all three shadows are pixel-exact.
- **Four lamps:** 2,115 blocks, with 1,717 of them shared with the three-lamp lattice. A repair pass places one block for each pixel no block could cast, where it only thickens a letter's edge, so all four words are complete with 30 stray edge pixels out of about 5,200. The proof sheets are `work/carve-three.png` and `work/carve-four.png`.
- **Diagonal shadows:** a cube seen corner-on casts a shadow about 1.4 blocks wide, so the diagonal words are a touch bolder than the pixel masks.
- **Lamps:** they're never drawn. Each is a parallel beam with soft rectangular edges and its own 2048 px shadow map, held in one depth texture array, with 4x MSAA. The fourth lamp swings in from 160° to 135° as it lights.
- **The room:** four octagon walls, one square on to each lamp, with plaster noise, and a floor with a soft spill under each beam. The camera stays on the lamp side, so it never looks through a wall.
- **The human:** a flat head-and-shoulders cut-out made of thin slices. It stands where only REVIEW's lamp reaches it, so its shadow falls beside REVIEW.
- **The collapse:** every block slides into a 13-block cube, and RESEARCH's lamp throws one plain square.
- **Shared memory:** during the proof shots, blocks that more than one shadow needs glow warm.
- **Score:** a relay clack for each lamp switching, and a filament hum on D, A, F sharp and E. Blocks sliding are wooden knocks, the handoffs are plucked runs (Karplus-Strong), and the finale is a struck chord.
