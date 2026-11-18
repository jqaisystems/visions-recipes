# R64 · Gist · concept

**Build decisions:**
- **The winding:** BRIEF in 634 passes over 313 of the 5,184 nails. The pass held for the reviewer is the longest of the last sixty, moved to the end with hidden jumps behind the board, so the wait reads from the foot of the F to its top.
- **Scattered:** each nail lands up to 230 units off its place, leaning up to 0.55 rad; twelve unused nails carry source-type tags. A ripple from the centre lifts each one, carries it home and taps it in.
- **Themes:** six patches from jittered seeds with ragged borders; the heads take coral, amber, teal, sage, sky or violet as the light passes. Earlier days' boards shift the colours, so no two are the same.
- **The board** runs out of every shot until the wall, then becomes one tile of fifteen (five weekdays, three weeks); the shadow map widens with the camera.
- **End card:** "AI News Curator", ai.joaoqueiros.com/systems/ai-news-curator and "RESEARCH BRIEFING WORKFLOW · THIS FILM IS CODE".

**Style:** string art in code, the second kind: a dark board full of nails, and one thread that only takes passes that stay inside a letter, so a word builds up out of crossing straight lines, like a hand-made string-art sign. It's a full board, not R63's ring, words instead of a picture, and one bone thread instead of colour.

**Made for:** AI News Curator (ai.joaoqueiros.com/systems/ai-news-curator), its second film after 024 Signal from Noise. The end card links to the case study.

**The idea:** the system's problem isn't collection, it's conversion. Every nail is a saved signal, the board is full of them, and nearly all of them stay bare. The thread joins only the ones that matter, and a word comes out of the board because the thread skips everything else. Then a person decides, and the day goes into an archive that you can see.

**Beats** (about 40 s, 96 bpm):
1. **Scattered:** nails rain into the dark board at random angles and heights, each on a beat, a few with tiny source-type tags (newsletter, release, docs update, saved link, community note). "USEFUL SIGNALS ARRIVE FROM EVERYWHERE." "AND SIT IN TABS UNTIL THEY'RE FORGOTTEN."
2. **Normalize:** in one wave, every nail straightens and slides onto an exact grid, the same height and the same head: one shape for every record. "EVERY LINK BECOMES A RECORD."
3. **Classify:** a light sweeps the board and each head takes a theme colour, so the board reads as patches of topic. "GROUPED BY TOPIC AND DATE."
4. **Brief:** a bone thread ties onto one nail and winds the word BRIEF, pass after pass inside the letters, slowly then quickly. The camera starts low at the nail heads and pulls back as the word comes out. The rest of the board stays bare. "THE LATEST USEFUL ITEMS," "IN ONE SHORT DAILY BRIEF."
5. **Review:** the thread stops one pass short, its end hanging at the last nail. A reviewer's lamp passes over it, and only then is the last pass laid. "A PERSON DECIDES WHAT EACH ONE BECOMES." "NOTHING IS PUBLISHED AUTOMATICALLY."
6. **Archive:** the thread ties off and the camera pulls far back. Today's board is the newest in a wall of fifteen boards, three weeks of weekdays under MON to FRI, today's marked TODAY. "KEPT BY DAY, MONTH AND TOPIC." "RESEARCH STARTS FROM MEMORY, NOT OLD TABS."
7. **Close:** the logo placed flat, "AI News Curator", the URL and "RESEARCH BRIEFING WORKFLOW · THIS FILM IS CODE".

**Technique:**
- **The winding:** `bake/wind.py`: a jittered nail grid, passes allowed only inside a slightly grown letter, greedy cover of bare letter, with the word BRIEF. Earlier days' boards reuse today's winding, baked once, with their theme colours shifted.
- **Normalize:** each nail gets a seeded scattered pose (offset, tilt, height) that eases to its grid pose in a ripple, so the scatter and the grid are the same nails.
- **Engine:** WebGL2: instanced nails with a shadow map, thread as instanced lit ribbons. The archive wall draws the earlier boards as instances of the same geometry at a distance.
- **Score:** a tap for every nail landing, a rising tone for the light, a pluck for every pass pitched by its length, one held note while the last pass waits, then its pluck when the reviewer lays it.

**Honesty rules:**
- **Facts come only from the case study:** signals arrive from newsletters, releases, social posts, saved links, docs updates and community notes; they sit in tabs and get forgotten; each item becomes a consistent record; items are grouped by topic and date; the latest useful items become a short daily brief; a person decides whether each becomes public content, private research, client context or an archived note; nothing is published automatically; the archive is kept by day, month, year, source and topic.
- **Demo content:** no real links, headlines or sources. The tags are source types only, and the theme colours carry no labels. On-screen label: "AI NEWS CURATOR · DEMO BOARD".
- **Nothing named or claimed:** no tool, model or API names (the page lists some, and the film names none). The case study's outcomes are qualitative, and the film claims none of them.
