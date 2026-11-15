import React, {useContext} from 'react';
import simpang4 from './data/simpang4/timeline.json';
import libaturus from './data/libaturus/timeline.json';

export type Timeline = {
  fps: number;
  durationInFrames: number;
  captions: any[];
  speech: number[][];
  gfx: any[];
  sfx: {name: string; start: number; volume: number}[];
  zooms: {start: number; scale: number; piece: string; ox?: number; oy?: number}[];
  cuts: number[];
  pieces: {id: string; start: number; end: number}[];
};

export type Project = {
  timeline: Timeline;
  footage: string; // under public/
  music: string; // under public/
  musicUnder?: number; // music gain while someone is talking
  musicOpen?: number; // music gain in gaps
  loudPieces?: string[]; // pieces where the music may rise a bit more (no speech)
  musicFadeFrames?: number; // music fade-out at the very end
};

export const PROJECTS: Record<string, Project> = {
  simpang4: {
    timeline: simpang4 as Timeline,
    footage: 'footage/simpang4/base.mp4',
    music: 'music/m473.mp3',
    loudPieces: ['react'],
  },
  libaturus: {
    timeline: libaturus as Timeline,
    footage: 'footage/libaturus/base.mp4',
    music: 'music/m34.mp3',
    musicUnder: 0.07,
    musicOpen: 0.26,
    loudPieces: ['outro'],
    musicFadeFrames: 40,
  },
};

export const ProjectCtx = React.createContext<Project>(PROJECTS.simpang4);
export const useProject = () => useContext(ProjectCtx);
export const useTimeline = () => useContext(ProjectCtx).timeline;
