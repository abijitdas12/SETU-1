with open('frontend/public/assets/index-v5.js', 'rb') as f:
    data = f.read()

target = b'toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join('
idx = data.find(target)
print("Target index:", idx)
if idx != -1:
    end_idx = data.find(b').forEach', idx)
    print("End index:", end_idx)
    if end_idx != -1:
        print("Slice to replace:", repr(data[idx:end_idx]))
        new_slice = b'toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join("\\n")'
        data = data[:idx] + new_slice + data[end_idx:]
        with open('frontend/public/assets/index-v5.js', 'wb') as f:
            f.write(data)
        with open('frontend/dist/assets/index-v5.js', 'wb') as f:
            f.write(data)
        print("FIX APPLIED SUCCESSFULLY!")
