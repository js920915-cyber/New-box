import React from 'react';
import {AbsoluteFill, Series, staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {S1Universe} from './scenes/S1Universe';
import {S2Seoul} from './scenes/S2Seoul';
import {S3Center} from './scenes/S3Center';
import {S4Question} from './scenes/S4Question';
import {S5Assess} from './scenes/S5Assess';
import {S6Train} from './scenes/S6Train';
import {S7Return} from './scenes/S7Return';
import {S8Brand} from './scenes/S8Brand';

export type BrandFilmProps = {
  logo?: string; // optional official logo file in public/, e.g. "logo.png"
  music?: boolean;
};

// FROM SPACE TO MOVEMENT — 55 s at 30 fps (scene timings follow the brief).
export const SCENES = [
  {id: 'S1-Universe', frames: 150},
  {id: 'S2-Seoul', frames: 150},
  {id: 'S3-Center', frames: 150},
  {id: 'S4-Question', frames: 180},
  {id: 'S5-Assess', frames: 300},
  {id: 'S6-Train', frames: 300},
  {id: 'S7-Return', frames: 240},
  {id: 'S8-Brand', frames: 180},
] as const;
export const TOTAL_FRAMES = SCENES.reduce((s, x) => s + x.frames, 0);

export const BrandFilm: React.FC<BrandFilmProps> = ({logo, music = true}) => (
  <AbsoluteFill style={{background: '#000'}}>
    <Series>
      <Series.Sequence name="1 Universe" durationInFrames={150}>
        <S1Universe />
      </Series.Sequence>
      <Series.Sequence name="2 Destination Seoul" durationInFrames={150}>
        <S2Seoul />
      </Series.Sequence>
      <Series.Sequence name="3 Discover the Center" durationInFrames={150}>
        <S3Center />
      </Series.Sequence>
      <Series.Sequence name="4 The Question" durationInFrames={180}>
        <S4Question />
      </Series.Sequence>
      <Series.Sequence name="5 Assessment First" durationInFrames={300}>
        <S5Assess />
      </Series.Sequence>
      <Series.Sequence name="6 Rehab & Performance" durationInFrames={300}>
        <S6Train />
      </Series.Sequence>
      <Series.Sequence name="7 Back to Movement" durationInFrames={240}>
        <S7Return />
      </Series.Sequence>
      <Series.Sequence name="8 Brand Reveal" durationInFrames={180}>
        <S8Brand logo={logo} />
      </Series.Sequence>
    </Series>
    {music ? <Audio src={staticFile('audio/score.wav')} /> : null}
  </AbsoluteFill>
);
