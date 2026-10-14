# 사용자에게 줄 납품물 3종만 <topic>/delivery/에 모은다: 01~NN.png, <slug>.pptx(Express 편집용), caption.md
# 사용: powershell -ExecutionPolicy Bypass -File tools/cardkit/deliver.ps1 -Topic content/<slug>
param([Parameter(Mandatory)][string]$Topic)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $Topic).Path
$slug = Split-Path $root -Leaf
$check = Get-Content (Join-Path $root 'qa/pptx-check.json') -Raw -Encoding utf8 | ConvertFrom-Json
if ($check.result -ne 'PASS') { throw 'verify_pptx.ps1 결과가 PASS가 아니므로 납품하지 않습니다.' }
$out = Join-Path $root 'delivery'
if (Test-Path $out) { Get-ChildItem $out -File | Remove-Item }
New-Item -ItemType Directory -Force $out | Out-Null
Get-ChildItem (Join-Path $root 'exports') -Filter '*.png' | Where-Object Name -match '^\d\d\.png$' | Copy-Item -Destination $out
Copy-Item (Join-Path $root "adobe-express/$slug-express.pptx") (Join-Path $out "$slug.pptx")
Copy-Item (Join-Path $root 'caption.md') $out
Get-ChildItem $out | Select-Object Name, @{n = 'KB'; e = { [math]::Round($_.Length / 1KB) } } | Format-Table -AutoSize | Out-String
