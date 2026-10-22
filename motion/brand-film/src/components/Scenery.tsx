import React, {useMemo} from 'react';
import {seeded} from '../lib/cam3d';
import {C, FONT, H, W} from '../theme';

// 2D side-view "camera": world meters → screen px.
export type View = {camX: number; s: number; gy: number; cx?: number};
export const sx = (v: View, x: number, par = 1) => (v.cx ?? W / 2) + (x - v.camX * par) * v.s;
export const sy = (v: View, y: number) => v.gy - y * v.s;

const wrap = (x: number, period: number) => ((x % period) + period) % period;

export const Sky: React.FC<{top?: string; bottom?: string; gy: number; glow?: string}> = ({top = '#02070F', bottom = '#0C2A50', gy, glow}) => (
  <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
    <defs>
      <linearGradient id="skyg" x1={0} y1={0} x2={0} y2={1}>
        <stop offset="0%" stopColor={top} />
        <stop offset={`${(gy / H) * 100}%`} stopColor={bottom} />
        <stop offset="100%" stopColor="#030A16" />
      </linearGradient>
      <radialGradient id="hglow" cx="50%" cy={`${(gy / H) * 100}%`} r="60%">
        <stop offset="0%" stopColor={glow ?? '#2F86E0'} stopOpacity={0.35} />
        <stop offset="100%" stopColor={glow ?? '#2F86E0'} stopOpacity={0} />
      </radialGradient>
    </defs>
    <rect width={W} height={H} fill="url(#skyg)" />
    <rect width={W} height={H} fill="url(#hglow)" />
  </svg>
);

export const Skyline: React.FC<{v: View; par: number; base: number; seed?: number; fill?: string; windows?: boolean; tower?: number}> = ({v, par, base, seed = 3, fill = '#0A1F3B', windows = true, tower}) => {
  const bld = useMemo(() => {
    const r = seeded(seed);
    const out: {x: number; w: number; h: number; lit: number[]}[] = [];
    let x = 0;
    while (x < 2600) {
      const w = 40 + r() * 90;
      const h = 40 + Math.pow(r(), 1.5) * 220;
      out.push({x, w, h, lit: Array.from({length: 8}, () => r())});
      x += w + r() * 14;
    }
    return out;
  }, [seed]);
  const off = wrap(v.camX * v.s * par, 2600);
  return (
    <g>
      {[0, 2600].map((rep) =>
        bld.map((b, i) => {
          const x = b.x - off + rep - 300;
          if (x > W + 50 || x + b.w < -50) return null;
          return (
            <g key={`${rep}-${i}`}>
              <rect x={x} y={base - b.h} width={b.w} height={b.h} fill={fill} />
              {windows
                ? b.lit.map((l, k) =>
                    l > 0.55 ? <rect key={k} x={x + 8 + (k % 3) * (b.w / 3.2)} y={base - b.h + 16 + Math.floor(k / 3) * 26} width={4} height={6} fill="#9CCBFF" fillOpacity={0.35 + l * 0.3} /> : null,
                  )
                : null}
            </g>
          );
        }),
      )}
      {tower !== undefined ? (
        <g transform={`translate(${tower - off * 0.5}, ${base})`}>
          <path d="M -140 0 Q -60 -95 0 -105 Q 70 -95 150 0 Z" fill={fill} />
          <rect x={-5} y={-260} width={10} height={160} fill={fill} />
          <rect x={-16} y={-235} width={32} height={26} rx={6} fill={fill} />
          <rect x={-2} y={-320} width={4} height={62} fill={fill} />
        </g>
      ) : null}
    </g>
  );
};

export const StreetLights: React.FC<{v: View; par?: number; spacing?: number; depth?: number}> = ({v, par = 0.7, spacing = 9, depth = 0.5}) => {
  const items = [];
  const k = v.s * depth;
  const cx = v.cx ?? W / 2;
  const left = v.camX * par - cx / k - spacing;
  const start = Math.floor(left / spacing) * spacing;
  for (let x = start; x < left + W / k + spacing * 2; x += spacing) {
    const X = cx + (x - v.camX * par) * k;
    const top = v.gy - 5.2 * k;
    items.push(
      <g key={x}>
        <line x1={X} y1={v.gy} x2={X} y2={top} stroke="#16365F" strokeWidth={6} />
        <line x1={X} y1={top} x2={X + 40} y2={top + 6} stroke="#16365F" strokeWidth={6} />
        <circle cx={X + 40} cy={top + 10} r={60} fill="url(#lampglow)" />
        <path d={`M ${X + 30} ${top + 12} L ${X + 50} ${top + 12} L ${X + 140} ${v.gy} L ${X - 60} ${v.gy} Z`} fill="#8CC6FF" fillOpacity={0.06} />
      </g>,
    );
  }
  return (
    <g>
      <defs>
        <radialGradient id="lampglow">
          <stop offset="0%" stopColor="#EAF6FF" stopOpacity={0.9} />
          <stop offset="25%" stopColor="#8CC6FF" stopOpacity={0.3} />
          <stop offset="100%" stopColor="#3AA0FF" stopOpacity={0} />
        </radialGradient>
      </defs>
      {items}
    </g>
  );
};

// Ground below the figure plane: gradient plus moving markings.
export const Ground: React.FC<{v: View; color?: string; marks?: 'road' | 'grid' | 'turf' | 'none'; markColor?: string}> = ({v, color = '#0A1D36', marks = 'grid', markColor = '#1E4878'}) => {
  const lines: React.ReactNode[] = [];
  if (marks === 'road') {
    const sp = 3;
    const k = v.s * 1.18;
    const cx = v.cx ?? W / 2;
    const left = v.camX - cx / k - sp;
    for (let x = Math.floor(left / sp) * sp; x < left + W / k + sp * 2; x += sp) {
      const X = cx + (x - v.camX) * k;
      lines.push(<rect key={x} x={X} y={v.gy + 64} width={1.3 * k} height={9} fill="#DCEBFF" fillOpacity={0.55} />);
    }
  }
  if (marks === 'grid') {
    for (let k = -12; k <= 12; k++) {
      const x0 = sx(v, Math.round(v.camX) + k * 1.0);
      const xb = (v.cx ?? W / 2) + (x0 - (v.cx ?? W / 2)) * 1.9;
      lines.push(<line key={'g' + k} x1={x0} y1={v.gy} x2={xb} y2={H} stroke={markColor} strokeWidth={1.2} strokeOpacity={0.6} />);
    }
    [0.08, 0.22, 0.45, 0.8].forEach((d, i) => {
      const y = v.gy + (H - v.gy) * d;
      lines.push(<line key={'h' + i} x1={0} x2={W} y1={y} y2={y} stroke={markColor} strokeWidth={1.2} strokeOpacity={0.5} />);
    });
  }
  if (marks === 'turf') {
    const sp = 5;
    const left = v.camX - W / 2 / v.s - sp;
    for (let x = Math.floor(left / sp) * sp; x < left + W / v.s + sp * 2; x += sp) {
      if (Math.round(x / sp) % 2 === 0) continue;
      const X0 = sx(v, x);
      const X1 = sx(v, x + sp);
      lines.push(<path key={x} d={`M ${X0} ${v.gy} L ${X1} ${v.gy} L ${(v.cx ?? W / 2) + (X1 - (v.cx ?? W / 2)) * 1.9} ${H} L ${(v.cx ?? W / 2) + (X0 - (v.cx ?? W / 2)) * 1.9} ${H} Z`} fill="#123D56" fillOpacity={0.55} />);
    }
    lines.push(<line key="touch" x1={0} x2={W} y1={v.gy + 52} y2={v.gy + 52} stroke="#E8F2FF" strokeOpacity={0.7} strokeWidth={5} />);
  }
  return (
    <g>
      <defs>
        <linearGradient id="groundg" x1={0} y1={0} x2={0} y2={1}>
          <stop offset="0%" stopColor={color} />
          <stop offset="100%" stopColor="#02060D" />
        </linearGradient>
      </defs>
      <rect x={0} y={v.gy} width={W} height={H - v.gy} fill="url(#groundg)" />
      {lines}
      <line x1={0} x2={W} y1={v.gy} y2={v.gy} stroke={markColor} strokeWidth={2} />
    </g>
  );
};

// Figure contact shadow.
export const Shadow: React.FC<{x: number; y: number; w: number; o?: number}> = ({x, y, w, o = 0.45}) => (
  <ellipse cx={x} cy={y + 4} rx={w} ry={w * 0.08} fill="#000" fillOpacity={o} />
);

export const Chip: React.FC<{text: string; sub?: string; opacity?: number; x?: number; y?: number; color?: string}> = ({text, sub, opacity = 1, x = 120, y = 96, color = C.blueLit}) => (
  <div style={{position: 'absolute', left: x, top: y, opacity, fontFamily: FONT, display: 'flex', alignItems: 'center', gap: 16}}>
    <div style={{width: 10, height: 44, background: color, borderRadius: 3}} />
    <div>
      <div style={{fontSize: 40, fontWeight: 800, color: C.white, letterSpacing: '-0.01em'}}>{text}</div>
      {sub ? <div style={{fontSize: 28, fontWeight: 500, color: C.mist, letterSpacing: '0.01em', marginTop: 2}}>{sub}</div> : null}
    </div>
  </div>
);

export const Flash: React.FC<{o: number}> = ({o}) => (o > 0.001 ? <div style={{position: 'absolute', inset: 0, background: '#EAF4FF', opacity: o}} /> : null);

export const Vignette: React.FC<{k?: number}> = ({k = 0.6}) => (
  <div style={{position: 'absolute', inset: 0, background: `radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(0,3,10,${k}) 100%)`}} />
);

// Integrate a playback-rate curve so slow motion keeps motion continuous.
export const warp = (t: number, rate: (t: number) => number, dt = 1 / 120) => {
  let acc = 0;
  for (let u = 0; u < t; u += dt) acc += rate(Math.min(u + dt / 2, t)) * Math.min(dt, t - u);
  return acc;
};
