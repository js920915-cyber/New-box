"""Create a portable project handoff without local runtimes or nested ZIPs."""
from pathlib import Path
import os, json, hashlib, zipfile, struct

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'cloud-delivery'
SKIP_DIRS = {'.git', 'node_modules', 'python-libs', '__pycache__', '.venv', 'venv', 'cloud-delivery'}

def files():
    for folder, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            p = Path(folder) / name
            if p.suffix.lower() not in {'.zip', '.pyc'}:
                yield p

def main():
    OUT.mkdir(exist_ok=True)
    items = list(files())
    records = []
    for p in items:
        data = p.read_bytes()
        records.append({'path': p.relative_to(ROOT).as_posix(), 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
    checks = {}
    for topic in ['acl-return-to-running-latest', 'achilles-elongation-anatomy']:
        result = []
        for n in range(1, 7):
            p = ROOT / 'content' / topic / 'exports' / f'{n:02}.png'
            data = p.read_bytes()
            assert data[:8] == b'\x89PNG\r\n\x1a\n', p
            size = struct.unpack('>II', data[16:24])
            assert size == (1080, 1350), (p, size)
            result.append({'card': p.name, 'width': size[0], 'height': size[1]})
        checks[topic] = result
    archive = OUT / 'R-Sports-Cloud-Handoff-2026-10-13.zip'
    manifest = {'date': '2026-10-13', 'file_count': len(records), 'files': records,
                'excluded': sorted(SKIP_DIRS) + ['*.zip', '*.pyc'], 'png_checks': checks}
    encoded = json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in items:
            z.write(p, 'R-Sports-Cardnews/' + p.relative_to(ROOT).as_posix())
        z.writestr('R-Sports-Cardnews/CLOUD_PACKAGE_MANIFEST.json', encoded)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for r in records:
            data = z.read('R-Sports-Cardnews/' + r['path'])
            assert hashlib.sha256(data).hexdigest() == r['sha256'], r['path']
    (OUT / 'CLOUD_PACKAGE_MANIFEST.json').write_bytes(encoded)
    summary = {'archive': archive.name, 'bytes': archive.stat().st_size,
               'file_count': len(records), 'zip_crc': 'PASS', 'all_sha256': 'PASS',
               'latest_png_dimensions': 'PASS (12 cards)',
               'scope': 'Packaging and file validation only; no new clinical, visual or Express import review.'}
    (OUT / 'PACKAGE_QA.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    main()
