# Oryzz · post-proceso con PowerPoint (Windows + Office)
#   - Guarda el .pptx con las fuentes TrueType incrustadas (Space Grotesk, Manrope, JetBrains Mono)
#   - Exporta cada diapositiva a PNG (render nativo de PowerPoint) y, opcionalmente, a PDF
# Uso: powershell -File pres_powerpoint.ps1 -In origen.pptx -Out destino.pptx [-PngDir carpeta] [-PngWidth 1920] [-Pdf salida.pdf] [-NoEmbed]
param(
  [Parameter(Mandatory = $true)][string]$In,
  [Parameter(Mandatory = $true)][string]$Out,
  [string]$PngDir = '',
  [int]$PngWidth = 1920,
  [string]$Pdf = '',
  [switch]$NoEmbed
)
$ErrorActionPreference = 'Stop'
$In = (Resolve-Path $In).Path
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open($In, 0, 0, 0)   # ReadOnly=false, Untitled=false, WithWindow=false
  $embed = -1
  if ($NoEmbed) { $embed = 0 }
  $pres.SaveAs($Out, 24, $embed)                   # 24 = ppSaveAsOpenXMLPresentation
  if ($PngDir -ne '') {
    New-Item -ItemType Directory -Force $PngDir | Out-Null
    $h = [int]($PngWidth * 9 / 16)
    $i = 0
    foreach ($s in $pres.Slides) {
      $i++
      $s.Export((Join-Path $PngDir ('s{0:D2}.png' -f $i)), 'PNG', $PngWidth, $h)
    }
  }
  if ($Pdf -ne '') { $pres.SaveAs($Pdf, 32) }      # 32 = ppSaveAsPDF
  $pres.Close()
  Write-Output "ok $Out"
} finally {
  $app.Quit()
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($app) | Out-Null
}
