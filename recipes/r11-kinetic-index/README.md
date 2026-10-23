# R11 · Kinetic Index

![Rows of titles in four sizes drifting across a dark frame, with the titles that contain the word light lit orange and underlined, and a search box typing light.](poster.jpg)

A prompt types out, then rows of titles pour from its line at four sizes, each row drifting at its own speed.
A search box types three words that land on the beat: the matching titles light up, underlined, while the rest
fade back. Then the river rushes and tilts into a floor under a headline that drops in word by word.
Made as the intro film for the blog on Imagined Worlds. Any list of words works: posts, products, a menu, a
changelog.

**Watch it:** [visions.joaoqueiros.com/recipes/blog-intro](https://visions.joaoqueiros.com/recipes/blog-intro/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

10 s · 1920×1080 · 30 fps · HTML, CSS and GSAP · one take · score composed in code · €0 to make

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

## Make it yours

1. Put your own titles in `titles.txt`, one per line (at least 12), then run `python make-data.py`.
2. In `index.html`, change the three search words in `Q` to words that appear in your titles, then `PROMPT` and
   the headline (`#t-prompt`, `#t-title`, `#t-sub`).
3. Put the same three words in `Q` in `score/compose.py` (the score ticks once per typed letter), then:

        pip install numpy
        python score/compose.py

For a portrait version, change `data-width` and `data-height` on `#root` (the site's phone version is
`1080` by `1350`): the layout reads the canvas size.

## Files

- `index.html`: the whole film. One painter draws every frame from the clock.
- `titles.txt` and `make-data.py`: the demo titles and the script that writes them to `assets/data.js`.
- `score/compose.py`: the 100 BPM score in F major, timed to the picture.
- `CONCEPT.md`: the concept card for this recipe.

## Licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)). The demo titles are made up; use them
  freely.
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Fraunces, Instrument Sans and IBM Plex Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the names Imagined Worlds, JQ VISIONS and João Queirós, and the site's own lines used as the
  example (the prompt and the headline). Replace them with your own before you publish a remix.
