
import os
import re

filepath = r'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Loader Hang in hE.init
# Move trigger("ready") to be more robust, and handle potential Prismic timeouts.
# We'll make the Prismic fetch optional for the loader to finish.

init_search = r'async init\(\) \{.*?try \{.*?\}\s+catch \(t\) \{.*?\}\s+this\.trigger\("ready"\)'
# Actually let's just find the start and end of the try block.

# We'll replace the whole hE.init method body for predictability.
hE_init_new_body = """
	async init() {
		try {
			// Load local products.json first as it is reliable
			const response = await fetch('/assets/products.json').catch(e => null);
			if (response && response.ok) {
				const rawProducts = await response.json();
				this.allProducts = rawProducts.map(p => ({
					uid: p.id.toString(),
					id: p.id.toString(),
					data: {
						article_title: [{ text: p.title.tr || p.productName }],
						article_image: { url: p.image },
						title: p.title.tr || p.productName,
						short_desc: (p.shortDescription && p.shortDescription.tr) ? p.shortDescription.tr.replace(/<[^>]*>?/gm, '').substring(0, 150) + '...' : "",
						etek_kesimi: p.mappedAttributes ? (p.mappedAttributes["Etek Kesimi"] || "-") : "-",
						kumas: p.mappedAttributes ? (p.mappedAttributes["Kumaş"] || "-") : "-",
						url: `https://minalidya.wedding/urun/${p.slug}`,
						category: p.category ? p.category[0] : "",
						isModest: p.isModest
					},
					first_publication_date: (p.updatedAt || new Date().toISOString())
				}));
				this.prismicCache.articles = this.allProducts;
				this.articles = this.allProducts;
			}

			// Map home page categories
			const homeCats = {
				"cat_1_l": { name: "Gelinlik", cat: "gelinlik", modest: false },
				"cat_1_r": { name: "Tesettür Gelinlik", cat: "gelinlik", modest: true },
				"cat_2_l": { name: "Nişanlık", cat: "nisanlik" },
				"cat_2_r": { name: "Kınalık", cat: "kinalik" },
				"cat_3_l": { name: "Söz", cat: "soz-elbisesi" },
				"cat_3_r": { name: "After Party", cat: "after-party" },
				"cat_4_l": { name: "Kaftan", cat: "kaftan" },
				"cat_4_r": { name: "Abiye", cat: "abiye" }
			};

			Object.entries(homeCats).forEach(([uid, info]) => {
				this.prismicCache[uid] = {
					uid: uid,
					title: info.name,
					data: {
						article_title: [{ text: info.name }],
						article_image: { url: `/kategori/${uid.replace('_', ' ')}.png`.replace('cat 1 l', '1 sol gelinlik').replace('cat 1 r', '1 sag tesettur gelinlik').replace('cat 2 l', '2 sol nisanlik').replace('cat 2 r', '2 sag kinalik').replace('cat 3 l', '3 sol soz').replace('cat 3 r', '3 sag after').replace('cat 4 l', '4 sol kaftan').replace('cat 4 r', '4 sag abiye') },
						title: info.name,
						short_desc: `${info.name} koleksiyonu.`
					}
				};
			});

			// Optional Prismic fetch in background or with timeout to avoid loader hang
			const prismicFetch = async () => {
				try {
					const t = ["home", "about", "gallery"];
					for (const n of t) {
						const i = await this.client.getByType(n, { pageSize: 100 }).catch(e => null);
						if(i) this.prismicCache[n] = i.results || [];
					}
				} catch(e) {}
			};
			prismicFetch();

		} catch (t) {
			console.error("Erreur récupération des données :", t)
		}
		this.trigger("ready");
		this.handleLocation();
	}
"""

content = re.sub(r'async init\(\) \{.*?this\.trigger\("ready"\), this\.handleLocation\(\)\s+\}', hE_init_new_body, content, flags=re.DOTALL)

# 2. Refactor Lb class for menu nesting
# We need to update selectCategory and refreshLinks

new_select_category = """
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
		this.experience.router.filterProducts(n);
        // Navigate to gallery if we are filtering
        if (window.location.pathname !== "/gallery") {
            window.history.pushState({}, "", "/gallery");
            this.experience.router.handleLocation();
        }
		this.refreshLinks();
	}
"""

content = re.sub(r'selectCategory\(e\) \{.*?\}', new_select_category, content, flags=re.DOTALL)

new_refresh_links = """
	refreshLinks() {
		const subContainers = document.querySelectorAll(".submenu_container");
		subContainers.forEach(c => {
			c.innerHTML = "";
			const categories = [
				{ id: "gelinlik", name: "Gelinlik" },
				{ id: "tesettur-gelinlik", name: "Tesettür Gelinlik" },
				{ id: "nisanlik", name: "Nişanlık" },
				{ id: "kinalik", name: "Kınalık" },
				{ id: "soz", name: "Söz" },
				{ id: "after-party", name: "After Party" },
				{ id: "kaftan", name: "Kaftan" },
				{ id: "abiye", name: "Abiye" }
			];
			categories.forEach(cat => {
				const a = document.createElement("a");
				a.href = "#";
				a.setAttribute("data-category", cat.id);
				a.innerText = cat.name;
				if (this.experience.router.activeCategory === cat.name) a.classList.add("active");
				a.addEventListener("click", (e) => {
					e.preventDefault();
					this.selectCategory(cat.id);
				});
				c.appendChild(a);
			});
		});

		this.linksContainer.innerHTML = "";
		this.experience.router.articles.forEach(s => {
			const t = (s.data && s.data.article_title && s.data.article_title[0]) ? s.data.article_title[0].text : (s.data ? s.data.title : s.uid);
			this.linksContainer.innerHTML += `<li><a href='/gallery/${s.uid}'>${t}</a><div class ='menu_links_hover'></div></li>`
		});

		this.menuLinks = document.querySelectorAll(".menu_links ul li");
		this.initLinkHoverVideo();
		this.updateActiveLink();
		this.activeLinkIndex = 0;
		const mainLinks = Array.from(document.querySelectorAll(".menu_main_links .menu_group span"));
		const prodLinks = Array.from(document.querySelectorAll(".menu_links ul li"));
		this.menuLinksArray = [...mainLinks, ...prodLinks];
	}
"""

content = re.sub(r'refreshLinks\(\) \{.*?this\.menuLinksArray = \[\.\.\.t, \.\.\.e\]\s+\}', new_refresh_links, content, flags=re.DOTALL)

# 3. Update wb class (Single Product Page) layout
# User wants: Top Left -> Title & Hem Cut. Bottom Left -> Fabric.
new_wb_setHtml = """
	setHtml() {
		const e = document.querySelector(".data_top"), t = document.querySelector(".data_bottom");
		e.innerHTML = ""; t.innerHTML = "";
		const { article_title: n, etek_kesimi: ek, kumas: km } = this.article.data;
		
		// Title and Hem Cut in Top Left
		if (n && n.length && n[0].text) {
			e.innerHTML += `<li><span><span><strong>${n[0].text}</strong></span></span></li>`;
		}
		if (ek && ek !== "-") {
			e.innerHTML += `<li><span><span>${ek}</span></span></li>`;
		}

		// Fabric in Bottom Left
		if (km && km !== "-") {
			t.innerHTML += `<li><span><span>${km}</span></span></li>`;
		}

		const h = document.querySelector(".article_arrows .arrowL a"), 
              u = document.querySelector(".article_arrows .arrowR a"),
              prevIdx = this.index !== 0 ? this.index - 1 : this.experience.articles.length - 1,
              nextIdx = this.index !== this.experience.articles.length - 1 ? this.index + 1 : 0,
              d = this.experience.articles[prevIdx],
              f = this.experience.articles[nextIdx];
		if(h && d) h.setAttribute("href", `/gallery/${d.uid}`);
		if(u && f) u.setAttribute("href", `/gallery/${f.uid}`);
	}
"""

content = re.sub(r'setHtml\(\) \{.*?u\.setAttribute\("href", `/gallery/\${f\.uid}`\)\s+\}', new_wb_setHtml, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied JS fixes for Loader, Menu Nesting, and Product Layout")
