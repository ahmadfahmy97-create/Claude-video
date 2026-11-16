import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import timeline from './timeline.json';
import {C, CX, MONT, SAFE_W, stroke} from './theme';

type Word = {text: string; start: number; end: number};
type Page = {start: number; end: number; words: Word[]; y?: number};

const KEY = /^(RM\d+|\d+|FAMA|OKU|Quran|Bahasa|Isyarat|solat|sempurna|menangis|khusyuk|pekak|tepuk|ribu|diluluskan|dunia|pasar|tani)[.,!?]?$/i;

export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const page = (timeline.captions as Page[]).find((p) => t >= p.start && t < p.end);
  if (!page) return null;
  const f0 = Math.round(page.start * fps);
  const pop = spring({frame: frame - f0, fps, config: {damping: 13, stiffness: 240, mass: 0.5}});
  const y = page.y ?? 1300;
  return (
    <div
      style={{
        position: 'absolute',
        left: CX - SAFE_W / 2,
        width: SAFE_W,
        top: y,
        transform: `translateY(-50%) scale(${interpolate(pop, [0, 1], [0.82, 1])})`,
        opacity: interpolate(pop, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'}),
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        alignContent: 'center',
        gap: '0px 24px',
        textAlign: 'center',
        fontFamily: MONT,
        fontWeight: 900,
        fontSize: 70,
        lineHeight: 1.12,
        letterSpacing: -0.5,
      }}
    >
      {page.words.map((w, i) => {
        const active = t >= w.start && t < (page.words[i + 1]?.start ?? page.end);
        const spoken = t >= w.start;
        const key = KEY.test(w.text);
        const wf = Math.round(w.start * fps);
        const wp = spring({frame: frame - wf, fps, config: {damping: 12, stiffness: 300, mass: 0.4}});
        const scale = active ? interpolate(wp, [0, 1], [1.0, 1.05]) : 1;
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              color: active ? C.yellow : key && spoken ? '#B9F6CA' : C.white,
              opacity: spoken ? 1 : 0.92,
              transform: `scale(${scale})`,
              textShadow: '0 6px 18px rgba(0,0,0,0.55)',
              ...stroke(13),
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
