
import os

filepath = r'd:\minadesign\github\antigravity\SERKAN\game\assets\index-845b001d.js'
output_path = r'd:\minadesign\github\antigravity\SERKAN\game\assets\bb_class.js'

with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i == 3672: # 3673-1
            index = line.find('class bb {')
            if index != -1:
                # Find the end of the class. This is tricky with minified code.
                # We'll just take from 'class bb' to the end of the line if it's the last class.
                # Or look for '} class ' which would be the start of next class.
                
                bb_code = line[index:]
                # Try to find the next class
                next_class_index = bb_code.find(' class ', 10)
                if next_class_index != -1:
                    bb_code = bb_code[:next_class_index]
                
                with open(output_path, 'w', encoding='utf-8') as out:
                    out.write(bb_code)
                print(f"Extracted bb class to {output_path}")
            else:
                print("class bb not found on line 3673")
            break
