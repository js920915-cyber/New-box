from pathlib import Path
import zipfile

root=Path(__file__).resolve().parents[1]
out=root.parent/'video-card-templates-5.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        if p.is_file():
            z.write(p,p.relative_to(root.parent))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    names=z.namelist()
    for d in ('previews','backgrounds','overlays'):
        assert len([n for n in names if f'/{d}/' in n and n.endswith('.png')])==5
print(f'PASS: {out.name}, 5 previews + 5 backgrounds + 5 overlays + editable source.')
