// Full Stop. Every frame is a pure function of the beat, drawn in Canvas 2D, exposed over 12 to 24 sub-frames for real motion blur, then printed by one WebGL2 pass that can turn the frame into halftone, dither, ASCII and more.
const $ = (s) => document.querySelector(s), TB = window.TB, W = 1920, H = 1080, FPS = 30, BEAT = TB.beat, DUR = TB.dur, SUB = 12;
const BONE = "#F3EAD6", INK = "#0F0F12", RED = "#FF3A1F", COBALT = "#1B2BFF", YEL = "#FFC400", MINT = "#19E3A6", PINK = "#FF7AC6", DARK = "#050507", VIOLET = "#2A0E6E";
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), lerp = (a, b, t) => a + (b - a) * t, r01 = (x, a, b) => clamp((x - a) / (b - a));
const eO = (t) => 1 - Math.pow(1 - t, 3), eI = (t) => t * t * t, eIO = (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, xO = (t) => t >= 1 ? 1 : 1 - Math.pow(2, -10 * t);
const back = (t, s = 1.9) => 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2);
const spr = (t, f = 26, d = 7) => t < 0 ? 0 : Math.exp(-d * t) * Math.cos(f * t);   // t in seconds: a struck thing settling
const hash = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

// ---------- type: per letter, so every letter can react on its own
const cache = {};
const F = (size, weight = 900, st = "normal") => `${weight} ${st} ${size}px Archivo`;
function lay(g, s, size, weight = 900, st = "normal") {
  const k = s + "|" + size + "|" + weight + "|" + st; if (cache[k]) return cache[k];
  g.font = F(size, weight, st); g.letterSpacing = "0px";
  const out = []; for (let i = 0; i < s.length; i++) out.push(g.measureText(s.slice(0, i)).width + 0);
  // kerning-true position of each letter from its prefix
  return (cache[k] = { x: out, w: g.measureText(s).width });
}
const fit = (g, s, maxW, weight = 900, st = "normal") => { g.font = F(100, weight, st); g.letterSpacing = "0px"; return 100 * maxW / g.measureText(s).width; };
// fn(i, n, letterCentreX) may return { dx, dy, sx, sy, rot, a }; squash stands on the baseline, like a real weight
function type(g, s, x, y, size, col, o = {}) {
  const w8 = o.weight ?? 900, st = o.st ?? "normal", L = lay(g, s, size, w8, st);
  const left = o.align === "center" ? x - L.w / 2 : o.align === "right" ? x - L.w : x;
  g.font = F(size, w8, st); g.textAlign = "left"; g.textBaseline = "alphabetic"; g.letterSpacing = "0px"; g.fillStyle = col;
  for (let i = 0; i < s.length; i++) {
    if (s[i] === " ") continue;
    const nx = i + 1 < s.length ? L.x[i + 1] : L.w, cx = left + (L.x[i] + nx) / 2, m = o.fn ? o.fn(i, s.length, cx) : null;
    if (m && m.a === 0) continue;
    g.save(); g.translate(cx + (m?.dx ?? 0), y + (m?.dy ?? 0)); if (m?.rot) g.rotate(m.rot); g.scale(m?.sx ?? 1, m?.sy ?? 1); if (m?.a !== undefined) g.globalAlpha *= m.a;
    if (o.stroke) { g.strokeStyle = col; g.lineWidth = o.stroke; g.lineJoin = "round"; g.strokeText(s[i], -(nx - L.x[i]) / 2, 0); } else g.fillText(s[i], -(nx - L.x[i]) / 2, 0);
    g.restore();
  }
  return { left, right: left + L.w };
}
function mono(g, s, x, y, size, col, al = "left", sp = "0.06em") { g.font = `600 ${size}px JBM`; g.letterSpacing = sp; g.textAlign = al; g.textBaseline = "alphabetic"; g.fillStyle = col; g.fillText(s, x, y); g.letterSpacing = "0px"; }
const bg = (g, c) => { g.fillStyle = c; g.fillRect(-200, -200, W + 400, H + 400); };

// ---------- the dot: arcs between keys. A key is [beat, x, y, height of the hop that lands there]
function hop(b, K) {
  if (b <= K[0][0]) return { x: K[0][1], y: K[0][2], since: 99 };
  for (let i = 1; i < K.length; i++) if (b < K[i][0]) {
    const a = K[i - 1], c = K[i], t = (b - a[0]) / (c[0] - a[0]), h = c[3] ?? 0;
    return { x: lerp(a[1], c[1], c[4] ? xO(t) : t), y: lerp(a[2], c[2], c[4] ? xO(t) : t) - 4 * h * t * (1 - t), since: a[3] !== undefined ? (b - a[0]) * BEAT : 99 };
  }
  const e = K[K.length - 1]; return { x: e[1], y: e[2], since: e[3] !== undefined ? (b - e[0]) * BEAT : 99 };
}
// stands on its baseline point: stretched along its velocity in the air, squashed on landing
function dot(g, fn, b, r, col = RED) {
  const p = fn(b), q = fn(b + 0.03), vx = (q.x - p.x) / 0.03, vy = (q.y - p.y) / 0.03, sp = Math.hypot(vx, vy);
  const st = 1 + Math.min(0.75, sp / 7000), sq = p.since !== undefined ? 0.34 * spr(p.since, 30, 11) : 0;
  g.save(); g.translate(p.x, p.y);
  if (sq > 0.01 || sp < 40) { const s = 1 - Math.max(0, sq); g.translate(0, r * (1 - s)); g.scale(1 / Math.sqrt(s) , s); }
  else if (sq < -0.01) { g.scale(1 + sq * 0.5, 1 - sq * 0.5); }
  else { g.rotate(Math.atan2(vy, vx)); g.scale(st, 1 / st); }
  g.fillStyle = col; g.beginPath(); g.arc(0, 0, r * (p.g ?? 1), 0, Math.PI * 2); g.fill(); g.restore();
  return p;
}
const label = (g, col) => mono(g, "AI AUTOMATION SYSTEMS · DEMO WORKFLOW", 56, H - 46, 18, col);
const iris = (g, x, y, r, fn) => { g.save(); g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.clip(); fn(); g.restore(); };

// ---------- A: the dot falls, then drags the first sentence out behind it
const A_S = 196, A_Y = 610;
function sentence(g, b) {
  const s = "THE SAME TASK", L = lay(g, s, A_S), left = (W - L.w - A_S * 0.26) / 2, pos = (k) => left + (k < s.length ? L.x[k] : L.w);
  const e = (w, f) => pos(w) + f; return { s, L, left, x3: pos(3), x8: pos(8), x13: L.w + left + A_S * 0.16 };
}
function sceneA(g, b) {
  bg(g, BONE); const S = sentence(g, b), r = A_S * 0.105, y = A_Y - r, x0 = S.left + 30;
  const K = [[0.3, x0, -120], [1, x0, y, 0], [1.5, x0, y, 150], [1.75, x0, y, 50], [1.875, x0, y, 16], [2, x0, y, 6], [2.18, S.x3 + 14, y, 0, 1], [2.5, S.x3 + 14, y], [2.68, S.x8 + 14, y, 0, 1], [3, S.x8 + 14, y], [3.2, S.x13, y, 0, 1], [3.72, S.x13, y]];
  const f = (bb) => hop(bb, K), P = f(b);
  const gone = b >= 4;
  if (b >= 2) {
    g.save(); g.beginPath(); g.rect(0, 0, P.x + 2, H); g.clip();
    type(g, S.s, S.left, A_Y, A_S, INK, { fn: (i, n, cx) => {
      const hit = i < 3 ? 2.18 : i < 8 ? 2.68 : 3.2, t = (b - hit) * BEAT + 0.05 - (cx > P.x ? 0 : 0);
      const fall = b >= 3.75 ? eI(r01(b, 3.75 + i * 0.018, 4.45 + i * 0.018)) : 0;
      const wave = spr((b - 3.2) * BEAT - (S.x13 - cx) / 4200, 22, 6) * (b >= 3.2 ? 0.16 : 0);
      return { dy: fall * 900 + 0, rot: fall * (hash(i) - 0.5) * 1.4, sy: 1 + wave + 0.2 * spr(t, 24, 9), sx: 1 - 0.5 * wave };
    } });
    g.restore();
  }
  dot(g, f, b, r);
  return { x: S.x13, y, r };
}
// ---------- B, C: the same move twice, the same way, on purpose
const AG_Y = 700, AG_S = 400, AG2_S = 262, AG2_Y = 640;
function sceneBC(g, b) {
  const S = sentence(g, b), rA = A_S * 0.105, start = [S.x13, A_Y - rA];
  const one = "AGAIN", two = "AND AGAIN", La = lay(g, one, AG_S), Lb = lay(g, two, AG2_S);
  const r1 = AG_S * 0.105, r2 = AG2_S * 0.105, la = (W - La.w - AG_S * 0.26) / 2, lb = (W - Lb.w - AG2_S * 0.26) / 2;
  const px1 = la + La.w + AG_S * 0.15, px2 = lb + Lb.w + AG2_S * 0.15;
  const K = [[3.9, start[0], start[1]], [4, start[0], start[1]], [5, px1, AG_Y - r1, 420], [5.5, px1, AG_Y - r1, 70], [6, px1, AG_Y - r1], [7, px2, AG2_Y - r2, 460], [7.5, px2, AG2_Y - r2, 70], [8, px2, AG2_Y - r2]];
  const f = (bb) => hop(bb, K), P = f(b);
  if (b < 5) { bg(g, BONE); if (b < 4.5) sceneAFall(g, b); }
  else if (b < 7) {
    bg(g, BONE); iris(g, px1, AG_Y - r1, xO(r01(b, 5, 5.45)) * 2400, () => { bg(g, INK); type(g, one, la, AG_Y, AG_S, BONE, { fn: (i) => {
      const u = back(r01(b, 5 + i * 0.05, 5.42 + i * 0.05)); return { dy: (1 - u) * 620, sy: 1 + 0.16 * spr((b - 5 - i * 0.05) * BEAT, 22, 7) }; } }); });
    if (b >= 6) { const fall = eI(r01(b, 6.0, 6.5)); /* the old word goes */ g.globalAlpha = 1; }
  }
  if (b >= 5.9 && b < 7) { /* the word is pulled down as the dot leaves */ }
  if (b >= 7) {
    bg(g, INK); iris(g, px2, AG2_Y - r2, xO(r01(b, 7, 7.45)) * 2400, () => { bg(g, YEL); type(g, two, lb, AG2_Y, AG2_S, INK, { fn: (i) => {
      const u = back(r01(b, 7 + i * 0.03, 7.4 + i * 0.03)); return { dy: (1 - u) * 620, sy: 1 + 0.16 * spr((b - 7 - i * 0.03) * BEAT, 22, 7) }; } }); });
  }
  dot(g, f, b, b < 5.8 ? r1 * lerp(rA / r1, 1, r01(b, 4, 5)) : lerp(r1, r2, r01(b, 6, 7)));
}
function sceneAFall(g, b) { const S = sentence(g, b); type(g, S.s, S.left, A_Y, A_S, INK, { fn: (i) => { const fall = eI(r01(b, 3.75 + i * 0.018, 4.45 + i * 0.018)); return { dy: fall * 900, rot: fall * (hash(i) - 0.5) * 1.4 }; } }); }

// ---------- D: one becomes sixty-four, every tile the same little job, the camera pulled back on each doubling
const GR = [[2, 1], [2, 2], [4, 2], [4, 4], [8, 4], [8, 8]], TCOL = [[BONE, INK], [INK, BONE], [YEL, INK], [COBALT, BONE], [MINT, INK], [PINK, INK]];
function sceneD(g, b) {
  const k = Math.min(5, Math.floor(b - 8)), [cx, cy] = GR[k], u = xO(r01(b, 8 + k, 8 + k + 0.4)), pull = lerp(k === 0 ? 1.6 : (GR[k][0] * GR[k][1] > GR[k - 1][0] * GR[k - 1][1] && GR[k][0] > GR[k - 1][0] ? 2 : 2), 1, u);
  let zoom = pull, tx = 0, ty = 0;
  const tw = W / cx, th = H / cy, zi = 4, zj = 4, dotR = Math.min(tw, th) * 0.05;
  const lb = (x) => x;
  const zt = r01(b, 13.45, 14); const fx = zi * tw + tw * 0.86, fy = zj * th + th * 0.7;
  g.save();
  if (zt > 0) { const s = Math.pow(2, eI(zt) * 9.6); g.translate(W / 2, H / 2); g.scale(s, s); g.translate(-lerp(W / 2, fx, Math.min(1, zt * 3)), -lerp(H / 2, fy, Math.min(1, zt * 3))); }
  else { g.translate(W / 2, H / 2); g.scale(zoom, zoom); g.translate(-W / 2, -H / 2); }
  for (let j = 0; j < cy; j++) for (let i = 0; i < cx; i++) {
    const [c1, c2] = TCOL[(i + j * 3 + ((i ^ j) & 1) * 2) % TCOL.length], x = i * tw, y = j * th;
    g.fillStyle = c1; g.fillRect(x, y, tw + 1, th + 1);
    const size = fit(g, "AGAIN", tw * 0.62), base = y + th * 0.7 , L = lay(g, "AGAIN", Math.round(size)), left = x + tw * 0.14, r = Math.round(size) * 0.105, px = left + L.w + Math.round(size) * 0.15;
    const ph = ((i + j) % 4) * 0.25 * (k >= 3 ? 1 : 0), per = k >= 5 ? 0.5 : k >= 2 ? 0.5 : 1, tt = (((b - ph) % per) + per) % per / per, ly = base - r - 4 * th * 0.28 * tt * (1 - tt);
    type(g, "AGAIN", left, base, Math.round(size), c2, { fn: () => ({ sy: 1 + 0.2 * spr(tt * per * BEAT, 24, 11) }) });
    const sq = 0.42 * spr(tt * per * BEAT, 30, 11);
    g.fillStyle = RED; g.beginPath(); g.ellipse(px, ly + (sq > 0 ? r * sq : 0), r / Math.sqrt(1 - Math.max(0, sq)), r * (1 - Math.max(0, sq)), 0, 0, Math.PI * 2); g.fill();
  }
  g.restore();
}

// ---------- E: karaoke. The dot lands on each word, and the word gets up to meet it
const E1 = { s: "IF YOU CAN", size: 168, y: 410 }, E2 = { s: "DESCRIBE IT", size: 262, y: 700 };
function sceneE(g, b) {
  g.save(); bg(g, COBALT);
  const L1 = lay(g, E1.s, E1.size), L2 = lay(g, E2.s, E2.size), l1 = (W - L1.w) / 2, l2 = (W - L2.w) / 2;
  const cx1 = (i0, i1) => l1 + (L1.x[i0] + (i1 < E1.s.length ? L1.x[i1] : L1.w)) / 2, cx2 = (i0, i1) => l2 + (L2.x[i0] + (i1 < E2.s.length ? L2.x[i1] : L2.w)) / 2;
  const y1 = E1.y - E1.size * 0.72 - 30, y2 = E2.y - E2.size * 0.72 - 30;
  const K = [[14, W / 2, H / 2], [14.5, cx1(0, 2), y1, 80], [15, cx1(3, 6), y1, 150], [15.5, cx1(7, 10), y1, 150], [16, cx2(0, 2), y2, 90], [16.5, cx2(2, 8), y2, 170], [17.5, cx2(9, 11), y2, 230], [18, cx2(9, 11), y2, 60], [18.5, cx2(9, 11), y2, 60], [19, cx2(9, 11), y2, 60], [19.5, cx2(9, 11), y2, 60], [20, 1500, 1010, 340]];
  const hitOf = (i) => i < 2 ? 14.5 : i < 6 ? 15 : 15.5, hit2 = (i) => i < 2 ? 16 : i < 8 ? 16.5 : 17.5, off = eI(r01(b, 19.5, 20));
  type(g, E1.s, l1, E1.y, E1.size, BONE, { fn: (i) => { const h = hitOf(i), u = r01(b, h - 0.02, h + 0.3); if (u <= 0) return { a: 0 }; return { dy: (1 - back(u)) * 90 + off * 1200, sy: back(u) * (1 - 0.3 * spr((b - h) * BEAT, 24, 8)), rot: off * (hash(i) - 0.5) }; } });
  type(g, E2.s, l2, E2.y, E2.size, BONE, { fn: (i, n, cx) => { const h = hit2(i) + (i >= 2 && i < 8 ? (i - 2) * 0.09 : 0), u = r01(b, h - 0.02, h + 0.3); if (u <= 0) return { a: 0 };
    const wob = b >= 18 && b < 19.5 ? Math.sin((b - 18) * 6.28 * 1 - i * 0.7) * 30 * r01(b, 18, 18.3) : 0; return { dy: (1 - back(u)) * 140 + wob * 0 + off * 1400 , sy: back(u) * (1 - 0.3 * spr((b - h) * BEAT, 24, 8)) + wob * 0.012, rot: off * (hash(i + 20) - 0.5) }; } });
  dot(g, (bb) => hop(bb, K), b, 34);
  g.restore();
}

// ---------- F: the map. The camera rolls at every corner, so the dot always runs left to right
const NODES = [["INTAKE", 0, 0], ["SORT", 1200, 0], ["CHECK", 2400, 0], ["DRAFT", 2400, 900], ["REVIEW", 1200, 900], ["SEND", 0, 900]], NB = [20.5, 22, 23.5, 25, 26.5, 28];
const HEAD = [0, 0, Math.PI / 2, Math.PI, Math.PI, Math.PI];
const icon = (g, k, c) => { g.strokeStyle = c; g.lineWidth = 9; g.lineCap = "round"; g.lineJoin = "round"; g.beginPath();
  if (k === 0) { g.rect(-34, -46, 68, 92); g.moveTo(-16, -16); g.lineTo(16, -16); g.moveTo(-16, 8); g.lineTo(16, 8); }
  if (k === 1) { g.moveTo(-44, -36); g.lineTo(44, -36); g.lineTo(10, 6); g.lineTo(10, 42); g.lineTo(-10, 30); g.lineTo(-10, 6); g.closePath(); }
  if (k === 2) { g.moveTo(-40, 2); g.lineTo(-10, 34); g.lineTo(44, -34); }
  if (k === 3) { g.moveTo(-40, 40); g.lineTo(-30, 8); g.lineTo(22, -44); g.lineTo(42, -24); g.lineTo(-10, 28); g.closePath(); }
  if (k === 4) { g.moveTo(-50, 0); g.quadraticCurveTo(0, -46, 50, 0); g.quadraticCurveTo(0, 46, -50, 0); g.moveTo(14, 0); g.arc(0, 0, 14, 0, 6.3); }
  if (k === 5) { g.moveTo(-46, 0); g.lineTo(40, 0); g.moveTo(10, -30); g.lineTo(42, 0); g.lineTo(10, 30); }
  g.stroke(); };
function mapPos(b) {
  // node to node with an anticipating ease, world coordinates
  if (b <= NB[0]) return { x: lerp(-900, 0, eIO(r01(b, 20, 20.5))), y: 0, since: 9 };
  for (let i = 1; i < 6; i++) if (b < NB[i]) { const t = r01(b, NB[i] - 0.8, NB[i]), e = t < 0.5 ? -0.1 * Math.sin(t * 6.28) : xO((t - 0.5) * 2) * 1; const a = NODES[i - 1], c = NODES[i], s = t < 0.5 ? -0.08 * Math.sin(t * 6.28) : eIO((t - 0.5) * 2); return { x: lerp(a[1], c[1], s), y: lerp(a[2], c[2], s), since: (b - NB[i - 1]) * BEAT }; }
  return { x: NODES[5][1], y: NODES[5][2], since: (b - NB[5]) * BEAT };
}
function sceneF(g, b) {
  bg(g, COBALT);
  const P = mapPos(b); let seg = 0; for (let i = 0; i < 6; i++) if (b >= NB[i] - 0.5) seg = i;
  const rollFrom = HEAD[Math.max(0, seg - 1)], rollTo = HEAD[seg], rt = back(r01(b, NB[seg] - 0.5, NB[seg] - 0.05), 1.2);
  const follow = 1 - eIO(r01(b, 28.2, 29.3)), zoom = lerp(0.36, 1.12, follow), roll = lerp(0, lerp(rollFrom, rollTo, rt) * -1, follow);
  const cxW = lerp(1200, P.x, follow), cyW = lerp(450, P.y, follow), scY = lerp(400, H / 2, follow);
  g.save(); g.translate(W / 2, scY); g.rotate(roll); g.scale(zoom, zoom); g.translate(-cxW, -cyW);
  // grid paper that travels with the world
  g.strokeStyle = "rgba(243,234,214,0.14)"; g.lineWidth = 2; g.beginPath(); for (let x = -2400; x <= 4800; x += 150) { g.moveTo(x, -2400); g.lineTo(x, 3400); } for (let y = -2400; y <= 3400; y += 150) { g.moveTo(-2400, y); g.lineTo(4800, y); } g.stroke();
  // side branches shoot off each node: the handoffs
  for (let i = 0; i < 6; i++) { const u = eO(r01(b, NB[i], NB[i] + 0.8)); if (u <= 0) continue; const n = NODES[i]; g.strokeStyle = "rgba(243,234,214,0.5)"; g.lineWidth = 4; g.setLineDash([12, 14]); g.beginPath();
    for (let a = 0; a < 4; a++) { const an = (hash(i * 7 + a) * 6.28), d = 260 + hash(i * 5 + a) * 240; g.moveTo(n[1], n[2]); g.lineTo(n[1] + Math.cos(an) * d * u, n[2] + Math.sin(an) * d * u); } g.stroke(); g.setLineDash([]);
    for (let a = 0; a < 4; a++) { const an = (hash(i * 7 + a) * 6.28), d = 260 + hash(i * 5 + a) * 240, s = back(r01(b, NB[i] + 0.3, NB[i] + 0.8)) * 14; if (s > 0) { g.fillStyle = BONE; g.fillRect(n[1] + Math.cos(an) * d - s, n[2] + Math.sin(an) * d - s, s * 2, s * 2); } } }
  // the line, drawn by the dot
  g.strokeStyle = BONE; g.lineWidth = 11; g.lineCap = "round"; g.lineJoin = "round"; g.beginPath(); g.moveTo(-900, 0); for (let i = 0; i < 6; i++) { if (b >= NB[i]) g.lineTo(NODES[i][1], NODES[i][2]); else { g.lineTo(P.x, P.y); break; } } g.stroke();
  // nodes
  for (let i = 0; i < 6; i++) { const n = NODES[i], u = r01(b, NB[i] - 0.06, NB[i] + 0.28); if (u <= 0) continue; const s = back(u, 2.6), w = 400, h = 400;
    g.save(); g.translate(n[1], n[2]); g.rotate(-lerp(rollFrom, rollTo, rt) * 0 ); g.scale(s, s * (1 + 0.14 * spr((b - NB[i]) * BEAT, 22, 8)));
    const ro = roll; g.rotate(-ro); // labels stay upright to the viewer
    g.fillStyle = BONE; g.beginPath(); g.roundRect(-w / 2, -h / 2, w, h, 26); g.fill(); g.save(); g.translate(0, -122); g.scale(0.85, 0.85); icon(g, i, COBALT); g.restore(); g.fillStyle = COBALT; g.beginPath(); g.arc(0, 8, 62, 0, 6.3); g.fill();
    type(g, n[0], 0, 158, 58, COBALT, { align: "center", weight: 800 }); g.restore();
    g.save(); g.translate(n[1], n[2]); g.rotate(-roll); type(g, "0" + (i + 1), 230, -70, 300, "rgba(243,234,214,0.16)", { weight: 900 }); g.restore();
    const ring = r01(b, NB[i], NB[i] + 0.9); if (ring > 0 && ring < 1) { g.strokeStyle = `rgba(243,234,214,${1 - ring})`; g.lineWidth = 8; g.beginPath(); g.arc(n[1], n[2], 150 + eO(ring) * 520, 0, 6.3); g.stroke(); }
  }
  // the dot rides on top, until it leaves for the caption
  if (b < 28.6) { const fn = (bb) => { const q = mapPos(bb); return { x: q.x, y: q.y, since: q.since }; }; const a = b < NB[0] ? 1 : 1; g.save(); dot(g, fn, b, 46); g.restore(); }
  g.restore();
  // caption, and the dot lands as its full stop
  if (b >= 28.3) { const t = "MAPPED BEFORE ANY CODE", S = Math.round(fit(g, t, 1520)), L = lay(g, t, S), l = (W - L.w - S * 0.26) / 2, base = 950, r = S * 0.105, px = l + L.w + S * 0.15;
    type(g, t, l, base, S, BONE, { fn: (i) => { const u = r01(b, 28.5 + i * 0.022, 28.95 + i * 0.022); return u <= 0 ? { a: 0 } : { dy: (1 - back(u)) * 90, sy: 1 + 0.14 * spr((b - 29.5) * BEAT, 22, 8) }; } });
    if (b >= 28.6) { const sc = zoom, sx = W / 2 + (NODES[5][1] - cxW) * sc * Math.cos(roll) - (NODES[5][2] - cyW) * sc * Math.sin(roll), sy = scY + (NODES[5][1] - cxW) * sc * Math.sin(roll) + (NODES[5][2] - cyW) * sc * Math.cos(roll);
      const K = [[28.6, sx, sy], [29.5, px, base - r, 360]], KK = [...K, [30, px, base - r]]; dot(g, (bb) => hop(bb, KK), b, r); } }
  label(g, "rgba(243,234,214,0.8)");
}

// ---------- G: the dot IS the dot in the code
const CODE = ["for task in queue:", "    if task.matches(pattern):", "        result = task.run()", "        checks.verify(result)", "    log.write(task.id)", "def run_on_schedule(cfg):", "    tasks = intake.read(cfg.source)", "    return [task.run() for task in tasks]", "review.request(result)", "output.save(result, cfg.folder)"];
function sceneG(g, b) {
  bg(g, INK); const u = b - 30;
  g.save(); g.globalAlpha = 0.22; for (let k = 0; k < 18; k++) { const y = 80 + ((k * 62 - u * 620) % 1116 + 1116) % 1116 - 18; mono(g, CODE[k % CODE.length], 96 + (k % 3) * 8, y, 30, k % 4 === 1 ? MINT : "#8E9BB8", "left", "0"); } g.restore();
  if (b < 31) { g.font = "800 230px JBM"; g.textAlign = "left"; g.textBaseline = "alphabetic"; const a = "task", c = "run()", wa = g.measureText(a).width, gap = g.measureText(".").width, wc = g.measureText(c).width, l = (W - wa - gap - wc) / 2, base = 625, r = 30;
    const land = xO(r01(b, 30, 30.2)); g.save(); g.translate(W / 2, base); g.scale(1, 1 + 0.08 * spr(u * BEAT, 22, 8)); g.translate(-W / 2, -base); g.font = "800 230px JBM"; g.fillStyle = BONE; g.fillText(a, l, base); g.fillStyle = MINT; g.fillText(c, l + wa + gap, base); g.restore();
    const K = [[29.9, l + wa + gap / 2, -60], [30, l + wa + gap / 2, base - r], [30.5, l + wa + gap / 2, base - r, 120], [31, l + wa + gap / 2, base - r, 120]]; dot(g, (bb) => hop(bb, K), b, r); }
  else { const s1 = "CUSTOM", s2 = "PYTHON", S = 320, base1 = 480, base2 = 800, La = lay(g, s2, S), l = (W - La.w - S * 0.26) / 2, r = S * 0.105, px = l + La.w + S * 0.15, y = base2 - r;
    const sl = (x, h, d) => { const q = xO(r01(b, h, h + 0.3)); return { dx: (1 - q) * d, sx: 1 + (1 - q) * 0.6 }; };
    type(g, s1, l, base1, S, BONE, { fn: () => sl(0, 31, -1900) }); if (b >= 31.5) type(g, s2, l, base2, S, MINT, { fn: () => sl(0, 31.5, 1900) });
    const K = [[31, l + 200, 500], [31.5, px, y, 240], [32, px, y, 110]]; dot(g, (bb) => hop(bb, K), b, r);
  }
  label(g, "rgba(243,234,214,0.75)");
}

// ---------- H: NOT A TEMPLATE, twenty cuts, never the same film twice. The dot keeps one bounce through all of it
const NAT = { a: "NOT A", b: "TEMPLATE", s: 252, xl: 150, y1: 470, y2: 770 };
function natDot(b, g) { const L = lay(g, NAT.b, NAT.s), r = NAT.s * 0.105, px = NAT.xl + L.w + NAT.s * 0.15, f = (bb) => { const per = 1, t = ((bb % per) + per) % per; return { x: px, y: NAT.y2 - r - 4 * 150 * t * (1 - t), since: t * BEAT }; }; return { f, r, px }; }
const nat = (g, col, o = {}) => { type(g, NAT.a, NAT.xl, NAT.y1, NAT.s, o.c1 ?? col, o); type(g, NAT.b, NAT.xl, NAT.y2, NAT.s, col, o); };
const stripes = (g, c, w, ang, ph = 0) => { g.save(); g.translate(W / 2, H / 2); g.rotate(ang); g.fillStyle = c; for (let x = -1400 + (ph % (w * 2)); x < 1400; x += w * 2) g.fillRect(x, -1400, w, 2800); g.restore(); };
const STYLES = [
  // 0 Swiss
  (g, b, l) => { bg(g, BONE); g.fillStyle = INK; g.fillRect(NAT.xl, 96, W - 2 * NAT.xl, 10); g.fillRect(NAT.xl, 900, W - 2 * NAT.xl, 4); nat(g, INK, { fn: (i) => ({ dy: (1 - xO(clamp(l * 5 - i * 0.2))) * 80 }) }); mono(g, "NOT A TEMPLATE", NAT.xl, 150, 26, INK); mono(g, "FIG. 01", W - NAT.xl, 150, 26, INK, "right"); return { mode: 0 }; },
  // 1 halftone
  (g, b, l) => { const r = g.createRadialGradient(1400, 300, 40, 1400, 300, 1400); r.addColorStop(0, "#fff"); r.addColorStop(1, "#111"); g.fillStyle = r; g.fillRect(0, 0, W, H); nat(g, "#fff"); return { mode: 1, a: [0.05, 0.06, 0.09], b: [0.98, 0.93, 0.8] }; },
  // 2 extrude
  (g, b, l) => { bg(g, YEL); stripes(g, "rgba(15,15,18,0.08)", 36, 0.7, l * 200); const n = 34; for (let k = n; k > 0; k--) nat(g, k === n ? INK : "#201A08", { fn: () => ({ dx: k * 2.4 * Math.cos(l * 2 + 0.6), dy: k * 2.4 * Math.sin(l * 2 + 0.9) }) }); nat(g, BONE); return { mode: 0 }; },
  // 3 dither
  (g, b, l) => { const v = g.createLinearGradient(0, 0, 0, H); v.addColorStop(0, "#000"); v.addColorStop(0.6, "#aaa"); v.addColorStop(1, "#000"); g.fillStyle = v; g.fillRect(0, 0, W, H); g.fillStyle = "#fff"; g.beginPath(); g.arc(1360, 330, 280, 0, 6.3); g.fill(); nat(g, "#000"); return { mode: 2, a: [0.09, 0.03, 0.26], b: [1.0, 0.72, 0.84] }; },
  // 4 moire
  (g, b, l) => { bg(g, "#000"); g.globalCompositeOperation = "difference"; g.lineWidth = 7; g.strokeStyle = "#fff"; for (const [cx, cy] of [[700 - l * 240, 540], [1200 + l * 240, 500]]) { g.beginPath(); for (let r = 6; r < 1900; r += 15) { g.moveTo(cx + r, cy); g.arc(cx, cy, r, 0, 6.3); } g.stroke(); } nat(g, "#fff"); g.globalCompositeOperation = "source-over"; return { mode: 0 }; },
  // 5 ascii
  (g, b, l) => { const r = g.createRadialGradient(960, 540, 60, 960, 540, 1100); r.addColorStop(0, "#555"); r.addColorStop(1, "#000"); g.fillStyle = r; g.fillRect(0, 0, W, H); nat(g, "#fff"); return { mode: 3, a: [0.02, 0.05, 0.04], b: [0.1, 0.89, 0.65] }; },
  // 6 slices
  (g, b, l) => { bg(g, COBALT); const n = 14, h = H / n; for (let k = 0; k < n; k++) { g.save(); g.beginPath(); g.rect(0, k * h, W, h + 1); g.clip(); g.translate(Math.sin(k * 1.7 + l * 9) * 90 * Math.exp(-l * 2.5), 0); nat(g, BONE); g.restore(); } return { mode: 0 }; },
  // 7 neon
  (g, b, l) => { bg(g, "#000"); g.strokeStyle = "#fff"; g.lineWidth = 14; g.strokeRect(70, 70, W - 140, H - 140); nat(g, "#fff"); return { mode: 7, a: [1.0, 0.25, 0.75], b: [0.03, 0.0, 0.07] }; },
  // 8 stack of widths
  (g, b, l) => { bg(g, MINT); const sts = ["extra-condensed", "condensed", "semi-condensed", "normal", "semi-expanded", "expanded"], n = 7, s = 150; for (let k = 0; k < n; k++) { const off = sts[Math.abs((k + Math.floor(l * 30 / 2)) % sts.length)]; type(g, k === 4 ? "TEMPLATE" : "NOT A TEMPLATE", 70, 142 + k * 148, s, k === 4 ? INK : "#0C8F69", { st: k === 4 ? "normal" : off }); } return { mode: 0, noDot: 1, dotAt: 1 }; },
  // 9 riso
  (g, b, l) => { bg(g, "#fff"); g.fillStyle = "#777"; g.beginPath(); g.arc(1420, 360, 300, 0, 6.3); g.fill(); g.fillStyle = "#b5b5b5"; g.fillRect(90, 110, 900, 800); nat(g, "#000"); return { mode: 6, a: [0.1, 0.17, 0.9], b: [1.0, 0.3, 0.55] }; },
  // 10 Bauhaus
  (g, b, l) => { bg(g, BONE); const q = Math.floor(l * 30 / 2) % 4; g.save(); g.translate(1320, 420); g.rotate(q * Math.PI / 2); g.fillStyle = COBALT; g.beginPath(); g.arc(0, 0, 370, 0, Math.PI); g.fill(); g.fillStyle = YEL; g.beginPath(); g.moveTo(-370, 0); g.lineTo(370, 0); g.lineTo(0, -370); g.fill(); g.restore(); g.fillStyle = INK; g.fillRect(0, 880, W, 200); nat(g, INK); return { mode: 0 }; },
  // 11 pixel
  (g, b, l) => { const v = g.createLinearGradient(0, 0, W, H); v.addColorStop(0, "#14D9FF"); v.addColorStop(0.55, "#7B3CFF"); v.addColorStop(1, "#FFB400"); g.fillStyle = v; g.fillRect(0, 0, W, H); nat(g, "#fff"); return { mode: 5 }; },
  // 12 checker warp
  (g, b, l) => { bg(g, "#000"); const s = 88, P = natDot(b, g); g.fillStyle = "#fff"; for (let j = -1; j < 14; j++) for (let i = -1; i < 24; i++) if ((i + j) & 1) { const x = i * s, y = j * s, dx = x + s / 2 - P.px, dy = y + s / 2 - 700, d = Math.hypot(dx, dy), w = 1 - 0.78 * Math.exp(-d / 420), ang = l * 0.5 * Math.exp(-d / 700); g.save(); g.translate(P.px + dx * w, 700 + dy * w); g.rotate(ang); g.fillRect(-s * w / 2, -s * w / 2, s * w, s * w); g.restore(); } g.globalCompositeOperation = "difference"; nat(g, "#fff"); g.globalCompositeOperation = "source-over"; return { mode: 0 }; },
  // 13 echo outlines
  (g, b, l) => { bg(g, INK); for (let k = 14; k >= 1; k--) { g.save(); const s = 1 + k * 0.045 * eO(clamp(l * 4)); g.translate(W / 2, H / 2); g.scale(s, s); g.translate(-W / 2, -H / 2); nat(g, k % 2 ? PINK : "#7A2A8E", { stroke: 2.5 }); g.restore(); } nat(g, PINK); return { mode: 0 }; },
  // 14 gradient mesh
  (g, b, l) => { bg(g, "#FF6A3D"); for (const [x, y, r, c] of [[300 + l * 500, 240, 900, "#8A2BFF"], [1560 - l * 400, 240, 900, "#00C2FF"], [960, 1000, 1000, "#FFD400"]]) { const q = g.createRadialGradient(x, y, 0, x, y, r); q.addColorStop(0, c); q.addColorStop(1, c + "00"); g.fillStyle = q; g.fillRect(0, 0, W, H); } nat(g, "#fff"); return { mode: 4, a: [0, 0, 0], b: [1, 1, 1] }; },
  // 15 blueprint
  (g, b, l) => { bg(g, "#07219E"); g.strokeStyle = "rgba(255,255,255,0.2)"; g.lineWidth = 2; g.beginPath(); for (let x = 0; x < W; x += 60) { g.moveTo(x, 0); g.lineTo(x, H); } for (let y = 0; y < H; y += 60) { g.moveTo(0, y); g.lineTo(W, y); } g.stroke(); nat(g, "#fff", { stroke: 4 }); const L = lay(g, NAT.b, NAT.s); g.strokeStyle = "#fff"; g.lineWidth = 3; g.beginPath(); g.moveTo(NAT.xl, 860); g.lineTo(NAT.xl + L.w, 860); g.moveTo(NAT.xl, 845); g.lineTo(NAT.xl, 875); g.moveTo(NAT.xl + L.w, 845); g.lineTo(NAT.xl + L.w, 875); g.stroke(); mono(g, "A PURPOSE-BUILT PIPELINE", NAT.xl + L.w / 2, 905, 26, "#fff", "center"); return { mode: 0 }; },
];
const ORDER = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 5, 4, 7];
function sceneH(g, b) {
  let k = 0; for (let i = 0; i < TB.styles.length; i++) if (b >= TB.styles[i]) k = i;
  const l = (b - TB.styles[k]) * BEAT, P = natDot(b, g), res = STYLES[ORDER[k]](g, b, l);
  if (!res.noDot) dot(g, P.f, b, P.r); else { const f = (bb) => { const q = P.f(bb); const Lb = lay(g, "TEMPLATE", 150); return { x: 70 + Lb.w + 40, y: 142 + 4 * 148 - 15 - (720 - q.y) * 0 - 4 * 60 * ((bb % 1 + 1) % 1) * (1 - ((bb % 1 + 1) % 1)), since: q.since }; }; dot(g, f, b, 18); }
  return res;
}

// ---------- I: nothing. One dot and the room
function sceneI(g, b) {
  bg(g, DARK); const y = H / 2;
  const K = [[41.95, 960, -80], [42, 960, y], [42.5, 960, y, 90], [42.75, 960, y, 24], [43.75, 960, y]];
  const f = (bb) => { const p = hop(bb, K); return p; };
  for (const tb of [43, 43.5]) { const u = r01(b, tb, tb + 0.8); if (u > 0 && u < 1) { g.strokeStyle = `rgba(243,234,214,${0.5 * (1 - u)})`; g.lineWidth = 3; g.beginPath(); g.arc(960, y, 34 + eO(u) * 260, 0, 6.3); g.fill; g.stroke(); } }
  const an = r01(b, 43.6, 44); g.fillStyle = RED; g.beginPath(); const P = f(b); const s = 1 - 0.35 * eIO(an); g.ellipse(P.x, P.y + 34 * (1 - s), 34 / Math.sqrt(s), 34 * s, 0, 0, 6.3); g.fill();
}

// ---------- J: the schedule. A clock you fall into, the dot orbiting ever faster
const TIMES = ["06:00", "12:00", "18:00", "00:00"], SKY = [["#FFC400", INK, "#FF9A00"], ["#F3EAD6", INK, "#19E3A6"], ["#FF7A3D", INK, "#2A0E6E"], ["#090A2A", BONE, "#1B2BFF"]];
function ringText(g, s, R, ang, size, col) { g.font = F(size, 800); g.textAlign = "center"; g.textBaseline = "middle"; g.fillStyle = col; const step = 2 * Math.PI / s.length; for (let i = 0; i < s.length; i++) { const a = ang + i * step; g.save(); g.translate(R * Math.cos(a), R * Math.sin(a)); g.rotate(a + Math.PI / 2); g.fillText(s[i], 0, 0); g.restore(); } }
function sceneJ(g, b) {
  const stage = b < 48 ? 0 : Math.min(3, Math.floor((b - 48) / 2)), [c1, c2, c3] = SKY[stage], cx = W / 2, cy = H / 2;
  bg(g, c1);
  const orbitT = (bb) => { const x = bb - 44; return x * Math.PI + Math.PI * Math.max(0, x - 4) * Math.max(0, x - 4) * 0.08 - Math.PI / 2; };
  if (b < 48) {
    // the great clock: wedges fill hour by hour
    const u = xO(r01(b, 44, 44.45)), Rm = 500 * u + 1500 * (1 - u), hours = Math.floor(((b - 44) / 2) * 12) ;
    g.save(); g.translate(cx, cy); g.rotate((1 - u) * -1.4);
    for (let i = 0; i < 12; i++) { const on = i <= hours % 12 || hours >= 12; g.fillStyle = on ? (i % 2 ? c3 : INK) : "rgba(15,15,18,0.08)"; const a0 = -Math.PI / 2 + i * Math.PI / 6 - 0.0, a1 = a0 + Math.PI / 6, pop = on ? 1 + 0.06 * spr(((b - 44) - i / 6) * BEAT, 24, 8) : 1; g.beginPath(); g.moveTo(0, 0); g.arc(0, 0, Rm * pop, a0, a1); g.closePath(); g.fill(); }
    g.fillStyle = c1; g.beginPath(); g.arc(0, 0, Rm * 0.56, 0, 6.3); g.fill(); g.restore();
    const hit = 44; type(g, "ON YOUR", cx, cy - 26, 104, INK, { align: "center", fn: (i) => { const v = r01(b, 44.2 + i * 0.03, 44.6 + i * 0.03); return v <= 0 ? { a: 0 } : { dy: (1 - back(v)) * 40 }; } });
    if (b >= 46) type(g, "SCHEDULE", cx, cy + 76, 104, INK, { align: "center", st: "condensed", fn: (i) => { const v = r01(b, 46 + i * 0.025, 46.36 + i * 0.025); return v <= 0 ? { a: 0 } : { dy: (1 - back(v)) * 40 , sy: 1 + 0.2 * spr((b - 46) * BEAT, 22, 8) }; } });
  } else {
    // falling through nested clock faces
    const ph = (b - 48) * 1.0, N = 9;
    for (let k = N; k >= 0; k--) { const zz = k - ((ph * 2) % 1), R = 60 * Math.pow(1.72, zz + 3.2), col = (k + Math.floor(ph * 2)) % 2 ? c3 : c2; if (R < 20) continue;
      g.fillStyle = col; g.beginPath(); g.arc(cx, cy, R, 0, 6.3); g.fill();
      g.save(); g.translate(cx, cy); g.rotate((k % 2 ? 1 : -1) * ph * 0.9); g.fillStyle = (k + Math.floor(ph * 2)) % 2 ? c2 : c3; for (let a = 0; a < 12; a++) { g.rotate(Math.PI / 6); g.fillRect(-R * 0.02, -R, R * 0.04, R * 0.14); } g.restore(); }
    g.fillStyle = c1; g.beginPath(); g.arc(cx, cy, 300, 0, 6.3); g.fill(); g.strokeStyle = c2; g.lineWidth = 10; g.stroke();
    g.save(); g.translate(cx, cy); ringText(g, "ON YOUR SCHEDULE · ON YOUR SCHEDULE · ", 252, (b - 48) * -0.9, 34, c2); g.restore();
    const tb = 48 + stage * 2, v = back(r01(b, tb, tb + 0.28), 2.4); g.save(); g.translate(cx, cy + 56); g.scale(v, v); type(g, TIMES[stage], 0, 0, 168, c2, { align: "center", st: "condensed" }); g.restore();
    g.fillStyle = c1; g.fillRect(W - 500, H - 76, 460, 46); mono(g, "SCHEDULED RUNS, IF YOU WANT THEM", W - 56, H - 46, 18, c2, "right");
  }
  const R = b < 48 ? 430 : 400 , out = b >= 55 ? eI(r01(b, 55, 56)) : 0;
  const fn = (bb) => { const a = orbitT(bb), rr = lerp(R, 0, b >= 55 ? out : 0); return { x: cx + rr * Math.cos(a), y: cy + rr * Math.sin(a) }; };
  const a0 = orbitT(b), tail = 16; g.lineCap = "round"; for (let i = tail; i > 0; i--) { const a = orbitT(b - i * 0.022), q = R * (1 - out); g.strokeStyle = `rgba(255,58,31,${0.42 * (1 - i / tail)})`; g.lineWidth = 44 * (1 - i / tail); g.beginPath(); g.arc(cx, cy, q, a, a + 0.09); g.stroke(); }
  const dr = lerp(40, 1500, eI(r01(b, 55.2, 56))); g.fillStyle = RED; const P = fn(b); g.beginPath(); g.arc(P.x, P.y, dr, 0, 6.3); g.fill();
  g.fillStyle = c1; g.fillRect(40, H - 76, 500, 46); label(g, c2);
}

// ---------- K: handed over. Sheets stacked, prompts sliding, switches flipping
function sentenceK(g, s, b, h, col, y = 340) { const S = 196, L = lay(g, s, S), left = 110, r = S * 0.105, px = left + L.w + S * 0.15; type(g, s, left, y, S, col, { fn: (i) => { const u = r01(b, h + i * 0.018, h + 0.3 + i * 0.018); return u <= 0 ? { a: 0 } : { dy: (1 - back(u)) * 150, sy: 1 + 0.16 * spr((b - h - 0.5) * BEAT, 22, 8) }; } }); return { px, py: y - r, r }; }
function sceneK(g, b) {
  const sec = b < 58 ? 0 : b < 60 ? 1 : 2;
  if (sec === 0) { const i0 = xO(r01(b, 56, 56.5)) * 2400; bg(g, RED); iris(g, W / 2, H / 2, i0, () => { bg(g, BONE);
      const n = Math.floor((b - 56) * 6); for (let k = 0; k < 13; k++) { const t = r01(b, 56.1 + k * 0.13, 56.1 + k * 0.13 + 0.26), yy = lerp(-400, 0, t * t); if (t <= 0) continue; const y = 980 - k * 42 + yy; g.save(); g.translate(1260 + (hash(k) - 0.5) * 34, y); g.transform(1, 0.28, -1.1, 0.28, 0, 0); g.fillStyle = k % 3 === 0 ? COBALT : k % 3 === 1 ? YEL : INK; g.fillRect(-250, -320, 500, 640); g.restore(); }
      for (let k = 0; k < 9; k++) { const u = r01(b, 56.4 + k * 0.08, 56.9 + k * 0.08); } }); }
  if (sec === 1) { bg(g, MINT); const rows = 10, h = H / rows; for (let k = 0; k < rows; k++) { const dir = k % 2 ? 1 : -1, sh = eO(r01(b, 58 + k * 0.04, 58.4 + k * 0.04)), x = (1 - sh) * dir * W + dir * (b - 58) * 60; g.save(); g.translate(x, 0); g.fillStyle = k % 2 ? "#0C8F69" : "#12C490"; g.fillRect(-300, k * h, W + 600, h - 8); mono(g, ">  " + ["describe the task", "check every row", "draft the reply", "flag what's unclear", "summarise the week"][k % 5] + "  ".repeat(3) + ">  keep it plain", 50, k * h + h * 0.68, 40, k % 2 ? "#BDF7E3" : "#075E45", "left", "0"); g.restore(); } }
  if (sec === 2) { bg(g, PINK); const cols = 16, rows = 9, s = W / cols; for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) { const hit = 60 + (Math.hypot(i - 12, j - 3)) * 0.1, on = eIO(r01(b, hit, hit + 0.25)), x = i * s + s / 2, y = j * s + s / 2; g.fillStyle = on > 0.5 ? INK : "#F05CB2"; g.beginPath(); g.roundRect(x - 44, y - 22, 88, 44, 22); g.fill(); g.fillStyle = on > 0.5 ? PINK : "#FFD6EE"; g.beginPath(); g.arc(x + lerp(-22, 22, on), y, 17, 0, 6.3); g.fill(); } }
  const words = ["EVERY FILE", "EVERY PROMPT", "EVERY CONFIG"], cols = [INK, INK, INK];
  if (sec === 1 || sec === 2) { const t = words[sec]; g.fillStyle = sec === 1 ? MINT : PINK; g.fillRect(70, 150, 1720, 240); }
  const Pk = sentenceK(g, words[sec], b, 56 + sec * 2, cols[sec]);
  const pts = [0, 1, 2].map((s) => { const L = lay(g, words[s], 196); return [110 + L.w + 196 * 0.15, 340 - 196 * 0.105]; });
  const K = [[56, W / 2, H / 2], [56.5, pts[0][0], pts[0][1], 200], [57, pts[0][0], pts[0][1], 40], [57.5, pts[0][0], pts[0][1], 40], [58, pts[0][0], pts[0][1], 40], [58.5, pts[1][0], pts[1][1], 300], [59, pts[1][0], pts[1][1], 40], [59.5, pts[1][0], pts[1][1], 40], [60, pts[1][0], pts[1][1], 40], [60.5, pts[2][0], pts[2][1], 300], [61, pts[2][0], pts[2][1], 40], [61.5, pts[2][0], pts[2][1], 40], [62, pts[2][0], pts[2][1], 40]];
  dot(g, (bb) => hop(bb, K), b, 196 * 0.105);
  label(g, "rgba(15,15,18,0.75)");
}

// ---------- L: YOURS. The only time it stops
const Y_S = 480, Y_B = 730;
function layoutY(g) { const s = "YOURS", S = Math.round(fit(g, s, 1490)), L = lay(g, s, S), left = (W - L.w - S * 0.28) / 2, r = S * 0.105; return { s, S, L, left, r, px: left + L.w + S * 0.15, py: 540 + S * 0.35 - r, base: 540 + S * 0.35 }; }
function endPlace(g) { const s = "AI Automation Systems", S = 88, L = lay(g, s, S, 800), left = (W - L.w - 30) / 2; return { s, S, left, px: left + L.w + 24, py: 625 - 11, r: 11 }; }
function sceneL(g, b) {
  bg(g, BONE); const Y = layoutY(g), E = endPlace(g);
  const shake = b < 64.6 ? 0 : 0, kicks = [...TB.letters, 65]; let sh = 0; for (const k of kicks) sh += Math.max(0, spr((b - k) * BEAT, 40, 16)) * (k === 65 ? 26 : 16);
  g.save(); g.translate(sh * (hash(Math.floor(b * 16)) - 0.5) * 2, sh * (hash(Math.floor(b * 16) + 5) - 0.5) * 2);
  if (b < 68.2) type(g, Y.s, Y.left, Y.base, Y.S, INK, { fn: (i, n, cx) => { const h = TB.letters[i], u = r01(b, h, h + 0.14); if (u <= 0) return { a: 0 }; const hit = spr((b - 65) * BEAT - Math.abs(Y.px - cx) / 2600, 20, 4.5) * (b >= 65 ? 0.2 : 0), s0 = lerp(2.4, 1, xO(u)); return { sx: s0 * (1 - hit * 0.3), sy: s0 * (1 + hit) * (1 + 0.1 * spr((b - h) * BEAT, 24, 9)) }; } });
  g.restore();
  if (b >= 67.5) { g.fillStyle = DARK; g.beginPath(); g.arc(Y.px, Y.py, eI(r01(b, 67.5, 68.15)) * 2400, 0, 6.3); g.fill(); }
  const K = [[63.9, W + 120, -220], [65, Y.px, Y.py, 340], [65.5, Y.px, Y.py, 110], [65.75, Y.px, Y.py, 38], [65.875, Y.px, Y.py, 12], [66, Y.px, Y.py, 3], [67.7, Y.px, Y.py], [68.4, E.px, E.py, 120]];
  const rr = lerp(lerp(26, Y.r, r01(b, 64, 65)), E.r, eIO(r01(b, 67.7, 68.4)));
  if (b >= 64) dot(g, (bb) => hop(bb, K), b, rr);
  if (b >= 68) { const v = r01(b, 68, 68.3); }
}
function sceneEnd(g, b) {
  bg(g, DARK); const E = endPlace(g), u = r01(b, TB.card, TB.card + 0.8), a = 1 - r01(b, 74.3, 75);
  g.save(); g.globalAlpha = a;
  const lw = 926 * 0.62, lh = 193 * 0.62; g.globalAlpha = a * eO(u); g.drawImage($("#logo"), W / 2 - lw / 2, 318 - (1 - eO(u)) * 14, lw, lh);
  g.globalAlpha = a * r01(b, 68.6, 69.1); type(g, E.s, E.left, 625, E.S, BONE, { weight: 800 });
  g.globalAlpha = a; g.fillStyle = RED; g.beginPath(); g.arc(E.px, E.py, E.r, 0, 6.3); g.fill();
  g.globalAlpha = a * r01(b, 69.1, 69.7); mono(g, "ai.joaoqueiros.com", W / 2, 696, 28, BONE, "center");
  g.globalAlpha = a * r01(b, 69.5, 70.1); mono(g, "A SERVICE · THIS FILM IS CODE", W / 2, 748, 20, "#9A9486", "center");
  g.restore();
}

// ---------- one frame
function drawAt(g, b) {
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = "source-over"; g.setLineDash([]);
  if (b < 4) { sceneA(g, b); return { mode: 0 }; }
  if (b < 8) { sceneBC(g, b); return { mode: 0 }; }
  if (b < 14) { sceneD(g, b); return { mode: 0 }; }
  if (b < 20) {
    const u = xO(r01(b, 14, 14.5)); if (u >= 1) sceneE(g, b); else { bg(g, RED); iris(g, W / 2, H / 2, u * 1200, () => sceneE(g, b)); }
    return { mode: 0 };
  }
  if (b < 30) { sceneF(g, b); return { mode: 0 }; }
  if (b < 32) { sceneG(g, b); return { mode: 0 }; }
  if (b < 42) return sceneH(g, b) || { mode: 0 };
  if (b < 44) { sceneI(g, b); return { mode: 0 }; }
  if (b < 56) { sceneJ(g, b); return { mode: 0 }; }
  if (b < 62) { sceneK(g, b); return { mode: 0 }; }
  if (b < TB.card) { sceneL(g, b); return { mode: 0 }; }
  sceneEnd(g, b); return { mode: 0, clean: 1 };
}

// ---------- the print: sub-frames added in linear light, then one pass that prints the frame in a chosen process
const VS = `#version 300 es
void main(){ vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2); gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0); }`;
const ACC = `#version 300 es
precision highp float; uniform sampler2D uT; uniform float uN; out vec4 o;
void main(){ vec3 c = texelFetch(uT, ivec2(gl_FragCoord.xy), 0).rgb; o = vec4(pow(c, vec3(2.2)) / uN, 1.0); }`;
const POST = `#version 300 es
precision highp float; uniform sampler2D uC, uAt; uniform int uMode; uniform vec3 uA, uB; uniform float uG, uF, uSplit; out vec4 o;
const vec2 R = vec2(1920.0, 1080.0);
vec3 C(vec2 p, float l){ return pow(max(textureLod(uC, p / R, l).rgb, 0.0), vec3(1.0 / 2.2)); }
float Y(vec3 c){ return dot(c, vec3(0.3, 0.59, 0.11)); }
bool isDot(vec3 c){ return c.r > 0.72 && c.g < 0.48 && c.b < 0.36 && c.r - c.g > 0.42; }
float bayer(ivec2 p){ int m[16] = int[16](0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5); return (float(m[(p.x & 3) + (p.y & 3) * 4]) + 0.5) / 16.0; }
float rnd(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233)) + uF * 0.77) * 43758.5453); }
void main(){
  vec2 p = gl_FragCoord.xy; vec3 src = C(p, 0.0), c = src;
  if (uMode == 1) { float a = 0.5; mat2 m = mat2(cos(a), -sin(a), sin(a), cos(a)); vec2 q = m * p / 15.0, f = fract(q) - 0.5, cell = (floor(q) + 0.5) * 15.0 * m; float l = Y(C(cell, 0.0)); float r = sqrt(max(1.0 - l, 0.0)) * 0.72; c = mix(uA, uB, smoothstep(r - 0.04, r + 0.04, length(f))); }
  if (uMode == 2) { ivec2 q = ivec2(p / 5.0); float l = Y(C((vec2(q) + 0.5) * 5.0, 0.0)); c = l > bayer(q) ? uB : uA; }
  if (uMode == 3) { vec2 cs = vec2(11.0, 19.0), q = floor(p / cs), f = fract(p / cs); float l = Y(C((q + 0.5) * cs, 1.0)); float idx = floor(clamp(l, 0.0, 0.999) * 10.0); float g = texture(uAt, vec2((idx + f.x) / 10.0, f.y)).r; c = mix(uA, uB, clamp(g * (0.25 + 1.3 * l), 0.0, 1.0)); }
  if (uMode == 4) { float wob = sin(p.x * 0.012 + uF * 0.5) * 8.0; float l = Y(src); float v = abs(fract((p.y + wob) / 13.0) - 0.5) * 2.0; c = mix(src * 0.8, src * 1.1, smoothstep(l, l + 0.15, v)); c += (rnd(p) - 0.5) * 0.09; }
  if (uMode == 5) { vec2 cs = vec2(24.0), q = (floor(p / cs) + 0.5) * cs; c = floor(C(q, 0.0) * 6.0 + 0.5) / 6.0; }
  if (uMode == 6) { float a1 = 1.0 - Y(C(p + vec2(7.0, -5.0), 0.0)), a2 = 1.0 - Y(C(p + vec2(-6.0, 4.0), 0.0)); float g1 = step(rnd(p), a1 * 1.05), g2 = step(rnd(p + 9.0), a2 * 0.92); c = vec3(0.98, 0.96, 0.9); c *= mix(vec3(1.0), uA, g1); c *= mix(vec3(1.0), uB, g2); }
  if (uMode == 7) { float e = 0.0; for (int i = 0; i < 4; i++) { vec2 d = vec2(cos(float(i) * 1.57), sin(float(i) * 1.57)) * 3.0; e += abs(Y(C(p + d, 0.0)) - Y(C(p - d, 0.0))); } e = clamp(e, 0.0, 1.0); float gl = 0.0; for (int i = 0; i < 12; i++) { float a = float(i) * 0.5236; vec2 d = vec2(cos(a), sin(a)) * 18.0; for (int j = 0; j < 4; j++) { vec2 dd = d * float(j + 1); float v = 0.0; v += abs(Y(C(p + dd + vec2(3.0, 0.0), 0.0)) - Y(C(p + dd - vec2(3.0, 0.0), 0.0))); gl += v / float(j + 1); } } c = uB + uA * (gl * 0.14) + mix(uA, vec3(1.0), 0.75) * e; }
  if (uMode != 0 && isDot(src)) c = src;
  if (uMode == 0 && uSplit > 0.25) { c.r = mix(c.r, C(p + vec2(uSplit, 0.0), 0.0).r, 0.8); c.b = mix(c.b, C(p - vec2(uSplit, 0.0), 0.0).b, 0.8); }
  c += (rnd(p * 0.5) - 0.5) * uG;
  o = vec4(c, 1.0);
}`;
let gl, scratch, sg, tex, accTex, accFb, PA, PP, atlasTex;
function prog(fs, names) { const mk = (t, s) => { const q = gl.createShader(t); gl.shaderSource(q, s); gl.compileShader(q); if (!gl.getShaderParameter(q, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(q)); return q; }; const p = gl.createProgram(); gl.attachShader(p, mk(gl.VERTEX_SHADER, VS)); gl.attachShader(p, mk(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); const U = {}; names.forEach((n) => (U[n] = gl.getUniformLocation(p, n))); return { p, U }; }
function initGL() {
  scratch = document.createElement("canvas"); scratch.width = W; scratch.height = H; sg = scratch.getContext("2d", { alpha: false });
  gl = $("#stage").getContext("webgl2", { antialias: false, alpha: false, preserveDrawingBuffer: true }); gl.getExtension("EXT_color_buffer_float"); gl.getExtension("OES_texture_float_linear");
  PA = prog(ACC, ["uT", "uN"]); PP = prog(POST, ["uC", "uAt", "uMode", "uA", "uB", "uG", "uF", "uSplit"]);
  gl.bindVertexArray(gl.createVertexArray());
  tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  accTex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, accTex); gl.texStorage2D(gl.TEXTURE_2D, 4, gl.RGBA16F, W, H); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  accFb = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, accFb); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, accTex, 0);
  // the ASCII glyphs, thin to heavy
  const a = document.createElement("canvas"); a.width = 280; a.height = 48; const ag = a.getContext("2d"); ag.fillStyle = "#000"; ag.fillRect(0, 0, 280, 48); ag.fillStyle = "#fff"; ag.font = "700 34px JBM"; ag.textAlign = "center"; ag.textBaseline = "middle"; " .:-=+*#%@".split("").forEach((c, i) => ag.fillText(c, i * 28 + 14, 25));
  atlasTex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, atlasTex); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true); gl.texImage2D(gl.TEXTURE_2D, 0, gl.R8, gl.RED, gl.UNSIGNED_BYTE, a); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
}
function paint(t) {
  if (!gl) return;
  const n = Math.round(t * FPS); let res = { mode: 0 };
  gl.bindFramebuffer(gl.FRAMEBUFFER, accFb); gl.viewport(0, 0, W, H); gl.clearColor(0, 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT);
  gl.useProgram(PA.p); gl.uniform1i(PA.U.uT, 0); const b00 = n / FPS / BEAT, sub = (b00 > 13.3 && b00 < 14) || (b00 > 28.1 && b00 < 29.4) || (b00 > 61.9 && b00 < 64.3) ? 24 : SUB; gl.uniform1f(PA.U.uN, sub); gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  for (let i = 0; i < sub; i++) { const b = (n + (i / sub) * 0.5) / FPS / BEAT; res = drawAt(sg, b) || res; gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE, scratch); gl.drawArrays(gl.TRIANGLES, 0, 3); }
  gl.disable(gl.BLEND); gl.bindTexture(gl.TEXTURE_2D, accTex); gl.generateMipmap(gl.TEXTURE_2D);
  gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, W, H); gl.useProgram(PP.p); gl.uniform1i(PP.U.uC, 0); gl.uniform1i(PP.U.uAt, 1); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, atlasTex); gl.activeTexture(gl.TEXTURE0);
  const b0 = n / FPS / BEAT; let sp = 0; for (const k of [...TB.words, ...TB.letters, ...TB.doubles, 44, 65]) if (b0 >= k) sp = Math.max(sp, 5 * Math.exp(-(b0 - k) * 7));
  gl.uniform1i(PP.U.uMode, res.mode | 0); gl.uniform3fv(PP.U.uA, res.a || [0, 0, 0]); gl.uniform3fv(PP.U.uB, res.b || [1, 1, 1]); gl.uniform1f(PP.U.uG, res.clean ? 0 : 0.022); gl.uniform1f(PP.U.uF, n % 240); gl.uniform1f(PP.U.uSplit, res.clean ? 0 : sp);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
}
const tl = window.__timelines["main"], clock = { t: 0 };
tl.to(clock, { t: DUR, duration: DUR, ease: "none", onUpdate: () => paint(clock.t) }, 0);
async function build() {
  await Promise.all([$("#logo").decode(), document.fonts.load('900 40px "Archivo"'), document.fonts.load('800 40px "Archivo"'), document.fonts.load('600 20px "JBM"'), document.fonts.load('800 40px "JBM"'), document.fonts.load('700 40px "JBM"')]);
  initGL(); window.addEventListener("hf-seek", (ev) => paint(ev.detail.time)); paint(0);
  if (window.__hfForceTimelineRebind) window.__hfForceTimelineRebind();
}
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {}; window.__hf.buildReady["full-stop"] = build();
