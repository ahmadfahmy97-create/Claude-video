// Motion graphics added for the FAMA x Indonesian delegation video (also reusable by other projects).
import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
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

// ------------------------------------------------------------------------------ flags (drawn, so they never depend on emoji fonts)
export const FlagID: React.FC<{w?: number}> = ({w = 60}) => (
  <svg width={w} height={(w * 2) / 3} viewBox="0 0 3 2" style={{borderRadius: 4, boxShadow: '0 2px 6px rgba(0,0,0,0.35)', display: 'block'}}>
    <rect width="3" height="1" fill="#E70011" />
    <rect y="1" width="3" height="1" fill="#FFFFFF" />
  </svg>
);

const starPoints = (cx: number, cy: number, n: number, r1: number, r2: number) => {
  const pts: string[] = [];
  for (let i = 0; i < n * 2; i++) {
    const r = i % 2 === 0 ? r1 : r2;
    const a = (Math.PI * i) / n - Math.PI / 2;
    pts.push(`${(cx + r * Math.cos(a)).toFixed(3)},${(cy + r * Math.sin(a)).toFixed(3)}`);
  }
  return pts.join(' ');
};

export const FlagMY: React.FC<{w?: number}> = ({w = 60}) => (
  <svg width={w} height={w / 2} viewBox="0 0 28 14" style={{borderRadius: 4, boxShadow: '0 2px 6px rgba(0,0,0,0.35)', display: 'block'}}>
    {new Array(14).fill(0).map((_, i) => (
      <rect key={i} y={i} width="28" height="1" fill={i % 2 === 0 ? '#CC0001' : '#FFFFFF'} />
    ))}
    <rect width="14" height="8" fill="#010066" />
    <circle cx="5.6" cy="4" r="3" fill="#FFCC00" />
    <circle cx="6.4" cy="4" r="2.55" fill="#010066" />
    <polygon points={starPoints(10.4, 4, 14, 2.3, 1.0)} fill="#FFCC00" />
  </svg>
);

// ------------------------------------------------------------------------------ hook: three Indonesian agencies merge into FAMA
const Agencies: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur);
  const items = g.items as [string, string, number][];
  const mf = Math.round((g.mergeAt - g.start) * fps);
  const merge = spring({frame: frame - mf, fps, config: {damping: 14, stiffness: 160, mass: 0.8}});
  const slam = spring({frame: frame - mf - 8, fps, config: {damping: 9, stiffness: 240, mass: 0.6}});
  const shake = frame > mf + 8 && frame < mf + 18 ? Math.sin(frame * 2.4) * (mf + 18 - frame) * 1.4 : 0;
  const ROW = 128;
  return (
    <Centered y={g.y ?? 980} style={{opacity: exit}}>
      <div style={{position: 'relative', width: SAFE_W, height: 3 * ROW + 20}}>
        {items.map(([abbr, full, at], i) => {
          const f = Math.round((at - g.start) * fps);
          const s = spring({frame: frame - f, fps, config: {damping: 12, stiffness: 220, mass: 0.6}});
          const y0 = i * ROW;
          const yc = ROW; // everything collapses into the middle row
          const y = interpolate(merge, [0, 1], [y0, yc]);
          const sc = interpolate(merge, [0, 1], [1, 0.55]);
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: 40,
                right: 40,
                top: y,
                height: ROW - 18,
                display: 'flex',
                alignItems: 'center',
                gap: 20,
                background: 'rgba(255,255,255,0.97)',
                borderRadius: 22,
                padding: '0 26px',
                boxShadow: '0 12px 30px rgba(0,0,0,0.4)',
                transform: `translateX(${interpolate(s, [0, 1], [i % 2 ? 700 : -700, 0])}px) scale(${sc})`,
                opacity: Math.min(s, interpolate(merge, [0.6, 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})),
              }}
            >
              <div style={{fontFamily: ANTON, fontSize: 40, color: 'white', background: '#E70011', borderRadius: 14, width: 64, height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                {i + 1}
              </div>
              <div style={{flex: 1, minWidth: 0}}>
                <div style={{fontFamily: ANTON, fontSize: 52, color: C.black, lineHeight: 1}}>{abbr}</div>
                <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 25, color: '#555', lineHeight: 1.2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{full}</div>
              </div>
              <FlagID w={66} />
            </div>
          );
        })}
        {/* result badge */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: ROW / 2 - 60,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            transform: `translateX(${shake}px) scale(${interpolate(slam, [0, 1], [2.6, 1])}) rotate(${interpolate(slam, [0, 1], [-12, -3])}deg)`,
            opacity: interpolate(slam, [0, 0.25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 22,
              background: 'linear-gradient(135deg, #065F46 0%, #16A34A 100%)',
              border: `8px solid ${C.yellow}`,
              borderRadius: 34,
              padding: '10px 42px 14px',
              boxShadow: '0 20px 60px rgba(0,0,0,0.55)',
            }}
          >
            <FlagMY w={110} />
            <div style={{fontFamily: ANTON, fontSize: 150, color: 'white', lineHeight: 1}}>{g.result}</div>
          </div>
          <div
            style={{
              marginTop: 14,
              fontFamily: MONT,
              fontWeight: 900,
              fontSize: 54,
              color: C.black,
              background: C.yellow,
              borderRadius: 999,
              padding: '8px 34px',
              boxShadow: '0 10px 28px rgba(0,0,0,0.45)',
            }}
          >
            {g.resultSub}
          </div>
        </div>
      </div>
    </Centered>
  );
};

// ------------------------------------------------------------------------------ Malaysia word = Indonesia word
const Kamus: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const r = spring({frame: frame - 7, fps, config: {damping: 12, stiffness: 220, mass: 0.6}});
  const eq = spring({frame: frame - 12, fps, config: {damping: 8, stiffness: 300, mass: 0.5}});
  const long = Math.max(g.my.length, g.id.length) > 9;
  const fs = long ? 50 : 66;
  const Side: React.FC<{flag: React.ReactNode; label: string; word: string; p: number; dir: number; bg: string}> = ({flag, label, word, p, dir, bg}) => (
    <div
      style={{
        flex: 1,
        background: bg,
        borderRadius: 24,
        padding: '18px 12px 20px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 10,
        boxShadow: '0 14px 34px rgba(0,0,0,0.45)',
        transform: `translateX(${interpolate(p, [0, 1], [dir * 500, 0])}px) rotate(${interpolate(p, [0, 1], [dir * 8, 0])}deg)`,
        opacity: p,
      }}
    >
      <div style={{display: 'flex', alignItems: 'center', gap: 12}}>
        {flag}
        <span style={{fontFamily: MONT, fontWeight: 900, fontSize: 24, letterSpacing: 2, color: 'rgba(255,255,255,0.92)'}}>{label}</span>
      </div>
      <div style={{fontFamily: ANTON, fontSize: fs, color: 'white', lineHeight: 1.02, textAlign: 'center'}}>{word}</div>
    </div>
  );
  return (
    <Centered y={g.y ?? 1000} style={{opacity: exit}}>
      <div
        style={{
          fontFamily: MONT,
          fontWeight: 900,
          fontSize: 30,
          letterSpacing: 3,
          color: C.black,
          background: C.yellow,
          borderRadius: 999,
          padding: '6px 22px',
          marginBottom: 14,
          opacity: enter,
          transform: `translateY(${interpolate(enter, [0, 1], [-30, 0])}px)`,
          boxShadow: '0 8px 20px rgba(0,0,0,0.35)',
        }}
      >
        📖 KAMUS SERUMPUN
      </div>
      <div style={{display: 'flex', alignItems: 'center', gap: 12, width: SAFE_W - 30}}>
        <Side flag={<FlagMY w={58} />} label="MALAYSIA" word={g.my} p={enter} dir={-1} bg="linear-gradient(160deg,#0B2A8A,#010066)" />
        <div
          style={{
            fontFamily: ANTON,
            fontSize: 84,
            color: C.yellow,
            transform: `scale(${eq})`,
            ...stroke(10),
          }}
        >
          =
        </div>
        <Side flag={<FlagID w={46} />} label="INDONESIA" word={g.id} p={r} dir={1} bg="linear-gradient(160deg,#E11D2A,#9B0E18)" />
      </div>
    </Centered>
  );
};

// ------------------------------------------------------------------------------ Malay proverb, typed in
const Proverb: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const lines = g.lines as string[];
  const total = lines.join(' ').length;
  const chars = Math.floor(interpolate(frame, [4, 4 + Math.round(1.4 * fps)], [0, total], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const m = spring({frame: frame - Math.round(1.6 * fps), fps, config: {damping: 12, stiffness: 200}});
  let used = 0;
  return (
    <Centered y={g.y ?? 980} style={{opacity: exit}}>
      <div
        style={{
          width: SAFE_W - 40,
          background: 'rgba(255,253,245,0.97)',
          borderRadius: 30,
          padding: '26px 36px 30px',
          boxShadow: '0 20px 56px rgba(0,0,0,0.5)',
          borderLeft: `16px solid ${C.green}`,
          transform: `scale(${interpolate(enter, [0, 1], [0.7, 1])}) rotate(${interpolate(enter, [0, 1], [-4, -1.2])}deg)`,
          opacity: enter,
          position: 'relative',
        }}
      >
        <div style={{position: 'absolute', right: 26, top: -36, fontFamily: ANTON, fontSize: 180, color: C.yellow, lineHeight: 1, ...stroke(10)}}>”</div>
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 28, letterSpacing: 3, color: C.green}}>{g.kicker}</div>
        {lines.map((l, i) => {
          const start = used;
          used += l.length + 1;
          const shown = Math.max(0, Math.min(l.length, chars - start));
          return (
            <div key={i} style={{fontFamily: MONT, fontWeight: 900, fontStyle: 'italic', fontSize: 58, color: C.black, lineHeight: 1.15, minHeight: 66}}>
              {l.slice(0, shown)}
              {shown > 0 && shown < l.length ? <span style={{color: C.green}}>|</span> : null}
            </div>
          );
        })}
        <div
          style={{
            display: 'inline-block',
            marginTop: 14,
            fontFamily: MONT,
            fontWeight: 800,
            fontSize: 34,
            color: 'white',
            background: C.deep,
            borderRadius: 12,
            padding: '6px 18px',
            opacity: m,
            transform: `translateY(${interpolate(m, [0, 1], [20, 0])}px)`,
          }}
        >
          {g.meaning}
        </div>
      </div>
    </Centered>
  );
};

// ------------------------------------------------------------------------------ event lower third
const Event: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, enter, exit} = useAnim(g.dur);
  const t2 = spring({frame: frame - 6, fps, config: {damping: 13, stiffness: 200}});
  return (
    <div
      style={{
        position: 'absolute',
        left: SAFE.left,
        top: g.y ?? 330,
        transform: `translateY(-50%) translateX(${interpolate(enter, [0, 1], [-900, 0])}px)`,
        opacity: exit,
        maxWidth: SAFE_W,
        display: 'flex',
        alignItems: 'stretch',
        borderRadius: 22,
        overflow: 'hidden',
        boxShadow: '0 14px 36px rgba(0,0,0,0.45)',
      }}
    >
      <div style={{background: C.green, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 8, padding: '0 18px'}}>
        <FlagMY w={58} />
        <FlagID w={44} />
      </div>
      <div style={{background: 'rgba(255,255,255,0.97)', padding: '14px 26px 16px'}}>
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 26, letterSpacing: 2.5, color: C.green}}>{g.kicker}</div>
        <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 40, color: C.black, lineHeight: 1.1, opacity: t2}}>{g.title}</div>
        <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 28, color: '#444', opacity: t2}}>{g.sub}</div>
      </div>
    </div>
  );
};

// ------------------------------------------------------------------------------ process chain
const Flow: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur);
  const items = g.items as [string, string, number][];
  const n = items.length;
  const W = SAFE_W - 20;
  const step = W / n;
  return (
    <Centered y={g.y ?? 1000} style={{opacity: exit}}>
      <div style={{position: 'relative', width: W, height: 220}}>
        {items.map(([icon, label, at], i) => {
          const f = Math.round((at - g.start) * fps);
          const s = spring({frame: frame - f, fps, config: {damping: 10, stiffness: 260, mass: 0.5}});
          const line = interpolate(frame - f, [0, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          const famaStep = label.startsWith('FAMA') || i >= 2;
          const cx = step * i + step / 2;
          return (
            <React.Fragment key={i}>
              {i > 0 ? (
                <div
                  style={{
                    position: 'absolute',
                    left: cx - step + 62,
                    top: 70,
                    height: 10,
                    width: (step - 124) * line,
                    background: C.yellow,
                    borderRadius: 5,
                    boxShadow: '0 3px 8px rgba(0,0,0,0.4)',
                  }}
                />
              ) : null}
              <div
                style={{
                  position: 'absolute',
                  left: cx - 62,
                  top: 13,
                  width: 124,
                  height: 124,
                  borderRadius: '50%',
                  background: famaStep ? C.green : 'white',
                  border: `6px solid ${famaStep ? C.yellow : C.green}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 62,
                  boxShadow: '0 12px 28px rgba(0,0,0,0.45)',
                  transform: `scale(${s})`,
                }}
              >
                {icon}
              </div>
              <div
                style={{
                  position: 'absolute',
                  left: cx - step / 2,
                  width: step,
                  top: 150,
                  textAlign: 'center',
                  fontFamily: MONT,
                  fontWeight: 900,
                  fontSize: label.length > 8 ? 26 : 32,
                  color: famaStep ? C.yellow : 'white',
                  opacity: s,
                  ...stroke(8),
                }}
              >
                {label}
              </div>
            </React.Fragment>
          );
        })}
      </div>
    </Centered>
  );
};

// ------------------------------------------------------------------------------ ✕ / ✓ rules
const Rule: React.FC<{g: G}> = ({g}) => {
  const {frame, fps, exit} = useAnim(g.dur);
  return (
    <Centered y={g.y ?? 1000} style={{opacity: exit, gap: 16}}>
      {(g.items as [string, string, number][]).map(([mark, text, at], i) => {
        const f = Math.round((at - g.start) * fps);
        const s = spring({frame: frame - f, fps, config: {damping: 11, stiffness: 260, mass: 0.5}});
        const good = mark === '✓';
        return (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 18,
              background: good ? C.green : '#B91C1C',
              borderRadius: 999,
              padding: '10px 36px 10px 12px',
              boxShadow: '0 12px 28px rgba(0,0,0,0.4)',
              transform: `scale(${interpolate(s, [0, 1], [1.8, 1])}) rotate(${good ? -2 : 2}deg)`,
              opacity: interpolate(s, [0, 0.3], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            }}
          >
            <div
              style={{
                width: 70,
                height: 70,
                borderRadius: '50%',
                background: 'white',
                color: good ? C.green : '#B91C1C',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: MONT,
                fontWeight: 900,
                fontSize: 48,
              }}
            >
              {mark}
            </div>
            <span style={{fontFamily: ANTON, fontSize: 64, color: 'white', letterSpacing: 1}}>{text}</span>
          </div>
        );
      })}
    </Centered>
  );
};

export const extraGraphic = (g: G): React.ReactElement | null => {
  switch (g.type) {
    case 'agencies':
      return <Agencies g={g} />;
    case 'kamus':
      return <Kamus g={g} />;
    case 'proverb':
      return <Proverb g={g} />;
    case 'event':
      return <Event g={g} />;
    case 'flow':
      return <Flow g={g} />;
    case 'rule':
      return <Rule g={g} />;
    default:
      return null;
  }
};
