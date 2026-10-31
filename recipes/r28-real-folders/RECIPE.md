# R28 · Real Folders

**Style:** 2D vector motion design. One SVG stage and GSAP, with no canvas, no WebGL and no 3D: a capture overlay whose
selection is a live mask, a loupe that is the scene itself scaled under a circle, an isometric city drawn flat from one
matrix, a camera tilt that is that matrix interpolated from flat, and redaction in solid pixels, in a flat dark palette.

**Made for:** Snapline, a screenshot and screen recording manager for Windows.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · SVG · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for Snapline, a screenshot and screen recording manager for
Windows whose line is "Real folders, not a database." 2D vector motion design only: one SVG stage and GSAP, no canvas,
no WebGL. Flat dark: ground #0a0c11, panel #11141b, text #e8ebf2, accent #6f72f1, lavender #c9c4ff, green #34d399 for
ticks only, and the violet-to-orchid gradient #6e63f2 to #9e57f6 for the hero moments only. Bricolage Grotesque, Inter
and JetBrains Mono. Every window, company and email address is fictional.
Capture: a desk of flat windows; the capture overlay drops in with a crosshair and a loupe that magnifies the desk
under a pixel grid; a marching-ants selection drags out with a px chip; the shutter fires and the selection lifts off
as a card.
File: captures land on the beat, faster and faster; the floor grid tilts from flat to isometric, a city of twelve
project folders rises, and every card flies into its folder, turning into the folder floor as it drops in.
Find: "invoice" types into a search field; a scan crosses the city, the words inside every card lift off, and only
the four matches rise out of their folders with "text in image · match" chips.
Mark up: dive into one invoice; an arrow and a box draw on, step badges pop in, and the email snaps into solid pixel
blocks, column by column.
Share: the gradient floods in behind the card, which settles with padding and a shadow; then it becomes a screen
recording with a REC frame, a timer and a strip of frames.
Title: the overlay selects the empty centre, the shutter fires on the official logo, flat, then the line and the URL.
Never redraw or recolour the mark. Score: compose it in code from the same table, 108 bpm, A minor to C major.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, in 2D vector motion design only (one SVG
stage and GSAP), flat {palette}. {the_capture} selects part of {the_scene} as a live mask and fires; {the_items} flood
in on the beat; the camera tilts into an isometric {the_places} drawn from one matrix and every item is filed; a search
for {the_query} lifts {the_hidden_detail} out of every item and only the matches rise; one is {the_edit}; and it lands,
{the_finish}. Then the flat logo with {line} and {url}. One baked table drives the items, the places, the matches and a
score composed in code.
```

Ideas: a photo library, with a camera roll flooding into albums and a search lifting the places out of every photo; a
notes app, with web clippings filed into notebooks; a receipts tracker, with a card number snapped into solid pixels; a
design handoff tool, with frames found by a component name.

## How it's built

1. **One SVG stage.** No canvas and no WebGL. The stage holds layers (the desk, the folder city, the cards, the big
   card, the capture overlay and the title). One GSAP tween drives the clock and calls `paint(t)`, a pure function of
   time, so any frame can be seeked in any order.
2. **The selection is a mask.** The scrim is a dark rectangle with a `<mask>`: white for the whole frame and a black
   rectangle for the selection, resized every frame. Marching ants are a dashed stroke with an animated dash offset over
   a solid dark one, with four handles and a px chip that reads the live size.
3. **A loupe over real pixels.** The desk is one group with an id. The loupe is a `<use>` of it, scaled four times
   about the cursor and clipped to a circle, with a 4 px pattern on top as the pixel grid.
4. **A city from one matrix.** `P(gx, gy, z)` projects a point isometrically. Each folder is two side faces, a top and a
   tab, drawn back to front, and its label sits on a face with `matrix(0.866, 0.5, 0, 1, x, y)`.
5. **Tilted and filed.** The camera's tilt is the floor grid's matrix interpolated from flat to isometric. Each card is
   filed the same way: its flat matrix (scale and rotation) is interpolated into the folder floor's, while its position
   follows an arc into the folder.
6. **Found and redacted.** As the scan crosses each folder, its cards' words lift and fade; the matches rise back out,
   their matrices interpolated from the floor to flat. The email is measured once the fonts load and covered by opaque
   squares, column by column.
7. **A vertical cut.** The 9:16 version frames the same world on its centre column (the city, the invoice and the logo
   row are all under 1,080 wide), grows the full-frame layers to cover portrait, and moves the search field and the
   type.

## Gotchas worth knowing

- Put a moving element's opacity on a wrapper group, not on the element you `<use>` elsewhere: a `<use>` copies the
  attributes of what it points to, so fading the desk would fade the loupe and the first card with it.
- Elements inside `<defs>` are not rendered, so `getBBox` on them returns nothing useful: measure a hidden clone in the
  live SVG, then remove it.
- Interpolating the four numbers of two linear matrices is enough for a convincing tilt in 2D; move the translation
  separately, along an arc.
- Give the scrim's mask an explicit region (`maskUnits="userSpaceOnUse"` with x, y, width and height) larger than the
  frame, or the mask clips at its default box and the scrim stops short.
- Brand rules hold in motion: the logo is the official file, flat, never redrawn or recoloured; the gradient appears
  only on the hero moments; redaction is solid pixels, never a soft smear.
