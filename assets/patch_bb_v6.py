import sys

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

# Find class bb constructor block
start_idx = content.find("class bb {\n        constructor")
if start_idx == -1: start_idx = content.find("class bb{\nconstructor")
if start_idx == -1: start_idx = content.find("class bb")

if start_idx != -1:
    # We just want to replace the whole constructor(e) { ... }
    const_start = content.find("constructor(e)", start_idx)
    if const_start != -1:
        brace_start = content.find("{", const_start)
        depth = 0
        end_idx = -1
        for i in range(brace_start, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break
        
        if end_idx != -1:
            new_const = """constructor(e) {
        this.experience = new Rt;
        this.scene = this.experience.scene;
        this.ressources = this.experience.resources || this.experience.ressources;
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
            
            let tx = this.ressources ? this.ressources.items[t.uid] : null;
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
            content = content[:const_start] + new_const + content[end_idx:]
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("bb constructor patched v6 successfully!!")
        else:
            print("Could not find end of constructor")
    else:
        print("constructor(e) not found after class bb")
else:
    print("class bb not found")
