import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Freeze,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import timeline from './timeline.json';
import {Captions} from './Captions';
import {Graphic} from './Graphics';

type Zoom = {start: number; scale: number; piece: string; ox?: number; oy?: number};
const zooms = timeline.zooms as Zoom[];
const pieces = timeline.pieces as {id: string; start: number; end: number; soft?: boolean}[];

const MUSIC = 'music/m33.mp3';
const freezes = ((timeline as any).freezes ?? []) as {start: number; end: number}[];
// Closing logo sting (landscape 1920x1080, 5 s, no audio) appended after the edit.
export const CLOSING_FRAMES = 150;
const MAIN_FRAMES = timeline.durationInFrames;

const Closing: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const w = 920; // keeps the logo clear of the TikTok/IG right-hand buttons
  return (
    <AbsoluteFill style={{backgroundColor: 'black', opacity: o}}>
      <div style={{position: 'absolute', left: 500 - w / 2, top: 940 - (w * 9) / 32, width: w, height: (w * 9) / 16}}>
        <OffthreadVideo src={staticFile('closing/closing.mp4')} muted style={{width: '100%', height: '100%'}} />
      </div>
    </AbsoluteFill>
  );
};

const FadeToBlack: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [MAIN_FRAMES - 10, MAIN_FRAMES - 1], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{backgroundColor: 'black', opacity: o}} />;
};

const useZoom = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  let i = -1;
  for (let k = 0; k < zooms.length; k++) if (zooms[k].start <= t + 1e-6) i = k;
  if (i < 0) return {scale: 1, ox: 0.5, oy: 0.35};
  const cur = zooms[i];
  const prev = i > 0 && zooms[i - 1].piece === cur.piece ? zooms[i - 1] : {...cur, scale: cur.scale};
  const p = spring({frame: frame - Math.round(cur.start * fps), fps, config: {damping: 22, stiffness: 260, mass: 0.6}});
  const scale = prev.scale + (cur.scale - prev.scale) * p;
  const ox = (prev.ox ?? 0.5) + ((cur.ox ?? 0.5) - (prev.ox ?? 0.5)) * p;
  const oy = (prev.oy ?? 0.35) + ((cur.oy ?? 0.35) - (prev.oy ?? 0.35)) * p;
  return {scale, ox, oy};
};

const Footage: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {scale, ox, oy} = useZoom();
  const t = frame / fps;
  const fz = freezes.find((f) => t >= f.start && t < f.end + 0.05);
  if (fz) return <PhotoFreeze start={fz.start} />;
  // little "push" at every new section
  let bump = 1;
  for (const p of pieces) {
    const f0 = Math.round(p.start * fps);
    if (f0 > 0 && !p.soft && frame >= f0 && frame < f0 + 10) bump = interpolate(frame - f0, [0, 9], [1.07, 1], {extrapolateRight: 'clamp'});
  }
  return (
    <AbsoluteFill style={{transform: `scale(${scale * bump})`, transformOrigin: `${ox * 100}% ${oy * 100}%`}}>
      <OffthreadVideo src={staticFile('footage/base.mp4')} />
    </AbsoluteFill>
  );
};

// Group photo: the picture freezes, flashes white and drops into a tilted print over a blurred copy.
const PhotoFreeze: React.FC<{start: number}> = ({start}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const f0 = Math.round(start * fps);
  const k = frame - f0;
  const s = spring({frame: k - 2, fps, config: {damping: 14, stiffness: 160, mass: 0.8}});
  const flash = interpolate(k, [0, 2, 9], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const vid = <OffthreadVideo src={staticFile('footage/base.mp4')} muted />;
  return (
    <AbsoluteFill>
      <Freeze frame={f0}>
        <AbsoluteFill style={{filter: 'blur(28px) brightness(0.55)', transform: 'scale(1.15)'}}>{vid}</AbsoluteFill>
        <div
          style={{
            position: 'absolute',
            left: 500 - 410,
            top: 250,
            width: 820,
            height: 1100,
            background: 'white',
            padding: '22px 22px 90px',
            boxSizing: 'border-box',
            boxShadow: '0 30px 80px rgba(0,0,0,0.6)',
            transform: `scale(${interpolate(s, [0, 1], [1.25, 1])}) rotate(${interpolate(s, [0, 1], [0, -3])}deg)`,
          }}
        >
          <div style={{width: '100%', height: '100%', overflow: 'hidden', position: 'relative'}}>
            <div style={{position: 'absolute', left: 388 - 540 * 1.15, top: 494 - 1170 * 1.15, width: 1080, height: 1920, transform: 'scale(1.15)', transformOrigin: '0 0'}}>{vid}</div>
          </div>
        </div>
      </Freeze>
      <AbsoluteFill style={{backgroundColor: 'white', opacity: flash}} />
    </AbsoluteFill>
  );
};

const SectionFlash: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  let o = 0;
  for (const p of pieces) {
    const f0 = Math.round(p.start * fps);
    if (f0 > 0 && !p.soft && frame >= f0 && frame < f0 + 6) o = interpolate(frame - f0, [0, 5], [0.45, 0]);
  }
  return <AbsoluteFill style={{backgroundColor: 'white', opacity: o, pointerEvents: 'none'}} />;
};

// soft vignette + bottom gradient so captions stay readable on bright footage
const Grade: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        'radial-gradient(ellipse at 50% 40%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.28) 100%), linear-gradient(to bottom, rgba(0,0,0,0) 55%, rgba(0,0,0,0.30) 100%)',
    }}
  />
);

const musicVolume = (frame: number, fps: number, total: number) => {
  const t = frame / fps;
  let d = 99;
  for (const [s, e] of timeline.speech as number[][]) {
    if (t >= s && t <= e) {
      d = 0;
      break;
    }
    d = Math.min(d, Math.abs(t - s), Math.abs(t - e));
  }
  const piece = pieces.find((p) => t >= p.start && t < p.end)?.id;
  const open = piece?.startsWith('m_') ? 0.34 : frame >= MAIN_FRAMES ? 0.3 : 0.24;
  const under = 0.075; // music sits ~-22 dB under the voice
  let v = interpolate(d, [0, 0.35], [under, open], {extrapolateRight: 'clamp'});
  v *= interpolate(frame, [0, 12], [0.6, 1], {extrapolateRight: 'clamp'});
  v *= interpolate(frame, [total - 75, total - 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return v;
};

export const Main: React.FC = () => {
  const {fps, durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      <Sequence durationInFrames={MAIN_FRAMES}>
        <Footage />
        <Grade />
        {(timeline.gfx as any[]).map((g, i) => (
          <Sequence key={i} from={Math.round(g.start * fps)} durationInFrames={Math.round(g.dur * fps)} layout="none">
            <Graphic g={g} />
          </Sequence>
        ))}
        <Captions />
        <SectionFlash />
        <FadeToBlack />
      </Sequence>
      <Sequence from={MAIN_FRAMES} durationInFrames={CLOSING_FRAMES}>
        <Closing />
      </Sequence>
      <Sequence from={MAIN_FRAMES + 4} durationInFrames={fps * 5} layout="none">
        <Audio src={staticFile('sfx/impact_logo.mp3')} volume={0.4} />
      </Sequence>

      <Audio src={staticFile(MUSIC)} loop volume={(f) => musicVolume(f, fps, durationInFrames)} />
      {(timeline.sfx as {name: string; start: number; volume: number}[]).map((s, i) => (
        <Sequence key={`s${i}`} from={Math.round(s.start * fps)} durationInFrames={fps * 6} layout="none">
          <Audio src={staticFile(`sfx/${s.name}.mp3`)} volume={s.volume} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
