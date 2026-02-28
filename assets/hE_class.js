class hE extends io {
	constructor() {
		super();
		this.activeCategory = "ALL";
		this.allProducts = [];
		Ra(this, "route", t => { t = t || window.event, t.preventDefault(), this.prevRoute = this.path || window.location.pathname, window.history.pushState({}, "", t.currentTarget.href), this.handleLocation() }); Ra(this, "handleLocation", async () => { if (this.isRouting) return; this.isRouting = !0, this.path = window.location.pathname; let t = this.routes[this.path] || this.routes[404], n = null; const i = this.isArticleRoute(this.path); if (i) n = this.prismicCache[i] || null, t = "/pages/article.html"; else if (this.routes[this.path]) { const o = { "/": "home", "/about": "about", "/gallery": "gallery" }[this.path]; n = this.prismicCache[o] ? this.prismicCache[o][0] : null } if (this.htmlCache[t]) this.html = this.htmlCache[t]; else try { this.html = await fetch(t).then(s => { if (!s.ok) throw new Error("Page non trouvée"); return s.text() }), this.htmlCache[t] = this.html } catch (s) { console.error("Erreur fetch HTML :", s); try { this.html = await fetch(this.routes[404]).then(o => o.text()), this.htmlCache[this.routes[404]] = this.html } catch (o) { console.error("Impossible de fetch la 404", o), this.html = "<h1>404</h1>" } } this.prismicData = n, this.trigger("routing"), this.isRouting = !1, this.isPopState = !1 }); this.experience = new Rt, this.camera = this.experience.camera, this.canvas = this.experience.canvas, this.client = cE("ThevertMenthe"), this.htmlCache = {}, this.prismicCache = {}, this.path = null, this.prevRoute = window.location.pathname, this.isRouting = !1, this.isPopState = !1, this.routes = { 404: "/pages/404.html", "/": "/pages/home.html", "/about": "/pages/about.html", "/gallery": "/pages/gallery.html" }, window.addEventListener("popstate", t => { t.preventDefault(), this.isPopState = !0, this.route({ currentTarget: { href: window.location.href }, preventDefault: () => { } }, !0) }), this.init()
	} async init() {
		try {
			const t = ["home", "about", "gallery"];
			for (const n of t) {
				const i = await this.client.getByType(n, { pageSize: 100 });
				this.prismicCache[n] = i.results || []
			}

			// Load real products from assets/products.json
			const response = await fetch('/assets/products.json');
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

			// Re-map home page categories to standard uids for standard home logic
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

		} catch (t) {
			console.error("Erreur récupération des données :", t)
		}
		this.trigger("ready"), this.handleLocation()
	}
	filterProducts(category) {
		this.activeCategory = category;
		const homeMapping = {
			"cat_1_l": "Gelinlik",
			"cat_1_r": "Tesettür Gelinlik",
			"cat_2_l": "Nişanlık",
			"cat_2_r": "Kınalık",
			"cat_3_l": "Söz",
			"cat_3_r": "After Party",
			"cat_4_l": "Kaftan",
			"cat_4_r": "Abiye"
		};
		const targetCategory = homeMapping[category] || category;

		if (!targetCategory || targetCategory === "ALL" || targetCategory === "ANASAYFA") {
			this.articles = this.allProducts;
		} 