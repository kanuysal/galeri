$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)
$idx = $s.IndexOf('.articles =')
if ($idx -ge 0) {
    Write-Output "Found at $idx"
    Write-Output $s.Substring($idx - 100, 300)
}
else {
    Write-Output "Not found"
}
