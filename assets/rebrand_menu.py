import os
import re

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

lb_start, lb_end = find_block(content, "class Lb {")
if lb_start != -1:
    lb_content = content[lb_start:lb_end]
    
    # Let's find the Exact string using a regex that handles whitespace variations
    # The part we want to replace starts with: this.linksContainer = document.querySelector(".menu_links ul")
    # And ends with: document.querySelectorAll(".menu_links_hover").forEach(s => s.style.opacity = "0")
    
    pattern = r'this\.linksContainer\s*=\s*document\.querySelector\("\.menu_links ul"\).*?document\.querySelectorAll\("\.menu_links_hover"\)\.forEach\(s\s*=>\s*s\.style\.opacity\s*=\s*"0"\);'
    
    new_loop = """
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
"""
    
    if re.search(pattern, lb_content, re.DOTALL):
        lb_content = re.sub(pattern, new_loop.replace('\\', '\\\\'), lb_content, flags=re.DOTALL)
        content = content[:lb_start] + lb_content + content[lb_end:]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Class Lb patched successfully.")
    else:
        print("Pattern not found in Lb_content.")
else:
    print("Failed to find class Lb.")
