
import re

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Loader fix (hE.init)
# Find: .catch(e=>console.error(e))
# Add: .finally(()=>this.readyState()) or similar
print("Patching hE.init...")
content = re.sub(
    r'\.catch\(([a-z])=>console\.error\(\1\)\)',
    r'.catch(\1=>console.error(\1)).finally(()=>this.ready())',
    content
)

# 2. Video Playback Error Fix (AbortError)
# Find: n.play().catch(l=>console.warn("Erreur lecture vidéo:",l))
print("Patching Video Playback...")
video_pattern = r'([a-z])\.play\(\)\.catch\(([a-z])=>console\.warn\("Erreur lecture vidéo:",\2\)\)'
video_replacement = r'((playPromise=\1.play())!==undefined?playPromise.catch(\2=>{if(\2.name!=="AbortError")console.warn("Erreur lecture vidéo:",\2)}):null)'
# We need to make sure playPromise is defined.
# A safer way in minified code:
content = re.sub(
    video_pattern,
    r'{let p=\1.play();if(p!==undefined)p.catch(\2=>{if(\2.name!=="AbortError")console.warn("Erreur lecture vidéo:",\2)})}',
    content
)

# 3. Lb Class - Menu Nesting & Submenus
# We need to replace the entire Lb constructor and methods or at least the relevant parts.
# Since it's minified, it's safer to replace the whole class if we have it?
# Actually, I have the refactored Lb class from previous work.
# Let's find "class Lb{" and replace until "}"
print("Patching Lb class...")
# I'll use the one I wrote before.

lb_replacement = """class Lb {
    constructor() {
        this.experience = new Rt,
        this.renderer = this.experience.renderer.instance,
        this.time = this.experience.time,
        this.camera = this.experience.camera.instance,
        this.scene = this.experience.scene,
        this.isOpen = !1,
        this.isClickable = !1,
        this.contactButton = document.querySelector(".menu_contact"),
        this.instaButton = document.querySelector(".menu_insta"),
        this.contactButton.addEventListener("click", () => {
            window.location.href = "mailto:etienne.dault@gmail.com"
        }),
        setTimeout(() => { this.isClickable = !0 }, 1500),
        this.linksContainer = document.querySelector(".menu_links ul"),
        this.inputField = document.querySelector(".search_bar input"),
        this.inputField.addEventListener("input", this.filterLinks.bind(this)),
        this.initLinkHoverVideo(),
        this.refreshLinks(),
        document.querySelector(".menu_open").addEventListener("click", this.open.bind(this)),
        document.querySelector(".menu_close").addEventListener("click", this.close.bind(this))
    }
    refreshLinks() {
        this.linksContainer.innerHTML = "";
        const cats = ["Gelinlik", "Tesettür Gelinlik", "Abiye", "Kaftan", "Nişanlık", "After Party", "Söz & Nişan", "Kınalık"];
        const homeCats = document.querySelector(".home_cats");
        const galleryCats = document.querySelector(".gallery_cats");
        if (homeCats) {
            homeCats.innerHTML = cats.map(c => `<a href="#" data-cat="${c}">${c}</a>`).join("");
            homeCats.querySelectorAll("a").forEach(a => {
                a.addEventListener("click", (e) => {
                    e.preventDefault();
                    this.selectCategory(a.dataset.cat);
                });
            });
        }
        if (galleryCats) {
            galleryCats.innerHTML = cats.map(c => `<a href="#" data-cat="${c}">${c}</a>`).join("");
            galleryCats.querySelectorAll("a").forEach(a => {
                a.addEventListener("click", (e) => {
                    e.preventDefault();
                    this.selectCategory(a.dataset.cat);
                });
            });
        }
        this.experience.articles.forEach(s => {
            const t = (s.data && s.data.article_title && s.data.article_title[0]) ? s.data.article_title[0].text : s.uid;
            const li = document.createElement("li");
            li.innerHTML = `<a href='/gallery/${s.uid}'>${t}</a><div class='menu_links_hover'></div>`;
            li.querySelector("a").addEventListener("click", e => {
                e.preventDefault();
                this.experience.router.route(e);
            });
            this.linksContainer.appendChild(li);
        });
    }
    selectCategory(cat) {
        window.activeCategory = cat;
        if (this.experience.world.gallery) {
            this.experience.world.gallery.refreshProducts();
        }
        if (window.location.pathname !== "/gallery") {
            const fakeEvent = { preventDefault: () => {}, currentTarget: { getAttribute: () => "/gallery" } };
            this.experience.router.route(fakeEvent);
        }
        this.close();
    }
    filterLinks() {
        const e = this.inputField.value.toLowerCase();
        Array.from(this.linksContainer.children).forEach(t => {
            t.textContent.toLowerCase().includes(e) ? t.style.display = "block" : t.style.display = "none"
        });
    }
    initLinkHoverVideo() {
        const n = document.querySelector(".menu_video"),
              i = document.querySelector(".menu_image");
        if (this.experience.isPhone) { n && n.remove(); return; }
        this.linksContainer.querySelectorAll("li").forEach(s => {
            s.addEventListener("mouseenter", () => {
                const title = s.querySelector("a").textContent;
                const art = this.experience.articles.find(a => (a.data.article_title[0].text === title));
                if (art) {
                    i.src = art.data.article_image.url;
                    n.currentTime = 0;
                    let p = n.play();
                    if (p !== undefined) p.catch(error => { if (error.name !== "AbortError") console.warn(error); });
                }
            });
        });
    }
    open() {
        if (!this.isClickable || this.isOpen) return;
        this.isOpen = !0;
        he.to(".menu", { x: 0, duration: 0.5, ease: "power2.out" });
        if(this.experience.world.personnage) this.experience.world.personnage.controlsEnabled = !1;
    }
    close() {
        if (!this.isClickable || !this.isOpen) return;
        this.isOpen = !1;
        he.to(".menu", { x: "100%", duration: 0.5, ease: "power2.in" });
        if(this.experience.world.personnage) this.experience.world.personnage.controlsEnabled = !0;
    }
}"""

content = re.sub(r'class Lb\{.*?\}', lb_replacement.replace('\\', '\\\\').replace('$', '\\$'), content, flags=re.DOTALL)

# 4. bb class - Product limit (15) and refreshProducts
print("Patching bb class...")
# I'll replace the constructor part to limit articles.
# And add refreshProducts.

bb_constructor_pattern = r'class bb\{constructor\(([a-z])\)\{(.+?)this\.articles=this\.experience\.articles'
bb_constructor_replacement = r'class bb{constructor(\1){\2this.articles=this.experience.articles.slice(-15).reverse()'

content = re.sub(bb_constructor_pattern, bb_constructor_replacement, content, flags=re.DOTALL)

# Add refreshProducts before the end of class bb
refresh_products_code = """
    refreshProducts() {
        this.articles = this.experience.router.articles.slice(-15).reverse();
        this.cadres.forEach(c => this.scene.remove(c.instance));
        this.btns.forEach(b => this.scene.remove(b.group));
        this.links.forEach(l => l.destroy());
        this.cadres = []; this.btns = []; this.links = [];
        this.articles.forEach((t, n) => {
            const i = new th(new P(1.2 + n * 1.2, .99 + n % 2 * .99, -.5), new P(0, 0, 0), 1.5, this.experience.ressources.items[t.uid], t.uid);
            const s = new dc(i.instance);
            const o = new Sb(i.instance, s, t);
            this.cadres.push(i); this.btns.push(s); this.links.push(o);
        });
    }
"""
content = re.sub(r'(class bb\{.*?)(destroy\(\)\{)', r'\1' + refresh_products_code + r'\2', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patching complete.")
