# R35 · Pop-Up · concept (as built)

**Style (season 4, film 4 of 4): paper cut-out stop motion, as a pop-up book.** It uses the same engine as R32 Pinned,
R33 Planner and R34 Footlights: torn-edge cut paper with stocks generated from noise, poses on twos with edge boil,
one Canvas 2D, `paint(t)` drawing every frame from one baked table.

Pinned and Planner were paper lying flat, seen from above. Footlights stood paper up, seen from the front. Pop-Up
closes the season with the one thing paper does that neither did: **it folds open into 3D.**
- **A pop-up book on a table, seen at three-quarters.** Each spread opens from 0 to 180 degrees, and the pieces glued
  across the gutter rise as the pages open: V-folds, box folds, layered stages and a pull tab. A piece's height is the
  sine of the page's angle, so everything stands up as the book opens and lies flat again as it turns.
- **Page turns.** A page is drawn as a sheet hinged at the spine, its width the cosine of its angle, with a curl
  shaded along its free edge. It's a new kind of move for the season.
  *As built:* an orthographic 3D view, where every plane (a page at any angle, a card on its hinge, a flap) is one
  affine `setTransform`, so torn edges, stocks and print turn with the page. Pop-ups follow the page angles (they rise
  as their leaf lands and fold as the next one lifts), the ? flap is hinged on its side like a door, and pages shade
  as they lift rather than curl.
- **Daylight.** A morning scene, after Footlights' night: soft window light from the left, long pale shadows, warm
  highlights on the folds.
- **A new palette:** linen grey-green table, cream and ivory pages, terracotta, teal, ochre and ink. There's no felt,
  plum or theatre red.

**Made for:** the AI Brief Generator (ai.joaoqueiros.com/systems/ai-brief-generator), João's internal tool that turns a
client intake form into a structured creative brief. The case study's own line is "Intake form in, full brief out."
No code for it exists on disk or on GitHub, so, as with R33, the brief on screen is an **illustrative sample**, labelled
on screen as a sample, never presented as the system's own output.

**The idea:** a brief is a book that builds itself. A thin form goes in at the spine, and every section of the brief
pops up off the page, until a person goes through it with a pencil and the book closes on a finished document.

1. **Intake form in (0 to 4 s).** On the linen table, a paper intake form with numbered questions slides in. Two of
   its answers are the vague kind the case study names, "professional but friendly" and "everyone who needs it",
   in handwriting. A small card of call notes slides in after it, tagged **optional**. Both feed into the spine of a
   closed book titled **Creative brief · sample**. "Intake form in,"
2. **The synthesis (4 to 9 s).** The cover swings open. On the first spread a paper sieve, a pull-tab slot, takes the
   vague answers: "professional but friendly" is drawn through the slot and comes out the other side as three
   concrete chips, for example "plain words", "short sentences", "a warm sign-off". A fixed template of seven section
   tabs fans out along the fore-edge. "Vague words in, concrete out."
3. **Audience (9 to 13 s).** The page turns. A box fold rises with three paper personas standing in a row, each
   with a name card and one line (invented). "Who it's for,"
4. **Tone and competition (13 to 18 s).** Turn. On the left page, a pull tab slides a pointer along a paper scale
   between two tone words. On the right, a V-fold skyline of three blocks rises, labelled Competitor A, B and C (never
   real names), with a thread marking the open gap between them. "how it should sound,"
5. **Visual direction and scope (18 to 23 s).** Turn. A fan of colour swatches and type specimens springs up from the
   gutter, and beside it a pop-up checklist of deliverables stands up line by line. "and what to make."
6. **Risks and questions (23 to 26 s).** The last section is a flap marked **?**. It lifts, and two paper tags stand
   up beneath it: questions flagged for a human to follow up. "Questions flagged."
7. **Human edit (26 to 29 s).** The book lies open while a red pencil goes through it: it strikes one word, writes a
   better one above it, and ticks the tabs. A small paper stamp lands: **reviewed**. "Then a person edits it."
8. **Export and title (29 to 33 s).** The book closes, flips over, and folds flat into a single PDF sheet that slides
   into an envelope. The table clears and the JQ AI SYSTEMS logo lands flat, never redrawn or recoloured, with "AI
   Brief Generator", "Intake form in, full brief out." and ai.joaoqueiros.com/systems/ai-brief-generator.

**The sample:** an invented client, a small neighbourhood fitness studio (one of the case study's own sample
industries), with invented answers, personas, tone words and deliverables. The client's name is invented and
generic; no real business.

**Score:** composed in code, about 88 bpm and morning-bright. It has a celesta and a music box for the pop-ups,
pizzicato strings, an upright piano, a soft kick and a shaker. Each paper move has its own sound on the beat:
- the form sliding and the card tapping down;
- the cover's creak and a page's whoosh on every turn;
- a rising pluck for each piece that pops up;
- the pull tab's slide and click;
- the chips dropping out of the slot;
- the flap lifting;
- the pencil's scratch and the stamp;
- the fold, the envelope, and a major chord with a bell on the logo.

**Honesty and brand:**
- **Facts used on screen**, all from the case study:
  - an intake form of 10 to 15 questions, plus optional call notes;
  - a fixed section template: project context, audience (with personas), tone and voice, competitive landscape,
    visual direction, scope and deliverables, risks and questions;
  - vague answers like "professional but friendly" turned into concrete attributes;
  - a human reviews and edits the draft;
  - export as a PDF and a shareable document.
- **Kept off screen:** "3h → 30m", "24h", "80%", "in minutes", "12+ years" and "replaces a discovery session". No
  times, counts or results.
- **Third-party names:** no Claude, Anthropic or model name on screen, no logos. Competitors are A, B and C.
- The brief is a sample and says so on its cover.
- The JQ AI SYSTEMS logo is the official file, placed flat.
- **Licence:** the system isn't public, so the recipe licenses only the film's code; the sample brief is invented.

**Cuts:** 16:9, plus a 9:16 vertical re-laid out for portrait, not cropped. In portrait the book turns to a top-bound
flip book on an easel: the pages turn upward, each section pops up off the lower page, and the type wraps to the
frame. About 33 s. *As built:* 33.4 s; the portrait book lies flat on the table, bound at the top, its leaves turning
upward over the spine, each pop-up on its own page (near page below the spine, far page above), the tabs out of the
right edge, the intake sliding down from above (`videos/popup-vertical`).

**Stack:** HyperFrames 0.8.184 · Canvas 2D · GSAP · Python (table, score). The film forks the R34 engine (`piece()`,
the stocks, the boil, `camAt`) and adds page turns and pop-up folds driven by each page's angle.
