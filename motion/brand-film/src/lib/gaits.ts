// Cyclic movement generators built on body.ts.
// Joint-angle curves are approximations of published sagittal-plane gait data
// (running ~3.5 m/s: knee ~20° at contact, ~40-45° mid-stance, ~100° mid-swing;
// walking: knee ~5° at contact, ~15-20° loading, ~60° peak swing).

import {Angles, fk, ikPose, lowest, Pose, SEG, Table, sampleTable, translate, v, V} from './body';

export type Gait = {
  thigh: Table;
  knee: Table;
  ankle: Table;
  stance: number; // fraction of the cycle a foot is on the ground
  period: number; // seconds per stride (two steps)
  lean: number;
  shoulder: number; // arm swing amplitude relative to thigh swing
  elbow: [number, number]; // elbow flexion mean, swing
};

export const RUN: Gait = {
  thigh: [[0, 24], [0.12, 8], [0.25, -8], [0.36, -20], [0.45, -16], [0.62, 12], [0.8, 38], [0.9, 34], [0.96, 28]],
  knee: [[0, 20], [0.13, 44], [0.26, 30], [0.36, 14], [0.5, 70], [0.62, 104], [0.78, 70], [0.9, 24], [0.96, 16]],
  ankle: [[0, 4], [0.14, 20], [0.26, 8], [0.36, -22], [0.48, -12], [0.7, 4], [0.88, 8], [0.96, 6]],
  stance: 0.36,
  period: 0.7,
  lean: 9,
  shoulder: 1.05,
  elbow: [88, 12],
};

export const JOG: Gait = {
  ...RUN,
  thigh: [[0, 20], [0.12, 6], [0.26, -8], [0.4, -16], [0.5, -10], [0.66, 12], [0.82, 28], [0.92, 26]],
  knee: [[0, 16], [0.14, 38], [0.28, 26], [0.4, 14], [0.54, 60], [0.66, 86], [0.82, 50], [0.94, 18]],
  stance: 0.4,
  period: 0.76,
  lean: 6,
  shoulder: 0.9,
};

export const WALK: Gait = {
  thigh: [[0, 25], [0.15, 18], [0.35, 0], [0.5, -10], [0.6, -8], [0.72, 10], [0.86, 26], [0.94, 26]],
  knee: [[0, 5], [0.12, 17], [0.3, 7], [0.45, 6], [0.6, 38], [0.72, 60], [0.84, 32], [0.95, 6]],
  ankle: [[0, 0], [0.08, -5], [0.3, 6], [0.48, 11], [0.6, -14], [0.7, -8], [0.82, 0], [0.95, 2]],
  stance: 0.62,
  period: 1.08,
  lean: 3,
  shoulder: 0.55,
  elbow: [18, 8],
};

const anglesAt = (g: Gait, phase: number): Angles => {
  const tN = sampleTable(g.thigh, phase);
  const tF = sampleTable(g.thigh, phase + 0.5);
  const mean = (g.thigh.reduce((s, k) => s + k[1], 0) / g.thigh.length);
  const elbowWave = Math.sin(2 * Math.PI * phase);
  return {
    lean: g.lean + Math.cos(4 * Math.PI * phase) * 1.2,
    head: -g.lean * 0.6,
    thighN: tN,
    kneeN: sampleTable(g.knee, phase),
    ankleN: sampleTable(g.ankle, phase),
    thighF: tF,
    kneeF: sampleTable(g.knee, phase + 0.5),
    ankleF: sampleTable(g.ankle, phase + 0.5),
    // arms swing opposite to the same-side leg
    shN: -(tN - mean) * g.shoulder + g.lean * 0.6,
    elN: g.elbow[0] + elbowWave * g.elbow[1],
    shF: -(tF - mean) * g.shoulder + g.lean * 0.6,
    elF: g.elbow[0] - elbowWave * g.elbow[1],
  };
};

type Cycle = {heights: number[]; speed: number; samples: number};
const cache = new Map<Gait, Cycle>();

// Pin the stance foot to the ground, fill flight phases ballistically,
// and measure the ground speed that keeps the planted foot from sliding.
const cycle = (g: Gait): Cycle => {
  const hit = cache.get(g);
  if (hit) return hit;
  const N = 240;
  const raw: (number | null)[] = [];
  for (let i = 0; i < N; i++) {
    const p = i / N;
    const pose = fk(anglesAt(g, p));
    const inN = p < g.stance;
    const inF = ((p + 0.5) % 1) < g.stance;
    if (!inN && !inF) {
      raw.push(null);
      continue;
    }
    const need = Math.max(inN ? -lowest(pose.legN) : -Infinity, inF ? -lowest(pose.legF) : -Infinity);
    raw.push(need);
  }
  const heights = raw.slice() as number[];
  for (let i = 0; i < N; i++) {
    if (raw[i] !== null) continue;
    let a = i;
    while (raw[(a - 1 + N) % N] === null) a--;
    let b = i;
    while (raw[(b + 1) % N] === null) b++;
    const h0 = raw[(a - 1 + N) % N] as number;
    const h1 = raw[(b + 1) % N] as number;
    const span = b - a + 2;
    const k = i - a + 1;
    const t1 = (k / N) * g.period;
    const t2 = ((span - k) / N) * g.period;
    heights[i] = h0 + ((h1 - h0) * k) / span + 0.5 * 9.81 * t1 * t2;
  }
  const a0 = fk(anglesAt(g, g.stance * 0.2)).legN.ankle.x;
  const a1 = fk(anglesAt(g, g.stance * 0.8)).legN.ankle.x;
  const speed = (a0 - a1) / (g.stance * 0.6 * g.period);
  const c = {heights, speed, samples: N};
  cache.set(g, c);
  return c;
};

export const gaitSpeed = (g: Gait) => cycle(g).speed;

// Pose at a cycle phase with the lowest foot on y = 0 and the hip at x = 0.
export const gaitPose = (g: Gait, phase: number): Pose => {
  const c = cycle(g);
  const p = ((phase % 1) + 1) % 1;
  const f = p * c.samples;
  const i = Math.floor(f);
  const h = c.heights[i % c.samples] * (1 - (f - i)) + c.heights[(i + 1) % c.samples] * (f - i);
  return fk(anglesAt(g, p), v(0, h));
};

// ---------- stairs (inverse kinematics) ----------

export const STAIR = {rise: 0.17, run: 0.29};

const smooth = (t: number) => t * t * (3 - 2 * t);

// Step-over-step stair ascent. Returns the pose in stair coordinates
// (step k's tread spans x in [k*run, (k+1)*run] at height k*rise).
export const stairPose = (t: number, period = 1.1, armToRail = true): Pose => {
  const cyc = t / period; // one cycle = two steps
  const footAt = (c: number, side: 0 | 1): {ankle: V; foot: number} => {
    // foot `side` lands on step 2n+side at cycle n + side/2
    const local = c - side / 2;
    const n = Math.floor(local);
    const ph = local - n;
    const stepIdx = (k: number) => 2 * k + side;
    const place = (k: number) => v(stepIdx(k) * STAIR.run + 0.12, stepIdx(k) * STAIR.rise + SEG.sole + SEG.footR);
    const swingStart = 0.56;
    if (ph < swingStart) {
      // stance: heel lifts late in stance
      const roll = Math.max(0, (ph - 0.38) / (swingStart - 0.38));
      const base = place(n);
      return {ankle: v(base.x + roll * 0.05, base.y + roll * 0.1), foot: -roll * 28};
    }
    const s = smooth((ph - swingStart) / (1 - swingStart));
    const a = place(n);
    const b = place(n + 1);
    const lift = Math.sin(Math.PI * s) * 0.16;
    return {ankle: v(a.x + (b.x - a.x) * s, a.y + (b.y - a.y) * s + lift), foot: -22 * (1 - s) + 8 * Math.sin(Math.PI * s)};
  };
  const nL = footAt(cyc, 0);
  const fL = footAt(cyc, 1);
  const slope = STAIR.rise / STAIR.run;
  const hx = cyc * 2 * STAIR.run + 0.02;
  const hy = hx * slope + 0.79 + Math.cos(cyc * 4 * Math.PI) * 0.015;
  const hip = v(hx, hy);
  const lean = 12 + Math.sin(cyc * 4 * Math.PI) * 2;
  const railHand = v(hx + 0.3, (hx + 0.3) * slope + 0.9);
  return ikPose({
    hip,
    lean,
    head: -6,
    legN: nL,
    legF: fL,
    armN: armToRail ? {hand: railHand} : {sh: 18 * Math.sin(cyc * 2 * Math.PI), el: 25},
    armF: {sh: -18 * Math.sin(cyc * 2 * Math.PI) + 4, el: 25},
  });
};

export const placeOnGround = (p: Pose, x: number, y = 0) => translate(p, v(x, y));
