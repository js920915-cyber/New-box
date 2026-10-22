import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {BLOCK_EDGE, BLOCK_FILL, Globe, MAGOK, TILE_FILL} from '../components/Globe';
import {blocksAround, tilesAround} from '../lib/city';
import {Cam, linePath, P3, polyPath, projectPoint, toCam} from '../lib/cam3d';
import {bankRoads, hanPolygon} from '../lib/seoul';
import {at, clamp, mix, smoothstep, spline} from '../lib/util';
import {C, FONT, FPS, H, W} from '../theme';
import {Pin, S2_END_SCALE} from './S2Seoul';

const F = 1300;
const H0 = (F * 6371000) / S2_END_SCALE; // altitude that matches the last frame of scene 2

const LAND = '#0F3260';
const SKY_TOP = '#02060E';
const SKY_HZ = '#0B2C55';

const BLOCKS = blocksAround(0, 0, 5200);
const TILES = tilesAround(0, 0, 6500);
const RIVER = hanPolygon();
const ROADS = bankRoads(900);

// ---------- the center's building ----------
const B = {x0: -22, x1: 22, z0: -15, z1: 15, h: 36};
const STORE = {x0: -20, x1: 20, y0: 0.25, y1: 3.8};
const DOOR = {x0: -1.5, x1: 1.5, y1: 2.8};
const SIGN = {x0: -7.5, x1: 7.5, y0: 4.25, y1: 5.35};

// ---------- interior (inside the building footprint) ----------
type Box = {a: P3; b: P3; fill: string; edge?: string; glow?: boolean};
const IN = {x0: -14.5, x1: 14.5, z0: -14.6, z1: 14.6, h: 4.2};
const box = (a: P3, b: P3, fill = '#173B66', edge = '#5FA8F0', glow = false): Box => ({a, b, fill, edge, glow});
const rack = (cx: number, cz: number): Box[] => {
  const out: Box[] = [];
  for (const dx of [-0.6, 0.6]) for (const dz of [-0.6, 0.6]) out.push(box([cx + dx - 0.04, 0, cz + dz - 0.04], [cx + dx + 0.04, 2.3, cz + dz + 0.04], '#24507F'));
  out.push(box([cx - 0.64, 2.24, cz - 0.64], [cx + 0.64, 2.3, cz - 0.56], '#24507F'));
  out.push(box([cx - 0.64, 2.24, cz + 0.56], [cx + 0.64, 2.3, cz + 0.64], '#24507F'));
  out.push(box([cx - 1.1, 1.38, cz - 0.62], [cx + 1.1, 1.42, cz - 0.58], '#C9DCEF', '#FFFFFF'));
  return out;
};
const treadmill = (cx: number, cz: number): Box[] => [
  box([cx - 0.42, 0, cz - 1.0], [cx + 0.42, 0.22, cz + 1.0], '#163A66'),
  box([cx - 0.42, 0, cz - 1.08], [cx - 0.36, 1.25, cz - 0.98], '#24507F'),
  box([cx + 0.36, 0, cz - 1.08], [cx + 0.42, 1.25, cz - 0.98], '#24507F'),
  box([cx - 0.45, 1.2, cz - 1.2], [cx + 0.45, 1.36, cz - 0.95], '#1E4B7C', '#7CC2FF'),
];
const tripod = (x: number, z: number): Box[] => [
  box([x - 0.025, 0, z - 0.025], [x + 0.025, 2.0, z + 0.025], '#24507F'),
  box([x - 0.14, 2.0, z - 0.1], [x + 0.14, 2.16, z + 0.1], '#24507F', '#9CD0FF', true),
];
const INTERIOR: Box[] = [
  // evaluation zone: force plates, display, motion-capture cameras, running-analysis treadmills
  box([-4.2, 0, 3.0], [-3.6, 0.06, 3.6], '#1E6FC8', '#9CD0FF', true),
  box([-3.5, 0, 3.0], [-2.9, 0.06, 3.6], '#1E6FC8', '#9CD0FF', true),
  box([-1.85, 0, 4.4], [-1.79, 1.2, 4.46], '#24507F'),
  box([-2.35, 1.2, 4.38], [-1.29, 1.84, 4.48], '#0B2140', '#7CC2FF'),
  ...tripod(-6.4, 1.4),
  ...tripod(-0.9, 1.4),
  ...tripod(-6.4, 6.6),
  ...tripod(-0.9, 6.6),
  ...treadmill(-12.2, 3.5),
  ...treadmill(-10.6, 3.5),
  ...tripod(-11.4, 1.0),
  // strength zone
  ...rack(5.2, 8.2),
  ...rack(9.6, 8.2),
  box([3.2, 0, 2.6], [3.9, 0.3, 3.2], '#1B4475'),
  box([4.1, 0, 2.6], [4.8, 0.45, 3.2], '#1B4475'),
  box([5.0, 0, 2.6], [5.7, 0.6, 3.2], '#1B4475'),
  box([7.6, 0, 3.4], [9.2, 0.45, 3.75], '#1B4475'),
  box([13.5, 0, -1], [14.2, 0.85, 6], '#163A66'),
  box([10.4, 0, -6.4], [12.4, 0.62, -5.7], '#1B4475'),
  // turf lane hurdles
  ...[-11, -8, -5].map((x) => box([x - 0.03, 0, 12.0], [x + 0.03, 0.3, 13.4], '#C9DCEF', '#FFFFFF')),
  // ceiling light strips
  ...[-9, -3, 3, 9].map((x) => box([x - 0.14, IN.h - 0.06, -13], [x + 0.14, IN.h - 0.02, 13], '#EAF5FF', '#FFFFFF', true)),
];
const PLATES: {x: number; y: number; z: number}[] = [5.2, 9.6].flatMap((cx) => [
  {x: cx - 0.86, y: 1.4, z: 7.6},
  {x: cx + 0.86, y: 1.4, z: 7.6},
]);

const boxFaces = (bx: Box): {pts: P3[]; n: P3}[] => {
  const [x0, y0, z0] = bx.a;
  const [x1, y1, z1] = bx.b;
  return [
    {n: [0, 1, 0], pts: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]]},
    {n: [0, -1, 0], pts: [[x0, y0, z0], [x0, y0, z1], [x1, y0, z1], [x1, y0, z0]]},
    {n: [0, 0, -1], pts: [[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0]]},
    {n: [0, 0, 1], pts: [[x0, y0, z1], [x0, y1, z1], [x1, y1, z1], [x1, y0, z1]]},
    {n: [-1, 0, 0], pts: [[x0, y0, z0], [x0, y1, z0], [x0, y1, z1], [x0, y0, z1]]},
    {n: [1, 0, 0], pts: [[x1, y0, z0], [x1, y0, z1], [x1, y1, z1], [x1, y1, z0]]},
  ];
};

const shade = (fill: string, n: P3) => (n[1] > 0 ? mix(fill, '#FFFFFF', 0.12) : n[0] !== 0 ? mix(fill, '#000000', 0.18) : fill);

// ---------- camera path ----------
const K = {
  t: [0, 0.8, 1.45, 2.05, 2.5, 2.85, 3.25, 4.0, 5.0],
  y: [H0, 1700, 430, 95, 9, 1.7, 1.6, 1.6, 1.6],
  z: [0, -260, -700, -360, -105, -48, -15.4, -8.5, -5.0],
  x: [0, 0, 0, 0, 0, 0, 0, 0.3, 1.0],
  pitch: [90, 72, 40, 16, 3, -1, 0, 0, -1],
  yaw: [0, 0, 0, 0, 0, 0, 0, -3, -10],
};
const ch = (arr: number[], t: number, log = false) =>
  log ? Math.exp(spline(K.t.map((k, i) => [k, Math.log(arr[i])]), t)) : spline(K.t.map((k, i) => [k, arr[i]]), t);

export const s3Camera = (t: number): Cam => ({
  pos: [ch(K.x, t), ch(K.y, t, true), ch(K.z, t)],
  pitch: ch(K.pitch, t),
  yaw: ch(K.yaw, t),
  f: F,
  cx: W / 2,
  cy: H / 2,
  near: 0.08,
});

const pathOf = (cam: Cam, pts: P3[]) => polyPath(cam, pts)?.pts ?? null;

export const S3Center: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const cam = s3Camera(t);
  const inside = cam.pos[2] > B.z0 + 0.05;
  const horizon = H / 2 - F * Math.tan((cam.pitch * Math.PI) / 180);
  const camDist = (x: number, z: number) => Math.hypot(x - cam.pos[0], z - cam.pos[2], cam.pos[1]);
  const fog = (d: number) => smoothstep(1800, 5200, d);

  // ---- ground ----
  const ground: React.ReactNode[] = [];
  if (!inside) {
    TILES.forEach((tl, i) => {
      const d = pathOf(cam, tl.poly.map(([x, z]) => [x, 0, z] as P3));
      if (d) ground.push(<path key={'t' + i} d={d} fill={TILE_FILL} />);
    });
    const river = pathOf(cam, RIVER.map(([x, z]) => [x, 0.2, z] as P3));
    if (river) ground.push(<path key="river" d={river} fill="#0E5CB0" fillOpacity={0.9} stroke="#58AFFF" strokeWidth={1.5} />);
    ROADS.forEach((road, r) =>
      road.slice(0, -1).forEach((p, i) => {
        const l = linePath(cam, [p[0], 0.3, p[1]], [road[i + 1][0], 0.3, road[i + 1][1]]);
        if (l) ground.push(<path key={`r${r}-${i}`} d={l.d} stroke="#9CCBFF" strokeOpacity={0.55} strokeWidth={Math.max(1.2, Math.min(10, (60 * F) / l.depth))} fill="none" />);
      }),
    );
    // plaza in front of the building
    const plaza = pathOf(cam, [[-60, 0.05, -90], [60, 0.05, -90], [60, 0.05, 40], [-60, 0.05, 40]]);
    if (plaza) ground.push(<path key="plaza" d={plaza} fill="#12355F" />);
    for (let k = -80; k <= 30; k += 6) {
      const l = linePath(cam, [-60, 0.06, k], [60, 0.06, k]);
      if (l) ground.push(<path key={'pz' + k} d={l.d} stroke="#21507F" strokeWidth={1} />);
    }
  }

  // ---- buildings (painter's order) ----
  type Item = {d: number; node: React.ReactNode};
  const items: Item[] = [];
  if (!inside) {
    BLOCKS.forEach((b, i) => {
      const dist = camDist(b.cx, b.cz);
      const c = toCam(cam, [b.cx, 0, b.cz]);
      if (c[2] < -200) return;
      if (c[2] > 0 && Math.abs(c[0] / c[2]) > 1.25 + 300 / c[2]) return;
      const rise = smoothstep(0.15 + Math.hypot(b.cx, b.cz) / 9000, 1.25 + Math.hypot(b.cx, b.cz) / 9000, t);
      const h = Math.max(0.5, b.h * rise);
      const fg = fog(dist);
      const faces: React.ReactNode[] = [];
      const pts = b.pts;
      for (let k = 0; k < 4; k++) {
        const p = pts[k];
        const q = pts[(k + 1) % 4];
        // outward normal for counter-clockwise footprint (x east, z north)
        const nx = q[1] - p[1];
        const nz = -(q[0] - p[0]);
        const mx = (p[0] + q[0]) / 2;
        const mz = (p[1] + q[1]) / 2;
        if (nx * (cam.pos[0] - mx) + nz * (cam.pos[2] - mz) <= 0) continue;
        const d = pathOf(cam, [[p[0], 0, p[1]], [q[0], 0, q[1]], [q[0], h, q[1]], [p[0], h, p[1]]]);
        if (!d) continue;
        const lit = 0.5 + 0.5 * ((nx - nz) / Math.hypot(nx, nz)) * 0.7;
        faces.push(<path key={k} d={d} fill={mix(mix('#0C2647', '#1A4677', lit), SKY_HZ, fg)} stroke={BLOCK_EDGE} strokeOpacity={0.35 * (1 - fg)} strokeWidth={1} />);
      }
      const top = pathOf(cam, pts.map(([x, z]) => [x, h, z] as P3));
      if (top) faces.push(<path key="top" d={top} fill={mix(BLOCK_FILL, SKY_HZ, fg)} stroke={BLOCK_EDGE} strokeOpacity={0.9 * (1 - fg)} strokeWidth={1.2} />);
      items.push({d: dist, node: <g key={'b' + i}>{faces}</g>});
    });
  }
  items.push({d: camDist(0, 0), node: <Target key="target" cam={cam} t={t} inside={inside} />});
  items.sort((a, b) => b.d - a.d);

  const pin = projectPoint(cam, [0, B.h + 2, 0]);
  const fromS2 = 1 - clamp(frame / 6);

  return (
    <AbsoluteFill style={{background: LAND}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <defs>
          <linearGradient id="sky" x1={0} y1={0} x2={0} y2={1}>
            <stop offset="0%" stopColor={SKY_TOP} />
            <stop offset="100%" stopColor={SKY_HZ} />
          </linearGradient>
          <linearGradient id="hzfog" x1={0} y1={0} x2={0} y2={1}>
            <stop offset="0%" stopColor={SKY_HZ} stopOpacity={1} />
            <stop offset="100%" stopColor={SKY_HZ} stopOpacity={0} />
          </linearGradient>
        </defs>
        {horizon > -40 ? <rect x={0} y={0} width={W} height={Math.max(0, horizon)} fill="url(#sky)" /> : null}
        {ground}
        {horizon > -40 && !inside ? <rect x={0} y={horizon - 2} width={W} height={160} fill="url(#hzfog)" /> : null}
        {items.map((it) => it.node)}
      </svg>
      {pin ? <Pin opacity={at(t, [0.5, 1.1], [1, 0])} t={t + 5} x={pin.x} y={pin.y} /> : null}
      {fromS2 > 0 ? (
        <AbsoluteFill style={{opacity: fromS2}}>
          <Globe t={5} scale={S2_END_SCALE} center={[MAGOK.lon, MAGOK.lat]} sunAngle={40} night={0} />
        </AbsoluteFill>
      ) : null}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,4,12,0.55) 100%)'}} />
      <Caption lines={[['움직임을 위한 ', {t: '전문적인 공간.', c: C.blueSoft}]]} from={3.3} to={4.95} y={860} size={78} />
    </AbsoluteFill>
  );
};

// The center's building: facade with storefront, door, sign, and the interior seen through the glass.
const Target: React.FC<{cam: Cam; t: number; inside: boolean}> = ({cam, t, inside}) => {
  const near = Math.hypot(cam.pos[0], cam.pos[1], cam.pos[2] + 15) < 260;
  const rise = smoothstep(0.15, 1.25, t);
  const h = Math.max(0.5, B.h * rise);
  const nodes: React.ReactNode[] = [];
  const faces: {n: P3; pts: P3[]; tag: string}[] = [
    {tag: 'w', n: [-1, 0, 0], pts: [[B.x0, 0, B.z1], [B.x0, 0, B.z0], [B.x0, h, B.z0], [B.x0, h, B.z1]]},
    {tag: 'e', n: [1, 0, 0], pts: [[B.x1, 0, B.z0], [B.x1, 0, B.z1], [B.x1, h, B.z1], [B.x1, h, B.z0]]},
    {tag: 'n', n: [0, 0, 1], pts: [[B.x1, 0, B.z1], [B.x0, 0, B.z1], [B.x0, h, B.z1], [B.x1, h, B.z1]]},
    {tag: 'top', n: [0, 1, 0], pts: [[B.x0, h, B.z0], [B.x1, h, B.z0], [B.x1, h, B.z1], [B.x0, h, B.z1]]},
  ];
  if (!inside) {
    for (const f of faces) {
      const c = f.pts.reduce((s, p) => [s[0] + p[0] / 4, s[1] + p[1] / 4, s[2] + p[2] / 4], [0, 0, 0]);
      if (f.n[0] * (cam.pos[0] - c[0]) + f.n[1] * (cam.pos[1] - c[1]) + f.n[2] * (cam.pos[2] - c[2]) <= 0) continue;
      const d = pathOf(cam, f.pts);
      if (d) nodes.push(<path key={f.tag} d={d} fill={f.tag === 'top' ? '#1D4B80' : '#11335C'} stroke={C.blueLit} strokeWidth={2} />);
    }
  }

  // interior, visible through the storefront (or everywhere once inside)
  const storePts: P3[] = [[STORE.x0, STORE.y0, B.z0], [STORE.x1, STORE.y0, B.z0], [STORE.x1, STORE.y1, B.z0], [STORE.x0, STORE.y1, B.z0]];
  const storePath = inside ? null : pathOf(cam, storePts);
  if (inside || (near && storePath)) {
    nodes.push(
      <g key="interior">
        {storePath ? (
          <defs>
            <clipPath id="store">
              <path d={storePath} />
            </clipPath>
          </defs>
        ) : null}
        <g clipPath={storePath ? 'url(#store)' : undefined}>
          <Interior cam={cam} t={t} />
        </g>
      </g>,
    );
  }

  if (!inside) {
    // south facade with the storefront cut out
    const outer = pathOf(cam, [[B.x0, 0, B.z0], [B.x1, 0, B.z0], [B.x1, h, B.z0], [B.x0, h, B.z0]]);
    if (outer) {
      nodes.push(<path key="south" d={outer + ' ' + (storePath ?? '')} fillRule="evenodd" fill="#163D6B" stroke={C.blueLit} strokeWidth={2} />);
      // floor bands and mullions
      for (let y = 7.6; y < h - 0.5; y += 3.6) {
        const l = linePath(cam, [B.x0, y, B.z0 - 0.02], [B.x1, y, B.z0 - 0.02]);
        if (l) nodes.push(<path key={'fl' + y} d={l.d} stroke="#4C8BCB" strokeOpacity={0.55} strokeWidth={1.2} />);
      }
      if (h > 6) {
        for (let x = B.x0 + 2.2; x < B.x1; x += 2.2) {
          const l = linePath(cam, [x, 6, B.z0 - 0.02], [x, h, B.z0 - 0.02]);
          if (l) nodes.push(<path key={'ml' + x} d={l.d} stroke="#3A74B0" strokeOpacity={0.4} strokeWidth={1} />);
        }
      }
      if (storePath) {
        // glass tint, mullions and sliding doors
        const slide = smoothstep(2.72, 3.1, t) * 1.45;
        const glass = (x0: number, x1: number, k: string) => {
          const d = pathOf(cam, [[x0, STORE.y0, B.z0 - 0.01], [x1, STORE.y0, B.z0 - 0.01], [x1, STORE.y1, B.z0 - 0.01], [x0, STORE.y1, B.z0 - 0.01]]);
          return d ? <path key={k} d={d} fill="#7CC2FF" fillOpacity={0.1} stroke="#9CD0FF" strokeOpacity={0.7} strokeWidth={1.2} /> : null;
        };
        nodes.push(glass(STORE.x0, DOOR.x0 - 0.05, 'gl'), glass(DOOR.x1 + 0.05, STORE.x1, 'gr'));
        for (let x = STORE.x0 + 2.5; x < STORE.x1; x += 2.5) {
          if (x > DOOR.x0 - 0.2 && x < DOOR.x1 + 0.2) continue;
          const l = linePath(cam, [x, STORE.y0, B.z0 - 0.02], [x, STORE.y1, B.z0 - 0.02]);
          if (l) nodes.push(<path key={'sm' + x} d={l.d} stroke="#9CD0FF" strokeOpacity={0.6} strokeWidth={1.5} />);
        }
        const door = (x0: number, x1: number, k: string) => {
          const d = pathOf(cam, [[x0, 0.02, B.z0 - 0.04], [x1, 0.02, B.z0 - 0.04], [x1, DOOR.y1, B.z0 - 0.04], [x0, DOOR.y1, B.z0 - 0.04]]);
          return d ? <path key={k} d={d} fill="#9CD0FF" fillOpacity={0.14} stroke="#CFE8FF" strokeWidth={2} /> : null;
        };
        nodes.push(door(DOOR.x0 - slide, -slide, 'dl'), door(slide, DOOR.x1 + slide, 'dr'));
        const top = linePath(cam, [DOOR.x0 - 0.1, DOOR.y1, B.z0 - 0.04], [DOOR.x1 + 0.1, DOOR.y1, B.z0 - 0.04]);
        if (top) nodes.push(<path key="dtop" d={top.d} stroke="#CFE8FF" strokeWidth={3} />);
      }
      // sign above the storefront
      const p0 = projectPoint(cam, [SIGN.x0, SIGN.y1, B.z0 - 0.05]);
      const p1 = projectPoint(cam, [SIGN.x1, SIGN.y1, B.z0 - 0.05]);
      const p2 = projectPoint(cam, [SIGN.x0, SIGN.y0, B.z0 - 0.05]);
      if (p0 && p1 && p2 && h > SIGN.y1 && p0.z < 400) {
        const tw = 1500;
        const th = 110;
        nodes.push(
          <g key="sign" transform={`matrix(${(p1.x - p0.x) / tw} ${(p1.y - p0.y) / tw} ${(p2.x - p0.x) / th} ${(p2.y - p0.y) / th} ${p0.x} ${p0.y})`}>
            <rect x={0} y={0} width={tw} height={th} fill="#0A1E38" stroke={C.blueLit} strokeWidth={4} />
            <text x={tw / 2} y={th * 0.74} textAnchor="middle" fill={C.white} fontFamily={FONT} fontWeight={800} fontSize={78} letterSpacing={6}>
              R스포츠재활센터
            </text>
          </g>,
        );
      }
    }
  }
  return <g>{nodes}</g>;
};

const Interior: React.FC<{cam: Cam; t: number}> = ({cam, t}) => {
  const nodes: React.ReactNode[] = [];
  const room: {pts: P3[]; fill: string; k: string}[] = [
    {k: 'ceil', fill: '#081A33', pts: [[IN.x0, IN.h, IN.z0], [IN.x0, IN.h, IN.z1], [IN.x1, IN.h, IN.z1], [IN.x1, IN.h, IN.z0]]},
    {k: 'back', fill: '#0D2647', pts: [[IN.x0, 0, IN.z1], [IN.x1, 0, IN.z1], [IN.x1, IN.h, IN.z1], [IN.x0, IN.h, IN.z1]]},
    {k: 'left', fill: '#0B2140', pts: [[IN.x0, 0, IN.z0], [IN.x0, 0, IN.z1], [IN.x0, IN.h, IN.z1], [IN.x0, IN.h, IN.z0]]},
    {k: 'right', fill: '#0B2140', pts: [[IN.x1, 0, IN.z1], [IN.x1, 0, IN.z0], [IN.x1, IN.h, IN.z0], [IN.x1, IN.h, IN.z1]]},
    {k: 'front', fill: '#0B2140', pts: [[IN.x1, 0, IN.z0], [IN.x0, 0, IN.z0], [IN.x0, IN.h, IN.z0], [IN.x1, IN.h, IN.z0]]},
    {k: 'floor', fill: '#102C52', pts: [[IN.x0, 0, IN.z0], [IN.x1, 0, IN.z0], [IN.x1, 0, IN.z1], [IN.x0, 0, IN.z1]]},
  ];
  room.forEach((r) => {
    const d = pathOf(cam, r.pts);
    if (d) nodes.push(<path key={r.k} d={d} fill={r.fill} />);
  });
  // turf sprint lane and floor grid
  const turf = pathOf(cam, [[-14.4, 0.01, 11.4], [1, 0.01, 11.4], [1, 0.01, 14.5], [-14.4, 0.01, 14.5]]);
  if (turf) nodes.push(<path key="turf" d={turf} fill="#0F3A6A" />);
  for (let x = -14; x <= 1; x += 2.5) {
    const l = linePath(cam, [x, 0.02, 11.4], [x, 0.02, 14.5]);
    if (l) nodes.push(<path key={'tz' + x} d={l.d} stroke="#CFE6FF" strokeOpacity={0.5} strokeWidth={1.5} />);
  }
  for (let x = -13.5; x <= 13.5; x += 1.5) {
    const l = linePath(cam, [x, 0.01, IN.z0], [x, 0.01, 11.4]);
    if (l) nodes.push(<path key={'gx' + x} d={l.d} stroke="#1E4878" strokeOpacity={0.7} strokeWidth={1} />);
  }
  for (let z = IN.z0; z <= 11.4; z += 1.5) {
    const l = linePath(cam, [IN.x0, 0.01, z], [IN.x1, 0.01, z]);
    if (l) nodes.push(<path key={'gz' + z} d={l.d} stroke="#1E4878" strokeOpacity={0.7} strokeWidth={1} />);
  }
  // back-wall accent stripe and mirror
  const mirror = pathOf(cam, [[2.5, 0.4, IN.z1 - 0.02], [14, 0.4, IN.z1 - 0.02], [14, 2.3, IN.z1 - 0.02], [2.5, 2.3, IN.z1 - 0.02]]);
  if (mirror) nodes.push(<path key="mirror" d={mirror} fill="#14375F" stroke="#3E78B4" strokeWidth={1.5} />);
  const stripe = pathOf(cam, [[IN.x0, 2.9, IN.z1 - 0.03], [IN.x1, 2.9, IN.z1 - 0.03], [IN.x1, 3.02, IN.z1 - 0.03], [IN.x0, 3.02, IN.z1 - 0.03]]);
  if (stripe) nodes.push(<path key="stripe" d={stripe} fill={C.blue} />);
  const stripeR = pathOf(cam, [[-3, 2.9, IN.z1 - 0.04], [-1, 2.9, IN.z1 - 0.04], [-1, 3.02, IN.z1 - 0.04], [-3, 3.02, IN.z1 - 0.04]]);
  if (stripeR) nodes.push(<path key="stripeR" d={stripeR} fill={C.red} />);

  // wall slogan
  const q0 = projectPoint(cam, [-8, 3.75, IN.z1 - 0.05]);
  const q1 = projectPoint(cam, [2, 3.75, IN.z1 - 0.05]);
  const q2 = projectPoint(cam, [-8, 3.3, IN.z1 - 0.05]);
  if (q0 && q1 && q2) {
    const tw = 2000;
    const th = 90;
    nodes.push(
      <text key="slogan" transform={`matrix(${(q1.x - q0.x) / tw} ${(q1.y - q0.y) / tw} ${(q2.x - q0.x) / th} ${(q2.y - q0.y) / th} ${q0.x} ${q0.y})`} x={tw / 2} y={th * 0.8} textAnchor="middle" fill="#CFE6FF" fillOpacity={0.85} fontFamily={FONT} fontWeight={800} fontSize={72} letterSpacing={18}>
        EVALUATE · REHABILITATE · PERFORM
      </text>,
    );
  }
  // equipment, far to near
  const faces: {d: string; depth: number; fill: string; edge?: string; glow?: boolean}[] = [];
  INTERIOR.forEach((bx) => {
    boxFaces(bx).forEach((f) => {
      const c = f.pts.reduce((s, p) => [s[0] + p[0] / 4, s[1] + p[1] / 4, s[2] + p[2] / 4], [0, 0, 0]);
      if (f.n[0] * (cam.pos[0] - c[0]) + f.n[1] * (cam.pos[1] - c[1]) + f.n[2] * (cam.pos[2] - c[2]) <= 0) return;
      const p = polyPath(cam, f.pts);
      if (p) faces.push({d: p.pts, depth: p.depth, fill: bx.glow ? bx.fill : shade(bx.fill, f.n), edge: bx.edge, glow: bx.glow});
    });
  });
  PLATES.forEach((pl, i) => {
    const pts: P3[] = Array.from({length: 20}, (_, k) => [pl.x, pl.y + Math.cos((k / 20) * Math.PI * 2) * 0.225, pl.z + Math.sin((k / 20) * Math.PI * 2) * 0.225]);
    const p = polyPath(cam, pts);
    if (p) faces.push({d: p.pts, depth: p.depth - 0.01 * i, fill: '#2A5A90', edge: '#9CD0FF'});
  });
  faces.sort((a, b) => b.depth - a.depth);
  faces.forEach((f, i) =>
    nodes.push(
      <path key={'f' + i} d={f.d} fill={f.fill} stroke={f.edge ?? 'none'} strokeWidth={1.4} strokeOpacity={0.85} style={f.glow ? {filter: 'drop-shadow(0 0 10px rgba(124,194,255,0.9))'} : undefined} />,
    ),
  );
  // live curve on the evaluation display
  const scr = [-2.3, 1.25, 4.37] as P3;
  const pts: string[] = [];
  for (let k = 0; k <= 24; k++) {
    const u = k / 24;
    const y = 0.08 + 0.38 * Math.max(0, Math.sin(u * Math.PI * 2 + t * 3) * Math.exp(-u));
    const p = projectPoint(cam, [scr[0] + u * 0.95, scr[1] + y, scr[2]]);
    if (p) pts.push(`${p.x.toFixed(1)},${p.y.toFixed(1)}`);
  }
  if (pts.length > 2) nodes.push(<polyline key="curve" points={pts.join(' ')} fill="none" stroke={C.blueLit} strokeWidth={2.5} />);
  return <g>{nodes}</g>;
};
