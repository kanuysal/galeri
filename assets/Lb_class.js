class Lb {
	constructor() {
		this.experience = new Rt, this.renderer = this.experience.renderer.instance, this.time = this.experience.time, this.camera = this.experience.camera.instance, this.scene = this.experience.scene, this.isOpen = !1, this.linkannim = [], this.isClickable = !1, this.contactButton = document.querySelector(".menu_contact"), this.instaButton = document.querySelector(".menu_insta"), this.contactButton.addEventListener("mouseenter", () => { this.contactButton.style.opacity = "1" }), this.instaButton.addEventListener("mouseenter", () => { this.instaButton.style.opacity = "1" }), this.contactButton.addEventListener("mouseleave", () => { this.contactButton.style.opacity = "0.6" }), this.instaButton.addEventListener("mouseleave", () => { this.instaButton.style.opacity = "0.6" }), this.contactButton.addEventListener("click", () => {
			const s = "etienne.dault@gmail.com", o = "Contact regarding your artworks", a = `  Hello,
                            I’m reaching out after discovering your work on your website. I’m interested in learning more about your available artworks.
                            Kind regards,

                        `, l = `mailto:${s}?subject=${encodeURIComponent(o)}&body=${encodeURIComponent(a)}`; window.location.href = l
		}), setTimeout(() => { this.isClickable = !0 }, 1500), this.linksContainer = document.querySelector(".menu_links ul"), this.linksContainer.innerHTML = "",

			this.categoryLinks = document.querySelectorAll(".menu_categories li a"),
			this.categoryLinks.forEach(s => {
				s.addEventListener("click", t => {
					t.preventDefault();
					const n = s.getAttribute("data-category");
					this.selectCategory(n)
				})
			}),

			this.refreshLinks();

		const e = document.querySelector(".menu_close"), t = document.querySelector(".menu_open"); e.addEventListener("click", this.toggleButton.bind(this)), t.addEventListener("click", this.toggleButton.bind(this)), window.addEventListener("keydown", s => { s.code === "Escape" && this.toggleButton() }), this.inputField = document.querySelector(".search_bar input"),
			this.inputField.addEventListener("input", this.filterLinks.bind(this)),
			he.fromTo(".menu_open button", { y: "100%" }, { y: "0%", duration: .3, ease: "sine.inOut", delay: 1 }), this.updateActiveLink(), this.activeLinkIndex = 0;

		window.addEventListener("keydown", s => { var u, d; const o = document.querySelector(".search_bar input"), a = /^[a-zA-Z0-9]$/; if (document.activeElement === o && a.test(s.key) || !this.isOpen) return; const l = this.menuLinksArray.filter(f => f.style.display !== "none"); if (!l.length) return; const c = f => { f.dispatchEvent(new Event("mouseenter")) }, h = f => { f.dispatchEvent(new Event("mouseleave")) }; if (s.key === "Enter") { const f = l[this.activeLinkIndex].querySelector("a"); f && f.click(), s.preventDefault() } switch (s.code) { case "ArrowDown": case "ArrowRight": case "KeyS": case "KeyD": this.activeLinkIndex = (this.activeLinkIndex + 1) % l.length; break; case "ArrowUp": case "ArrowLeft": case "KeyW": case "KeyA": this.activeLinkIndex = (this.activeLinkIndex - 1 + l.length) % l.length; break; case "Enter": (d = (u = l[this.activeLinkIndex]) == null ? void 0 : u.querySelector("a")) == null || d.click(); break; default: return }l.forEach((f, _) => { const g = _ === 0 || _ === 1; _ === this.activeLinkIndex ? (c(f), g ? f.querySelector("a").style.opacity = .2 : f.querySelector(".menu_links_hover").style.display = "block") : (h(f), g ? f.querySelector("a").style.opacity = 1 : f.querySelector(".menu_links_hover").style.display = "none") }), s.preventDefault() })
	}

	selectCategory(e) {
		const t = {
			"gelinlik": "Gelinlik",
			"tesettur-gelinlik": "Tesettür Gelinlik",
			"nisanlik": "Nişanlık",
			"kinalik": "Kınalık",
			"soz": "Söz",
			"after-party": "After Party",
			"kaftan": "Kaftan",
			"abiye": "Abiye"
		};
		const n = t[e] || "ALL";
		this.experience.router.filterProducts(n),
			this.categoryLinks.forEach(i => {
				i.getAttribute("data-category") === e ? i.classList.add("active") : i.classList.remove("active")
			}),
			this.refreshLinks()
	}

	refreshLinks() {
		this.linksContainer.innerHTML = "",
			this.experience.router.articles.forEach(s => {
				const t = (s.data && s.data.article_title && s.data.article_title[0]) ? s.data.article_title[0].text : (s.data ? s.data.title : s.uid);
				this.linksContainer.innerHTML += `<li><a href='/gallery/${s.uid}'>${t}</a><div class ='menu_links_hover'></div></li>`
			}),
			document.querySelectorAll(".menu_links_hover").forEach(s => s.style.opacity = "0"),
			this.menuLinks = document.querySelectorAll(".menu_links ul li"),
			this.initLinkHoverVideo(),
			this.updateActiveLink();
		const e = Array.from(document.querySelectorAll(".menu_links ul li")),
			t = Array.from(document.querySelectorAll(".menu_main_links span"));
		this.menuLinksArray = [...t, ...e]
	}

	updateActiveLink() { const e = window.location.pathname, t = document.querySelectorAll(".menu_links