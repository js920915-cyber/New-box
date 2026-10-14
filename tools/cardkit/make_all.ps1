# 한 주제의 전체 출고: HTML 생성 → PNG 렌더/QA → 줄 좌표 추출 → Express용 PPTX → PowerPoint 검증 → delivery/ 3종
# 사용: powershell -ExecutionPolicy Bypass -File tools/cardkit/make_all.ps1 -Topic content/<slug>
param([Parameter(Mandatory)][string]$Topic)
$ErrorActionPreference = 'Stop'
$kit = $PSScriptRoot
$root = (Resolve-Path $Topic).Path
python (Join-Path $root 'source/build.py'); if ($LASTEXITCODE) { throw 'build.py 실패' }
& powershell -ExecutionPolicy Bypass -File (Join-Path $kit 'render.ps1') -Topic $root
& powershell -ExecutionPolicy Bypass -File (Join-Path $kit 'extract_layers.ps1') -Topic $root
python (Join-Path $kit 'build_pptx.py') $root; if ($LASTEXITCODE) { throw 'build_pptx.py 실패' }
& powershell -ExecutionPolicy Bypass -File (Join-Path $kit 'verify_pptx.ps1') -Topic $root
& powershell -ExecutionPolicy Bypass -File (Join-Path $kit 'deliver.ps1') -Topic $root
