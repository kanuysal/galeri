import sys

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("setGalerie")
if idx == -1:
    print("setGalerie not found!")
else:
    print("Context around setGalerie:")
    # Find all occurrences of setGalerie
    start = 0
    while True:
        idx = content.find("setGalerie", start)
        if idx == -1: break
        print("..." + content[max(0, idx - 100):idx + 300] + "...")
        print("---")
        start = idx + 1
