import React from "react";
import { Composition, Folder } from "remotion";
import "./kit";
import { B1, B2, B3, B4, Reel, reelDuration, SceneDef } from "./reels";

const make = (scenes: SceneDef[]) => {
  const Comp: React.FC = () => <Reel scenes={scenes} />;
  return Comp;
};

const reels: [string, SceneDef[], React.FC][] = [
  ["B1-Growth", B1, make(B1)],
  ["B2-Reinjury", B2, make(B2)],
  ["B3-Strength", B3, make(B3)],
  ["B4-Prevention", B4, make(B4)],
];

export const RemotionRoot: React.FC = () => (
  <Folder name="Motion-Graphics">
    {reels.map(([id, scenes, Comp]) => (
      <Composition
        key={id}
        id={id}
        component={Comp}
        durationInFrames={reelDuration(scenes)}
        fps={30}
        width={1080}
        height={1920}
      />
    ))}
  </Folder>
);
