# R14 · Orrery

**Style:** a system of specialists as a brass-and-glass orrery, filmed like a luxury watch commercial. Clockwork that
really turns, work that travels as light, and one satisfying payoff: every ring snapping into a single plane.
**Made for:** AI Agent Architecture (ai.joaoqueiros.com/services/agent-architecture).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom) · GSAP · Python (word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Agent Architecture service: a multi-agent system shown as a
brass-and-glass orrery in a dark starfield, Three.js with bloom and reflections, teal #00BFB4 light.
The orchestrator is the sun. Each agent is a glass planet lit from inside (research teal, writer amber, reviewer
violet) on its own gimballed brass ring, with a moon for its memory and small satellites for its skills. A brass
pillar and an engraved base.
Open in the dark with a clockwork tick: "brief: launch report for Q4" types, collapses into a comet that arcs across
the frame and strikes the sun. The orrery wakes ring by ring. Research: a thread of light to the first planet, then
sources fly in from the starfield and its moon flashes for each. Write: the sources stream to the writer, which spins
them into a ribbon of text. Review: pieces of the draft fly to the reviewer and a ring scans them; one flashes red and
goes back to the writer to be fixed; one rises on a gold beam to a card "Escalated to a person" where a cursor ticks
Approve. Conjunction: every ring blends into one plane, outer first, the planets line up with the sun and the result
fires at the camera as a beam with a flash. The beam breaks into beads that form the word "agents". End on
"AI Agent Architecture", the service's line and the URL. Station titles wipe on bottom left; a HUD shows each agent's
state.
Technique: every ring an Object3D nested in its parent, one angle each, all a function of time; the conjunction as a
quaternion slerp; work as seeded instanced particles on curves; one timing table.
Score: compose it in code from the same table: a clockwork escapement on the beat, a chime for each ring and handoff
in one harmonic series, a buzz for the rejected piece, one chord at the conjunction, a quiet pad under it all.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: {system} shown as a brass-and-glass orrery
in a dark starfield, Three.js with bloom and reflections, {accent} light.
The center is {center}. Each part is a glass planet on its own gimballed ring: {part_1}, {part_2}, {part_3}, each with
a moon for {memory} and satellites for {skills}.
Open on "{input}" becoming a comet that strikes the center. Then {step_1}, {step_2}, {step_3}, with work travelling
between planets as light, and {human_moment}.
Conjunction: every ring blends into one plane and the result fires out as a beam that becomes the word "{word}".
End on {title}, {line} and {url}. One timing table drives the picture and a score composed in code.
```

Ideas: a product's modules around its core; a team's roles around a project; the departments of a company around its
mission; the services of an app around its database.

## How it's built

1. **Clockwork as a hierarchy.** Each agent is a chain of nested groups: a gimbal (the ring's tilt), a spin (its orbit)
   and a body (the planet, its moon and satellites). One angle per group, all functions of time, so any frame renders
   on its own.
2. **Waking up.** Each ring scales in with a back ease while a swing rotation settles, so the brass looks like it swings
   into place.
3. **Work as light.** The comet, the thread, the sources, the stream and the beads are instanced spheres placed on
   curves every frame, seeded, additive and bloomed.
4. **The human moment.** The escalation card is HTML, placed every frame by projecting a 3D point to the screen, so it
   rides the camera; a cursor glides in and ticks Approve.
5. **The conjunction.** Each ring's rotation blends from its tilt to the shared plane with a quaternion slerp, outer
   ring first, while its orbit angle blends to the one that lines the planet up toward the camera.

## Gotchas worth knowing

- A beam that runs past the camera shows you the inside of a tube: stop it well short of the lens.
- When you blend an orbit angle into its aligned angle, unwrap it to the nearest turn first, or the planet spins
  several times on the way.
- Faded-out parts behind a word still catch light; fade the stand and dim the sun fully before the end card.
- A comet that starts off-screen with an ease-in is invisible for half its flight: start it in frame and arc it.
