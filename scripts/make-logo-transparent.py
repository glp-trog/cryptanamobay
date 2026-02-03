from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'assets' / 'img' / 'logo.jpg'
dst = ROOT / 'assets' / 'img' / 'logo.png'

im = Image.open(src).convert('RGBA')
px = im.load()

# Remove near-white background (tweakable)
# Anything with RGB all >= threshold becomes transparent.
threshold = 248
w, h = im.size
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if r >= threshold and g >= threshold and b >= threshold:
            px[x, y] = (r, g, b, 0)

# Light smoothing: make slightly-off-white mostly transparent too
# (optional) 

dst.parent.mkdir(parents=True, exist_ok=True)
im.save(dst, 'PNG', optimize=True)
print('wrote', dst)
