import React from 'react';
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import data from './montage.json';
import {Overlay} from './Overlays';

export type Shot = {
  src: string; // file in public/mz
  from: number; // frame in the edit
  dur: number; // frames
  in: number; // seconds into the source clip
  vol: number; // 0 for b-roll, ~1 for a soundbite
  z0: number; // Ken Burns start/end scale
  z1: number;
  ox: number; // transform origin (0..1)
  oy: number;
  fadeIn?: number; // cross-dissolve frames from the previous shot
  speed?: number;
};

const shots = data.shots as Shot[];
export const MAIN = data.durationInFrames;
export const CLOSING = 125;

const ShotView: React.FC<{s: Shot}> = ({s}) => {
  const f = useCurrentFrame();
  const z = interpolate(f, [0, s.dur], [s.z0, s.z1]);
  const o = s.fadeIn ? interpolate(f, [0, s.fadeIn], [0, 1], {extrapolateRight: 'clamp'}) : 1;
  // short audio fades so soundbites never click
  const af = Math.min(1, f / 4, (s.dur - f) / 6);
  return (
    <AbsoluteFill style={{opacity: o, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${z})`, transformOrigin: `${s.ox * 100}% ${s.oy * 100}%`}}>
        <OffthreadVideo
          src={staticFile(`mz/${s.src}`)}
          startFrom={Math.round(s.in * 25)}
          playbackRate={s.speed ?? 1}
          volume={Math.max(0, s.vol * af)}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// warm filmic look: gentle vignette + soft top/bottom gradients so type stays readable
const Grade: React.FC = () => (
  <AbsoluteFill
    style={{
      pointerEvents: 'none',
      background:
        'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.38) 100%), linear-gradient(to bottom, rgba(0,0,0,0.18) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 72%, rgba(0,0,0,0.32) 100%)',
    }}
  />
);

const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity: 0.06, mixBlendMode: 'overlay'}}>
      <svg width="1920" height="1080">
        <filter id="g">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 12} />
        </filter>
        <rect width="1920" height="1080" filter="url(#g)" />
      </svg>
    </AbsoluteFill>
  );
};

const Flashes: React.FC = () => {
  const f = useCurrentFrame();
  let o = 0;
  for (const t of data.flashes as number[]) if (f >= t && f < t + 7) o = Math.max(o, interpolate(f - t, [0, 6], [0.55, 0]));
  return <AbsoluteFill style={{backgroundColor: '#fff8e0', opacity: o, pointerEvents: 'none'}} />;
};

const Fades: React.FC = () => {
  const f = useCurrentFrame();
  const o = Math.max(
    interpolate(f, [0, 12], [1, 0], {extrapolateRight: 'clamp'}),
    interpolate(f, [MAIN - 14, MAIN - 1], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
  );
  return <AbsoluteFill style={{backgroundColor: 'black', opacity: o}} />;
};

const Closing: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 8, CLOSING - 12, CLOSING - 1], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: 'black', opacity: o}}>
      <OffthreadVideo src={staticFile('closing/closing.mp4')} muted />
    </AbsoluteFill>
  );
};

const music = data.music as {src: string; offset: number; volume: number};
const ducks = data.ducks as [number, number][]; // frame ranges where the chairman speaks

const musicVolume = (f: number, total: number) => {
  let d = 999;
  for (const [s, e] of ducks) {
    if (f >= s && f <= e) {
      d = 0;
      break;
    }
    d = Math.min(d, Math.abs(f - s), Math.abs(f - e));
  }
  // ~-20 dB under speech, eased over 10 frames
  let v = interpolate(d, [0, 10], [0.1 * music.volume, music.volume], {extrapolateRight: 'clamp'});
  v *= interpolate(f, [total - 50, total - 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return v;
};

export const Montage: React.FC = () => {
  const {durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      <Sequence durationInFrames={MAIN}>
        {shots.map((s, i) => (
          <Sequence key={i} from={s.from} durationInFrames={s.dur}>
            <ShotView s={s} />
          </Sequence>
        ))}
        <Grade />
        {(data.overlays as any[]).map((g, i) => (
          <Sequence key={`o${i}`} from={g.from} durationInFrames={g.dur} layout="none">
            <Overlay g={g} />
          </Sequence>
        ))}
        <Flashes />
        <Grain />
        <Fades />
      </Sequence>
      <Sequence from={MAIN} durationInFrames={CLOSING}>
        <Closing />
      </Sequence>
      <Sequence from={MAIN + 2} layout="none">
        <Audio src={staticFile('sfx/impact_logo.mp3')} volume={0.35} />
      </Sequence>
      <Audio
        src={staticFile(music.src)}
        startFrom={Math.round(music.offset * 25)}
        volume={(f) => musicVolume(f, durationInFrames)}
      />
      {(data.vo as {src: string; at: number; in: number; dur: number; volume: number}[]).map((v, i) => (
        <Sequence key={`v${i}`} from={v.at} durationInFrames={v.dur} layout="none">
          <Audio
            src={staticFile(`mz/${v.src}`)}
            startFrom={Math.round(v.in * 25)}
            volume={(f) => v.volume * Math.min(1, f / 3, (v.dur - f) / 8)}
          />
        </Sequence>
      ))}
      {(data.sfx as {name: string; at: number; volume: number}[]).map((s, i) => (
        <Sequence key={`s${i}`} from={s.at} durationInFrames={150} layout="none">
          <Audio src={staticFile(`sfx/${s.name}.mp3`)} volume={s.volume} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
