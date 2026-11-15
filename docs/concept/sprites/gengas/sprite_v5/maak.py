# raster.txt (één teken per pixel, '.' = transparant, tekens/kleuren in pal.py) -> gengas_v5.png (64x64, geïndexeerd,
# index 0 transparant). Geen inkleuring: alleen omzetten.
# Volledige keten (reproduceerbaar):
#   zie bouw.sh
import os; from PIL import Image
from pal import PAL,CH
D=os.path.dirname(os.path.abspath(__file__))+'/'
rows=[l.rstrip('\n') for l in open(D+'raster.txt')][:64]
assert len(rows)==64 and all(len(r)==64 for r in rows)
im=Image.new('P',(64,64)); flat=[v for c in PAL for v in c]
im.putpalette(flat+[0]*(768-len(flat)))
im.putdata([CH.index(c) for r in rows for c in r])
im.save(D+'gengas_v5.png',transparency=0); print('gengas_v5.png')
