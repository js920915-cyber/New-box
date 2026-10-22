// Exercise and test movements for the pictogram athletes.
// Ranges are typical textbook values (e.g. deep goblet squat knee flexion ~110°,
// CMJ flight 0.5 s ≈ 31 cm), used here for illustration rather than as clinical norms.
import {add, Angles, fk, ikPose, lowest, mul, Pose, SEG, translate, v, V} from './body';
import {clamp, lerp, spline} from './util';
import {gaitPose, gaitSpeed, Gait} from './gaits';

export const G = 9.81;

// Translate a pose so the chosen foot's lowest point is on y = 0 and its ankle is at x.
export const plant = (p: Pose, x = 0, leg: 'N' | 'F' = 'N') => {
  const l = leg === 'N' ? p.legN : p.legF;
  return translate(p, v(x - l.ankle.x, -lowest(l)));
};

export const STAND: Angles = {lean: 2, head: 0, thighN: 2, kneeN: 4, ankleN: 2, thighF: -1, kneeF: 3, ankleF: 2, shN: 6, elN: 12, shF: -4, elF: 10};

export const standPose = (over: Partial<Angles> = {}) => plant(fk({...STAND, ...over}));

// Goblet squat, depth 0..1; hands hold a weight at the chest.
export const squatPose = (d: number): {pose: Pose; weight: V} => {
  const knee = 4 + 108 * d;
  const ank = 2 + 30 * d;
  const lean = 6 + 30 * d;
  const thigh = knee - ank;
  const base = fk({lean, head: -lean * 0.4, thighN: thigh, kneeN: knee, ankleN: ank, thighF: thigh - 2, kneeF: knee, ankleF: ank, shN: 0, elN: 0, shF: 0, elF: 0});
  const p0 = plant(base);
  const chest = add(p0.shoulder, add(mul(v(Math.sin((lean * Math.PI) / 180), Math.cos((lean * Math.PI) / 180)), -0.2), v(0.2, 0)));
  const pose = ikPose({
    hip: p0.hip,
    lean,
    head: -lean * 0.4,
    legN: {ankle: p0.legN.ankle, foot: 0},
    legF: {ankle: p0.legF.ankle, foot: 0},
    armN: {hand: chest},
    armF: {hand: add(chest, v(-0.03, 0.01))},
  });
  return {pose, weight: add(chest, v(0.05, -0.04))};
};

// Single-leg Romanian deadlift on the near leg, hinge 0..1.
export const sldlPose = (h: number): Pose => {
  const lean = 82 * h;
  const knee = 8 + 14 * h;
  const ank = 4 + 8 * h;
  const p = fk({
    lean,
    head: -lean * 0.15,
    thighN: knee - ank,
    kneeN: knee,
    ankleN: ank,
    thighF: lerp(-2, -lean * 0.97, h) + (1 - h) * 6,
    kneeF: lerp(18, 6, h),
    ankleF: lerp(-10, -5, h),
    shN: lean,
    elN: 6,
    shF: lean - 4,
    elF: 8,
  });
  return plant(p);
};

// ---------- jumps: quintic segments so the derived ground reaction force is smooth ----------

type Seg = {t0: number; t1: number; p0: number; v0: number; a0: number; p1: number; v1: number; a1: number};
const quintic = (s: Seg, t: number) => {
  const T = s.t1 - s.t0;
  const u = clamp((t - s.t0) / T);
  const P0 = s.p0;
  const V0 = s.v0 * T;
  const A0 = s.a0 * T * T;
  const P1 = s.p1;
  const V1 = s.v1 * T;
  const A1 = s.a1 * T * T;
  const c3 = 10 * (P1 - P0) - 6 * V0 - 4 * V1 - 1.5 * A0 + 0.5 * A1;
  const c4 = -15 * (P1 - P0) + 8 * V0 + 7 * V1 + 1.5 * A0 - A1;
  const c5 = 6 * (P1 - P0) - 3 * V0 - 3 * V1 - 0.5 * A0 + 0.5 * A1;
  return P0 + V0 * u + 0.5 * A0 * u * u + c3 * u ** 3 + c4 * u ** 4 + c5 * u ** 5;
};

export const CMJ = {
  start: 0.35,
  bottom: 0.85,
  takeoff: 1.15,
  land: 1.65,
  absorbed: 1.92,
  end: 2.7,
  depth: 0.3,
  rise: 0.06,
};
const V0 = (G * (CMJ.land - CMJ.takeoff)) / 2;

const SEGS: Seg[] = [
  {t0: CMJ.start, t1: CMJ.bottom, p0: 0, v0: 0, a0: 0, p1: -CMJ.depth, v1: 0, a1: 1.3 * G},
  {t0: CMJ.bottom, t1: CMJ.takeoff, p0: -CMJ.depth, v0: 0, a0: 1.3 * G, p1: CMJ.rise, v1: V0, a1: -G},
  {t0: CMJ.land, t1: CMJ.absorbed, p0: CMJ.rise, v0: -V0, a0: -G, p1: -0.26, v1: 0, a1: 0.3 * G},
  {t0: CMJ.absorbed, t1: CMJ.end, p0: -0.26, v0: 0, a0: 0.3 * G, p1: 0, v1: 0, a1: 0},
];

// Vertical hip displacement relative to quiet standing (m).
export const cmjHeight = (t: number) => {
  if (t <= CMJ.start) return 0;
  if (t >= CMJ.takeoff && t <= CMJ.land) {
    const tau = t - CMJ.takeoff;
    return CMJ.rise + V0 * tau - 0.5 * G * tau * tau;
  }
  const s = SEGS.find((g) => t >= g.t0 && t <= g.t1);
  return s ? quintic(s, t) : 0;
};

// Vertical ground reaction force in body weights (derived from the hip trajectory).
export const cmjForce = (t: number) => {
  if (t > CMJ.takeoff && t < CMJ.land) return 0;
  const h = 1 / 240;
  const a = (cmjHeight(t + h) - 2 * cmjHeight(t) + cmjHeight(t - h)) / (h * h);
  return Math.max(0, 1 + a / G);
};
export const cmjJumpHeight = (G * (CMJ.land - CMJ.takeoff) ** 2) / 8;

const STAND_HIP = standPose().hip;

// Countermovement jump (also used for hurdle hops with `forward` metres of travel).
export const cmjPose = (t: number, forward = 0): Pose => {
  const y = cmjHeight(t);
  const depth = clamp(-y / CMJ.depth);
  const air = t > CMJ.takeoff && t < CMJ.land;
  const airU = clamp((t - CMJ.takeoff) / (CMJ.land - CMJ.takeoff));
  const travel = forward * (t <= CMJ.takeoff ? 0 : t >= CMJ.land ? 1 : airU);
  const lean = spline([[0, 2], [CMJ.start, 2], [CMJ.bottom, 36], [CMJ.takeoff, 4], [CMJ.land - 0.1, 8], [CMJ.absorbed, 30], [CMJ.end, 3]], t);
  const sh = spline([[0, 6], [CMJ.start, 6], [CMJ.bottom, -55], [CMJ.takeoff, 150], [CMJ.land - 0.15, 70], [CMJ.absorbed, 35], [CMJ.end, 6]], t);
  const el = spline([[0, 12], [CMJ.bottom, 20], [CMJ.takeoff, 14], [CMJ.absorbed, 40], [CMJ.end, 12]], t);
  const plantar = spline([[0, 0], [CMJ.bottom + 0.12, 0], [CMJ.takeoff, -38], [CMJ.land - 0.08, -24], [CMJ.land + 0.07, 0], [CMJ.end, 0]], t);
  const hipY = STAND_HIP.y + y;
  const hipX = STAND_HIP.x - 0.13 * depth + travel;
  if (!air) {
    const toeX = 0.18 + (t >= CMJ.land ? forward : 0);
    const r = (plantar * Math.PI) / 180;
    const f = v(Math.cos(r), Math.sin(r));
    const n = v(f.y, -f.x);
    const toe = v(toeX, SEG.footR + SEG.sole - SEG.sole * 0.75);
    const ankle = add(add(toe, mul(f, -SEG.toe)), mul(n, -SEG.sole * 0.75));
    return ikPose({
      hip: v(hipX, hipY),
      lean,
      head: -lean * 0.35,
      legN: {ankle, foot: plantar},
      legF: {ankle: add(ankle, v(-0.02, 0)), foot: plantar},
      armN: {sh, el},
      armF: {sh: sh - 6, el: el + 4},
    });
  }
  const tuck = Math.sin(Math.PI * airU);
  const thigh = 6 + 26 * tuck * (forward > 0 ? 1 : 0.5);
  const knee = 8 + 40 * tuck * (forward > 0 ? 1 : 0.4) + 12 * airU;
  const p = fk(
    {lean, head: -lean * 0.3, thighN: thigh, kneeN: knee, ankleN: plantar + 6, thighF: thigh - 3, kneeF: knee, ankleF: plantar + 6, shN: sh, elN: el, shF: sh - 6, elF: el + 4},
    v(hipX, hipY),
  );
  return p;
};

// ---------- cutting: approach run, plant, 180° turn, re-acceleration ----------

export const CUT = {plant: 1.05, turn0: 1.32, turn1: 1.58, end: 2.6};

// Returns pose (in facing-local coordinates), world hip x, and facing scale (cos of turn angle).
export const cutState = (t: number, gait: Gait): {pose: Pose; x: number; turn: number} => {
  // distance travelled (m): decelerate into the plant, accelerate out
  const xIn = (tt: number) => -5.2 + 5.2 * (1 - Math.pow(1 - clamp(tt / CUT.plant), 2.2));
  const xOut = (tt: number) => -0.9 * Math.pow(clamp((tt - CUT.turn1) / (CUT.end - CUT.turn1)), 1.7) * 4.2;
  const plantPose = plant(
    fk({lean: -16, head: 12, thighN: 42, kneeN: 62, ankleN: 16, thighF: -16, kneeF: 48, ankleF: -8, shN: 55, elN: 60, shF: -45, elF: 55}),
    0.25,
  );
  if (t < CUT.plant) {
    const dist = xIn(t) + 5.2;
    const run = gaitPose(gait, dist / (gaitSpeed(gait) * gait.period));
    const k = clamp((t - (CUT.plant - 0.16)) / 0.16);
    const hipX = xIn(t);
    return {pose: k > 0 ? blendPoses(run, translate(plantPose, v(-plantPose.hip.x, 0)), k) : run, x: hipX, turn: 1};
  }
  if (t < CUT.turn1) {
    const turn = Math.cos(Math.PI * clamp((t - CUT.turn0) / (CUT.turn1 - CUT.turn0)));
    return {pose: translate(plantPose, v(-plantPose.hip.x, 0)), x: 0, turn};
  }
  const out = clamp((t - CUT.turn1) / 0.18);
  const dist = -xOut(t);
  const run = gaitPose(gait, 0.55 + dist / (gaitSpeed(gait) * gait.period));
  const drive = fk({lean: 24, head: -10, thighN: 44, kneeN: 70, ankleN: 4, thighF: -22, kneeF: 20, ankleF: -18, shN: -40, elN: 90, shF: 50, elF: 80});
  const driveP = plant(drive, 0, 'F');
  return {pose: out < 1 ? blendPoses(translate(driveP, v(-driveP.hip.x, 0)), run, out) : run, x: xOut(t), turn: -1};
};

const blendPoses = (a: Pose, b: Pose, k: number): Pose => {
  const L = (p: V, q: V) => v(lerp(p.x, q.x, k), lerp(p.y, q.y, k));
  return {
    hip: L(a.hip, b.hip),
    shoulder: L(a.shoulder, b.shoulder),
    head: L(a.head, b.head),
    legN: {knee: L(a.legN.knee, b.legN.knee), ankle: L(a.legN.ankle, b.legN.ankle), heel: L(a.legN.heel, b.legN.heel), toe: L(a.legN.toe, b.legN.toe)},
    legF: {knee: L(a.legF.knee, b.legF.knee), ankle: L(a.legF.ankle, b.legF.ankle), heel: L(a.legF.heel, b.legF.heel), toe: L(a.legF.toe, b.legF.toe)},
    armN: {elbow: L(a.armN.elbow, b.armN.elbow), wrist: L(a.armN.wrist, b.armN.wrist)},
    armF: {elbow: L(a.armF.elbow, b.armF.elbow), wrist: L(a.armF.wrist, b.armF.wrist)},
  };
};
export {blendPoses};

// ---------- clinic poses ----------

// Seated on a plinth (top at y = seatY), knee at 90°, pushing into a handheld dynamometer.
export const seatedPose = (seatY: number, effort: number): Pose =>
  fk(
    {lean: -4 - 6 * effort, head: 4, thighN: 88, kneeN: 88 - 4 * effort, ankleN: 4, thighF: 86, kneeF: 92, ankleF: 4, shN: -12, elN: 8, shF: -16, elF: 10},
    v(0, seatY + 0.09),
  );

// Standing therapist reaching both hands to a target (e.g. holding a device).
export const reachPose = (hand: V, stanceX: number): Pose => {
  const base = fk({lean: 32, head: -12, thighN: 28, kneeN: 40, ankleN: 14, thighF: -14, kneeF: 22, ankleF: 2, shN: 60, elN: 30, shF: 60, elF: 30});
  const p = plant(base, stanceX);
  return ikPose({
    hip: p.hip,
    lean: 32,
    head: -14,
    legN: {ankle: p.legN.ankle, foot: 0},
    legF: {ankle: p.legF.ankle, foot: 0},
    armN: {hand},
    armF: {hand: add(hand, v(-0.04, 0.05))},
  });
};

// Standing with one arm pointing (sh ≈ shoulder flexion of the pointing arm).
export const pointPose = (sh: number, wave = 0): Pose =>
  standPose({shN: sh, elN: 8 + wave * 10, shF: -2, elF: 14, lean: 0, head: -4});

// Observing/cueing: one hand raised in front.
export const cuePose = (k: number): Pose => standPose({shN: 35 + 25 * k, elN: 70 - 30 * k, shF: 0, elF: 20, lean: 4, head: -6});

// Hand on the knee (hesitating after a few steps).
export const kneeHoldPose = (): Pose => {
  const base = plant(fk({lean: 34, head: -26, thighN: 20, kneeN: 30, ankleN: 12, thighF: -6, kneeF: 8, ankleF: 4, shN: 0, elN: 0, shF: 0, elF: 0}));
  return ikPose({
    hip: base.hip,
    lean: 34,
    head: -26,
    legN: {ankle: base.legN.ankle, foot: 0},
    legF: {ankle: base.legF.ankle, foot: 0},
    armN: {hand: add(base.legN.knee, v(0.04, 0.06))},
    armF: {hand: add(base.legN.knee, v(-0.02, 0.12))},
  });
};

// Half-kneeling tester (far knee on the floor) reaching both hands to `hand` (local coords, facing +x).
export const kneelReachPose = (hand: V): Pose => {
  const hip = v(0, 0.55);
  const lean = 40;
  const base = fk({lean, head: -18, thighN: 84, kneeN: 86, ankleN: 4, thighF: 0, kneeF: 96, ankleF: 0, shN: 70, elN: 20, shF: 70, elF: 20}, hip);
  return ikPose({
    hip,
    lean,
    head: -18,
    legN: {ankle: base.legN.ankle, foot: 0},
    legF: {ankle: base.legF.ankle, foot: -96},
    armN: {hand},
    armF: {hand: add(hand, v(-0.03, 0.04))},
  });
};
