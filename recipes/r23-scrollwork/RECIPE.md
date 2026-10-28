# R23 · Scrollwork

**Style:** cel-shaded anime. 3D rendered like a hand-drawn anime cut: flat colour in three hard bands of light, ink
outlines, screentone dots printed into the shadows, a painted backdrop, the drawings changing 12 times a second while
the camera moves on every frame, smear frames, impact frames and speed lines.
**Made for:** Scrollwork (ai.joaoqueiros.com/scrollwork), the web design studio of João Queirós.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL toon materials and outline pass) · Canvas 2D ·
GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for Scrollwork, my web design studio, whose mark is an S drawn as a
double spiral wound on a rod (a scroll on its spindle, and a scroll bar with its thumb). Cel-shaded anime: Three.js
with a three-band toon ramp, ink outlines, screentone dots in the shadow band, a painted backdrop, the 3D animated on
twos (12 drawings a second) while the camera moves on ones, smear frames, impact frames and speed lines. Navy, vault,
brass, paper and ink, Fraunces and IBM Plex Mono.
The rod: ink black, a dry brush stroke paints down the frame, the rod falls along it and slams on an impact frame.
The mark: the spiral unfurls out of the rod and spins on it over a sunburst, smearing, into a pose.
The scroll: a long paper scroll unrolls through a painted night sky with my six featured sites on it, each stamped
with its plate numeral as it passes, then the camera pulls back to the whole scroll in the sky.
The thumb: the mark rides down a long rod as the scroll thumb, sparks where it grinds, and the site in a browser
frame beside it scrolls with it; every new site lands on an impact frame.
The cabinet: a manga page, seven more sites slamming in as panels on the half beat, each panning down its page.
Title: the mark spins on its rod and settles, then the flat lockup wipes on with "Websites you play by scrolling."
and the URL. Never rotate the logo: only the spiral turns, about its own rod, and the lockup is flat, no shading.
Score: compose it in code from the same table, 100 bpm, D minor to D major, like an anime opening: taiko and a crash
on every impact frame, a whoosh on every smear, plucked strings, a groove under the scroll, a metal sizzle under the
thumb, D major on the title.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: cel-shaded anime, Three.js with a
three-band toon ramp, ink outlines, screentone shadows, a painted backdrop, the 3D on twos and the camera on ones,
smear frames, impact frames and speed lines, in {palette}. {logo} slams in and transforms into {hero_pose};
it becomes {the_vehicle} that carries {the_work} through {a_painted_world}; then {the_payoff}, a manga page of
{more_work}, and the flat lockup with {line} and {url}. One baked table drives the impacts, the smears and a score
composed in code.
```

Ideas: a band's discography on a scroll through a festival sky; a bakery's menu unrolling as a recipe scroll; a
studio's case studies as manga panels; an app's features as a henshin of its icon.

## How it's built

1. **Toon materials.** Every surface is a `MeshToonNodeMaterial` with a three-texel gradient map (nearest filter), so
   light falls in three hard bands. A hard rim band is added as an emissive node from the view angle.
2. **Screentone.** Each material's `outputNode` compares the light it received with its own base colour; in the
   shadow band it prints halftone dots on a rotated screen grid. The sky never gets dots, only the drawn objects.
3. **Ink outlines.** `toonOutlinePass` draws every toon mesh a second time, back faces pushed out along the normals,
   in ink.
4. **On twos.** Everything that moves in 3D reads `floor(t * 12) / 12`; the camera and the 2D effects read the real
   time, so the drawings hold for two frames while the shot keeps moving.
5. **Smear and impact frames.** The table lists them. A smear frame stretches the mark along its spin and draws
   motion lines; an impact frame prints the whole stage in ink and paper for two or three frames, with a burst of ink
   lines and a camera shake after it.
6. **The scroll.** One long sheet is painted on a canvas (six plates, each with its numeral). Its vertices are moved
   every frame: the unrolled length hangs, the rest wraps a roller as a spiral.
7. **The painted layers.** The sky, the sunburst and the falling streaks are a canvas on a plane fixed to the camera;
   the brush, speed lines, sparks, stamps and the manga page are a 2D canvas over the WebGL canvas.

## Gotchas worth knowing

- A mesh whose vertices you move every frame keeps its first bounding sphere: once it moves out of it, it is culled
  and vanishes. Turn off frustum culling for it, or give it a sphere big enough for the whole move.
- A logo extruded from an SVG with its y axis flipped by a negative scale comes out inside out and renders black.
  Rotate it half a turn about x instead.
- Screentone by brightness alone covers the dark sky too. Use the light the surface received, relative to its own
  base colour.
- Keep brand rules in motion: here the logo is never rotated, only the spiral turns about its own rod, and the end
  lockup is the flat logo.
