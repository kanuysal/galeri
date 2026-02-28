import shutil
import re
import os

base_dir = "d:/minadesign/github/antigravity/SERKAN/game/assets"
src = r"C:\Users\Serkan\Downloads\codrops-tutorial-text-animation-main\thevertmenthe dault lafon fr\assets\index-845b001d.js"
dst = os.path.join(base_dir, "index-845b001d.js")

shutil.copyfile(src, dst)

with open(dst, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Patch hE (Router)
router_old = r'const s=await fetch\("https://minalidya\.com/api/articles"\);if\(!s\.ok\)throw new Error\("Network response was not ok"\);const o=await s\.json\(\);this\.articles=o\.data'
router_new = 'const s=await fetch("/products.json");if(!s.ok)throw new Error("Network response was not ok");const o=await s.json();this.articles=o.data'
content = re.sub(router_old, router_new, content)

# 2. Patch db (Homepage setGalerie)
db_start = content.find("class db {")
if db_start == -1: db_start = content.find("class db{")
set_galerie_start = content.find("setGalerie(){", db_start)
if set_galerie_start == -1: set_galerie_start = content.find("setGalerie() {", db_start)
if set_galerie_start != -1:
    brace_start = content.find("{", set_galerie_start)
    depth = 0
    end_idx = -1
    for i in range(brace_start, len(content)):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    new_set_galerie = """setGalerie() {
        this.galeryGroup = new Nn;
        this.scene.add(this.galeryGroup);
        const cats = [
            { id: "gelinlik", name: "Gelinlik", texture: "cat_1_l", path: "/gallery/gelinlik" },
            { id: "tesettur", name: "Tesettür Gelinlik", texture: "cat_1_r", path: "/gallery/tesettur" },
            { id: "akesim", name: "A-Kesim Gelinlik", texture: "cat_2_l", path: "/gallery/akesim" },
            { id: "prenses", name: "Prenses Gelinlik", texture: "cat_2_r", path: "/gallery/prenses" },
            { id: "helen", name: "Helen Gelinlik", texture: "cat_3_l", path: "/gallery/helen" },
            { id: "balik", name: "Balık Gelinlik", texture: "cat_3_r", path: "/gallery/balik" },
            { id: "nikah", name: "Nikah Elbisesi", texture: "cat_4_l", path: "/gallery/nikah" },
            { id: "buyukbeden", name: "Büyük Beden", texture: "cat_4_r", path: "/gallery/buyukbeden" }
        ];
        this.cadres = [];
        this.btns = [];
        this.links = [];
        
        cats.forEach((cat, index) => {
            const isLeft = index % 2 === 0;
            const xPos = isLeft ? 1 : -1;
            const zPos = 1 - Math.floor(index / 2) * 2 - 2;
            const yRot = isLeft ? -0.2 : 0.2;
            
            // Fast reliable texture lookup bypassing CORS
            let tex = this.ressources.items[cat.texture] || this.ressources.items[cat.id];
            if (!tex) {
                 tex = this.ressources.loaders.textureLoader.load('/textures/oeuvre.png');
                 tex.colorSpace = 'srgb';
            }
            
            const i = new th(new P(xPos, 1.2, zPos), new P(0, yRot, 0), 1.5, tex, cat.name);
            const s = new dc(i.instance);
            const mockArticle = { uid: cat.id, data: { category: cat.id, article_title: [{text: cat.name}] } };
            const o = new Sb(i.instance, s, mockArticle);
            
            this.cadres.push(i);
            this.btns.push(s);
            this.links.push(o);
            this.galeryGroup.add(i.instance);
        });
        
        setTimeout(() => {
            document.querySelectorAll(".link_galerie").forEach((el, idx) => {
                if (cats[idx]) {
                    const textEl = el.querySelector("p, span, h2");
                    if (textEl) textEl.textContent = cats[idx].name;
                    el.href = cats[idx].path;
                }
            });
        }, 1000);
    }"""
    if end_idx != -1:
        # Avoid duplicating `setGalerie` by finding the exact brace start and replacing from there
        content = content[:brace_start] + new_set_galerie[13:] + content[end_idx:]

# 3. Patch bb (Gallery)
bb_start = content.find("class bb {\\n        constructor")
if bb_start == -1: bb_start = content.find("class bb{\\nconstructor")
if bb_start == -1: bb_start = content.find("class bb{constructor")
if bb_start == -1: bb_start = content.find("class bb")

if bb_start != -1:
    const_start = content.find("constructor(e)", bb_start)
    if const_start != -1:
        brace_start = content.find("{", const_start)
        depth = 0
        end_idx = -1
        for i in range(brace_start, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break
        new_bb_const = """constructor(e) {
        this.experience = new Rt;
        this.scene = this.experience.scene;
        this.ressources = this.experience.resources || this.experience.ressources;
        this.time = this.experience.time;
        this.camera = this.experience.camera.instance;
        this.group = new Nn;
        this.scene.add(this.group);
        this.cadres = [];
        this.btns = [];
        this.links = [];
        this.fromGallery = e;

        let filterStr = null;
        if (this.experience.router.activeCategory && this.experience.router.activeCategory !== "ALL") {
            filterStr = this.experience.router.activeCategory;
        }

        this.articles = [...this.experience.router.articles];
        
        if (filterStr && filterStr !== "ALL" && filterStr.length > 2) {
            const lf = filterStr.toLowerCase();
            this.articles = this.articles.filter(a => {
                const ac = a.data.category ? a.data.category.toLowerCase() : "";
                const ai = a.uid ? a.uid.toLowerCase() : "";
                return ac.includes(lf) || ai.includes(lf);
            });
        }

        this.articles = this.articles.slice(-15).reverse();

        let zObj = -0.5;
        this.articles.forEach((t, n) => {
            const xObj = n % 2 === 0 ? 1.5 : -1.5;
            zObj -= 2.5;
            const yRot = n % 2 === 0 ? -0.2 : 0.2;
            
            let tx = this.ressources ? this.ressources.items[t.uid] : null;
            if (!tx && t.data && t.data.article_image) {
                // Ignore CORS locally
                tx = this.ressources.loaders.textureLoader.load('/textures/oeuvre.png');
                tx.colorSpace = 'srgb';
            }

            const i = new th(new P(xObj, 1.2, zObj), new P(0, yRot, 0), 1.5, tx, t.uid);
            const s = new dc(i.instance);
            const o = new Sb(i.instance, s, t);
            this.cadres.push(i);
            this.btns.push(s);
            this.links.push(o);
        });
        
        this.group.add(...this.cadres.map(c => c.instance));
    }"""
        if end_idx != -1:
            content = content[:const_start] + new_bb_const + content[end_idx:]

# 4. Patch Lb (Menu) - Only overwrite the constructor, keep the methods!
lb_start = content.find("class Lb")
if lb_start != -1:
    lb_const_start = content.find("constructor()", lb_start)
    if lb_const_start != -1:
        brace_start = content.find("{", lb_const_start)
        depth = 0
        end_idx = -1
        for i in range(brace_start, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break
        
        new_lb_const = """constructor() {
        this.experience = new Rt;
        this.renderer = this.experience.renderer.instance;
        this.time = this.experience.time;
        this.camera = this.experience.camera.instance;
        this.scene = this.experience.scene;
        this.isOpen = !1;
        this.linkannim = [];
        this.isClickable = !1;
        this.contactButton = document.querySelector(".menu_contact");
        this.instaButton = document.querySelector(".menu_insta");
        this.contactButton.addEventListener("mouseenter", () => { this.contactButton.style.opacity = "1" });
        this.instaButton.addEventListener("mouseenter", () => { this.instaButton.style.opacity = "1" });
        this.contactButton.addEventListener("mouseleave", () => { this.contactButton.style.opacity = "0.6" });
        this.instaButton.addEventListener("mouseleave", () => { this.instaButton.style.opacity = "0.6" });
        this.contactButton.addEventListener("click", () => {
            const s = "info@minalidya.com", o = "Mina Lidya Randevu", a = `Merhaba,\\nTasarımlarınız hakkında bilgi almak istiyorum.\\n\\n`; 
            const l = `mailto:${s}?subject=${encodeURIComponent(o)}&body=${encodeURIComponent(a)}`; 
            window.location.href = l;
        });
        
        setTimeout(() => { this.isClickable = !0 }, 1500);

        this.linksContainer = document.querySelector(".menu_links ul");
        const cats = [
            { id: "all", label: "Tümü" },
            { id: "gelinlik", label: "Gelinlik" },
            { id: "tesettur", label: "Tesettür Gelinlik" },
            { id: "akesim", label: "A-Kesim Gelinlik" },
            { id: "prenses", label: "Prenses Gelinlik" },
            { id: "helen", label: "Helen Gelinlik" },
            { id: "balik", label: "Balık Gelinlik" },
            { id: "nikah", label: "Nikah Elbisesi" },
            { id: "buyukbeden", label: "Büyük Beden" }
        ];

        const homeCats = document.querySelector(".home_cats");
        const galleryCats = document.querySelector(".gallery_cats");
        
        const createCatLinks = (container) => {
            if(!container) return;
            container.innerHTML = cats.map(c => `<li><a href="#" data-cat="${c.id}" class="cat_link">${c.label}</a></li>`).join("");
            container.querySelectorAll("a").forEach(a => {
                a.addEventListener("click", e => {
                    e.preventDefault();
                    document.querySelectorAll('.cat_link').forEach(l => l.style.opacity = '0.5');
                    document.querySelectorAll(`.cat_link[data-cat="${a.dataset.cat}"]`).forEach(m => m.style.opacity = '1');
                    if (this.refreshProducts) this.refreshProducts(a.dataset.cat);
                });
            });
        };
        createCatLinks(homeCats);
        createCatLinks(galleryCats);

        this.refreshProducts = (categoryId = "all") => {
            if (!this.linksContainer) return;
            this.linksContainer.innerHTML = "";
            let filteredProps = this.experience.router.articles || [];
            if (categoryId !== "all") {
                filteredProps = filteredProps.filter(s => {
                    const catName = s.data && s.data.category ? s.data.category.toLowerCase() : "";
                    const idName = s.uid ? s.uid.toLowerCase() : "";
                    return catName.includes(categoryId) || idName.includes(categoryId);
                });
            }
            
            filteredProps.forEach(s => {
                const title = s.data && s.data.article_title && s.data.article_title[0] ? s.data.article_title[0].text : s.uid;
                this.linksContainer.innerHTML += `<li><a href='/gallery/${s.uid}'>${title}</a><div class='menu_links_hover'></div></li>`;
            });
            document.querySelectorAll(".menu_links_hover").forEach(s => s.style.opacity = "0");
            if (this.initLinkHoverVideo) this.initLinkHoverVideo();
        };

        const e_btn = document.querySelector(".menu_close"), t_btn = document.querySelector(".menu_open"); 
        if (e_btn) e_btn.addEventListener("click", this.toggleButton.bind(this));
        if (t_btn) t_btn.addEventListener("click", this.toggleButton.bind(this));
        
        window.addEventListener("keydown", s => { s.code === "Escape" && this.toggleButton() });
        this.inputField = document.querySelector(".search_bar input");
        if (this.inputField) this.inputField.addEventListener("input", this.filterLinks.bind(this));
        
        this.refreshProducts("all");
        
        he.fromTo(".menu_open button", { y: "100%" }, { y: "0%", duration: .3, ease: "sine.inOut", delay: 1 });
        this.updateActiveLink();
        this.activeLinkIndex = 0;
        
        window.addEventListener("keydown", s => { 
            const o = document.querySelector(".search_bar input");
            const a = /^[a-zA-Z0-9]$/; 
            if (document.activeElement === o && a.test(s.key) || !this.isOpen) return; 
            const n = Array.from(document.querySelectorAll(".menu_links ul li"));
            const i = Array.from(document.querySelectorAll(".menu_main_links span")); 
            this.menuLinksArray = [...i, ...n];
            const l = this.menuLinksArray.filter(f => f.style.display !== "none"); 
            if (!l.length) return; 
            
            const c = f => { f.dispatchEvent(new Event("mouseenter")) };
            const h = f => { f.dispatchEvent(new Event("mouseleave")) }; 
            
            if (s.key === "Enter") { 
                const f = l[this.activeLinkIndex].querySelector("a"); 
                if (f) { f.click(); s.preventDefault(); return; }
            } 
            
            let changed = false;
            switch (s.code) { 
                case "ArrowDown": case "ArrowRight": case "KeyS": case "KeyD": 
                    this.activeLinkIndex = (this.activeLinkIndex + 1) % l.length; 
                    changed = true;
                    break; 
                case "ArrowUp": case "ArrowLeft": case "KeyW": case "KeyA": 
                    this.activeLinkIndex = (this.activeLinkIndex - 1 + l.length) % l.length; 
                    changed = true;
                    break;
            }
            if (changed) {
                l.forEach((f, _) => { 
                    const g = _ === 0 || _ === 1; 
                    if (_ === this.activeLinkIndex) {
                        c(f);
                        if (g && f.querySelector("a")) f.querySelector("a").style.opacity = .2;
                        else if (f.querySelector(".menu_links_hover")) f.querySelector(".menu_links_hover").style.display = "block";
                    } else {
                        h(f);
                        if (g && f.querySelector("a")) f.querySelector("a").style.opacity = 1;
                        else if (f.querySelector(".menu_links_hover")) f.querySelector(".menu_links_hover").style.display = "none";
                    } 
                });
                s.preventDefault();
            }
        });
    }"""
        if end_idx != -1:
            content = content[:lb_const_start] + new_lb_const + content[end_idx:]

# 5. Patch Video Playback AbortError
play_old = 'play().catch(l=>console.warn("Erreur lecture vid\\xe9o:",l))'
play_new = 'play().catch(l=>{if(l.name!=="AbortError")console.warn("Erreur lecture vidéo:",l)})'
content = content.replace(play_old, play_new)

# 6. Loader safety
loader_old = 'setTimeout(()=>{this.loaded<this.toLoad&&(this.trigger("ready"),console.warn("Loader timeout"))},1e4)'
loader_new = 'setTimeout(()=>{if(this.loaded<this.toLoad){console.warn("Loader safety");this.trigger("ready");}},5000)'
content = content.replace(loader_old, loader_new)

with open(dst, "w", encoding="utf-8") as f:
    f.write(content)

print("Master patch applied successfully!")
