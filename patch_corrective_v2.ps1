$f = 'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
$s = [System.IO.File]::ReadAllText($f)

# 1. Update mock data in hE.init to be fully compatible
$mock_data = 'const mocks=[{uid:"cat_1_l",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"Gelinlik - Klasik"}],article_image:{url:"/kategori/1 sol gelinlik.png"},title:"Gelinlik - Klasik",short_desc:"Zarif ve zamansız bir gelinlik.",etek_kesimi:"A Kesim",kumas:"Fransız Danteli",url:"https://minalidya.wedding/kategori/gelinlik"}},{uid:"cat_1_r",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"Tesettür Gelinlik"}],article_image:{url:"/kategori/1 sag tesettur gelinlik.png"},title:"Tesettür Gelinlik",short_desc:"Modern ve nazik tesettür tasarımı.",etek_kesimi:"Prenses",kumas:"Mikas",url:"https://minalidya.wedding/kategori/tesettur-gelinlik"}},{uid:"cat_2_l",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"Nişanlık - Modern"}],article_image:{url:"/kategori/2 sol nisanlik.png"},title:"Nişanlık - Modern",short_desc:"Özel günleriniz için modern şıklık.",etek_kesimi:"Balık",kumas:"Saten",url:"https://minalidya.wedding/kategori/nisanlik"}},{uid:"cat_2_r",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"Kınalık - Geleneksel"}],article_image:{url:"/kategori/2 sag kinalik.png"},title:"Kınalık - Geleneksel",short_desc:"Geleneksel motiflerle bezeli kinalık.",etek_kesimi:"Bindallı",kumas:"Kadife",url:"https://minalidya.wedding/kategori/kinalik"}},{uid:"cat_3_l",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"Söz Elbisesi"}],article_image:{url:"/kategori/3 sol soz.png"},title:"Söz Elbisesi",short_desc:"Sade ve etkileyici bir söz elbisesi.",etek_kesimi:"Düz",kumas:"Şifon",url:"https://minalidya.wedding/kategori/soz-elbisesi"}},{uid:"cat_3_r",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"After Party Elbisesi"}],article_image:{url:"/kategori/3 sag after.png"},title:"After Party Elbisesi",short_desc:"Eğlence dolu anlar için konforlu şıklık.",etek_kesimi:"Kısa",kumas:"Simli Kumaş",url:"https://minalidya.wedding/kategori/after-party"}},{uid:"cat_4_l",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"Kaftan - El İşçiliği"}],article_image:{url:"/kategori/4 sol kaftan.png"},title:"Kaftan - El İşçiliği",short_desc:"Yüksek kalite el işçiliği ile üretilmiştir.",etek_kesimi:"Geleneksel",kumas:"İpek",url:"https://minalidya.wedding/kategori/kaftan"}},{uid:"cat_4_r",first_publication_date:new Date().toISOString(),data:{article_title:[{text:"Abiye - Gece Elbisesi"}],article_image:{url:"/kategori/4 sag abiye.png"},title:"Abiye - Gece Elbisesi",short_desc:"Gecenin yıldızı olmanız için tasarlandı.",etek_kesimi:"Yırtmaçlı",kumas:"Brokar",url:"https://minalidya.wedding/kategori/abiye"}}]; mocks.forEach(m=>{this.articles.push(m);this.prismicCache[m.uid]=m});'

# We need to find where we injected the previous mock_data and replace it.
# Or just find the end of articles.forEach and append mocks there.
# I'll try to find my previous injection marker.
$old_injection_marker = 'this.articles.forEach(n=>{this.prismicCache[n.uid]=n})'
# We replace it with the marker + our mocks. We make sure not to double inject if the file already has them.
if ($s.Contains('const mocks=')) {
    # If already injected, we replace the old mocks with new ones.
    # We find the start of 'const mocks=' and the end of 'this.prismicCache[m.uid]=m});'
    $start = $s.IndexOf('const mocks=[')
    $end = $s.IndexOf('this.prismicCache[m.uid]=m});', $start) + 'this.prismicCache[m.uid]=m});'.Length
    $s = $s.Remove($start, $end - $start).Insert($start, $mock_data)
}
else {
    $s = $s.Replace($old_injection_marker, $old_injection_marker + ';' + $mock_data)
}

# 2. Add null safety to Lb constructor to prevent crash
$old_lb_loop = 'this.experience.articles.forEach(s=>{this.linksContainer.innerHTML+=`<li><a href=''/gallery/${s.uid}''>${s.data.article_title[0].text}</a><div class =''menu_links_hover''></div></li>  `})'
$new_lb_loop = 'this.experience.articles.forEach(s=>{const t=(s.data&&s.data.article_title&&s.data.article_title[0])?s.data.article_title[0].text:(s.data?s.data.title:s.uid);this.linksContainer.innerHTML+=`<li><a href=''/gallery/${s.uid}''>${t}</a><div class =''menu_links_hover''></div></li>  `})'
$s = $s.Replace($old_lb_loop, $new_lb_loop)

# 3. Fix Sb update to be more robust (if not already)
$old_sb_update = 'update(){if(!this.overlay)this.overlay=document.querySelector(".details_content");if(!this.overlay)return;if(this.btn.isOpen){this.overlay.classList.add("active");const t=document.querySelector(".details_title"),d=document.querySelector(".details_desc"),e=document.querySelector(".etek_value"),k=document.querySelector(".kumas_value"),c=document.querySelector(".details_cta");if(t)t.innerHTML=this.article.data.title;if(d)d.innerHTML=this.article.data.short_desc;if(e)e.innerHTML=this.article.data.etek_kesimi;if(k)k.innerHTML=this.article.data.kumas;if(c)c.href=this.article.data.url;}else{const anyOpen=this.experience.world&&this.experience.world.page&&this.experience.world.page.btns&&this.experience.world.page.btns.some(b=>b.isOpen);if(!anyOpen)this.overlay.classList.remove("active");}}'
# No change needed here if it's already patched, but let's ensure it maps to article_title if needed.
# Actually, Sb.update should probably use the same fallback for title.
$safe_sb_update = 'update(){if(!this.overlay)this.overlay=document.querySelector(".details_content");if(!this.overlay)return;if(this.btn.isOpen){this.overlay.classList.add("active");const t=document.querySelector(".details_title"),d=document.querySelector(".details_desc"),e=document.querySelector(".etek_value"),k=document.querySelector(".kumas_value"),c=document.querySelector(".details_cta");const title=(this.article.data&&this.article.data.article_title&&this.article.data.article_title[0])?this.article.data.article_title[0].text:(this.article.data?this.article.data.title:this.article.uid);if(t)t.innerHTML=title;if(d)d.innerHTML=this.article.data.short_desc;if(e)e.innerHTML=this.article.data.etek_kesimi;if(k)k.innerHTML=this.article.data.kumas;if(c)c.href=this.article.data.url;}else{const anyOpen=this.experience.world&&this.experience.world.page&&this.experience.world.page.btns&&this.experience.world.page.btns.some(b=>b.isOpen);if(!anyOpen&&this.overlay)this.overlay.classList.remove("active");}}'
$s = $s.Replace($old_sb_update, $safe_sb_update)

[System.IO.File]::WriteAllText($f, $s)
Write-Output "Corrective patch V2 applied successfully."
