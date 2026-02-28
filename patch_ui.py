
import os

# 1. Update index.html
html_path = r'd:\minadesign\github\antigravity\SERKAN\game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Font replacement
old_font_link = '<link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&display=swap"\n    rel="stylesheet" />'
# The file showed:
# 16:   <link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&display=swap"
# 17:     rel="stylesheet" />
# Note the indentation of 2 spaces and newline.

new_font_link = '  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@100;300;400;600;700&display=swap" rel="stylesheet" />'

import re
html_content = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Josefin\+Sans.*?\n\s+rel="stylesheet" />', new_font_link, html_content, flags=re.DOTALL)

# Menu replacement
old_menu_search = r'<div class="menu_main_links">.*?<div class="menu_categories">.*?</div>'
new_menu_content = """<div class="menu_main_links">
      <div class="menu_group">
        <span><a href="/">Anasayfa</a> ></span>
        <div class="submenu_container home_cats"></div>
      </div>
      <div class="menu_group">
        <span><a href="/gallery">Galeri</a> ></span>
        <div class="submenu_container gallery_cats"></div>
      </div>
      <div class="menu_group">
        <span><a href="/about">Hakkımızda</a> ></span>
      </div>
      <div class="menu_group">
        <span><a href="/contact">İletişim</a> ></span>
      </div>
    </div>"""

html_content = re.sub(r'<div class="menu_main_links">.*?</div>\s+<div class="menu_categories">.*?</div>', new_menu_content, html_content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print("Updated index.html")

# 2. Update CSS
css_path = r'd:\minadesign\github\antigravity\SERKAN\game\assets\index-c354b78a.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace font var
css_content = css_content.replace('--font_family: "Josefin Sans", sans-serif', '--font_family: "Outfit", sans-serif')

# Add submenu styles
submenu_styles = """
.submenu_container { padding-right: 15rem; overflow: hidden; height: 0; transition: height 0.3s ease-out; display: flex; flex-direction: column; align-items: flex-end; }
.menu_group:hover .submenu_container { height: auto; margin-bottom: 25rem; }
.submenu_container a { font-size: 15rem !important; opacity: 0.6; display: block; margin-top: 10rem; text-transform: uppercase; font-weight: 300; }
.submenu_container a:hover, .submenu_container a.active { opacity: 1; font-weight: 600; }
.menu_group { margin-bottom: 15rem; text-align: right; }
"""
css_content += submenu_styles

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)
print("Updated CSS")
