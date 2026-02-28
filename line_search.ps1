$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$lines = Get-Content $f
$patterns = @{
    "bb"          = "class bb{";
    "ub"          = "class ub{";
    "Lb"          = "class Lb{";
    "hE"          = "class hE";
    "Rt"          = "class Rt{";
    "hE_articles" = ".articles=await this.client.getAllByType"
}

foreach ($key in $patterns.Keys) {
    $p = $patterns[$key]
    for ($i = 0; $i -lt $lines.Length; $i++) {
        if ($lines[$i].Contains($p)) {
            Write-Output "$key on line $($i + 1)"
        }
    }
}
