$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$file = (Resolve-Path "scratch/test_tornado_strref.xlsx").Path
$wb = $excel.Workbooks.Open($file)
$ws = $wb.Worksheets.Item(1)
$ch = $ws.ChartObjects(1).Chart
$out = (Resolve-Path "scratch").Path + "\test_tornado_strref_result.png"
$ch.Export($out)
$wb.Close($false)
$excel.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
Write-Host "Exported to: $out"
