import os
import re

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# We need to find the block from 'this.linksContainer = document.querySelector(".menu_links ul");'
# down to 'this.refreshProducts("Tümü");'
# AND any extra '};' that might be lingering.

# In the current file, we have:
# this.linksContainer = document.querySelector(".menu_links ul");
# ... cats ...
# this.refreshProducts = (categoryId = "all") => { ... };
# this.refreshProducts("all");
# ...
# this.initLinkHoverVideo();
# };
# ...
# this.refreshProducts("Tümü");

start_str = 'this.linksContainer = document.querySelector(".menu_links ul");'
end_str = 'this.refreshProducts("Tümü");'

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_str)
    
    # We will replace this entire section with the correct, clean logic
    clean_logic = """this.linksContainer = document.querySelector(".menu_links ul");
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
        
        this.refreshProducts("all");"""
        
    new_content = content[:start_idx] + clean_logic + content[end_idx:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Cleaned up duplicated Lb constructor logic!")
else:
    print("Could not find start or end strings.")
