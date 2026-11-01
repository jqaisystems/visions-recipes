# The clips

The motion section plays three muted clips inside the compass rings: `the-dive.mp4`, `iris.mp4` and
`painted-swell.mp4`. They are not included: they are João Queirós's own motion pieces from
visions.joaoqueiros.com/motion and are not part of this repo's licence.

Add three clips of your own with these names (or change the `src` of `#v0`, `#v1` and `#v2` in `index.html`). Each
plays for about four seconds from its start, cropped to a circle, so a square-safe centre works best. For smooth
seeking, encode them all-intra, for example `ffmpeg -i in.mp4 -an -vf scale=1280:-2 -c:v libx264 -g 1 -crf 18 out.mp4`.
