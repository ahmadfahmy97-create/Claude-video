import {continueRender, delayRender, staticFile} from 'remotion';

// Fonts are bundled locally (public/fonts) so rendering never depends on the network.
export const MONT = 'MontserratLocal';
export const ANTON = 'AntonLocal';

const fonts: [string, string, string][] = [
  [MONT, 'fonts/Montserrat-var.woff2', '100 900'],
  [ANTON, 'fonts/Anton-400.woff2', '400'],
];
if (typeof document !== 'undefined') {
  const handle = delayRender('Loading local fonts');
  Promise.all(
    fonts.map(([family, file, weight]) => {
      const face = new FontFace(family, `url(${staticFile(file)}) format('woff2')`, {weight});
      document.fonts.add(face);
      return face.load();
    }),
  )
    .then(() => continueRender(handle))
    .catch((e) => {
      console.error(e);
      continueRender(handle);
    });
}

export const C = {
  yellow: '#FFD60A',
  green: '#16A34A',
  deep: '#064E3B',
  white: '#FFFFFF',
  black: '#0B0B0B',
  red: '#EF4444',
  orange: '#FF6B1A',
};

// TikTok + Instagram Reels safe area on a 1080x1920 canvas.
// Top ~230px (status / tabs), bottom ~440px (caption, username, music), right ~140px (action buttons).
export const SAFE = {left: 60, right: 940, top: 230, bottom: 1480};
export const CX = (SAFE.left + SAFE.right) / 2; // 500 – horizontal centre of the safe area
export const SAFE_W = SAFE.right - SAFE.left;

export const stroke = (px: number, color = '#000') => ({
  WebkitTextStroke: `${px}px ${color}`,
  paintOrder: 'stroke fill' as const,
});
