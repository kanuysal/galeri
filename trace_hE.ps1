$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)
$idx = $s.IndexOf('class hE')
if ($idx -ge 0) {
    $end = $s.IndexOf('class ', $idx + 10)
    if ($end -lt 0) { $end = $s.Length }
    $chunk = $s.Substring($idx, $end - $idx)
    $artIdx = $chunk.IndexOf('.articles=')
    if ($artIdx -ge 0) {
        Write-Output "Found .articles= in class hE at $($idx + $artIdx)"
        Write-Output $chunk.Substring($artIdx, 500)
    }
    else {
        Write-Output "Not found .articles= in class hE"
        Write-Output "Checking first 2000 chars of class hE:"
        Write-Output $chunk.Substring(0, 2000)
    }
}
else {
    Write-Output "hE not found"
}
