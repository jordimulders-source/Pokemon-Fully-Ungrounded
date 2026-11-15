# maak.py: raster.txt (één teken per pixel = paletindex, '.'=0 transparant) -> gengas_r2.png (64x64, geïndexeerd)
# + vergelijking 8x naast de kleurgids (vergelijk_8x.png). Geen inkleuring: alleen omzetten.
import sys; sys.path.insert(0,'.')
from PIL import Image
from pal import PAL,CH
rows=[l.rstrip('\n') for l in open('raster.txt')][:64]
assert len(rows)==64 and all(len(r)==64 for r in rows), [len(r) for r in rows]
im=Image.new('P',(64,64)); flat=[]
for c in PAL: flat+=list(c)
im.putpalette(flat+[0]*(768-len(flat)))
im.putdata([CH.index(ch) for r in rows for ch in r])
im.save('gengas_r2.png',transparency=0)
def rgba(p):
    i=Image.open(p).convert('RGBA'); return i
s=rgba('gengas_r2.png'); k=Image.open('../model/kleurgids_64.png').convert('RGBA')
V=Image.new('RGBA',(64*8*2+16,64*8),(255,255,255,255))
bg=Image.new('RGBA',(512,512),(255,255,255,255)); bg.alpha_composite(s.resize((512,512),Image.NEAREST))
V.paste(bg,(0,0)); V.paste(k.resize((512,512),Image.NEAREST),(528,0)); V.save('vergelijk_8x.png')
print('ok')
