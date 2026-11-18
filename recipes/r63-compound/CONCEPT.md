# R63 · Compound · concept

**Build decisions:**
- **The winding:** 300 nails, bone 1,103 passes, then coral 320, amber 160 and teal 200. Each pass carries a fifth of the light the first test used, so the picture needs many fine passes, and a pass pays a penalty for every bit of empty board it crosses (0.03 for bone, 0.07 for colour), which keeps colour on the flower instead of washing the ring.
- **Thread as light:** passes are drawn at the thread's true width and add up; where a pass is thinner than a pixel and a half it fades by the same amount, so hundreds of passes build like real thread. The first three passes are drawn thick enough to follow, and the thread thins as the passes rush.
- **The first days** are seen from a three-quarter view of the whole ring, so each pass reads from nail to nail; a tip-following camera lost the ring.
- **Pins** have round heads in coral, amber, teal and bone.

**Style:** string art in code, the classic ring loom. A ring of nails on a dark board and one thread. Every pass is a straight line from nail to nail, and no single pass means anything, but each one is chosen so that together they draw a picture. It starts as a scribble and, pass by pass, a flower comes out of nothing but straight lines. Then more threads in the brand colours wind over it, and the flower blooms in colour.

**Made for:** the Pinterest Growth Automation service (ai.joaoqueiros.com/services/pinterest-growth), its second film after R47 Flywheel. The film sells the service, so it ends with the service link.

**The idea:** a pin a day doesn't look like much. The service's whole point is that it compounds: the batch is designed once, a pin goes out every day without anyone touching a scheduler, and old pins keep surfacing for months. String art is that, literally. One pass is a meaningless line; hundreds of them, none taken back, become a picture. The nails around the ring are the batch; the thread is the daily pipeline visiting them; the picture is what builds up.

**Beats** (about 40 s):
1. **The batch:** nails hammer into a dark board in a ring, on the beat, each head catching a little brand colour. "A BATCH OF ON-BRAND PINS." "DESIGNED ONCE."
2. **Approved:** one light runs round the ring and every nail ticks. "YOU APPROVE THE BATCH, NOT EACH POST."
3. **Day one:** the thread ties on. Seen from a three-quarter view of the whole ring, it lays one pass, a pluck. "DAY 1". Then a second, a third. "ONE PIN, EVERY DAY." "NOBODY TOUCHING A SCHEDULER."
4. **It compounds:** the passes speed up, from one a beat to hundreds a second, the plucks merge into a shimmer, and the camera pulls back. Nothing is taken away, so a flower comes out of the lines. "PINS KEEP SURFACING FOR MONTHS." "IT COMPOUNDS."
5. **In your brand:** three more threads (coral, amber, teal) wind over the first, each its own greedy winding of one colour, and the flower blooms in colour. "IN YOUR BRAND, ON YOUR ACCOUNTS."
6. **Yours:** the thread ties off, the light settles on the finished piece. "YOU OWN THE SYSTEM." "AND THE AUDIENCE."
7. **Close:** the logo placed flat, "Pinterest Growth Automation", the URL and "A SERVICE · THIS FILM IS CODE".

**Technique:**
- **The winding** (`bake/wind.py`, NumPy): the target is a flower drawn in code (petals, a seed disc, shading), split into one darkness map per thread colour. From the nail it's on, each thread takes the pass that covers the most still-needed darkness, then subtracts what it laid. Nails close to each other are skipped so no pass is a stub. The whole sequence is baked once, so any frame knows exactly which passes are laid.
- **Engine:** WebGL2: instanced nails with heads and shadows, every pass an instanced thin ribbon, drawn additively with low opacity so crossings build up like real thread. Every frame is worked out from the time alone. The pass count over time is an easing curve baked in the table, so the slow start and the rush are exact.
- **One table** (`bake/table.py`) drives the film and the score.
- **Score** (`score/compose.py`): a hammer tap for each nail, then a plucked string for every pass, its pitch set by the pass's length like a real string, kept in one key. As the passes speed up, the plucks merge into a rising shimmer; the colour threads each add a voice; the tie-off is one last pluck, held.

**Honesty rules:**
- **Facts come only from the service page:** a batch of on-brand pins designed once; you approve the batch, not each daily post; a pin is published every day without anyone touching a scheduler; pins keep surfacing for months and reach compounds over weeks and months; everything runs on your accounts, so you own the system and the audience.
- **Demo content:** the flower is drawn in code for the film, not a client's pin or brand. On-screen label: "PINTEREST GROWTH AUTOMATION · DEMO BOARD". "DAY 1" is a demo count, and no day count past the first few is shown.
- **Nothing named or claimed:** no tool, platform-partner or model names (the page names several; the film names none, and "Pinterest" appears only in the service's name), no reach figures or any other results, no prices and no running-cost claim, no guarantees. Never mention the case study or the page's live example. No sparrow or any other image that could be read as a client's.
