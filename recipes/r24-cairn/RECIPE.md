# R24 · Cairn

**Style:** cel-shaded anime, with painted background art. 3D rendered like a hand-drawn anime cut: flat colour in three
hard bands of light, ink outlines, screentone in the shadows, and the drawings changing 12 times a second while the
camera moves on every frame. Around it:
- a painted panorama of mountain rings at real depths;
- a cel sea of cloud;
- a sky painted in hard bands;
- time-lapse light with cast shadows;
- manga lettering.

**Made for:** Cairn (ai.joaoqueiros.com/cairn), the done-for-you SEO service of João Queirós.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL toon materials, outline pass, shadow maps) ·
Canvas 2D · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for Cairn, my SEO service, whose mark is six stones stacked into a C.
A cairn marks the way on a mountain trail; each checkpoint adds a stone. Cel-shaded anime with painted background
art: Three.js with a three-band toon ramp, ink outlines, screentone in the shadow band, cast shadows, the 3D on twos
while the camera moves on ones, impact frames and smear frames. Around the summit, four rings of painted mountains at
real depths with inked ridges, a cel sea of cloud in the valleys, and a sky painted in hard bands with the sun, the
moon, stars and inked clouds placed against the true horizon. Night, lichen green, chalk, stone and clay; Outfit,
Instrument Serif Italic and IBM Plex Mono.
Night: forty dashboard numbers hail onto the summit and shatter on the rock; a gust of hand-drawn wind blows them
away and three cards stay: 01 Indexed, 02 Buyer searches, 03 Enquiries.
The first stone: the camera tilts up into a cloud bank lit gold by the dawn, the first stone falls out of it and lands
on an impact frame with a cel dust cloud; a trail sign reads START, position 18, page 2, labelled as an illustration.
Every four weeks: a time-lapse, the sun racing over and the shadows sweeping across the stones; at week 4 a stone
lands and the sign climbs to 9, at week 8 to 3.
The checkpoint: at dusk, four hard cuts, each decision of a real checkpoint slammed in as manga lettering: GO,
NO-GO in clay red, VOID, CLOSED; then "A checkpoint that only ever says go is not measuring anything."
The summit: the last stones land on the beat until the C stands, the sun breaks through with rays, and the camera
cranes up over the sea of cloud. Title: the flat logo, "Search, checked every four weeks." and the URL. Never rotate
the mark or recolour a single stone; the logo at the end is flat.
Score: compose it in code from the same table, 84 bpm, A minor to C major: wind, a glassy tick for every number
that hits the rock, a breathy flute, a hit on every stone, a fast clock under the time-lapse, a dead stop before
every decision, C major on the summit.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: cel-shaded anime with painted
background art, Three.js with a three-band toon ramp, ink outlines, screentone, cast shadows, the 3D on twos and the
camera on ones, in {palette}. Set it in {a_painted_world} built as rings of painted layers at real depths, with a
banded sky placed against the true horizon. {the_noise} falls and blows away, leaving {what_matters}; {the_mark}
is built piece by piece as time-lapse light races over; {the_decisions} slam in as manga lettering; the last piece
lands, the light breaks through, and the flat lockup with {line} and {url}. One baked table drives the landings,
the impacts and a score composed in code.
```

Ideas: a bakery's year as loaves rising in a time-lapse kitchen; a running club's training block as flags planted up
a ridge; a studio's process as stones stacked on a riverbank; a product's releases as lanterns lit along a harbour.

## How it's built

1. **Six stones from one mark.** Each path of the logo SVG is extruded on its own and centred on itself, so every
   stone can fall, tumble and land exactly where the logo puts it. Sorted by height, they land bottom first.
2. **Toon light that tells time.** Every surface is a toon material with a three-band ramp and screentone in the
   shadow band. One function gives the sun's angle at any moment. It drives:
   - the light's direction and colour, and the shadow maps;
   - the sky's colours;
   - the tint of the painted mountains.
   During the time-lapse the bands and the shadows sweep across the stones.
3. **A painted panorama with real depth.** Four open cylinders around the summit carry painted ridges (lit faces,
   strata, snow, ink lines on the nearer two), so the layers slide past each other as the camera moves. A ring of
   inked cloud clusters lies in the valleys.
4. **A sky placed against the horizon.** The sky is a canvas fixed to the camera and repainted every frame. The sun,
   the moon, the stars and the clouds are projected from real directions, so they sit where the 3D world says they
   should, even when the camera tilts up into the cloud.
5. **On twos, with impacts.** The 3D reads `floor(t * 12) / 12`. A falling stone is stretched on its smear frames
   and squashed when it lands. Impact frames print the stage in ink and paper.
6. **The 2D layer.** The numbers, the wind, the dust, the week stamps and the lettering are drawn on a canvas over the
   WebGL canvas, at points projected from the 3D scene.
7. **The trail sign.** An unlit canvas on a toon board shows the search result. It redraws when the rank changes, so
   the text stays readable in every light.

## Gotchas worth knowing

- A sky drawn on a camera-fixed plane must size its clouds by the lens. Size them in pixels without the focal length
  and they come out eight times too big, covering the sun and the moon.
- Painted ridges must never touch the top of their texture: a ring whose ridge is cut flat shows its top edge as a
  line across the sky.
- Brand rules hold in motion: the camera moves around the stones, never the mark; no stone is recoloured; and the
  logo at the end is flat.
- Example rankings are labelled as an illustration on screen, as on the page, because they are not results.
