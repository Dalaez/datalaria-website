try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $file = (Resolve-Path -LiteralPath "packages/Suite_02_Toma_Decisiones/03_Business_Case_VAN_TIR/[ES]_Business_Case_VAN_TIR/Business_Case_VAN_TIR_Datalaria_ES.xlsx").Path
    $wb = $excel.Workbooks.Open($file)
    foreach ($s in $wb.Worksheets) {
        Write-Host "Found Worksheet:" $s.Name
    }
    $ws = $wb.Worksheets.Item("Sensibilidad & Tornado")
    Write-Host "Sheet name:" $ws.Name
    Write-Host "Chart count:" $ws.ChartObjects().Count
    $ch = $ws.ChartObjects(1).Chart
    $out = (Resolve-Path "scratch").Path + "\official_tornado_result.png"
    $ch.Export($out)
    Write-Host "Chart exported to:" $out
    $wb.Close($false)
    $excel.Quit()
} catch {
    Write-Host "Caught exception at line:" $_.InvocationInfo.ScriptLineNumber
    Write-Host "Line text:" $_.InvocationInfo.Line
    Write-Host "Error message:" $_.Exception.ToString()
}
