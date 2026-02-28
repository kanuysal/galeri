$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)
$idx = $s.IndexOf('class Rt')
if ($idx -ge 0) {
    Write-Output "Found Rt at $idx"
    Write-Output $s.Substring($idx, 2000)
}
else {
    Write-Output "Rt not found"
}
