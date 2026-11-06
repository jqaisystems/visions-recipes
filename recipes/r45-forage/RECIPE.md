# R45 · Forage

**Style:** ink feedback (season 6, film 3). 409,600 agents steer by the trail they deposit in one WebGL2 feedback buffer, the
way slime mould forages, running forward from one anchor so any frame can be rebuilt. Crisp type on a 2D layer above.
**Made for:** the AI Client Acquisition System, two internal tools that find and score businesses and write an email for a person to approve or reject.
**Length:** 34.44 s · 1920×1080 · 30 fps, with a 9:16 cut grown in its own tall dish.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 34.44-second 1920x1080 film in HyperFrames for the AI Client Acquisition System, two internal tools that find businesses,
score them from 0 to 100 with a written reason and draft an email for a person to approve. Make it dynamic motion design, a showreel
piece. The funnel is an organism making up its mind: 409,600 agents in WebGL2 steer by the trail they deposit in one feedback buffer, the
way slime mould forages, over a 1280x720 dish. The simulation runs forward from one anchor at time 0 and replays on a back-seek. One mask
canvas feeds it: red is food, green repels, blue is words. 108 bpm, 62 beats. Near-black #07080A, bioluminescent yellow #F5D117, bone #F4F0DC,
hard inversions to ink on yellow on the big hits, Archivo at 900, JetBrains Mono for labels, a score composed in code. All businesses, scores and
emails are fictional and labelled DEMO DATA.
One spore: a point on the first kick and veins feeling their way out. "500 COLD RESULTS."
The search: the reach grows until a living lace covers 500 dots, each flaring as it's found.
Words: SEARCH and SCORE grow inside their letterforms, with the lace visible inside each letter.
Scores: every dot takes a rolling score.
The contraction: one held breath, then weak food stops feeding and the network starves into 30 glowing arteries. "500", "BELOW 40: FILTERED OUT", "30", "QUALIFIED, OUT OF 500".
One business: fly along an artery to TIDAL BAKERY, 87 / 100, "NO WEBSITE. SOCIAL PAGE ONLY.", labelled fictional.
The flip: ink on yellow, "SOMETHING SPECIFIC ABOUT THEM."
The draft: a card labelled "DRAFT · NOT SENT · DEMO TEXT". APPROVE keeps a vein alive; REJECT cuts another, and it dies. "YOU DECIDE WHAT GOES OUT."
Never twice: contacted dots turn repellent and the network bends around them. "NO PROSPECT EMAILED TWICE."
Close: everything draws back to one point, and the logo lands flat, never redrawn or recoloured, with the system's name, the URL and "INTERNAL SYSTEM · DEMO DATA".
Take facts only from the case study. Claim no replies, clients or revenue, and don't imply it's for sale or that emails send themselves.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose story is {the_story}, grown by hundreds of thousands of
agents that steer by the trail they deposit in one WebGL2 feedback buffer, like slime mould. Feed them through one mask canvas: food for
{what_attracts}, repellent for {what_is_avoided}, and letterforms for {your_words}, clipping the light so they read at once. Let the network
cover everything, then starve it on one held breath so only {what_survives} is left. Run it forward from one anchor so any frame can be rebuilt.
End with everything drawing back to one point and {your_mark}, placed flat, with {line} and {url}, in {one_colour} on near-black, at {bpm} bpm with a
score composed in code.
```

Ideas:

- A logistics company: the network finds real routes between depots, then drops the wasteful ones.
- A city transport plan: stations as food, with the mould drawing a metro map on its own.
- A mycology or science festival: the real organism's behaviour, with the title grown inside its letters.
- A newsletter that cuts the noise: a thousand sources as food, and only the ones worth reading stay fed.

## How it's built

1. **One spore.** A point on the first kick, with a few veins feeling their way out and a sentence below it.
2. **A living lace.** The reach grows on a curve and agents wake as the front arrives, so density stays at the front and doesn't bunch at the centre.
3. **Words that grow.** Agents are fed along the letters and the display clips light to the letterform, so the lace lives inside each letter and the word reads at once.
4. **Every dot takes a score.** Numbers roll at each business, then settle to fictional scores. Only those above the line keep their food.
5. **The contraction.** On the drop the agents get long senses and fast legs, and only the fed routes pay. Hundreds of veins starve in under two seconds.
6. **Along an artery.** The camera flies one surviving route to one fictional business, its 87 and its written reason.
7. **A cut you can see.** A person rejects a lead. Repellent lands on its vein, the food goes, and the severed end dies.
8. **Going around.** Contacted businesses turn repellent, so the network visibly bends around them. It's the simplest picture of no duplicates.

## Gotchas worth knowing

- Spawn every agent at the centre and the lace bunches there. Spread them out and wake them as the front arrives.
- A word grown from veins alone won't read. Clip the display by the letterform so light only lives inside it.
- Type on a living network needs a halo, or the veins will cross it on every frame.
- A simulation has history and a renderer seeks. Replay from one anchor or a re-render won't match.
- Agent films can become a lovely texture that says nothing. Decide what feeds them, because that's the script.
