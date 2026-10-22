import React from 'react';
import {Composition, Folder} from 'remotion';
import {BrandFilm, TOTAL_FRAMES} from './BrandFilm';
import {Lab, MoveLab, StairLab} from './Lab';
import {S1Universe} from './scenes/S1Universe';
import {S2Seoul} from './scenes/S2Seoul';
import {S3Center} from './scenes/S3Center';
import {S4Question} from './scenes/S4Question';
import {S5Assess} from './scenes/S5Assess';
import {S6Train} from './scenes/S6Train';
import {S7Return} from './scenes/S7Return';
import {S8Brand} from './scenes/S8Brand';
import './fonts';

const base = {width: 1920, height: 1080, fps: 30} as const;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="BrandFilm" component={BrandFilm} {...base} durationInFrames={TOTAL_FRAMES} defaultProps={{music: true, captions: true}} />
      <Folder name="Scenes">
        <Composition id="S1-Universe" component={S1Universe} {...base} durationInFrames={150} />
        <Composition id="S2-Seoul" component={S2Seoul} {...base} durationInFrames={150} />
        <Composition id="S3-Center" component={S3Center} {...base} durationInFrames={150} />
        <Composition id="S4-Question" component={S4Question} {...base} durationInFrames={180} />
        <Composition id="S5-Assess" component={S5Assess} {...base} durationInFrames={300} />
        <Composition id="S6-Train" component={S6Train} {...base} durationInFrames={300} />
        <Composition id="S7-Return" component={S7Return} {...base} durationInFrames={240} />
        <Composition id="S8-Brand" component={S8Brand} {...base} durationInFrames={180} defaultProps={{}} />
      </Folder>
      <Folder name="Dev">
        <Composition id="Lab" component={Lab} {...base} durationInFrames={60} />
        <Composition id="StairLab" component={StairLab} {...base} durationInFrames={60} />
        <Composition id="MoveLab" component={MoveLab} {...base} durationInFrames={1} />
      </Folder>
    </>
  );
};
