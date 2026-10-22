import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {Figure} from '../components/Figure';
import {Chip, Flash, Ground, Shadow, Skyline, Sky, StreetLights, sx, sy, View, Vignette, warp} from '../components/Scenery';
import {blend, Pose} from '../lib/body';
import {gaitPose, gaitSpeed, JOG, RUN, STAIR, stairPose} from '../lib/gaits';
import {kneeHoldPose} from '../lib/moves';
import {at, clamp, smoothstep} from '../lib/util';
import {C, FPS, H, W} from '../theme';

export const CUT_A = 1.5;
export const CUT_B = 3.0;

export const Ball: React.FC<{x: number; y: number; r: number; rot: number}> = ({x, y, r, rot}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`}>
    <circle r={r} fill="#F4F8FC" />
    <path d={`M ${-r * 0.3} ${-r * 0.25} L 0 ${-r * 0.45} L ${r * 0.3} ${-r * 0.25} L ${r * 0.2} ${r * 0.1} L ${-r * 0.2} ${r * 0.1} Z`} fill="#0A1E38" />
    <path d={`M ${-r * 0.3} ${-r * 0.25} L ${-r * 0.75} ${-r * 0.45} M ${r * 0.3} ${-r * 0.25} L ${r * 0.75} ${-r * 0.45} M ${r * 0.2} ${r * 0.1} L ${r * 0.45} ${r * 0.7} M ${-r * 0.2} ${r * 0.1} L ${-r * 0.45} ${r * 0.7}`} stroke="#0A1E38" strokeWidth={r * 0.08} />
  </g>
);

const pulseOf = (phase: number, len = 0.45) => {
  const p = ((phase % 1) + 1) % 1;
  return p < len ? p / len : null;
};

const RunnerShot: React.FC<{t: number}> = ({t}) => {
  const spd = gaitSpeed(RUN);
  const wx = spd * t;
  const v: View = {camX: wx + 0.25, s: at(t, [0, CUT_A], [300, 335]), gy: 830, cx: W * 0.46};
  const phase = t / RUN.period + 0.1;
  const pose = gaitPose(RUN, phase);
  const pulse = t > 0.45 ? pulseOf(phase) : null;
  return (
    <AbsoluteFill>
      <Sky gy={v.gy} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Skyline v={v} par={0.06} base={v.gy - 10} />
        <StreetLights v={v} />
        <Ground v={v} marks="road" color="#0B1F3A" markColor="#1B3F6B" />
        <Shadow x={sx(v, wx)} y={v.gy} w={70} />
        <Figure pose={pose} x={sx(v, wx)} y={v.gy} scale={v.s} knee={pulse !== null ? {color: C.redLit, pulse} : undefined} bg="#0B2140" />
      </svg>
      <Chip text="러너" sub="달리다 느낀 무릎 불편감" opacity={at(t, [0.15, 0.5], [0, 1])} />
    </AbsoluteFill>
  );
};

const SoccerShot: React.FC<{t: number}> = ({t}) => {
  const spd = gaitSpeed(JOG);
  // jog with the ball, then ease to a stop and hold the knee
  const stopK = smoothstep(0.62, 1.05, t);
  const travel = (u: number) => spd * (u < 0.62 ? u : 0.62 + (u - 0.62) * (1 - smoothstep(0.62, 1.05, u)) * 0.6);
  const wx = travel(t);
  const jog = gaitPose(JOG, wx / (spd * JOG.period));
  const pose: Pose = stopK > 0 ? blend(jog, kneeHoldPose(), stopK) : jog;
  const v: View = {camX: wx + 0.3, s: 320, gy: 840, cx: W * 0.45};
  const ballX = wx + 0.62 + (1 - stopK) * 0.1 * Math.sin((wx / (spd * JOG.period)) * Math.PI * 2) + stopK * 0.35;
  const pulse = t > 0.95 ? pulseOf((t - 0.95) / 0.55, 0.6) : null;
  return (
    <AbsoluteFill>
      <Sky gy={v.gy} top="#01050B" bottom="#0A2242" glow="#7CC2FF" />
      <div style={{position: 'absolute', left: -200, top: -260, width: 700, height: 700, background: 'radial-gradient(circle, rgba(170,210,255,0.32), rgba(0,0,0,0) 60%)'}} />
      <div style={{position: 'absolute', right: -200, top: -260, width: 700, height: 700, background: 'radial-gradient(circle, rgba(170,210,255,0.28), rgba(0,0,0,0) 60%)'}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Skyline v={v} par={0.1} base={v.gy - 40} seed={9} fill="#0A1B33" windows={false} />
        <rect x={0} y={v.gy - 46} width={W} height={46} fill="#0B2342" />
        <Ground v={v} marks="turf" color="#0B2A44" markColor="#1B4C6B" />
        <Shadow x={sx(v, wx)} y={v.gy} w={70} />
        <Shadow x={sx(v, ballX)} y={v.gy} w={30} />
        <Ball x={sx(v, ballX)} y={sy(v, 0.11)} r={0.11 * v.s} rot={(ballX / 0.11) * 57.3} />
        <Figure pose={pose} x={sx(v, wx)} y={v.gy} scale={v.s} knee={pulse !== null ? {color: C.redLit, pulse} : undefined} bg="#0B2A44" />
      </svg>
      <Chip text="축구선수" sub="부상 후 복귀 준비" opacity={at(t, [0.1, 0.45], [0, 1])} />
    </AbsoluteFill>
  );
};

const StairShot: React.FC<{t: number}> = ({t}) => {
  const period = 1.5;
  const tau = warp(t, (u) => 1 - 0.88 * smoothstep(0.7, 1.15, u)) + 0.15;
  const pose = stairPose(tau, period);
  const camX = pose.hip.x;
  const camY = pose.hip.y;
  const s = 270;
  const ox = W * 0.36 - camX * s;
  const oy = 760 + camY * s;
  const cyc = tau / period;
  const pulse = pulseOf(cyc, 0.4);
  const slow = smoothstep(0.7, 1.2, t);
  const steps: string[] = [];
  for (let i = -6; i < 14; i++) {
    steps.push(`L ${ox + i * STAIR.run * s} ${oy - i * STAIR.rise * s} L ${ox + (i + 1) * STAIR.run * s} ${oy - i * STAIR.rise * s} L ${ox + (i + 1) * STAIR.run * s} ${oy - (i + 1) * STAIR.rise * s}`);
  }
  const x0 = ox - 6 * STAIR.run * s;
  const y0 = oy + 6 * STAIR.rise * s;
  const rail = (x: number) => oy - ((x - ox) / s) * (STAIR.rise / STAIR.run) * s - 0.9 * s;
  return (
    <AbsoluteFill style={{background: '#071630'}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {Array.from({length: 18}).map((_, i) => (
          <line key={i} x1={0} x2={W} y1={((i * 90 + camY * s * 0.3) % 1260) - 90} y2={((i * 90 + camY * s * 0.3) % 1260) - 90} stroke="#0E2547" strokeWidth={2} />
        ))}
        <path d={`M ${x0} ${H + 20} L ${x0} ${y0} ${steps.join(' ')} L ${W + 400} ${H + 20} Z`} fill="#0D2A50" stroke="#5FA8F0" strokeWidth={2.5} strokeLinejoin="round" />
        <line x1={x0} y1={rail(x0)} x2={W + 200} y2={rail(W + 200)} stroke="#CFE6FF" strokeWidth={6} strokeLinecap="round" />
        {Array.from({length: 10}).map((_, i) => {
          const x = ox + (i * 2 - 4) * STAIR.run * s + 0.14 * s;
          const yb = oy - (i * 2 - 4) * STAIR.rise * s;
          return <line key={i} x1={x} y1={yb} x2={x} y2={rail(x)} stroke="#4A86C4" strokeWidth={3} />;
        })}
        <Figure pose={pose} x={ox} y={oy} scale={s} knee={pulse !== null ? {color: C.redLit, pulse} : undefined} bg="#0D2A50" />
      </svg>
      <Chip text="일상생활" sub="계단이 불편한 하루" opacity={at(t, [0.1, 0.45], [0, 1]) * (1 - slow)} />
      <div style={{position: 'absolute', inset: 0, background: '#01040A', opacity: slow * 0.55}} />
    </AbsoluteFill>
  );
};

export const S4Question: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const flash = Math.max(at(t, [CUT_A - 0.03, CUT_A, CUT_A + 0.14], [0, 0.5, 0]), at(t, [CUT_B - 0.03, CUT_B, CUT_B + 0.14], [0, 0.5, 0]), at(t, [0, 0.14], [0.6, 0]));
  return (
    <AbsoluteFill style={{background: C.navy}}>
      {t < CUT_A ? <RunnerShot t={t} /> : t < CUT_B ? <SoccerShot t={t - CUT_A} /> : <StairShot t={t - CUT_B} />}
      <Vignette />
      <Flash o={flash} />
      <Caption lines={[['통증이 줄었다고,'], [{t: '회복이 끝난 걸까요?', c: C.white}]]} from={3.85} to={5.97} y={150} size={84} stagger={0.35} />
      {/* thin red rule under the question */}
      <div style={{position: 'absolute', left: W / 2 - 60, top: 400, width: 120, height: 4, background: C.red, opacity: at(t, [4.5, 4.9], [0, 1]) * at(t, [5.6, 5.97], [1, 0]), scale: `${clamp((t - 4.5) / 0.4)} 1`}} />
    </AbsoluteFill>
  );
};
