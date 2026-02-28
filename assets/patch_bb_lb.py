import re

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# For class bb, let's find the constructor exactly
old_bb = r'class bb\s*\{\s*constructor\(e\)\s*\{.*?group\.add\(\.\.\.this\.cadres\.map\(c=>c\.instance\)\)\}'

new_bb = """class bb {
    constructor(e) {
        this.experience = new Rt;
        this.scene = this.experience.scene;
        this.ressources = this.experience.ressources;
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
            
            let tx = this.ressources.items[t.uid];
            if (!tx && t.data && t.data.article_image) {
                tx = new Pe().load(t.data.article_image.url);
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

content, count_bb = re.subn(old_bb, new_bb, content, flags=re.DOTALL | re.IGNORECASE)
print(f"Patched bb: {count_bb}")


# Apply Lb patch (Menu filtering logic)
old_lb = r'class Lb\s*\{\s*constructor\(\)\s*\{.*?\}\);\s*\}'
new_lb = """class Lb {
    constructor() {
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
                    this.refreshProducts(a.dataset.cat);
                });
            });
        };
        createCatLinks(homeCats);
        createCatLinks(galleryCats);

        this.refreshProducts = (categoryId = "all") => {
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
            this.initLinkHoverVideo();
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
content, count_lb = re.subn(old_lb, new_lb, content, flags=re.DOTALL)
print(f"Patched lb: {count_lb}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
