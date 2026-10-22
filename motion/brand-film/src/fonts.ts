import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
import {FONT} from './theme';

// RCardnews = the center's card-news typeface (SIL OFL 1.1, templates/fonts).
const weights = ['500', '700', '800', '850'] as const;

export const fontsReady = Promise.all(
  weights.map((weight) =>
    loadFont({family: FONT, url: staticFile(`fonts/RCardnews-W${weight}.ttf`), weight}),
  ),
);
