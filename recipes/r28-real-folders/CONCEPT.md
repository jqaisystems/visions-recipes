# R28 · Real Folders · concept

**Style (season 2, film 3 of 3, the finale): 2D vector motion design.** SVG and GSAP only, like R26 and R27: no
WebGL, no canvas, no 3D engine. R26 used morphs, line draws and mattes, and R27 used ribbons, glyph morphs and
branching. This film closes the season with techniques new to the library:
- **isometric vector:** a whole city of folders drawn flat in code, every face a 2D shape placed by one isometric
  matrix, so depth comes from geometry, not a 3D renderer;
- **the selection is a mask:** Snapline's own capture overlay (scrim, marching ants, corner handles, px chip) as a live
  SVG mask that reveals and crops the world;
- **a live loupe:** a round lens that shows a magnified copy of the scene under it (a scaled `<use>` clipped to a
  circle), with a pixel grid;
- **solid pixels:** redaction as a cascade of square blocks snapping over the text, never a soft smear;
- **flat colour:** Snapline's dark ground, with the violet-to-orchid gradient kept for the hero moments only.

**Made for:** Snapline (snapline.joaoqueiros.com), a screenshot and screen recording manager for Windows, free on the
Microsoft Store. Its own line is "Screenshots and screen recordings, organized into projects", and the showreel's
"Real folders, not a database." This film is pure vector, with no
screenshots of the app.

**The idea:** a screenshot is only useful once it's filed. Snapline files every capture as you shoot, into real folders
on your own PC, finds the words inside it, and makes it ready to send.

1. **The shutter (0 to 4 s).** A dark desktop of flat vector windows. The capture overlay drops in: the scrim, a
   crosshair, the loupe magnifying real pixels, then a marching-ants selection drags out with its px chip. Shutter
   flash. The selected region lifts off as a card.
2. **A flood of captures (4 to 9 s).** Card after card, shutter after shutter, faster on the beat, until dozens of
   flat cards hang in the air. The camera tilts into an isometric view and a city of folders rises from the floor,
   each folder a project. Every card flies into its folder. "Real folders, not a database."
3. **Found by its words (9 to 15 s).** A search field types "invoice". A scan line crosses the city; the words inside
   every card lift off as text, and only the matching cards rise out of their folders and light up, with "text in
   image · match" chips.
4. **Marked up and redacted (15 to 21 s).** The camera dives into one card. An arrow and a box draw on, a step badge
   pops in, and an email address on the card snaps into solid pixel blocks, square by square, under "redact · solid
   pixels".
5. **Client-ready (21 to 27 s), the showpiece.** The card lifts off the folder city onto a backdrop that floods from flat
   ground into the violet-to-orchid gradient, gains padding and rounded corners, and turns to face the camera. Then the
   same card becomes a screen recording: a REC frame, a timer, and a strip of frames unrolling beneath it.
6. **Title (27 to 32 s).** The folder city folds back into the floor, the capture overlay selects the empty centre, the
   shutter fires, and the official Snapline logo sits in the selection, flat. Then the line, "Free · Windows 10 and 11
   · no account needed", and snapline.joaoqueiros.com.

**Spec:**
- 32 s, 1920×1080, 30 fps, with a 9:16 cut.
- One SVG stage, one root camera group, `paint(t)` a pure function of time (the season's skeleton).
- Isometric faces drawn flat from one matrix.
- The selection is a `<mask>` updated each frame; the loupe is a `<use>` of the world, scaled under a circular clip.
- One baked Python table holds the shutters, the cards, the folders, the search hits, the redaction blocks and the
  recording frames. The score is composed in code from it.

**Score:** 108 bpm, A minor to C major. Clean electronic: a shutter click on every capture, which become a rhythm as the
flood speeds up, a soft thock for every card filed, a typing tick per letter of the search, a rising chime for every
match, short bit-crushed blips as the pixels snap into place, a warm pad as the gradient floods in, and a final shutter
on the logo.

**Palette and type (Snapline's frame.md):**
- Colours: ground #0a0c11, panel #11141b, panel-2 #161a23, text #e8ebf2, muted #8b94a8, accent #6f72f1, lavender #c9c4ff.
- The violet-to-orchid gradient #6e63f2 → #9e57f6 appears only on hero moments: the client-ready backdrop and the logo.
- Green #34d399 for UI ticks only.
- Type: Bricolage Grotesque 700/800 for titles, Inter for body, JetBrains Mono for px chips, timers and labels.
- Expo and power3 eases, one shutter flash per capture, no bounce on the logo.

**Brand rules kept in motion:**
- The official logo file, unchanged and flat; the Microsoft Store badge only as the official file, with no implied
  endorsement.
- Redaction is "solid pixels", never a soft smear.
- AI is never implied as on by default; OCR is described as offline.

**Honesty:**
- Every window, card, client and email address is fictional demo content.
- No metric, rating, download count or number of captures appears on screen.
- "Local-first" only as the product says it: captures save to your own folders, and offline OCR stays on your PC.
