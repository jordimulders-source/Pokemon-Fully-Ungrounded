# Bouwt sprite.png (64x64, geindexeerd, 16 kleuren) en normal.pal uit raster.txt (met de hand bewerkt tekstraster).
import sys
from PIL import Image
from pal import PAL
fn=sys.argv[1] if len(sys.argv)>1 else 'raster.txt'
out=sys.argv[2] if len(sys.argv)>2 else 'sprite.png'
rows=[r.rstrip('\n') for r in open(fn) if r.strip()]
assert len(rows)==64,len(rows)
for i,r in enumerate(rows): assert len(r)==64,(i,len(r))
im=Image.new('P',(64,64)); im.putpalette([v for c in PAL for v in c])
im.putdata([0 if c=='.' else int(c,16) for r in rows for c in r]); im.info['transparency']=0
im.save(out,transparency=0,bits=4)
with open('normal.pal','w') as f:
    f.write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
