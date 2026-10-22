# R06 · Brand Readiness Scan · concept card (approved by João 2026-10-22: Brand Readiness Check, his own business card, checks list + band scale with no score claimed, headline + address ending)

**Style (reusable):** Depth scan. An object is read by a scanner line that sweeps across it; behind the line the
object turns into a relief of glowing scanlines (a depth map drawn as stacked contour lines), and each feature
lights up as the line finds it. A gauge fills as the checks pass. Anyone can swap the object and the checks.

**Subject:** the free Brand Readiness Check (joaoqueiros.com/brand-readiness-check.html, published 2026-10-16).
Its own facts: 8 questions, about 60 seconds, a score out of 100, four bands (0 to 39 Starting point, 40 to 69
Growing pains, 70 to 89 Strong foundations, 90 to 100 Ready to scale), the three things to fix first, no email
needed for the score, answers stay in your browser. Its headline: "Is your brand ready to grow?"

**The eight signals on screen** (the page's own words, shortened): clarity in five seconds · a logo that works at
16 px, in one colour, on a van · the same colours and fonts everywhere · guidelines a printer could follow ·
the original vector files · as credible as your best competitor · fit with the business you are today ·
proud to hand over your card.

**Story in one line:** a business card lies in the dark. A teal scanner line sweeps it and the card becomes a
glowing relief. The line pauses on eight features in turn (the headline, the logo shrinking to 16 px, the
colours, a guide page, the vector anchor points, a competitor card beside it, a "since launch" date, a hand
holding the card out), each one ticking a gauge on the side. The gauge passes through the four bands, and the
film ends on the check's headline and its address.

**The card:** your own (JQ mark, João Queirós, brand identity designer, joaoqueiros.com). No invented client.

**Spec:** about 26 s, 16:9 1920×1080, 30 fps. Score composed in code: a low scanner drone with a soft sweep, a
clean blip for each check, the drone rising a step per band, and a resolved chord on the headline. Same MIT
source routine on GitHub.

**Look:** near-black (#111110), the scan in teal #00A89D with bone #F5F5F0 highlights, the relief in thin grey
contour lines. Manrope for labels, Instrument Serif for the headline. Technique: Canvas 2D. The card is drawn
once into an offscreen height map (raised logo, raised type, edges); every frame redraws it as 200 horizontal
scanlines displaced by height, revealed behind the sweep. Not particles (R01), paper (R02), filings (R03), one
line (R04) or a shader (R05).

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 3 s | Dark. A teal line wakes at the left edge; the card appears as a flat outline | sweep, outline |
| 3 to 7 s | The line sweeps across: the card rises into a relief of scanlines; the gauge appears, 0 / 8 | height map to ridge lines |
| 7 to 19 s | Eight checks, 1.5 s each: the scanner stops on a feature, it lights up, a one-line label, the gauge ticks | per-feature highlight masks |
| 19 to 22 s | The gauge fills through the four bands and their names | gauge, band labels |
| 22 to 26 s | Lockup: "Is your brand ready to grow?" · 8 questions · about 60 seconds · joaoqueiros.com/brand-readiness-check | type, one eased drift |

## Open choices for João
- Subject: the Brand Readiness Check (recommended).
- The card: your own business card (recommended).
- The gauge: run through all four bands as the scale, without claiming a score for your brand (recommended), or
  land on a score.
- Ending: the check's headline and address (recommended), plus "No email needed for your score" if you want the
  privacy point on screen.
