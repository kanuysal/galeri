import os
import re

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print("Initial length:", len(content))

# 1. Undo db class mangling
# The v5 script did: r'this\.setCadres\(\)': 'setCadres() {' + set_cadres_content + '}',
# set_cadres_content started with '\n        const categories = ['
# and ended with 'this.links.push(u);\n        });'

# We need to find: setCadres() { const categories = ... }); } 
# and replace it back with this.setCadres()

# Let's use a very specific regex based on what was in v5.py
db_bad_block = r'setCadres\(\)\s*\{.*?this\.links\.push\(u\);\s*\}\);\s*\}'
content = re.sub(db_bad_block, 'this.setCadres()', content, flags=re.DOTALL)

# 2. Undo bb class mangling
# v5 did: r'class bb\{constructor\(e\)\{': 'class bb{constructor(e) {' + bb_patch + '}',
# bb_patch ended with 'this.group.add(...this.cadres.map(c => c.instance));'
bb_bad_block = r'class bb\{constructor\(e\)\s*\{.*?this\.group\.add\(\.\.\.this\.cadres\.map\(c => c\.instance\)\);\s*\}'
content = re.sub(bb_bad_block, 'class bb{constructor(e){', content, flags=re.DOTALL)

# 3. Undo Lb class mangling
# lb_patch ended with '});'
lb_bad_block = r'class Lb\{constructor\(\)\s*\{.*?this\.categories = \[.*?\}\s*\}\);\s*\}'
content = re.sub(lb_bad_block, 'class Lb{constructor(){', content, flags=re.DOTALL)

print("Final length:", len(content))

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Restoration complete.")
