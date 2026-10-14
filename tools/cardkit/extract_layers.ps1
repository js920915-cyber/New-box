# 카드 HTML을 ?layers 모드로 열어 줄 단위 텍스트·도형 좌표를 <topic>/adobe-express/build/layers.json에 저장한다.
# 사진(.cover-photo 등 overflow:hidden 크롭)은 보이는 영역 그대로 Chrome으로 원본 해상도 캡처한다.
# 사용: powershell -ExecutionPolicy Bypass -File tools/cardkit/extract_layers.ps1 -Topic content/<slug>
param([Parameter(Mandatory)][string]$Topic)
$ErrorActionPreference = 'Continue'
$root = (Resolve-Path $Topic).Path
$src = Join-Path $root 'source'
$build = Join-Path $root 'adobe-express/build'
New-Item -ItemType Directory -Force $build | Out-Null
$chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
$cards = @()
foreach ($html in Get-ChildItem $src -Filter '*.html' | Where-Object Name -match '^\d\d\.html$' | Sort-Object Name) {
  $n = $html.BaseName
  $url = ([Uri]$html.FullName).AbsoluteUri
  $dom = & $chrome --headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=4000 --window-size=1080,1350 --dump-dom "$url`?layers" 2>$null | Out-String
  $m = [regex]::Match($dom, '<pre id="layers-out">(.*?)</pre>', 'Singleline')
  if (-not $m.Success) { throw "layers not found: $n (build.py가 tools/cardkit/layers.js를 포함했는지 확인)" }
  $data = [System.Net.WebUtility]::HtmlDecode($m.Groups[1].Value) | ConvertFrom-Json
  $i = 0
  foreach ($s in $data.shapes | Where-Object type -eq 'photo') {
    $i++
    $k = [math]::Max(1, $s.img.naturalW / $s.img.w)
    $page = Join-Path $src "_crop-$n-$i.html"
    $html = "<!doctype html><html><body style='margin:0;overflow:hidden'><div style='position:relative;width:$($s.w)px;height:$($s.h)px;overflow:hidden'>" +
      "<img src='$($s.src)' style='position:absolute;width:$($s.img.w)px;left:$($s.img.x - $s.x)px;top:$($s.img.y - $s.y)px'></div></body></html>"
    [IO.File]::WriteAllText($page, $html, (New-Object Text.UTF8Encoding $false))
    $out = Join-Path $build "$n-photo$i.png"
    & $chrome --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files --virtual-time-budget=3000 "--force-device-scale-factor=$k" "--window-size=$([int]$s.w),$([int]$s.h)" "--screenshot=$out" ([Uri]$page).AbsoluteUri 2>$null | Out-Null
    Remove-Item -LiteralPath $page
    $s | Add-Member -NotePropertyName file -NotePropertyValue "$n-photo$i.png" -Force
  }
  $cards += [pscustomobject]@{card = $n; lines = $data.lines; shapes = $data.shapes}
  "$n : $(@($data.lines).Count) lines, $(@($data.shapes).Count) shapes"
}
[IO.File]::WriteAllText((Join-Path $build 'layers.json'), ($cards | ConvertTo-Json -Depth 8), (New-Object Text.UTF8Encoding $false))
