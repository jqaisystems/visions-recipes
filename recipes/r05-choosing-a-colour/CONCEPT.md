# R05 · Choosing a Colour · concept card (approved by João 2026-10-22: brand colours article, adjectives "clear, warm, precise", article-page palette as 4 swatches per the article's 1 primary · 1 secondary · 2 neutrals, lockup joaoqueiros.com)

**Style (reusable):** Marbled ink. Every colour at once swirls like ink on water, then a method takes over:
the flow slows, the colours that don't fit drain away, and what is left pools and separates into a few clean,
labelled swatches. Anyone can swap the colours, the steps and the final palette.

**Subject:** the blog post "How to Choose Brand Colours That Actually Work for Your Business" (joaoqueiros.com,
20 January 2026). Its own words drive the film: the problem ("I like blue"), the five steps (define your
personality in 3 to 5 adjectives, study 10 to 15 competitors, choose a primary, build supporting colours, test
across applications), the palette structure (1 primary, 1 to 2 secondary, 1 to 2 neutrals) and the mistake it
warns about last ("Blue" isn't specific enough: define every colour with exact codes).

**Story in one line:** a swirl of every colour, and the line "Most brands start with “I like blue.”" Then the
method: three adjectives filter the swirl, a competitor scan shows everyone crowding blue, one primary pools out
of the ink, supporting colours and neutrals separate beside it with exact HEX codes, and the palette is tested on
a card, a web page, a social post, dark and light. Close on the article's title.

**The palette it lands on:** the colours of the article page itself, João's own: teal #00A89D, ink #1A1A18,
bone #F5F5F0, blue #0099D6, grey #767672. No invented client, no invented brand.

**Spec:** about 26 s, 16:9 1920×1080, 30 fps. Score composed in code: a watery, slowly modulated pad and soft
drops while the ink swirls; it thins to a few clear tones as colours drain; one chime per swatch as it locks;
a resolved chord on the title. Same MIT source routine on GitHub.

**Look:** the ink is the picture, full frame, rich and saturated at the start. Type in the article's style:
Manrope for labels and codes, Instrument Serif for the lines. Technique: WebGL2, one fragment shader. The marbling
is computed from time alone (each pixel traces itself back through a moving flow field), so any frame can be
rendered on its own with no simulation state. Nothing like R01 to R04 (particles, paper, Canvas, one line).

**Safety:** no statistics on screen (the article's "90%" and "1,200+ projects" stay out of the film). Every word
on screen is quoted or paraphrased from the article.

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 4 s | Every colour at once, marbling. Line types: "Most brands start with “I like blue.”" | time-only flow-map shader |
| 4 to 8 s | 01 Personality: three adjectives type in; colours that don't fit them drain to grey | per-hue saturation mask |
| 8 to 12 s | 02 Competitors: 12 small dots settle around the frame, most of them blue; "Most cluster around one colour." The gap is marked | dots + hue ring |
| 12 to 16 s | 03 Primary: the remaining ink pools into one teal body; #00A89D types beside it | attractor in the flow field |
| 16 to 20 s | 04 Supporting: the pool separates into five swatches: primary, secondary, two neutrals, with HEX codes | flow splits into bands |
| 20 to 23 s | 05 Test: the palette drops onto five small layouts: a card, a web page, a social post, dark, light | swatches into mockups |
| 23 to 26 s | Lockup: "How to choose brand colours that actually work." · joaoqueiros.com | type, one eased drift |

## Open choices for João
- Subject: the brand colours article (recommended).
- The three adjectives on screen (step 1). They should be true of your brand; my suggestion is "clear, warm,
  precise", but please give me your own.
- Final palette: the article page's own colours (recommended), or your personal brand palette if it differs.
- Lockup URL: "joaoqueiros.com" with the article title above it (recommended, the full URL is long), or the full
  address of the post.
