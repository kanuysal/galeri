$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)

# 1. isPhone fix
$old_isPhone = 'window.matchMedia("(max-width: 820px)").matches?_c=!0:_c=!1;new Rt(fE,_c);'
$new_isPhone = 'window.matchMedia("(max-width: 820px)").matches&&/Mobi|Android/i.test(navigator.userAgent)?_c=!0:_c=!1;new Rt(fE,_c);'
$s = $s.Replace($old_isPhone, $new_isPhone)

# 2. directionOffset fix
$old_dir = 'directionOffset(e){var t=0;return this.experience.isPhone&&this.experience.joystick?t=-this.experience.joystick.angle+Math.PI*.5:e.keys||e.arrowdown?e.keyd||e.arrowright?t=Math.PI/4:(e.keya||e.arrowleft)&&(t=-Math.PI/4):e.keyw||e.arrowup?e.keyd||e.arrowright?t=Math.PI/4+Math.PI/2:e.keya||e.arrowleft?t=-Math.PI/4-Math.PI/2:t=Math.PI:e.keyd||e.arrowright?t=Math.PI/2:(e.keya||e.arrowleft)&&(t=-Math.PI/2),t}'
$new_dir = 'directionOffset(e){var t=0;const hj = this.experience.joystick && this.experience.joystick.distance > 0.1;if(hj){t=-this.experience.joystick.angle+Math.PI*.5}else if(e.keyw||e.keya||e.keys||e.keyd||e.arrowup||e.arrowleft||e.arrowdown||e.arrowright){if(e.keys||e.arrowdown){e.keyd||e.arrowright?t=Math.PI/4:(e.keya||e.arrowleft)&&(t=-Math.PI/4)}else if(e.keyw||e.arrowup){e.keyd||e.arrowright?t=Math.PI/4+Math.PI/2:e.keya||e.arrowleft?t=-Math.PI/4-Math.PI/2:t=Math.PI}else if(e.keyd||e.arrowright){t=Math.PI/2}else if(e.keya||e.arrowleft){t=-Math.PI/2}}return t}'
$s = $s.Replace($old_dir, $new_dir)

# 3. voir les détails -> detaylar
$s = $s.Replace('<span>voir les détails</span>', '<span>detaylar</span>')

# 4. showJoystick fix
$old_show = 'showJoystick(e){document.querySelector(".joystick_container").style.display=e?"block":"none"}'
$new_show = 'showJoystick(e){const c=document.querySelector(".joystick_container");if(c)c.style.display="block"}'
$s = $s.Replace($old_show, $new_show)

[System.IO.File]::WriteAllText($f, $s)
Write-Output "Patch applied successfully."
