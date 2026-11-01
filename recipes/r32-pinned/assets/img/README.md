# The listing's media

The film reads a listing's media from this folder. It is not included: the photos, charts, video and cover in the
published film are João Queirós's own Etsy listing and are not part of this repo's licence.

Add your own before you preview or render:

- `photo0.jpg` to `photo3.jpg`: four product photos, at 2:3 (the film used 800×1200). They become the prints, the
  pins and the schedule.
- `size.jpg` and `colour.jpg`: the two images the filter leaves out, at 2:3.
- `cover.jpg`: the video's cover, at 2:3.
- `frames/f000.jpg` to `frames/f072.jpg`: the listing video as 12 fps frames at 9:16 (the film used 360×640), for
  example `ffmpeg -i video.mp4 -vf "fps=12,scale=360:640" -start_number 0 frames/f%03d.jpg`. Set `frames` in
  `MEDIA` in `bake/table.py` to the number of frames you made.

Any file that is missing draws as plain paper, so the film still runs. The listing's title, tags, boards and each
pin's title and alt text are in `bake/table.py`: change them there, then run `python bake/table.py`.
