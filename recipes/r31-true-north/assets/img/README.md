# The pictures

The film reads twenty images from this folder, `s00.jpg` to `s19.jpg`. They are not included: the stills in the
published film are João Queirós's own artwork from visions.joaoqueiros.com/stills and are not part of this repo's
licence.

Add twenty images of your own here before you preview or render, each at 3:2 (the film used 1024×683, and every image
is uploaded into one texture array, so they must all be the same size). Without them, the film does not start.

`s05.jpg` is the still the needle points at last and the camera dives into, and the zoom runs through `DROSTE` in
`bake/table.py`. Each image's title and prompt on screen are in `stills` in `bake/table.json`: change them there,
then run `python bake/table.py`.
