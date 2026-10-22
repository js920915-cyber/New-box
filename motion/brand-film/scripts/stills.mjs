// Usage: node scripts/stills.mjs <outDir> <compId>:<frame,frame,...> [<compId>:<frames> ...]
// Bundles once and renders the requested frames as PNGs for visual QA.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {existsSync, mkdirSync} from 'node:fs';
import path from 'node:path';

const [outDir, ...jobs] = process.argv.slice(2);
mkdirSync(outDir, {recursive: true});
const shell = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const browserExecutable = existsSync(shell) ? shell : undefined;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), enableCaching: true});
for (const job of jobs) {
  const [id, frames] = job.split(':');
  const composition = await selectComposition({serveUrl, id, browserExecutable});
  for (const f of frames.split(',').map(Number)) {
    const output = path.join(outDir, `${id}-${String(f).padStart(4, '0')}.png`);
    await renderStill({serveUrl, composition, frame: f, output, browserExecutable, scale: 0.5});
    console.log(output);
  }
}
