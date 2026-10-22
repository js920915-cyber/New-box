import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Figure} from '../components/Figure';
import {Flash, Ground, Shadow, Skyline, Sky, StreetLights, sx, View, Vignette} from '../components/Scenery';
import {gaitPose, gaitSpeed, RUN, STAIR, stairPose} from '../lib/gaits';
import {CUT, cutState} from '../lib/moves';

const CUT_TURN1 = CUT.turn1;
import {at, EASE, smoothstep} from '../lib/util';
import {C, FONT, FPS, H, W} from '../theme';
import {useCaptions} from '../captions';
import {Ball} from './S4Question';

const CUTS = [2.5, 5.0];
const DAWN = {top: '#030B1A', bottom: '#2A5E9A'};

const Sun: React.FC<{x: number; y: number; r: number}> = ({x, y, r}) => (
  <g>
    <circle cx={x} cy={y} r={r * 5} fill="url(#sunglow)" />
    <circle cx={x} cy={y} r={r} fill="#FF7A70" />
    <defs>
      <radialGradient id="sunglow">
        <stop offset="0%" stopColor="#FF8C7A" stopOpacity={0.55} />
        <stop offset="35%" stopColor="#CC414A" stopOpacity={0.18} />
        <stop offset="100%" stopColor="#CC414A" stopOpacity={0} />
      </radialGradient>
    </defs>
  </g>
);

// Daily life: brisk stair climb outdoors.
const StairsShot: React.FC<{t: number}> = ({t}) => {
  const period = 1.0;
  const tau = t + 0.4;
  const pose = stairPose(tau, period, false);
  const s = 250;
  const ox = W * 0.42 - pose.hip.x * s;
  const oy = 770 + pose.hip.y * s;
  const steps: string[] = [];
  for (let i = -8; i < 16; i++) {
    steps.push(`L ${ox + i * STAIR.run * s} ${oy - i * STAIR.rise * s} L ${ox + (i + 1) * STAIR.run * s} ${oy - i * STAIR.rise * s} L ${ox + (i + 1) * STAIR.run * s} ${oy - (i + 1) * STAIR.rise * s}`);
  }
  const x0 = ox - 8 * STAIR.run * s;
  const y0 = oy + 8 * STAIR.rise * s;
  const v: View = {camX: pose.hip.x * 0.3, s: 120, gy: 640 + pose.hip.y * 30};
  return (
    <AbsoluteFill>
      <Sky gy={v.gy} top={DAWN.top} bottom={DAWN.bottom} glow="#FF8C7A" />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Sun x={1500} y={v.gy - 40} r={34} />
        <Skyline v={v} par={0.2} base={v.gy} seed={21} fill="#0B2445" />
        <path d={`M ${x0} ${H + 20} L ${x0} ${y0} ${steps.join(' ')} L ${W + 600} ${H + 20} Z`} fill="#10335C" stroke="#7CC2FF" strokeWidth={2.5} strokeLinejoin="round" />
        <Figure pose={pose} x={ox} y={oy} scale={s} bg="#10335C" />
      </svg>
    </AbsoluteFill>
  );
};

// Runner along the Han River at dawn.
const RiverShot: React.FC<{t: number}> = ({t}) => {
  const g = {...RUN, period: 0.66};
  const spd = gaitSpeed(g);
  const wx = spd * t;
  const v: View = {camX: wx + 0.4, s: 290, gy: 860, cx: W * 0.42};
  const pose = gaitPose(g, t / g.period);
  const far = v.gy - 300;
  return (
    <AbsoluteFill>
      <Sky gy={far} top={DAWN.top} bottom={DAWN.bottom} glow="#FF8C7A" />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Sun x={1420 - t * 6} y={far - 70} r={40} />
        <Skyline v={v} par={0.02} base={far} seed={5} fill="#0C2547" tower={1000} />
        {/* river with shimmer */}
        <rect x={0} y={far} width={W} height={v.gy - far} fill="#0B2D55" />
        {Array.from({length: 26}).map((_, i) => {
          const y = far + 8 + Math.pow(i / 26, 1.6) * (v.gy - far - 40);
          const off = ((i * 173 + wx * 30 * (0.3 + i / 26)) % 600) - 100;
          return <line key={i} x1={off} x2={off + 80 + i * 6} y1={y} y2={y} stroke={i % 5 === 0 ? '#FF9A8A' : '#8CC6FF'} strokeOpacity={0.25 + (i % 3) * 0.08} strokeWidth={2} />;
        })}
        <rect x={1420 - t * 6 - 30} y={far + 4} width={60} height={160} fill="url(#sunpath)" />
        <defs>
          <linearGradient id="sunpath" x1={0} y1={0} x2={0} y2={1}>
            <stop offset="0%" stopColor="#FF8C7A" stopOpacity={0.45} />
            <stop offset="100%" stopColor="#FF8C7A" stopOpacity={0} />
          </linearGradient>
        </defs>
        {/* bridge */}
        <g transform={`translate(${-((wx * 290 * 0.18) % 900)} 0)`}>
          {[0, 900, 1800].map((bx) => (
            <g key={bx}>
              <path d={`M ${bx - 100} ${far - 30} L ${bx + 1000} ${far - 30}`} stroke="#16406E" strokeWidth={10} />
              {[0, 300, 600].map((a) => (
                <g key={a}>
                  <path d={`M ${bx + a} ${far - 30} Q ${bx + a + 150} ${far - 140} ${bx + a + 300} ${far - 30}`} stroke="#2A5E9A" strokeWidth={5} fill="none" />
                  <line x1={bx + a} x2={bx + a} y1={far - 30} y2={far + 30} stroke="#16406E" strokeWidth={14} />
                </g>
              ))}
            </g>
          ))}
        </g>
        <rect x={0} y={v.gy - 26} width={W} height={26} fill="#0E2E52" />
        <StreetLights v={v} par={1} spacing={6} depth={0.75} />
        <Ground v={v} marks="road" color="#0E2B4F" markColor="#2A5E9A" />
        <Shadow x={sx(v, wx)} y={v.gy} w={70} />
        <Figure pose={pose} x={sx(v, wx)} y={v.gy} scale={v.s} bg="#0E2B4F" />
      </svg>
    </AbsoluteFill>
  );
};

// Footballer: sprint, plant, change direction under the floodlights.
const PitchShot: React.FC<{t: number}> = ({t}) => {
  const tau = 0.05 + t * 1.0;
  const st = cutState(tau, RUN);
  const s = 270;
  const camX = at(tau, [0, 1.05, 1.6, 2.6], [-1.8, 0.0, 0.0, -1.6], EASE);
  const v: View = {camX, s, gy: 860};
  const X = (wx: number) => sx(v, wx);
  const k = st.turn;
  const trail: string[] = [];
  for (let j = 0; j < 26; j++) {
    const q = cutState(Math.max(0.05, tau - j * 0.035), RUN);
    trail.push(`${X(q.x)},${v.gy + 14}`);
  }
  // ball runs ahead, is stopped at the plant, then leaves with the player in the new direction
  const ballX = tau < 0.9 ? st.x + 0.7 : tau < CUT_TURN1 ? 0.95 - 0.35 * smoothstep(0.9, CUT_TURN1, tau) : Math.min(0.6, st.x - 0.62);
  return (
    <AbsoluteFill>
      <Sky gy={v.gy - 60} top="#01050B" bottom="#0A2242" glow="#7CC2FF" />
      <div style={{position: 'absolute', left: -200, top: -260, width: 800, height: 800, background: 'radial-gradient(circle, rgba(170,210,255,0.38), rgba(0,0,0,0) 60%)'}} />
      <div style={{position: 'absolute', right: -200, top: -260, width: 800, height: 800, background: 'radial-gradient(circle, rgba(170,210,255,0.34), rgba(0,0,0,0) 60%)'}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Skyline v={v} par={0.1} base={v.gy - 50} seed={9} fill="#0A1B33" windows={false} />
        <rect x={0} y={v.gy - 56} width={W} height={56} fill="#0B2342" />
        <Ground v={v} marks="turf" color="#0B2A44" markColor="#1B4C6B" />
        <polyline points={trail.join(' ')} fill="none" stroke={C.blueLit} strokeWidth={8} strokeLinecap="round" opacity={0.6} style={{filter: 'drop-shadow(0 0 10px rgba(58,160,255,0.9))'}} />
        <path d={`M ${X(0.75) - 24} ${v.gy} L ${X(0.75)} ${v.gy - 64} L ${X(0.75) + 24} ${v.gy} Z`} fill={C.red} />
        <Ball x={X(ballX)} y={v.gy - 0.11 * s} r={0.11 * s} rot={ballX * 520} />
        <Shadow x={X(st.x)} y={v.gy} w={80} />
        <g transform={`translate(${X(st.x)} 0) scale(${Math.abs(k) < 0.08 ? 0.08 * Math.sign(k || 1) : k} 1) translate(${-X(st.x)} 0)`}>
          <Figure pose={st.pose} x={X(st.x)} y={v.gy} scale={s} bg="#0B2A44" />
        </g>
      </svg>
    </AbsoluteFill>
  );
};

const Line: React.FC<{parts: {text: string; at: number; color?: string}[]; t: number; size: number}> = ({parts, t, size}) => (
  <div style={{display: 'flex', justifyContent: 'center', gap: size * 0.32}}>
    {parts.map((p, i) => {
      const k = at(t, [p.at, p.at + 0.6], [0, 1], EASE);
      return (
        <span key={i} style={{opacity: k, translate: `0px ${(1 - k) * 24}px`, filter: `blur(${(1 - k) * 10}px)`, color: p.color ?? C.white}}>
          {p.text}
        </span>
      );
    })}
  </div>
);

export const S7Return: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const flash = Math.max(at(t, [0, 0.12], [0.35, 0]), ...CUTS.map((c) => at(t, [c - 0.02, c, c + 0.12], [0, 0.35, 0])));
  const pull = smoothstep(6.9, 8.0, t);
  const captions = useCaptions();
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{scale: `${1 - 0.1 * pull}`, opacity: 1 - pull * 0.9}}>
        {t < CUTS[0] ? <StairsShot t={t} /> : t < CUTS[1] ? <RiverShot t={t - CUTS[0]} /> : <PitchShot t={t - CUTS[1]} />}
        <Vignette k={0.55} />
        <Flash o={flash} />
      </AbsoluteFill>
      <div style={{display: captions ? 'block' : 'none', position: 'absolute', left: 0, right: 0, top: 130, fontFamily: FONT, fontWeight: 800, fontSize: 84, letterSpacing: '-0.02em', color: C.white, textShadow: '0 6px 40px rgba(0,0,0,0.6)', lineHeight: 1.25, opacity: at(t, [7.3, 7.9], [1, 0])}}>
        <Line t={t} size={84} parts={[{text: '일상으로.', at: 0.35}, {text: '운동으로.', at: CUTS[0] + 0.2}]} />
        <Line t={t} size={84} parts={[{text: '다시 당신의 움직임으로.', at: CUTS[1] + 0.25, color: C.blueSoft}]} />
      </div>
    </AbsoluteFill>
  );
};
