import React from 'react';
import {geoCircle, geoGraticule10, geoInterpolate, geoOrthographic, geoPath} from 'd3-geo';
import type {Feature, FeatureCollection, Geometry} from 'geojson';
import land110 from '../data/land-110m.json';
import region50 from '../data/region-50m.json';
import korea10 from '../data/korea-10m.json';
import {bankRoads, hanPolygon, MAGOK, toLocal, toLonLat} from '../lib/seoul';
import {cellBuildings, tilesAround, VARIANTS} from '../lib/city';
import {clamp, smoothstep} from '../lib/util';
import {C, W, H} from '../theme';

const RAD = Math.PI / 180;
const LAND = land110 as unknown as Feature<Geometry>;
const REGION = region50 as unknown as FeatureCollection;
const KOREA = korea10 as unknown as FeatureCollection;
const SOUTH = KOREA.features.filter((f) => String(f.id) === '410');
const HAN = {type: 'Polygon', coordinates: [[...hanPolygon().map(([x, z]) => toLonLat(x, z)), toLonLat(...hanPolygon()[0])]]} as Geometry;
const ROADS = bankRoads(900).map((line) => ({type: 'LineString', coordinates: line.map(([x, z]) => toLonLat(x, z))}) as Geometry);

export const CITIES: Record<string, [number, number]> = {
  seoul: [126.98, 37.57], tokyo: [139.69, 35.69], beijing: [116.4, 39.9], shanghai: [121.47, 31.23],
  hongkong: [114.17, 22.32], singapore: [103.82, 1.35], bangkok: [100.5, 13.75], manila: [120.98, 14.6],
  jakarta: [106.85, -6.2], sydney: [151.2, -33.87], delhi: [77.2, 28.6], taipei: [121.56, 25.03],
  osaka: [135.5, 34.69], vladivostok: [131.9, 43.12], ulaanbaatar: [106.9, 47.9], hanoi: [105.85, 21.03],
  busan: [129.07, 35.18], perth: [115.86, -31.95], guam: [144.79, 13.44], sapporo: [141.35, 43.06],
};

export type Arc = {from: string; to: string; start: number; dur: number};

// Orthographic projection of lon/lat (+ altitude as a fraction of the radius).
const ortho = (lon: number, lat: number, c: [number, number], alt = 0) => {
  const l = lon * RAD;
  const p = lat * RAD;
  const l0 = c[0] * RAD;
  const p0 = c[1] * RAD;
  const x = Math.cos(p) * Math.sin(l - l0);
  const y = Math.cos(p0) * Math.sin(p) - Math.sin(p0) * Math.cos(p) * Math.cos(l - l0);
  const z = Math.sin(p0) * Math.sin(p) + Math.cos(p0) * Math.cos(p) * Math.cos(l - l0);
  const k = 1 + alt;
  const visible = z > 0 || k * Math.hypot(x, y) > 1;
  return {x: x * k, y: y * k, visible};
};

// Point at angular distance `dist` (deg) along compass `bearing` (deg) from lon/lat.
export const destination = (lon: number, lat: number, bearing: number, dist: number): [number, number] => {
  const p1 = lat * RAD;
  const l1 = lon * RAD;
  const b = bearing * RAD;
  const d = dist * RAD;
  const p2 = Math.asin(Math.sin(p1) * Math.cos(d) + Math.cos(p1) * Math.sin(d) * Math.cos(b));
  const l2 = l1 + Math.atan2(Math.sin(b) * Math.sin(d) * Math.cos(p1), Math.cos(d) - Math.sin(p1) * Math.sin(p2));
  return [l2 / RAD, p2 / RAD];
};

export type GlobeProps = {
  scale: number;
  center: [number, number];
  cx?: number;
  cy?: number;
  sunAngle: number; // angular distance of the sun from the view center (180 = directly behind)
  sunBearing?: number;
  night?: number; // strength of night shading
  t: number; // seconds, for arc animation
  arcs?: Arc[];
  arcOpacity?: number;
  koreaGlow?: number;
};

export const Globe: React.FC<GlobeProps> = ({scale, center, cx = W / 2, cy = H / 2, sunAngle, sunBearing = 300, night = 1, t, arcs = [], arcOpacity = 1, koreaGlow = 0}) => {
  const proj = geoOrthographic().scale(scale).translate([cx, cy]).rotate([-center[0], -center[1]]).clipAngle(90).precision(0.3);
  const path = geoPath(proj);
  const sun = destination(center[0], center[1], sunBearing, sunAngle);
  const anti: [number, number] = [sun[0] + 180, -sun[1]];
  const sunScreen = ortho(sun[0], sun[1], center);
  const sunDir = Math.atan2(-sunScreen.y, sunScreen.x);
  const sx = Math.cos(sunDir);
  const sy = Math.sin(sunDir);
  const zoomed = smoothstep(1400, 3500, scale); // regional detail
  const city = smoothstep(26000, 120000, scale); // Seoul detail
  const globeVis = 1 - smoothstep(5000, 14000, scale);
  const pxPerM = scale / 6371000;
  const dotsOpacity = 1 - smoothstep(9000, 40000, scale);

  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
      <defs>
        <pattern id="dots" width={9} height={9} patternUnits="userSpaceOnUse">
          <circle cx={4.5} cy={4.5} r={1.9} fill="#9CC9F5" />
        </pattern>
        <pattern id="dotsKR" width={9} height={9} patternUnits="userSpaceOnUse">
          <circle cx={4.5} cy={4.5} r={2.3} fill={C.blueLit} />
        </pattern>
        <radialGradient id="ocean" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#0B2A52" />
          <stop offset="75%" stopColor="#071A36" />
          <stop offset="100%" stopColor="#03101F" />
        </radialGradient>
        <radialGradient id="atmo" cx="50%" cy="50%" r="50%">
          <stop offset={`${(1 / 1.16) * 100 - 2}%`} stopColor="#3AA0FF" stopOpacity={0} />
          <stop offset={`${(1 / 1.16) * 100}%`} stopColor="#6DB8FF" stopOpacity={0.55} />
          <stop offset={`${(1.04 / 1.16) * 100}%`} stopColor="#2F86E0" stopOpacity={0.22} />
          <stop offset="100%" stopColor="#0A3A75" stopOpacity={0} />
        </radialGradient>
        <linearGradient id="rim" x1={0.5 - sx / 2} y1={0.5 + sy / 2} x2={0.5 + sx / 2} y2={0.5 - sy / 2}>
          <stop offset="0%" stopColor="#1C5FA8" stopOpacity={0.1} />
          <stop offset="70%" stopColor="#7CC2FF" stopOpacity={0.55} />
          <stop offset="100%" stopColor="#E6F4FF" stopOpacity={1} />
        </linearGradient>
        <radialGradient id="flare" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#FFFFFF" stopOpacity={1} />
          <stop offset="12%" stopColor="#EAF6FF" stopOpacity={0.85} />
          <stop offset="40%" stopColor="#7CC2FF" stopOpacity={0.25} />
          <stop offset="100%" stopColor="#3AA0FF" stopOpacity={0} />
        </radialGradient>
        <clipPath id="disc">
          <circle cx={cx} cy={cy} r={scale} />
        </clipPath>
      </defs>

      {globeVis > 0 ? (
        <g opacity={globeVis}>
          <circle cx={cx} cy={cy} r={scale * 1.16} fill="url(#atmo)" />
        </g>
      ) : null}
      {scale < 6000 ? <circle cx={cx} cy={cy} r={scale} fill="url(#ocean)" /> : <rect width={W} height={H} fill="#06182F" />}

      <g clipPath={scale < 6000 ? 'url(#disc)' : undefined}>
        <path d={path(geoGraticule10()) ?? ''} fill="none" stroke="#2A5C94" strokeOpacity={0.35 * globeVis} strokeWidth={1} />
        <g opacity={1 - zoomed}>
          <path d={path(LAND) ?? ''} fill="#123B6B" fillOpacity={0.55} />
          <path d={path(LAND) ?? ''} fill="url(#dots)" fillOpacity={0.9} />
        </g>
        {zoomed > 0 ? (
          <g opacity={zoomed}>
            <path d={path(REGION) ?? ''} fill="#0D2B50" stroke="#2D6AA8" strokeWidth={1.2} />
            <path d={path(KOREA) ?? ''} fill="#0F3260" stroke="#4F98DE" strokeWidth={1.4} />
            <path d={path(REGION) ?? ''} fill="url(#dots)" fillOpacity={0.5 * dotsOpacity} />
            <path d={path(KOREA) ?? ''} fill="url(#dots)" fillOpacity={0.7 * dotsOpacity} />
          </g>
        ) : null}
        {koreaGlow > 0 ? (
          <g opacity={koreaGlow * dotsOpacity}>
            <path d={path({type: 'FeatureCollection', features: SOUTH} as FeatureCollection) ?? ''} fill="url(#dotsKR)" stroke={C.blueLit} strokeWidth={2.2} />
          </g>
        ) : null}
        {city > 0 ? <CityFabric proj={proj} pxPerM={pxPerM} center={center} land={path(KOREA) ?? ''} /> : null}
        {city > 0 ? (
          <g opacity={city}>
            <path d={path(HAN) ?? ''} fill="#0E5CB0" fillOpacity={0.85} stroke="#58AFFF" strokeWidth={1.5} />
            {ROADS.map((r, i) => (
              <path key={i} d={path(r) ?? ''} fill="none" stroke="#9CCBFF" strokeOpacity={0.55} strokeWidth={Math.max(1, 60 * pxPerM)} />
            ))}
          </g>
        ) : null}
        {night > 0 ? (
          <g opacity={night}>
            {[96, 92, 88, 84].map((r, i) => (
              <path key={r} d={path(geoCircle().center(anti).radius(r)()) ?? ''} fill="#010409" fillOpacity={[0.2, 0.22, 0.25, 0.28][i]} />
            ))}
          </g>
        ) : null}
      </g>

      {globeVis > 0 ? (
        <circle cx={cx} cy={cy} r={scale} fill="none" stroke="url(#rim)" strokeWidth={Math.max(2, scale * 0.012)} opacity={globeVis} />
      ) : null}

      {arcs.length > 0 && arcOpacity > 0 ? (
        <g opacity={arcOpacity}>
          {arcs.map((a, i) => {
            const p = (t - a.start) / a.dur;
            if (p <= 0 || p >= 1.6) return null;
            const interp = geoInterpolate(CITIES[a.from], CITIES[a.to]);
            const head = clamp(p);
            const tail = clamp(p - 0.45);
            const fade = 1 - clamp((p - 1) / 0.6);
            const pts: string[] = [];
            const n = 28;
            for (let k = 0; k <= n; k++) {
              const s = tail + ((head - tail) * k) / n;
              const [lo, la] = interp(s);
              const o = ortho(lo, la, center, Math.sin(Math.PI * s) * 0.06);
              if (!o.visible) continue;
              pts.push(`${(cx + o.x * scale).toFixed(1)},${(cy - o.y * scale).toFixed(1)}`);
            }
            const [hl, ha] = interp(head);
            const ho = ortho(hl, ha, center, Math.sin(Math.PI * head) * 0.06);
            const col = i % 5 === 2 ? C.redLit : i % 2 ? '#BFE0FF' : C.blueLit;
            return (
              <g key={i} opacity={fade}>
                {pts.length > 1 ? <polyline points={pts.join(' ')} fill="none" stroke={col} strokeWidth={2.2} strokeLinecap="round" strokeOpacity={0.85} /> : null}
                {ho.visible && p < 1 ? <circle cx={cx + ho.x * scale} cy={cy - ho.y * scale} r={3.6} fill="#FFFFFF" /> : null}
              </g>
            );
          })}
        </g>
      ) : null}

      {globeVis > 0 && sunAngle > 80 ? (
        <circle
          cx={cx + Math.cos(sunDir) * scale * 1.005}
          cy={cy - Math.sin(sunDir) * scale * 1.005}
          r={scale * 0.55}
          fill="url(#flare)"
          opacity={globeVis * clamp((sunAngle - 80) / 40) * clamp((150 - Math.abs(sunAngle - 100)) / 50)}
        />
      ) : null}
    </svg>
  );
};

// District tiles filled with block patterns; pattern space is anchored at Magok so it lines up with scene 3.
const CityFabric: React.FC<{proj: ReturnType<typeof geoOrthographic>; pxPerM: number; center: [number, number]; land: string}> = ({proj, pxPerM, center, land}) => {
  const o = proj([MAGOK.lon, MAGOK.lat]) ?? [W / 2, H / 2];
  const [lx, lz] = toLocal(center[0], center[1]);
  const radius = Math.hypot(W, H) / 2 / pxPerM + 2000;
  const tiles = tilesAround(lx, lz, radius);
  const S = (x: number, z: number) => `${(o[0] + x * pxPerM).toFixed(1)} ${(o[1] - z * pxPerM).toFixed(1)}`;
  return (
    <g opacity={smoothstep(30000, 140000, pxPerM * 6371000)}>
      <defs>
        {VARIANTS.map((v, i) => {
          const r = (v.rot * Math.PI) / 180;
          const s = pxPerM;
          return (
            <pattern
              key={i}
              id={`blk${i}`}
              patternUnits="userSpaceOnUse"
              width={2 * v.pitch}
              height={2 * v.pitch}
              patternTransform={`matrix(${s * Math.cos(r)} ${-s * Math.sin(r)} ${-s * Math.sin(r)} ${-s * Math.cos(r)} ${o[0]} ${o[1]})`}
            >
              {cellBuildings(v.pitch).map((b, k) => (
                <rect key={k} x={b.u0} y={b.v0} width={b.u1 - b.u0} height={b.v1 - b.v0} fill={BLOCK_FILL} stroke={BLOCK_EDGE} strokeWidth={3} />
              ))}
            </pattern>
          );
        })}
        <clipPath id="landclip">
          <path d={land} />
        </clipPath>
      </defs>
      <g clipPath="url(#landclip)">
        {tiles.map((t, i) => {
          const d = 'M' + t.poly.map(([x, z]) => S(x, z)).join(' L') + ' Z';
          return (
            <g key={i}>
              <path d={d} fill={TILE_FILL} />
              <path d={d} fill={`url(#blk${t.v})`} />
            </g>
          );
        })}
      </g>
    </g>
  );
};

export const BLOCK_FILL = '#1A3F6E';
export const BLOCK_EDGE = '#3166A0';
export const TILE_FILL = '#0C2547';

export const projectLonLat = (lon: number, lat: number, scale: number, center: [number, number], cx = W / 2, cy = H / 2) => {
  const o = ortho(lon, lat, center);
  return {x: cx + o.x * scale, y: cy - o.y * scale, visible: o.visible};
};

export {MAGOK};
