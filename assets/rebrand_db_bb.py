import os
import re

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# We found the block:
# setCadres() { const e = ["cat_1_l", "cat_1_r", "cat_2_l", "cat_2_r", "cat_3_l", "cat_3_r", "cat_4_l", "cat_4_r"]; this.cadresControllers.forEach((t, n) => { const uid = e[n % e.length]; const data = this.experience.router.prismicCache[uid]; if (!data) return; const pos = new P; t.getWorldPosition(pos); const texUrl = data.data.article_image.url; const tex = new Pe().load(texUrl); const l = new th(pos, t.rotation, 2, tex, uid); const c = new dc(l.instance); const h = this.experience.router.allProducts.find(f => f.uid === uid) || data; const u = new ub(l.instance, c, h); this.cadres.push(l), this.btns.push(c), this.links.push(u) }) }

old_block = r'setCadres\(\)\s*\{\s*const e\s*=\s*\["cat_1_l", "cat_1_r", "cat_2_l", "cat_2_r", "cat_3_l", "cat_3_r", "cat_4_l", "cat_4_r"\];\s*this\.cadresControllers\.forEach\(\(t, n\) => \{.*?\)\s*\}\)\s*\}'

new_block = """setCadres() {
    const e = ["cat_1_l", "cat_1_r", "cat_2_l", "cat_2_r", "cat_3_l", "cat_3_r", "cat_4_l", "cat_4_r"];
    const catsAndFilters = [
        { uid: "cat_1_l", cat: "gelinlik" },
        { uid: "cat_1_r", cat: "tesettur" },
        { uid: "cat_2_l", cat: "nisanlik" },
        { uid: "cat_2_r", cat: "kinalik" },
        { uid: "cat_3_l", cat: "soz-elbisesi" },
        { uid: "cat_3_r", cat: "after-party" },
        { uid: "cat_4_l", cat: "kaftan" },
        { uid: "cat_4_r", cat: "abiye" }
    ];
    this.cadresControllers.forEach((t, n) => {
        const uid = e[n % e.length];
        const data = this.experience.router.prismicCache[uid];
        if (!data) return;
        const pos = new P;
        t.getWorldPosition(pos);
        
        let texUrl = data.data.article_image.url;
        // The texture loader Pe is actually Wf or EM internally, but new Wf().load(texUrl) usually works, the original minified used `new EM(this.options.manager)` or similar, let's use what the original script used IF we can: Wait, the original was `new Fe().load` or `this.textureLoader.load`? 
        // Oh, the original says: `const tex = new Pe().load(texUrl);`
        const tex = new Pe().load(texUrl);
        tex.colorSpace = "srgb";
        
        const l = new th(pos, t.rotation, 2, tex, uid);
        const c = new dc(l.instance);
        
        // Ensure clicking a category leads to filtered gallery
        let mappedCat = catsAndFilters.find(c => c.uid === uid);
        const passData = Object.assign({}, data, { isCategory: true, linkedCat: mappedCat ? mappedCat.cat : "gelinlik" });
        
        const u = new ub(l.instance, c, passData);
        this.cadres.push(l);
        this.btns.push(c);
        this.links.push(u);
    });
}"""

# Actually, the original block has `new Pe().load`. I don't need to rebuild it exactly if I can just use `re.sub`.
content, count = re.subn(old_block, new_block, content, flags=re.DOTALL)

if count > 0:
    # Now let's do `class bb` which was skipped earlier because of `constructor(e)` vs `constructor()`
    # We found `class bb { constructor(e) {`
    bb_old_block = r'class bb\s*\{\s*constructor\(e\)\s*\{\s*if\s*\(\s*this\.experience.*?this\.group\.add\(\.\.\.this\.cadres\.map\(c\s*=>\s*c\.instance\)\)\s*\}'
    
    bb_new_block = """class bb {
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

        let filterStr = window.location.pathname.replace("/gallery/", "").replace("/gallery", "");
        if (filterStr.includes("?category=")) filterStr = filterStr.split("?category=")[1];
        if (!filterStr && this.experience.router.activeCategory && this.experience.router.activeCategory !== "ALL") {
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

        this.articles = this.articles.slice(0, 15);

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
    
    content, count_bb = re.subn(bb_old_block, bb_new_block, content, flags=re.DOTALL)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Patched db: {count} times")
    print(f"Patched bb: {count_bb} times")
else:
    print("Could not find old_block in file!")
