$excel = [System.Runtime.InteropServices.Marshal]::GetActiveObject('Excel.Application')
foreach ($wb in $excel.Workbooks) {
    Write-Host "Open: $($wb.FullName)"
}
