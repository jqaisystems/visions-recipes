# R37 · Batch

**Style:** a batch played as time. Time as the material, applied to stills: a folder of images in one texture array
in the CSV's order, and one WebGL2 fragment shader where every pixel picks its own still, for a slit that freezes a
flipbook, letters that show a later take, near-duplicates that melt into each other, rows displaced in time and a
tunnel of stills, under a 2D canvas and HTML type.
**Made for:** the Adobe Stock Uploader, batch metadata, validated first.
**Length:** 33.75 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · GLSL · GSAP · Python (CSV, checks, table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.75-second 1920x1080 film in HyperFrames for the Adobe Stock Uploader, my system that reads a
folder of images and writes a title, exactly 46 ordered keywords and a category for each, then validates the CSV before
upload. Use time as the material: put the hundred stills of one real batch into one texture array in the CSV's order and
play the batch like footage, in one WebGL2 fragment shader where every pixel picks its own still. Near-black ground, one
off-white line weight, teal for what passes, Libre Baskerville, Inter and JetBrains Mono, and a score composed in code
at 96 bpm. Read the CSV in Python, group the stills into concepts by their filenames, and re-run the uploader's checks.
One folder in: the stills flick past as a flipbook; a bright slit crosses the frame and freezes the batch into one
image, a column for each still. "One folder in,"
Every image read: the first still, a scan line, and its first six keywords lift out over what they name, their letters
showing a later take of the same picture. "every image read,"
Forty-six keywords: the real title types on, the words fly into a grid and the rest pop in, numbered, the first ten
boxed, then the image's category. "forty-six keywords, in order,"
Near-duplicates: the whole batch as one strip; inside each concept the takes melt into each other, between concepts
the seams cut hard, and each concept lights up with its count. "near-duplicates found,"
Validated first: the CSV as a wall of rows, each showing its own still displaced in time, while the checks tick one by
one, the banned words struck through, to "100 rows · 0 errors". "validated first,"
A human checks: the wall closes into one file, a tunnel of stills, and the two boxes a human ticks in the portal. "then
a human checks."
Title: the name in letters that each show a different still, then the logo, placed flat, never redrawn or recoloured,
with "Batch metadata, validated first." and the URL.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject} with time as the material:
{n_items} {your_stills} in one texture array, played as a sequence, and one fragment shader where every pixel picks its
own still. Flick through them until a slit freezes them into one image; read {one_item} with a scan line and lift
{its_first_words} out of it as letters that show {a_later_take}; set {the_full_output} in order under {its_title};
lay the whole set out as one strip where {each_group}'s takes melt and the groups cut hard; run {the_real_file} past as
a wall while {your_checks} pass; close it into {one_file} and dive through a tunnel of the stills to {the_human_step};
end on the name in letters cut out of the set and {your_mark} with {line} and {url}. One baked table drives the beats,
the type and a score composed in code.
```

Ideas:

- A photo culling app: a wedding's two thousand frames as one strip, the burst shots melting together, the keepers lifting out with their star ratings.
- A product catalogue tool: every SKU photo in one array, each product's colourways melting into each other, its attributes lifting out of the picture.
- An archive digitiser: scanned pages played as a flipbook, the OCR's words lifting out of each page and the duplicates found as motion.
- A font foundry: every weight of a family as one strip, the glyphs melting from thin to black, the specimen's metrics checked as a wall.

## How it's built

1. **The flipbook and the slit.** Ahead of the slit the frame shows the still the batch has reached; behind it each column keeps the still that was playing when the slit passed, so the batch freezes into one image, one column for each still.
2. **Read.** A scan line crosses the first still and everything above it settles darker. As it passes each word's place, the word lifts out of the picture.
3. **Letters from a later take.** Each lifted word is drawn into an offscreen mask that names a still in its green channel, so its letters show a later take of the same concept, in the same place.
4. **Forty-six, in order.** The six lifted words fly to the first slots of a numbered grid and the other forty pop in after them; the first ten are boxed, the slots where order matters most.
5. **Near-duplicates as motion.** Each band of the strip is one concept, as wide as its count. Its columns cross-fade through the concept's own takes along a wave, so near-duplicates melt into each other while the seams between concepts stay hard.
6. **The wall.** Each row of the CSV shows its own still through its line of text, sliding in time at its own rate, while the uploader's checks tick and count up to 100 of 100.
7. **A tunnel of stills.** Two planes run to a horizon, and each ring of depth is the next still of the batch, so the dive runs through the whole set.
8. **Type cut out of the batch.** The title is drawn into the same mask, a different still for each letter, over the batch held as one image.

## Gotchas worth knowing

- Draw the letter mask with additive blending and divide its green channel by its red: antialiased edges scale both by the same coverage, so the ratio still names the right still.
- Lift the stills that fill the letters (a floor of about 0.4 plus the picture): a word laid over a dark part of a later take disappears into it otherwise.
- Let each concept's band cycle through its takes slowly: one take every few pixels reads as stripes, while about one take across the band shows the pictures melting.
- Keep the batch in the CSV's order: the concepts then sit together without a separate sort, and the strip, the wall and the tunnel all agree on which still is which.
- For the portrait cut, extract each still's own 9:16 centre from the source: cropping the landscape array leaves less than half its width, and stretched to full frame it goes soft.
- Keep the shader in a JavaScript template string, not a script tag with a custom type: the HyperFrames linter parses
  inline scripts and fails on GLSL.
