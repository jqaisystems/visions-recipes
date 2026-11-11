# R59 · Counter · concept

**Style:** one unbroken zoom, all motion graphics. Every scene lives inside a counter, the typographic name for the hole in a letter, of the scene before: the hole in an O, a dial's knob, a full stop, a network's centre node, the hole in a 0. The camera spirals down through each one, six times without a cut, and lands on the next scene at full frame. Each scene is its own motion system: typed type, dials driving a sample, strikes, a growing network, dealt and flipped cards, and a chain.

**Made for:** the Prompt Engineering service (ai.joaoqueiros.com/services/prompt-engineering). The film sells the service, so it ends with the service link.

**The idea:** look inside one prompt and there's an engineered library: a voice spec, an anti-pattern library, domain knowledge, a prompt library and multi-step chains. Each one sits literally inside the last.

**Beats** (42 s, 120 bpm):
1. **The prompt:** "WRITE IT IN OUR VOICE." is typed, and the O of VOICE opens.
2. **A voice spec:**
   - Three dials, TONE, RHYTHM and VOCABULARY, turn to PLAIN, SHORT and OURS.
   - The sample output scrambles from "We leverage seamless synergies." to "We fix it. Then we tell you."
   - The VOCABULARY knob opens.
3. **An anti-pattern library:** eight demo clichés fly in and are struck out in red, one every half beat, each tagged CAUGHT. Then "CAUGHT AT PROMPT LEVEL", whose red full stop opens.
4. **Domain knowledge:** a network grows round one node, with THE VOCABULARY, HOW THE FIELD THINKS and WHAT EXPERT READS LIKE. The centre node opens.
5. **A prompt library:** twenty cards are dealt (posts, reports, emails, briefs, summaries) while a count runs from 05 to 20. The cards flip to "v3 · TESTED", and the hole in the 0 of 20 opens.
6. **Multi-step chains:** DRAFT, CRITIQUE (red strikes: CLICHÉ, JARGON, FILLER), REWRITE: "We fix it. Then we tell you", whose teal full stop opens.
7. **Close:** "NOT A MAGIC PROMPT." "A LIBRARY YOU OWN." "DOCUMENTED · EDITABLE · YOURS". Then the logo placed flat, "Prompt Engineering", the URL and "A SERVICE · THIS FILM IS CODE".

**Technique:**
- **The zoom:**
  - **Placement:** a scene is drawn inside its parent's counter, shrunk so its whole frame fits inside the hole and turned (0°, 90°, -90°, 0°, 180°, -90°).
  - **Camera:** a spiral zoom about the one point that placement leaves where it is, so landing in the counter is exactly the next scene at full frame. There are no cuts and no crossfades.
  - **Counters:** each counter is found by drawing the glyph and looking outward from its middle until the ink starts.
- **Motion blur:** 12 samples across half a frame's shutter while diving. Each landing punches in and settles.
- **Engine:** Canvas 2D, with every frame worked out from the time alone. One table (`bake/table.py`) drives both the film and the score.
- **Score** (`score/compose.py`):
  - **Groove:** 120 bpm in D minor, Dm, Bb, F, C.
  - **Dives:** a riser into each dive, an impact on each landing, and a pop as each counter opens.
  - **Scene parts:** keystrokes, dial ratchets, a clap and a zap per strike, plucked notes for the network, card flicks, and the chain's arrows.
  - **Close:** the drums drop out, and a chord brings in the mark.

**Honesty rules:**
- **Facts come only from the service page:** a voice specification, an anti-pattern library "caught at prompt level", domain knowledge, a prompt library of 5 to 20 prompts (posts, reports, emails, briefs, summaries), multi-step chains (draft, critique, rewrite), documented and editable files the team owns, and not a magic prompt.
- **Demo content:** the clichés, the sample sentences and the network labels are demo content.
- **On-screen label:** "PROMPT ENGINEERING · DEMO LIBRARY".
- **Nothing named or claimed:** no model or tool names, no results and no prices.
