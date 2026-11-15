import React from 'react';
import {Composition} from 'remotion';
import {CLOSING_FRAMES, Main} from './Main';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Main"
    component={Main}
    durationInFrames={timeline.durationInFrames + CLOSING_FRAMES}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
);
