// Copies the card-news typeface (templates/fonts, SIL OFL 1.1) into public/ so the film uses the same type.
import {copyFileSync, mkdirSync} from 'node:fs';

mkdirSync('public/fonts', {recursive: true});
for (const w of ['500', '700', '800', '850']) {
  copyFileSync(new URL(`../../../templates/fonts/RCardnews-W${w}.ttf`, import.meta.url), `public/fonts/RCardnews-W${w}.ttf`);
}
copyFileSync(new URL('../../../templates/fonts/OFL.txt', import.meta.url), 'public/fonts/OFL.txt');
