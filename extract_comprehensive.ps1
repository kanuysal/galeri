$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)

function Get-Class ($name) {
    Write-Output "Searching for: class $name..."
    $pattern = "class $name{"
    $i = $s.IndexOf($pattern)
    if ($i -ge 0) {
        Write-Output "--- START class $name at $i ---"
        Write-Output $s.Substring($i, 15000) # Increased length to be safe
        Write-Output "--- END class $name ---"
        Write-Output "`r`n"
    }
    else {
        Write-Output "--- class $name not found ---"
    }
}

Get-Class "hE"
Get-Class "bb"
Get-Class "ub"
Get-Class "Lb"
