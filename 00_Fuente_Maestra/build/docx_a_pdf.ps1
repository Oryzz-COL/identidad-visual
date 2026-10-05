# Oryzz · convierte .docx a PDF con Microsoft Word (verificación visual de plantillas)
# Uso: powershell -ExecutionPolicy Bypass -File docx_a_pdf.ps1 -Entrada <carpeta o .docx> -Salida <carpeta>
param([Parameter(Mandatory=$true)][string]$Entrada, [Parameter(Mandatory=$true)][string]$Salida)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $Salida | Out-Null
$files = if ((Get-Item $Entrada).PSIsContainer) { Get-ChildItem -Path $Entrada -Recurse -Filter *.docx | Where-Object { $_.Name -notlike '~$*' } } else { @(Get-Item $Entrada) }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  foreach ($f in $files) {
    $doc = $word.Documents.Open($f.FullName, $false, $true)
    [string]$out = [System.IO.Path]::Combine($Salida, $f.BaseName + '.pdf')
    $doc.ExportAsFixedFormat($out, 17)
    $doc.Close([ref]0)
    Write-Output "ok $out"
  }
} finally { $word.Quit() }
