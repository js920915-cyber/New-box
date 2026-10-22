// Stylized Seoul geography shared by the map zoom (scene 2) and the 3D city (scene 3).
// The Han River course is a hand-simplified centerline (approximate, for motion graphics only).

export const MAGOK = {lon: 126.826, lat: 37.561};
const R = 6371000;
const k = Math.cos((MAGOK.lat * Math.PI) / 180);

export const toLocal = (lon: number, lat: number): [number, number] => [
  ((lon - MAGOK.lon) * Math.PI * R * k) / 180,
  ((lat - MAGOK.lat) * Math.PI * R) / 180,
];
export const toLonLat = (x: number, z: number): [number, number] => [
  MAGOK.lon + (x * 180) / (Math.PI * R * k),
  MAGOK.lat + (z * 180) / (Math.PI * R),
];

// East → west
const HAN: [number, number][] = [
  [127.2, 37.548], [127.16, 37.556], [127.125, 37.553], [127.1, 37.531], [127.075, 37.52],
  [127.045, 37.527], [127.02, 37.532], [126.998, 37.524], [126.98, 37.514], [126.955, 37.517],
  [126.93, 37.533], [126.905, 37.542], [126.885, 37.553], [126.86, 37.567], [126.835, 37.58],
  [126.81, 37.593], [126.78, 37.608], [126.745, 37.63], [126.7, 37.66], [126.66, 37.69],
];

export const hanCenter = HAN.map(([lon, lat]) => toLocal(lon, lat));

// River as a polygon in local meters (centerline offset by half width each side).
export const hanPolygon = (width = 950): [number, number][] => {
  const L: [number, number][] = [];
  const Rr: [number, number][] = [];
  for (let i = 0; i < hanCenter.length; i++) {
    const a = hanCenter[Math.max(0, i - 1)];
    const b = hanCenter[Math.min(hanCenter.length - 1, i + 1)];
    const dx = b[0] - a[0];
    const dz = b[1] - a[1];
    const l = Math.hypot(dx, dz) || 1;
    const nx = -dz / l;
    const nz = dx / l;
    const w = width * (i > 15 ? 1.5 : 1) * 0.5;
    L.push([hanCenter[i][0] + nx * w, hanCenter[i][1] + nz * w]);
    Rr.push([hanCenter[i][0] - nx * w, hanCenter[i][1] - nz * w]);
  }
  return [...L, ...Rr.reverse()];
};

// Riverside expressways (offset lines on both banks).
export const bankRoads = (offset: number): [number, number][][] => {
  const side = (sgn: number) =>
    hanCenter.map((p, i) => {
      const a = hanCenter[Math.max(0, i - 1)];
      const b = hanCenter[Math.min(hanCenter.length - 1, i + 1)];
      const dx = b[0] - a[0];
      const dz = b[1] - a[1];
      const l = Math.hypot(dx, dz) || 1;
      return [p[0] + (-dz / l) * offset * sgn, p[1] + (dx / l) * offset * sgn] as [number, number];
    });
  return [side(1), side(-1)];
};

// Distance from a point to the river centerline (meters).
export const riverDistance = (x: number, z: number) => {
  let best = Infinity;
  for (let i = 0; i < hanCenter.length - 1; i++) {
    const [ax, az] = hanCenter[i];
    const [bx, bz] = hanCenter[i + 1];
    const dx = bx - ax;
    const dz = bz - az;
    const t = Math.max(0, Math.min(1, ((x - ax) * dx + (z - az) * dz) / (dx * dx + dz * dz)));
    best = Math.min(best, Math.hypot(x - (ax + dx * t), z - (az + dz * t)));
  }
  return best;
};
