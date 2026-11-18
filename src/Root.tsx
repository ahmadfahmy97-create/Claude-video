import React from 'react';
import {Composition} from 'remotion';
import {CLOSING_FRAMES, Main} from './Main';
import timeline from './timeline.json';
import {CLOSING, MAIN, Montage} from './montage/Montage';

export const RemotionRoot: React.FC = () => (
  <>
    {/* 16:9 waiting-room montage: Mengenali Pengerusi FAMA */}
    <Composition id="Montage" component={Montage} durationInFrames={MAIN + CLOSING} fps={25} width={1920} height={1080} />
    <Composition
      id="Main"
      component={Main}
      durationInFrames={timeline.durationInFrames + CLOSING_FRAMES}
      fps={timeline.fps}
      width={1080}
      height={1920}
    />
  </>
);
