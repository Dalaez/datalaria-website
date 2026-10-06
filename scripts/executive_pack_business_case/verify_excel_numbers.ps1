# verify_excel_numbers.ps1
# =========================
# Verificación numérica automatizada mediante Microsoft Excel COM:
# Abre ambos libros (ES y EN), lee los valores calculados en celdas y nombres clave
# y valida consistencia numérica frente a model_core.py con tolerancia < 0.5%.

$ErrorActionPreference = "Stop"

$expectedWacc = 0.0950
$expectedNpvBase = 692991.33
$expectedIrrBase = 0.2889
$expectedPaybackDesc = 3.35
$expectedNpvExp = 741197.01

$files = @(
    @{
        Label = "ES";
        RelPath = "packages\Suite_02_Toma_Decisiones\03_Business_Case_VAN_TIR\[ES]_Business_Case_VAN_TIR\Business_Case_VAN_TIR_Datalaria_ES.xlsx";
        ExpectedCuadre = "Modelo cuadrado";
        ExpectedMotor = "Motor cuadrado";
    },
    @{
        Label = "EN";
        RelPath = "packages\Suite_02_Toma_Decisiones\03_Business_Case_VAN_TIR\[EN]_Financial_Business_Case\Financial_Business_Case_NPV_IRR_Datalaria_EN.xlsx";
        ExpectedCuadre = "Model Balanced";
        ExpectedMotor = "Engine Balanced";
    }
)

Write-Host "================================================================================"
Write-Host "AUDITORÍA NUMÉRICA AUTOMATIZADA EXCEL COM (MICROSOFT EXCEL APPLICATION)"
Write-Host "================================================================================"

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false

$totalErrors = 0

try {
    foreach ($item in $files) {
        $label = $item.Label
        $root = (Get-Item $PSScriptRoot).Parent.Parent.FullName
        $absPath = Join-Path $root $item.RelPath
        Write-Host "`n>>> Verificando libro [$label]: $absPath"

        if (-not (Test-Path -LiteralPath $absPath)) {
            Write-Host "[ERROR CRÍTICO] Archivo no encontrado: $absPath" -ForegroundColor Red
            $totalErrors++
            continue
        }

        $resolvedItem = Get-Item -LiteralPath $absPath
        $wb = $excel.Workbooks.Open($resolvedItem.FullName)
        if ($wb -eq $null) {
            Write-Host "[ERROR CRÍTICO] No se pudo abrir el libro (Workbooks.Open retornó null)." -ForegroundColor Red
            $totalErrors++
            continue
        }
        Write-Host "  [OK] Libro abierto correctamente. Hojas: $($wb.Sheets.Count)"

        # Sheet 1: Dashboard, Sheet 2: Assumptions, Sheet 3: DCF, Sheet 4: Sensitivity
        $wsDash = $wb.Sheets.Item(1)
        $wsAssump = $wb.Sheets.Item(2)
        $wsDcf = $wb.Sheets.Item(3)
        $wsSens = $wb.Sheets.Item(4)

        # Lectura de celdas clave
        $waccVal = [double]$wsAssump.Range("C28").Value2
        $vanBaseVal = [double]$wsDcf.Range("C33").Value2
        $tirBaseVal = [double]$wsDcf.Range("C35").Value2
        $paybackDescVal = [double]$wsDcf.Range("C38").Value2
        $vanExpVal = [double]$wsSens.Range("D53").Value2
        $cuadreDcf = [string]$wsDcf.Range("C42").Value2
        $cuadreMotor = [string]$wsSens.Range("N7").Value2
        $dictamen = [string]$wsDash.Range("B8").Value2

        Write-Host ("  • WACC Calculado (C28):       {0:P2} (Esperado: {1:P2})" -f $waccVal, $expectedWacc)
        Write-Host ("  • VAN Base 5Y (C33):          {0:N2} € (Esperado: {1:N2} €)" -f $vanBaseVal, $expectedNpvBase)
        Write-Host ("  • TIR Base (C35):             {0:P2} (Esperado: {1:P2})" -f $tirBaseVal, $expectedIrrBase)
        Write-Host ("  • Payback Descontado (C38):   {0:N2} años (Esperado: {1:N2} años)" -f $paybackDescVal, $expectedPaybackDesc)
        Write-Host ("  • VAN Esperado E[VAN] (D53):  {0:N2} € (Esperado: {1:N2} €)" -f $vanExpVal, $expectedNpvExp)
        Write-Host ("  • Dictamen Comité (Dash B8):  {0}" -f $dictamen)
        Write-Host ("  • Control Cuadre DCF (C42):   {0}" -f $cuadreDcf)
        Write-Host ("  • Control Motor Sens (N7):    {0}" -f $cuadreMotor)

        # Validaciones de Tolerancia (< 0.5%)
        $diffWacc = [Math]::Abs($waccVal - $expectedWacc)
        $diffNpv = [Math]::Abs($vanBaseVal - $expectedNpvBase) / $expectedNpvBase
        $diffIrr = [Math]::Abs($tirBaseVal - $expectedIrrBase)
        $diffPayback = [Math]::Abs($paybackDescVal - $expectedPaybackDesc)
        $diffExp = [Math]::Abs($vanExpVal - $expectedNpvExp) / $expectedNpvExp

        if ($diffWacc -gt 0.001) {
            Write-Host "    [FALLO] WACC difiere de model_core.py" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] WACC coincide exactamente." -ForegroundColor Green
        }

        if ($diffNpv -gt 0.005) {
            Write-Host "    [FALLO] VAN Base difiere en más de 0.5%" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] VAN Base coincide dentro de tolerancia (< 0.5%)." -ForegroundColor Green
        }

        if ($diffIrr -gt 0.005) {
            Write-Host "    [FALLO] TIR Base difiere en más de 0.5 pp" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] TIR Base coincide dentro de tolerancia." -ForegroundColor Green
        }

        if ($diffPayback -gt 0.05) {
            Write-Host "    [FALLO] Payback descontado difiere en más de 0.05 años" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] Payback descontado coincide con interpolación." -ForegroundColor Green
        }

        if ($diffExp -gt 0.005) {
            Write-Host "    [FALLO] VAN Esperado difiere en más de 0.5%" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] VAN Esperado coincide dentro de tolerancia." -ForegroundColor Green
        }

        if (-not ($cuadreDcf -match $item.ExpectedCuadre)) {
            Write-Host "    [FALLO] Control de cuadre DCF fallido: $cuadreDcf" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] Control de cuadre matemático verificado ($($item.ExpectedCuadre))." -ForegroundColor Green
        }

        if (-not ($cuadreMotor -match $item.ExpectedMotor)) {
            Write-Host "    [FALLO] Control del motor de sensibilidad fallido: $cuadreMotor" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] Consistencia de recálculo del motor verificada ($($item.ExpectedMotor))." -ForegroundColor Green
        }

        if (-not ($dictamen -match "APROBAR" -or $dictamen -match "APPROVE")) {
            Write-Host "    [FALLO] Dictamen inesperado: $dictamen" -ForegroundColor Red
            $totalErrors++
        } else {
            Write-Host "    [OK] Dictamen de inversión C-Level verificado (APROBAR/APPROVE)." -ForegroundColor Green
        }

        $wb.Close($false)
    }
} finally {
    try {
        if ($excel) {
            $excel.Quit()
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
        }
    } catch {
        # Ignorar fallos de quit COM si el proceso ya cerró
    }
    [System.GC]::Collect()
    Start-Sleep -Milliseconds 300
    Get-Process EXCEL -ErrorAction SilentlyContinue | Stop-Process -Force
}

Write-Host "`n================================================================================"
if ($totalErrors -eq 0) {
    Write-Host "[AUDITORÍA NUMÉRICA SUPERADA] Todas las cifras coinciden con model_core.py (100% consistencia)." -ForegroundColor Green
    exit 0
} else {
    Write-Host "[AUDITORÍA NUMÉRICA CON ERRORES] Se detectaron $totalErrors discrepancias." -ForegroundColor Red
    exit 1
}
