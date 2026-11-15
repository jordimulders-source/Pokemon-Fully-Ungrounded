"""Diff t.o.v. v7: alles binnen de mond (x19-33, y32-38)? palet gelijk, index 0 transparant."""
from PIL import Image; import numpy as np, glob, os
H=os.path.dirname(os.path.abspath(__file__))
v7=Image.open(os.path.join(H,'..','sprite_v7','hauntflare_v7.png')); a=np.array(v7)
for p in sorted(glob.glob(os.path.join(H,'kandidaat_*.png'))):
    im=Image.open(p); b=np.array(im)
    ys,xs=np.nonzero(a!=b)
    buiten=[(x,y) for x,y in zip(xs,ys) if not (19<=x<=33 and 32<=y<=38)]
    print(os.path.basename(p), im.mode, 'transp', im.info.get('transparency'), 'palet gelijk', im.getpalette()==v7.getpalette(),
          'px anders', len(xs), 'buiten mond', len(buiten), 'silhouet', int(((a==0)!=(b==0)).sum()),
          'pixels', sorted(zip(xs.tolist(),ys.tolist())))
