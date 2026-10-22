import React, {useMemo} from 'react';
import {seeded} from '../lib/cam3d';
import {W, H} from '../theme';

// Star field seen by a camera moving forward by `travel` (scene units); `streak` draws motion blur.
export const Stars: React.FC<{travel: number; streak?: number; opacity?: number; twinkle?: number}> = ({travel, streak = 0, opacity = 1, twinkle = 0}) => {
  const stars = useMemo(() => {
    const r = seeded(11);
    return Array.from({length: 900}, () => ({
      x: (r() - 0.5) * 2.2,
      y: (r() - 0.5) * 1.3,
      z: 0.6 + r() * 9,
      m: Math.pow(r(), 3),
      p: r() * 6.28,
    }));
  }, []);
  const f = W * 0.5;
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0, opacity}}>
      {stars.map((s, i) => {
        const z = s.z - travel;
        if (z <= 0.05) return null;
        const x = W / 2 + (f * s.x) / z;
        const y = H / 2 + (f * s.y) / z;
        if (x < -50 || x > W + 50 || y < -50 || y > H + 50) return null;
        const size = 0.6 + s.m * 2.2 + 1.2 / z;
        const tw = 0.65 + 0.35 * Math.sin(s.p + twinkle * (1 + s.m * 3));
        const a = Math.min(1, (0.35 + s.m * 0.9) * tw * Math.min(1, 3 / z));
        if (streak > 0.001) {
          const z0 = z + streak;
          const x0 = W / 2 + (f * s.x) / z0;
          const y0 = H / 2 + (f * s.y) / z0;
          return <line key={i} x1={x0} y1={y0} x2={x} y2={y} stroke="#DCEBFF" strokeOpacity={a} strokeWidth={size} strokeLinecap="round" />;
        }
        return <circle key={i} cx={x} cy={y} r={size} fill="#DCEBFF" fillOpacity={a} />;
      })}
    </svg>
  );
};
