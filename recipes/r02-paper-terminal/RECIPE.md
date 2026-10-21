# R02 · Paper Terminal

**Style:** a terminal window is a sheet of paper. A command prints a document onto it, the sheet folds along
its sections into a card, and the card files itself on a shelf of many others.
**Made for:** JQ AI Skills, JQ AI SYSTEMS (github.com/jqaisystems/jqai-ai-skills, 47 MIT skills).
**Length:** 26 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · HTML · CSS 3D transforms · GSAP (one clock) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames for JQ AI Skills, my library of reusable AI skill folders.
Story: a terminal drawn as a sheet of warm off-white paper. The same long brand-voice prompt has been typed on
Monday and Tuesday and is typed again today ("typed 103×"). Then "$ /skill brand-voice-linter". A roller
prints the real SKILL.md down the sheet in four sections: 00 Load the voice guide, 01 Scan, 02 Report,
03 Fix (only when asked). The sheet folds like an accordion along those four sections, with paper shading and
a teal crease on each fold, until only a strip is left. A card label stamps onto it, it flies onto a shelf,
and the camera pulls back to all 47 real skill names as paper cards. Five cards lift as they are called.
End on "Repeatable AI workflows, packaged as skills." and the repo URL.
Technique: CSS 3D only. Four strips nested inside each other, each hinged at its parent's bottom edge, so a
zigzag fold is three rotateX values. One painter function writes every element from time; no tweens fight.
The packet's flight target is computed from the shelf's own camera transform, so it lands exactly in its slot.
Brand: #111110 background, #F3F1EC paper, #0E0F0F ink, #00A89D teal, Geist, Geist Mono, Instrument Serif.
Score: compose it in code with numpy: key ticks, a printer roll, paper creases, a stamp, a slide, a warm
F major bed and a chime for each call, from the same timing table.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames.
A terminal drawn as paper shows {the_repeated_task}. Then "{command}". A roller prints {document} in
{n} sections: {section_titles}. The sheet folds along those sections into a card labelled {card_label},
which files itself on a shelf of {collection}. Pull back to the whole shelf, lift {k} cards as they are used,
and close on {final_line}. CSS 3D nested hinged strips, one painter writing everything from time.
Palette: {palette}. Fonts: {fonts}. Score composed in code with paper sounds, synced to the picture.
```

Ideas: a recipe that folds into a card in a recipe box, a contract that folds into an envelope in a filing
cabinet, a lesson plan that folds into a course catalogue, a bug report that folds into a closed ticket.

## How it's built

1. **A terminal that is paper.** The sheet is four strips; the terminal text is a layer above them. The prompt
   types from a fixed string, so every frame is exact, and the terminal scrolls like a real one.
2. **Print, then fold.** A roller line moves down the sheet: terminal text is clipped away below it, SKILL.md
   sections are revealed above it. Each strip is nested inside the one above and hinged at its top edge, so the
   accordion is three rotateX values (−178°, +178°, −178°) with shading from each strip's angle.
3. **A card, not a cut.** The shelf card is the same HTML element as the stamp on the folded packet, scaled up
   2.53×, so the hand-off from packet to shelf is invisible.
4. **A camera with maths you can trust.** The shelf is one layer moved by translate + scale. The packet's target
   each frame is the slot's position under that same transform, so it flies straight into place while the camera
   is still moving.
5. **Sound from the same clock.** Ticks for the typed prompt, a printer roll, one crease per fold pitched up each
   time, a stamp, a slide, a building pulse and a chime per called skill, all generated in Python.

## Gotchas worth knowing

- Text that ends in an ellipsis on purpose still fails a layout check if it overflows. Shorten it instead.
- Nested `preserve-3d` strips need `backface-visibility: hidden` on both faces, with the back face pre-rotated
  180°, or the folded sheet shows mirrored text.
- Keep the final camera slightly wider than the shelf (0.9 here) so the HUD lines never sit on top of the cards.
