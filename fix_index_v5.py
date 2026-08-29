import os

def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'rb') as f:
        data = f.read()

    # Search for map(([t,n])=>t+": "+n).join(`\n\n`) or variant with backticks
    # Find position of `toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join(`
    target = b'toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join('
    idx = data.find(target)
    print(f"File {filepath} target at: {idx}")
    if idx != -1:
        print("Substr:", repr(data[idx:idx+150]))
        # Replace the entire broken toString method with valid JS
        old_pattern_start = data.find(b'toString(){return Object.entries(this.toJSON())', idx)
        old_pattern_end = data.find(b').forEach(function(u)', idx)
        if old_pattern_start != -1 and old_pattern_end != -1:
            old_slice = data[old_pattern_start:old_pattern_end]
            print("Old slice:", repr(old_slice))
            new_slice = b'toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join("\\r\\n")}'
            data = data[:old_pattern_start] + new_slice + data[old_pattern_end:]
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"Successfully fixed {filepath}")

fix_file('frontend/public/assets/index-v5.js')
fix_file('frontend/dist/assets/index-v5.js')
