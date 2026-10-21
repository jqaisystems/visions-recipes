# R02 · Paper Terminal · concept card (approved 2026-10-21; skill shown: brand-voice-linter)

**Style (reusable):** Paper Terminal. A terminal window is a sheet of paper. Each command creases it, and the
folds turn flat text into a 3D object. Anyone can swap the commands, the folds and the final shape.

**Subject:** JQ AI Skills (`/systems/jq-ai-skills`, public repo `jqaisystems/jqai-ai-skills`, 47 skills, MIT).
Approved tagline: "Reusable Codex/Claude-style skill folders for repeatable AI workflows." Headline on the case
study: "Repeatable AI workflows, packaged as skills."

**Story in one line:** a long, messy chat prompt is retyped for the hundredth time. Then the terminal paper
folds itself, crease by crease, into a skill folder: trigger, steps, outputs, review. The folder files itself
next to 46 others, and the camera pulls back to a whole shelf of folded skills.

**Spec:** about 26 s, 16:9 1920×1080, 30 fps. Score composed in code (paper sounds: creases, slides, a soft
stamp). Same MIT source routine as R01.

**Look:** the ai site's dark palette (#111110, #F5F5F0, teal #00A89D), but the terminal is warm off-white paper
(#F3F1EC, the ai site's own "paper" token) with Geist Mono ink. Real skill names from the repo.

## Beats
| Time | Beat | Technique |
|---|---|---|
| 0 to 4 s | A paper terminal. The same long prompt types for the third time; a counter reads "typed 103 times". | type-on, paper grain shader |
| 4 to 9 s | `/skill brand-voice-linter`. The sheet creases along four folds (TRIGGER, STEPS, OUTPUTS, REVIEW), each fold labelled as it turns. | CSS 3D hinged panels, GSAP, real paper shading from fold angle |
| 9 to 14 s | The folded sheet becomes a skill folder with its SKILL.md tab and slides onto a shelf. | 3D flip, match cut on the folder tab |
| 14 to 20 s | Pull back: 47 folded folders, each with a real skill name (em-dash-remover, github-safe-publisher, case-study-writer...). A few unfold and refold as they are "called". | instanced 3D grid, camera pull-back |
| 20 to 26 s | Lockup: "Repeatable AI workflows, packaged as skills." · JQ AI Skills · github.com/jqaisystems/jqai-ai-skills | type on paper, logo |

## Why it fits
The product's own mechanic (one prompt becomes a reusable folder) becomes the transition grammar, the house style
of your best films. It looks nothing like R01: warm paper, tactile folds and quiet paper sounds instead of light,
particles and rain.

## Open choices for João
- Final line: the case study headline "Repeatable AI workflows, packaged as skills." (recommended), or your own.
- Which skill gets folded on screen: brand-voice-linter (recommended, it echoes R01), github-safe-publisher, or em-dash-remover.

## As built
The four folds use the four real steps of skills/brand-voice-linter/SKILL.md (Load the voice guide, Scan, Report,
Fix only when asked) instead of the placeholder labels above.
