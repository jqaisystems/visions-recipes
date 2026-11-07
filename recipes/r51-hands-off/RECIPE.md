# R51 · Hands Off

**Style:** sand animation on a lightbox, in code. The sand is one WebGL2 height texture, one height per pixel, run forwards frame by frame. A stroke shader pushes, sweeps and lays it, a slump pass lets it settle,
and a shade pass sends light up through it, so thin sand breaks into grains and thick sand stops the light. No footage and no 3D engine.
**Made for:** AI Automation Systems, a service: custom Python pipelines for repetitive, high-volume work, where the client keeps every file, prompt and config.
**Length:** 33.6 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.6-second 1920x1080 film in HyperFrames for AI Automation Systems, a service that builds custom Python pipelines for repetitive work. Make it a sand animation on a lightbox, in code: the live art where a performer draws and wipes images in sand on a glowing table. A fingertip draws the same task over and over, then lifts off the table, and the sand carries on without it.
The sand is one R16F height texture in WebGL2, one height per pixel, run forwards frame by frame. A stroke shader moves it three ways: a finger pushes it aside and leaves a ridge, the side of a hand sweeps it back in streaks, and sand can be laid down. A slump pass lets it slide until the slope holds. The shade pass is light coming up through it: test each grain against the thickness, so thin sand breaks up into single grains and thick sand stops the light, with a low lamp catching the slopes. Keep the halo around the lines small, or it reads as neon. The hand is a true silhouette built from capsules, with the table's light wrapping its edge. Amber light moving to night blue, and nothing else. Carve the words in with a hand-drawn single-stroke font, through the same engine. One table holds every stroke and drives both the film and the score, at 100 bpm. A "AI AUTOMATION SYSTEMS · DEMO WORKFLOW" label stays on screen. The score is composed in code in A minor: Karplus-Strong plucked strings, a hand drum, and noise shaped to every stroke, as loud as the stroke is fast.
Light on: black, a click, the table lights up amber, and sand pours in and spreads.
The same task: the finger writes "THE SAME TASK." and draws a sheet copied across to a second sheet. It wipes them with one sweep and draws them again, faster each time. "AGAIN." "AND AGAIN."
Plain English: one sweep clears the table, and the finger writes "IF YOU CAN DESCRIBE IT..."
The map: boxes and handoffs, with the handoff points pressed in deep. "MAPPED BEFORE ANY CODE."
The code: "CUSTOM PYTHON. NOT A TEMPLATE." and a short demo script, written faster than a hand should go.
Hands off: the finger presses one last dot and lifts away. Nearly silent. Then a sweep nobody made clears the table, and the same drawing draws and wipes itself, on the grid.
The wall: eight by four of them, each on its own loop, speeding up until the whole wall lands complete on one downbeat with one big hit. A sun drawn in the sand crosses the top.
On your schedule: the light cools to blue, a moon comes up, "ON YOUR SCHEDULE." is written, and waves of redrawing keep running through the wall.
Yours: morning clears the table to bright amber. Sand is laid back down as a folder, with "EVERY FILE. EVERY PROMPT. YOURS." The light clicks off.
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Automation Systems", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The workflow and the script are demos. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} sand animation on a lightbox in HyperFrames for {product}, in code. Keep the sand as one WebGL2 height texture run forwards frame by frame, with light coming up through it so thin sand breaks into grains and thick sand stops the light. A {what_draws_it} draws {the_repeated_thing} over and over, wiping it each time, then {your_second_drawing} and {your_third_drawing}. Then the {what_draws_it} leaves, and the sand carries on without it, until {how_many} of them run across the table. Carve {your_words} into the sand with a single-stroke font. Move the light from {first_colour} to {second_colour} for {what_the_change_means}. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where every stroke is noise as loud as it is fast.
```

Ideas:

- A handwriting course: a pen writes one line, over and over, until the student's own lines carry on without it.
- A bakery: a finger draws a loaf in flour on a lit board, then the loaves keep coming by themselves.
- A note-taking app: one hand sketches a note, the hand leaves, and the page fills in on its own.
- A climate report: sand drawn away from a coastline, a little more each year, with nobody touching it.

## How it's built

1. **The table lights up.** A click, a flicker, then amber. The pour grows as a noisy disc, so the sand arrives before anything is drawn on it.
2. **Teach the rule.** The finger writes and draws, and sand moves only where it goes. Every wipe is a real sweep, and the same drawing comes back faster each time.
3. **Carved words.** The words go through the same engine as the drawings, in a hand-made single-stroke font, so they stay part of the sand and aren't laid over it.
4. **Too fast for a hand.** The script is written faster than a hand should go, which is the first hint that something's about to change.
5. **The lift.** One last dot, deep, and the hand softens and grows as it rises towards the lamp. The music drops to almost nothing, and the table is empty of hands for the first time.
6. **The sweep nobody made.** The same wipe and the same task come from the same table with the finger switched off. Now the score sits exactly on the grid.
7. **The wall.** Thirty-two copies, each on its own loop, tighten from a wave until all of them land whole on one downbeat with one big hit.
8. **Night, then morning.** The light cools while the wall keeps redrawing, then morning clears the table and the folder is laid in dark sand on bright, the only inverted scene.

## Gotchas worth knowing

- Bright lines on black read as neon and not as sand. The first version did: cut the halo right back and let a low lamp pick out the slopes, so each line becomes a channel with a ridge beside it.
- A hand lit from above looks like a smooth plastic shape. Backlit, it should be close to black with the light wrapping the edge, which also hides most of what's wrong with a hand made from capsules.
- Bright gaps in the sand kill any words that cross them. Keep the sand thick through the middle of the frame and let the table show at the edges.
- The simulation only runs forwards, so seeking back means starting from zero. That's fine for a render but slow in preview, so keep test seeks moving forward.
- In portrait, the arm has to be much longer: when the finger reaches the far corner, the rounded end of the arm comes on screen.
