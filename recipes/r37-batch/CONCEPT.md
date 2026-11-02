# R37 · Batch · concept

**Style (season 5, film 2 of 3): time as a material.** It uses R36's engine: one WebGL2 fragment shader, a
`sampler2DArray` of real frames, and every pixel picks its own moment. The new move is that the "footage" is a
**batch of stills played as time**. One hundred stills sit in one texture array, so the batch becomes a film, and
everything the shader does to time it now does to the batch.

**Made for:** the Adobe Stock Uploader (ai.joaoqueiros.com/systems/adobe-stock-uploader), João's internal system
that reads a folder of images and writes upload-ready metadata. The case study's own line is "Batch metadata,
validated first."

**The stills:** the hundred stills of one of João's real batches (AI-generated for stock) and the uploader's own CSV for
them, read by `bake/prep.py` and never committed. In this repo, `bake/demo.py` makes a stand-in batch and CSV.

**The idea:** a contributor's batch is really a sequence: eight takes of one idea, then the next idea. Play the
batch as a film and the near-duplicates *move*: the variants of one concept slit-scan into each other like frames
of one shot, while a change of concept cuts hard. The thing the duplicate check looks for becomes visible as motion.
The film reads the batch the way the uploader does: one image at a time, then all of them at once.

1. **One folder in (0 to 4 s).** The hundred stills play as a flipbook at 24 frames a second, a strobing film of
   greenhouses, light trails, surf and coral. A bright slit sweeps across, and behind it the batch freezes into one
   slit-scan image, each column a different still. "One folder in,"
2. **Read the actual image (4 to 9 s).** Time stops on one still, the abandoned greenhouse. A scan line crosses it,
   and where it passes, words lift off the picture: greenhouse, abandoned, glass, panels, broken. Each word is cut
   out of time, showing the still a few frames later through its letters. "every image read,"
3. **Forty-six keywords, in order (9 to 14 s).** The words stack into a column, counted 01 to 46. The first ten
   hold brighter, the slots where order matters most, and the real title types itself above them: "Abandoned
   Industrial Greenhouse Wall with Broken Glass and Copy Space". "forty-six keywords, in order,"
4. **Near-duplicates (14 to 19 s).** The whole batch is laid out as one strip of time, ten bands wide. Inside each
   band the variants melt into one another in a time smear; between bands the seams cut hard. Each band lights up
   as one near-duplicate group, with its real count (8, 12, 16). "near-duplicates found,"
5. **Validated first (19 to 26 s).** The hundred CSV rows scroll as a wall of stripes, each row's still showing
   through its own line of text, displaced in time. The checks run down the wall and tick, one rule at a time:
   - 46 tags;
   - no repeats;
   - lowercase;
   - no banned terms (the banned list shown struck through: stock, photo, image, picture, download, preview, ai,
     generated, generative);
   - title length;
   - unique filenames.

   It ends on "100 rows · 0 errors". "validated first,"
6. **Portal-ready (26 to 30 s).** The wall collapses into one CSV file, and the camera dives through a slit-scan
   tunnel built from the hundred stills, one ring per still. A short checklist lands at the end: the boxes the
   human still ticks in the portal. "then the human checks."
7. **Title (30 to 33.5 s).** **Adobe Stock Uploader** in letters that each show a different still of the batch,
   over a frame held still. "Batch metadata, validated first." The JQ AI SYSTEMS logo lands flat, never redrawn or
   recoloured, with ai.joaoqueiros.com/systems/adobe-stock-uploader.

**Look:** the stills carry the colour, so the graphics stay minimal:
- one off-white line weight;
- teal (#00A89D) from the ai site for the first ten keywords and the passing checks;
- type in Inter and Libre Baskerville, the case study's own pair, with JetBrains Mono for the CSV;
- a near-black ground (#0B0C0D).

**Sound:** a score composed in code, around 96 bpm:
- the flipbook as a soft shutter clatter that rises into a pitch;
- a keyboard-like pluck per keyword, rising through the 46;
- a low swell under the near-duplicate strip;
- a dry tick for each passing check;
- a wash under the tunnel;
- a two-note resolve on the logo.

**Honesty and brand:**
- **Facts used on screen**, all from the case study and the real CSV:
  - a folder of images in, one CSV out;
  - each image read visually;
  - one title and exactly 46 lowercase keywords per image, the strongest ten first;
  - near-duplicates flagged;
  - validation before upload (tag count, duplicates, banned terms, title length, unique filenames);
  - a final human review in the portal.
- **"100 rows · 0 errors"** is the result of the real checks on the real CSV, which I re-ran. It's not the case
  study's 108-row proof run, so the film never says 108.
- **Kept off screen:**
  - downloads, sales, acceptance rates or any results;
  - the portfolio size;
  - the separate duplicate audit against the live portfolio;
  - the vision model's name.
- **Third-party names:** the system's own name, Adobe Stock Uploader, is the only one. No Adobe logo or portal
  screens, and no model or tool names.
- **Licence:** the uploader is private, so the recipe licenses only the film's code. The public repo ships none of
  João's stills: the README says "drop in your own folder", with a short procedural demo batch so it runs out of
  the box.

**Cuts:** 16:9, plus a 9:16 vertical re-laid for portrait:
- the keyword column runs full height;
- the strip of the batch runs top to bottom;
- the tunnel stays centred.

About 33 s.

**Stack:** HyperFrames 0.8.184 · WebGL2 (one fragment shader, texture arrays, R36's engine) · GSAP for the type ·
Python (the stills into the array, the CSV into a table, the checks, the score).


**As built:**
- **The CSV is the batch's final, revised file,** with real Category IDs, so each image's category is on screen
  (category 2 for the greenhouse; ten concepts, one category each).
- The uploader's checks, re-run on that file: 46 keywords, no repeats, lowercase, no banned terms, title length,
  unique filenames, category 1 to 21. All seven pass on all 100 rows: "100 rows · 0 errors".
- The six lifted words are the first six keywords, each placed over what it names in the greenhouse still; their
  letters show a later take of the same concept.
- 96 bpm, 33.75 s. The score is composed in code.
- **The 9:16 cut** (`videos/batch-vertical`) is re-laid for portrait, not cropped:
  - every still comes from its own 9:16 centre of the source (`p%03d.jpg`, 720×1280), and the first from a 1080×1920
    centre, so the full-frame portrait stays sharp;
  - the slit, the frozen batch and the ten concept bands run down the frame;
  - the six words are placed over what they name in the portrait crop;
  - the keywords sit in three columns of sixteen, and the checks in two columns under the wall.
