import os
import re

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"

def find_block(content, start_marker, end_marker="{"):
    start_index = content.find(start_marker)
    if start_index == -1:
        return -1, -1
    
    # Find the opening brace
    brace_start = content.find(end_marker, start_index + len(start_marker))
    if brace_start == -1:
        return -1, -1
        
    depth = 0
    for i in range(brace_start, len(content)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return start_index, i + 1
    return -1, -1

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Patch db class (Homepage)
# We want to replace the setCadres method or the whole class if easier.
# Let's target setCadres inside db.
db_start, db_end = find_block(content, "class db")
if db_start != -1:
    db_content = content[db_start:db_end]
    # Replace setCadres logic
    new_set_cadres = """setCadres() {
        const categories = [
            { label: "Gelinlik", uid: "gelinlik", image: "image_left_bottom" },
            { label: "Tesettür Gelinlik", uid: "tesettur", image: "image_left_mid" },
            { label: "A-Kesim Gelinlik", uid: "akesim", image: "image_left_mid_loin" },
            { label: "Prenses Gelinlik", uid: "prenses", image: "image_left_top" },
            { label: "Helen Gelinlik", uid: "helen", image: "image_right_bottom" },
            { label: "Balık Gelinlik", uid: "balik", image: "image_right_mid" },
            { label: "Nikah Elbisesi", uid: "nikah", image: "image_right_mid_loin" },
            { label: "Büyük Beden", uid: "buyukbeden", image: "image_right_top" }
        ];
        this.cadresControllers.forEach((t, n) => {
            const cat = categories[n % categories.length];
            const s = this.homeData[cat.image].uid;
            const o = this.ressources.items[s];
            const a = new P;
            t.getWorldPosition(a);
            const l = new th(a, t.rotation, 2, o);
            const c = new dc(l.instance);
            // Clicking category leads to filtered gallery
            const h = { uid: cat.uid, data: { article_title: [{ text: cat.label }] }, isCategory: true };
            const u = new ub(l.instance, c, h);
            this.cadres.push(l), this.btns.push(c), this.links.push(u);
        });
    }"""
    # Find setCadres in db_content
    sc_start, sc_end = find_block(db_content, "setCadres")
    if sc_start != -1:
        db_content = db_content[:sc_start] + new_set_cadres + db_content[sc_end:]
        content = content[:db_start] + db_content + content[db_end:]

# 2. Patch bb class (Gallery)
bb_start, bb_end = find_block(content, "class bb")
if bb_start != -1:
    bb_content = content[bb_start:bb_end]
    # Replace constructor
    new_bb_constructor = """constructor(e) {
        this.experience = new Rt;
        this.scene = this.experience.scene;
        this.ressources = this.experience.resources;
        this.camera = this.experience.camera.instance;
        this.group = new Nn;
        this.scene.add(this.group);
        this.cadres = [];
        this.btns = [];
        this.links = [];
        this.fromGallery = e;
        
        // Filter logic
        const params = new URLSearchParams(window.location.search);
        const filter = params.get('category') || params.get('filter');
        
        this.articles = [...this.experience.router.articles];
        if (filter) {
            this.articles = this.articles.filter(a => 
                (a.data.category && a.data.category.toLowerCase() === filter.toLowerCase()) ||
                (a.uid && a.uid.toLowerCase().includes(filter.toLowerCase()))
            );
        }
        
        // Limit to 15
        this.articles = this.articles.slice(-15).reverse();
        
        this.articles.forEach((t, n) => {
            const i = new th(new P(1.2 + n * 1.2, 0.99 + n % 2 * 0.99, -0.5), new P(0, 0, 0), 1.5, this.experience.resources.items[t.uid], t.uid);
            const s = new dc(i.instance);
            const o = new Sb(i.instance, s, t);
            this.cadres.push(i), this.btns.push(s), this.links.push(o);
        });
        this.group.add(...this.cadres.map(c => c.instance));
    }"""
    const_start, const_end = find_block(bb_content, "constructor")
    if const_start != -1:
        bb_content = bb_content[:const_start] + new_bb_constructor + bb_content[const_end:]
        content = content[:bb_start] + bb_content + content[bb_end:]

# 3. Patch Lb class (Menu)
lb_start, lb_end = find_block(content, "class Lb")
if lb_start != -1:
    lb_content = content[lb_start:lb_end]
    # Update menu structure injection
    # In constructor, we'll replace the linksContainer population
    menu_patch = """
        this.linksContainer = document.querySelector(".menu_links ul");
        this.linksContainer.innerHTML = \"\"";
        
        // Split menu into filters and products
        this.linksContainer.style.display = "flex";
        this.linksContainer.style.width = "100%";
        
        const filterHtml = `
            <div class="menu_left_filters" style="width: 30%; border-right: 1px solid rgba(255,255,255,0.2); padding-right: 20px;">
                <h3 style="font-size: 1.2rem; margin-bottom: 20px; opacity: 0.8;">KATEGORİLER</h3>
                <ul class="cat_filters" style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="all" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Tümü</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="gelinlik" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Gelinlik</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="tesettur" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Tesettür</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="akesim" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">A-Kesim</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="prenses" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Prenses</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="helen" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Helen</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="balik" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Balık</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="nikah" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Nikah Elbisesi</a></li>
                    <li style="margin-bottom: 10px;"><a href="#" data-filter="buyukbeden" style="text-decoration: none; color: white; opacity: 0.6; transition: 0.3s;">Büyük Beden</a></li>
                </ul>
            </div>
            <div class="menu_right_products" style="width: 70%; padding-left: 40px; overflow-y: auto; max-height: 60vh;">
                <ul class="product_list" style="list-style: none; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <!-- items will be injected here -->
                </ul>
            </div>
        `;
        this.linksContainer.innerHTML = filterHtml;
        
        const prodList = this.linksContainer.querySelector(".product_list");
        const refreshProds = (filter = "all") => {
            prodList.innerHTML = "";
            let items = this.experience.articles;
            if (filter !== "all") {
                items = items.filter(s => (s.data.category && s.data.category.toLowerCase() === filter) || s.uid.includes(filter));
            }
            items.forEach(s => {
                prodList.innerHTML += `<li><a href='/gallery/${s.uid}' style="font-size: 0.9rem; text-decoration: none; color: white; opacity: 0.8;">${s.data.article_title[0].text}</a></li>`;
            });
            // Update routing for new links
            prodList.querySelectorAll("a").forEach(a => {
                a.addEventListener("click", e => { e.preventDefault(); this.experience.router.route(new URL(a.href).pathname); this.toggleButton(); });
            });
        };
        refreshProds();
        
        this.linksContainer.querySelectorAll(".cat_filters a").forEach(a => {
            a.addEventListener("click", e => {
                e.preventDefault();
                this.linksContainer.querySelectorAll(".cat_filters a").forEach(link => link.style.opacity = "0.6");
                a.style.opacity = "1";
                refreshProds(a.getAttribute("data-filter"));
            });
        });
    """
    # Replace the old forEach articles loop
    old_loop = 'this.linksContainer=document.querySelector(".menu_links ul"),this.linksContainer.innerHTML="",this.experience.articles.forEach(s=>{this.linksContainer.innerHTML+=`<li><a href=\'/gallery/${s.uid}\'>${s.data.article_title[0].text}</a><div class =\'menu_links_hover\'></div></li>  `})'
    if old_loop in lb_content:
        lb_content = lb_content.replace(old_loop, menu_patch)
        
    # Fix Video Error
    old_play = 'n.play().catch(l=>console.warn("Erreur lecture vidéo:",l))'
    new_play = 'const p=n.play();if(p!==undefined){p.catch(l=>{})}'
    lb_content = lb_content.replace(old_play, new_play)
    
    content = content[:lb_start] + lb_content + content[lb_end:]

# 4. Patch Loader (_w class)
loader_start, loader_end = find_block(content, "class _w")
if loader_start != -1:
    loader_content = content[loader_start:loader_end]
    # Add safety timeout to ready trigger
    timeout_patch = """this.startLoading();
        setTimeout(() => { if(this.loaded < this.toLoad) { console.log("Safety ready trigger"); this.trigger("ready"); } }, 5000);
    """
    if "this.startLoading()" in loader_content:
        loader_content = loader_content.replace("this.startLoading()", timeout_patch)
    content = content[:loader_start] + loader_content + content[loader_end:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied successfully.")
