# 카드 HTML(source/01.html ...)을 Chrome headless로 1080x1350 PNG 렌더 + ?qa 측정 + 360x450 축소본.
# 사용: powershell -ExecutionPolicy Bypass -File tools/cardkit/render.ps1 -Topic content/<slug>
param([Parameter(Mandatory)][string]$Topic)
$ErrorActionPreference = 'Continue'  # Chrome은 무해한 로그를 stderr로 출력한다
$root = (Resolve-Path $Topic).Path
$chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
Add-Type -AssemblyName System.Drawing
foreach ($d in 'exports', 'qa') { New-Item -ItemType Directory -Force (Join-Path $root $d) | Out-Null }
$results = @()
foreach ($html in Get-ChildItem (Join-Path $root 'source') -Filter '*.html' | Where-Object Name -match '^\d\d\.html$' | Sort-Object Name) {
  $n = $html.BaseName
  $url = ([Uri]$html.FullName).AbsoluteUri
  $png = Join-Path $root "exports/$n.png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --allow-file-access-from-files --virtual-time-budget=4000 --window-size=1080,1350 "--screenshot=$png" $url 2>$null | Out-Null
  $dom = & $chrome --headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=4000 --window-size=1080,1350 --dump-dom "$url`?qa" 2>$null | Out-String
  $m = [regex]::Match($dom, '<pre id="qa-out">(.*?)</pre>', 'Singleline')
  $qa = if ($m.Success) { [System.Net.WebUtility]::HtmlDecode($m.Groups[1].Value) | ConvertFrom-Json } else { $null }
  $img = [System.Drawing.Image]::FromFile($png)
  $size = "$($img.Width)x$($img.Height)"
  $thumb = New-Object System.Drawing.Bitmap 360, 450
  $g = [System.Drawing.Graphics]::FromImage($thumb)
  $g.InterpolationMode = 'HighQualityBicubic'; $g.DrawImage($img, 0, 0, 360, 450); $g.Dispose()
  $thumb.Save((Join-Path $root "qa/$n-mobile.png"), [System.Drawing.Imaging.ImageFormat]::Png); $thumb.Dispose(); $img.Dispose()
  $results += [pscustomobject]@{card = $n; size = $size; contentBottom = $qa.contentBottom; bottomGap = $qa.bottomGap; errors = ($qa.errors -join '; '); fonts = $qa.fonts}
}
$results | ConvertTo-Json -Depth 4 | Out-File (Join-Path $root 'qa/layout-check.json') -Encoding utf8
$results | Format-Table card, size, contentBottom, bottomGap, errors -AutoSize | Out-String -Width 200
