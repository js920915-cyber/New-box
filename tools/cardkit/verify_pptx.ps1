# PPTX를 PowerPoint로 열어 각 장을 1080x1350 PNG로 내보내고 원본 PNG(exports/)와 비교한다.
# 검사: 슬라이드 수, 줄 상자의 자동 줄바꿈/자동 맞춤/여러 문단 여부, 글자가 상자보다 넓은지, 세로 어긋남(px), 픽셀 차이.
# 폰트는 설치하지 않고 AddFontResource로 현재 Windows 세션에만 임시 등록 후 해제한다.
# 사용: powershell -ExecutionPolicy Bypass -File tools/cardkit/verify_pptx.ps1 -Topic content/<slug>
param([Parameter(Mandatory)][string]$Topic)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $Topic).Path
$slug = Split-Path $root -Leaf
$pptx = Join-Path $root "adobe-express/$slug-express.pptx"
$outDir = Join-Path $root 'adobe-express/build/pptx-render'
New-Item -ItemType Directory -Force $outDir | Out-Null
$fontDir = Join-Path $PSScriptRoot '../../templates/fonts'
Add-Type @'
using System; using System.Runtime.InteropServices;
public static class CardkitFonts {
  [DllImport("gdi32.dll", CharSet=CharSet.Unicode)] public static extern int AddFontResourceW(string f);
  [DllImport("gdi32.dll", CharSet=CharSet.Unicode)] public static extern bool RemoveFontResourceW(string f);
  [DllImport("user32.dll")] public static extern IntPtr SendMessageTimeout(IntPtr h, uint m, IntPtr w, IntPtr l, uint f, uint t, out IntPtr r);
}
'@
$fonts = Get-ChildItem (Join-Path $fontDir 'RCardnews-W*.ttf')
$broadcast = { $r = [IntPtr]::Zero; [CardkitFonts]::SendMessageTimeout([IntPtr]0xffff, 0x1D, [IntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$r) | Out-Null }
foreach ($f in $fonts) { [CardkitFonts]::AddFontResourceW($f.FullName) | Out-Null }
& $broadcast
$warn = @()
try {
  $app = New-Object -ComObject PowerPoint.Application
  $pres = $app.Presentations.Open($pptx, $true, $false, $false)
  $slideCount = $pres.Slides.Count
  foreach ($s in $pres.Slides) {
    $s.Export((Join-Path $outDir ('{0:D2}.png' -f $s.SlideIndex)), 'PNG', 1080, 1350)
    foreach ($sh in $s.Shapes) {
      if ($sh.HasTextFrame -and $sh.TextFrame.HasText) {
        $tf = $sh.TextFrame2
        if ($tf.WordWrap -ne 0 -or $tf.AutoSize -ne 0 -or $tf.TextRange.Paragraphs().Count -ne 1) { $warn += "slide $($s.SlideIndex): $($sh.Name) wrap/autosize/paragraphs" }
        if ($tf.TextRange.BoundWidth -gt $sh.Width + 0.5) { $warn += "slide $($s.SlideIndex): text wider than box: $($sh.Name)" }
      }
    }
  }
  $pres.Close(); $app.Quit()
} finally {
  foreach ($f in $fonts) { [CardkitFonts]::RemoveFontResourceW($f.FullName) | Out-Null }
  & $broadcast
}
Add-Type -AssemblyName System.Drawing
function Profile($bmp) { $p = New-Object double[] 1350; for ($y = 0; $y -lt 1350; $y++) { $c = 0; for ($x = 100; $x -lt 980; $x += 4) { if ($bmp.GetPixel($x, $y).R -lt 120) { $c++ } }; $p[$y] = $c }; , $p }
$rows = @(); $fail = $false
$exports = Get-ChildItem (Join-Path $root 'exports') -Filter '*.png' | Where-Object Name -match '^\d\d\.png$' | Sort-Object Name
if ($exports.Count -ne $slideCount) { $warn += "slide count $slideCount != PNG count $($exports.Count)"; $fail = $true }
foreach ($e in $exports) {
  $a = [System.Drawing.Bitmap]::new($e.FullName); $b = [System.Drawing.Bitmap]::new((Join-Path $outDir $e.Name))
  $diff = 0; $total = 0
  for ($y = 0; $y -lt 1350; $y += 3) { for ($x = 0; $x -lt 1080; $x += 3) {
    $p = $a.GetPixel($x, $y); $q = $b.GetPixel($x, $y); $total++
    if ([math]::Abs($p.R - $q.R) + [math]::Abs($p.G - $q.G) + [math]::Abs($p.B - $q.B) -gt 120) { $diff++ } } }
  $pa = Profile $a; $pb = Profile $b; $best = 0; $bestv = 1e18
  foreach ($d in -10..10) { $v = 0; for ($y = 120; $y -lt 1230; $y++) { $v += [math]::Pow($pa[$y] - $pb[$y + $d], 2) }; if ($v -lt $bestv) { $bestv = $v; $best = $d } }
  $ok = ([math]::Abs($best) -le 2) -and ($diff / $total -lt 0.08)
  if (-not $ok) { $fail = $true }
  $rows += [pscustomobject]@{card = $e.BaseName; verticalShiftPx = $best; diffPct = [math]::Round(100 * $diff / $total, 2); pass = $ok}
  $a.Dispose(); $b.Dispose()
}
if ($warn.Count) { $fail = $true }
$report = [pscustomobject]@{pptx = $pptx; slides = $slideCount; warnings = $warn; cards = $rows; result = $(if ($fail) { 'FAIL' } else { 'PASS' })}
$report | ConvertTo-Json -Depth 4 | Out-File (Join-Path $root 'qa/pptx-check.json') -Encoding utf8
$rows | Format-Table -AutoSize | Out-String
if ($warn.Count) { $warn }
"PPTX check: $($report.result)  (PowerPoint 렌더 기준. Adobe Express 실제 가져오기는 별도 확인)"
