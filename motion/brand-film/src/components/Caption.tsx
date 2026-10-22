import React from 'react';
import {useCurrentFrame} from 'remotion';
import {at, EASE} from '../lib/util';
import {C, FONT, FPS} from '../theme';

export type Span = string | {t: string; c: string};

// Cinematic on-screen line. `from`/`to` are scene-local seconds.
export const Caption: React.FC<{
  lines: Span[][];
  from: number;
  to: number;
  y?: number;
  size?: number;
  weight?: number;
  stagger?: number;
}> = ({lines, from, to, y = 820, size = 80, weight = 800, stagger = 0.18}) => {
  const t = useCurrentFrame() / FPS;
  const out = at(t, [to - 0.4, to], [1, 0]);
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: y,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: size * 0.28,
        fontFamily: FONT,
        fontWeight: weight,
        fontSize: size,
        lineHeight: 1.18,
        letterSpacing: '-0.02em',
        color: C.white,
        textAlign: 'center',
        opacity: out,
        textShadow: '0 6px 40px rgba(0,0,0,0.65)',
        pointerEvents: 'none',
      }}
    >
      {lines.map((line, i) => {
        const s = from + i * stagger;
        const p = at(t, [s, s + 0.7], [0, 1], EASE);
        return (
          <div
            key={i}
            style={{
              opacity: p,
              translate: `0px ${(1 - p) * 26}px`,
              filter: `blur(${(1 - p) * 10}px)`,
              whiteSpace: 'pre',
            }}
          >
            {line.map((sp, j) =>
              typeof sp === 'string' ? <span key={j}>{sp}</span> : <span key={j} style={{color: sp.c}}>{sp.t}</span>,
            )}
          </div>
        );
      })}
    </div>
  );
};
