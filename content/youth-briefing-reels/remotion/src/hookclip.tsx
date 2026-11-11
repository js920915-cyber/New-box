import React from "react";
import { Video } from "@remotion/media";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { C, FONT, Rich, Rise, s, Slam } from "./kit";

// 운동 숏폼(A 시리즈) 틀: 0.8초 안에 질문형 큰 자막 → 클립 컷 편집(줌 펀치·플래시) → 한 줄 정리 + 설명회 안내
// 사용자 영상은 public/clips/ 에 둔다(원본은 Drive '유소년 설명회').

export type Cut = { from: number; to: number; rate?: number };
export type HookClipProps = {
  src: string; // public/ 기준 경로, 예: "clips/blazepod.mp4"
  hook: string; // "*강조*" 지원, 줄바꿈 \n
  end: string;
  cuts: Cut[];
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const END_SEC = 2.2;

export const cutsFrames = (cuts: Cut[]) =>
  cuts.map((c) => Math.round(((c.to - c.from) / (c.rate ?? 1)) * 30));

export const hookClipDuration = (p: HookClipProps) =>
  cutsFrames(p.cuts).reduce((a, b) => a + b, 0) + s(END_SEC);

const CutClip: React.FC<{ src: string; cut: Cut; dur: number; idx: number }> = ({
  src,
  cut,
  dur,
  idx,
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          // 컷마다 살짝 다른 방향으로 줌 펀치
          scale: String(interpolate(frame, [0, 4, dur], [1.14, 1.04, 1.1], clamp)),
          translate: `${idx % 2 ? -14 : 14}px 0px`,
        }}
      >
        <Video
          src={staticFile(src)}
          trimBefore={Math.round(cut.from * 30)}
          trimAfter={Math.round(cut.to * 30)}
          playbackRate={cut.rate ?? 1}
          muted
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </AbsoluteFill>
      <AbsoluteFill
        style={{ backgroundColor: C.white, opacity: interpolate(frame, [0, 3], [0.55, 0], clamp) }}
      />
    </AbsoluteFill>
  );
};

export const HookClip: React.FC<HookClipProps> = (p) => {
  const frame = useCurrentFrame();
  const durs = cutsFrames(p.cuts);
  const clipTotal = durs.reduce((a, b) => a + b, 0);
  let acc = 0;
  const hookOut = interpolate(frame, [s(1.6), s(2.0)], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, fontFamily: FONT, textAlign: "center", wordBreak: "keep-all" }}>
      {p.cuts.map((c, i) => {
        const from = acc;
        acc += durs[i];
        return (
          <Sequence key={i} from={from} durationInFrames={durs[i]}>
            <CutClip src={p.src} cut={c} dur={durs[i]} idx={i} />
          </Sequence>
        );
      })}
      {/* 위아래 어둡게: 자막 가독성 */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(18,20,22,0.85) 0%, rgba(18,20,22,0) 34%, rgba(18,20,22,0) 62%, rgba(18,20,22,0.7) 100%)",
        }}
      />
      {/* 후킹 자막: 처음엔 화면 가운데 크게, 1.6초 뒤 위로 올라가 작아짐 */}
      <AbsoluteFill
        style={{
          justifyContent: "flex-start",
          alignItems: "center",
          paddingTop: interpolate(hookOut, [0, 1], [640, 250]),
          color: C.white,
        }}
      >
        <div
          style={{
            fontSize: interpolate(hookOut, [0, 1], [112, 68]),
            fontWeight: 850,
            lineHeight: 1.2,
            padding: "0 90px",
            textShadow: "0 6px 30px rgba(0,0,0,0.45)",
            isolation: "isolate",
          }}
        >
          {p.hook.split("\n").map((ln, i) => (
            <Slam key={i} delay={i * 5}>
              <Rich text={ln} at={8 + i * 5} marker={false} />
            </Slam>
          ))}
        </div>
      </AbsoluteFill>
      {/* 마무리 */}
      <Sequence from={clipTotal}>
        <AbsoluteFill
          style={{
            backgroundColor: C.ink,
            color: C.white,
            justifyContent: "center",
            alignItems: "center",
            padding: "250px 100px 430px",
          }}
        >
          <div style={{ fontSize: 96, fontWeight: 850, lineHeight: 1.25, isolation: "isolate" }}>
            {p.end.split("\n").map((ln, i) => (
              <Slam key={i} delay={i * 6}>
                <Rich text={ln} at={8 + i * 6} />
              </Slam>
            ))}
          </div>
          <Rise delay={16} style={{ marginTop: 60 }}>
            <div style={{ fontSize: 44, fontWeight: 800, lineHeight: 1.5 }}>
              12.12 (토) 유소년 축구 학부모 설명회
              <br />
              <span style={{ color: C.dim, fontWeight: 650 }}>
                신청은 <span style={{ color: C.white }}>프로필 링크</span>에서
              </span>
            </div>
          </Rise>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
