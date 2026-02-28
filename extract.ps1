$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)

$patterns = @('class hE{', 'class bb{', 'class ub{', 'class Lb{')

foreach ($p in $patterns) {
    $i = $s.IndexOf($p)
    if ($i -ge 0) {
        Write-Output "--- $p ---"
        # Extract about 8000 chars for Lb and bb as they are large
        Write-Output $s.Substring($i, 8000)
        Write-Output "`r`n"
    }
}
