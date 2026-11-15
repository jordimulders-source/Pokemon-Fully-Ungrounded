# tekstraster -> indexed png (+8x). Gebruik: render.py raster.txt uit.png
import sys,numpy as np; from PIL import Image; from palet import PAL,CH
rows=[l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]
g=np.array([[CH.index(c) for c in r] for r in rows],'uint8'); assert g.shape==(64,64),g.shape
im=Image.fromarray(g,'P'); fl=[v for c in PAL for v in c]; im.putpalette(fl); im.save(sys.argv[2],transparency=0)
im.resize((512,512),Image.NEAREST).save(sys.argv[2].replace('.png','_8x.png'),transparency=0)
m=g>0; ys,xs=np.where(m); print('px',m.sum(),'w',xs.max()-xs.min()+1,'h',ys.max()-ys.min()+1,'kleuren',len(set(g.ravel())))
