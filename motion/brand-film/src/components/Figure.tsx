import React from 'react';
import {Arm, kneeFlexion, Leg, Pose, V} from '../lib/body';
import {C, FONT} from '../theme';

export type FigureProps = {
  pose: Pose;
  x: number; // screen px of world origin
  y: number;
  scale: number; // px per meter
  facing?: 1 | -1;
  color?: string;
  farColor?: string;
  bg?: string; // used for the separation outline between overlapping limbs
  solidity?: number; // 1 = pictogram, 0 = thin analysis skeleton
  keypoints?: number; // opacity of the joint-marker overlay
  knee?: {color: string; pulse: number}; // highlight ring at the near knee
  kneeAngle?: number; // opacity of the live knee-angle readout
  opacity?: number;
};

const W = {trunk: 0.17, thigh: 0.125, shank: 0.1, upper: 0.088, fore: 0.078, foot: 0.07, head: 0.105};

export const Figure: React.FC<FigureProps> = ({
  pose,
  x,
  y,
  scale,
  facing = 1,
  color = C.white,
  farColor = '#7F98B5',
  bg = C.navy,
  solidity = 1,
  keypoints = 0,
  knee,
  kneeAngle = 0,
  opacity = 1,
}) => {
  const P = (q: V) => [x + facing * q.x * scale, y - q.y * scale] as const;
  const w = (m: number) => Math.max(2.5, m * scale * solidity + 2.5 * (1 - solidity));
  const seg = (a: V, b: V, width: number, col: string, outline: boolean, key: string) => {
    const [x1, y1] = P(a);
    const [x2, y2] = P(b);
    return (
      <g key={key}>
        {outline && solidity > 0.5 ? (
          <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={bg} strokeWidth={w(width) + 0.03 * scale} strokeLinecap="round" />
        ) : null}
        <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={col} strokeWidth={w(width)} strokeLinecap="round" />
      </g>
    );
  };
  const leg = (l: Leg, col: string, outline: boolean, k: string) => (
    <g key={k}>
      {seg(pose.hip, l.knee, W.thigh, col, outline, k + 't')}
      {seg(l.knee, l.ankle, W.shank, col, outline, k + 's')}
      {seg(l.heel, l.toe, W.foot, col, false, k + 'f')}
      {seg(l.ankle, {x: (l.heel.x + l.toe.x) / 2 - (l.toe.x - l.heel.x) * 0.15, y: (l.heel.y + l.toe.y) / 2}, W.foot, col, false, k + 'a')}
    </g>
  );
  const arm = (a: Arm, col: string, outline: boolean, k: string) => (
    <g key={k}>
      {seg(pose.shoulder, a.elbow, W.upper, col, outline, k + 'u')}
      {seg(a.elbow, a.wrist, W.fore, col, outline, k + 'f')}
    </g>
  );
  const [hx, hy] = P(pose.head);
  const [kx, ky] = P(pose.legN.knee);
  const joints = [pose.head, pose.shoulder, pose.armN.elbow, pose.armN.wrist, pose.hip, pose.legN.knee, pose.legN.ankle, pose.legN.toe, pose.legF.knee, pose.legF.ankle];
  const flex = kneeFlexion(pose.hip, pose.legN);
  const [hipX, hipY] = P(pose.hip);
  const [ax, ay] = P(pose.legN.ankle);
  const unit = (dx: number, dy: number) => {
    const l = Math.hypot(dx, dy) || 1;
    return [dx / l, dy / l] as const;
  };
  const ext = unit(kx - hipX, ky - hipY); // thigh line extended through the knee
  const shk = unit(ax - kx, ay - ky);
  const sweep = ext[0] * shk[1] - ext[1] * shk[0] > 0 ? 1 : 0;
  const r = 0.2 * scale;
  return (
    <g opacity={opacity}>
      {arm(pose.armF, farColor, false, 'af')}
      {leg(pose.legF, farColor, false, 'lf')}
      {seg(pose.hip, pose.shoulder, W.trunk, color, false, 'tr')}
      <circle cx={hx} cy={hy} r={Math.max(4, W.head * scale * (0.35 + 0.65 * solidity))} fill={solidity > 0.2 ? color : 'none'} stroke={color} strokeWidth={2.5} />
      {leg(pose.legN, color, true, 'ln')}
      {arm(pose.armN, color, true, 'an')}
      {knee ? (
        <g>
          <circle cx={kx} cy={ky} r={0.07 * scale + knee.pulse * 0.12 * scale} fill="none" stroke={knee.color} strokeWidth={3 + 3 * (1 - knee.pulse)} opacity={1 - knee.pulse * 0.85} />
          <circle cx={kx} cy={ky} r={0.06 * scale} fill={knee.color} opacity={0.55} />
        </g>
      ) : null}
      {keypoints > 0 ? (
        <g opacity={keypoints}>
          {[
            [pose.head, pose.shoulder], [pose.shoulder, pose.hip], [pose.shoulder, pose.armN.elbow], [pose.armN.elbow, pose.armN.wrist],
            [pose.hip, pose.legN.knee], [pose.legN.knee, pose.legN.ankle], [pose.legN.ankle, pose.legN.toe],
            [pose.hip, pose.legF.knee], [pose.legF.knee, pose.legF.ankle],
          ].map(([a, b], i) => {
            const [x1, y1] = P(a);
            const [x2, y2] = P(b);
            return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={C.blueLit} strokeWidth={2} />;
          })}
          {joints.map((j, i) => {
            const [jx, jy] = P(j);
            return <circle key={i} cx={jx} cy={jy} r={7} fill={C.navy} stroke={C.blueSoft} strokeWidth={2.5} />;
          })}
        </g>
      ) : null}
      {kneeAngle > 0 ? (
        <g opacity={kneeAngle}>
          <line x1={kx} y1={ky} x2={kx + ext[0] * r * 1.4} y2={ky + ext[1] * r * 1.4} stroke={C.blueSoft} strokeWidth={2} strokeDasharray="6 6" />
          <path
            d={`M ${kx + ext[0] * r} ${ky + ext[1] * r} A ${r} ${r} 0 0 ${sweep} ${kx + shk[0] * r} ${ky + shk[1] * r}`}
            fill="none"
            stroke={C.blueLit}
            strokeWidth={3}
          />
          <text x={kx + facing * 0.32 * scale} y={ky + 12} fill={C.white} fontFamily={FONT} fontSize={34} fontWeight={800} textAnchor={facing === 1 ? 'start' : 'end'} style={{fontVariantNumeric: 'tabular-nums'}}>
            {Math.round(flex)}°
          </text>
        </g>
      ) : null}
    </g>
  );
};
