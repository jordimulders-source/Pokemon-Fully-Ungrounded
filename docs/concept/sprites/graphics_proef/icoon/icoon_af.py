"""Poetsen + frame 2 + oplevering (ICOON_WERKWIJZE stap 4, 7, 8), uit hetzelfde soort-JSON als icoon_bouw.py.

python3 docs/concept/sprites/graphics_proef/icoon/icoon_af.py <soort.json> [map]
  invoer : <map>/onderlaag.png (uit icoon_bouw.py)
  uit    : <map>/icon.png (32x64, 2 frames, modus P, index 0 transparant), icon_anim.gif, icon_8x_vergelijk.png
JSON-sleutels:
 "poets":  {"zone": [[x, y, index], ...], ...}   # pixelreparaties per zone op frame 1 (alleen technisch)
 "frame2": {"split": y,                          # alles BOVEN rij y schuift 1 px omlaag; rij y vervalt (pootrij)
            "vast": [[x0,y0,x1,y1], ...],        # pixels in deze vakken blijven staan (klein gebaar, bv. staart)
            "extra": [[x, y, index], ...]}       # optioneel: pixels in frame 2 (alleen om een rand te dichten)
"""
import sys, os, json, numpy as np
from PIL import Image
ARGV = [os.path.abspath(a) for a in sys.argv[1:]]
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import icoon_bouw as B   # chdir naar de repo-root
cfg = json.load(open(ARGV[0])); D = ARGV[1] if len(ARGV) > 1 else os.path.dirname(ARGV[0])
im = Image.open(os.path.join(D, 'onderlaag.png')); P = np.array(im.getpalette()[:48]).reshape(16, 3)
pk = [k for k in range(6) if (B.IPAL[k][1:] == P[1:]).all()][0]
f1 = np.array(im)[:32].copy(); basis = f1.copy()
for zone, px in cfg.get('poets', {}).items():
    for x, y, v in px: f1[y, x] = v
    print(f'poets {zone}: {int((f1 != basis).sum())} px t.o.v. de onderlaag (cumulatief)')
fr2 = cfg.get('frame2', {}); y_s = fr2.get('split', 27)
f2 = f1.copy(); f2[1:y_s + 1] = f1[:y_s]; f2[0] = 0          # bovendeel 1 px omlaag, rij y_s vervalt
for x0, y0, x1, y1 in fr2.get('vast', []): f2[y0:y1 + 1, x0:x1 + 1] = f1[y0:y1 + 1, x0:x1 + 1]   # gebaar blijft staan
for x, y, v in fr2.get('extra', []): f2[y, x] = v
weg = int(((f1 > 0).sum()) - (f2 > 0).sum())
print(f'frame 2: split rij {y_s}, {weg} px minder (de vervallen rij), vaste vakken {len(fr2.get("vast", []))}')
ic = np.vstack([f1, f2]).astype(np.uint8)
out = Image.fromarray(ic, 'P'); out.putpalette(P.flatten().tolist() + [0] * 720)
out.save(os.path.join(D, 'icon.png'), transparency=0)
# gif (8x, 2 frames)
fr = []
for a in (f1, f2):
    o = np.zeros((32, 32, 3), np.uint8) + np.array([115, 197, 164], np.uint8)
    for k in range(1, 16): o[a == k] = P[k]
    fr.append(Image.fromarray(o).resize((256, 256), Image.NEAREST))
fr[0].save(os.path.join(D, 'icon_anim.gif'), save_all=True, append_images=fr[1:], duration=270, loop=0)
B.vel(cfg, [f1, f2], (['icoon frame 1', 'icoon frame 2'], [pk, pk]), os.path.join(D, 'icon_8x_vergelijk.png'))
print(f'palet pal{pk} (.iconPalIndex = {pk})')
