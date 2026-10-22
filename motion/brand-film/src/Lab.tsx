// Development sheets for visual QA of the movement library.
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Figure} from './components/Figure';
import {gaitPose, RUN, WALK, JOG, stairPose, STAIR} from './lib/gaits';
import {cmjPose, cmjForce, CMJ, cutState, cuePose, kneeHoldPose, pointPose, reachPose, seatedPose, sldlPose, squatPose} from './lib/moves';
import {C} from './theme';

export const Lab: React.FC = () => {
  const frame = useCurrentFrame();
  const rows = [RUN, JOG, WALK];
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: 'RCardnews'}}>
      <svg width={1920} height={1080}>
        {rows.map((g, r) => (
          <g key={r}>
            <line x1={0} x2={1920} y1={300 + r * 300} y2={300 + r * 300} stroke={C.line} />
            {Array.from({length: 8}).map((_, i) => (
              <Figure key={i} pose={gaitPose(g, i / 8 + frame / 30 / g.period)} x={120 + i * 230} y={300 + r * 300} scale={140} kneeAngle={i === 0 ? 1 : 0} />
            ))}
          </g>
        ))}
      </svg>
    </AbsoluteFill>
  );
};

export const MoveLab: React.FC = () => {
  const s = 120;
  const row = (y: number, poses: {p: ReturnType<typeof sldlPose>; facing?: 1 | -1}[]) =>
    poses.map((q, i) => <Figure key={i} pose={q.p} x={110 + i * 210} y={y} scale={s} facing={q.facing} kneeAngle={1} />);
  return (
    <AbsoluteFill style={{background: C.navy, fontFamily: 'RCardnews'}}>
      <svg width={1920} height={1080}>
        {[250, 520, 790, 1060].map((y) => <line key={y} x1={0} x2={1920} y1={y} y2={y} stroke={C.line} />)}
        {row(250, [0, 0.33, 0.66, 1].map((d) => ({p: squatPose(d).pose})).concat([0, 0.5, 1].map((h) => ({p: sldlPose(h)}))).concat([{p: kneeHoldPose()}, {p: cuePose(1)}]))}
        {row(520, [0.2, 0.6, 0.85, 1.0, 1.15, 1.3, 1.45, 1.65, 1.85].map((t) => ({p: cmjPose(t)})))}
        {row(790, [0.3, 0.8, 1.0, 1.1, 1.3, 1.45, 1.6, 1.7, 2.0].map((t) => {
          const c = cutState(t, RUN);
          return {p: c.pose, facing: (c.turn >= 0 ? 1 : -1) as 1 | -1};
        }))}
        {row(1060, [{p: seatedPose(0.55, 1)}, {p: reachPose({x: 0.3, y: 0.3}, 0.9)}, {p: pointPose(80)}, {p: stairPose(0.3)}])}
        <polyline fill="none" stroke={C.blueLit} strokeWidth={3} points={Array.from({length: 300}, (_, i) => { const t = i / 100; return `${1000 + i * 3},${1000 - cmjForce(t) * 60}`; }).join(' ')} />
        <line x1={1000} x2={1900} y1={940} y2={940} stroke={C.muted} />
        <text x={1000} y={900} fill="white" fontSize={24}>{`peak ${Math.max(...Array.from({length: 300}, (_, i) => cmjForce(i / 100))).toFixed(2)} BW, takeoff ${CMJ.takeoff}`}</text>
      </svg>
    </AbsoluteFill>
  );
};

export const StairLab: React.FC = () => {
  const frame = useCurrentFrame();
  const s = 160;
  return (
    <AbsoluteFill style={{background: C.navy}}>
      <svg width={1920} height={1080}>
        {Array.from({length: 4}).map((_, k) => {
          const pose = stairPose(k * 0.275 + frame / 30);
          const ox = 100 + k * 460 - pose.hip.x * s;
          const oy = 400 + pose.hip.y * s;
          const steps = [];
          for (let i = 0; i < 12; i++) steps.push(`L ${ox + i * STAIR.run * s} ${oy - i * STAIR.rise * s} L ${ox + (i + 1) * STAIR.run * s} ${oy - i * STAIR.rise * s} L ${ox + (i + 1) * STAIR.run * s} ${oy - (i + 1) * STAIR.rise * s}`);
          return (
            <g key={k}>
              <path d={`M ${ox} ${oy} ${steps.join(' ')}`} fill="none" stroke={C.blueSoft} strokeWidth={2} />
              <Figure pose={pose} x={ox} y={oy} scale={s} />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
