import sys
file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("class bb")
if idx == -1:
    print("class bb not found!")
else:
    print("Context around class bb:")
    print("..." + content[max(0, idx - 200):idx + 200] + "...")

print("\n---")
idx2 = content.find("this.link.classList.remove(\"link_open\")")
if idx2 != -1:
    print("Context around link_open:")
    print("..." + content[max(0, idx2 - 100):idx2 + 200] + "...")
