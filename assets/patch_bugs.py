import os
import re

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

# 1. Patch Loader (_w class)
loader_start, loader_end = find_block(content, "class _w extends Zn {") # Or _w
if loader_start == -1:
    loader_start, loader_end = find_block(content, "class _w") 
    
if loader_start != -1:
    loader_content = content[loader_start:loader_end]
    # Add safety timeout to ready trigger
    if "this.startLoading()" in loader_content and "setTimeout(() => { if(this.loaded < this.toLoad)" not in loader_content:
        timeout_patch = """this.startLoading();
        setTimeout(() => { if(this.loaded < this.toLoad) { console.log("Safety ready trigger"); this.trigger("ready"); } }, 5000);
        """
        loader_content = loader_content.replace("this.startLoading()", timeout_patch)
        content = content[:loader_start] + loader_content + content[loader_end:]
        print("Loader _w timeout patched.")
    else:
        print("Loader _w timeout already patched or startLoading not found.")
else:
    # Actually wait, let me look at `class _w` or `class dE` in the file.
    # In my previous checks, the Loader class was called `_w` or `dE`. Let's search for "class dE"
    de_start, de_end = find_block(content, "class dE extends Zn {")
    if de_start == -1:
        de_start, de_end = find_block(content, "class dE")
    if de_start != -1:
        de_content = content[de_start:de_end]
        if "this.startLoading()" in de_content and "setTimeout(() => { if(this.loaded < this.toLoad)" not in de_content:
            timeout_patch = """this.startLoading();
            setTimeout(() => { if(this.loaded < this.toLoad) { console.log("Safety ready trigger"); this.trigger("ready"); } }, 5000);
            """
            de_content = de_content.replace("this.startLoading()", timeout_patch)
            content = content[:de_start] + de_content + content[de_end:]
            print("Loader dE timeout patched.")
        else:
            print("Loader dE timeout already patched or startLoading not found.")

# 2. Patch Video AbortError
# The `AbortError` usually happens in `Lb` or `db` when play() is called and quickly paused/interrupted.
# However, I already did handle this in the new `rebrand_menu.py`:
# `let p = n.play(); if (p !== undefined) p.catch(error => ...)`
# But wait, looking at my `rebrand_menu.py`, I did not patch `class lb` or `class wb` video tags, only `initLinkHoverVideo` inside `Lb`.

# Let's globally replace `.play().catch(` with the safer variant... Actually it's safer to just replace specific occurrences if we know them.
# The user's exact ask: `Fixing the `AbortError` on video playback`.
# Let's use regex to find: `n.play().catch(l=>console.warn("Erreur lecture vidéo:",l))`
video_pattern1 = r'([a-zA-Z_$][0-9a-zA-Z_$]*)\.play\(\)\.catch\(([a-zA-Z_$][0-9a-zA-Z_$]*)=>console\.warn\("Erreur lecture vidéo:",\2\)\)'
# Replacement: `let p = $1.play(); if(p !== undefined) p.catch($2 => { if($2.name !== "AbortError") console.warn("Erreur lecture vidéo:", $2); })`
def video_repl(m):
    obj = m.group(1)
    err = m.group(2)
    return f'((playPromise={obj}.play())!==undefined?playPromise.catch({err}=>{{if({err}.name!=="AbortError")console.warn("Erreur lecture vidéo:",{err})}}):null)'

new_content, count = re.subn(video_pattern1, video_repl, content)
if count > 0:
    content = new_content
    print(f"Patched {count} video play() calls for AbortError.")

# 3. Patch the Router catch (Loader Fix 2)
# hE.init often has `.catch(e=>console.error(e))` and we want to add `.finally(()=>this.ready())`
router_pattern = r'\.catch\(([a-zA-Z_$])=>console\.error\(\1\)\)'
# We want to make sure we only patch the hE router one or just globally append the `.finally`?
# Actually it's probably better to just leave it if the timeout is applied correctly.

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Bug fixes script execution complete.")
