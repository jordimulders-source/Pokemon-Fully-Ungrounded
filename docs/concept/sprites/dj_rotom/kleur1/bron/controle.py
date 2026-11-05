"""Controle: alpha-diff met het bevroren silhouet, open randen, losse pixels, palet."""
import numpy as np
from PIL import Image
S='../../silhouet_af/silhouet.png'
im=Image.open('../dj_rotom.png'); a=np.array(im); s=np.array(Image.open(S))
print('modus',im.mode,im.size,'transparency',im.info.get('transparency'),'max index',a.max())
print('alpha-diff met silhouet:',int(((a>0)!=(s>0)).sum()),'px')
GLOED={1}  # alleen de buitenste gloedtint mag aan transparant grenzen
open_=[];los=[]
for y in range(64):
    for x in range(64):
        v=a[y,x]
        if not v: continue
        n4=[a[yy,xx] if 0<=yy<64 and 0<=xx<64 else 0 for yy,xx in((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
        if 0 in n4 and v not in GLOED: open_.append((x,y,v))
        n8=[a[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if (yy,xx)!=(y,x) and 0<=yy<64 and 0<=xx<64]
        if all(k==0 for k in n8): los.append((x,y))
print('open randen (niet-buitengloed naast transparant):',open_)
print('losse pixels (geen buren):',los)
print('aantal px:',int((a>0).sum()),' gebruikte indexen:',sorted(set(np.unique(a))-{0}))
