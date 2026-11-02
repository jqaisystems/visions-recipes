# R36 · Tideline · concept

**Style (season 5, film 1 of 3): time as a material.** Slit-scan and time displacement on real footage, in one WebGL2
fragment shader.

The 35 films before this one are all drawn worlds. Season 5 takes real footage and treats **time** as the thing you
shape:
- **How it works.** The frames of a real clip are loaded as one texture array, and each pixel samples its own moment
  in time, steered by a displacement map: a gradient, a radial sweep, a word mask, or the beat. That one move gives the
  season its vocabulary:
  - **slit-scan:** a moving slit writes time across the frame, the 2001 stargate effect;
  - **time smear:** a wave stretches into a ribbon;
  - **echo trails;**
  - **a datamosh-style hold and bloom;**
  - **type cut out of time:** the letters show a different second from the frame around them.
- **Determinism.** The frames are pre-extracted with ffmpeg to a fixed count (about 240 frames at 1080p per clip,
  packed into atlases), and `paint(t)` reads one baked table, the pattern R32 to R35 use.
- **The stack is new to the library:** WebGL2 with `sampler2DArray`, a frame-history ring, and displacement maps
  baked in Python.

**Made for:** the Tidesstunes Social Pipeline (ai.joaoqueiros.com/systems/tidesstunes-social-pipeline), João's internal
system for the Tidesstunes music project, relaxing piano and ocean music. The case study's own line is "One video
in, three platforms out."

**Footage:** a real Tidesstunes video and its track, João's own (AI-generated imagery for the channel), read by
`bake/prep.py` and never committed. In this repo, `bake/demo.py` makes a stand-in clip.

**The idea:** a tideline is the mark the sea leaves on the sand, the moment it reached written as a line. The film is
a strip of time, which is what slit-scan is. One long video washes in, the pipeline finds its strongest minute, and
that minute is cut, stood up vertical and carried out to three places, the sea writing time across every frame.

1. **One video in (0 to 4 s).** One whole Tidesstunes video is laid out as a single slit-scan strip, each column one
   moment of the four minutes, a band of ocean colour running from dawn blue to sunset orange. A playhead runs along
   it, and where it passes, the strip opens into the moving picture: a piano in the surf. "One video in,"
2. **The strongest minute (4 to 9 s).** The track's real audio energy, computed in the bake from the actual
   soundtrack, rises off the strip as a tide-height line. A 60-second window slides along it and locks onto the
   peak, not the first minute. Inside the window the frames unfold from the strip in a slit-scan sweep. "the strongest
   minute,"
3. **Cut to vertical (9 to 14 s).** The picture splits into vertical slits. The slits outside the centre crop drift
   back in time and fall away as echo trails, and the 9:16 frame stands up out of the wave, sharp. "cut to
   vertical,"
4. **Hosted once (14 to 18 s).** The clip freezes in a datamosh hold (the last frame's motion vectors keep pushing the
   sunset across the keys) and blooms into one bright line: a single link. No CDN name. "one link,"
5. **Three platforms, three captions (18 to 26 s).** The vertical clip splits into three phone frames, each showing
   the same footage at a different time offset (a radial time displacement, so the three are visibly one wave seen at
   three moments). Each gets its own caption, typed on, from the case study's own descriptions:
   - short with hashtags;
   - an engagement hook in the case study's voice ("Close your eyes and drift...");
   - a keyword-rich description pinned to the board "Ocean Piano Meditation Music".

   The platforms are never named or shown as logos; the frames carry the three caption styles. "three captions,"
6. **Queued (26 to 30 s).** The three posts drop into a queue, spaced out in time (the case study's rate limiting).
   On the downbeat the camera dives through a slit-scan tunnel made of the sea itself. "spaced out, queued."
7. **Title (30 to 33.5 s).** The type is cut out of time: **Tidesstunes Social Pipeline** in letters that each show a
   different second of the waves, over a frame held still. "One video in, three platforms out." The JQ AI SYSTEMS logo
   lands flat, never redrawn or recoloured (or the Tidesstunes mark, if João prefers and supplies it), with
   ai.joaoqueiros.com/systems/tidesstunes-social-pipeline.

**Look:** the footage carries the colour, so the graphics are minimal:
- one off-white line weight for the playhead, energy line and link;
- teal (#00A89D) from the ai site for the 60-second window;
- type in Inter and Libre Baskerville, the case study's own pair;
- a deep sea-ink ground (#0A1418) behind the strip and the phones.

**Sound:** the soundtrack is **the strongest minute of a real Tidesstunes track**, chosen by the same energy analysis
the film shows. That's what the case study's own film did. On top of it, a few sound marks made in code:
- a soft swell on each slit sweep;
- a tick on the window lock;
- a tape-stop on the datamosh hold;
- three bell notes for the three phones;
- a low wash under the tunnel.

If the music can't go in the film, the fallback is a score composed in code (piano and sea, about 72 bpm).

**Honesty and brand:**
- **Facts used on screen**, all from the case study:
  - one video in, three platforms out;
  - the best 60-second segment chosen by audio energy, not the first minute;
  - re-encoded to 9:16 with a centre crop;
  - one hosted link reused for all three posts;
  - platform-specific captions (short with hashtags, an engagement hook, keyword-rich for search on the "Ocean Piano
    Meditation Music" board);
  - posts spaced out by rate limiting.
- **Kept off screen:** "39+ videos", "~2 min per video", "30+ minutes", any post counts or results.
- **Third-party names:** no YouTube, TikTok, Instagram, Pinterest, Cloudinary, Buffer, yt-dlp or FFmpeg names or logos
  on screen. The film says "three platforms" and "one link".
- **Licence:** the pipeline code is private, so the recipe licenses only the film's code. The public repo ships no
  Tidesstunes footage or music: the README says "drop in your own clip" (as R31 and R32 did), with a short procedural
  demo clip so it runs out of the box.

**Cuts:** 16:9 and a 9:16 vertical, re-laid out, not cropped. The vertical cut is native here, because the pipeline
makes vertical clips: in portrait the strip runs top to bottom and the three phones stack as overlapping cards.
About 33 s.

**Stack:** HyperFrames 0.8.184 · WebGL2 (one fragment shader, texture arrays) · GSAP for the type · Python (frame
extraction, audio energy, displacement maps, table, sound marks).


**As built (draft 1, approved at gate 2 on 2026-11-02):**
- **The source is the original, not the pipeline's output.** The film uses the landscape master "Oceansong - Piano
  Waves for Inner Peace" (the no-logos version, 1608×1080, 4:00) and its MP3, from João's
  Tidesstunes library. It's the same
  video the pipeline turned into `clip_full_xkictSVrg9k.mp4`, so the film shows the real input and output.
  `bake/prep.py` only reads it.
- **The strongest minute is real:** 1:52 to 2:52, by RMS energy over every 60-second window.
  - The strip is a real slit-scan of the whole four minutes. The source loops, so it reads as a woven chevron.
  - The slab is 144 frames at 12 fps from 1:52, and the soundtrack is the track's own audio from the same moment.
- **The three captions are the pipeline's own,** from `build_caption()` in `tidesstunes_pipeline.py` for Oceansong,
  with the platform names and the YouTube line left out. The link chip shows the clip's real public ID,
  `tidesstunes/clip_xkictSVrg9k`, with no CDN name.
- **The datamosh** is a smooth flow field over 16 px blocks that stop refreshing; it spreads from the bottom up.
- **The 9:16 cut** (`videos/tideline-vertical`) is re-laid for portrait, not cropped:
  - the strip of time runs down the frame, with the energy line down the right and the clock down the left;
  - the landscape original shrinks to the frame's width before its crop falls away, and then the 9:16 picture grows
    to fill the frame;
  - the three phones sit side by side at 0.8 scale, and the title is set to the portrait width.
  - A second texture array holds the 9:16 centre of the source at full resolution (608×1080, `c%03d.jpg`), so the
    full-frame portrait picture stays sharp.
  - The portrait datamosh uses 12 px blocks and reaches less of the frame.
