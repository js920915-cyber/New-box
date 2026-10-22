// Extracts the small GeoJSON subsets the film needs from world-atlas (Natural Earth, public domain).
import {readFileSync, writeFileSync} from 'node:fs';
import {feature} from 'topojson-client';

const load = (f) => JSON.parse(readFileSync(new URL(`../node_modules/world-atlas/${f}`, import.meta.url)));
const round = (g) => JSON.parse(JSON.stringify(g, (k, v) => (typeof v === 'number' ? Math.round(v * 1e4) / 1e4 : v)));

const land110 = load('land-110m.json');
writeFileSync('src/data/land-110m.json', JSON.stringify(round(feature(land110, land110.objects.land))));

const c50 = load('countries-50m.json');
const near = feature(c50, c50.objects.countries).features.filter((f) => ['156', '392', '643', '496'].includes(f.id));
writeFileSync('src/data/region-50m.json', JSON.stringify(round({type: 'FeatureCollection', features: near})));

const c10 = load('countries-10m.json');
const korea = feature(c10, c10.objects.countries).features.filter((f) => ['410', '408'].includes(f.id));
writeFileSync('src/data/korea-10m.json', JSON.stringify(round({type: 'FeatureCollection', features: korea})));
console.log(near.map((f) => f.properties.name), korea.map((f) => f.properties.name));
