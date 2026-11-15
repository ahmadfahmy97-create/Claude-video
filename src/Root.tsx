import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import {PROJECTS} from './projects';

export const RemotionRoot: React.FC = () => (
  <>
    {Object.entries(PROJECTS).map(([id, p]) => (
      <Composition
        key={id}
        id={id}
        component={Main}
        defaultProps={{project: id}}
        durationInFrames={p.timeline.durationInFrames}
        fps={p.timeline.fps}
        width={1080}
        height={1920}
      />
    ))}
  </>
);
