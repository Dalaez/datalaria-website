$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {
    $wbPath = "C:\Users\dalae\OneDrive\Emprendiendo\datalaria\packages\ES_Matriz_McKinsey_GE_Datalaria.xlsx"
    $wb = $excel.Workbooks.Open($wbPath)
    
    foreach ($ws in $wb.Sheets) {
        Write-Host "`n=== Sheet: $($ws.Name) ==="
        Write-Host "ProtectContents: $($ws.ProtectContents)"
        Write-Host "Protection.AllowSelectingLockedCells: $($ws.Protection.AllowSelectingLockedCells)"
        Write-Host "Protection.AllowSelectingUnlockedCells: $($ws.Protection.AllowSelectingUnlockedCells)"
        Write-Host "Protection.AllowFormattingCells: $($ws.Protection.AllowFormattingCells)"
        Write-Host "Protection.AllowInsertingRows: $($ws.Protection.AllowInsertingRows)"
        Write-Host "Protection.AllowDeletingRows: $($ws.Protection.AllowDeletingRows)"
    }
    
    $wb.Close($false)
} finally {
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}
