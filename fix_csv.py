import csv

new_data = [
    ["Identifier", "Title", "Right_Row_1", "Right_Row_2", "Right_Row_3", "Left_Bottom_1", "Left_Bottom_2", "Left_Bottom_3", "Left_Bottom_4", "Product_URL"],
    ["1 sol Gelinlik", "Ahu Gelinlik", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Ahu+Gelinlik+Hakkında+Bilgi+Almak+İstiyorum"],
    ["2 sol Nisanlik", "Berta Gelinlik", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Berta+Gelinlik+Hakkında+Bilgi+Almak+İstiyorum"],
    ["3 sol Soz", "Arya Nişanlık", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Arya+Nişanlık+Hakkında+Bilgi+Almak+İstiyorum"],
    ["4 sol Kaftan", "Pandora Kaftan", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Pandora+Kaftan+Hakkında+Bilgi+Almak+İstiyorum"],
    ["1 sag tesettur", "Ayna After", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Ayna+After+Hakkında+Bilgi+Almak+İstiyorum"],
    ["2 sag Kinalik", "Belkıs Kınalık", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Belkıs+Kınalık+Hakkında+Bilgi+Almak+İstiyorum"],
    ["3 sag After", "Nova After", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Nova+After+Hakkında+Bilgi+Almak+İstiyorum"],
    ["4 sag Abiye", "Mihrimah Abiye", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Mihrimah+Abiye+Hakkında+Bilgi+Almak+İstiyorum"],
    ["Ajda Gelinlik", "Ajda Gelinlik", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Ajda+Gelinlik+Hakkında+Bilgi+Almak+İstiyorum"],
    ["Ayda Gelinlik", "Ayda Gelinlik", "Özel Tasarım", "Detaylar", "2026 Koleksiyonu", "Zarif İşleme", "Fransız Danteli", "Özel Dikim", "Mina Lidya İmzalı", "https://wa.me/905421131641?text=Ayda+Gelinlik+Hakkında+Bilgi+Almak+İstiyorum"]
]

with open('product_content.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(new_data)
print("CSV exported with UTF-8 BOM and semicolons!")
