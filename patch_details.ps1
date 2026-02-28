$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)

# 1. Translate "See details" in ub
$old_see = 'this.link.innerHTML="<p>See details</p><div></div>"'
$new_see = 'this.link.innerHTML="<p>detaylar</p><div></div>"'
$s = $s.Replace($old_see, $new_see)

# 2. Patch Sb constructor
$old_sb_const = 'class Sb{constructor(e,t,n){this.experience=new Rt,this.scene=this.experience.scene,this.ressources=this.experience.ressources,this.time=this.experience.time,this.ref=e,this.btn=t,this.article=n,this.projectedPosition=new P,this.link=document.createElement("a"),this.link.classList.add("gallery_link"),this.link.href=`/gallery/${this.article.uid}`,this.link.innerHTML="<span>voir les d\u00e9tails</span><div></div>",this.isClassAdded=!1,this.delayTimeout=null,this.isVisible=!0,Object.assign(this.link.style,{position:"absolute",transform:"translate(-50%, -50%)",transition:"opacity 0.2s ease"}),this.container=document.querySelector(".container"),this.container.appendChild(this.link),this.link.addEventListener("click",i=>{i.preventDefault(),this.experience.world.page.needTransition=!0,this.link.style.opacity="0",this.experience.router.route(i)}),this.link.addEventListener("touchstart",i=>{i.preventDefault(),this.experience.world.page.needTransition=!0,this.link.style.opacity="0",this.experience.router.route(i)}),window.addEventListener("keydown",this._keydownListener=e=>{const t=this.link.classList;if(e.key==="Enter"&&t.contains("link_open")){const n=document.activeElement;if(n&&(n.tagName==="INPUT"||n.tagName==="TEXTAREA"||n.isContentEditable))return;this.link.click()}})}'
$new_sb_const = 'class Sb{constructor(e,t,n){this.experience=new Rt,this.scene=this.experience.scene,this.ressources=this.experience.ressources,this.time=this.experience.time,this.ref=e,this.btn=t,this.article=n,this.overlay=document.querySelector(".details_content")}'
$s = $s.Replace($old_sb_const, $new_sb_const)

# 3. Patch Sb update
$old_sb_update = 'update(){this.projectedPosition.set(this.ref.position.x-.3,this.ref.position.y+.8,this.ref.position.z).project(this.experience.camera.instance);const e=(this.projectedPosition.x*.5+.5)*window.innerWidth,t=(-this.projectedPosition.y*.5+.5)*window.innerHeight;this.link.style.left=`${e}px`,this.link.style.top=`${t}px`,this.btn.isOpen&&this.isVisible?this.link.classList.add("link_open"):this.link.classList.remove("link_open")}'
$new_sb_update = 'update(){if(this.btn.isOpen){this.overlay.classList.add("active");document.querySelector(".details_title").innerHTML=this.article.data.title;document.querySelector(".details_desc").innerHTML=this.article.data.short_desc;document.querySelector(".etek_value").innerHTML=this.article.data.etek_kesimi;document.querySelector(".kumas_value").innerHTML=this.article.data.kumas;document.querySelector(".details_cta").href=this.article.data.url;}else{const anyOpen=this.experience.world&&this.experience.world.page&&this.experience.world.page.btns&&this.experience.world.page.btns.some(b=>b.isOpen);if(!anyOpen)this.overlay.classList.remove("active");}}'
$s = $s.Replace($old_sb_update, $new_sb_update)

[System.IO.File]::WriteAllText($f, $s)
Write-Output "Details patch applied successfully."
