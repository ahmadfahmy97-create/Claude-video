import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import timeline from './timeline.json';
import {TOTAL_FRAMES} from './Closing';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Main"
    component={Main}
    durationInFrames={TOTAL_FRAMES}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
);
