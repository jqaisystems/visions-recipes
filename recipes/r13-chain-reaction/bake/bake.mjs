// Runs the Chain Reaction machine once with a fixed timestep and writes every moving body's position per film
// frame to ../assets/bake.js, plus every impact to events.json for the score. The film only reads the table, so
// any frame renders the same on its own. Usage: node bake.mjs
import Matter from "matter-js";
import { writeFileSync } from "node:fs";

const { Engine, Bodies, Body, Composite, Constraint, Events } = Matter;

const FPS = 30, SUB = 4, DT = 1000 / (FPS * SUB);   // 120 physics steps a second, 30 recorded
const T0 = 2.4;                                    // the ball drops at 2.4 s of the film
const T_END = 19.0;                                // stop recording here

const engine = Engine.create({ positionIterations: 10, velocityIterations: 8 });
engine.gravity.y = 4;
const world = engine.world;

// ---------- static parts (also exported, so the film draws exactly what the physics used) ----------
const statics = [];
const wall = (x1, y1, x2, y2, th = 16, tag = "track") => {
  const len = Math.hypot(x2 - x1, y2 - y1), ang = Math.atan2(y2 - y1, x2 - x1);
  const b = Bodies.rectangle((x1 + x2) / 2, (y1 + y2) / 2, len, th, { isStatic: true, angle: ang, friction: tag === "floor" ? 0.9 : 0.05, frictionStatic: tag === "floor" ? 1 : 0, label: tag });
  Composite.add(world, b);
  statics.push({ tag, x1, y1, x2, y2, th });
  return b;
};
const pegs = [];
const peg = (x, y, r = 9) => { Composite.add(world, Bodies.circle(x, y, r, { isStatic: true, restitution: 0.4, label: "peg" })); pegs.push([x, y, r]); };

// 0 · trigger: a short chute under the terminal
wall(240, 330, 520, 420);
// 1 · collect: ramp into the inbox tray (a seesaw)
wall(520, 420, 1150, 600);
const PIV = { x: 1360, y: 640 };
// a symmetric seesaw: it rests left-down on the stop, the ball rolls up it, passes the pivot and tips it
const tray = Bodies.rectangle(PIV.x, PIV.y, 330, 14, { friction: 0.05, density: 0.004, label: "tray" });
Body.setAngle(tray, -0.12);
Composite.add(world, [tray, Constraint.create({ pointA: { ...PIV }, bodyB: tray, pointB: { x: 0, y: 0 }, stiffness: 1, length: 0 })]);
wall(1200, 668, 1200, 720, 14, "stop");            // the left end rests on this until the ball passes the pivot
wall(1478, 718, 1548, 718, 14, "stop");            // the right end comes to rest here, about 20 degrees down
// 2 · clean: ramp, a raised rail, then the dominoes on a lower floor
wall(1520, 770, 2300, 880);
wall(2300, 880, 2436, 880);
wall(2400, 960, 2960, 960, 16, "floor");
wall(2408, 888, 2408, 960, 14, "stop");             // closes the gap under the rail
const dominoes = [];
const ND = 8;
for (let i = 0; i < ND; i++) {
  const d = Bodies.rectangle(2450 + i * 64, 960 - 8 - 60, 20, 120, { friction: 0.4, frictionStatic: 0.9, density: 0.001, label: "domino" });
  dominoes.push(d); Composite.add(world, d);
}
// the relay ball waits at the far end of the floor
const ball2 = Bodies.circle(2930, 960 - 8 - 18, 18, { restitution: 0.25, friction: 0.02, frictionStatic: 0, frictionAir: 0.0005, density: 0.004, label: "ball2" });
Composite.add(world, ball2);
// 3 · sort: a peg field and a funnel
for (let r = 0; r < 6; r++) for (let c = 0; c < 6; c++) peg(2840 + c * 76 + (r % 2 ? 38 : 0), 1080 + r * 70);
wall(2780, 1000, 2780, 1525, 14, "board");          // the peg board's sides
wall(3320, 1000, 3320, 1525, 14, "board");
wall(2780, 1520, 3030, 1600, 14, "funnel");
wall(3320, 1520, 3090, 1600, 14, "funnel");
// 4 · review: the ramp down to the gate
wall(2950, 1680, 3500, 1760);
wall(3500, 1760, 4120, 1910);
const GATE_X = 3580, GATE_Y = 1760 + (GATE_X - 3500) * (150 / 620) - 60;
const gate = Bodies.rectangle(GATE_X, GATE_Y, 18, 110, { isStatic: true, label: "gate" });
Composite.add(world, gate);
// 5 · send: the bell, then the out tray
wall(4120, 1910, 4550, 1950);
wall(4550, 1950, 4800, 1950, 16, "floor");
wall(4800, 1950, 4800, 1880, 14, "stop");
const BELL_P = { x: 4330, y: 1660 };
const bell = Bodies.circle(BELL_P.x, BELL_P.y + 190, 46, { density: 0.0006, frictionAir: 0.004, label: "bell" });
Composite.add(world, [bell, Constraint.create({ pointA: { ...BELL_P }, bodyB: bell, stiffness: 1, length: 190 })]);

// ---------- the ball ----------
const ball = Bodies.circle(300, 290, 18, { restitution: 0.25, friction: 0.02, frictionStatic: 0, frictionAir: 0.0005, density: 0.01, label: "ball" });
Body.setStatic(ball, true);
Composite.add(world, ball);

// ---------- impacts, for the score ----------
const events = [];
let step = 0;
const now = () => step * DT / 1000;
Events.on(engine, "collisionStart", (e) => {
  for (const p of e.pairs) {
    const a = p.bodyA.parent.label, b = p.bodyB.parent.label;
    const v = Math.hypot(p.bodyA.velocity.x - p.bodyB.velocity.x, p.bodyA.velocity.y - p.bodyB.velocity.y);
    if (v > 0.6) events.push({ t: +now().toFixed(3), a, b, v: +v.toFixed(2) });
  }
});

// ---------- run ----------
const MOVING = { ball, tray, ball2, gate, bell, ...Object.fromEntries(dominoes.map((d, i) => [`d${i}`, d])) };
const rec = Object.fromEntries(Object.keys(MOVING).map((k) => [k, []]));
let gateOpenAt = null, restSince = null;
const GATE_WAIT = 1.1, GATE_LIFT = 0.45;
const total = Math.round(T_END * FPS * SUB);
for (step = 0; step <= total; step++) {
  const t = now();
  if (t >= T0 && ball.isStatic) Body.setStatic(ball, false);
  // the gate opens a beat after the relay ball has come to rest against it (a human tick, then the lift)
  if (gateOpenAt === null) {
    const near = Math.abs(ball2.position.x - (GATE_X - 27)) < 12 && Math.hypot(ball2.velocity.x, ball2.velocity.y) < 0.25;
    if (near) { if (restSince === null) restSince = t; if (t - restSince > 0.25) gateOpenAt = t + GATE_WAIT; } else restSince = null;
  } else if (t >= gateOpenAt) {
    const u = Math.min(1, (t - gateOpenAt) / GATE_LIFT), e = u * u * (3 - 2 * u);
    Body.setPosition(gate, { x: GATE_X, y: GATE_Y - 150 * e });
  }
  if (step % SUB === 0) for (const [k, b] of Object.entries(MOVING)) rec[k].push([+b.position.x.toFixed(1), +b.position.y.toFixed(1), +b.angle.toFixed(3)]);
  Engine.update(engine, DT);
}

// when each station happens, read from the run itself, so labels and sound land on the physics
const first = (f) => { const e = events.find(f); return e ? e.t : null; };
const has = (e, x, y) => (e.a === x && e.b === y) || (e.a === y && e.b === x);
const marks = {
  drop: T0,
  tray: first((e) => has(e, "ball", "tray")),
  domino: first((e) => has(e, "ball", "domino")),
  // the last domino nudges the relay ball too softly to count as an impact, so mark the moment it starts to move
  relay: +(rec.ball2.findIndex(([x]) => x > rec.ball2[0][0] + 1.5) / FPS).toFixed(3),
  pegs: first((e) => has(e, "ball2", "peg")),
  gate: first((e) => has(e, "ball2", "gate")),
  open: gateOpenAt,
  bell: first((e) => has(e, "ball2", "bell")),
  out: first((e) => e.t > (gateOpenAt || 0) && has(e, "ball2", "floor")),
};
const bake = { fps: FPS, t0: T0, frames: rec.ball.length, marks, gateLift: GATE_LIFT, statics, pegs, pivot: PIV, bellPivot: BELL_P, bodies: rec };
writeFileSync(new URL("../assets/bake.js", import.meta.url), "window.BAKE = " + JSON.stringify(bake) + ";\n");
writeFileSync(new URL("./events.json", import.meta.url), JSON.stringify({ marks, events }, null, 1));

// ---------- report: where the balls were, every half second ----------
const at = (k, s) => rec[k][Math.min(rec[k].length - 1, Math.round(s * FPS))];
for (let s = T0; s <= T_END + 1e-6; s += 0.5) console.log(s.toFixed(1), "ball", at("ball", s).slice(0, 2).join(","), " ball2", at("ball2", s).slice(0, 2).join(","), " tray", at("tray", s)[2], " d7", at("d7", s)[2], " bell", at("bell", s).slice(0, 2).join(","));
console.log("marks", JSON.stringify(marks), " events", events.length);
