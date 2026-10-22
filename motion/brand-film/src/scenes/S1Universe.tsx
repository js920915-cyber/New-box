import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Caption} from '../components/Caption';
import {Arc, Globe} from '../components/Globe';
import {Stars} from '../components/Stars';
import {at, INOUT} from '../lib/util';
import {C, FPS} from '../theme';

// Shared with scene 2 so the zoom continues without a seam.
export const S1_END = {scale: 655, center: [118, 30] as [number, number], logVel: 0.33};
export const s1Scale = (t: number) => 230 + 20 * t + 2.6 * t * t * t;
export const s1Center = (t: number): [number, number] => [at(t, [0, 5], [104, S1_END.center[0]], INOUT), at(t, [0, 5], [18, S1_END.center[1]], INOUT)];
export const starTravel = (t: number) => 0.12 * t + 0.15 * t * t;

export const S1_ARCS: Arc[] = [
  ['tokyo', 'singapore'], ['beijing', 'sydney'], ['shanghai', 'delhi'], ['manila', 'osaka'], ['hongkong', 'vladivostok'],
  ['bangkok', 'tokyo'], ['jakarta', 'shanghai'], ['taipei', 'ulaanbaatar'], ['perth', 'hanoi'], ['guam', 'beijing'],
  ['sapporo', 'singapore'], ['delhi', 'tokyo'], ['busan', 'manila'], ['sydney', 'hongkong'],
].map(([from, to], i) => ({from, to, start: 1.5 + i * 0.22, dur: 1.5}));

export const S1Universe: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const speed = 0.12 + 0.3 * t;
  return (
    <AbsoluteFill style={{background: C.space}}>
      <Stars travel={starTravel(t)} streak={Math.max(0, speed - 0.9) * 0.25} opacity={at(t, [0.15, 1.2], [0, 1])} twinkle={t * 2} />
      <AbsoluteFill style={{opacity: at(t, [0.5, 2.2], [0, 1])}}>
        <Globe
          t={t}
          scale={s1Scale(t)}
          center={s1Center(t)}
          sunAngle={at(t, [0.4, 4.6], [174, 72], INOUT)}
          arcs={S1_ARCS}
          night={1}
        />
      </AbsoluteFill>
      <Caption lines={[['수많은 움직임이 존재하는 지구.']]} from={1.5} to={4.75} y={880} size={78} />
    </AbsoluteFill>
  );
};
