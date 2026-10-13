"""Package canonical V4 guidance and portable project assets; retain legacy history."""
from pathlib import Path
import hashlib, json, os, re, struct, zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'final-delivery'
DATE = '2026-10-13'
DOCS = ['AGENTS.md', 'DESIGN_SYSTEM.md', 'CARDNEWS_WORKFLOW.md',
        'CARDNEWS_PROMPT.md', 'PROJECT_HANDOFF.md', 'CLOUD_START.md',
        'README.md', 'FINAL_CHANGELOG.md', 'FINAL_QA.md']
SKIP_DIRS = {'.git', 'node_modules', 'python-libs', '__pycache__', '.venv',
             'venv', 'cloud-delivery', 'final-delivery'}

def validate():
    issues = []
    for name in DOCS[:-1]:
        p = ROOT / name
        text = p.read_text(encoding='utf-8')
        if re.search('[\u3040-\u30ff]', text): issues.append(name + ': unexpected Japanese text')
        if text.count('```') % 2: issues.append(name + ': unmatched code fence')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if not re.match(r'https?://',target) and not (p.parent / target.split('#')[0]).exists():
                issues.append(name + ': missing link ' + target)
    for name in ['AGENTS.md','DESIGN_SYSTEM.md','CARDNEWS_WORKFLOW.md','CARDNEWS_PROMPT.md']:
        text=(ROOT/name).read_text(encoding='utf-8')
        assert 'V4' in text and '200px' in text, name
    tokens=json.loads((ROOT/'templates/design_tokens.json').read_text(encoding='utf-8'))
    assert tokens['type_px']['cover']==88 and tokens['type_px']['body']==44
    counts={}
    for folder,expected in [('original',10),('user_selected',6),('avoid',1),('approved_acl_v3',8)]:
        paths=[p for p in (ROOT/'references'/folder).iterdir() if p.suffix.lower() in {'.png','.jpg','.jpeg'}]
        counts[folder]=len(paths)
        assert len(paths)==expected,(folder,len(paths))
    pngs=[]
    for topic in ['acl-return-to-running-latest','achilles-elongation-anatomy']:
        for n in range(1,7):
            p=ROOT/'content'/topic/'exports'/f'{n:02}.png'
            raw=p.read_bytes()
            assert raw[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',raw[16:24])==(1080,1350),p
            pngs.append(p.relative_to(ROOT).as_posix())
    assert not issues,issues
    return counts,pngs

def inventory():
    for folder,dirs,names in os.walk(ROOT):
        dirs[:]=sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            p=Path(folder)/name
            if p.suffix.lower() not in {'.zip','.pyc'}: yield p

def archive(label,paths):
    dest=OUT/f'R-Sports-V4-{label}-{DATE}.zip'
    records=[]
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in paths:
            raw=p.read_bytes();relative=p.relative_to(ROOT).as_posix()
            records.append({'path':relative,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
            z.writestr('R-Sports-Cardnews/'+relative,raw)
        manifest={'version':'4.0','date':DATE,'kind':label,'file_count':len(records),'files':records,
                  'excluded':sorted(SKIP_DIRS)+['*.zip','*.pyc'],
                  'note':'Markdown bundle omits images/sources. Portable bundle includes them. Historical content snapshots are not active V4 guidance.'}
        z.writestr('R-Sports-Cardnews/PACKAGE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for record in records:
            assert hashlib.sha256(z.read('R-Sports-Cardnews/'+record['path'])).hexdigest()==record['sha256']
    return {'file':dest.name,'bytes':dest.stat().st_size,'files':len(records),'crc':'PASS','sha256':'PASS'}

def main():
    OUT.mkdir(exist_ok=True)
    counts,pngs=validate()
    (ROOT/'FINAL_QA.md').write_text('''# V4 문서·패키지 확인 — 2026-10-13

- 루트 지침/독립 프롬프트/인계 문서의 V4 기준과 역할 구분 확인.
- 표지88/내부84/본문44/보조36px와 디자인 토큰의 시작값 확인.
- 실제 콘텐츠 하단 y1140~1240 목표, 200px 초과 공백 검토·출고 기준 반영.
- 활성 루트 문서의 상대 링크 대상 존재·코드 블록 닫힘·문자 인코딩 확인.
- 원본10/선택6/실패1/ACL8 이미지 파일 존재 확인. 이번 문서 작업에서 새 시각 검수는 수행하지 않음.
- 기존 ACL/아킬레스 카드12개의 1080×1350 해상도 확인. 확대/V4 재제작 완료를 뜻하지 않음.
- 기존 큰 글씨 초안은 미완료 상태 유지. 이전 제작 스냅샷·코드는 당시 수치이며 신규 실행 전 V4 반영 필요.
- 이전 지침 갱신기의 수치 복원 중단. 백업은 final-delivery/history-before-v4에 보존.
- 압축 CRC 및 모든 포함 파일 SHA-256 일치 확인. 자세한 결과는 final-delivery/PACKAGE_QA.json.
- 이번 완료 범위는 지침 통합·파일 확인·패키징. 임상 재검수·새 이미지 렌더·클라우드 실행·Express 가져오기·실제 영상 검수는 수행하지 않음.
''',encoding='utf-8')
    small=[ROOT/name for name in DOCS]+[ROOT/'templates/design_tokens.json']
    results=[archive('Markdown',small),archive('Portable',list(inventory()))]
    summary={'version':'4.0','date':DATE,'archives':results,'references':counts,'existing_png_dimensions_checked':len(pngs),
             'scope':'Documentation and packaging only; no new visual, clinical, cloud runtime or Express validation.'}
    (OUT/'PACKAGE_QA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
