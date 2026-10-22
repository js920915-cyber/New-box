import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {Figure} from '../components/Figure';
import {HudFrame, LabBackdrop, Plot, Readout} from '../components/Hud';
import {Shadow, Vignette} from '../components/Scenery';
import {kneeFlexion, Pose, v} from '../lib/body';
import {Cam, linePath, P3, projectPoint} from '../lib/cam3d';
import {gaitPose, gaitSpeed, RUN} from '../lib/gaits';
import {cmjForce, cmjJumpHeight, cmjPose, CMJ, kneelReachPose, pointPose, seatedPose, squatPose, standPose} from '../lib/moves';
import {at, clamp, EASE, smoothstep} from '../lib/util';
import {C, FONT, FPS, H, W} from '../theme';

const THERAPIST = {color: C.blueLit, farColor: '#1F5C9C'};

// ---------- 01 AI running analysis ----------
const RunPanel: React.FC<{t: number}> = ({t}) => {
  const gy = 850;
  const s = 300;
  const X = W * 0.33;
  const phase = t / RUN.period + 0.2;
  const pose = gaitPose(RUN, phase);
  const belt = (t * gaitSpeed(RUN) * s) % 60;
  const knee = kneeFlexion(pose.hip, pose.legN);
  const win = 1.4;
  const pw = 640;
  const ph = 300;
  const pts: string[] = [];
  for (let k = 0; k <= 70; k++) {
    const tt = t - win + (k / 70) * win;
    const p = gaitPose(RUN, tt / RUN.period + 0.2);
    pts.push(`${((k / 70) * pw).toFixed(1)},${(ph - (kneeFlexion(p.hip, p.legN) / 120) * ph).toFixed(1)}`);
  }
  const box = {x0: X - 0.75 * s, x1: X + 0.75 * s, y0: gy - 1.95 * s, y1: gy + 0.08 * s};
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy + 0.17 * s} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {/* treadmill */}
        <rect x={X - 1.05 * s} y={gy} width={2.1 * s} height={0.17 * s} rx={18} fill="#123660" stroke="#5FA8F0" strokeWidth={2} />
        {Array.from({length: 12}).map((_, i) => (
          <line key={i} x1={X - 1.0 * s + ((i * 60 - belt + 720) % 720)} x2={X - 1.0 * s + ((i * 60 - belt + 720) % 720) + 24} y1={gy + 4} y2={gy + 4} stroke="#9CD0FF" strokeOpacity={0.6} strokeWidth={3} />
        ))}
        <line x1={X + 0.98 * s} y1={gy} x2={X + 1.12 * s} y2={gy - 1.2 * s} stroke="#5FA8F0" strokeWidth={8} strokeLinecap="round" />
        <rect x={X + 1.02 * s} y={gy - 1.32 * s} width={0.32 * s} height={0.14 * s} rx={8} fill="#123660" stroke="#5FA8F0" strokeWidth={2} />
        <Figure pose={pose} x={X} y={gy} scale={s} keypoints={1} kneeAngle={1} bg="#0B2140" />
        {/* AI tracking box */}
        <path
          d={`M ${box.x0} ${box.y0 + 40} L ${box.x0} ${box.y0} L ${box.x0 + 40} ${box.y0} M ${box.x1 - 40} ${box.y0} L ${box.x1} ${box.y0} L ${box.x1} ${box.y0 + 40} M ${box.x0} ${box.y1 - 40} L ${box.x0} ${box.y1} L ${box.x0 + 40} ${box.y1} M ${box.x1 - 40} ${box.y1} L ${box.x1} ${box.y1} L ${box.x1} ${box.y1 - 40}`}
          stroke={C.blueLit}
          strokeWidth={3}
          fill="none"
        />
        <text x={box.x0} y={box.y0 - 14} fill={C.blueSoft} fontFamily={FONT} fontSize={24} fontWeight={700} letterSpacing={3}>
          AI POSE TRACKING
        </text>
      </svg>
      <Plot x={1150} y={430} w={pw} h={ph} grid={[ph, ph - (45 / 120) * ph, ph - (90 / 120) * ph]}>
        <polyline points={pts.join(' ')} fill="none" stroke={C.blueLit} strokeWidth={4} strokeLinejoin="round" />
        <circle cx={pw} cy={ph - (knee / 120) * ph} r={9} fill={C.white} />
        <text x={0} y={ph + 52} fill={C.muted} fontFamily={FONT} fontSize={22} fontWeight={700}>
          무릎 굴곡 각도 · 최근 1.4초
        </text>
      </Plot>
      <Readout x={1150} y={250} label="무릎 굴곡" value={`${Math.round(knee)}°`} />
      <Readout x={1480} y={250} label="케이던스" value={`${Math.round(120 / RUN.period)}`} unit="spm" />
    </AbsoluteFill>
  );
};

// ---------- 02 handheld dynamometer ----------
const HHD = {left: 312, right: 268};
const StrengthPanel: React.FC<{t: number}> = ({t}) => {
  const gy = 820;
  const s = 340;
  const X = W * 0.25;
  const effort = smoothstep(0.15, 0.6, t);
  const seatY = 0.62;
  const client = seatedPose(seatY, effort);
  const dev = v(client.legN.ankle.x + 0.07, client.legN.ankle.y + 0.07);
  const Xt = dev.x + 0.68;
  const tester = kneelReachPose(v(Xt - dev.x - 0.02, dev.y));
  const f = (u: number) => (u < 0.15 ? 0 : HHD.right * (1 - Math.exp(-(u - 0.15) / 0.16)) * (1 + 0.01 * Math.sin(u * 40)));
  const pw = 560;
  const ph = 300;
  const pts: string[] = [];
  for (let k = 0; k <= 60; k++) {
    const u = (k / 60) * Math.min(t, 1.5);
    pts.push(`${((u / 1.5) * pw).toFixed(1)},${(ph - (f(u) / 360) * ph).toFixed(1)}`);
  }
  const lsi = Math.round((HHD.right / HHD.left) * 100);
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy} shift={300} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {/* plinth */}
        <rect x={X - 0.5 * s} y={gy - seatY * s} width={0.92 * s} height={0.1 * s} rx={10} fill="#1B4475" stroke="#5FA8F0" strokeWidth={2} />
        {[-0.42, 0.32].map((dx) => (
          <line key={dx} x1={X + dx * s} x2={X + dx * s} y1={gy - (seatY - 0.1) * s} y2={gy} stroke="#2D5E95" strokeWidth={10} />
        ))}
        <Shadow x={X} y={gy} w={170} o={0.35} />
        <Figure pose={client} x={X} y={gy} scale={s} bg="#0B2140" />
        <Figure pose={tester} x={X + Xt * s} y={gy} scale={s} facing={-1} color={THERAPIST.color} farColor={THERAPIST.farColor} bg="#0B2140" />
        <rect x={X + (dev.x - 0.015) * s} y={gy - (dev.y + 0.07) * s} width={0.075 * s} height={0.14 * s} rx={8} fill={C.white} stroke={C.red} strokeWidth={4} />
        {effort > 0.05 ? (
          <path d={`M ${X + (dev.x + 0.11) * s} ${gy - dev.y * s} l ${-40 * effort} 0 m 0 0 l 14 -10 m -14 10 l 14 10`} stroke={C.redLit} strokeWidth={4} fill="none" opacity={effort} />
        ) : null}
      </svg>
      <Plot x={1180} y={400} w={pw} h={ph} grid={[ph, ph - (HHD.left / 360) * ph]}>
        <line x1={0} x2={pw} y1={ph - (HHD.left / 360) * ph} y2={ph - (HHD.left / 360) * ph} stroke={C.mist} strokeWidth={2} strokeDasharray="10 8" />
        <text x={pw} y={ph - (HHD.left / 360) * ph - 12} textAnchor="end" fill={C.mist} fontFamily={FONT} fontSize={22} fontWeight={700}>
          좌 {HHD.left} N
        </text>
        <polyline points={pts.join(' ')} fill="none" stroke={C.blueLit} strokeWidth={4} />
        <text x={0} y={ph + 52} fill={C.muted} fontFamily={FONT} fontSize={22} fontWeight={700}>
          무릎 폄 등척성 근력 · 휴대용 근력계
        </text>
      </Plot>
      <Readout x={1180} y={220} label="우측" value={`${Math.round(f(Math.min(t, 1.5)))}`} unit="N" />
      <Readout x={1500} y={220} label="좌우 비율 (LSI)" value={`${lsi}%`} color={C.blueSoft} opacity={at(t, [0.9, 1.15], [0, 1])} />
    </AbsoluteFill>
  );
};

// ---------- 03 force plate jump & landing ----------
const T0 = 0.2;
const LANDING_PEAK = Math.max(...Array.from({length: 200}, (_, i) => cmjForce(CMJ.land + i / 400)));
const JumpPanel: React.FC<{t: number}> = ({t}) => {
  const gy = 800;
  const s = 300;
  const X = W * 0.3;
  const tau = t + T0;
  const pose = cmjPose(tau);
  const plateH = 0.05;
  const F = cmjForce(tau);
  const pw = 620;
  const ph = 320;
  const span = 2.1;
  const pts: string[] = [];
  for (let k = 0; k <= 160; k++) {
    const u = T0 + (k / 160) * span;
    if (u > tau) break;
    pts.push(`${(((u - T0) / span) * pw).toFixed(1)},${(ph - (cmjForce(u) / 4) * ph).toFixed(1)}`);
  }
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy} shift={620} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <rect x={X - 0.42 * s} y={gy - plateH * s} width={0.84 * s} height={plateH * s} rx={6} fill="#1E6FC8" stroke="#9CD0FF" strokeWidth={2} style={{filter: 'drop-shadow(0 0 16px rgba(58,160,255,0.8))'}} />
        <Shadow x={X} y={gy - plateH * s} w={90 * clamp(1 - Math.max(0, pose.legN.toe.y - 0.06) * 2)} />
        {F > 0.02 ? <line x1={X + 0.05 * s} y1={gy - plateH * s} x2={X + 0.05 * s} y2={gy - plateH * s - F * 0.32 * s} stroke={C.redLit} strokeWidth={6} markerEnd="url(#arrow)" /> : null}
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX={5} refY={5} markerWidth={4} markerHeight={4} orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill={C.redLit} />
          </marker>
        </defs>
        <Figure pose={pose} x={X} y={gy - plateH * s} scale={s} bg="#0B2140" />
      </svg>
      <Plot x={1120} y={420} w={pw} h={ph} grid={[ph, ph - ph / 4, ph - ph / 2, ph - (3 * ph) / 4]}>
        <text x={pw + 12} y={ph - ph / 4 + 8} fill={C.muted} fontFamily={FONT} fontSize={20} fontWeight={700}>
          1×
        </text>
        <text x={pw + 12} y={ph - (3 * ph) / 4 + 8} fill={C.muted} fontFamily={FONT} fontSize={20} fontWeight={700}>
          3×
        </text>
        <polyline points={pts.join(' ')} fill="none" stroke={C.blueLit} strokeWidth={4} strokeLinejoin="round" />
        <text x={0} y={ph + 52} fill={C.muted} fontFamily={FONT} fontSize={22} fontWeight={700}>
          수직 지면반력 (체중 배수)
        </text>
      </Plot>
      <Readout x={1120} y={230} label="점프 높이" value={`${Math.round(cmjJumpHeight * 100)}`} unit="cm" opacity={at(tau, [CMJ.land, CMJ.land + 0.15], [0, 1])} />
      <Readout x={1440} y={230} label="착지 최대 힘" value={`${LANDING_PEAK.toFixed(1)}×`} unit="체중" color={C.blueSoft} opacity={at(tau, [CMJ.absorbed - 0.05, CMJ.absorbed + 0.1], [0, 1])} />
    </AbsoluteFill>
  );
};

// ---------- 04 3D motion analysis ----------
const to3D = (p: Pose): {pts: Record<string, P3>; bones: [string, string][]} => {
  const L = (q: {x: number; y: number}, z: number): P3 => [q.x, q.y, z];
  const pts: Record<string, P3> = {
    head: L(p.head, 0),
    nck: L(p.shoulder, 0),
    shR: L(p.shoulder, 0.19),
    shL: L(p.shoulder, -0.19),
    elR: L(p.armN.elbow, 0.24),
    elL: L(p.armF.elbow, -0.24),
    wrR: L(p.armN.wrist, 0.16),
    wrL: L(p.armF.wrist, -0.16),
    hpR: L(p.hip, 0.11),
    hpL: L(p.hip, -0.11),
    knR: L(p.legN.knee, 0.13),
    knL: L(p.legF.knee, -0.13),
    anR: L(p.legN.ankle, 0.13),
    anL: L(p.legF.ankle, -0.13),
    toR: L(p.legN.toe, 0.15),
    toL: L(p.legF.toe, -0.15),
  };
  const bones: [string, string][] = [
    ['head', 'nck'], ['shR', 'shL'], ['shR', 'elR'], ['elR', 'wrR'], ['shL', 'elL'], ['elL', 'wrL'],
    ['nck', 'hpR'], ['nck', 'hpL'], ['hpR', 'hpL'], ['hpR', 'knR'], ['knR', 'anR'], ['anR', 'toR'], ['hpL', 'knL'], ['knL', 'anL'], ['anL', 'toL'],
  ];
  return {pts, bones};
};

const MotionPanel: React.FC<{t: number}> = ({t}) => {
  const d = (u: number) => 0.5 - 0.5 * Math.cos((2 * Math.PI * u) / 1.5);
  const pose = squatPose(d(t)).pose;
  const {pts, bones} = to3D(pose);
  const yaw = at(t, [0, 2.0], [-58, 24]);
  const pitch = 10;
  const R = 3.6;
  const r = (Math.PI / 180);
  const target: P3 = [0, 0.82, 0];
  const fwd: P3 = [Math.sin(yaw * r) * Math.cos(pitch * r), -Math.sin(pitch * r), Math.cos(yaw * r) * Math.cos(pitch * r)];
  const cam: Cam = {pos: [target[0] - fwd[0] * R, target[1] - fwd[1] * R, target[2] - fwd[2] * R], yaw, pitch, f: 1500, cx: W * 0.36, cy: H * 0.5, near: 0.1};
  const grid: React.ReactNode[] = [];
  for (let k = -6; k <= 6; k++) {
    const a = linePath(cam, [k * 0.25, 0, -1.5], [k * 0.25, 0, 1.5]);
    const b = linePath(cam, [-1.5, 0, k * 0.25], [1.5, 0, k * 0.25]);
    if (a) grid.push(<path key={'a' + k} d={a.d} stroke="#1E4878" strokeWidth={1.5} />);
    if (b) grid.push(<path key={'b' + k} d={b.d} stroke="#1E4878" strokeWidth={1.5} />);
  }
  const trail: string[] = [];
  for (let k = 0; k <= 30; k++) {
    const u = Math.max(0, t - 1 + k / 30);
    const q = squatPose(d(u)).pose;
    const pp = projectPoint(cam, [q.legN.knee.x, q.legN.knee.y, 0.13]);
    if (pp) trail.push(`${pp.x.toFixed(1)},${pp.y.toFixed(1)}`);
  }
  const knee = kneeFlexion(pose.hip, pose.legN);
  return (
    <AbsoluteFill>
      <LabBackdrop gy={760} shift={940} />
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(circle at 36% 55%, rgba(8,121,216,0.18), rgba(0,0,0,0) 45%)'}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {grid}
        <polyline points={trail.join(' ')} fill="none" stroke={C.redLit} strokeWidth={3} strokeOpacity={0.9} />
        {bones.map(([a, b], i) => {
          const l = linePath(cam, pts[a], pts[b]);
          return l ? <path key={i} d={l.d} stroke={C.blueSoft} strokeWidth={4} strokeLinecap="round" /> : null;
        })}
        {Object.entries(pts).map(([k, p]) => {
          const q = projectPoint(cam, p);
          if (!q) return null;
          return <circle key={k} cx={q.x} cy={q.y} r={Math.max(6, 34 / q.z)} fill={k.startsWith('kn') ? C.redLit : C.white} stroke="#0B2140" strokeWidth={3} />;
        })}
      </svg>
      <Readout x={1200} y={300} label="무릎 굴곡 (우)" value={`${Math.round(knee)}°`} />
      <Readout x={1200} y={460} label="추적 관절 마커" value={`${Object.keys(pts).length}`} unit="개" color={C.blueSoft} size={52} />
      <div style={{position: 'absolute', left: 1200, top: 620, width: 560, fontFamily: FONT, fontSize: 26, fontWeight: 500, color: C.mist, lineHeight: 1.5}}>
        관절 위치를 여러 방향에서 확인하고
        <br />
        움직임 궤적을 비교합니다.
      </div>
    </AbsoluteFill>
  );
};

// ---------- 05 explaining the results ----------
const ResultPanel: React.FC<{t: number}> = ({t}) => {
  const gy = 840;
  const s = 270;
  const tx = 360;
  const cx = 1560;
  const point = at(t, [0.15, 0.6], [5, 62], EASE);
  const therapist = pointPose(point, Math.sin(t * 5) * 0.3);
  const client = standPose({head: -2, shN: 4, shF: -2});
  const sc = {x: 520, y: 150, w: 880, h: 500};
  const reveal = (k: number) => at(t, [0.25 + k * 0.18, 0.6 + k * 0.18], [0, 1], EASE);
  const curve: string[] = [];
  for (let k = 0; k <= 60; k++) {
    const u = T0 + (k / 60) * 2.1;
    curve.push(`${(k / 60) * 230},${110 - cmjForce(u) * 26}`);
  }
  return (
    <AbsoluteFill>
      <LabBackdrop gy={gy} shift={1300} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <rect x={sc.x} y={sc.y} width={sc.w} height={sc.h} rx={24} fill="#071A33" stroke="#3A78B8" strokeWidth={3} />
        <rect x={sc.x + sc.w / 2 - 6} y={sc.y + sc.h} width={12} height={gy - sc.y - sc.h} fill="#1E4878" />
        <text x={sc.x + 50} y={sc.y + 72} fill={C.white} fontFamily={FONT} fontWeight={800} fontSize={40}>
          평가 요약
        </text>
        <g opacity={reveal(0)} transform={`translate(${sc.x + 50} ${sc.y + 130})`}>
          <text y={0} fill={C.mist} fontFamily={FONT} fontWeight={700} fontSize={24}>무릎 폄 근력</text>
          <rect y={30} width={230 * (HHD.left / 360) * reveal(0)} height={34} rx={6} fill={C.blueSoft} />
          <rect y={80} width={230 * (HHD.right / 360) * reveal(0)} height={34} rx={6} fill={C.blueLit} />
          <text x={0} y={160} fill={C.white} fontFamily={FONT} fontWeight={800} fontSize={34}>LSI {Math.round((HHD.right / HHD.left) * 100)}%</text>
        </g>
        <g opacity={reveal(1)} transform={`translate(${sc.x + 330} ${sc.y + 130})`}>
          <text y={0} fill={C.mist} fontFamily={FONT} fontWeight={700} fontSize={24}>점프·착지</text>
          <polyline points={curve.join(' ')} fill="none" stroke={C.blueLit} strokeWidth={3} transform="translate(0 30)" />
          <text x={0} y={190} fill={C.white} fontFamily={FONT} fontWeight={800} fontSize={34}>{Math.round(cmjJumpHeight * 100)} cm</text>
        </g>
        <g opacity={reveal(2)} transform={`translate(${sc.x + 610} ${sc.y + 130})`}>
          <text y={0} fill={C.mist} fontFamily={FONT} fontWeight={700} fontSize={24}>러닝</text>
          <circle cx={100} cy={100} r={64} fill="none" stroke="#1E4878" strokeWidth={14} />
          <circle cx={100} cy={100} r={64} fill="none" stroke={C.blueLit} strokeWidth={14} strokeDasharray={`${402 * 0.78 * reveal(2)} 402`} transform="rotate(-90 100 100)" />
          <text x={100} y={112} textAnchor="middle" fill={C.white} fontFamily={FONT} fontWeight={800} fontSize={34}>{Math.round(120 / RUN.period)}</text>
          <text x={0} y={210} fill={C.mist} fontFamily={FONT} fontWeight={700} fontSize={22}>케이던스 spm</text>
        </g>
        <Shadow x={tx} y={gy} w={80} />
        <Shadow x={cx} y={gy} w={80} />
        <Figure pose={therapist} x={tx} y={gy} scale={s} color={THERAPIST.color} farColor={THERAPIST.farColor} bg="#0B2140" />
        <Figure pose={client} x={cx} y={gy} scale={s} facing={-1} bg="#0B2140" />
      </svg>
    </AbsoluteFill>
  );
};

const PANELS: {from: number; to: number; C: React.FC<{t: number}>; index: string; title: string; sub: string}[] = [
  {from: 0, to: 2.0, C: RunPanel, index: '01', title: 'AI 러닝 분석', sub: 'RUNNING ANALYSIS'},
  {from: 2.0, to: 3.5, C: StrengthPanel, index: '02', title: '근력 평가', sub: 'HANDHELD DYNAMOMETRY'},
  {from: 3.5, to: 5.5, C: JumpPanel, index: '03', title: '점프·착지 평가', sub: 'FORCE PLATE'},
  {from: 5.5, to: 7.5, C: MotionPanel, index: '04', title: '3D 움직임 분석', sub: '3D MOTION ANALYSIS'},
  {from: 7.5, to: 10.0, C: ResultPanel, index: '05', title: '결과 설명', sub: 'REVIEW & EXPLAIN'},
];

export const S5Assess: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const i = Math.max(0, PANELS.findIndex((p) => t >= p.from && t < p.to));
  const P = PANELS[i];
  const wipe = clamp((t - P.from) / 0.28);
  const prev = i > 0 && wipe < 1 ? PANELS[i - 1] : null;
  const lineX = W * EASE(wipe);
  return (
    <AbsoluteFill style={{background: C.navy}}>
      {prev ? (
        <AbsoluteFill style={{clipPath: `inset(0 0 0 ${lineX}px)`}}>
          <prev.C t={prev.to - prev.from} />
          <HudFrame index={prev.index} title={prev.title} sub={prev.sub} />
        </AbsoluteFill>
      ) : null}
      <AbsoluteFill style={{clipPath: prev ? `inset(0 ${W - lineX}px 0 0)` : undefined}}>
        <P.C t={t - P.from} />
        <HudFrame index={P.index} title={P.title} sub={P.sub} />
      </AbsoluteFill>
      {prev ? <div style={{position: 'absolute', top: 0, bottom: 0, left: lineX - 2, width: 4, background: '#DCEFFF', boxShadow: '0 0 30px 8px rgba(58,160,255,0.8)'}} /> : null}
      <Vignette k={0.5} />
      <Caption lines={[['우리는 먼저 ', {t: '평가', c: C.blueSoft}, '합니다.']]} from={7.9} to={9.97} y={918} size={80} />
    </AbsoluteFill>
  );
};
