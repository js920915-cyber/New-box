import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {Figure} from '../components/Figure';
import {LabBackdrop} from '../components/Hud';
import {Chip, Flash, Shadow, Vignette, warp} from '../components/Scenery';
import {RUN} from '../lib/gaits';
import {cmjForce, cmjPose, cuePose, cutState, sldlPose, squatPose} from '../lib/moves';
import {at, clamp, smoothstep} from '../lib/util';
import {C, FPS, H, W} from '../theme';

const TH = {color: C.blueLit, farColor: '#1F5C9C'};
const CUTS = [2.5, 5.0, 7.5];

const Cue: React.FC<{d: string; o: number}> = ({d, o}) => <path d={d} stroke={C.blueSoft} strokeWidth={3} strokeDasharray="10 10" fill="none" opacity={o} />;

const Check: React.FC<{x: number; y: number; o: number}> = ({x, y, o}) => (
  <g opacity={o} transform={`translate(${x} ${y})`}>
    <circle r={30} fill={C.blue} />
    <path d="M -13 1 L -3 11 L 14 -9" stroke={C.white} strokeWidth={6} fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </g>
);

const SquatShot: React.FC<{t: number}> = ({t}) => {
  const gy = 850;
  const s = 310;
  const X = W * 0.4;
  const d = 0.5 - 0.5 * Math.cos((2 * Math.PI * Math.max(0, t - 0.35)) / 1.15);
  const {pose, weight} = squatPose(d);
  const solid = smoothstep(0.05, 0.75, t);
  const tx = W * 0.7;
  const gesture = 0.5 + 0.5 * Math.sin(t * 4.2);
  const toe = pose.legN.toe;
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy} shift={200} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {/* data line settling into the floor */}
        <polyline
          points={Array.from({length: 80}, (_, k) => `${(k / 79) * W},${gy - Math.max(0, cmjForce(0.2 + (k / 79) * 2.1)) * 60 * (1 - solid)}`).join(' ')}
          fill="none"
          stroke={C.blueLit}
          strokeWidth={3}
          opacity={1 - solid * 0.6}
        />
        <Shadow x={X} y={gy} w={90} o={0.4 * solid} />
        <Figure pose={pose} x={X} y={gy} scale={s} solidity={solid} keypoints={1 - solid} bg="#0B2140" />
        <g opacity={solid}>
          <circle cx={X + weight.x * s} cy={gy - weight.y * s} r={0.085 * s} fill="#2A5A90" stroke={C.blueSoft} strokeWidth={3} />
          <path d={`M ${X + (weight.x - 0.05) * s} ${gy - (weight.y + 0.07) * s} q ${0.05 * s} ${-0.08 * s} ${0.1 * s} 0`} stroke={C.blueSoft} strokeWidth={6} fill="none" />
        </g>
        <Cue d={`M ${X + toe.x * s} ${gy} L ${X + toe.x * s} ${gy - 0.75 * s}`} o={at(t, [0.9, 1.2], [0, 1])} />
        <Check x={X + (toe.x + 0.22) * s} y={gy - 0.62 * s} o={at(t, [1.5, 1.7], [0, 1]) * clamp(d * 2)} />
        <Shadow x={tx} y={gy} w={80} o={0.4} />
        <Figure pose={cuePose(gesture)} x={tx} y={gy} scale={s * 0.92} facing={-1} color={TH.color} farColor={TH.farColor} bg="#0B2140" opacity={at(t, [0.3, 0.8], [0, 1])} />
      </svg>
      <Chip text="일상 복귀 · 하체 근력" sub="고블릿 스쿼트" opacity={at(t, [0.5, 0.9], [0, 1])} />
    </AbsoluteFill>
  );
};

const HingeShot: React.FC<{t: number}> = ({t}) => {
  const gy = 850;
  const s = 300;
  const X = W * 0.38;
  const h = 0.5 - 0.5 * Math.cos((2 * Math.PI * Math.max(0, t - 0.1)) / 2.3);
  const pose = sldlPose(h);
  const tx = W * 0.74;
  const P = (q: {x: number; y: number}) => `${X + q.x * s} ${gy - q.y * s}`;
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy} shift={700} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Shadow x={X} y={gy} w={90} />
        <Figure pose={pose} x={X} y={gy} scale={s} bg="#0B2140" />
        <rect x={X + pose.armN.wrist.x * s - 0.11 * s} y={gy - pose.armN.wrist.y * s - 0.03 * s} width={0.22 * s} height={0.06 * s} rx={8} fill="#2A5A90" stroke={C.blueSoft} strokeWidth={3} />
        <Cue d={`M ${P(pose.head)} L ${P(pose.legF.heel)}`} o={smoothstep(0.55, 0.8, h)} />
        <Check x={X - 0.15 * s} y={gy - 1.35 * s} o={smoothstep(0.85, 0.97, h)} />
        <Shadow x={tx} y={gy} w={80} o={0.4} />
        <Figure pose={cuePose(0.3 + 0.3 * Math.sin(t * 3))} x={tx} y={gy} scale={s * 0.95} facing={-1} color={TH.color} farColor={TH.farColor} bg="#0B2140" />
      </svg>
      <Chip text="러너 · 한발 운동" sub="싱글 레그 루마니안 데드리프트" />
    </AbsoluteFill>
  );
};

const HopShot: React.FC<{t: number}> = ({t}) => {
  const gy = 850;
  const s = 300;
  const X = W * 0.3;
  const tau = 0.25 + warp(t, (u) => 1 - 0.72 * smoothstep(1.2, 1.35, u) * (1 - smoothstep(2.2, 2.35, u)));
  const fwd = 0.75;
  const pose = cmjPose(tau, fwd);
  const slow = smoothstep(1.2, 1.35, t) * (1 - smoothstep(2.2, 2.35, t));
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy} shift={1100} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {/* mini hurdle */}
        <g stroke={C.blueSoft} strokeWidth={6} strokeLinecap="round">
          <line x1={X + 0.5 * s} y1={gy} x2={X + 0.5 * s} y2={gy - 0.3 * s} />
          <line x1={X + 0.5 * s - 18} y1={gy - 0.3 * s} x2={X + 0.5 * s + 18} y2={gy - 0.3 * s} />
        </g>
        <Shadow x={X + (pose.hip.x + 0.05) * s} y={gy} w={90 * clamp(1.2 - Math.max(0, Math.min(pose.legN.toe.y, pose.legN.heel.y)) * 2)} />
        <Figure pose={pose} x={X} y={gy} scale={s} kneeAngle={slow} bg="#0B2140" />
        <Shadow x={W * 0.8} y={gy} w={80} o={0.4} />
        <Figure pose={cuePose(0.2)} x={W * 0.8} y={gy} scale={s * 0.95} facing={-1} color={TH.color} farColor={TH.farColor} bg="#0B2140" />
      </svg>
      <div style={{position: 'absolute', inset: 0, boxShadow: `inset 0 0 220px rgba(8,121,216,${0.35 * slow})`}} />
      <Chip text="축구 복귀 · 점프 착지" sub="허들 홉 · 부드러운 착지" />
    </AbsoluteFill>
  );
};

const CutShot: React.FC<{t: number}> = ({t}) => {
  const gy = 860;
  const s = 270;
  const rate = (u: number) => 1 - 0.65 * smoothstep(0.7, 0.82, u) * (1 - smoothstep(1.4, 1.5, u));
  const tau = 0.15 + warp(t, rate);
  const st = cutState(tau, RUN);
  const camX = at(tau, [0, 1.0, 1.6, 2.4], [-1.6, 0.1, 0.1, -1.4]);
  const X = (wx: number) => W * 0.5 + (wx - camX) * s;
  const k = st.turn;
  const trail: string[] = [];
  for (let j = 0; j < 24; j++) {
    const q = cutState(Math.max(0.15, tau - j * 0.03), RUN);
    trail.push(`${X(q.x)},${gy + 14}`);
  }
  const slow = smoothstep(0.7, 0.82, t) * (1 - smoothstep(1.4, 1.5, t));
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy} shift={1500 + camX * 120} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {[0.75, -5.2].map((cx) => (
          <path key={cx} d={`M ${X(cx) - 26} ${gy} L ${X(cx)} ${gy - 70} L ${X(cx) + 26} ${gy} Z`} fill={C.red} stroke={C.redLit} strokeWidth={2} />
        ))}
        <polyline points={trail.join(' ')} fill="none" stroke={C.blueLit} strokeWidth={8} strokeLinecap="round" opacity={0.55} style={{filter: 'drop-shadow(0 0 10px rgba(58,160,255,0.9))'}} />
        {/* U-turn arrow above the cone during the turn */}
        <path
          d={`M ${X(0.2) - 90} ${gy - 1.95 * s} C ${X(0.2) + 40} ${gy - 1.95 * s}, ${X(0.2) + 40} ${gy - 1.55 * s}, ${X(0.2) - 90} ${gy - 1.55 * s}`}
          stroke={C.redLit}
          strokeWidth={6}
          fill="none"
          strokeLinecap="round"
          strokeDasharray="420"
          strokeDashoffset={420 * (1 - smoothstep(1.0, 1.4, tau))}
          opacity={1 - smoothstep(2.0, 2.3, tau)}
          markerEnd="url(#uarrow)"
        />
        <defs>
          <marker id="uarrow" viewBox="0 0 10 10" refX={5} refY={5} markerWidth={4} markerHeight={4} orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill={C.redLit} />
          </marker>
        </defs>
        <Shadow x={X(st.x)} y={gy} w={80} />
        <g transform={`translate(${X(st.x)} 0) scale(${Math.abs(k) < 0.08 ? 0.08 * Math.sign(k || 1) : k} 1) translate(${-X(st.x)} 0)`}>
          <Figure pose={st.pose} x={X(st.x)} y={gy} scale={s} bg="#0B2140" />
        </g>
      </svg>
      <div style={{position: 'absolute', inset: 0, boxShadow: `inset 0 0 220px rgba(8,121,216,${0.35 * slow})`}} />
      <Chip text="축구 복귀 · 방향 전환" sub="감속 · 방향 전환 · 가속" />
    </AbsoluteFill>
  );
};

export const S6Train: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const flash = Math.max(...CUTS.map((c) => at(t, [c - 0.02, c, c + 0.12], [0, 0.4, 0])));
  return (
    <AbsoluteFill style={{background: C.navy}}>
      {t < CUTS[0] ? <SquatShot t={t} /> : t < CUTS[1] ? <HingeShot t={t - CUTS[0]} /> : t < CUTS[2] ? <HopShot t={t - CUTS[1]} /> : <CutShot t={t - CUTS[2]} />}
      <Vignette k={0.5} />
      <Flash o={flash} />
      <Caption lines={[['평가를 바탕으로, ', {t: '필요한 과정', c: C.blueSoft}, '을 설계합니다.']]} from={0.7} to={4.7} y={922} size={72} />
    </AbsoluteFill>
  );
};
