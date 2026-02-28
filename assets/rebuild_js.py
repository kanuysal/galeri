import os
import re

js_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"
backup_path = "d:/minadesign/github/antigravity/SERKAN/game/extracted_classes_utf8.txt"

with open(js_path, "r", encoding="utf-8") as f:
    full_content = f.read()

# 1. Identify the boundaries of the classes section.
# It starts after GSAP/CSSPlugin: qe.Circ; (or similar)
# and ends before the shader strings at the end.

# Let's find 'qe.Circ;'
gsap_end_marker = "qe.Circ;"
gsap_index = full_content.find(gsap_end_marker)
if gsap_index == -1:
    print("Could not find GSAP end marker")
    exit(1)

start_index = gsap_index + len(gsap_end_marker)

# Find the end marker. 
# Looking at the view_file output, after hE/Lb classes, there are shaders like Eb, Ab.
# 'var Eb=`varying vec2 vUv; \r'
shader_start_marker = "var Eb=`varying vec2 vUv;"
end_index = full_content.find(shader_start_marker)

if end_index == -1:
    print("Could not find shader start marker")
    exit(1)

print(f"Classes section: {start_index} to {end_index}")

# 2. Get the new classes content from the backup
# We need to extract the classes from extracted_classes_utf8.txt
with open(backup_path, "r", encoding="utf-8") as f:
    backup_text = f.read()

# The backup_text has markers like '--- START class bb at ... ---'
# and contains: bb, ub, db, fb (empty), dc, th, Sb, Lb.
# Wait, it actually has db inside the 'class ub' section in the view_file output?
# No, let's look at the view_file output of extracted_classes_utf8.txt carefully.

# Actually, I'll just use the classes I found in assets/ as well.
# Lb_class.js, bb_class_large.js, hE_class.js, wb_class.js

def get_class(name, path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

classes_content = ""
# Order matters if there are dependencies, but in JS classes it mostly doesn't.
# However, we should try to match the original structure.

# Let's use the content from extracted_classes_utf8.txt as it's a bundle.
# It starts with 'class bb' at line 5 (in view_file output)
# and ends with 'class Lb' at the end.

# I'll manually construct the block from the backup text.
# Extract class bb
bb_match = re.search(r'class bb\{.*?\}\}\}', backup_text, re.DOTALL)
# Extract class ub + db + fb + dc + th + Sb
ub_db_match = re.search(r'class ub\{.*?\}\}', backup_text, re.DOTALL)
# Extract class Lb
lb_match = re.search(r'class Lb\{.*?\}\}', backup_text, re.DOTALL)

# Let's just use the whole text between START/END markers if possible.
cleaned_classes = ""
for line in backup_text.splitlines():
    if line.startswith("---") or line.startswith("Searching for:"):
        continue
    cleaned_classes += line + "\n"

# 3. Assemble the file
new_content = full_content[:start_index] + "\n" + cleaned_classes + "\n" + full_content[end_index:]

with open(js_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("File rebuilt successfully.")
