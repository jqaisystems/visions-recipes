# R35 · Pop-Up

![A paper pop-up book open on a linen table: on the left page a terracotta pull tab and a pointer on a tone scale from formal to casual, with three tone cards standing up, plain, warm and direct; on the right page a skyline of three paper buildings labelled Competitor A, B and C; seven coloured section tabs fan out of the book's edge, under the words "how it should sound,"](poster.jpg)

## Purpose

A film for the AI Brief Generator, João's internal tool that turns a client intake form into a structured creative
brief, made as paper cut-out stop motion in a pop-up book. Every spread is a section of the tool's own template.

- **Intake:** a form and the optional call notes slide in under a closed book marked as a sample.
- **Synthesis:** the cover opens and two vague answers are pulled through a slot and come out as concrete chips; the
  seven section tabs fan out.
- **Audience:** three invented personas stand up on a box fold.
- **Tone and competition:** a pull tab moves a pointer on a tone scale; three unnamed competitors rise as a skyline,
  with a card for the gap.
- **Visual and scope:** a fan of swatches and a type specimen spring up; the deliverables stand up line by line.
- **Questions:** a ? flap swings open on two questions for a person.
- **Edit:** a red pencil strikes a word, writes a better one and ticks the lines; a stamp says reviewed.
- **Export and title:** the book closes, folds flat into a PDF and goes into an envelope; the logo lands, flat.

Made for the AI Brief Generator. The client, the answers and everything in the brief are an invented sample, the
competitors are unnamed, and no time or result is claimed.

**Source release:** [Pop-Up source](https://github.com/jqaisystems/visions-recipes/releases/tag/r35-popup-v1)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

33.4 s · 1920×1080 · 30 fps · one Canvas 2D, paper cut-out on twos in an orthographic 3D view · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge. The bake and the score need Python; the score needs `pip install numpy`.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render    # MP4 to renders/

## Editable elements

1. **Your input and your story.** The intake form, the call notes, the vague answers and what each becomes, the
   sections, the personas, the tone words, the competitors, the swatches, the deliverables, the questions, the summary
   and the pencil's edit are in `bake/table.py`. Change them and run `python bake/table.py`.
2. **Your mark.** The end card is the image in `assets/brand/`, placed flat as `#t-logo`, with the name, line and URL
   set as text in `index.html`.
3. **The clock.** The beat grid, every event (`E`), the sections (`T`) and the HUD are in `bake/table.py`.
4. **The look.** The paper stocks (`STOCK`), the view angles (`PSI`, `PHI`), the book's size (`PW`, `PD`, `BT`), what
   is printed on each page (`FACES`), the camera's keys (`camAt`) and the light (`makePost`, `post`) are in
   `index.html`.
5. **The score.** Rebuild it with `python score/compose.py`.

## Source files

- `index.html`: the whole film.
  - `piece(P)`: one piece of paper, a torn outline, a stock, a shadow and whatever is printed on it.
  - `pl()`, `plane(O, U, V)`: the orthographic view; `plane` sets the one affine transform that draws a flat piece on
    any plane in the scene. `flat()` lies a piece on the table, `stand()` stands a card on its hinge.
  - `leafA()`, `rise()`, `stackY()`: the angle of each leaf, how far each spread's pop-ups stand, and the height of
    each stack of pages.
  - `leaf`, `block`, `board`, `drawTabs`, `drawBook`: the book. `pops0` to `pops4`: the pop-ups, a spread at a time.
  - `drawTable`, `drawIntake`, `drawExport`: the table, the form going in, the PDF and the envelope.
  - `paint(t)` snaps `t` to a pose and draws the whole frame for it.
- `bake/table.py`: the one table. `score/compose.py`: the score, timed to the table.
- `CONCEPT.md`: the concept card for this recipe.

## Credits and licences

- **Code, composition and score:** MIT (see the repo [LICENSE](../../LICENSE)).
- **GSAP** (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- **Fonts:** Archivo, Instrument Serif and JetBrains Mono are under the SIL Open Font License 1.1
  (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the JQ AI SYSTEMS logo (`assets/brand/jqai-logo.png`) and the names JQ AI SYSTEMS and AI Brief
  Generator. Use your own mark in a remix. The AI Brief Generator itself is not public and is not in this repo; only
  the film's code is.
- **Sample data:** the client, the answers, the personas and everything in the brief are invented for this film.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
