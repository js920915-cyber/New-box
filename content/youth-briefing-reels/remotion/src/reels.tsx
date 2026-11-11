import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Bar, C, CountUp, EndCard, H, Kicker, Rich, Rise, s, Scene, Slam, Sub } from "./kit";

// 근거 매핑은 ../research/claims.md (C1~C15). 문구를 바꾸면 claims.md도 같이 고친다.

export type SceneDef = { dur: number; el: React.ReactNode };
export const T = 7; // 장면 전환 길이(프레임)

export const reelDuration = (scenes: SceneDef[]) =>
  scenes.reduce((a, b) => a + b.dur, 0) - T * (scenes.length - 1);

export const Reel: React.FC<{ scenes: SceneDef[] }> = ({ scenes }) => (
  <TransitionSeries>
    {scenes.map((sc, i) => (
      <React.Fragment key={i}>
        {i > 0 ? (
          <TransitionSeries.Transition
            presentation={slide({ direction: "from-bottom" })}
            timing={linearTiming({ durationInFrames: T })}
          />
        ) : null}
        <TransitionSeries.Sequence durationInFrames={sc.dur}>{sc.el}</TransitionSeries.Sequence>
      </React.Fragment>
    ))}
  </TransitionSeries>
);

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/* ───────────── B1. 유소년은 성인과 다르다 ───────────── */

const B1_Bars: React.FC = () => (
  <Scene>
    <Kicker>키가 크는 속도별 · 성장 관련 부상</Kicker>
    <H text={"빨리 클 때\n*2.8배* 더 많았어요"} size={100} />
    <div style={{ width: "100%", marginTop: 70 }}>
      <Bar label="보통 속도로 크는 시기" value={0.9} max={2.5} display="1배" color={C.dim} delay={18} />
      <Bar
        label="1년에 7.2cm 넘게 크는 시기"
        value={2.5}
        max={2.5}
        display={<CountUp to={2.8} decimals={1} delay={26} dur={26} suffix="배" />}
        color={C.blue}
        delay={26}
      />
    </div>
    <Sub text="급성장기 무렵 · 남자 유소년 선수 연구" delay={40} size={38} color={C.muted} />
  </Scene>
);

export const B1: SceneDef[] = [
  {
    dur: s(2.6),
    el: (
      <Scene dark>
        <H text={"요즘 키가\n*훅* 컸나요?"} size={124} slam />
      </Scene>
    ),
  },
  {
    dur: s(3.0),
    el: (
      <Scene>
        <H text={"아이 몸은\n*작은 어른*이 아니에요"} size={106} />
        <Sub text="자라는 속도가 부상과 관련 있어요" delay={14} color={C.muted} />
      </Scene>
    ),
  },
  { dur: s(5.4), el: <B1_Bars /> },
  {
    dur: s(3.6),
    el: (
      <Scene>
        <Kicker>대표적인 성장기 통증</Kicker>
        <H text={"오스굿병 · 세버병"} size={100} />
        <Sub text={"무릎 아래, 발뒤꿈치\n*성장판 주변*이 아파요"} delay={12} />
      </Scene>
    ),
  },
  {
    dur: s(3.8),
    el: (
      <Scene dark flash={false}>
        <Kicker dark>부모님이 할 일 하나</Kicker>
        <H text={"키를\n*3~4개월*마다\n재 주세요"} size={110} slam />
      </Scene>
    ),
  },
  { dur: s(4.0), el: <EndCard /> },
];

/* ───────────── B2. 부상은 왜 반복될까 ───────────── */

const LoopScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nodes = ["다침", "쉼", "복귀", "또 다침"];
  const R = 300;
  const draw = interpolate(frame, [4, 40], [0, 1], clamp);
  const circ = 2 * Math.PI * R;
  return (
    <Scene>
      <Kicker>이런 패턴, 익숙하지 않나요?</Kicker>
      <div style={{ position: "relative", width: 2 * R + 220, height: 2 * R + 160 }}>
        <svg
          width={2 * R + 220}
          height={2 * R + 160}
          style={{ position: "absolute", inset: 0, rotate: `${frame * 0.6}deg` }}
        >
          <circle
            cx={R + 110}
            cy={R + 80}
            r={R}
            fill="none"
            stroke={C.line}
            strokeWidth={10}
            strokeDasharray={circ}
            strokeDashoffset={circ * (1 - draw)}
            strokeLinecap="round"
          />
        </svg>
        {nodes.map((n, i) => {
          const a = -Math.PI / 2 + (i * Math.PI) / 2;
          const sp = spring({ frame: frame - 8 - i * 9, fps, config: { damping: 12, stiffness: 200 } });
          const last = i === 3;
          return (
            <div
              key={n}
              style={{
                position: "absolute",
                left: R + 110 + R * Math.cos(a),
                top: R + 80 + R * Math.sin(a),
                translate: "-50% -50%",
                scale: String(sp),
                fontSize: 52,
                fontWeight: 850,
                color: last ? C.white : C.ink,
                backgroundColor: last ? C.red : C.white,
                border: `4px solid ${last ? C.red : C.ink}`,
                borderRadius: 999,
                padding: "18px 40px",
                whiteSpace: "nowrap",
              }}
            >
              {n}
            </div>
          );
        })}
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 64,
            fontWeight: 850,
            color: C.muted,
            opacity: interpolate(frame, [44, 52], [0, 1], clamp),
          }}
        >
          반복
        </div>
      </div>
    </Scene>
  );
};

const ThreeCauses: React.FC = () => {
  const items = ["너무 많이 (과사용)", "잘못된 자세", "과한 부하 (무게·강도)"];
  return (
    <Scene>
      <Kicker>부상과 관련된 것들</Kicker>
      <H text={"이 셋을 보세요"} size={106} />
      <div style={{ marginTop: 56, width: "100%" }}>
        {items.map((t, i) => (
          <Rise key={t} delay={12 + i * 9} style={{ marginBottom: 26 }}>
            <div
              style={{
                fontSize: 54,
                fontWeight: 800,
                padding: "30px 20px",
                borderRadius: 24,
                backgroundColor: C.soft,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 24,
              }}
            >
              <span style={{ color: C.blue, fontWeight: 850 }}>{i + 1}</span>
              {t}
            </div>
          </Rise>
        ))}
      </div>
    </Scene>
  );
};

const NotEqual: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Scene dark flash={false}>
      <Slam>
        <div style={{ fontSize: 96, fontWeight: 850, lineHeight: 1.2 }}>안 아픈 것</div>
      </Slam>
      <Slam delay={10}>
        <div
          style={{
            fontSize: 150,
            fontWeight: 850,
            color: C.blue,
            lineHeight: 1.1,
            rotate: `${interpolate(frame, [10, 22], [-90, 0], clamp)}deg`,
          }}
        >
          ≠
        </div>
      </Slam>
      <Slam delay={18}>
        <div style={{ fontSize: 96, fontWeight: 850, lineHeight: 1.2 }}>준비된 것</div>
      </Slam>
      <Sub text="복귀 전, *측정*으로 확인해요" delay={30} />
    </Scene>
  );
};

export const B2: SceneDef[] = [
  {
    dur: s(2.6),
    el: (
      <Scene dark>
        <H text={"또\n*그 자리*가\n아프대요"} size={124} slam />
      </Scene>
    ),
  },
  { dur: s(4.0), el: <LoopScene /> },
  {
    dur: s(3.6),
    el: (
      <Scene>
        <H text={"한 번 다친 곳은\n*다음 부상*의\n위험 요인이에요"} size={100} />
        <Sub text="축구에서 잘 알려진 사실이에요" delay={16} color={C.muted} />
      </Scene>
    ),
  },
  { dur: s(4.4), el: <ThreeCauses /> },
  { dur: s(4.0), el: <NotEqual /> },
  { dur: s(4.0), el: <EndCard /> },
];

/* ───────────── B3. 어린 나이 근력운동, 괜찮을까 ───────────── */

const MythScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame: frame - 14, fps, config: { damping: 10, stiffness: 220 } });
  return (
    <Scene dark>
      <H text={"근력운동 하면\n*키 안 큰다?*"} size={116} slam />
      <div
        style={{
          marginTop: 70,
          fontSize: 64,
          fontWeight: 850,
          color: C.red,
          border: `6px solid ${C.red}`,
          borderRadius: 20,
          padding: "14px 44px",
          rotate: "-6deg",
          scale: String(interpolate(sp, [0, 1], [2.4, 1])),
          opacity: interpolate(frame, [14, 17], [0, 1], clamp),
        }}
      >
        흔한 오해
      </div>
    </Scene>
  );
};

const Conditions: React.FC = () => {
  const items = [
    ["제대로 배우고", "지도"],
    ["곁에서 지켜보고", "감독"],
    ["자세 먼저, 무게는 나중", "기술 우선"],
  ];
  return (
    <Scene>
      <Kicker>단, 조건이 있어요</Kicker>
      <div style={{ width: "100%" }}>
        {items.map(([t, k], i) => (
          <Rise key={t} delay={8 + i * 10} style={{ marginBottom: 30 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 28,
                padding: "34px 40px",
                borderRadius: 26,
                border: `3px solid ${C.line}`,
                textAlign: "left",
              }}
            >
              <span
                style={{
                  fontSize: 38,
                  fontWeight: 800,
                  color: C.white,
                  backgroundColor: C.blue,
                  borderRadius: 14,
                  padding: "8px 18px",
                  whiteSpace: "nowrap",
                }}
              >
                {k}
              </span>
              <span style={{ fontSize: 54, fontWeight: 800 }}>{t}</span>
            </div>
          </Rise>
        ))}
      </div>
    </Scene>
  );
};

const Stages: React.FC = () => {
  const rows = [
    ["7~9세", "맨몸 · 버티기"],
    ["10~11세", "밴드 · 메디신볼 · 기구"],
    ["12세~", "자세가 되면 무게를 조금씩"],
  ];
  const frame = useCurrentFrame();
  return (
    <Scene>
      <Kicker>몸이 크는 만큼, 무게도 천천히</Kicker>
      <H text={"나이에 맞게\n*단계적으로*"} size={100} />
      <div style={{ position: "relative", width: "100%", marginTop: 64 }}>
        <div
          style={{
            position: "absolute",
            left: 126,
            top: 40,
            width: 8,
            borderRadius: 4,
            backgroundColor: C.blue,
            height: `${interpolate(frame, [6, 40], [0, 82], clamp)}%`,
          }}
        />
        {rows.map(([age, what], i) => (
          <Rise key={age} delay={8 + i * 11} style={{ marginBottom: 56 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 40, textAlign: "left" }}>
              <div
                style={{
                  width: 260,
                  flexShrink: 0,
                  fontSize: 46,
                  fontWeight: 850,
                  color: C.blue,
                  backgroundColor: C.white,
                  border: `4px solid ${C.blue}`,
                  borderRadius: 999,
                  padding: "14px 0",
                  textAlign: "center",
                  position: "relative",
                }}
              >
                {age}
              </div>
              <div style={{ fontSize: 54, fontWeight: 800, lineHeight: 1.3 }}>{what}</div>
            </div>
          </Rise>
        ))}
      </div>
    </Scene>
  );
};

export const B3: SceneDef[] = [
  { dur: s(3.0), el: <MythScene /> },
  {
    dur: s(3.4),
    el: (
      <Scene>
        <H text={"근력운동은\n*초등학생*부터\n안전하고 효과적"} size={106} />
        <Sub text="유소년 근력운동 연구 리뷰의 결론" delay={16} color={C.muted} size={40} />
      </Scene>
    ),
  },
  { dur: s(4.4), el: <Conditions /> },
  { dur: s(4.4), el: <Stages /> },
  {
    dur: s(3.8),
    el: (
      <Scene dark flash={false}>
        <Kicker dark>부모님이 물어볼 것</Kicker>
        <Slam>
          <div style={{ fontSize: 70, fontWeight: 750, color: C.dim, textDecoration: "line-through" }}>
            몇 kg 드나요?
          </div>
        </Slam>
        <Slam delay={12}>
          <div style={{ fontSize: 110, fontWeight: 850, marginTop: 24 }}>
            <Rich text={"*누가* 가르치나요?"} at={20} />
          </div>
        </Slam>
      </Scene>
    ),
  },
  { dur: s(4.0), el: <EndCard /> },
];

/* ───────────── B4. 부상 예방 프로그램 ───────────── */

const StudyCount: React.FC = () => (
  <Scene>
    <Kicker>유럽 4개국 유소년 축구 연구</Kicker>
    {[
      { n: 3895, suf: "명", label: "선수" },
      { n: 13, from: 7, pre: "7~", suf: "세", label: "나이" },
      { n: 1, suf: "시즌", label: "추적" },
    ].map((it, i) => (
      <Rise key={it.label} delay={6 + i * 9} style={{ marginBottom: 34 }}>
        <div style={{ fontSize: 40, fontWeight: 700, color: C.muted }}>{it.label}</div>
        <div style={{ fontSize: 120, fontWeight: 850, lineHeight: 1.1 }}>
          <CountUp to={it.n} from={(it as {from?: number}).from ?? 0} prefix={it.pre ?? ""} suffix={it.suf} delay={6 + i * 9} dur={22} />
        </div>
      </Rise>
    ))}
  </Scene>
);

const Reduction: React.FC = () => (
  <Scene>
    <Kicker>준비운동 '11+ Kids'를 한 팀</Kicker>
    <H text={"부상이 이만큼\n*줄었어요*"} size={100} />
    <div style={{ width: "100%", marginTop: 64 }}>
      <Bar label="전체 부상" value={48} max={80} display={<CountUp to={48} delay={14} prefix="−" suffix="%" />} color={C.blue} delay={14} />
      <Bar label="하체 부상" value={55} max={80} display={<CountUp to={55} delay={22} prefix="−" suffix="%" />} color={C.blue} delay={22} />
      <Bar label="4주 넘게 쉰 큰 부상" value={74} max={80} display={<CountUp to={74} delay={30} prefix="−" suffix="%" />} color={C.blue} delay={30} />
    </div>
  </Scene>
);

export const B4: SceneDef[] = [
  {
    dur: s(2.8),
    el: (
      <Scene dark>
        <H text={"준비운동 20분이\n부상을 *절반* 가까이"} size={104} slam />
      </Scene>
    ),
  },
  { dur: s(4.0), el: <StudyCount /> },
  { dur: s(5.4), el: <Reduction /> },
  {
    dur: s(3.8),
    el: (
      <Scene>
        <Kicker>핵심은 꾸준함</Kicker>
        <H text={"주 1회 이상,\n*주 2회* 권장"} size={100} />
        <Sub text="자주 한 아이일수록 더 줄었어요" delay={14} />
      </Scene>
    ),
  },
  {
    dur: s(3.6),
    el: (
      <Scene dark flash={false}>
        <H text={"같은 예방도\n*우리 아이*에게\n맞춰야 해요"} size={104} slam />
        <Sub text="측정으로 약한 곳을 먼저 찾습니다" delay={22} color={C.dim} />
      </Scene>
    ),
  },
  { dur: s(4.0), el: <EndCard /> },
];
