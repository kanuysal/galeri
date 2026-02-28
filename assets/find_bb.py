import sys

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("class bb")
if idx == -1:
    print("class bb not found!")
else:
    print("Context around class bb:")
    print("..." + content[max(0, idx - 100):idx + 200] + "...")
