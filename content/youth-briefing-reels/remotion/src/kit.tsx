import React from "react";
import { loadFont } from "@remotion/fonts";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// 브랜드 색 (DESIGN_SYSTEM.md): 흰/검정 중심, 강조 블루, 경고에만 레드
export const C = {
  ink: "#121416",
  muted: "#5E6570",
  blue: "#0879D8",
  red: "#CC414A",
  soft: "#F0F7FC",
  line: "#D0DCE5",
  white: "#FFFFFF",
  dim: "#9AA3AD",
};

export const FONT = "RCardnews";
const WEIGHTS = [500, 650, 700, 750, 800, 850] as const;
export const fontsReady = Promise.all(
  WEIGHTS.map((w) =>
    loadFont({
      family: FONT,
      url: staticFile(`fonts/RCardnews-W${w}.ttf`),
      weight: String(w),
    }),
  ),
);

export const FPS = 30;
export const s = (sec: number) => Math.round(sec * FPS);

const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

// "*강조*" 구간을 블루로 칠하고, 형광펜이 지나가듯 밑줄 띠를 그린다
export const Rich: React.FC<{ text: string; hl?: string; at?: number; marker?: boolean }> = ({
  text,
  hl = C.blue,
  at = 10,
  marker = true,
}) => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [at, at + 9], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <>
      {text.split("*").map((part, i) =>
        i % 2 === 1 ? (
          <span key={i} style={{ color: hl, position: "relative", whiteSpace: "nowrap" }}>
            {marker ? (
              <span
                style={{
                  position: "absolute",
                  left: "-0.06em",
                  bottom: "0.06em",
                  height: "0.32em",
                  width: `calc(${w}% + 0.12em)`,
                  backgroundColor: hl,
                  opacity: 0.18,
                  borderRadius: "0.08em",
                  zIndex: -1,
                }}
              />
            ) : null}
            {part}
          </span>
        ) : (
          <React.Fragment key={i}>{part}</React.Fragment>
        ),
      )}
    </>
  );
};

// 크게 찍히듯 들어오는 글자 (후킹용)
export const Slam: React.FC<{
  delay?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ delay = 0, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const f = frame - delay;
  const sp = spring({ frame: f, fps, config: { damping: 14, stiffness: 260, mass: 0.6 } });
  const shake =
    f > 0 && f < 8 ? Math.sin(f * 2.4) * interpolate(f, [0, 8], [10, 0], clamp) : 0;
  return (
    <div
      style={{
        opacity: interpolate(f, [0, 3], [0, 1], clamp),
        scale: String(interpolate(sp, [0, 1], [1.55, 1])),
        translate: `${shake}px 0px`,
        filter: `blur(${interpolate(f, [0, 5], [12, 0], clamp)}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// 아래에서 올라오며 나타나는 글자
export const Rise: React.FC<{
  delay?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
  distance?: number;
}> = ({ delay = 0, children, style, distance = 60 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame: frame - delay, fps, config: { damping: 200 }, durationInFrames: 14 });
  return (
    <div
      style={{
        opacity: interpolate(frame - delay, [0, 6], [0, 1], clamp),
        translate: `0px ${interpolate(sp, [0, 1], [distance, 0])}px`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// 숫자 카운트업
export const CountUp: React.FC<{
  to: number;
  from?: number;
  delay?: number;
  dur?: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  style?: React.CSSProperties;
}> = ({ to, from = 0, delay = 0, dur = 24, decimals = 0, prefix = "", suffix = "", style }) => {
  const frame = useCurrentFrame();
  const v = interpolate(frame - delay, [0, dur], [from, to], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const txt = v.toLocaleString("ko-KR", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return (
    <span style={{ fontVariantNumeric: "tabular-nums", ...style }}>
      {prefix}
      {txt}
      {suffix}
    </span>
  );
};

// 장면 바탕: dark=후킹, light=설명
export const Scene: React.FC<{
  dark?: boolean;
  children: React.ReactNode;
  flash?: boolean;
}> = ({ dark, children, flash = true }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: dark ? C.ink : C.white,
        color: dark ? C.white : C.ink,
        fontFamily: FONT,
        textAlign: "center",
        wordBreak: "keep-all",
      }}
    >
      {/* 아주 느린 줌으로 정지 화면 느낌을 없앤다 */}
      <AbsoluteFill
        style={{
          scale: String(interpolate(frame, [0, durationInFrames], [1, 1.035])),
          // 인스타 UI(상단 계정명·하단 캡션·오른쪽 버튼)를 피한 안전 영역
          padding: "250px 110px 430px 110px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {children}
      </AbsoluteFill>
      {flash && dark ? (
        <AbsoluteFill
          style={{
            backgroundColor: C.white,
            opacity: interpolate(frame, [0, 5], [0.85, 0], clamp),
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};

export const Kicker: React.FC<{ children: React.ReactNode; delay?: number; dark?: boolean }> = ({
  children,
  delay = 0,
  dark,
}) => (
  <Rise delay={delay} distance={30}>
    <div
      style={{
        display: "inline-block",
        fontSize: 40,
        fontWeight: 750,
        color: dark ? C.white : C.blue,
        backgroundColor: dark ? C.blue : C.soft,
        padding: "12px 30px",
        borderRadius: 999,
        marginBottom: 44,
      }}
    >
      {children}
    </div>
  </Rise>
);

export const H: React.FC<{ text: string; size?: number; delay?: number; slam?: boolean }> = ({
  text,
  size = 108,
  delay = 0,
  slam,
}) => {
  const lines = text.split("\n");
  return (
    <div style={{ fontSize: size, fontWeight: 850, lineHeight: 1.22, letterSpacing: "-0.02em" }}>
      {lines.map((ln, i) =>
        slam ? (
          <Slam key={i} delay={delay + i * 7} style={{ isolation: "isolate" }}>
            <Rich text={ln} at={delay + i * 7 + 8} />
          </Slam>
        ) : (
          <Rise key={i} delay={delay + i * 5} style={{ isolation: "isolate" }}>
            <Rich text={ln} at={delay + i * 5 + 10} />
          </Rise>
        ),
      )}
    </div>
  );
};

export const Sub: React.FC<{ text: string; delay?: number; color?: string; size?: number }> = ({
  text,
  delay = 0,
  color,
  size = 54,
}) => (
  <Rise delay={delay} style={{ marginTop: 48, isolation: "isolate" }}>
    <div style={{ fontSize: size, fontWeight: 650, lineHeight: 1.4, color: color ?? "inherit" }}>
      {text.split("\n").map((ln, i) => (
        <div key={i}>
          <Rich text={ln} at={delay + 8} />
        </div>
      ))}
    </div>
  </Rise>
);

// 가로 막대 (값 비교)
export const Bar: React.FC<{
  label: string;
  value: number;
  max: number;
  display: React.ReactNode;
  color: string;
  delay?: number;
}> = ({ label, value, max, display, color, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame: frame - delay, fps, config: { damping: 20, stiffness: 90 } });
  const w = (value / max) * 100 * sp;
  return (
    <Rise delay={delay} distance={30} style={{ width: "100%", marginBottom: 46 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          fontSize: 42,
          fontWeight: 700,
          marginBottom: 16,
        }}
      >
        <span>{label}</span>
        <span style={{ fontSize: 56, fontWeight: 850, color }}>{display}</span>
      </div>
      <div style={{ height: 56, borderRadius: 16, backgroundColor: C.soft, overflow: "hidden" }}>
        <div style={{ width: `${w}%`, height: "100%", borderRadius: 16, backgroundColor: color }} />
      </div>
    </Rise>
  );
};

// 마지막 안내 카드
export const EndCard: React.FC = () => (
  <Scene dark>
    <Kicker dark>학부모 · 지도자 설명회</Kicker>
    <H text={"우리 아이는 왜\n맨날 *다칠까요?*"} size={92} slam />
    <Rise delay={14} style={{ marginTop: 60 }}>
      <div style={{ fontSize: 50, fontWeight: 800, lineHeight: 1.45 }}>
        12.12 (토) 오후 3–5시
        <br />
        <span style={{ fontWeight: 650, color: C.dim, fontSize: 44 }}>
          R스포츠재활센터 · 강서구 마곡
        </span>
      </div>
    </Rise>
    <Rise delay={22} style={{ marginTop: 56 }}>
      <div
        style={{
          fontSize: 46,
          fontWeight: 800,
          color: C.ink,
          backgroundColor: C.white,
          padding: "22px 46px",
          borderRadius: 999,
        }}
      >
        신청은 <span style={{ color: C.blue }}>프로필 링크</span>에서
      </div>
    </Rise>
  </Scene>
);
