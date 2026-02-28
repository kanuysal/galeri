
import os

filepath = r'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add refreshProducts to bb class
search = '} update() { this.init || (this.setCamPos(), this.init = !0), this.updateGalleryCam() }'
if search in content:
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
    new_content = refresh_products_code + search
    content = content.replace(search, new_content)
    print("Added refreshProducts to bb class")
else:
    print("Could not find insertion point for refreshProducts in bb")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
