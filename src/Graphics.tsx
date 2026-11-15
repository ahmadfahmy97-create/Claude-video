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

// ------------------------------------------------------------------------------ Harumanis additions
const Nametag: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const bar = spring({frame: frame - 2, fps, config: {damping: 16, stiffness: 160}});
  const role = spring({frame: frame - 7, fps, config: {damping: 14, stiffness: 200}});
  return (
    <div style={{position: 'absolute', left: SAFE.left, top: g.y ?? 1100, transform: 'translateY(-50%)', opacity: exit}}>
      <div style={{display: 'flex', alignItems: 'stretch', filter: 'drop-shadow(0 10px 24px rgba(0,0,0,0.45))'}}>
        <div style={{width: 12, background: C.mango, borderRadius: 6, transform: `scaleY(${bar})`}} />
        <div style={{marginLeft: 14, overflow: 'hidden'}}>
          <div
            style={{
              fontFamily: MONT,
              fontWeight: 900,
              fontSize: 40,
              color: C.black,
              background: 'white',
              padding: '8px 20px',
              borderRadius: 10,
              transform: `translateX(${interpolate(enter, [0, 1], [-640, 0])}px)`,
              whiteSpace: 'nowrap',
            }}
          >
            {g.name}
          </div>
          <div
            style={{
              display: 'inline-block',
              marginTop: 8,
              fontFamily: MONT,
              fontWeight: 800,
              fontSize: 32,
              letterSpacing: 2,
              color: 'white',
              background: C.green,
              padding: '6px 16px',
              borderRadius: 8,
              transform: `translateX(${interpolate(role, [0, 1], [-420, 0])}px)`,
            }}
          >
            {g.role.toUpperCase()}
          </div>
        </div>
      </div>
    </div>
  );
};

// "DULU <struck-out> -> KINI <stamped>" – tells the whole story in one card
const BeforeAfter: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const strike = interpolate(frame, [Math.round(0.9 * fps), Math.round(0.9 * fps) + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const now = spring({frame: frame - Math.round(1.2 * fps), fps, config: {damping: 10, stiffness: 240, mass: 0.6}});
  const label = (t: string, bg: string, fg: string) => (
    <span style={{fontFamily: MONT, fontWeight: 900, fontSize: 30, letterSpacing: 3, background: bg, color: fg, padding: '4px 14px', borderRadius: 8}}>{t}</span>
  );
  return (
    <Centered y={g.y ?? 1000} style={{opacity: exit}}>
      <div style={{opacity: enter, transform: `translateY(${interpolate(enter, [0, 1], [30, 0])}px)`, textAlign: 'center'}}>
        {label('DULU', 'rgba(11,11,11,0.85)', 'white')}
        <div style={{position: 'relative', display: 'inline-block', marginTop: 8}}>
          <div style={{fontFamily: ANTON, fontSize: 70, color: 'white', lineHeight: 1.05, opacity: interpolate(strike, [0, 1], [1, 0.7]), ...stroke(10)}}>{g.before}</div>
          <div
            style={{
              position: 'absolute',
              left: -12,
              top: '52%',
              height: 12,
              width: `${strike * 106}%`,
              background: C.red,
              borderRadius: 6,
              transform: 'rotate(-4deg)',
              transformOrigin: 'left center',
              boxShadow: '0 3px 10px rgba(0,0,0,0.5)',
            }}
          />
        </div>
      </div>
      <div
        style={{
          marginTop: 18,
          textAlign: 'center',
          opacity: interpolate(now, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
          transform: `scale(${interpolate(now, [0, 1], [1.8, 1])}) rotate(-3deg)`,
        }}
      >
        {label('KINI', C.mango, C.black)}
        <div style={{fontFamily: ANTON, fontSize: 92, color: C.mango, lineHeight: 1.02, marginTop: 6, textShadow: '0 12px 30px rgba(0,0,0,0.5)', ...stroke(14)}}>{g.after}</div>
      </div>
    </Centered>
  );
};

// camera-flash for the group photos
const Flash: React.FC<{g: G}> = ({g}) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 1, 10], [0, 0.85, 0], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{backgroundColor: 'white', opacity: o}} />;
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
    case 'nametag':
      return <Nametag g={g} />;
    case 'beforeafter':
      return <BeforeAfter g={g} />;
    case 'flash':
      return <Flash g={g} />;
    default:
      return null;
  }
};
