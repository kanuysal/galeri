import os

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# The error context:
old_str = 'remove("link_open") } class bb {'
new_str = 'remove("link_open") } } class bb {'

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed missing brace before class bb!")
else:
    print("Could not find the exact string to replace!")
    # Let's try matching with regex to handle potential whitespace
    import re
    pattern = r'remove\("link_open"\)\s*\}\s*class\s*bb\s*\{'
    replacement = r'remove("link_open") } } class bb {'
    new_content, count = re.subn(pattern, replacement, content)
    if count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Fixed missing brace before class bb via regex!")
    else:
        print("Still couldn't find the pattern!")
