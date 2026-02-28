$f = 'd:\minadesign\github\antigravity\SERKAN\minalidya.wedding\assets\json\products.json'
$json = Get-Content $f -Raw | ConvertFrom-Json
$allCats = @()
foreach ($p in $json) {
    if ($p.category) {
        $allCats += $p.category
    }
}
$uniqueCats = $allCats | Select-Object -Unique
Write-Output "Unique Categories:"
Write-Output ($uniqueCats -join ", ")
