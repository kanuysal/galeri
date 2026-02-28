import sys

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("this.cadresControllers.forEach")
if idx == -1:
    print("this.cadresControllers.forEach not found!")
else:
    print("Context around this.cadresControllers.forEach:")
    print("..." + content[max(0, idx - 200):idx + 800] + "...")
