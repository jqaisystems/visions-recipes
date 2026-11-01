# R34 · Footlights · concept (as built)

**Style (season 4, film 3 of 4): paper cut-out stop motion, backlit.** It uses the same engine as R32 Pinned and R33
Planner: torn-edge cut paper with stocks generated from noise, poses on twos with edge boil, one Canvas 2D, `paint(t)`
drawing every frame from one baked table.

Pinned and Planner were paper lying flat on a table under a top light, seen from above. Footlights stands the paper
up, so it can't read as either of them:
- **A paper toy theatre, seen from the front.** There's a proscenium arch, painted flats that slide in on grooves, a
  footlight row, and a tunnel book of five or six layers in depth. The camera dollies *into* the layers, a new kind of
  move for the season.
- **Backlight instead of a table light.** It's a night scene. Light comes through the paper: translucent stocks glow
  where a lamp sits behind them, cut-outs throw light shafts and silhouettes onto the back wall, and the colours
  change on the beat. The first two films lit only the front of the paper.
- **New mechanics:** sliding flats on grooves, pull-strings, a paper zoetrope, a string of frames on a pulley loop, a
  roller blind, and pop-out footlights.
- **A new palette:** deep plum and midnight blue, lamp amber, cyan screen light, cream and a red curtain. There's no
  felt, birch or cutting mat.

**Made for:** Phone Webcam Bridge (ai.joaoqueiros.com/systems/phone-webcam-bridge), João's local Android-to-Windows
camera system for video meetings. It's released (v1.0.0), and the source is public on GitHub. Its line is "Your phone.
Your webcam." The only film it has, /code 011, uses a HeyGen AI voice, so this is its first film that can be a recipe.

**The idea:** a video call as a night show on a paper stage. The camera in your pocket becomes the lens for the
evening. Every frame of the picture travels from the phone to the PC on a string of paper frames and lands on stage
in the meeting. Nothing leaves the theatre.

1. **Curtain up (0 to 4 s).** The red paper curtains part on a dim stage: a home office at night, cut in layers, with
   a laptop on a desk and a meeting window drawn on a flat. An empty tile waits. "Your phone."
2. **The phone (4 to 9 s).** A paper phone rises on a stand from a trap in the stage floor. Its screen is a lit
   flat. Two flaps flip: **720p / 1080p**, then **front / back**. The phone's screen dims to black, but light keeps
   pouring from its lens: it keeps streaming with the screen off. "is the camera."
3. **Pairing (9 to 13 s).** A row of six paper number tiles flips over on the phone, a 6-digit PIN (sample digits),
   and the same six flip on the PC's flat to match. A cable unrolls from the phone across the stage floor marked
   **USB**. Behind it, on a separate pull-string, three paper rings ripple out marked **Wi-Fi**. "USB or Wi-Fi."
4. **The feed (13 to 20 s).** This is the centrepiece. The picture is carried as a string of small paper frames on a
   pulley loop, each one a lit card with the face drawn on it. They run from the phone's lens across the stage to the
   PC, like a zoetrope pulled straight. A paper **30 fps** counter flips over on the beat. Then the PC's control
   panel slides in as a flat, with paper sliders labelled **zoom** and **exposure**, a **profile** dial, and a
   **switch camera** toggle. Each one moves, and the frames on the string change with it: brighter, closer, the other
   camera's view. "You run the picture."
5. **On stage (20 to 25 s).** A paper button marked **Start OBS Camera** presses in, and the frames feed into the
   meeting flat. The empty tile lights up with the paper face, and the footlights pop up along the front of the stage.
   "Live in your meeting."
6. **Stays local (25 to 29 s).** A paper cloud hangs at the back with a login card on it. A roller blind comes down
   over the window, and the cloud goes dark. Three small tags flip: **0 accounts**, **no server**, **no telemetry**.
   "Nothing leaves the room."
7. **Title (29 to 33 s).** The curtains close. A black front-cloth drops, and the JQ AI SYSTEMS logo lands flat,
   never redrawn or recoloured. Then come "Phone Webcam Bridge", "Your phone. Your webcam." and
   ai.joaoqueiros.com/systems/phone-webcam-bridge.

**The face on the frames:** an invented paper puppet, a simple cut-out head and shoulders in a sweater. It's not a
real person, and it's not João.

**Score:** composed in code, about 96 bpm and night-time. It has warm electric piano chords, a round sub bass, brushes
and a soft vinyl hiss. Each move on stage has its own sound on the beat:
- the curtain rings sliding;
- flats running in their grooves;
- the PIN tiles flipping;
- the cable unrolling;
- a fast flutter for the frames on the pulley, ticking at the fps counter;
- slider clicks;
- the button's press;
- the footlights coming on with a hum and a chord;
- the blind's rattle.

The logo lands on a major chord with a bell.

**Honesty and brand:**
- **Facts used on screen**, all from the case study and the public README:
  - Android to Windows;
  - 720p or 1080p, front or back camera;
  - it keeps streaming with the screen off;
  - a 6-digit pairing PIN;
  - USB or Wi-Fi;
  - preview, switch camera, zoom, exposure, profile and frame rate in the bridge;
  - Start OBS Camera, then choose the virtual camera in your meeting app;
  - 0 accounts, no hosted server, no telemetry;
  - 30 fps.
- **Kept off screen:** latency, setup times and "high-quality" comparisons with laptop webcams. The phone microphone
  (VB-CABLE) is left out, to keep the film on the picture.
- The PIN digits are a sample. The control labels are the bridge's own (`Connect USB`, `Start OBS Camera`, zoom,
  exposure, profile).
- **Third-party names:** no Android, Windows, OBS, Zoom, Meet or Teams logos or brand colours. The meeting app stays
  unnamed: a generic paper meeting window. "Android", "Windows" and the button label "Start OBS Camera" appear as type
  only, the way Planner set platform names.
- The JQ AI SYSTEMS logo is the official file, placed flat.
- **Licence:** the system's repo has no open-source licence, so the recipe licenses only the film's code. The bridge
  itself stays João's.

**Cuts:** 16:9, plus a 9:16 vertical re-laid out for portrait, not cropped. In portrait the stage becomes a tall
proscenium: the phone sits low, the meeting window sits high, and the string of frames runs up between them.
About 33 s.

**Stack:** HyperFrames 0.8.184 · Canvas 2D · GSAP · Python (table, score). The film forks the R33 engine (`piece()`,
the stocks, the boil, `camAt`) and adds a backlight pass and depth layers.
