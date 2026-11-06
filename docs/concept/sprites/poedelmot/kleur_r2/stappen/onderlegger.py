# onderlegger: per pixel de dichtstbijzijnde vacht/vleugeltint uit de gids (alleen startpunt)
import numpy as np
from PIL import Image
from palet import PAL, CH
g=np.array(Image.open('/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/silhouet/gids_gemiddeld.png')).astype(int)
keuze='123456789ABC'
out=[]
for y in range(64):
    row=''
    for x in range(64):
        if g[y,x,3]==0: row+='.'; continue
        c=g[y,x,:3]
        best=min(keuze,key=lambda k: sum((c-np.array(PAL[CH.index(k)]))**2))
        row+=best
    out.append(row)
open('onderlegger.txt','w').write('\n'.join(out)+'\n')
