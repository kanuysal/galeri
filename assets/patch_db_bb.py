import fileinput
import re
import os

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

def find_block(content, start_marker, end_marker="{"):
    start_index = content.find(start_marker)
    if start_index == -1: return -1, -1
    brace_start = content.find(end_marker, start_index + len(start_marker))
    if brace_start == -1: return -1, -1
    depth = 0
    for i in range(brace_start, len(content)):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0: return start_index, i + 1
    return -1, -1

patched = False

# 1. Patch db class (Homepage)
db_start, db_end = find_block(content, "class db {")
if db_start == -1: db_start, db_end = find_block(content, "class db")

if db_start != -1:
    db_content = content[db_start:db_end]
    # In minified code, it might be `setCadres(){` or `setCadres(e){`
    sc_start, sc_end = find_block(db_content, "setCadres()")
    if sc_start == -1: sc_start, sc_end = find_block(db_content, "setCadres(e)")
    if sc_start == -1: sc_start, sc_end = find_block(db_content, "setCadres") # Fallback
    
    if sc_start != -1:
        new_set_cadres = """setCadres() {
        const categories = [
            { label: "Gelinlik", uid: "gelinlik", image: "image_left_bottom", cat: "gelinlik" },
            { label: "Tesettür Gelinlik", uid: "tesettur", image: "image_left_mid", cat: "tesettur" },
            { label: "Nişanlık", uid: "nisanlik", image: "image_left_mid_loin", cat: "nisanlik" },
            { label: "Kınalık", uid: "kinalik", image: "image_left_top", cat: "kinalik" },
            { label: "Söz", uid: "soz-elbisesi", image: "image_right_bottom", cat: "soz-elbisesi" },
            { label: "After Party", uid: "after-party", image: "image_right_mid", cat: "after-party" },
            { label: "Kaftan", uid: "kaftan", image: "image_right_mid_loin", cat: "kaftan" },
            { label: "Abiye", uid: "abiye", image: "image_right_top", cat: "abiye" }
        ];
        this.cadresControllers.forEach((t, n) => {
            const cat = categories[n % categories.length];
            // The UID here needs to map to Prismic format "cat_1_l" etc that we set in hE
            const mapping = ["cat_1_l", "cat_1_r", "cat_2_l", "cat_2_r", "cat_3_l", "cat_3_r", "cat_4_l", "cat_4_r"];
            const prismicUid = mapping[n % mapping.length];
            
            const s = this.homeData[cat.image].uid; // The position identifier
            const o = this.ressources.items[prismicUid]; // get our translated prismic obj
            const a = new P; 
            t.getWorldPosition(a);
            const l = new th(a, t.rotation, 2, o);
            const c = new dc(l.instance);
            const h = Object.assign({}, o, { isCategory: true, linkedCat: cat.cat });
            const u = new ub(l.instance, c, h);
            this.cadres.push(l); this.btns.push(c); this.links.push(u);
        });
    }"""
        db_content = db_content[:sc_start] + new_set_cadres + db_content[sc_end:]
        content = content[:db_start] + db_content + content[db_end:]
        print("db class patched.")
        patched = True
    else:
        print("setCadres not found in db class")
else:
    print("db class not found")

# 2. Patch bb class (Gallery)
bb_start, bb_end = find_block(content, "class bb {")
if bb_start == -1: bb_start, bb_end = find_block(content, "class bb")

if bb_start != -1:
    bb_content = content[bb_start:bb_end]
    # We want to patch the constructor completely to implement zigzag & 15 limit
    const_start, const_end = find_block(bb_content, "constructor")
    if const_start != -1:
        new_bb_constructor = """constructor(e) {
        this.experience = new Rt;
        this.scene = this.experience.scene;
        this.ressources = this.experience.resources; // Wait, original code uses ressources 
        this.ressources = this.experience.ressources;
        this.camera = this.experience.camera.instance;
        this.group = new Nn;
        this.scene.add(this.group);
        this.cadres = [];
        this.btns = [];
        this.links = [];
        this.fromGallery = e;
        
        const params = new URLSearchParams(window.location.search);
        let filter = window.activeCategory || params.get('category') || params.get('filter');
        if (!filter && this.experience.router.activeCategory && this.experience.router.activeCategory !== "ALL") {
            filter = this.experience.router.activeCategory;
        }
        
        this.articles = [...this.experience.router.articles];
        if (filter && filter !== "ALL" && filter !== "Tümü") {
            const lowerFilter = filter.toLowerCase();
            this.articles = this.articles.filter(a => {
                const c = a.data.category ? a.data.category.toLowerCase() : "";
                const idName = a.uid ? a.uid.toLowerCase() : "";
                const tName = a.data.title ? a.data.title.toLowerCase() : "";
                return c.includes(lowerFilter) || idName.includes(lowerFilter) || tName.includes(lowerFilter);
            });
        }
        
        this.articles = this.articles.slice(-15).reverse();
        
        let zPos = -0.5;
        this.articles.forEach((t, n) => {
            const xPos = n % 2 === 0 ? 1.5 : -1.5;
            zPos -= 2.5;
            const yRot = n % 2 === 0 ? -0.2 : 0.2;
            const i = new th(new P(xPos, 1.2, zPos), new P(0, yRot, 0), 1.5, this.experience.ressources.items[t.uid], t.uid);
            const s = new dc(i.instance);
            const o = new Sb(i.instance, s, t);
            this.cadres.push(i); this.btns.push(s); this.links.push(o);
        });
        
        this.group.add(...this.cadres.map(c => c.instance));
    }"""
        bb_content = bb_content[:const_start] + new_bb_constructor + bb_content[const_end:]
        content = content[:bb_start] + bb_content + content[bb_end:]
        print("bb class patched.")
        patched = True
    else:
        print("constructor not found in bb class")
else:
    print("bb class not found")

if patched:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("File saved.")
