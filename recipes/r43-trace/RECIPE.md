# R43 · Trace

**Style:** oscilloscope music. One beam of light steered by the film's own WAV: left channel across, right channel up and
down. How fast it redraws an image is the note. There is no separate music bed.
**Made for:** Codex Control Center, a local-first dashboard that keeps the shape and not the words.
**Length:** 34 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait, with its own WAV.
**Stack:** HyperFrames · WebGL2 · Python (NumPy) · GSAP · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 34-second 1920x1080 film in HyperFrames for Codex Control Center, a local-first dashboard that keeps the
shape of a session and not its words. Make it dynamic motion design, a showreel piece. The soundtrack is the picture: the film is
one beam of light on an oscilloscope, where the WAV's left channel is x and its right channel is y, so nothing is in the signal
that isn't drawn and there is no separate music bed. One Python script builds both from one array at 48 kHz: a hand-made
single-stroke font, a 3D wire projector, a path sampler where pen-up jumps are nearly instant, and morphs that blend two paths
sample for sample. How fast an image is redrawn is the note: tune the rates to E, C, A and B at 120 bpm, 68 beats. A kick throws the
picture and pumps its size, a snare frazzles it, and a held dot is silence. The script writes the WAV and the same samples for the
film. The film draws each frame's samples as additive WebGL2 line segments, brighter where the beam moves slowly, with an afterglow,
bloom, curved near-black glass #030505 and a faint graticule. The colour is keyed by time: teal, aqua, amber for the gate, red for
the refusal. All log text and figures are fictional and labelled DEMO DATA.
The dot: a dot and a hum open into Lissajous figures and a wire sphere.
The log: a demo log whose private words melt into waveform. "SEES THE SHAPE", "NOT THE WORDS", "METADATA ONLY."
Observe: a wire 3D dashboard turning in space. "NO API KEY TO OBSERVE."
The gate: a wire gate, "APPROVE?", the beam collapses to a held dot and the sound stops. The gate opens into a tunnel. "READ-ONLY".
"FULL ACCESS" gets a red X and a harsh buzz.
Publish check: words fall through a wire grid and scatter, three things stay and get ticked. "CHECKED BEFORE IT'S PUBLIC."
Close: the tube switches off to a line and a dot, then the logo placed flat, silent and never redrawn or recoloured, with
"Codex Control Center", the URL and "Open source · MIT", drawn by the beam. Use "Codex" only in the system's name, take facts only
from the case study and claim no results.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, where the soundtrack is the picture: one beam of
light on an oscilloscope, with the WAV's left channel as x and its right channel as y. One script builds both from one array: a
single-stroke font, a 3D wire projector, nearly instant pen-up jumps and sample-for-sample morphs. Redraw rates are the notes, tuned
to {your_key} at {bpm} bpm; the kick pumps the picture's size, and a held dot is silence. Draw {your_forms} and {your_words} as one line,
with phosphor, bloom and curved glass, colour keyed by time from {your_colours}. Build to {the_big_moment}, collapse to a held dot just
before it, switch the tube off at the end, and place {your_mark} flat with {line} and {url}. Say plainly what isn't in the audio.
```

Ideas:

- A synth or audio plugin: the interface and its name drawn by the sound it makes.
- A band's album teaser: the track's own stems drawing the title and the sleeve as one line.
- A monitoring tool: a healthy trace, a fault, a recovery, with the sound changing as the picture does.
- A science museum: Lissajous figures turning into the exhibit's name, with the WAV as a free download.

## How it's built

1. **Lissajous.** Two sine waves at simple ratios, stepping up. It's the classic scope figure, and each step is a chord change you can see.
2. **A sphere as one line.** A wire sphere is projected in Python and walked as one path, so turning it changes the sound's timbre.
3. **Words melt.** The demo log's private words are morphed sample for sample into waveform, while time and event stay as letters.
4. **A dashboard in one line.** Bars, a ring and a number on a turning 3D plane, labelled DEMO DATA by the beam itself. More strokes mean a dimmer picture, so density is a budget.
5. **Silence is a dot.** A dot has no movement, so it has no sound. The film's biggest pause isn't an edit: the picture and the sound collapse as one thing.
6. **The tunnel.** Squares in depth at full volume. The zoom and the pitch come from the same numbers, and READ-ONLY gets its own larger scene so it has enough samples to hold.
7. **The X.** The beam's colour turns red by the time key, and the added strokes make the buzz harsher. The refusal is heard because it's drawn.
8. **Switch-off.** The picture collapses to a line, then a dot, and the sound goes with it. The logo that follows is flat and silent, and the copy says so.

## Gotchas worth knowing

- Too few samples in a redraw and a word collapses. Use fewer letters per scene, or a slower rate, which lowers the note.
- Pen-up jumps still cost samples and show as lines. Weight them to almost nothing and they nearly vanish, but never entirely.
- Scope audio is harsh by nature. Round the corners a little, tune the rates and keep it short, and judge it on speakers.
- A compressed copy only approximates the signal, so a claim about the picture has to point at the WAV a reader composes.
- Be exact about the claim. Colour, the logo and the glass aren't in the audio, and saying so makes the rest of it more impressive.
