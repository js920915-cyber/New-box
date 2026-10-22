import React from 'react';
import {C, FONT, W, H} from '../theme';

// Corner brackets + index label used on assessment panels.
export const HudFrame: React.FC<{index: string; title: string; sub: string; opacity?: number; inset?: number}> = ({index, title, sub, opacity = 1, inset = 70}) => {
  const L = 46;
  const c = (x: number, y: number, dx: number, dy: number) => `M ${x} ${y + dy * L} L ${x} ${y} L ${x + dx * L} ${y}`;
  return (
    <div style={{position: 'absolute', inset: 0, opacity}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <path d={[c(inset, inset, 1, 1), c(W - inset, inset, -1, 1), c(inset, H - inset, 1, -1), c(W - inset, H - inset, -1, -1)].join(' ')} stroke={C.blueSoft} strokeOpacity={0.7} strokeWidth={3} fill="none" />
      </svg>
      <div style={{position: 'absolute', left: inset + 40, top: inset + 30, fontFamily: FONT, display: 'flex', alignItems: 'baseline', gap: 22}}>
        <div style={{fontSize: 30, fontWeight: 800, color: C.blueLit, letterSpacing: '0.08em'}}>{index}</div>
        <div>
          <div style={{fontSize: 46, fontWeight: 800, color: C.white, letterSpacing: '-0.01em'}}>{title}</div>
          <div style={{fontSize: 22, fontWeight: 700, color: C.muted, letterSpacing: '0.28em', marginTop: 4}}>{sub}</div>
        </div>
      </div>
    </div>
  );
};

// Small labelled numeric readout.
export const Readout: React.FC<{x: number; y: number; label: string; value: string; unit?: string; color?: string; opacity?: number; size?: number}> = ({x, y, label, value, unit, color = C.white, opacity = 1, size = 64}) => (
  <div style={{position: 'absolute', left: x, top: y, fontFamily: FONT, opacity}}>
    <div style={{fontSize: 26, fontWeight: 700, color: C.mist}}>{label}</div>
    <div style={{fontSize: size, fontWeight: 850, color, fontVariantNumeric: 'tabular-nums', letterSpacing: '-0.02em', lineHeight: 1.1}}>
      {value}
      {unit ? <span style={{fontSize: size * 0.45, fontWeight: 700, color: C.mist, marginLeft: 8}}>{unit}</span> : null}
    </div>
  </div>
);

// Chart panel with axes; children draw inside (0..w, 0..h) with y down.
export const Plot: React.FC<{x: number; y: number; w: number; h: number; children: React.ReactNode; grid?: number[]; opacity?: number}> = ({x, y, w, h, children, grid = [], opacity = 1}) => (
  <svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity}}>
    <g transform={`translate(${x} ${y})`}>
      <rect x={-24} y={-24} width={w + 48} height={h + 48} rx={18} fill="#071A33" fillOpacity={0.82} stroke="#1E4878" strokeWidth={2} />
      {grid.map((gy, i) => (
        <line key={i} x1={0} x2={w} y1={gy} y2={gy} stroke="#1E4878" strokeWidth={1.5} strokeDasharray={i === 0 ? undefined : '6 8'} />
      ))}
      {children}
    </g>
  </svg>
);

// Clinic backdrop: back wall panels, light strips and a perspective floor grid.
export const LabBackdrop: React.FC<{gy: number; shift?: number}> = ({gy, shift = 0}) => (
  <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
    <defs>
      <linearGradient id="wall" x1={0} y1={0} x2={0} y2={1}>
        <stop offset="0%" stopColor="#040D1C" />
        <stop offset="100%" stopColor="#0C2647" />
      </linearGradient>
      <linearGradient id="floor" x1={0} y1={0} x2={0} y2={1}>
        <stop offset="0%" stopColor="#0E2A4E" />
        <stop offset="100%" stopColor="#030A16" />
      </linearGradient>
      <radialGradient id="spot" cx="50%" cy="100%" r="60%">
        <stop offset="0%" stopColor="#3AA0FF" stopOpacity={0.22} />
        <stop offset="100%" stopColor="#3AA0FF" stopOpacity={0} />
      </radialGradient>
    </defs>
    <rect width={W} height={gy} fill="url(#wall)" />
    {Array.from({length: 12}).map((_, i) => {
      const x = ((i * 220 - shift) % 2640 + 2640) % 2640 - 360;
      return <line key={i} x1={x} x2={x} y1={0} y2={gy} stroke="#0F2A4E" strokeWidth={2} />;
    })}
    <rect x={0} y={gy - 230} width={W} height={4} fill={C.blue} opacity={0.55} />
    <rect width={W} height={gy} fill="url(#spot)" />
    <rect y={gy} width={W} height={H - gy} fill="url(#floor)" />
    {Array.from({length: 25}).map((_, k) => {
      const x0 = W / 2 + (k - 12) * 160 - (shift % 160);
      return <line key={k} x1={x0} y1={gy} x2={W / 2 + (x0 - W / 2) * 2.2} y2={H} stroke="#1E4878" strokeOpacity={0.45} strokeWidth={1.2} />;
    })}
    {[0.1, 0.27, 0.5, 0.82].map((d, i) => (
      <line key={i} x1={0} x2={W} y1={gy + (H - gy) * d} y2={gy + (H - gy) * d} stroke="#1E4878" strokeOpacity={0.4} strokeWidth={1.2} />
    ))}
    <line x1={0} x2={W} y1={gy} y2={gy} stroke="#2D5E95" strokeWidth={2} />
  </svg>
);
