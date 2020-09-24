function do-autorunsc () {
    write-output "Benchmarks place this function's average runtime around 60 seconds. Please be patient"
    if ((Test-Path "env:TOOL_DIR") -eq $True){
        $toolDir = $env:TOOL_DIR
    } else {
        $toolDir = "C:\Security\"
    }
    New-Item $toolDir -ItemType Directory -ErrorAction SilentlyContinue
    Set-Location $toolDir
    .\autorunsc.exe -accepteula -nobanner -a * -c -m -s > .\autoruns.csv
    $all = Import-csv "autoruns.csv"

    #Create blank object to hold output from formatting function.
    $OutObj = @()

    # Only log objects with a valid entry
    $all | ForEach-Object -process {
        if ($_.entry -ne ""){
            $outObj = $outObj + $_
        }
    }

    #Output formatted csv to file
    $OutObj | Export-Csv .\AutorunsLog.csv -force

    #cleanup
    del -Force .\autoruns.csv -ErrorAction SilentlyContinue | out-null
    write-output "$toolDir\AutorunsLog.csv has been written to disk"
    Pop-Location
}
