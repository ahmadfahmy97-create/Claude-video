import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ANTON, MONT} from '../theme';

export const K = {
  gold: '#F5C542',
  goldDeep: '#C9971C',
  green: '#0F7A3D',
  deep: '#06301C',
  white: '#FFFFFF',
};

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// fade everything out over the last frames of an overlay
const useOut = (dur: number, n = 10) => {
  const f = useCurrentFrame();
  return interpolate(f, [dur - n, dur - 1], [1, 0], clamp);
};

// text that slides up out of a mask
const Rise: React.FC<{delay?: number; children: React.ReactNode; style?: React.CSSProperties; dist?: number}> = ({
  delay = 0,
  children,
  style,
  dist = 110,
}) => {
  const f = useCurrentFrame();
  const p = interpolate(f - delay, [0, 18], [0, 1], {...clamp, easing: ease});
  return (
    <div style={{overflow: 'hidden', ...style}}>
      <div style={{transform: `translateY(${(1 - p) * dist}%)`, opacity: p}}>{children}</div>
    </div>
  );
};

const Line: React.FC<{delay?: number; w: number; color?: string; h?: number; origin?: string}> = ({
  delay = 0,
  w,
  color = K.gold,
  h = 4,
  origin = 'left',
}) => {
  const f = useCurrentFrame();
  const p = interpolate(f - delay, [0, 20], [0, 1], {...clamp, easing: ease});
  return <div style={{width: w, height: h, background: color, transform: `scaleX(${p})`, transformOrigin: origin}} />;
};

const shadow = '0 4px 28px rgba(0,0,0,0.55), 0 1px 3px rgba(0,0,0,0.6)';

type G = {
  type: string;
  dur: number;
  side?: 'left' | 'right' | 'center';
  pos?: 'top' | 'bottom';
  [k: string]: any;
};

/* ---------- opening title: MENGENALI / PENGERUSI FAMA ---------- */
const Title: React.FC<{g: G}> = ({g}) => {
  const f = useCurrentFrame();
  const out = useOut(g.dur, 14);
  const sweep = interpolate(f, [22, 52], [-30, 130], clamp);
  const scale = interpolate(f, [0, g.dur], [1.0, 1.06]);
  const align = g.side === 'left' ? 'flex-start' : g.side === 'right' ? 'flex-end' : 'center';
  const pad = g.side === 'center' ? 0 : 150;
  return (
    <AbsoluteFill style={{opacity: out, justifyContent: 'center', alignItems: align, padding: `0 ${pad}px`}}>
      <div style={{transform: `scale(${scale})`, display: 'flex', flexDirection: 'column', alignItems: align}}>
        <Rise delay={2}>
          <div style={{fontFamily: MONT, fontWeight: 600, fontSize: 38, letterSpacing: 18, color: K.gold, textShadow: shadow}}>
            {g.kicker}
          </div>
        </Rise>
        <div style={{height: 10}} />
        <Rise delay={8}>
          <div
            style={{
              fontFamily: ANTON,
              fontSize: 140,
              lineHeight: 1,
              letterSpacing: 4,
              color: 'transparent',
              backgroundImage: `linear-gradient(100deg, #fff 0%, #fff ${sweep - 12}%, #FFE9A8 ${sweep}%, #fff ${sweep + 12}%, #fff 100%)`,
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
              filter: 'drop-shadow(0 6px 24px rgba(0,0,0,0.5))',
            }}
          >
            {g.title}
          </div>
        </Rise>
        <div style={{height: 22}} />
        <Line delay={20} w={g.side === 'center' ? 520 : 420} origin={g.side === 'right' ? 'right' : g.side === 'center' ? 'center' : 'left'} />
      </div>
    </AbsoluteFill>
  );
};

/* ---------- name card ---------- */
const Name: React.FC<{g: G}> = ({g}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const out = useOut(g.dur, 12);
  const right = g.side === 'right';
  const bar = spring({frame: f, fps, config: {damping: 200, stiffness: 120}});
  return (
    <AbsoluteFill
      style={{
        opacity: out,
        justifyContent: g.pos === 'top' ? 'flex-start' : 'flex-end',
        alignItems: right ? 'flex-end' : 'flex-start',
        padding: g.pos === 'top' ? '110px 130px' : '0 130px 120px',
      }}
    >
      <div style={{display: 'flex', flexDirection: right ? 'row-reverse' : 'row', alignItems: 'stretch', gap: 26}}>
        <div style={{width: 8, background: `linear-gradient(${K.gold}, ${K.goldDeep})`, transform: `scaleY(${bar})`, transformOrigin: 'top', borderRadius: 2}} />
        <div style={{display: 'flex', flexDirection: 'column', alignItems: right ? 'flex-end' : 'flex-start'}}>
          <Rise delay={4}>
            <div style={{fontFamily: MONT, fontWeight: 600, fontSize: 30, letterSpacing: 6, color: K.gold, textShadow: shadow}}>{g.honor}</div>
          </Rise>
          <Rise delay={8}>
            <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 64, lineHeight: 1.08, color: '#fff', textShadow: shadow, whiteSpace: 'pre-line', textAlign: right ? 'right' : 'left'}}>
              {g.name}
            </div>
          </Rise>
          <div style={{height: 14}} />
          <Rise delay={14}>
            <div
              style={{
                fontFamily: MONT,
                fontWeight: 700,
                fontSize: 30,
                letterSpacing: 3,
                color: K.deep,
                background: K.gold,
                padding: '8px 18px',
                borderRadius: 4,
              }}
            >
              {g.role}
            </div>
          </Rise>
          {g.note ? (
            <Rise delay={20}>
              <div style={{marginTop: 12, fontFamily: MONT, fontWeight: 500, fontSize: 26, color: 'rgba(255,255,255,0.9)', textShadow: shadow}}>{g.note}</div>
            </Rise>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- chapter card (corner) ---------- */
const Chapter: React.FC<{g: G}> = ({g}) => {
  const out = useOut(g.dur, 12);
  const right = g.side === 'right';
  const bottom = g.pos === 'bottom';
  return (
    <AbsoluteFill
      style={{
        opacity: out,
        justifyContent: bottom ? 'flex-end' : 'flex-start',
        alignItems: right ? 'flex-end' : 'flex-start',
        padding: bottom ? '0 110px 100px' : '90px 110px',
      }}
    >
      <div style={{display: 'flex', flexDirection: 'column', alignItems: right ? 'flex-end' : 'flex-start'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 18, flexDirection: right ? 'row-reverse' : 'row'}}>
          <Rise delay={0}>
            <div style={{fontFamily: ANTON, fontSize: 64, color: K.gold, lineHeight: 1, textShadow: shadow}}>{g.num}</div>
          </Rise>
          <Line delay={4} w={110} origin={right ? 'right' : 'left'} h={3} />
        </div>
        <Rise delay={6}>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 56, color: '#fff', letterSpacing: 1, textShadow: shadow, textAlign: right ? 'right' : 'left'}}>
            {g.title}
          </div>
        </Rise>
        {g.sub ? (
          <Rise delay={11}>
            <div style={{fontFamily: MONT, fontWeight: 500, fontSize: 28, color: 'rgba(255,255,255,0.88)', letterSpacing: 2, textShadow: shadow}}>{g.sub}</div>
          </Rise>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

/* ---------- soundbite subtitles with karaoke highlight ---------- */
const Sub: React.FC<{g: G}> = ({g}) => {
  const f = useCurrentFrame();
  const t = f / 25;
  const o = interpolate(f, [0, 5, g.dur - 5, g.dur], [0, 1, 1, 0], clamp);
  const top = g.pos === 'top';
  return (
    <AbsoluteFill style={{justifyContent: top ? 'flex-start' : 'flex-end', alignItems: 'center', padding: top ? '70px 200px' : '0 200px 70px', opacity: o}}>
      <div
        style={{
          fontFamily: MONT,
          fontWeight: 700,
          fontSize: 46,
          lineHeight: 1.3,
          textAlign: 'center',
          color: '#fff',
          textShadow: '0 3px 14px rgba(0,0,0,0.85), 0 0 2px rgba(0,0,0,0.9)',
          maxWidth: 1450,
        }}
      >
        {(g.words as {w: string; s: number}[]).map((w, i) => (
          <span key={i} style={{color: t >= w.s ? '#fff' : 'rgba(255,255,255,0.55)', transition: 'none'}}>
            {w.w}{' '}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/* ---------- big pull-quote on a side panel ---------- */
const Quote: React.FC<{g: G}> = ({g}) => {
  const f = useCurrentFrame();
  const out = useOut(g.dur, 12);
  const right = g.side === 'right';
  const panel = interpolate(f, [0, 16], [0, 1], {...clamp, easing: ease});
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          [right ? 'right' : 'left']: 0,
          width: 760,
          background: right
            ? 'linear-gradient(to left, rgba(6,48,28,0.86) 55%, rgba(6,48,28,0))'
            : 'linear-gradient(to right, rgba(6,48,28,0.86) 55%, rgba(6,48,28,0))',
          opacity: panel,
        }}
      />
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          [right ? 'right' : 'left']: 110,
          width: 560,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        <Rise delay={4}>
          <div style={{fontFamily: ANTON, fontSize: 150, color: K.gold, lineHeight: 0.8, height: 80}}>“</div>
        </Rise>
        {(g.lines as string[]).map((l, i) => (
          <Rise key={i} delay={8 + i * 5}>
            <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 50, lineHeight: 1.18, color: i === g.hl ? K.gold : '#fff'}}>{l}</div>
          </Rise>
        ))}
        <div style={{height: 22}} />
        <Line delay={20} w={120} h={3} />
        <Rise delay={24}>
          <div style={{marginTop: 12, fontFamily: MONT, fontWeight: 600, fontSize: 24, letterSpacing: 3, color: 'rgba(255,255,255,0.85)'}}>{g.by}</div>
        </Rise>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- end title ---------- */
const End: React.FC<{g: G}> = ({g}) => {
  const f = useCurrentFrame();
  const bg = interpolate(f, [0, 20], [0, 0.55], clamp);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 50%, rgba(6,48,28,${bg}) 0%, rgba(0,0,0,${bg}) 100%)`}} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <Rise delay={4}>
          <div style={{fontFamily: MONT, fontWeight: 600, fontSize: 36, letterSpacing: 16, color: K.gold}}>{g.kicker}</div>
        </Rise>
        <div style={{height: 12}} />
        <Rise delay={10}>
          <div style={{fontFamily: ANTON, fontSize: 150, color: '#fff', letterSpacing: 4, lineHeight: 1, textShadow: shadow}}>{g.title}</div>
        </Rise>
        <div style={{height: 24}} />
        <Line delay={22} w={480} origin="center" />
        <div style={{height: 20}} />
        <Rise delay={26}>
          <div style={{fontFamily: MONT, fontWeight: 500, fontSize: 30, letterSpacing: 4, color: 'rgba(255,255,255,0.9)'}}>{g.sub}</div>
        </Rise>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const Overlay: React.FC<{g: G}> = ({g}) => {
  switch (g.type) {
    case 'title':
      return <Title g={g} />;
    case 'name':
      return <Name g={g} />;
    case 'chapter':
      return <Chapter g={g} />;
    case 'sub':
      return <Sub g={g} />;
    case 'quote':
      return <Quote g={g} />;
    case 'end':
      return <End g={g} />;
    default:
      return null;
  }
};
