import type {ProjectConfig} from '../../Edit';
import timeline from './timeline.json';

export const famaSimpang4: ProjectConfig = {
  id: 'FamaSimpang4',
  timeline: timeline as any,
  footage: 'footage/fama-simpang4/base.mp4',
  music: 'music/m473.mp3',
  musicLoudPieces: ['react'],
  keyWords: /^(RM\d+|\d+%?|SARA|FAMA|Super|El|Nino\.?|Combo|Madani|Happy|Hour|30%|50%|3)[.,!?]?$/i,
};
