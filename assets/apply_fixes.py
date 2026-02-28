
import os

filepath = r'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add refreshProducts to bb class
# We find where bb class ends or inside it.
# bb ends with "} class wb"
bb_search = "this.updateGalleryCam() } update() { this.init || (this.setCamPos(), this.init = !0), this.updateGalleryCam() } resize() { this.setCamPos() } destroy() {"
if bb_search in content:
    refresh_products_code = """
	refreshProducts() {
		this.cadres.forEach(c => c.destroy());
		this.btns.forEach(b => b.destroy());
		this.links.forEach(l => l.destroy());
		this.cadres = [];
		this.btns = [];
		this.links = [];
		this.articles = this.experience.router.articles;
		this.size = this.articles.length * 1.2 + 12;
		this.articles.forEach((t, n) => {
			const i = new th(new P(1.2 + n * 1.2, .99 + n % 2 * .99, -.5), new P(0, 0, 0), 1.5, this.experience.ressources.items[t.uid], t.uid),
				s = new dc(i.instance),
				o = new Sb(i.instance, s, t);
			this.cadres.push(i), this.btns.push(s), this.links.push(o)
		});
		if (this.roomGroup) {
			this.scene.remove(this.roomGroup);
			this.setRoom();
		}
		if (this.p1) {
			[this.p1, this.p2, this.p3, this.p4].forEach(p => { 
                if(p) { this.scene.remove(p); if(p.geometry) p.geometry.dispose(); if(p.material) p.material.dispose(); }
            });
			this.setPanneaux();
		}
	}
    """
    new_bb_content = refresh_products_code + bb_search
    content = content.replace(bb_search, new_bb_content)
    print("Added refreshProducts to bb class")
else:
    print("Could not find insertion point for refreshProducts in bb")

# 2. Update ub class (Homepage links) to handle categories
ub_search = 'this.link.addEventListener("click", i => { i.preventDefault(), this.experience.world.page.needTransition = !0, this.link.style.opacity = "0", this.experience.router.route(i) })'
if ub_search in content:
    ub_replacement = 'this.link.addEventListener("click", i => { i.preventDefault(), this.experience.world.page.needTransition = !0, this.link.style.opacity = "0", this.article.uid.startsWith("cat_") ? (this.experience.router.filterProducts(this.article.uid), window.history.pushState({}, "", "/gallery"), this.experience.router.handleLocation()) : this.experience.router.route(i) })'
    content = content.replace(ub_search, ub_replacement)
    print("Updated ub class click handler")
else:
    print("Could not find click handler in ub class")

# 3. Update ub touchstart (same logic for mobile)
ub_touch_search = 'this.link.addEventListener("touchstart", i => { i.preventDefault(), this.experience.world.page.needTransition = !0, this.link.style.opacity = "0", this.experience.router.route(i) })'
if ub_touch_search in content:
    ub_touch_replacement = 'this.link.addEventListener("touchstart", i => { i.preventDefault(), this.experience.world.page.needTransition = !0, this.link.style.opacity = "0", this.article.uid.startsWith("cat_") ? (this.experience.router.filterProducts(this.article.uid), window.history.pushState({}, "", "/gallery"), this.experience.router.handleLocation()) : this.experience.router.route(i) })'
    content = content.replace(ub_touch_search, ub_touch_replacement)
    print("Updated ub class touchstart handler")
else:
    print("Could not find touchstart handler in ub class")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
