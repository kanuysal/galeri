$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)

# 1. Inject Category Textures into Sources (Lw)
# We append the new categories to the Lw constant array. 
# It's better to add them as new objects in the array.
$category_sources = ',{name:"cat_1_r",type:"texture",path:"/kategori/1 sag tesettur gelinlik.png"},{name:"cat_1_l",type:"texture",path:"/kategori/1 sol gelinlik.png"},{name:"cat_2_r",type:"texture",path:"/kategori/2 sag kinalik.png"},{name:"cat_2_l",type:"texture",path:"/kategori/2 sol nisanlik.png"},{name:"cat_3_r",type:"texture",path:"/kategori/3 sag after.png"},{name:"cat_3_l",type:"texture",path:"/kategori/3 sol soz.png"},{name:"cat_4_r",type:"texture",path:"/kategori/4 sag abiye.png"},{name:"cat_4_l",type:"texture",path:"/kategori/4 sol kaftan.png"}'
$s = $s.Replace('path:"/textures/oeuvre.png"}]', 'path:"/textures/oeuvre.png"}' + $category_sources + ']')

# 2. Modify db.setCadres to use our hardcoded categories
# We replace the dynamic prismic-based mapping with our fixed category mapping.
$old_setCadres = 'setCadres(){const e=["image_left_bottom","image_left_mid","image_left_mid_loin","image_left_top","image_right_bottom","image_right_mid","image_right_mid_loin","image_right_top"];this.cadresControllers.forEach((t,n)=>{var d;const i=e[n%e.length],s=(d=this.homeData[i])==null?void 0:d.uid,o=this.ressources.items[s],a=new P;t.getWorldPosition(a);const l=new th(a,t.rotation,2,o),c=new dc(l.instance),h=this.experience.router.articles.find(f=>{var _;return f.uid===((_=this.homeData[i])==null?void 0:_.uid)}),u=new ub(l.instance,c,h);this.cadres.push(l),this.btns.push(c),this.links.push(u)})}'
$new_setCadres = 'setCadres(){const cats=[{id:"cat_1_l",texture:"cat_1_l"},{id:"cat_2_l",texture:"cat_2_l"},{id:"cat_3_l",texture:"cat_3_l"},{id:"cat_4_l",texture:"cat_4_l"},{id:"cat_1_r",texture:"cat_1_r"},{id:"cat_2_r",texture:"cat_2_r"},{id:"cat_3_r",texture:"cat_3_r"},{id:"cat_4_r",texture:"cat_4_r"}];this.cadresControllers.forEach((t,n)=>{const cat=cats[n%cats.length];const o=this.ressources.items[cat.texture];const a=new P;t.getWorldPosition(a);const l=new th(a,t.rotation,2,o);const c=new dc(l.instance);const h={uid:cat.id,title:cat.id};const u=new ub(l.instance,c,h);this.cadres.push(l),this.btns.push(c),this.links.push(u)})}'
$s = $s.Replace($old_setCadres, $new_setCadres)

[System.IO.File]::WriteAllText($f, $s)
Write-Output "Category mapping patch applied successfully."
