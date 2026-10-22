import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {at, clamp, EASE, INOUT} from '../lib/util';
import {C, FONT, FPS, H, W} from '../theme';
import {useCaptions} from '../captions';

const CX = W / 2;
const CY = H / 2 - 40;

type Trail = {pts: [number, number][]; color: string; width: number; delay: number; o: number};

// Cubic bezier sampled into points.
const bez = (p0: number[], p1: number[], p2: number[], p3: number[], n = 90): [number, number][] =>
  Array.from({length: n + 1}, (_, i) => {
    const u = i / n;
    const a = (1 - u) ** 3;
    const b = 3 * (1 - u) ** 2 * u;
    const c = 3 * (1 - u) * u * u;
    const d = u ** 3;
    return [a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]];
  });

const TRAILS: Trail[] = [
  {pts: [...bez([-80, 980], [420, 1020], [520, 360], [880, 520]), ...bez([880, 520], [1000, 575], [900, CY], [CX, CY]).slice(1)], color: C.blueLit, width: 7, delay: 0, o: 1},
  {pts: [...bez([2000, 80], [1500, 40], [1400, 760], [1050, 600]), ...bez([1050, 600], [960, 560], [1030, CY], [CX, CY]).slice(1)], color: C.redLit, width: 7, delay: 0.08, o: 1},
  {pts: bez([-80, 820], [500, 760], [700, 300], [CX, CY]), color: C.blueSoft, width: 2.5, delay: 0.15, o: 0.6},
  {pts: bez([-80, 300], [400, 200], [760, 700], [CX, CY]), color: C.blue, width: 2.5, delay: 0.25, o: 0.5},
  {pts: bez([2000, 1000], [1500, 1060], [1250, 360], [CX, CY]), color: '#FF8C7A', width: 2.5, delay: 0.2, o: 0.55},
  {pts: bez([2000, 420], [1600, 520], [1200, 820], [CX, CY]), color: C.red, width: 2.5, delay: 0.3, o: 0.45},
];

export const S8Brand: React.FC<{logo?: string}> = ({logo}) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const end = at(t, [5.25, 6.0], [1, 0]);
  const burst = clamp((t - 2.1) / 0.6);
  const word = at(t, [2.15, 2.95], [0, 1], EASE);
  const rule = at(t, [2.25, 2.9], [0, 1], EASE);
  const tag = ['EVALUATE.', 'REHABILITATE.', 'PERFORM.'];
  const captions = useCaptions();
  return (
    <AbsoluteFill style={{background: '#01040A'}}>
      <AbsoluteFill style={{opacity: end}}>
        <AbsoluteFill style={{background: `radial-gradient(circle at 50% 46%, rgba(8,60,120,${0.35 * word}), rgba(0,0,0,0) 55%)`}} />
        <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
          <g style={{filter: 'drop-shadow(0 0 12px rgba(120,190,255,0.9))'}} opacity={1 - clamp((t - 2.2) / 0.5) * 0.85}>
            {TRAILS.map((tr, i) => {
              const p = INOUT(clamp((t - 0.25 - tr.delay) / 1.85));
              if (p <= 0) return null;
              const n = Math.max(2, Math.round(p * (tr.pts.length - 1)) + 1);
              const shown = tr.pts.slice(0, n);
              const tail = Math.max(0, n - 70);
              const [hx, hy] = shown[shown.length - 1];
              return (
                <g key={i} opacity={tr.o}>
                  <polyline points={shown.slice(tail).map((q) => q.join(',')).join(' ')} fill="none" stroke={tr.color} strokeWidth={tr.width} strokeLinecap="round" strokeLinejoin="round" />
                  <polyline points={shown.slice(0, tail + 1).map((q) => q.join(',')).join(' ')} fill="none" stroke={tr.color} strokeWidth={tr.width * 0.4} strokeOpacity={0.35} />
                  {p < 1 ? <circle cx={hx} cy={hy} r={tr.width * 1.4} fill="#FFFFFF" /> : null}
                </g>
              );
            })}
          </g>
          {burst > 0 && burst < 1 ? (
            <g>
              <circle cx={CX} cy={CY} r={30 + burst * 520} fill="none" stroke="#CFE6FF" strokeWidth={3 * (1 - burst)} opacity={1 - burst} />
              <circle cx={CX} cy={CY} r={120 * (1 - burst)} fill="#EAF6FF" opacity={0.8 * (1 - burst)} />
            </g>
          ) : null}
          {/* the two paths settle into a split rule under the name */}
          <line x1={CX} x2={CX - 260 * rule} y1={CY + 92} y2={CY + 92} stroke={C.blueLit} strokeWidth={5} strokeLinecap="round" />
          <line x1={CX} x2={CX + 260 * rule} y1={CY + 92} y2={CY + 92} stroke={C.redLit} strokeWidth={5} strokeLinecap="round" />
        </svg>
        <div style={{position: 'absolute', left: 0, right: 0, top: CY - 100, display: captions || logo ? 'flex' : 'none', justifyContent: 'center', opacity: word, filter: `blur(${(1 - word) * 14}px)`}}>
          {logo ? (
            <Img src={staticFile(logo)} style={{height: 150, objectFit: 'contain'}} />
          ) : (
            <div style={{fontFamily: FONT, fontWeight: 850, fontSize: 132, color: C.white, letterSpacing: `${-0.02 + (1 - word) * 0.12}em`, lineHeight: 1.1}}>R스포츠재활센터</div>
          )}
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, top: CY + 130, display: captions ? 'flex' : 'none', justifyContent: 'center', gap: 38, fontFamily: FONT, fontWeight: 700, fontSize: 38, letterSpacing: '0.3em', color: C.mist}}>
          {tag.map((w, i) => {
            const k = at(t, [2.8 + i * 0.22, 3.3 + i * 0.22], [0, 1], EASE);
            return (
              <span key={w} style={{opacity: k, translate: `0px ${(1 - k) * 14}px`, color: i === 2 ? C.white : C.mist}}>
                {w}
              </span>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
