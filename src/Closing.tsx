import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import timeline from './timeline.json';

// Branded closing (16:9 logo animation on black, 5 s, no audio) appended after the edit.
export const CLOSING_FRAMES = 150;
export const CLOSING_OVERLAP = 8; // cross-fade from the end card into the black closing
export const MAIN_FRAMES = timeline.durationInFrames;
export const TOTAL_FRAMES = MAIN_FRAMES + CLOSING_FRAMES - CLOSING_OVERLAP;

// logo occupies x 184-1740 / y 297-860 of the 1920x1080 source (centre 962, 578): scale to 56% and centre
// it on the TikTok/IG safe area (x 60-940), so it sits ~871 px wide clear of the right-hand buttons.
const S = 0.56;
const LOGO_CX = 962;
const LOGO_CY = 578;
const SAFE_CX = 500;
const SAFE_CY = 900;
const VW = 1920 * S;
const VH = 1080 * S;

export const Closing: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, CLOSING_OVERLAP], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: 'black', opacity: o}}>
      <OffthreadVideo
        src={staticFile('closing/closing_abang_kerdee.mp4')}
        muted
        style={{position: 'absolute', width: VW, height: VH, left: SAFE_CX - LOGO_CX * S, top: SAFE_CY - LOGO_CY * S}}
      />
      <Sequence from={CLOSING_OVERLAP} layout="none">
        <Audio src={staticFile('sfx/whoosh_air.mp3')} volume={0.2} />
      </Sequence>
      <Sequence from={CLOSING_OVERLAP + 40} layout="none">
        <Audio src={staticFile('sfx/impact_logo.mp3')} volume={0.28} />
      </Sequence>
    </AbsoluteFill>
  );
};
