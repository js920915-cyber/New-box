// Procedural Magok/Seoul city fabric (local meters, x east, z north).
// The same rules drive the flat map texture in scene 2 and the extruded 3D blocks in scene 3,
// so the hand-off between the two scenes lines up block for block.
import {seeded} from './cam3d';
import {riverDistance} from './seoul';

export const TILE = 1500;
export const VARIANTS = [
  {rot: -28, pitch: 170},
  {rot: -12, pitch: 140},
  {rot: 6, pitch: 190},
  {rot: 18, pitch: 155},
];
export const STREET = 34;

const hash = (i: number, j: number) => {
  let h = (i * 374761393 + j * 668265263) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return (h ^ (h >>> 16)) >>> 0;
};

export type Tile = {i: number; j: number; v: number; poly: [number, number][]};

// Slightly jittered tile corners so district edges are not a perfect grid.
const corner = (i: number, j: number): [number, number] => {
  const h = hash(i * 7 + 3, j * 11 + 5);
  return [i * TILE + ((h % 300) - 150), j * TILE + (((h >>> 9) % 300) - 150)];
};

export const tilesAround = (cx: number, cz: number, radius: number): Tile[] => {
  const out: Tile[] = [];
  const i0 = Math.floor((cx - radius) / TILE);
  const i1 = Math.floor((cx + radius) / TILE);
  const j0 = Math.floor((cz - radius) / TILE);
  const j1 = Math.floor((cz + radius) / TILE);
  for (let i = i0; i <= i1; i++) {
    for (let j = j0; j <= j1; j++) {
      const g = STREET * 0.9;
      const a = corner(i, j);
      const b = corner(i + 1, j);
      const c = corner(i + 1, j + 1);
      const d = corner(i, j + 1);
      out.push({
        i,
        j,
        v: hash(i, j) % VARIANTS.length,
        poly: [
          [a[0] + g, a[1] + g],
          [b[0] - g, b[1] + g],
          [c[0] - g, c[1] - g],
          [d[0] + g, d[1] - g],
        ],
      });
    }
  }
  return out;
};

// Building footprints inside one pattern repeat (2×2 cells), in cell space (meters).
// Shared by the SVG <pattern> (scene 2) and the explicit 3D blocks (scene 3).
export const cellBuildings = (pitch: number): {u0: number; v0: number; u1: number; v1: number; k: number}[] => {
  const s = STREET / 2;
  const p = pitch;
  const m = p / 2;
  return [
    {u0: s, v0: s, u1: p - s, v1: p - s, k: 0},
    {u0: p + s, v0: s, u1: p + m - 6, v1: p - s, k: 1},
    {u0: p + m + 6, v0: s, u1: 2 * p - s, v1: p - s, k: 2},
    {u0: s + 10, v0: p + s + 10, u1: p - s - 10, v1: 2 * p - s - 10, k: 3},
    {u0: p + s, v0: p + s, u1: 2 * p - s, v1: p + m - 6, k: 4},
    {u0: p + s, v0: p + m + 6, u1: 2 * p - s, v1: 2 * p - s, k: 5},
  ];
};

const inside = (poly: [number, number][], x: number, z: number) => {
  let c = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, zi] = poly[i];
    const [xj, zj] = poly[j];
    if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) c = !c;
  }
  return c;
};

export type Block = {pts: [number, number][]; cx: number; cz: number; h: number; tile: number};

export const CLEAR_RADIUS = 150; // plaza around the center's building

// Explicit blocks (world footprints + heights) within `radius` of (cx, cz).
export const blocksAround = (cx: number, cz: number, radius: number): Block[] => {
  const out: Block[] = [];
  for (const t of tilesAround(cx, cz, radius)) {
    const {rot, pitch} = VARIANTS[t.v];
    const r = (rot * Math.PI) / 180;
    const cs = Math.cos(r);
    const sn = Math.sin(r);
    const toW = (u: number, v: number): [number, number] => [cs * u - sn * v, sn * u + cs * v];
    const toC = (x: number, z: number): [number, number] => [cs * x + sn * z, -sn * x + cs * z];
    const xs = t.poly.map((p) => toC(p[0], p[1]));
    const uMin = Math.min(...xs.map((p) => p[0]));
    const uMax = Math.max(...xs.map((p) => p[0]));
    const vMin = Math.min(...xs.map((p) => p[1]));
    const vMax = Math.max(...xs.map((p) => p[1]));
    const rep = 2 * pitch;
    const rnd = seeded(hash(t.i + 1000, t.j + 2000));
    for (let a = Math.floor(uMin / rep); a <= Math.floor(uMax / rep); a++) {
      for (let b = Math.floor(vMin / rep); b <= Math.floor(vMax / rep); b++) {
        for (const c of cellBuildings(pitch)) {
          const h = 14 + Math.pow(rnd(), 1.6) * 70;
          const u0 = a * rep + c.u0;
          const u1 = a * rep + c.u1;
          const v0 = b * rep + c.v0;
          const v1 = b * rep + c.v1;
          const pts = [toW(u0, v0), toW(u1, v0), toW(u1, v1), toW(u0, v1)];
          const [mx, mz] = toW((u0 + u1) / 2, (v0 + v1) / 2);
          if (Math.hypot(mx - cx, mz - cz) > radius) continue;
          if (!pts.every(([x, z]) => inside(t.poly, x, z))) continue;
          if (riverDistance(mx, mz) < 560 || mx < -15000) continue;
          if (Math.hypot(mx, mz) < CLEAR_RADIUS + Math.max(u1 - u0, v1 - v0) / 2) continue;
          out.push({pts, cx: mx, cz: mz, h, tile: t.v});
        }
      }
    }
  }
  return out;
};
