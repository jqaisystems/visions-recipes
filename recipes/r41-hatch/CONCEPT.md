# R41 · Hatch · concept

**Idea:** almost the whole film is one engraved field of lines, like a banknote or op art. Nothing is shaded: 3D forms and big words exist only because the lines swell or bend, and only the small labels and the logo are flat. Codex Control Center sees the shape of the activity and not the words, so the showpiece is "NOT THE WORDS" losing all its ink and staying readable only through the bent lines.

**Technique:** one WebGL2 fragment shader, stateless. Raymarched forms (sphere, bars and ring, gate, X) give tone and depth; tone sets line width, cross-hatching comes in on the darkest tones, lines follow the surface in world space. Type enters through one canvas: red swells the lines, blue only bends them, green is flat small type. Colour changes on a front of solid ink. Three sub-frames of motion blur, eight with a narrow shutter in the tunnel and the collapse.

**The film:** still lines; a sphere rises only by bending them, then takes ink on the first hit; a demo log whose private words lose their ink; SEES THE SHAPE; NOT THE WORDS melts; METADATA ONLY; bars and a ring, NO API KEY TO OBSERVE; a gate, APPROVE?, silence, the doors burst; a tunnel, READ-ONLY, BY DEFAULT; FULL ACCESS, an X slams, BLOCKED IN V1; CHECKED BEFORE IT'S PUBLIC, private words fall through a sieve as bends, SOURCE, DOCS and DEMO stay; every line collapses into one hairline; the logo.

**Sound:** a composed score in A minor (score/compose.py), hard four on the floor, rolling bass, an impact per word, a silence before the doors.

**Honesty:** facts only from the case study. Log text and bars are fictional and labelled DEMO DATA. "Codex" only in the system's name. No results. The logo is a flat image, never put through the lines.

