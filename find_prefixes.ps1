$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$content = [System.IO.File]::ReadAllText($f)
$classes = @('class bb', 'class ub', 'class Lb', 'class hE')
foreach ($c in $classes) {
    try {
        $idx = $content.IndexOf($c)
        if ($idx -ge 0) {
            $found = $content.Substring($idx, [math]::Min(100, $content.Length - $idx))
            Write-Output ("Found {0}: {1}" -f $c, $found)
        }
        else {
            Write-Output ("Not found {0}" -f $c)
        }
    }
    catch {
        Write-Output ("Error finding {0}" -f $c)
    }
}
