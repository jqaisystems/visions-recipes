# R07 · Gommage · concept card (approved by João 2026-10-22: Lantern Festival into Sea of Blooms, autumn leaves, name Gommage, nothing from the game)

**Style (reusable):** Gommage. An image doesn't cut or fade: it comes apart from one edge into thousands of
small leaves, each carrying the exact colour of the spot it left, and a wind carries them off with a soft glow.
Then they settle into the next image. Anyone can swap the images, the leaf shape and the wind.

**Why now:** "gommage" (French for erasing) is how many motion designers name this dissolve-into-petals effect,
after the 2025 game Clair Obscur: Expedition 33, where the word is used for it. We use only the word and the
general effect: no characters, no art, no names or music from the game, and no people dissolving.

**Subject:** the Stills collection on visions (Imagined Worlds), your own Midjourney images. Two of them:
"Lantern Festival" (warm reds and ambers, the most autumnal still) and "Sea of Blooms" (a ship among giant
flowers, with petals already in the air). No collection count on screen, as with the page intros.

**Story in one line:** Lantern Festival holds still for a breath, then a dissolve front crosses it from the left
and the picture breaks into leaves in its own colours. A wind lifts them into a slow spiral, they glow, and they
settle petal by petal into Sea of Blooms. Its petals keep drifting as the title appears: "Imagined Worlds" and
visions.joaoqueiros.com/stills.

**Spec:** about 26 s, 16:9 1920×1080, 30 fps. Score composed in code: an autumn piece, a warm felt-piano and
string-pad waltz in D minor turning to F, with a breathy wind that rises with the dissolve and a soft rustle of
leaves that follows the particle speed. Same MIT source routine on GitHub.

**Look:** the images themselves, full frame; the leaves are tiny shapes (a two-lobed leaf drawn in the shader),
lit by bloom so the dissolve edge burns gold. Type: Instrument Serif and Manrope. Technique: Three.js
WebGPURenderer with TSL, like R01, but the opposite idea: R01 builds particles from letters, R07 breaks a
photograph into instanced leaves that each sample the image, with a noise-driven dissolve front, curl-noise wind
and a bloom pass. Every position is computed from time and a per-leaf seed, so any frame renders on its own.

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 3 s | Lantern Festival, full frame, a slow push-in | image plane |
| 3 to 9 s | The dissolve front crosses from left to right: the image breaks into leaves in its colours, the edge glows gold | noise threshold + instanced leaves |
| 9 to 15 s | Wind: the leaves lift into a wide slow spiral across the frame, turning and catching the light | curl noise + spiral field, bloom |
| 15 to 21 s | They fall and settle, leaf by leaf, into Sea of Blooms, which resolves from the bottom up | per-leaf target in the second image |
| 21 to 26 s | Sea of Blooms holds with a few petals drifting; "Imagined Worlds" and visions.joaoqueiros.com/stills | type, one eased drift |

## Open choices for João
- The two stills: Lantern Festival into Sea of Blooms (recommended), or another pair from the 43.
- Particle shape: autumn leaves (recommended), or petals.
- Name: "Gommage" (recommended, it's the term people search for), or a plainer name such as "Leaf Fall".
