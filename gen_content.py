import json
import os

content_dir = 'content'
files = os.listdir(content_dir)

# Helper to find matching file case-insensitively, prioritizing .webp
def find_file(name):
    for f in files:
        if f.lower().startswith(name.lower()) and f.lower().endswith('.webp'):
            return f
    for f in files:
        if f.lower().startswith(name.lower()):
            return f
    return "textures/oeuvre.png"

home_mapping = [
    {"pos": "image_left_bottom", "title": "Ahu Gelinlik", "file_prefix": "1 sol Gelinlik"},
    {"pos": "image_left_mid", "title": "Berta Gelinlik", "file_prefix": "2 sol Nisanlik"},
    {"pos": "image_left_mid_loin", "title": "Arya Nişanlık", "file_prefix": "3 sol Soz"},
    {"pos": "image_left_top", "title": "Pandora Kaftan", "file_prefix": "4 sol Kaftan"},
    {"pos": "image_right_bottom", "title": "Ayna After", "file_prefix": "1 sag tesettur"},
    {"pos": "image_right_mid", "title": "Belkıs Kınalık", "file_prefix": "2 sag Kinalik"},
    {"pos": "image_right_mid_loin", "title": "Nova After", "file_prefix": "3 sag After"},
    {"pos": "image_right_top", "title": "Mihrimah Abiye", "file_prefix": "4 sag Abiye"}
]

gallery_data = [
    ("Ahu Gelinlik", "Gelinlik"), ("Ajda Gelinlik", "Gelinlik"), ("Arya Nişanlık", "Nişanlık"),
    ("Ayda Gelinlik", "Gelinlik"), ("Ayna After", "After"), ("Barbie Nişanlık", "Nişanlık"),
    ("Belkıs Kınalık", "Kınalık"), ("Berta Gelinlik", "Gelinlik"), ("Bianca Gelinlik", "Gelinlik"),
    ("Bridgerton Nişanlık", "Nişanlık"), ("Celine Gelinlik", "Gelinlik"), ("Cherry Kınalık", "Kınalık"),
    ("Dark Nişanlık", "Nişanlık"), ("Devran Kınalık", "Kınalık"), ("Eleni Gelinlik", "Gelinlik"),
    ("Hanzade Gelinlik", "Gelinlik"), ("Jale Nişanlık", "Nişanlık"), ("Kate Gelinlik", "Gelinlik"),
    ("Kösem Kınalık", "Kınalık"), ("Lavanta Nişanlık", "Nişanlık"), ("Merve Nişanlık", "Nişanlık"),
    ("Mihrimah Abiye", "Abiye"), ("Mihrişah Kınalık", "Kınalık"), ("Milla Gelinlik", "Gelinlik"),
    ("Nadide Gelinlik", "Gelinlik"), ("Naime Kınalık", "Kınalık"), ("Narin Nişanlık", "Nişanlık"),
    ("Nevbahar Nişanlık", "Nişanlık"), ("Nova After", "After"), ("Novia Gelinlik", "Gelinlik"),
    ("Pandora Kaftan", "Kaftan"), ("Paris Gelinlik", "Gelinlik"), ("Pera Gelinlik", "Gelinlik"),
    ("Petit Gelinlik", "Gelinlik"), ("Roma Gelinlik", "Gelinlik"), ("Safiye Kınalık", "Kınalık"),
    ("Simay Gelinlik", "Gelinlik"), ("Songül Gelinlik", "Gelinlik"), ("Stellar Nişanlık", "Nişanlık"),
    ("Stephany Gelinlik", "Gelinlik"), ("Valeria Kınalık", "Kınalık"), ("Velvet Kaftan", "Kaftan"),
    ("Veronica Gelinlik", "Gelinlik"), ("Yakut Kınalık", "Kınalık")
]

articles = []
art_id = 1

def create_article(title, category, filename, uid=None):
    global art_id
    if not uid:
        uid = title.lower().replace(' ', '-').replace('ı', 'i').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g').replace('ö', 'o').replace('ü', 'u')
    doc_id = f"art-{art_id}"
    art_id += 1

    wa_url = f"https://wa.me/905421131641?text={title.replace(' ', '+')}+Hakkında+Bilgi+Almak+İstiyorum"

    return {
        "id": doc_id,
        "uid": uid,
        "type": "article",
        "href": f"https://thevertmenthe.cdn.prismic.io/api/v2/documents/search?q=%5B%5Bat%28document.id%2C%22{doc_id}%22%29%5D%5D",
        "tags": [category],
        "first_publication_date": "2025-01-01T12:00:00+0000",
        "last_publication_date": "2025-01-01T12:00:00+0000",
        "slugs": [uid],
        "linked_documents": [],
        "lang": "fr-fr",
        "data": {
            "article_title": [{"type": "heading1", "text": title, "spans": []}],
            "article_image": {
                "url": f"/content/{filename}",
                "dimensions": {"width": 800, "height": 1200},
                "alt": title,
                "copyright": "Mina Lidya"
            },
            "vendu": False,
            "right_row_1": [{"type": "paragraph", "text": "2026 Koleksiyonu", "spans": []}],
            "right_row_2": [{"type": "paragraph", "text": "Özel Tasarım", "spans": []}],
            "right_row_3": [{"type": "paragraph", "text": "Haute Couture", "spans": []}],
            "left_bottom_1": [{"type": "paragraph", "text": "İnegöl Mağaza", "spans": []}],
            "left_bottom_2": [{"type": "paragraph", "text": "Valencia Atellier", "spans": []}],
            "left_bottom_3": [{"type": "paragraph", "text": "Sevgiyle yapıyoruz", "spans": []}],
            "left_bottom_4": [{"type": "paragraph", "text": "Aşkla giyiniz...", "spans": []}],
            "product_url": {"link_type": "Web", "url": wa_url},
            "size": [{"type": "paragraph", "text": "Özel Tasarım", "spans": []}],
            "year": [{"type": "paragraph", "text": "Haute Couture", "spans": []}],
            "importance": "medium"
        }
    }

home_articles_dict = {}
all_articles = []

for item in home_mapping:
    fname = find_file(item['file_prefix'])
    art = create_article(item['title'], "Homepage", fname)
    home_articles_dict[item['pos']] = art

for title, cat in gallery_data:
    fname = find_file(title)
    art = create_article(title, cat, fname)
    articles.append(art)
    all_articles.append(art)
    # NO DOUBLE APPENDING HERE ANYMORE

home_doc = {
    "id": "home-1",
    "uid": "home",
    "type": "home",
    "href": "https://thevertmenthe.cdn.prismic.io/api/v2/documents/search?q=%5B%5Bat%28document.type%2C%22home%22%29%5D%5D",
    "tags": [],
    "slugs": ["home"],
    "linked_documents": [],
    "lang": "fr-fr",
    "data": {
        "home_title": [{"type": "heading1", "text": "Mina Lidya Gallery", "spans": []}]
    }
}

for pos, art in home_articles_dict.items():
    home_doc['data'][pos] = {
        "id": art['id'],
        "type": "article",
        "tags": art['tags'],
        "slug": art['uid'],
        "lang": "fr-fr",
        "uid": art['uid'],
        "link_type": "Document",
        "isBroken": False
    }

content = {
    "about": {"results": []},
    "gallery": {"results": articles},
    "article": {"results": all_articles},
    "home": {"results": [home_doc]}
}

with open('site_content.json', 'w', encoding='utf-8') as f:
    json.dump(content, f, indent=2, ensure_ascii=False)

print("Generated site_content.json successfully.")
