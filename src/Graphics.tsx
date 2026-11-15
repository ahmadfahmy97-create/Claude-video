import React from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ANTON, C, CX, MONT, SAFE, SAFE_W, stroke} from './theme';

type G = {type: string; start: number; dur: number; y?: number; [k: string]: any};

const useAnim = (dur: number, out = 8) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const D = Math.round(dur * fps);
  const enter = spring({frame, fps, config: {damping: 13, stiffness: 190, mass: 0.7}});
  const exit = interpolate(frame, [D - out, D], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return {frame, fps, D, enter, exit};
};

const Centered: React.FC<{y: number; children: React.ReactNode; style?: React.CSSProperties}> = ({y, children, style}) => (
  <div
    style={{
      position: 'absolute',
      left: CX - SAFE_W / 2,
      width: SAFE_W,
      top: y,
      transform: 'translateY(-50%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      ...style,
    }}
  >
    {children}
  </div>
);

const Check: React.FC<{size?: number; color?: string; bg?: string}> = ({size = 46, color = 'white', bg = C.green}) => (
  <svg width={size} height={size} viewBox="0 0 48 48">
    <circle cx="24" cy="24" r="23" fill={bg} />
    <path d="M14 25 l7 7 l14 -15" stroke={color} strokeWidth="5.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Pin: React.FC<{size?: number}> = ({size = 64}) => (
  <svg width={size} height={size} viewBox="0 0 48 48">
    <circle cx="24" cy="24" r="24" fill={C.green} />
    <path d="M24 11c-5.5 0-9.5 4.2-9.5 9.4 0 7 9.5 16.6 9.5 16.6s9.5-9.6 9.5-16.6c0-5.2-4-9.4-9.5-9.4z" fill="white" />
    <circle cx="24" cy="20.6" r="3.6" fill={C.green} />
  </svg>
);

// ------------------------------------------------------------------------------ pieces
const Headline: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const words: string[] = g.text.split(' ');
  return (
    <Centered y={g.y ?? 390} style={{opacity: exit}}>
      <div
        style={{
          fontFamily: MONT,
          fontWeight: 900,
          fontSize: 36,
          letterSpacing: 2,
          color: C.black,
          background: C.yellow,
          padding: '10px 22px',
          borderRadius: 12,
          transform: `translateY(${interpolate(enter, [0, 1], [-40, 0])}px) rotate(-2deg)`,
          opacity: enter,
          boxShadow: '0 8px 24px rgba(0,0,0,0.35)',
        }}
      >
        {g.kicker}
      </div>
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 16px', marginTop: 14, maxWidth: SAFE_W}}>
        {words.map((w, i) => {
          const s = spring({frame: frame - 3 - i * 2, fps, config: {damping: 12, stiffness: 220, mass: 0.5}});
          const hi = w === 'SARA';
          return (
            <span
              key={i}
              style={{
                fontFamily: ANTON,
                fontSize: hi ? 104 : 84,
                lineHeight: 1.05,
                color: hi ? C.yellow : C.white,
                transform: `translateY(${interpolate(s, [0, 1], [50, 0])}px) scale(${interpolate(s, [0, 1], [0.6, 1])})`,
                opacity: s,
                textShadow: '0 8px 22px rgba(0,0,0,0.6)',
                ...stroke(12),
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
    </Centered>
  );
};

const BigStat: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const slam = spring({frame, fps, config: {damping: 9, stiffness: 260, mass: 0.6}});
  const shake = frame < 8 ? Math.sin(frame * 2.2) * (8 - frame) * 1.6 : 0;
  return (
    <Centered y={g.y ?? 420} style={{opacity: exit, transform: `translateY(-50%) translateX(${shake}px)`}}>
      <div
        style={{
          fontFamily: MONT,
          fontWeight: 900,
          fontSize: 38,
          color: 'white',
          background: C.green,
          padding: '8px 24px',
          borderRadius: 999,
          letterSpacing: 1.5,
          opacity: enter,
          boxShadow: '0 6px 18px rgba(0,0,0,0.35)',
        }}
      >
        {g.bottom}
      </div>
      <div
        style={{
          fontFamily: ANTON,
          fontSize: g.value.length > 4 ? 170 : 230,
          lineHeight: 1,
          color: C.yellow,
          transform: `scale(${interpolate(slam, [0, 1], [2.4, 1])}) rotate(${interpolate(slam, [0, 1], [-10, -3])}deg)`,
          opacity: interpolate(slam, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
          textShadow: '0 14px 40px rgba(0,0,0,0.55)',
          ...stroke(18),
        }}
      >
        {g.value}
      </div>
      <div style={{fontFamily: ANTON, fontSize: 64, color: 'white', marginTop: -6, opacity: enter, ...stroke(10)}}>{g.top}</div>
    </Centered>
  );
};

const Location: React.FC<{g: G}> = ({g}) => {
  const {enter, exit} = useAnim(g.dur);
  return (
    <div
      style={{
        position: 'absolute',
        left: SAFE.left,
        top: g.y ?? 1080,
        transform: `translateY(-50%) translateX(${interpolate(enter, [0, 1], [-700, 0])}px)`,
        opacity: exit,
        display: 'flex',
        alignItems: 'center',
        gap: 18,
        background: 'rgba(255,255,255,0.96)',
        padding: '16px 30px 16px 16px',
        borderRadius: 999,
        boxShadow: '0 12px 30px rgba(0,0,0,0.35)',
        maxWidth: SAFE_W,
      }}
    >
      <Pin size={74} />
      <div>
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 46, color: C.black, lineHeight: 1.05}}>{g.title}</div>
        <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 34, color: C.green}}>{g.sub}</div>
      </div>
    </div>
  );
};

const Combo: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  return (
    <Centered y={g.y ?? 420} style={{opacity: exit}}>
      <div
        style={{
          width: 640,
          background: 'white',
          borderRadius: 32,
          overflow: 'hidden',
          boxShadow: '0 18px 50px rgba(0,0,0,0.45)',
          transform: `scale(${interpolate(enter, [0, 1], [0.6, 1])}) rotate(${interpolate(enter, [0, 1], [6, -1.5])}deg)`,
          opacity: enter,
        }}
      >
        <div style={{background: C.green, padding: '18px 0', textAlign: 'center', fontFamily: ANTON, fontSize: 58, color: C.yellow, letterSpacing: 1}}>
          {g.title}
        </div>
        <div style={{padding: '18px 34px 24px'}}>
          {(g.items as string[]).map((it, i) => {
            const s = spring({frame: frame - 8 - i * 6, fps, config: {damping: 13, stiffness: 220}});
            return (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 18,
                  padding: '8px 0',
                  opacity: s,
                  transform: `translateX(${interpolate(s, [0, 1], [60, 0])}px)`,
                }}
              >
                <Check size={44} />
                <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 42, color: C.black}}>{it}</span>
              </div>
            );
          })}
        </div>
      </div>
    </Centered>
  );
};

const Confetti: React.FC<{seed: string}> = ({seed}) => {
  const frame = useCurrentFrame();
  const colors = [C.yellow, C.green, '#FFFFFF', C.red, '#38BDF8'];
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {new Array(70).fill(0).map((_, i) => {
        const ang = random(`${seed}a${i}`) * Math.PI * 2;
        const sp = 18 + random(`${seed}s${i}`) * 26;
        const t = frame;
        const x = CX + Math.cos(ang) * sp * t;
        const y = 760 + Math.sin(ang) * sp * t * 0.8 + 0.9 * t * t;
        const rot = random(`${seed}r${i}`) * 360 + t * 14;
        const o = interpolate(t, [0, 30, 50], [1, 1, 0], {extrapolateRight: 'clamp'});
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: 16,
              height: 26,
              background: colors[i % colors.length],
              transform: `rotate(${rot}deg)`,
              opacity: o,
              borderRadius: 3,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const Stamp: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur);
  const s = spring({frame, fps, config: {damping: 10, stiffness: 280, mass: 0.7}});
  return (
    <>
      {g.confetti ? <Confetti seed={g.text} /> : null}
      <Centered y={g.y ?? 420} style={{opacity: exit}}>
        <div
          style={{
            fontFamily: ANTON,
            fontSize: 108,
            color: C.yellow,
            padding: '10px 36px',
            border: `10px solid ${C.yellow}`,
            borderRadius: 26,
            background: 'rgba(6,78,59,0.88)',
            transform: `scale(${interpolate(s, [0, 1], [3, 1])}) rotate(-7deg)`,
            opacity: interpolate(s, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'}),
            boxShadow: '0 16px 50px rgba(0,0,0,0.5)',
            whiteSpace: 'nowrap',
          }}
        >
          {g.text}
        </div>
      </Centered>
    </>
  );
};

const Price: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const sf = Math.round(g.strikeAt * fps);
  const strike = interpolate(frame, [sf, sf + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const n = spring({frame: frame - sf - 2, fps, config: {damping: 9, stiffness: 240, mass: 0.6}});
  return (
    <Centered y={g.y ?? 420} style={{opacity: exit}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 34}}>
        <div style={{position: 'relative', opacity: enter, transform: `scale(${interpolate(enter, [0, 1], [0.5, 1])})`}}>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 30, color: 'white', textAlign: 'center', ...stroke(7)}}>{g.oldLabel ?? 'HARGA PASARAN'}</div>
          <div style={{fontFamily: ANTON, fontSize: 130, color: 'white', lineHeight: 1, opacity: interpolate(strike, [0, 1], [1, 0.75]), ...stroke(14)}}>
            {g.old}
          </div>
          <div
            style={{
              position: 'absolute',
              left: -10,
              top: 100,
              height: 16,
              width: `${strike * 112}%`,
              background: C.red,
              borderRadius: 8,
              transform: 'rotate(-12deg)',
              transformOrigin: 'left center',
              boxShadow: '0 3px 10px rgba(0,0,0,0.5)',
            }}
          />
        </div>
        <div style={{opacity: interpolate(n, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}), transform: `scale(${interpolate(n, [0, 1], [2, 1])}) rotate(-4deg)`}}>
          <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 34, color: C.black, background: C.yellow, borderRadius: 10, padding: '4px 14px', textAlign: 'center'}}>
            {g.newLabel ?? 'HARGA AGRO MADANI'}
          </div>
          <div style={{fontFamily: ANTON, fontSize: 190, color: C.yellow, lineHeight: 1, textShadow: '0 12px 30px rgba(0,0,0,0.5)', ...stroke(16)}}>{g.new}</div>
        </div>
      </div>
    </Centered>
  );
};

const Tag: React.FC<{g: G}> = ({g}) => {
  const {enter, exit} = useAnim(g.dur);
  return (
    <div
      style={{
        position: 'absolute',
        left: SAFE.left,
        top: g.y ?? 300,
        transform: `translateY(-50%) translateX(${interpolate(enter, [0, 1], [-600, 0])}px)`,
        opacity: exit,
        display: 'flex',
        alignItems: 'stretch',
        boxShadow: '0 10px 26px rgba(0,0,0,0.4)',
        borderRadius: 12,
        overflow: 'hidden',
      }}
    >
      <div style={{width: 14, background: C.yellow}} />
      <div style={{background: 'rgba(11,11,11,0.82)', padding: '12px 24px', fontFamily: MONT, fontWeight: 900, fontSize: 36, color: 'white', letterSpacing: 1.5}}>
        {g.text}
      </div>
    </div>
  );
};

const Calendar: React.FC<{g: G}> = ({g}) => {
  const {enter, exit} = useAnim(g.dur);
  return (
    <Centered y={g.y ?? 420} style={{opacity: exit}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 30}}>
        <div style={{fontFamily: ANTON, fontSize: 96, color: 'white', opacity: enter, transform: `translateX(${interpolate(enter, [0, 1], [-80, 0])}px)`, ...stroke(12)}}>
          MULAI
        </div>
        <div
          style={{
            width: 280,
            borderRadius: 28,
            overflow: 'hidden',
            background: 'white',
            boxShadow: '0 18px 46px rgba(0,0,0,0.5)',
            transform: `perspective(900px) rotateX(${interpolate(enter, [0, 1], [-95, 0])}deg)`,
            transformOrigin: 'top center',
          }}
        >
          <div style={{background: C.red, color: 'white', fontFamily: MONT, fontWeight: 900, fontSize: 40, textAlign: 'center', padding: '10px 0'}}>{g.month}</div>
          <div style={{fontFamily: ANTON, fontSize: 170, color: C.black, textAlign: 'center', lineHeight: 1.05}}>{g.day}</div>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 40, color: C.green, textAlign: 'center', paddingBottom: 12}}>{g.year}</div>
        </div>
      </div>
    </Centered>
  );
};

const Sara: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const c = spring({frame: frame - 8, fps, config: {damping: 9, stiffness: 260}});
  return (
    <Centered y={g.y ?? 420} style={{opacity: exit}}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 26,
          background: 'linear-gradient(135deg, #065F46 0%, #16A34A 100%)',
          borderRadius: 34,
          padding: '24px 40px',
          boxShadow: '0 18px 50px rgba(0,0,0,0.45)',
          border: '5px solid rgba(255,255,255,0.85)',
          transform: `scale(${interpolate(enter, [0, 1], [0.5, 1])})`,
          opacity: enter,
          maxWidth: SAFE_W,
        }}
      >
        <div style={{transform: `scale(${c})`}}>
          <Check size={110} bg={C.yellow} color={C.deep} />
        </div>
        <div>
          <div style={{fontFamily: ANTON, fontSize: 120, color: 'white', lineHeight: 1}}>{g.title}</div>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 40, color: C.yellow, lineHeight: 1.15, maxWidth: 520}}>{g.sub}</div>
        </div>
      </div>
    </Centered>
  );
};

const Checklist: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur);
  return (
    <Centered y={g.y ?? 420} style={{opacity: exit}}>
      <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 38, color: 'white', marginBottom: 10, letterSpacing: 1, ...stroke(8)}}>UNTUNG BERSAMA</div>
      <div style={{display: 'flex', gap: 16, flexWrap: 'wrap', justifyContent: 'center'}}>
        {(g.items as [string, number][]).map(([name, at], i) => {
          const f = Math.round((at - g.start) * fps);
          const s = spring({frame: frame - f, fps, config: {damping: 11, stiffness: 260, mass: 0.5}});
          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                background: 'white',
                borderRadius: 999,
                padding: '10px 22px 10px 10px',
                boxShadow: '0 10px 24px rgba(0,0,0,0.35)',
                transform: `scale(${s})`,
                opacity: s,
              }}
            >
              <Check size={46} />
              <span style={{fontFamily: MONT, fontWeight: 900, fontSize: 36, color: C.black}}>{name}</span>
            </div>
          );
        })}
      </div>
    </Centered>
  );
};

const Warning: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur);
  const s = spring({frame, fps, config: {damping: 10, stiffness: 260, mass: 0.6}});
  const shake = frame < 12 ? Math.sin(frame * 2.6) * (12 - frame) * 1.3 : 0;
  const blink = frame % 16 < 8 ? 1 : 0.75;
  return (
    <Centered y={g.y ?? 400} style={{opacity: exit}}>
      <div
        style={{
          padding: 12,
          borderRadius: 26,
          background: `repeating-linear-gradient(-45deg, ${C.yellow} 0 26px, #111 26px 52px)`,
          transform: `translateX(${shake}px) scale(${interpolate(s, [0, 1], [1.8, 1])})`,
          opacity: interpolate(s, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
          boxShadow: '0 18px 50px rgba(0,0,0,0.5)',
        }}
      >
        <div style={{background: `rgba(220,38,38,${blink})`, borderRadius: 16, padding: '16px 40px', textAlign: 'center'}}>
          <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 36, color: C.yellow, letterSpacing: 3}}>⚠ AMARAN CUACA</div>
          <div style={{fontFamily: ANTON, fontSize: 116, color: 'white', lineHeight: 1.05}}>{g.text}</div>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 34, color: 'white'}}>{g.sub}</div>
        </div>
      </div>
    </Centered>
  );
};

const Heat: React.FC<{g: G}> = ({g}) => {
  const {frame, D} = useAnim(g.dur);
  const o = interpolate(frame, [0, 10, D - 10, D], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const pulse = 0.85 + Math.sin(frame / 6) * 0.15;
  return (
    <AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(255,120,20,0.55), rgba(255,60,0,0.12) 60%, rgba(255,140,0,0.35))', mixBlendMode: 'overlay'}} />
      <div
        style={{
          position: 'absolute',
          right: 120,
          top: 250,
          width: 260,
          height: 260,
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(255,240,180,0.95) 0%, rgba(255,170,40,0.55) 45%, rgba(255,120,0,0) 72%)',
          transform: `scale(${pulse})`,
          mixBlendMode: 'screen',
        }}
      />
    </AbsoluteFill>
  );
};

const Question: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur, 5);
  const len: number = g.text.length;
  const chars = Math.floor(interpolate(frame, [0, Math.round(0.55 * fps)], [0, len], {extrapolateRight: 'clamp'}));
  return (
    <Centered y={g.y ?? 400} style={{opacity: exit}}>
      <div style={{fontFamily: ANTON, fontSize: 112, color: 'white', textAlign: 'center', lineHeight: 1.05, ...stroke(14)}}>
        {g.text.slice(0, chars).replace('?', '')}
        {chars >= g.text.length ? <span style={{color: C.yellow}}>?</span> : null}
      </div>
    </Centered>
  );
};

const EndCard: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter} = useAnim(g.dur, 1);
  const cta = spring({frame: frame - 12, fps, config: {damping: 11, stiffness: 200}});
  const pulse = 1 + Math.max(0, Math.sin((frame - 20) / 5)) * 0.05;
  return (
    <Centered y={g.y ?? 1060}>
      <div
        style={{
          width: SAFE_W - 20,
          background: 'linear-gradient(160deg, rgba(6,78,59,0.95), rgba(22,163,74,0.95))',
          borderRadius: 36,
          padding: '30px 34px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.5)',
          transform: `translateY(${interpolate(enter, [0, 1], [300, 0])}px)`,
          opacity: enter,
          textAlign: 'center',
          border: '4px solid rgba(255,255,255,0.7)',
        }}
      >
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 38, color: C.yellow, letterSpacing: 1.5}}>{g.line1.toUpperCase()}</div>
        <div style={{fontFamily: ANTON, fontSize: 82, color: 'white', lineHeight: 1.08, marginTop: 6}}>{g.line2.toUpperCase()}</div>
        <div
          style={{
            display: 'inline-block',
            marginTop: 20,
            background: C.yellow,
            color: C.black,
            fontFamily: MONT,
            fontWeight: 900,
            fontSize: 38,
            padding: '14px 30px',
            borderRadius: 999,
            transform: `scale(${cta * pulse})`,
          }}
        >
          ➦ {g.cta}
        </div>
      </div>
    </Centered>
  );
};

const Sticker: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur, 6);
  const s = spring({frame, fps, config: {damping: 7, stiffness: 300, mass: 0.5}});
  const wiggle = Math.sin(frame / 2.5) * 8 * Math.max(0, 1 - frame / 20);
  return (
    <Centered y={g.y ?? 420} style={{opacity: exit}}>
      <div
        style={{
          width: 170,
          height: 170,
          borderRadius: '50%',
          background: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 112,
          boxShadow: '0 12px 34px rgba(0,0,0,0.4)',
          border: `8px solid ${C.yellow}`,
          transform: `scale(${s}) rotate(${-10 + wiggle}deg)`,
        }}
      >
        {g.emoji}
      </div>
    </Centered>
  );
};

// ------------------------------------------------------------------------------ libaturus pieces
const Search: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur, 6);
  const t0 = Math.round((g.typeAt ?? 0.4) * fps);
  const td = Math.round((g.typeDur ?? 1.2) * fps);
  const text: string = g.text;
  const n = Math.floor(interpolate(frame, [t0, t0 + td], [0, text.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const caret = frame % 16 < 9;
  const done = frame >= t0 + td;
  const sugg: string[] = g.suggest ?? [];
  const press = spring({frame: frame - t0 - td - 2, fps, config: {damping: 10, stiffness: 300, mass: 0.4}});
  return (
    <Centered y={g.y ?? 960} style={{opacity: exit}}>
      <div
        style={{
          width: SAFE_W - 40,
          background: 'white',
          borderRadius: 44,
          boxShadow: '0 22px 60px rgba(0,0,0,0.5)',
          transform: `translateY(${interpolate(enter, [0, 1], [120, 0])}px) scale(${interpolate(enter, [0, 1], [0.85, 1]) * (done ? 1 + 0.03 * Math.sin(press * Math.PI) : 1)})`,
          opacity: enter,
          overflow: 'hidden',
        }}
      >
        <div style={{display: 'flex', alignItems: 'center', gap: 20, padding: '24px 32px'}}>
          <svg width="52" height="52" viewBox="0 0 48 48">
            <circle cx="20" cy="20" r="13" stroke="#5F6368" strokeWidth="5" fill="none" />
            <path d="M30 30 L42 42" stroke="#5F6368" strokeWidth="6" strokeLinecap="round" />
          </svg>
          <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 54, color: n ? '#111' : '#9AA0A6', whiteSpace: 'nowrap', flex: 1}}>
            {n ? text.slice(0, n) : 'Cari...'}
            <span style={{opacity: caret ? 1 : 0, color: C.green, fontWeight: 400}}>|</span>
          </div>
        </div>
        {sugg.map((s, i) => {
          const sp = spring({frame: frame - t0 - td - 4 - i * 4, fps, config: {damping: 14, stiffness: 220}});
          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                padding: '14px 36px',
                borderTop: '2px solid #EEE',
                fontFamily: MONT,
                fontWeight: 600,
                fontSize: 40,
                color: '#333',
                opacity: sp,
                height: interpolate(sp, [0, 1], [0, 78]),
                boxSizing: 'border-box',
                overflow: 'hidden',
              }}
            >
              <svg width="34" height="34" viewBox="0 0 48 48">
                <circle cx="20" cy="20" r="13" stroke="#9AA0A6" strokeWidth="5" fill="none" />
                <path d="M30 30 L42 42" stroke="#9AA0A6" strokeWidth="6" strokeLinecap="round" />
              </svg>
              {s}
            </div>
          );
        })}
      </div>
    </Centered>
  );
};

const Lower: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur, 8);
  const bar = spring({frame, fps, config: {damping: 16, stiffness: 160}});
  const txt = spring({frame: frame - 6, fps, config: {damping: 15, stiffness: 180}});
  return (
    <div style={{position: 'absolute', left: SAFE.left, top: g.y ?? 1080, transform: 'translateY(-50%)', opacity: exit}}>
      <div style={{display: 'flex', alignItems: 'stretch', overflow: 'hidden', borderRadius: 14, boxShadow: '0 14px 34px rgba(0,0,0,0.45)', width: interpolate(bar, [0, 1], [0, SAFE_W - 60])}}>
        <div style={{width: 16, background: C.yellow, flexShrink: 0}} />
        <div style={{background: 'linear-gradient(120deg, rgba(6,78,59,0.96), rgba(22,163,74,0.94))', padding: '16px 26px', flex: 1, whiteSpace: 'nowrap'}}>
          <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 40, color: 'white', transform: `translateX(${interpolate(txt, [0, 1], [-40, 0])}px)`, opacity: txt}}>{g.name}</div>
          <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 32, color: C.yellow, transform: `translateX(${interpolate(txt, [0, 1], [-60, 0])}px)`, opacity: txt, letterSpacing: 0.5}}>{g.role}</div>
        </div>
      </div>
    </div>
  );
};

const Nope: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur, 6);
  const s = spring({frame, fps, config: {damping: 11, stiffness: 260, mass: 0.6}});
  const sf = Math.round((g.strike ?? 0.6) * fps);
  const strike = interpolate(frame, [sf, sf + 5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const x = spring({frame: frame - sf - 3, fps, config: {damping: 8, stiffness: 300, mass: 0.5}});
  const shake = frame >= sf && frame < sf + 10 ? Math.sin((frame - sf) * 2.4) * (10 - (frame - sf)) * 1.4 : 0;
  return (
    <Centered y={g.y ?? 960} style={{opacity: exit}}>
      <div style={{transform: `translateX(${shake}px) scale(${interpolate(s, [0, 1], [1.6, 1])})`, opacity: interpolate(s, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}), display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 34, letterSpacing: 3, color: 'white', background: C.red, padding: '8px 22px', borderRadius: 10, marginBottom: 12}}>{g.kicker}</div>
        <div style={{position: 'relative'}}>
          <div style={{fontFamily: ANTON, fontSize: 118, lineHeight: 1.02, color: 'white', textAlign: 'center', textShadow: '0 12px 30px rgba(0,0,0,0.55)', ...stroke(14), opacity: interpolate(strike, [0, 1], [1, 0.8])}}>
            {g.text}
          </div>
          <div style={{position: 'absolute', left: -14, right: -14, top: '50%', height: 20, background: C.red, borderRadius: 10, transform: `rotate(-6deg) scaleX(${strike})`, transformOrigin: 'left center', boxShadow: '0 4px 14px rgba(0,0,0,0.5)'}} />
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          right: 10,
          top: -70,
          width: 130,
          height: 130,
          borderRadius: '50%',
          background: C.red,
          border: '8px solid white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: MONT,
          fontWeight: 900,
          fontSize: 86,
          color: 'white',
          transform: `scale(${x}) rotate(${interpolate(x, [0, 1], [-40, 8])}deg)`,
          boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
        }}
      >
        ✕
      </div>
    </Centered>
  );
};

const Hashtag: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur, 8);
  const text: string = g.text;
  const sweep = interpolate(frame, [10, 24], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const glow = 0.5 + 0.5 * Math.sin(frame / 5);
  const hs = spring({frame, fps, config: {damping: 9, stiffness: 240, mass: 0.6}});
  const fontSize = text.length > 10 ? 112 : 140;
  return (
    <>
      {frame < 40 ? <Confetti seed={text} /> : null}
      <Centered y={g.y ?? 960} style={{opacity: exit}}>
        <div style={{display: 'flex', alignItems: 'baseline'}}>
          <span
            style={{
              fontFamily: ANTON,
              fontSize: fontSize * 1.15,
              color: C.green,
              transform: `scale(${hs}) rotate(${interpolate(hs, [0, 1], [-30, -8])}deg)`,
              display: 'inline-block',
              marginRight: 6,
              ...stroke(14, 'white'),
            }}
          >
            #
          </span>
          {text.split('').map((ch, i) => {
            const s = spring({frame: frame - 2 - i * 1.2, fps, config: {damping: 11, stiffness: 260, mass: 0.45}});
            const hi = i >= 4; // FAMA | SANTUNI
            return (
              <span
                key={i}
                style={{
                  display: 'inline-block',
                  fontFamily: ANTON,
                  fontSize,
                  lineHeight: 1,
                  color: hi ? C.yellow : 'white',
                  transform: `translateY(${interpolate(s, [0, 1], [-70, 0])}px) scale(${interpolate(s, [0, 1], [1.8, 1])})`,
                  opacity: interpolate(s, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
                  textShadow: hi ? `0 0 ${18 + glow * 22}px rgba(255,214,10,${0.45 + glow * 0.35}), 0 12px 30px rgba(0,0,0,0.6)` : '0 12px 30px rgba(0,0,0,0.6)',
                  ...stroke(13),
                }}
              >
                {ch}
              </span>
            );
          })}
        </div>
        <div style={{height: 14, width: `${sweep * 92}%`, background: `linear-gradient(90deg, ${C.green}, ${C.yellow})`, borderRadius: 7, marginTop: 10, boxShadow: '0 6px 18px rgba(0,0,0,0.4)'}} />
      </Centered>
    </>
  );
};

const Goal: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur, 8);
  const total: number = g.total ?? 13;
  const done: number = g.done ?? 10;
  const pf = Math.round((g.pending ?? 99) * fps);
  const pend = frame >= pf;
  return (
    <Centered y={g.y ?? 960} style={{opacity: exit}}>
      <div
        style={{
          width: SAFE_W - 20,
          background: 'rgba(11,11,11,0.78)',
          borderRadius: 34,
          padding: '24px 30px 30px',
          border: '3px solid rgba(255,255,255,0.25)',
          boxShadow: '0 18px 50px rgba(0,0,0,0.45)',
          transform: `scale(${interpolate(enter, [0, 1], [0.7, 1])})`,
          opacity: enter,
          textAlign: 'center',
        }}
      >
        <div style={{display: 'inline-block', fontFamily: MONT, fontWeight: 900, fontSize: 34, color: C.black, background: C.yellow, padding: '6px 20px', borderRadius: 10, letterSpacing: 2}}>{g.kicker}</div>
        <div style={{fontFamily: ANTON, fontSize: 62, color: 'white', lineHeight: 1.1, marginTop: 10}}>{g.title}</div>
        <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 14, marginTop: 18}}>
          {new Array(total).fill(0).map((_, i) => {
            const isDone = i < done;
            const s = spring({frame: frame - 10 - i * 3, fps, config: {damping: 12, stiffness: 260, mass: 0.5}});
            const p = pend && !isDone ? 1 + 0.12 * Math.sin((frame - pf) / 3) : 1;
            return (
              <div
                key={i}
                style={{
                  width: 84,
                  height: 84,
                  borderRadius: '50%',
                  background: isDone ? C.green : pend ? C.red : 'rgba(255,255,255,0.18)',
                  border: `5px solid ${isDone ? '#B9F6CA' : pend ? '#FFD4D4' : 'rgba(255,255,255,0.4)'}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontFamily: MONT,
                  fontWeight: 900,
                  fontSize: 44,
                  color: 'white',
                  transform: `scale(${s * p})`,
                }}
              >
                {isDone ? '☕' : pend ? '?' : ''}
              </div>
            );
          })}
        </div>
      </div>
    </Centered>
  );
};

const Ladder: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur, 8);
  const sf = Math.round(g.strike * fps);
  const hf = Math.round(g.hero * fps);
  const cf = Math.round(g.chip * fps);
  const hero = spring({frame: frame - hf, fps, config: {damping: 9, stiffness: 240, mass: 0.6}});
  const chip = spring({frame: frame - cf, fps, config: {damping: 10, stiffness: 260}});
  // once the hero price lands, the other franchises shrink into a small strip at the top
  const away = spring({frame: frame - hf + 4, fps, config: {damping: 16, stiffness: 180}});
  const items = g.items as [string, number][];
  return (
    <Centered y={g.y ?? 960} style={{opacity: exit}}>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          transform: `translateY(${interpolate(away, [0, 1], [0, -150])}px) scale(${interpolate(away, [0, 1], [1, 0.55])})`,
          opacity: interpolate(away, [0, 1], [1, 0.8]),
          marginBottom: interpolate(away, [0, 1], [0, -235]),
        }}
      >
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 36, color: 'white', background: 'rgba(11,11,11,0.78)', padding: '6px 20px', borderRadius: 10, letterSpacing: 2, opacity: enter}}>{g.label}</div>
        {items.map(([name, at], i) => {
          const f = Math.round(at * fps);
          const s = spring({frame: frame - f, fps, config: {damping: 10, stiffness: 260, mass: 0.5}});
          const st = interpolate(frame, [sf + i * 3, sf + i * 3 + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <div key={i} style={{position: 'relative', marginTop: 12, transform: `scale(${s})`, opacity: s}}>
              <div
                style={{
                  fontFamily: ANTON,
                  fontSize: 100,
                  lineHeight: 1.05,
                  color: 'white',
                  background: `rgba(220,38,38,${0.92 - st * 0.35})`,
                  padding: '2px 34px',
                  borderRadius: 16,
                  boxShadow: '0 10px 26px rgba(0,0,0,0.45)',
                }}
              >
                {name}
              </div>
              <div style={{position: 'absolute', left: -14, right: -14, top: '47%', height: 14, background: C.yellow, borderRadius: 7, transform: `rotate(-7deg) scaleX(${st})`, transformOrigin: 'left center', boxShadow: '0 3px 10px rgba(0,0,0,0.5)'}} />
            </div>
          );
        })}
      </div>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: interpolate(hero, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}), transform: `scale(${interpolate(hero, [0, 1], [2.2, 1])}) rotate(-3deg)`, height: frame < hf ? 0 : undefined}}>
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 38, color: C.black, background: C.yellow, padding: '6px 20px', borderRadius: 10}}>{g.heroLabel}</div>
        <div style={{fontFamily: ANTON, fontSize: 220, lineHeight: 1, color: C.yellow, textShadow: '0 14px 40px rgba(0,0,0,0.55)', ...stroke(18)}}>{g.heroText}</div>
      </div>
      <div style={{marginTop: 6, fontFamily: MONT, fontWeight: 900, fontSize: 44, color: 'white', background: C.green, padding: '10px 28px', borderRadius: 999, transform: `scale(${chip})`, boxShadow: '0 10px 26px rgba(0,0,0,0.45)', height: frame < cf ? 0 : undefined, overflow: 'hidden'}}>🔒 {g.chipText}</div>
    </Centered>
  );
};

const Roi: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur, 8);
  const count = Math.round(interpolate(frame, [0, Math.round(0.75 * fps)], [1, g.value], {extrapolateRight: 'clamp', easing: (t) => 1 - Math.pow(1 - t, 3)}));
  const landed = frame >= Math.round(0.75 * fps);
  const slam = spring({frame: frame - Math.round(0.75 * fps), fps, config: {damping: 8, stiffness: 300, mass: 0.6}});
  const sf = Math.round(g.stamp * fps);
  const st = spring({frame: frame - sf, fps, config: {damping: 10, stiffness: 280, mass: 0.7}});
  return (
    <>
      {frame >= sf && frame < sf + 50 ? <Confetti seed={'roi' + g.start} /> : null}
      <Centered y={g.y ?? 960} style={{opacity: exit}}>
        <div style={{display: 'flex', alignItems: 'flex-end', gap: 18, opacity: enter}}>
          <div style={{fontFamily: ANTON, fontSize: 260, lineHeight: 0.9, color: C.yellow, transform: `scale(${landed ? interpolate(slam, [0, 1], [1.35, 1]) : 1})`, textShadow: '0 14px 40px rgba(0,0,0,0.55)', ...stroke(18), minWidth: 300, textAlign: 'right'}}>{count}</div>
          <div style={{fontFamily: ANTON, fontSize: 100, color: 'white', marginBottom: 24, ...stroke(12)}}>{g.unit}</div>
        </div>
        <div
          style={{
            marginTop: 10,
            fontFamily: ANTON,
            fontSize: 92,
            color: C.yellow,
            padding: '6px 30px',
            border: `9px solid ${C.yellow}`,
            borderRadius: 22,
            background: 'rgba(6,78,59,0.9)',
            transform: `scale(${interpolate(st, [0, 1], [3, 1])}) rotate(-6deg)`,
            opacity: interpolate(st, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'}),
            boxShadow: '0 16px 50px rgba(0,0,0,0.5)',
            whiteSpace: 'nowrap',
          }}
        >
          ✓ {g.stampText}
        </div>
      </Centered>
    </>
  );
};

export const Graphic: React.FC<{g: G}> = ({g}) => {
  switch (g.type) {
    case 'headline':
      return <Headline g={g} />;
    case 'bigstat':
      return <BigStat g={g} />;
    case 'location':
      return <Location g={g} />;
    case 'combo':
      return <Combo g={g} />;
    case 'stamp':
      return <Stamp g={g} />;
    case 'price':
      return <Price g={g} />;
    case 'tag':
      return <Tag g={g} />;
    case 'calendar':
      return <Calendar g={g} />;
    case 'sara':
      return <Sara g={g} />;
    case 'checklist':
      return <Checklist g={g} />;
    case 'warning':
      return <Warning g={g} />;
    case 'heat':
      return <Heat g={g} />;
    case 'sticker':
      return <Sticker g={g} />;
    case 'question':
      return <Question g={g} />;
    case 'endcard':
      return <EndCard g={g} />;
    case 'search':
      return <Search g={g} />;
    case 'lower':
      return <Lower g={g} />;
    case 'nope':
      return <Nope g={g} />;
    case 'hashtag':
      return <Hashtag g={g} />;
    case 'goal':
      return <Goal g={g} />;
    case 'ladder':
      return <Ladder g={g} />;
    case 'roi':
      return <Roi g={g} />;
    default:
      return null;
  }
};
