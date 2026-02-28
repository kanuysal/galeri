
import os

filepath = r'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
output_path = r'd:\minadesign\github\antigravity\SERKAN\game\assets\bb_class.js'

with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i == 3672:
            index = line.find('class bb {')
            if index != -1:
                bb_code = line[index:]
                # Next class might be " class ", "}class ", " class ", etc.
                # Actually, let's look for the next "class " keyword after our class name.
                next_class_index = bb_code.find('class ', 10)
                if next_class_index != -1:
                    bb_code = bb_code[:next_class_index]
                
                with open(output_path, 'w', encoding='utf-8') as out:
                    out.write(bb_code)
                print(f"Extracted bb class of length {len(bb_code)} to {output_path}")
                # Print first 200 chars to verify
                print(f"Start: {bb_code[:200]}")
            else:
                print("class bb not found")
            break
