// Minimal perspective camera for line/polygon scenes drawn in SVG.
// World: x east, y up, z north (meters).

export type P3 = [number, number, number];
export type Cam = {pos: P3; yaw: number; pitch: number; f: number; cx: number; cy: number; near?: number};

const RAD = Math.PI / 180;

export const toCam = (c: Cam, p: P3): P3 => {
  const sy = Math.sin(c.yaw * RAD);
  const cy = Math.cos(c.yaw * RAD);
  const sp = Math.sin(c.pitch * RAD);
  const cp = Math.cos(c.pitch * RAD);
  const d: P3 = [p[0] - c.pos[0], p[1] - c.pos[1], p[2] - c.pos[2]];
  const right: P3 = [cy, 0, -sy];
  const fwd: P3 = [sy * cp, -sp, cy * cp];
  const up: P3 = [sy * sp, cp, cy * sp];
  const dot = (a: P3, b: P3) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  return [dot(d, right), dot(d, up), dot(d, fwd)];
};

const proj = (c: Cam, q: P3): [number, number] => [c.cx + (c.f * q[0]) / q[2], c.cy - (c.f * q[1]) / q[2]];

// Clip a camera-space polygon to z > near (Sutherland–Hodgman, one plane).
const clipNear = (pts: P3[], near: number): P3[] => {
  const out: P3[] = [];
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i];
    const b = pts[(i + 1) % pts.length];
    const ain = a[2] > near;
    const bin = b[2] > near;
    if (ain) out.push(a);
    if (ain !== bin) {
      const t = (near - a[2]) / (b[2] - a[2]);
      out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, near]);
    }
  }
  return out;
};

export type Face = {pts: string; depth: number};

export const polyPath = (c: Cam, world: P3[]): Face | null => {
  const near = c.near ?? 0.05;
  const cs = clipNear(world.map((p) => toCam(c, p)), near);
  if (cs.length < 3) return null;
  const depth = cs.reduce((s, q) => s + q[2], 0) / cs.length;
  return {pts: 'M' + cs.map((q) => proj(c, q).map((n) => n.toFixed(1)).join(' ')).join(' L') + ' Z', depth};
};

export const linePath = (c: Cam, a: P3, b: P3): {d: string; depth: number} | null => {
  const near = c.near ?? 0.05;
  let p = toCam(c, a);
  let q = toCam(c, b);
  if (p[2] <= near && q[2] <= near) return null;
  if (p[2] <= near || q[2] <= near) {
    const t = (near - p[2]) / (q[2] - p[2]);
    const m: P3 = [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, near];
    if (p[2] <= near) p = m;
    else q = m;
  }
  const [x1, y1] = proj(c, p);
  const [x2, y2] = proj(c, q);
  return {d: `M${x1.toFixed(1)} ${y1.toFixed(1)} L${x2.toFixed(1)} ${y2.toFixed(1)}`, depth: (p[2] + q[2]) / 2};
};

export const projectPoint = (c: Cam, p: P3): {x: number; y: number; z: number} | null => {
  const q = toCam(c, p);
  if (q[2] <= (c.near ?? 0.05)) return null;
  const [x, y] = proj(c, q);
  return {x, y, z: q[2]};
};

// Axis-aligned box as faces (bottom omitted). Returns world-space quads with a face tag.
export type Quad = {pts: P3[]; tag: 'top' | 'n' | 's' | 'e' | 'w'};
export const boxQuads = (x0: number, x1: number, y0: number, y1: number, z0: number, z1: number): Quad[] => [
  {tag: 'top', pts: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]]},
  {tag: 's', pts: [[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0]]},
  {tag: 'n', pts: [[x1, y0, z1], [x0, y0, z1], [x0, y1, z1], [x1, y1, z1]]},
  {tag: 'e', pts: [[x1, y0, z0], [x1, y0, z1], [x1, y1, z1], [x1, y1, z0]]},
  {tag: 'w', pts: [[x0, y0, z1], [x0, y0, z0], [x0, y1, z0], [x0, y1, z1]]},
];

// Box edges as line segments.
export const boxEdges = (x0: number, x1: number, y0: number, y1: number, z0: number, z1: number): [P3, P3][] => {
  const c: P3[] = [
    [x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1],
    [x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1],
  ];
  const e = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  return e.map(([a, b]) => [c[a], c[b]]);
};

export const seeded = (seed: number) => {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
};
