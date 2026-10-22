// Side-view human model for the pictogram athletes.
// Units are meters, x points in the direction the figure faces, y points up.
// Segment lengths follow standard anthropometric ratios for a ~1.75 m adult.

export type V = {x: number; y: number};
export type Leg = {knee: V; ankle: V; heel: V; toe: V};
export type Arm = {elbow: V; wrist: V};
export type Pose = {
  hip: V;
  shoulder: V;
  head: V;
  legN: Leg;
  legF: Leg;
  armN: Arm;
  armF: Arm;
};

export const SEG = {
  thigh: 0.43,
  shank: 0.43,
  trunk: 0.5,
  neck: 0.25,
  upper: 0.3,
  fore: 0.29,
  heel: 0.06,
  toe: 0.18,
  sole: 0.065,
  footR: 0.036,
};

const RAD = Math.PI / 180;
export const v = (x: number, y: number): V => ({x, y});
export const add = (a: V, b: V): V => ({x: a.x + b.x, y: a.y + b.y});
export const sub = (a: V, b: V): V => ({x: a.x - b.x, y: a.y - b.y});
export const mul = (a: V, k: number): V => ({x: a.x * k, y: a.y * k});
export const lerpV = (a: V, b: V, t: number): V => ({x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t});
export const len = (a: V) => Math.hypot(a.x, a.y);

// Direction of a segment hanging from a joint, angle measured from straight down, forward positive.
const down = (deg: number): V => ({x: Math.sin(deg * RAD), y: -Math.cos(deg * RAD)});

const foot = (ankle: V, footDeg: number): Pick<Leg, 'heel' | 'toe'> => {
  const f = {x: Math.cos(footDeg * RAD), y: Math.sin(footDeg * RAD)};
  const n = {x: f.y, y: -f.x}; // toward the sole
  return {
    heel: add(add(ankle, mul(f, -SEG.heel)), mul(n, SEG.sole)),
    toe: add(add(ankle, mul(f, SEG.toe)), mul(n, SEG.sole * 0.75)),
  };
};

export type Angles = {
  lean: number; // trunk forward lean from vertical
  head?: number; // extra head tilt
  thighN: number; // thigh angle from vertical (forward +)
  kneeN: number; // knee flexion
  ankleN: number; // ankle dorsiflexion (+) / plantarflexion (-)
  thighF: number;
  kneeF: number;
  ankleF: number;
  shN: number; // shoulder flexion relative to trunk
  elN: number; // elbow flexion
  shF: number;
  elF: number;
};

const legFK = (hip: V, thigh: number, knee: number, ankle: number): Leg => {
  const k = add(hip, mul(down(thigh), SEG.thigh));
  const shankDeg = thigh - knee;
  const a = add(k, mul(down(shankDeg), SEG.shank));
  return {knee: k, ankle: a, ...foot(a, shankDeg + ankle)};
};

const armFK = (shoulder: V, lean: number, sh: number, el: number): Arm => {
  const upper = -lean + sh;
  const e = add(shoulder, mul(down(upper), SEG.upper));
  return {elbow: e, wrist: add(e, mul(down(upper + el), SEG.fore))};
};

const torso = (hip: V, lean: number, head = 0) => {
  const shoulder = add(hip, {x: Math.sin(lean * RAD) * SEG.trunk, y: Math.cos(lean * RAD) * SEG.trunk});
  const h = add(shoulder, {x: Math.sin((lean + head) * RAD) * SEG.neck, y: Math.cos((lean + head) * RAD) * SEG.neck});
  return {shoulder, head: h};
};

export const fk = (a: Angles, hip: V = v(0, 0)): Pose => {
  const {shoulder, head} = torso(hip, a.lean, a.head);
  return {
    hip,
    shoulder,
    head,
    legN: legFK(hip, a.thighN, a.kneeN, a.ankleN),
    legF: legFK(hip, a.thighF, a.kneeF, a.ankleF),
    armN: armFK(shoulder, a.lean, a.shN, a.elN),
    armF: armFK(shoulder, a.lean, a.shF, a.elF),
  };
};

// Two-bone IK. `bend` = +1 puts the middle joint forward (knee), -1 backward (elbow).
export const ik2 = (root: V, target: V, l1: number, l2: number, bend: 1 | -1): {mid: V; end: V} => {
  const d0 = sub(target, root);
  const dist = Math.min(Math.max(len(d0), Math.abs(l1 - l2) + 1e-4), l1 + l2 - 1e-4);
  const u = mul(d0, 1 / (len(d0) || 1));
  const a = Math.acos((l1 * l1 + dist * dist - l2 * l2) / (2 * l1 * dist)) * bend;
  const r = {x: u.x * Math.cos(a) - u.y * Math.sin(a), y: u.x * Math.sin(a) + u.y * Math.cos(a)};
  const mid = add(root, mul(r, l1));
  const end = add(mid, mul(sub(target, mid), l2 / (len(sub(target, mid)) || 1)));
  return {mid, end};
};

export type LegTarget = {ankle: V; foot: number}; // foot = absolute foot angle (0 = flat, + toes up)
export type ArmSpec = {sh: number; el: number} | {hand: V};

export type IKSpec = {
  hip: V;
  lean: number;
  head?: number;
  legN: LegTarget;
  legF: LegTarget;
  armN: ArmSpec;
  armF: ArmSpec;
};

const legIK = (hip: V, t: LegTarget): Leg => {
  const {mid, end} = ik2(hip, t.ankle, SEG.thigh, SEG.shank, 1);
  return {knee: mid, ankle: end, ...foot(end, t.foot)};
};

const armIK = (shoulder: V, lean: number, s: ArmSpec): Arm => {
  if ('hand' in s) {
    const {mid, end} = ik2(shoulder, s.hand, SEG.upper, SEG.fore, -1);
    return {elbow: mid, wrist: end};
  }
  return armFK(shoulder, lean, s.sh, s.el);
};

export const ikPose = (s: IKSpec): Pose => {
  const {shoulder, head} = torso(s.hip, s.lean, s.head);
  return {
    hip: s.hip,
    shoulder,
    head,
    legN: legIK(s.hip, s.legN),
    legF: legIK(s.hip, s.legF),
    armN: armIK(shoulder, s.lean, s.armN),
    armF: armIK(shoulder, s.lean, s.armF),
  };
};

const mapPose = (p: Pose, f: (q: V) => V): Pose => ({
  hip: f(p.hip),
  shoulder: f(p.shoulder),
  head: f(p.head),
  legN: {knee: f(p.legN.knee), ankle: f(p.legN.ankle), heel: f(p.legN.heel), toe: f(p.legN.toe)},
  legF: {knee: f(p.legF.knee), ankle: f(p.legF.ankle), heel: f(p.legF.heel), toe: f(p.legF.toe)},
  armN: {elbow: f(p.armN.elbow), wrist: f(p.armN.wrist)},
  armF: {elbow: f(p.armF.elbow), wrist: f(p.armF.wrist)},
});

export const translate = (p: Pose, d: V) => mapPose(p, (q) => add(q, d));
export const mirror = (p: Pose) => mapPose(p, (q) => ({x: -q.x, y: q.y}));

export const blend = (a: Pose, b: Pose, t: number): Pose => {
  const pts = (p: Pose) => [
    p.hip, p.shoulder, p.head,
    p.legN.knee, p.legN.ankle, p.legN.heel, p.legN.toe,
    p.legF.knee, p.legF.ankle, p.legF.heel, p.legF.toe,
    p.armN.elbow, p.armN.wrist, p.armF.elbow, p.armF.wrist,
  ];
  const pa = pts(a);
  const pb = pts(b);
  let i = 0;
  return mapPose(a, () => {
    const r = lerpV(pa[i], pb[i], t);
    i++;
    return r;
  });
};

export const lowest = (l: Leg) => Math.min(l.heel.y, l.toe.y) - SEG.footR;

// Interior knee flexion angle in degrees (0 = straight).
export const kneeFlexion = (hip: V, l: Leg) => {
  const a = sub(l.knee, hip);
  const b = sub(l.ankle, l.knee);
  const c = (a.x * b.x + a.y * b.y) / (len(a) * len(b));
  return Math.acos(Math.max(-1, Math.min(1, c))) / RAD;
};

// ---------- periodic keyframe tables ----------

export type Table = [number, number][];

// Periodic Catmull-Rom through (phase, value) keys, phase in [0,1).
export const sampleTable = (t: Table, phase: number) => {
  const p = ((phase % 1) + 1) % 1;
  const n = t.length;
  let i = n - 1;
  for (let k = 0; k < n; k++) {
    if (t[k][0] <= p) i = k;
  }
  const at = (k: number) => {
    const idx = ((k % n) + n) % n;
    const wrap = Math.floor(k / n);
    return [t[idx][0] + wrap, t[idx][1]] as const;
  };
  const [x0, y0] = at(i - 1);
  const [x1, y1] = at(i);
  const [x2, y2] = at(i + 1);
  const [x3, y3] = at(i + 2);
  const pp = p < x1 ? p + 1 : p;
  const u = (pp - x1) / (x2 - x1);
  const m1 = ((y2 - y0) / (x2 - x0)) * (x2 - x1);
  const m2 = ((y3 - y1) / (x3 - x1)) * (x2 - x1);
  const u2 = u * u;
  const u3 = u2 * u;
  return (2 * u3 - 3 * u2 + 1) * y1 + (u3 - 2 * u2 + u) * m1 + (-2 * u3 + 3 * u2) * y2 + (u3 - u2) * m2;
};
