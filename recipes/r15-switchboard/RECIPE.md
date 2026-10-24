# R15 · Switchboard

**Style:** workflow integration as a 1940s telephone switchboard rebuilt as a luxury object. Walnut, brass and cloth,
cables that hang and swing like real ones, light running down the wire, and a board that ends up woven into one web.
**Made for:** AI Workflow Integration (ai.joaoqueiros.com/services/workflow-integration).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom) · GSAP · Python (word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Workflow Integration service: a 1940s telephone switchboard
rebuilt as a luxury object, Three.js with bloom and reflections, warm key light, teal #00BFB4 accents.
Smoked walnut panel in a brass frame, four rows of six brass jacks with engraved labels: your tools on top (INBOX,
FORMS, CHAT, CALENDAR, SHEETS, ALERTS; MAIL, WEBHOOKS, SURVEYS, TICKETS, INVOICES, LEADS), your teams below (SALES,
SUPPORT, BILLING, OPS, CRM, ON CALL; FINANCE, PRODUCT, MARKETING, LEGAL, SUCCESS, ARCHIVE). A lamp above every jack, a
shelf of cloth patch cables with brass plugs, and a brass relay under a glass dome at the top: the AI decision layer.
Open on a macro of one amber lamp blinking above INBOX, with an old telephone ring, then pull out along the board.
Route: a cable lifts off the shelf, both plugs arc through the air and click INBOX into SUPPORT, light runs down the
wire, the lamp turns green and a card slides out: "Drafted reply attached". Enrich: patches land on the beat, FORMS
into CRM ("Record enriched"), CHAT into SALES ("Lead qualified"), CALENDAR into OPS ("Meeting booked"), MAIL into
BILLING ("Invoice filed"). Decide: the camera rises to the relay; an ALERTS lamp turns red, a red line runs from the
relay to ON CALL and the patch lands there: "Escalated to a person". Connect: six more patches in a rush until the
board is a woven web of swinging cables, then every lamp turns green in a wave. Pull back: the board steps into the
dark and a neon sign above it lights "connected" letter by letter, with a flicker. End on "AI Workflow Integration",
the service's line and the URL. Station titles wipe on bottom left; a HUD shows the board's state.
Technique: every patch is the same small timeline (blink, plug A flies, plug B flies, pulse, lamp, card) placed from
one table; each cable is a tube rebuilt every frame along a hanging curve between its two plugs, with a sag and a
swing that settles; the neon tubes follow the word's outlines from the film's own font.
Score: compose it in code from the same table: a 1940s band reimagined (walking bass, brushed swing hats, soft piano),
a brass click for every plug, a zip of light down the wire, a chime for each card, an alarm and a bell for the urgent
one, horn stabs in the rush, a rising run as the lamps turn green, a neon hum into one last chord.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: {system} as a 1940s telephone
switchboard rebuilt as a luxury object, Three.js with bloom and reflections, {accent} accents.
The jacks are {inputs} on top and {destinations} below, with a lamp above each and {layer} at the top.
Open on one lamp blinking above {first_input}. Then patch cables fly and click in: {patch_1}, {patch_2}, {patch_3},
each with light down the wire and a card saying {what_happened}. {human_moment}. Then every line goes busy until the
board is one woven web, the lamps turn green, and a neon sign lights "{word}".
End on {title}, {line} and {url}. One table drives the picture and a score composed in code.
```

Ideas: a help desk routing tickets to teams; a newsroom routing stories to desks; a studio routing briefs to
designers; a home routing sensors to rooms.

## How it's built

1. **One patch, many times.** Every patch is one row of a table (from, to, start, speed, card). A small function turns
   it into its own clock: the lamp blinks, plug A flies, plug B flies, a pulse runs, the lamp turns green, the card
   shows. The rush at the end is the same function with a faster speed, so it is data, not hand animation.
2. **Cables that hang right.** Each cable is a tube rebuilt every frame along a cubic curve between its two plugs.
   The handles drop by a sag that grows with the distance, and a damped swing after each landing makes it settle.
3. **Plugs that fly.** A plug's flight is a curve from the shelf to its jack through a point lifted toward the
   camera, while it turns from upright to pointing into the board, with a small settle when it lands.
4. **Light down the wire.** A few bright beads ride the same curve as the cable, from tool to team, and the bloom does
   the rest.
5. **The neon sign.** The word's outlines come from the film's own font; each contour becomes a glowing tube that
   flickers on in turn, from a seeded hash, so every frame renders on its own.

## Gotchas worth knowing

- Rebuild a cable's tube in place every frame (one buffer, new positions and normals); making a new TubeGeometry per
  frame is slow and leaks.
- Point a card at the camera, not at the board: a card flat on the panel turns into a sliver on the angled shots.
- Too many lamps at full glow blow out under bloom: keep their glow sprites faint and let the emissive do the work.
- Labels in a 3D scene still need contrast: put a dark band behind the HUD for the shots where the board is bright.
