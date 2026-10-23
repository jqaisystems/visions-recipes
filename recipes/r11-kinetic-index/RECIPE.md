# R11 · Kinetic Index

**Style:** a prompt types out, then rows of titles pour from its line at four sizes, each row drifting at its own
speed and direction. A search types three words that land on the beat and light up the matching titles while the
rest fade back, then the river rushes and tilts into a floor under the headline.
**Made for:** the blog on Imagined Worlds (visions.joaoqueiros.com/blog). It's the page's intro film.
**Length:** 10 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · HTML · CSS · GSAP (one clock and its eases) · Python (titles and score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 10-second 1920x1080 intro film in HyperFrames for my blog, Field notes for imagined worlds, on #0b0a09.
The prompt "/index visions --searchable --field-notes" types out in IBM Plex Mono with an ember #ff6d3b caret.
On Enter it lifts into the HUD and rows of my real post titles pour out of its line in Fraunces at four sizes,
each row drifting at its own speed and direction, separated by ember dots. A search box types three queries,
each landing on the beat of a 100 BPM score: the titles that contain the word turn ember with the match
underlined, while the rest fade back. Then the river rushes, tilts back into a receding floor and dims, and the
headline "Field notes for imagined worlds." drops in word by word, the second line in Fraunces italic ember,
with the prompt above it and "Practical research on AI image and video tools." below.
Titles only, no thumbnails, and no counts anywhere: the blog grows.
Technique: one painter draws every frame from time; build every row's markup up front; a Python script pulls the
titles from my blog's data.
Score: compose it in code with numpy, 100 BPM in F major: a tick per typed letter, a chime as each search lands,
air and a riser for the tilt, and one hit for the headline.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, on {background}.
The prompt "{prompt}" types out, then rows of {list} pour out of its line in {display_font} at four sizes, each
row drifting at its own speed. A search types {word_1}, {word_2} and {word_3}, each landing on the beat: the
matching items turn {accent} with the match underlined while the rest fade back.
Then the rows rush and tilt into a floor under the headline "{headline}", word by word.
No counts anywhere. One painter draws every frame from time; build every row's markup up front.
Score composed in code at {bpm} BPM: a tick per letter, a chime on each match, one hit for the headline.
```

Ideas: a shop's product names searched by colour; a restaurant menu searched by ingredient; a changelog
searched by feature; a portfolio's client list searched by sector.

## How it's built

1. **A river of rows.** Rows at four sizes fill the frame top to bottom. Each one gets its own order of the
   titles, a speed and a direction from a seeded hash, so the river has depth and every render is the same.
2. **Distance, not speed.** The river speeds up and slows down over the film, so each row's position comes from
   the distance travelled up to that moment, summed in small steps. Any frame can be rendered on its own.
3. **Markup built up front.** For each search, every row's HTML (with the matches wrapped and underlined) is
   built once at load. On a frame the painter only swaps in the right version and sets opacities.
4. **Searches on the beat.** Each query types out, then lands on a beat of the 100 BPM grid; the matches light
   up as it lands, and the query deletes just before the next one.
5. **The tilt.** The whole river gets a perspective and a rotateX of up to 58 degrees, so it falls back into a
   floor while it rushes and dims under the headline.

## Gotchas worth knowing

- Register the italic as its own font family. Registered as an italic style of the same family, Chrome rendered
  some roman rows in italic.
- Wrap each row in two copies of the same content so it can loop: the offset wraps at one copy's width.
- The underline is a border on the match, so it adds no width and a row only needs measuring once.
- Keep the three words in the score and the picture the same: the score ticks once per letter.
