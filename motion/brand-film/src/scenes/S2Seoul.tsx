import React from 'react';
import {AbsoluteFill, Easing, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {Arc, Globe, MAGOK, projectLonLat} from '../components/Globe';
import {Stars} from '../components/Stars';
import {seeded} from '../lib/cam3d';
import {at, clamp, smoothstep} from '../lib/util';
import {C, FONT, FPS, H, W} from '../theme';
import {S1_ARCS, S1_END, starTravel} from './S1Universe';

export const S2_END_SCALE = 1600000; // ≈7.6 km across the frame
const L0 = Math.log(S1_END.scale);
const L1 = Math.log(S2_END_SCALE);
const zoomEase = Easing.bezier(0.3, 0.077, 0.25, 1);
export const s2Scale = (t: number) => Math.exp(L0 + (L1 - L0) * zoomEase(clamp(t / 5)));

const ARCS: Arc[] = [
  // arcs still in flight at the end of scene 1 continue here
  ...S1_ARCS.map((a) => ({...a, start: a.start - 5})),
  ...['tokyo', 'beijing', 'shanghai', 'hongkong', 'taipei', 'osaka', 'vladivostok', 'sapporo', 'manila', 'busan'].map((from, i) => ({
    from,
    to: 'seoul',
    start: -0.3 + i * 0.07,
    dur: 1.1,
  })),
];

const CLOUDS = (() => {
  const r = seeded(5);
  return Array.from({length: 26}, () => ({a: r() * Math.PI * 2, d: 120 + r() * 520, s: 160 + r() * 340, k: 0.6 + r() * 0.9}));
})();

const Label: React.FC<{x: number; y: number; text: string; sub?: string; opacity: number; size?: number}> = ({x, y, text, sub, opacity, size = 30}) => (
  <div style={{position: 'absolute', left: x, top: y, opacity, fontFamily: FONT, color: C.white, translate: '0px -50%'}}>
    <div style={{fontSize: size, fontWeight: 800, letterSpacing: '0.32em'}}>{text}</div>
    {sub ? <div style={{fontSize: size * 0.62, fontWeight: 500, letterSpacing: '0.12em', color: C.mist, marginTop: 6}}>{sub}</div> : null}
  </div>
);

export const S2Seoul: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const scale = s2Scale(t);
  const L = Math.log(scale);
  const r = smoothstep(L0, Math.log(9000), L);
  const center: [number, number] = [S1_END.center[0] + (MAGOK.lon - S1_END.center[0]) * r, S1_END.center[1] + (MAGOK.lat - S1_END.center[1]) * r];
  const logVel = (Math.log(s2Scale(t + 0.05)) - L) / 0.05;
  const haze = Math.exp(-Math.pow((L - Math.log(2600)) / 0.75, 2));
  const q = scale / 2600;
  const korea = projectLonLat(128.3, 36.2, scale, center);
  const seoul = projectLonLat(126.99, 37.57, scale, center);
  const pinIn = at(t, [3.3, 3.9], [0, 1]);
  return (
    <AbsoluteFill style={{background: C.space}}>
      <Stars travel={starTravel(5 + t)} streak={Math.max(0, 0.12 + 0.3 * (5 + t) - 0.9) * 0.25} opacity={1 - smoothstep(Math.log(900), Math.log(2200), L)} />
      <Globe
        t={t}
        scale={scale}
        center={center}
        sunAngle={at(t, [0, 1.2], [72, 40])}
        night={1 - smoothstep(Math.log(1000), Math.log(3000), L)}
        arcs={ARCS}
        arcOpacity={1 - smoothstep(Math.log(2500), Math.log(6000), L)}
        koreaGlow={smoothstep(Math.log(2200), Math.log(6000), L) * (1 - smoothstep(Math.log(30000), Math.log(90000), L))}
      />
      {/* atmosphere entry */}
      <AbsoluteFill style={{opacity: haze * 0.9, background: 'radial-gradient(circle at 50% 50%, rgba(220,238,255,0.55), rgba(90,160,235,0.35) 45%, rgba(10,40,80,0) 80%)'}} />
      {CLOUDS.map((c, i) => {
        const k = q * c.k;
        const o = Math.exp(-Math.pow(Math.log(k) / 0.55, 2)) * 0.5;
        if (o < 0.01) return null;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: W / 2 + Math.cos(c.a) * c.d * k - c.s * k,
              top: H / 2 + Math.sin(c.a) * c.d * k * 0.7 - c.s * k * 0.6,
              width: c.s * k * 2,
              height: c.s * k * 1.2,
              borderRadius: '50%',
              opacity: o,
              background: 'radial-gradient(ellipse at center, rgba(240,248,255,0.9), rgba(220,235,250,0.35) 40%, rgba(220,235,250,0) 70%)',
            }}
          />
        );
      })}
      {/* speed lines */}
      <svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity: clamp((logVel - 1.2) / 2.5) * 0.55}}>
        {Array.from({length: 48}).map((_, i) => {
          const a = (i / 48) * Math.PI * 2 + i * 0.37;
          const r0 = 520 + ((i * 97 + frame * 41) % 380);
          return <line key={i} x1={W / 2 + Math.cos(a) * r0} y1={H / 2 + Math.sin(a) * r0} x2={W / 2 + Math.cos(a) * (r0 + 160)} y2={H / 2 + Math.sin(a) * (r0 + 160)} stroke="#CFE6FF" strokeWidth={2} strokeOpacity={0.5} />;
        })}
      </svg>
      <Label x={korea.x + 40} y={korea.y} text="KOREA" sub="대한민국" opacity={smoothstep(Math.log(3500), Math.log(6000), L) * (1 - smoothstep(Math.log(20000), Math.log(40000), L))} />
      <Label x={seoul.x + 30} y={seoul.y - 60} text="SEOUL" sub="서울" opacity={smoothstep(Math.log(30000), Math.log(60000), L) * (1 - smoothstep(Math.log(160000), Math.log(300000), L))} />
      <Pin opacity={pinIn} t={t} />
      <Caption lines={[['대한민국, ', {t: '서울.', c: C.blueSoft}]]} from={1.6} to={4.75} y={880} size={78} />
    </AbsoluteFill>
  );
};

export const Pin: React.FC<{opacity: number; t: number; x?: number; y?: number}> = ({opacity, t, x = W / 2, y = H / 2}) => {
  const pulse = (t * 1.2) % 1;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, opacity}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <circle cx={x} cy={y} r={14 + pulse * 46} fill="none" stroke={C.redLit} strokeWidth={3} strokeOpacity={1 - pulse} />
        <circle cx={x} cy={y} r={11} fill={C.red} stroke={C.white} strokeWidth={3} />
        <line x1={x} y1={y - 16} x2={x} y2={y - 92} stroke={C.white} strokeWidth={2} />
      </svg>
      <div style={{position: 'absolute', left: x + 18, top: y - 128, fontFamily: FONT, color: C.white}}>
        <div style={{fontSize: 28, fontWeight: 800, letterSpacing: '0.3em'}}>MAGOK</div>
        <div style={{fontSize: 20, fontWeight: 500, letterSpacing: '0.1em', color: C.mist, marginTop: 4}}>37.56°N 126.83°E</div>
      </div>
    </div>
  );
};
