# R43 · Trace · concept

**Idea:** the soundtrack is the picture. The film is one beam of light on an oscilloscope, steered by its own audio: left is x, right is y. How fast the beam redraws an image is the note. Codex Control Center watches the shape of the activity and not the words, and an oscilloscope does the same.

**Technique:** `score/compose.py` builds both picture and sound as one signal: a hand-made single-stroke font, a 3D wire projector, a path sampler where pen-up jumps are nearly instant, morphs by blending two paths sample for sample, redraw rates tuned to E, C, A and B. It writes `assets/bgm/score.wav` and `assets/beam.js`, the same samples. `index.html` draws each frame's samples as additive WebGL2 line segments, brighter where the beam moves slowly, with bloom, curved glass and a graticule.

**Drums are the picture too:** the kick throws the picture and pumps its size (a real sidechain), a snare frazzles it. There is no separate music bed. A dot is silence.

**The film:** dot and Lissajous figures, a wire sphere; a demo log whose private words melt into waveform; "Sees the shape / not the words / metadata only"; a wire 3D dashboard; "No API key to observe"; a wire gate, "Approve?", the beam collapses to a dot and the sound stops; the gate opens into a tunnel, "Read-only"; "Full access" gets a red X; words fall through a wire grid and scatter; three things stay and get ticked; "Checked before it's public"; the tube switches off to a line and a dot; the logo.

**What the claim covers:**
- True: the WAV's left and right channels are the beam. Checked 2026-11-04: ffmpeg's own `avectorscope`, plotting only the WAV, draws "NOT THE WORDS", the dashboard, the gate with "APPROVE?" and the X over "FULL ACCESS" (its axes come out turned or flipped depending on the plot's settings, a display convention, and it shows the beam's fast jumps as thin lines). Rechecked on draft 2 for NOT THE WORDS and the X over FULL ACCESS.
- Not in the audio: the colour (keyed by time), the logo (a flat, silent image), the glass and the graticule, and the exposure, which is a brightness setting per frame.
- The site and social files are compressed, so "plot the WAV" must point at the WAV a reader composes from the source, not at the MP4's audio.

**Honesty:** facts only from the case study. Demo text is fictional. The dashboard figures (86, the bars, the usage ring) are invented and carry a DEMO DATA label drawn by the beam, as does the log. "Codex" only as part of the system's name. No results.

