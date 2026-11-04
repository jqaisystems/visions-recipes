# R40 · One Take

**Style:** one unbroken camera. Twelve worlds, each with its own colours and motion, drawn on one Canvas 2D stage in
shared coordinates, so the camera can dive through a shape in one to land in the next. Every frame is accumulated from
sub-frames for real motion blur.
**Made for:** Client Portal Automation, a portal that updates itself, in development.
**Length:** 33.75 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · Canvas 2D · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.75-second 1920x1080 film in HyperFrames for Client Portal Automation, an internal system I
am still building, whose problem is that project status lives in twelve places. Make it dynamic motion design, a
showreel piece. One Canvas 2D stage and one unbroken camera: draw every scene as a function of its own local time in
the same 1920x1080 coordinates, so a scene can be drawn inside a shape in another scene. Each frame is stateless and
accumulated from 16 sub-frames for real motion blur. 128 bpm, 72 beats. A flat, bold palette led by teal #00A89D and
blue #0099D6, on ink #111110 and bone #E9E4D6, with navy, aqua, gold and coral for the colour changes. Archivo at its
heaviest for full-frame kinetic type, JetBrains Mono for small labels, no gradients or glow, a score composed in code.
The dot: on black, one dot falls on the kick, squashes, bounces and bursts into twelve. "Project status lives in 12 places"
Twelve worlds, speeding up, three beats each down to one, each with its own palette and motion, and the camera dives
through a shape in one to land in the next, turning as it goes, with no cuts: email (the flap closes, dive through the
seal), chat, weekly video (through the play mark), shared page, drive folder (a tunnel of folders), files, feedback
(pins drop and squash), time log, invoice (the number rolls, a stamp slams), handover notes, commits, uploads.
The wall: one beat of silence, then a sub drop as the camera rockets back, and all twelve were tiles on one wall,
still playing. "All twelve. All at once." They fall in turn into one sheet, a line for each. "One record per project."
New project: the sheet becomes one button; press it, and five cards deal out with 3D flips: kickoff brief, asset request
list, first-week plan, risk list, tracking sheet. Label it "working locally". "One trigger. Five documents."
Friday: Mon, Tue, Wed, Thu riffle past and FRIDAY slams full frame. Three panels slide up, one per client: an email, a
shared page, a short video, with demo text. Label it "in development". "Every Friday, in their format."
Close: back to the dot, one bounce, and it clears the frame for the logo, placed flat, never redrawn or recoloured, with
"A portal that updates itself.", the URL and "In development". Say it is in development, and claim no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose problem is {the_problem},
as one unbroken camera through {number} worlds, one for each of {the_scattered_things}. One Canvas 2D stage, every world a
function of its own local time in shared coordinates, each frame stateless and accumulated from sub-frames for real
motion blur, at {bpm} bpm. Give each world its own palette from {your_palette} and its own motion, and end each one on a
shape the camera dives through, zooming on a log scale and turning, to land in the next. On the drop, pull back: all
the worlds were tiles on one wall, still playing. Fold the wall into {the_one_thing}, show {what_it_produces} as cards dealt
out with 3D flips, slam in {the_key_word} full frame, come back to the opening shape and end on {your_mark} with {line}
and {url}. A score composed in code, with a sound for each world, a whoosh for each dive and one beat of silence before the drop.
```

Ideas:

- A password manager: twelve sticky notes, inboxes and spreadsheets as worlds, then the wall folds into one vault.
- A restaurant booking system: phone, paper diary, chat and walk-ins as worlds, then one floor plan.
- A music label's release plan: artwork, masters, contracts and socials as worlds, then one release sheet.
- A school's parent updates: letters, group chats and notice boards as worlds, then one weekly note.

## How it's built

1. **One dot.** The dot falls on an ease-in, squashes as it hits, stretches as it leaves and bursts on the second landing, so the film's first move already has weight.
2. **A seal becomes a door.** The envelope's flap closes, the seal stamps, and the seal is the portal: chat is already drawn inside it, and the camera dives through and lands.
3. **A tunnel inside a dive.** The drive folder world is folders inside folders on a geometric scale, so the camera's zoom and the world's own motion stack.
4. **The number rolls.** Each digit of the invoice number is a reel with its own stop time, and the motion blur does the rest; the stamp lands on the beat and is the next door.
5. **The wall.** After one beat of silence, the camera rockets back from the world on screen. The same twelve functions run as tiles on a grid, each on a loop, so the reveal is alive.
6. **One record.** The tiles fall in turn into one sheet, and each one's arrival writes its line on the sheet.
7. **Five cards.** The button squashes when pressed and each card flies out while it flips, faked with a horizontal scale by the cosine of the angle and a little stretch at the turn.
8. **Friday.** The days flip in on half beats, then FRIDAY lands too big, with a shake that decays, and settles to full width.

## Gotchas worth knowing

- Zoom on a log scale: a linear scale spends nearly all its time at the start and then jumps, and the dive looks like a cut.
- Size the next world from the portal's inner radius, not its outer one, or the frame's corners show past the shape just before landing.
- Paint each world's background far past its frame, or the camera's turn shows the edge as it starts to dive.
- Six sub-frames show as stepped ghosts on a fast whip. Use more, and weight each by 1/(i+1) so the first isn't the strongest.
- Let every world take negative local time and hold its first state: during the dive, the next world is on screen before its own clock starts.
