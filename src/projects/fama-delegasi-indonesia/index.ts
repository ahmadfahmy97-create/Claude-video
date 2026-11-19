import type {ProjectConfig} from '../../Edit';
import timeline from './timeline.json';

export const famaDelegasiIndonesia: ProjectConfig = {
  id: 'FamaDelegasiIndonesia',
  timeline: timeline as any,
  footage: 'footage/fama-delegasi-indonesia/base.mp4',
  music: 'music/m440.mp3',
  musicLoudPieces: ['selfie'],
  keyWords: /^(FAMA|BAPANAS|BULOG|3|1|34|8-9|cili|cabai|geran|oleh-oleh|buah|tangan|Sarawak|Borneo|dua|2|pemasaran|abang|serumpun|Timbalan|wakil|kepala)[.,!?]?$/i,
};
