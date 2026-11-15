# raster_v8a/b.txt -> gengas_v8a/b.png (64x64, geïndexeerd, index 0 transparant). Keten: python3 v8.py && python3 maak.py && python3 vel.py
import os; from PIL import Image
from pal import PAL,CH
D=os.path.dirname(os.path.abspath(__file__))+'/'
for v in "x":
    rows=[l.rstrip('\n') for l in open(D+f'raster.txt')][:64]
    assert len(rows)==64 and all(len(r)==64 for r in rows)
    im=Image.new('P',(64,64)); flat=[c for p in PAL for c in p]
    im.putpalette(flat+[0]*(768-len(flat))); im.putdata([CH.index(c) for r in rows for c in r])
    im.save(D+f'gengas_v9.png',transparency=0); print(f'gengas_v9.png')
