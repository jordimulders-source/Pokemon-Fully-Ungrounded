# Technisch opschonen: (1) lucht-zone vervangen door de overgenomen modellijnen (lijnen.py); (2) buitenlijn 1 px op de
# bestaande silhouetrand (silhouet blijft gelijk): bruin aan de lichtkant (achtergrond alleen boven/links) -> selout 15
# (donkerbruin), verder zwart. Zwart en grijs blijven. -> schoon.npy
import numpy as np
o=np.load('kaal.npy').copy(); z=np.load('lucht.npy'); L=np.load('lijn.npy')
o[z]=0; o[L>0]=1
H,W=o.shape; ring=np.zeros_like(o)
for y in range(H):
    for x in range(W):
        v=o[y,x]
        if v in (0,1,15): continue
        up=y==0 or o[y-1,x]==0; dn=y==H-1 or o[y+1,x]==0; lf=x==0 or o[y,x-1]==0; rt=x==W-1 or o[y,x+1]==0
        if not(up or dn or lf or rt): continue
        if v in (2,3,4) and (up or lf) and not (dn or rt): ring[y,x]=15
        else: ring[y,x]=1
print('ringpixels',(ring>0).sum(),'waarvan selout',(ring==15).sum())
o[ring>0]=ring[ring>0]
np.save('schoon.npy',o)
