# R34 · Footlights

**Style:** paper toy theatre, as paper cut-out stop motion. One Canvas 2D: every piece a path whose edge is torn by
noise, filled with a paper stock generated from noise, posed twelve times a second like stop motion on twos, stood up
in five flat layers at different depths with one camera dollying through them, and lit from behind like tissue on a
lamp, with HTML only for the HUD and the end card.

**Made for:** Phone Webcam Bridge, a system that turns an Android phone into the webcam on a Windows PC.
**Length:** 33.1 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Canvas 2D · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.1-second 1920x1080 film in HyperFrames for Phone Webcam Bridge, my system that turns an Android
phone into the webcam on a Windows PC, as paper cut-out stop motion staged as a backlit toy theatre. Reuse the paper
engine from Planner: one Canvas 2D, each piece a cut path with an edge torn by noise, filled with a paper stock
generated from noise, poses on twos with the edges re-cut on each pose. Stand it up: five flat layers at different
depths (back wall, set, apron, arch, curtains) and one camera that dollies through them, so near layers slide faster
than far ones. Screens, lamps and footlights are tissue lit from behind. A paper home office at night: plum wallpaper,
a window on a starry sky with a cloud and a sign-in card, a floor lamp, a desk and a monitor showing a video meeting
of invented paper puppets. Plum, night blue, theatre red, gold, amber and cream, with cyan for the phone's light.
Archivo, Instrument Serif italic and JetBrains Mono, each word of the lines on its own strip of paper.
Curtain up: the lamp flickers on and the red curtains part. "Your phone"
The phone: it rises through a trap on a rod; two flaps on its screen turn from 720p to 1080p and from back to front,
and the lens throws a cone of light. "is the camera."
Pairing: the bridge's panel slides onto the monitor; six PIN tiles flip on the phone, then the same six on the PC,
a bell when they match, and the phone's screen goes dark while the lens stays lit: "screen off · still streaming".
Link: a cursor presses Connect USB and a cable unrolls across the stage; Wi-Fi rings ripple behind it. "USB or Wi-Fi."
The feed: the picture runs from the lens to the PC as paper frames on a pulley; the preview shows the face and a
30 fps tag; the zoom and exposure sliders move and the camera switch flips. "You run the picture."
On stage: Start OBS Camera, the panel slides away, the "you" tile in the meeting lights up, and six footlights pop
up one by one. "Live in your meeting."
Stays local: a roller blind drops over the window and its cloud, and three tags land: 0 accounts, no server, no
telemetry. "Nothing leaves the room."
Title: the curtains close, a front-cloth drops, and the JQ AI SYSTEMS logo lands flat, never redrawn or recoloured,
with the system's name, "Your phone. Your webcam." and the URL. Score: compose it in code from the same table, 96 bpm,
electric piano, sub bass and brushes over vinyl hiss, with the curtain rings, flaps, tiles, cable, frames, controls
and footlights on the beat.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject} as paper cut-out stop motion
staged as a backlit toy theatre: five flat layers at different depths and one camera dollying through them, torn
edges, paper stocks made from noise, tissue lit from behind and poses on twos. The curtains part on {the_set};
{the_device} rises through a trap and its flaps set {the_settings}; {the_handshake}; {the_connection} crosses the
stage; {the_output} runs along a pulley while {the_controls} are set; {the_moment} lights up and the footlights pop
up one by one; a roller blind drops over {what_stays_out} with {the_tags}; and the curtains close for the logo,
placed flat with {line} and {url}. One baked table drives the beats, the pieces, the type and a score composed in code.
```

Ideas: a smart doorbell, with a camera rising on the door frame and the picture running on a pulley to a phone in the
kitchen; a home recording app, with a microphone through the trap and the track lighting up in the mix; a wireless
speaker, with notes running on the pulley as the record starts; a local photo backup, with photos running to a drive
under the desk and the blind down over the cloud.

## How it's built

1. **One canvas, one clock.** A GSAP tween drives the clock and calls `paint(t)`, which snaps `t` to twelve poses a
   second and draws the whole frame for that pose, back to front. Any frame can be seeked in any order.
2. **A theatre in layers.** The back wall, the set, the apron, the arch and the curtains sit at fixed depths (`D`).
   `layer(d)` sets a scale of `d / (d - z)` and an offset from the camera's position, so one dolly moves the curtains
   faster than the back wall. The camera's keys are written as a point on the set and its scale there.
3. **Cut paper.** `piece(P)` resamples a shape every few pixels and pushes each point along its normal by value
   noise, so every edge is torn; the outline is filled with one of 20 paper stocks generated once from a seeded random.
4. **Backlit paper.** A backlit piece fills with a radial glow inside its own cut shape, like tissue over a lamp;
   `cone()` and `glowAt()` add light on top, so the lens, the lamp, the monitor and the footlights throw light across
   the set.
5. **Up through a trap.** The phone rises on a rod with a little overshoot, and the apron in front of it hides the
   part still below the boards.
6. **PIN tiles that match.** Six tiles flip on the phone, then the same six on the PC a beat later; the match is a
   bell, and the phone's screen goes dark while the lens keeps its glow.
7. **Frames on a pulley.** The picture runs between two wheels as small paper frames pegged to a line, clipped to the
   space between the wheels; each frame shows the face the camera sees, and the preview follows the zoom, the
   exposure and the camera switch.
8. **Footlights and a blind.** Six cups pop up along the apron, each with a glow and a cone of warm light; the roller
   blind drops with a ratchet that slows as it goes, and three tags land on it.
9. **The logo, flat.** The curtains close, a front-cloth drops and the official file lands on it as an image,
   untouched, with the name, the line and the URL typed as text.

## Gotchas worth knowing

- Work out every layer's transform from its depth and the camera's, rather than moving layers by hand: the parallax
  stays consistent through every camera key.
- Put the near layers (arch and curtains) at a depth just in front of the set, or the dolly pushes them out of frame
  long before it reaches the screen.
- Hold the phone's screen dark but keep the lens lit: the point of the beat is that it still streams with the screen
  off.
- Key every per-pose cache by the pose, never by time, so the same frame always boils the same way.
- Re-lay the portrait cut rather than cropping it: the stage becomes a tall proscenium, the pulley stands upright, and
  the curtains open further so they never hide the phone.
