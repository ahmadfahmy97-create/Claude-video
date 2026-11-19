import React from 'react';
import {Composition} from 'remotion';
import {Edit, ProjectConfig, totalFrames} from './Edit';
import {famaSimpang4} from './projects/fama-simpang4';
import {famaDelegasiIndonesia} from './projects/fama-delegasi-indonesia';

const projects: ProjectConfig[] = [famaDelegasiIndonesia, famaSimpang4];

export const RemotionRoot: React.FC = () => (
  <>
    {projects.map((cfg) => (
      <Composition
        key={cfg.id}
        id={cfg.id}
        component={() => <Edit cfg={cfg} />}
        durationInFrames={totalFrames(cfg)}
        fps={cfg.timeline.fps}
        width={1080}
        height={1920}
      />
    ))}
  </>
);
