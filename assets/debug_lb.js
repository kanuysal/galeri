class Lb {
	constructor() {
		this.experience = new Rt, this.renderer = this.experience.renderer.instance, this.time = this.experience.time, this.camera = this.experience.camera.instance, this.scene = this.experience.scene, this.isOpen = !1, this.linkannim = [], this.isClickable = !1, this.contactButton = document.querySelector(".menu_contact"), this.instaButton = document.querySelector(".menu_insta"), this.contactButton.addEventListener("mouseenter", () => { this.contactButton.style.opacity = "1" }), this.instaButton.addEventListener("mouseenter", () => { this.instaButton.style.opacity = "1" }), this.contactButton.addEventListener("mouseleave", () => { this.contactButton.style.opacity = "0.6" }), this.instaButton.addEventListener("mouseleave", () => { this.instaButton.style.opacity = "0.6" }), this.contactButton.addEventListener("click", () => {
			const s = "etienne.dault@gmail.com", o = "Contact regarding your artworks", a = `  Hello,
                            I’m reaching out after discovering your work on your website. I’m interested in learning more about your available artworks.
                            Kind regards,

                        `, l = `mailto:${s}?subject=${encodeURIComponent(o)}&body=${encodeURIComponent(a)}`; window.location.href = l
		}), setTimeout(() => { this.isClickable = !0 }, 1500), 
        
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
            let filteredProps = this.experience.articles;
            if (categoryId !== "all") {
                filteredProps = this.experience.articles.filter(s => {
                    const catName = s.data.category ? s.data.category.toLowerCase() : "";
                    const idName = s.uid ? s.uid.toLowerCase() : "";
                    return catName.includes(categoryId) || idName.includes(categoryId);
                });
            }
            
            filteredProps.forEach(s => {
                const title = s.data.article_title && s.data.article_title[0] ? s.data.article_title[0].text : s.uid;
                this.linksContainer.innerHTML += `<li><a href='/gallery/${s.uid}'>${title}</a><div class='menu_links_hover'></div></li>`;
            });
            
            document.querySelectorAll(".menu_links_hover").forEach(s => s.style.opacity = "0");
            this.initLinkHoverVideo();
        };
        
        this.refreshProducts("all");
 const e = document.querySelector(".menu_close"), t = document.querySelector(".menu_open"); e.addEventListener("click", this.toggleButton.bind(this)), t.addEventListener("click", this.toggleButton.bind(this)), window.addEventListener("keydown", s => { s.code === "Escape" && this.toggleButton() }), this.inputField = document.querySelector(".search_bar input"), this.menuLinks = document.querySelectorAll(".menu_links ul li"), this.inputField.addEventListener("input", this.filterLinks.bind(this)), this.initLinkHoverVideo(), he.fromTo(".menu_open button", { y: "100%" }, { y: "0%", duration: .3, ease: "sine.inOut", delay: 1 }), this.updateActiveLink(), this.activeLinkIndex = 0; const n = Array.from(document.querySelectorAll(".menu_links ul li")), i = Array.from(document.querySelectorAll(".menu_main_links span")); this.menuLinksArray = [...i, ...n], window.addEventListener("keydown", s => { var u, d; const o = document.querySelector(".search_bar input"), a = /^[a-zA-Z0-9]$/; if (document.activeElement === o && a.test(s.key) || !this.isOpen) return; const l = this.menuLinksArray.filter(f => f.style.display !== "none"); if (!l.length) return; const c = f => { f.dispatchEvent(new Event("mouseenter")) }, h = f => { f.dispatchEvent(new Event("mouseleave")) }; if (s.key === "Enter") { const f = l[this.activeLinkIndex].querySelector("a"); f && f.click(), s.preventDefault() } switch (s.code) { case "ArrowDown": case "ArrowRight": case "KeyS": case "KeyD": this.activeLinkIndex = (this.activeLinkIndex + 1) % l.length; break; case "ArrowUp": case "ArrowLeft": case "KeyW": case "KeyA": this.activeLinkIndex = (this.activeLinkIndex - 1 + l.length) % l.length; break; case "Enter": (d = (u = l[this.activeLinkIndex]) == null ? void 0 : u.querySelector("a")) == null || d.click(); break; default: return }l.forEach((f, _) => { const g = _ === 0 || _ === 1; _ === this.activeLinkIndex ? (c(f), g ? f.querySelector("a").style.opacity = .2 : f.querySelector(".menu_links_hover").style.display = "block") : (h(f), g ? f.querySelector("a").style.opacity = 1 : f.querySelector(".menu_links_hover").style.display = "none") }), s.preventDefault() })
	}