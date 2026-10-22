# Visions Recipes

Films built entirely in code, shared as recipes: the prompt that started each one, a template to remix it,
how it's built, and the full source. Made by [João Queirós](https://www.joaoqueiros.com) with Claude Code,
[HyperFrames](https://github.com/heygen-com/hyperframes), Three.js, Canvas, SVG, GSAP and a score composed in code.

Watch the films and read the recipes at **[visions.joaoqueiros.com/recipes](https://visions.joaoqueiros.com/recipes/?utm_source=github&utm_medium=referral&utm_campaign=recipes)**.

| | Recipe | Made for | Stack | Get it |
|---|---|---|---|---|
| <img src="recipes/r04-one-hundred-marks/poster.jpg" width="240" alt="One Hundred Marks, One Line: the JQ mark above the word Marks"> | **R04 · [One Hundred Marks, One Line](recipes/r04-one-hundred-marks)**<br>One line that never lifts off the page closes into one shape after another, faster and faster, and settles on the last. Ships with demo shapes and the tracer for your own. | Marks · João Queirós | HTML, SVG, GSAP, Python (tracing and score) | [watch](https://visions.joaoqueiros.com/recipes/one-hundred-marks/?utm_source=github&utm_medium=referral&utm_campaign=recipes) · [zip](https://github.com/jqaisystems/visions-recipes/releases/tag/r04-one-hundred-marks-v1) |
| <img src="recipes/r03-signal-from-noise/poster.jpg" width="240" alt="Signal from Noise: iron-filing fragments gathered around six teal poles"> | **R03 · [Signal from Noise](recipes/r03-signal-from-noise)**<br>Thousands of fragments line up like iron filings, gather around the poles that matter, and the strongest few are pulled out into one reviewed list. | AI News Curator · JQ AI SYSTEMS | HTML, Canvas 2D, GSAP, Python (score) | [watch](https://visions.joaoqueiros.com/recipes/signal-from-noise/?utm_source=github&utm_medium=referral&utm_campaign=recipes) · [zip](https://github.com/jqaisystems/visions-recipes/releases/tag/r03-signal-from-noise-v1) |
| <img src="recipes/r02-paper-terminal/poster.jpg" width="240" alt="Paper Terminal: a sheet of paper folding along the four steps of a SKILL.md"> | **R02 · [Paper Terminal](recipes/r02-paper-terminal)**<br>A terminal drawn as paper prints a document, folds along its sections into a card, and files the card on a shelf of many. | JQ AI Skills · JQ AI SYSTEMS | HTML, CSS 3D, GSAP, Python (score) | [watch](https://visions.joaoqueiros.com/recipes/paper-terminal/?utm_source=github&utm_medium=referral&utm_campaign=recipes) · [zip](https://github.com/jqaisystems/visions-recipes/releases/tag/r02-paper-terminal-v1) |
| <img src="recipes/r01-token-rain/poster.jpg" width="240" alt="Token Rain: token particles pouring through a glowing ring labelled 01 DRAFT"> | **R01 · [Token Rain](recipes/r01-token-rain)**<br>Text dissolves into particles sampled from its own letters, rains through a sequence of gates and recompiles as new text. | Prompt Engineering · JQ AI SYSTEMS | Three.js WebGPURenderer, TSL, GSAP, Canvas 2D, Python (score) | [watch](https://visions.joaoqueiros.com/recipes/token-rain/?utm_source=github&utm_medium=referral&utm_campaign=recipes) · [zip](https://github.com/jqaisystems/visions-recipes/releases/tag/r01-token-rain-v1) |

## Use a recipe

Each folder in [`recipes/`](recipes) is a complete HyperFrames project. You need Node 22+ and Chrome or Edge.

    cd recipes/r01-token-rain
    npx --yes hyperframes@0.8.184 preview     # live preview in the browser
    npm run render                            # MP4 to renders/

Or skip the code: copy the prompt from the recipe's `RECIPE.md`, change the words, and give it to Claude Code
with the HyperFrames skills installed.

## Licence

Code, compositions and scores are MIT (see [LICENSE](LICENSE)). Fonts and libraries keep their own licences,
listed in each recipe's README. The JQ AI SYSTEMS logo and the names JQ AI SYSTEMS and João Queirós are not
licensed: replace them with your own before you publish a remix.

Want a film like these for your own product? See
[Product Films](https://www.ai.joaoqueiros.com/services/product-films?utm_source=github&utm_medium=referral&utm_campaign=recipes).
