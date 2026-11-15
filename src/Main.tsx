import React from 'react';
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {PROJECTS, ProjectCtx, Timeline, useProject, useTimeline} from './projects';
import {Captions} from './Captions';
import {Graphic} from './Graphics';

const useZoom = () => {
  const {zooms} = useTimeline();
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
  const {pieces} = useTimeline();
  const {footage} = useProject();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {scale, ox, oy} = useZoom();
  // little "push" at every new section
  let bump = 1;
  for (const p of pieces) {
    const f0 = Math.round(p.start * fps);
    if (f0 > 0 && frame >= f0 && frame < f0 + 10) bump = interpolate(frame - f0, [0, 9], [1.07, 1], {extrapolateRight: 'clamp'});
  }
  return (
    <AbsoluteFill style={{transform: `scale(${scale * bump})`, transformOrigin: `${ox * 100}% ${oy * 100}%`}}>
      <OffthreadVideo src={staticFile(footage)} />
    </AbsoluteFill>
  );
};

const SectionFlash: React.FC = () => {
  const {pieces} = useTimeline();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  let o = 0;
  for (const p of pieces) {
    const f0 = Math.round(p.start * fps);
    if (f0 > 0 && frame >= f0 && frame < f0 + 6) o = interpolate(frame - f0, [0, 5], [0.45, 0]);
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

const musicVolume = (frame: number, fps: number, total: number, tl: Timeline, cfg: {loud: string[]; under: number; open: number; fade: number}) => {
  const t = frame / fps;
  let d = 99;
  for (const [s, e] of tl.speech) {
    if (t >= s && t <= e) {
      d = 0;
      break;
    }
    d = Math.min(d, Math.abs(t - s), Math.abs(t - e));
  }
  const piece = tl.pieces.find((p) => t >= p.start && t < p.end)?.id;
  const open = piece && cfg.loud.includes(piece) ? cfg.open * 1.4 : cfg.open;
  const under = cfg.under; // music sits ~-22 dB under the voice
  let v = interpolate(d, [0, 0.35], [under, open], {extrapolateRight: 'clamp'});
  v *= interpolate(frame, [0, 12], [0.6, 1], {extrapolateRight: 'clamp'});
  v *= interpolate(frame, [total - cfg.fade, total - 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return v;
};

export const Main: React.FC<{project: string}> = ({project}) => {
  const p = PROJECTS[project];
  return (
    <ProjectCtx.Provider value={p}>
      <Edit />
    </ProjectCtx.Provider>
  );
};

const Edit: React.FC = () => {
  const {fps, durationInFrames} = useVideoConfig();
  const p = useProject();
  const timeline = p.timeline;
  const cfg = {loud: p.loudPieces ?? [], under: p.musicUnder ?? 0.075, open: p.musicOpen ?? 0.24, fade: p.musicFadeFrames ?? 75};
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      <Footage />
      <Grade />
      {timeline.gfx.map((g, i) => (
        <Sequence key={i} from={Math.round(g.start * fps)} durationInFrames={Math.round(g.dur * fps)} layout="none">
          <Graphic g={g} />
        </Sequence>
      ))}
      <Captions />
      <SectionFlash />

      <Audio src={staticFile(p.music)} loop volume={(f) => musicVolume(f, fps, durationInFrames, timeline, cfg)} />
      {timeline.sfx.map((s, i) => (
        <Sequence key={`s${i}`} from={Math.round(s.start * fps)} durationInFrames={fps * 6} layout="none">
          <Audio src={staticFile(`sfx/${s.name}.mp3`)} volume={s.volume} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
