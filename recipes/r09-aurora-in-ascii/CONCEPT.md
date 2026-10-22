# R09 · Aurora in ASCII · concept card (approved by João 2026-10-22: the Recipes library, green/teal/violet, shrink beat kept, subtitle "films, prompts and source")

**Style (reusable):** Aurora in ASCII. A real 3D scene is drawn only in text characters, like an old terminal
screen: every cell of a grid picks a glyph by how bright the picture is behind it, from " . : - = + * # % @",
and takes its colour. Anyone can swap the scene, the character set and the palette.

**Why now:** ASCII and dither shaders are a popular look in creative coding and motion design right now, often
mixed with Y2K terminal styling. The twist here: the text isn't a filter on a video. A live Three.js scene is
rendered and turned into characters in the same shader, so any frame renders on its own.

**Subject:** the Recipes library itself (/recipes on visions). It has no film of its own yet, and this is the
last of the planned nine, so it closes the set. No count on screen, as with the page intros.

**Story in one line:** a black terminal, a blinking cursor, and a command types itself: `render aurora --ascii`.
Characters start to flicker in, and curtains of aurora rise and ripple across a night sky above a dark ridge, all
in glyphs. Halfway through, the cells shrink until the aurora is almost a smooth picture, then grow back into
large characters. The light gathers and the glyphs settle into the title: "Recipes", "films, prompts and
source" and visions.joaoqueiros.com/recipes.

**Spec:** about 26 s, 16:9 1920×1080, 30 fps. Score composed in code: a slow analog-style synth pad in A minor
with a shimmering arpeggio that rises with the aurora, soft keyboard clicks as the command types, and a low
hum that swells when the cells shrink. Same MIT source routine on GitHub.

**Look:** near-black #07090C, aurora in green #5CF2A2 to teal #3FC8D8 with violet #9B7BFF at the tops, a faint
scanline and phosphor glow on the glyphs. Type: IBM Plex Mono (already on the site) for the terminal and the
glyphs, Fraunces for the title. Technique: Three.js WebGPURenderer with TSL. Aurora curtains are a few
ribbon meshes moved by noise, rendered to a texture; one post shader cuts the frame into cells, measures each
cell, and draws the matching glyph from a font atlas made on a canvas. Cell size is a uniform, which gives the
shrink beat for free. Different from R01 (particles from text) and R07 (leaves from an image): here text is the
screen.

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 4 s | Black terminal, cursor, `render aurora --ascii` types itself | DOM type-on, clicks in the score |
| 4 to 10 s | Glyphs flicker in; aurora curtains rise above a ridge | noise-driven ribbons, ASCII pass |
| 10 to 15 s | The curtains ripple and brighten, the arpeggio climbs | colour per cell, phosphor glow |
| 15 to 19 s | Cells shrink to near picture, then grow back | cell-size uniform |
| 19 to 26 s | Light gathers; glyphs settle into "Recipes" · "films, prompts and source" · visions.joaoqueiros.com/recipes | title mask sampled by the same pass |

## Open choices for João
- Subject: the Recipes library (recommended), or the Motion page.
- Palette: aurora green, teal and violet (recommended), or classic one-colour green phosphor.
- The shrink beat (cells to near picture and back): keep (recommended) or drop for a pure ASCII film.
- Subtitle: "films, prompts and source" (recommended), or the first line of the page intro.
