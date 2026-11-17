# R62 · Pinpoint

**Style:** kinetic motion graphics around one coral dot that is never cut away from: found in a field of prospects, the needle of a gauge, the top bar of a list, the marker on a record, the cursor of a message, then the nose of a paper plane that freezes short of SEND.
Every frame is worked out from the beat alone, and drawn eight times across half a frame's shutter for real motion blur. No footage, no images.
**Made for:** AI Lead Generation & Outreach, a service: it finds prospects that match your ideal customer, enriches each one with public evidence, scores each for fit from 0 to 100 so warm leads come first, and drafts a personalised first message for a person to review. Nothing sends automatically.
**Length:** 38.7 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · Canvas 2D · GSAP · Python (table and score) · NumPy · SciPy · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 39-second 1920x1080 film in HyperFrames for AI Lead Generation & Outreach, a service that finds prospects that match your ideal customer, enriches each one with public evidence, scores each for fit from 0 to 100 so warm leads come first, not a random pile, and drafts a personalised first message for a person to review. Nothing sends automatically: you keep the send button. Make it kinetic motion graphics, the showreel kind, built around one coral dot that is never cut away from: every scene hands it to the next.
Draw it all on one Canvas 2D stage, every frame a pure function of the beat. Draw each frame eight times across half a frame's shutter and average them, so fast moves streak like real motion blur; step typed text once a frame so it never ghosts. Flip the background hard between scenes, ink, bone, teal, coral, and make the big words land letter by letter on the beat, each with a small camera shake and a ghost that springs off the word. One table in Python holds every cue, down to the beat each letter lands and each key is typed, and drives both the film and the score, at 124 bpm. An "AI LEAD GENERATION & OUTREACH · DEMO PIPELINE" label stays on screen. The score is composed in code: a groove in A minor, a hit for every letter, a click for every gauge tick and every key, whooshes for every move.
Open: a reticle waits, the dot drops into it, bounces, gathers itself and bursts into 2,304 prospects that streak out to a jittered grid.
Find: "FIND" slams in. A lens sweeps the field and magnifies as it goes; the good fits light teal and a counter climbs. It locks on the coral dot, "PROSPECT 0412 · FIT 87", and the camera dives into it. "PROSPECTS THAT MATCH YOUR IDEAL CUSTOMER".
Score: inside the dot is a bone page. A gauge draws itself tick by tick, the dot becomes its needle and swings to 87. The ticks fall, the needle unrolls into a bar, seven more bars rise and sort themselves, warm ones first. "EVERY PROSPECT SCORED FOR FIT, 0 TO 100" "WARM LEADS FIRST, NOT A RANDOM PILE".
Enrich: a teal wipe opens out of the dot, the top bar becomes a record card, and each detail slams in from the edges and is ticked. "EACH RECORD ENRICHED WITH PUBLIC EVIDENCE".
Draft: the card flips; its back is a message that writes itself with the dot as the cursor, the words taken from the record underlined in coral, then stamped "DRAFT · FOR REVIEW". "A PERSONALISED FIRST MESSAGE" "READY FOR A PERSON TO REVIEW". It folds into a paper plane, the wings lifting into a V and the keel folding down, lit in 3D, and flies off.
Your call: the plane flies at a giant SEND button and freezes short of it, and the music stops dead. "NOTHING SENDS AUTOMATICALLY." types itself into the silence. The dot leaves the plane and rests beside the button, never pressing it. "YOU KEEP THE SEND BUTTON." "WAITING FOR YOUR REVIEW".
Close: everything folds into the dot, it pops, and the logo placed flat, never redrawn or recoloured, on dark with "AI Lead Generation & Outreach", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The pipeline, the prospect and the message are a demo. Name no sources, tools or models, and claim no prices and no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made as kinetic motion graphics around one {colour} dot that is never cut away from: every scene hands it to the next, {your_scenes}, each with a hard colour flip and a big word that lands letter by letter on the beat. Draw every frame eight times across half a frame's shutter and average them for real motion blur, carry the dot through {your_moment_of_choice} and stop everything there, music too, then end with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where every letter, tick and key lands on its frame.
```

Ideas:

- A checkout flow: one dot is the product, the basket, the card and the parcel, and it stops at the door.
- A hiring pipeline: one dot is the candidate, from the pile to the shortlist to the offer, which a person signs.
- A support ticket: one dot is the question, sorted, answered in draft, and waiting for a person to send.
- An app onboarding: one dot is the user's first tap, carried through every screen.

## How it's built

1. **Found.** The dot drops into a reticle, bounces and bursts into a field of prospects.
2. **Find.** A lens sweeps the field, the fits light up, and it locks on the coral dot; the camera dives in.
3. **Score.** The dot becomes a gauge's needle and swings to 87; the needle becomes a bar and the bars sort, warm ones first.
4. **Enrich.** The top bar becomes a record card and every detail slams in and is ticked.
5. **Draft.** The card flips into a message the dot types, then folds into a paper plane.
6. **Your call.** The plane freezes short of SEND, the music stops, and the dot rests beside the button.
7. **The mark.** The logo, the service and the link, flat on dark.

## Gotchas worth knowing

- Motion blur from sub-frames also blurs typing: each sub-frame shows a different number of letters and the line ghosts. Step typed text once a frame, from the middle of the frame, and keep the blur for motion.
- A flat dart doesn't read as a paper plane. Fold it in 3D, wings up in a V and a keel down, turn it to a three-quarter view and give each face its own shade, darkest on the keel.
- To dive into a dot, scale the whole field about it exponentially and centre it first; a dot nine pixels across needs about 170 times to cover the frame.
- Keep the dot on screen at every cut: each scene starts where the last one left it, so the eye never has to look for it.
- Mark the big words by their order in the table, not by their pixel size, or the portrait cut, with smaller words, sounds and shakes differently from the landscape one.
- The freeze only lands if the sound stops on the same frame. Cut the mix there and add only one quiet note after it.
