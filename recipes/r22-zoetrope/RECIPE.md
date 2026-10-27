# R22 · Zoetrope

**Style:** the oldest machines made to make pictures move, built in 3D and lit by a strobe. Each one is a spinning
blur until the strobe locks to its turn, and then the pictures on it come alive.
**Made for:** the Motion page of Imagined Worlds (visions.joaoqueiros.com/motion), João Queirós' cinematic loops.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom) · GSAP · Python (frames, table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for the Motion page of my site, where my Midjourney video loops live:
the oldest machines made to make pictures move, playing my loops under a strobe. Three.js with bloom, a dark cabinet
at night, black velvet, oiled walnut and brass, one warm lamp and one cold strobe, ember #ff6d3b as the only accent,
Fraunces and IBM Plex Mono.
Spin: a lacquered zoetrope drum on a walnut pedestal spins under the lamp, its painted numerals smeared into streaks.
Lock: a strobe stutters on, a few frames at first, then more, the pictures drifting, until it fires on every frame and
locks to the spin: the drum stands still and my thermal horse gallops around the inside.
The dive: the camera drops into the drum and through the far picture, and a flash cuts to the loop itself, full frame.
The cabinet: a flash back out to a walnut table of machines with brass plaques: a praxinoscope with a ballerina
dancing in its mirrors, a phenakistiscope disc with a ring of kingfishers flapping, a flip book riffling through a
child running in dusty ruins. Then all four in one wide shot.
Out of phase: the strobe drifts off the beat and the pictures slide, then it stops, everything smears and winds down
under the lamp, and one flash locks it all again.
End on a last flash into my burning carousel loop, under "Motion", "Worlds that refused to hold still." and the URL.
Station titles wipe on bottom left; a HUD names the light.
Technique: the film's own frame clock is the strobe. A machine that turns exactly one slot per film frame reads as
still while its pictures move. Off the lock, a frame is several renders averaged into real motion blur. One table
baked in Python holds the clock, the frames the strobe fires on and the spin, and every machine turns by its integral.
Each loop is cut to 60 frames on one atlas, the stretch whose end best matches its start, cross-faded into a loop.
Score: compose it in code from the same table: a whirr at the rate the slots pass, a xenon tick on every flash that
becomes a projector clatter when locked, a 150 bpm pulse with one beat per turn (Dm, Bb, F, C), four hooves a stride,
a music box for the mirror drum, wing beats for the disc, a paper riffle for the flip book, a tape stop as the machines
slow, and D major on the title.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: a cabinet of strobe-lit motion machines,
Three.js with bloom, {materials}, one warm lamp and one cold strobe, {accent} accents. A {first_machine} spins as a
blur, the strobe stutters on and locks, and {first_loop} comes alive inside it; the camera dives into it and cuts to
the clip, full frame. Then {machines}, each playing {loops}. The strobe drifts out of phase, everything smears, and
one flash locks it again. End on {title}, {line} and {url}. The film's frame clock is the strobe; one baked table drives
the spin, the flashes and a score composed in code.
```

Ideas: a band's tour clips on a cabinet of zoetropes, one per song; a sports club's best moments on spinning discs; a
product's features playing in a praxinoscope's mirrors; a family's home videos in a flip book.

## How it's built

1. **One table.** `bake/table.py` holds the film's clock, the film frames the strobe fires on, and the spin in slots per
   film frame, which is exactly 1 while locked. It integrates the spin into a phase and snaps it to a whole number of
   slots at each lock, so the drum stands with its slots where they were. The film reads `assets/table.js` and the score
   reads `bake/table.json`.
2. **The strobe is the frame clock.** A machine with twelve slots that turns one slot per film frame looks the same in
   every frame, so it reads as still, while the slot in each place shows the next picture. Locked, each slot's picture is
   chosen from the place it stands in and the playhead; off the lock, each slot keeps its own picture and the drum turns
   for real.
3. **Real motion blur.** On a frame the strobe does not fire on, the scene is rendered eight times across half a frame
   into a half-float target and averaged with additive blending; a flash frame is one render, frozen. Bloom runs on the
   average.
4. **The frames.** `bake/frames.py` cuts 60 frames from each loop onto a 10 × 6 atlas, choosing the stretch whose last
   frame best matches its first and skipping glitchy stretches, then cross-fades the last 8 frames into the frames
   before the start. One node material per slot picks its cell from a uniform.
5. **The machines.** The zoetrope is open cylinder pieces with slits between them and curved pictures inside, seen from
   the back; the praxinoscope adds twelve mirror facets that show the picture facing them; the disc rotates a ring of
   pictures about its axis; the flip book rotates three pages about the spine.
6. **The clips.** The dive and the title cut to the loops themselves as HyperFrames video clips, each on a white flash.

## Gotchas worth knowing

- AI video loops rarely have a clean repeating cycle. Pick the stretch whose end best matches its start and cross-fade
  the seam, or the animation hitches every time it wraps.
- Averaged renders need an additive blend of one and one: the default additive blend multiplies by alpha and darkens
  the average.
- A white picture under a strobe and bloom becomes a light. Darken it in its material so it reads as paper.
- A portrait cut needs the camera pulled back for the cabinet but not at the end of the dive: mask the pull by time,
  and stop the mask once the dive is over.
