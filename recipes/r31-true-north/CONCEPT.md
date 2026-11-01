# R31 · True North · concept

Season 3, film 3 of 3, after Seamless (R29) and Ninefold (R30).

**Style (season 3, film 3 of 3): raymarched shader.** One WebGL2 shader in two passes: the scene into a half-float
target with a mip chain, then bloom, a chromatic kick on the beats, soft clip, grain and the logo's light. No meshes,
no Three.js. R29 was liquid chrome and R30 a glass field; this one carries real images: twenty of João's stills in one
texture array, on a globe, in a Droste zoom and in a tunnel. Type is HTML over the canvas. `paint(t)` sets the
uniforms from one baked table (`bake/table.py`), so every frame is a pure function of time.

**Made for:** Atlas Studio (ai.joaoqueiros.com/atlastudio), João's visual prompt studio. The logo is the approved
compass lockup from the live app (`atlas-studio-logo-approved*.png`), never the old leaf SVG.

**The idea:** the needle always points at the next image. Prompts live in Atlas; the pictures they lead to are the
ones on visions.

1. **Open (0 to 3.1 s).** A raymarched ring draws on from north, the blades scale in from the hub, the coral dot
   lights, and a prompt from the Atlas library types out verbatim (v6 Light Architecture · Backgrounds · Prompt 3).
   "Every image starts as a prompt."
2. **Globe (3.1 to 10.3 s).** The camera pulls back to a glass globe, 16 longitudes by 8 bands, tiled with stills and
   ruled with the logo's meridians and dashed parallels, the needle inside. Three whips and brakes on the beat; the
   needle points at Sea of Blooms, Neon Velocity and Voyage Through Time, each tagged `--stills · <title>`. "--" slams
   in and the camera dives into the last.
3. **Droste (10.3 to 18.6 s).** Eight stills, each inside the compass ring of the last (factor 4, 0.35 rad per level),
   a push every second beat, the needle's sweep revealing the next, each with its site title and prompt.
4. **Tunnel (18.6 to 23.8 s).** The last ring holds the tunnel, so the zoom arrives inside it with no cut: a cylinder
   of stills, eight around, time-smeared along the flight. "Prompts from Atlas Studio." "Images on --stills." with
   visions.joaoqueiros.com/stills typed under it.
5. **--motion (23.8 to 27.9 s).** The tunnel brakes; three rings open with The Dive, Iris and Painted Swell playing.
   "Some became --motion." with visions.joaoqueiros.com/motion typed under it.
6. **Title (27.9 to 33.1 s).** Light gathers into needle and ring where the logo lands, the paper opens from the hub,
   the approved lockup flat (its own paper feathered into the card, never recoloured), "Visual Prompt Studio",
   ai.joaoqueiros.com/atlastudio typed.

**Score:** composed in code (`score/compose.py`), 116 bpm, E minor to G major: bezel ratchets, a whip, sub and struck
glass per brake, a hit and climbing glass per zoom push over a groove, a rush through the tunnel, a glass per ring,
a G major chord and bell on the lockup, typing ticks for every typed line.

**Honesty:** the only claim about Atlas is "Prompts from Atlas Studio". The film never says Atlas made the images and
never names the image tool. No counts, users or results. The stills and clips are João's own and are not in the
public repo; each keeps its own title and prompt from the site.

**Cuts:** `videos/true-north/` (16:9) and `videos/true-north-vertical/` (9:16, a wider lens, the zoom and tunnel pulled
back, the rings stacked, the type re-set).
