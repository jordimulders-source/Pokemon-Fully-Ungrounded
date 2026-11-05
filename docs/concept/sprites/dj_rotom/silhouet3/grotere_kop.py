"""DJ Rotom silhouet 3: het middenstuk (kop-kubus + spits) in de bron groter maken; de bliksem houdt zijn maat en schuift mee.
Jordi (5 nov): "ja dan moet het middenstuk misschien wat groter om de ogen enzo goed te kunnen uitbeelden".
Kop-laag uit de bron (polygoon in broncoördinaten) wordt geschaald rond het midden van de onderkant;
de rechterspeaker (dichtbij) blijft ervóór; rond de vergrote kop komt de mintgloed mee.
Gebruik: python3 grotere_kop.py <bron> <uit.png> <schaal>"""
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
bron, uit, s = sys.argv[1], sys.argv[2], float(sys.argv[3])
PAD = 400
src = Image.open(bron).convert('RGBA')
W, H = src.size
base = Image.new('RGBA', (W, H + PAD)); base.paste(src, (0, PAD))
def m(poly):
    im = Image.new('L', base.size); ImageDraw.Draw(im).polygon([(x, y + PAD) for x, y in poly], fill=255); return im
kop = m([(660, 950), (700, 925), (1090, 915), (1165, 935), (1172, 1562), (660, 1562)])
spits = m([(862, 935), (918, 750), (968, 935)])
bliksem = m([(640, 300), (1060, 300), (1060, 905), (640, 905)])
a = np.array(base)
bl = (np.array(bliksem) > 0) & (a[..., 3] > 0) & (a[..., 1] > a[..., 0])   # alleen mint/wit plasma
mask = (np.array(kop) > 0) | (np.array(spits) > 0)
laag = a.copy(); laag[~mask] = 0
bliks = a.copy(); bliks[~bl] = 0                                           # bliksem: zelfde maat, schuift mee met de spitspunt
rechts = a.copy(); rechts[:, :1165] = 0                                    # rechterspeaker blijft vóór
ax, ay = 915, 1562 + PAD
L = Image.fromarray(laag)
Lw, Lh = int(W * s), int((H + PAD) * s)
Ls = L.resize((Lw, Lh), Image.LANCZOS)
groot = Image.new('RGBA', base.size)
groot.paste(Ls, (int(ax - ax * s), int(ay - ay * s)), Ls)
# mintgloed rond de vergrote kop
ga = groot.split()[3].point(lambda v: 255 if v > 128 else 0).filter(ImageFilter.MaxFilter(51))
gloed = Image.new('RGBA', base.size, (184, 239, 198, 255)); gloed.putalpha(ga)
out = base.copy()
out.alpha_composite(gloed); out.alpha_composite(groot)
dy = int(round((750 + PAD - ay) * (s - 1)))                                # spitspunt schuift zoveel omhoog
dx = int(round((918 - ax) * (s - 1)))
B = Image.fromarray(bliks); sh = Image.new('RGBA', base.size); sh.paste(B, (dx, dy), B)
out.alpha_composite(sh); out.alpha_composite(Image.fromarray(rechts))
out.save(uit)
