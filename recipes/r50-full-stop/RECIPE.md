# R50 · Full Stop

**Style:** motion graphics led by one character. Every frame is a pure function of the beat, drawn in Canvas 2D with per-letter type, exposed over 12 to 24 sub-frames for real motion blur,
then printed by one WebGL2 pass that can turn the frame into halftone, dither, ASCII, a line screen, pixels, riso or neon. No simulation, no footage and no 3D engine.
**Made for:** AI Automation Systems, a service: custom Python pipelines for repetitive, high-volume work, where the client keeps every file, prompt and config.
**Length:** 40 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · Canvas 2D · WebGL2 · GSAP · Python (score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 40-second 1920x1080 film in HyperFrames for AI Automation Systems, a service that builds custom Python pipelines for repetitive work. Make it dynamic motion graphics, like a motion designer's showreel. The hero is a full stop: one red dot, #FF3A1F, ends every sentence in the film and won't stay put, because a full stop that keeps going is a task that keeps running. It stops once.
Every frame is a pure function of the beat: 112.5 bpm, 75 beats, 30 fps. Draw in Canvas 2D with per-letter type in Archivo at 900, and give the dot real animation: stretched along its speed, squashed on landing, with anticipation and overshoot. Expose each frame from 12 sub-frames over half a frame's time, added in linear light in a float buffer, and 24 on the fastest moves. Then print it with one WebGL2 pass that can turn the frame into halftone, Bayer dither, ASCII, a line screen, pixels, riso or neon, and always keeps the dot red. Bone, ink, cobalt, yellow, mint and pink. A "AI AUTOMATION SYSTEMS · DEMO WORKFLOW" label stays on screen wherever there's a demo. One timing table drives the film and the score. The score is composed in code in A minor: a tight funk kit and slap bass, a rubber ball for every landing, marimba for the map, and one instrument per style.
The same task: the dot falls onto empty paper and bounces, then dashes right three times and drags "THE SAME TASK" out behind it, ending as its full stop.
Again: it jumps off, the sentence falls away, and it lands to raise "AGAIN." on black behind an iris, then "AND AGAIN." on yellow.
Doubling: one tile becomes 2, 4, 8, 16, 32 and 64, every one running the same little job. The camera falls into one dot until the screen is red.
Plain English: karaoke. The dot lands on each word of "IF YOU CAN DESCRIBE IT", and each word gets up to meet it.
The map: the dot draws a workflow node by node: INTAKE, SORT, CHECK, DRAFT, REVIEW, SEND. The camera rolls at each corner, so the dot always runs left to right. It pulls back to the whole map, and the dot flies off to end "MAPPED BEFORE ANY CODE."
Code: the dot is the dot in task.run(), over scrolling demo code. Then "CUSTOM PYTHON."
Not a template: the same words and the same bounce in twenty cuts across sixteen styles: Swiss, halftone, extrusion, dither, moire, ASCII, slices, neon, a stack of widths, riso, Bauhaus, pixel, warped checker, echo outlines, a gradient line screen and blueprint. One a beat, then two, then four.
Nothing: black, one dot, two ticks.
On your schedule: a clock fills hour by hour, then you fall through nested clock faces from 06:00 to 00:00 as the day goes from morning to night, with the dot orbiting faster and faster. A chip says "SCHEDULED RUNS, IF YOU WANT THEM".
Handed over: "EVERY FILE." sheets stack. "EVERY PROMPT." prompts slide. "EVERY CONFIG." a wall of switches flips.
Yours: five letters, five slams, Y O U R S. The dot comes in from far away, lands, bounces smaller and smaller, and stops. So does the music: real silence, then dark spreads out from the dot.
Close: the dot travels to end "AI Automation Systems." The logo lands flat, never redrawn or recoloured, with the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The workflow, prompts, code and clock times are demos. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} motion graphics film in HyperFrames for {product}, led by one character: {a_small_shape} in {one_hot_colour}, which is {what_it_means_in_your_story}. Draw every frame as a pure function of the beat in Canvas 2D with per-letter type in {your_typeface}, expose it from 12 to 24 sub-frames for real motion blur, and print it with one WebGL2 pass of halftone, dither, ASCII, riso and neon that never touches the character's colour. Let it carry {your_sentences}, multiply {the_repeated_thing} from one tile to 64, draw {your_diagram} with a camera that rolls at each corner, then run {your_claim} through a roll of {number} graphic styles that gets faster and faster. Drop to nothing, build {your_second_idea}, and hand over {what_they_keep}. Let the character stop once, on {your_last_word}, and stop the music with it. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm with a score composed in code.
```

Ideas:

- A punctuation mark for an editing tool: a comma that keeps a sentence alive, stopping only when the copy is right.
- A loading dot for a developer tool: it runs through every style while it waits, and stops when the build is done.
- A ball for a sports brand: the same bounce through twenty looks, stopping only in the net.
- A cursor for a design course: one blinking line draws every lesson, and it stops on the student's own name.

## How it's built

1. **The dot gets a personality.** It falls, bounces four times with shrinking squash, and dashes three times. By the end of the first sentence it's a character and not a shape, and everything after depends on that.
2. **The same move, on purpose.** It leaves, and the same landing raises AGAIN, then AND AGAIN, each through an iris from the dot. The repetition is the point of the service.
3. **From one to 64.** The screen doubles six times on the beat, every tile running the same job. Then the camera falls into one dot until the frame is solid red, which is the wipe into the next scene.
4. **A camera that rolls.** The workflow turns corners, but the camera rolls with it, so the dot always runs left to right and the labels stay upright. It only shows you the shape when it pulls back.
5. **The roll.** NOT A TEMPLATE stays in the same place with the same bounce through twenty cuts. Sixteen styles are drawn in Canvas 2D or printed by the shader, one a beat, then two, then four.
6. **Nothing.** After the fastest moment in the film comes black, one dot and two ticks. The roll only feels fast because of what comes straight after it.
7. **A fall through the day.** Nested clock faces scale exponentially, so the fall can loop for as long as it's needed. The dot's orbit speeds up, and the colours go from morning to midnight.
8. **The stop.** Five slams, one long flight in, and bounces that halve each time. The score is gated hard at the same beat, so the silence is real, and dark spreads out from the dot to the end card.

## Gotchas worth knowing

- A print pass reads brightness, so it eats a coloured dot. Test for the dot's colour and put the original pixel back after every process, or the hero turns grey in half the film.
- A chromatic split on the beat is lovely on plain frames and ruins printed ones: it turned ASCII and halftone magenta. Only run it in the plain mode.
- Only squash the dot on a real landing. If every key squashes it, the dot goes flat each time it's just waiting for the next beat.
- Twelve sub-frames show visible steps on the fastest camera moves. Raising the count for three short ranges costs far less than raising it for the whole film.
- Don't crop a film like this for portrait. Most of the words won't fit, so re-lay them: the font's width axis keeps TEMPLATE and YOURS tall and not just small.
