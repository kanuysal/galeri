import fileinput

file_path = "d:/minadesign/github/antigravity/SERKAN/game/assets/index-845b001d.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

def find_block(content, start_marker, end_marker="{"):
    start_index = content.find(start_marker)
    if start_index == -1: return -1, -1
    brace_start = content.find(end_marker, start_index + len(start_marker))
    if brace_start == -1: return -1, -1
    depth = 0
    for i in range(brace_start, len(content)):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0: return start_index, i + 1
    return -1, -1

db_start, db_end = find_block(content, "class db {")
if db_start == -1: db_start, db_end = find_block(content, "class db")

if db_start != -1:
    with open("d:/minadesign/github/antigravity/SERKAN/game/assets/debug_db.js", "w", encoding="utf-8") as out:
        out.write(content[db_start:db_end])
    print("Exported class db to debug_db.js")
else:
    print("db not found")
