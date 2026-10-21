# R01 · Token Rain · concept card (approved by João 2026-10-21; final line "Same model. Your voice.")

**Style (reusable):** Token Rain. Text dissolves into particles, the particles flow through a sequence of gates,
then recompile into new text. Anyone can swap the phrases, the gates and the palette.

**Subject:** Prompt Engineering, service 12 on ai.joaoqueiros.com
(`/services/prompt-engineering`). Approved tagline: "Structured, branded prompt libraries and multi-step chains
that make the right model write in your voice and reason about your domain."

**Story in one line:** a generic AI paragraph has its clichés caught by the anti-pattern library. The clichés burn
into token rain, the rain falls through the chain (draft, critique, rewrite) and lands as one sharp line in the
brand's voice.

**Spec:** about 26 s, 16:9 1920×1080, 30 fps; a 9:16 cut later. The score is composed in code, so the source zip
can ship under MIT.

**Look:** the ai site's dark palette. Background #111110, text #F5F5F0, teal #00A89D, blue #0099D6, live green
#22D390. Type in Geist, Geist Mono for the prompt field and labels, and Instrument Serif for the final line.

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 4 s | A caret types a brief into a mono prompt field. A stock AI paragraph streams back ("In today's fast-paced world, we're thrilled to unlock..."). | type-on, token streaming |
| 4 to 9 s | A teal scan line passes the paragraph: the anti-pattern library. Flagged phrases light up, lift off and shatter into glyph particles. The rest of the text stays readable. | text to particles (glyph pixels sampled to positions) |
| 9 to 15 s | Token rain: tens of thousands of particles pour through three glowing gates labelled draft, critique, rewrite, as the camera dollies down. | Three.js instanced points, TSL noise flow field |
| 15 to 21 s | The rain converges and recompiles into one serif line, which holds for a clean read. | particles to text, eased settle |
| 21 to 26 s | Lockup: Prompt Engineering · JQ AI SYSTEMS · ai.joaoqueiros.com | the particles of the line become the underline |

The seams are continuous particle moves, with no fades. Held text and the lockup get no beat punches or scale
pulses, only one eased drift.

## Technical approach and risk
- The particles are pure functions of time (seeded position, then a curve), with no simulation state, so the
  render is deterministic in HyperFrames' parallel workers.
- Three.js WebGPURenderer with TSL, forced onto its WebGL2 backend for the headless render. **First step after
  approval:** a 2 s spike render to prove the GPU path, before the full build.

## Remix knobs (for the recipe page)
`{brief}`, `{cliche_phrases}`, `{gates}`, `{final_line}`, `{palette}`, `{particle_count}`, `{duration}`

## Open choice for João
The final line. Options: "Same model. Your voice." / "Your voice, every time." / his own line.
