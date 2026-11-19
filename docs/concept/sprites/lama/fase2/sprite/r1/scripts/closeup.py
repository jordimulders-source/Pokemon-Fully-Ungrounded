# Close-up: sprite-uitsnede 12x naast hetzelfde stuk model (zelfde raster), met rasterlijntjes.
# Gebruik: python3 closeup.py SPRITE.png UIT.png x0 y0 x1 y1   (spritecoordinaten)
import sys, os
from PIL import Image, ImageDraw
HIER = os.path.dirname(os.path.abspath(__file__)); FASE2 = os.path.dirname(os.path.dirname(os.path.dirname(HIER)))
sys.path.insert(0, HIER); from reduceer import S, X0, Y0, COLS
sp, uit = sys.argv[1], sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7]); Z = int(os.environ.get("Z", 12))
im = Image.open(sp); im.save('/tmp/_c.png', transparency=0) if im.mode == 'P' else None
im = Image.open('/tmp/_c.png').convert('RGBA') if im.mode == 'P' else im.convert('RGBA')
ox = (64 - COLS) // 2
mdl = Image.open(os.path.join(FASE2, 'gemini/poten/r4_poten_r12.png')).convert('RGB')
def m2(x, y): return (X0 + (x - ox) * S, Y0 + (y - 1) * S)
a0 = m2(x0, y0); a1 = m2(x1, y1)
mc = mdl.crop((int(a0[0]), int(a0[1]), int(a1[0]), int(a1[1]))).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.LANCZOS)
sc = Image.new('RGBA', ((x1 - x0) * Z, (y1 - y0) * Z), (255, 255, 255, 255))
c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.NEAREST); sc.alpha_composite(c)
W = Image.new('RGB', (sc.width * 2 + 10, sc.height), (255, 255, 255)); W.paste(sc.convert('RGB'), (0, 0)); W.paste(mc, (sc.width + 10, 0))
d = ImageDraw.Draw(W)
for k in range(x1 - x0 + 1):
    for off in (0, sc.width + 10): d.line([(off + k * Z, 0), (off + k * Z, sc.height)], fill=(200, 200, 200) if (x0 + k) % 5 else (120, 160, 255))
for k in range(y1 - y0 + 1):
    for off in (0, sc.width + 10): d.line([(off, k * Z), (off + sc.width, k * Z)], fill=(200, 200, 200) if (y0 + k) % 5 else (120, 160, 255))
W.save(uit)
