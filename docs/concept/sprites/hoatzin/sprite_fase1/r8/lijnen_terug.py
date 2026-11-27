# Ronde 8 (Jordi op r7: "de lijn moet niet verdwijnen maar minder zwart"). Basis r7; de binnenlijnen tussen vleugel, lijf en poot
# terug op precies de r6-pixels, maar zachter: tegen het lijf 13 (donkerste dons-schaduw), tegen grijze delen (poot) 12.
# Veerlijnen in de vleugel terug zoals r6 (12). Slagschaduw van r7 blijft. Buitenlijn en silhouet ongewijzigd.
import numpy as np
from PIL import Image
im7=Image.open('../r7/kuiken_r7.png'); a7=np.array(im7); a6=np.array(Image.open('../r6/kuiken_r6.png'))
W=np.load('../r6/vleugel.npy'); out=a7.copy(); n={}
N4=((-1,0),(1,0),(0,-1),(0,1))
DONS={2,3,4,6,7,13}
tr=lambda y,x: not (0<=y<64 and 0<=x<64) or a7[y,x]==0
for y,x in zip(*np.nonzero(W)):
    buiten=[(dy,dx) for dy,dx in N4 if not W[y+dy,x+dx]]
    if buiten and not any(tr(y+dy,x+dx) for dy,dx in buiten):          # binnenlijn vleugelrand (r6: 1 of 12)
        assert a6[y,x] in (1,12),(x,y,a6[y,x])
        tegen_lijf=y<=45   # tot en met rij 45 grenst de vleugel aan het lijf (ook waar r6 daar zwart had), daaronder aan de poten: één tint per lijn
        v=13 if tegen_lijf else 12; k='lijn tegen lijf (13)' if tegen_lijf else 'lijn tegen poot (12)'
    elif not buiten and a6[y,x]==12: v=12; k='veerlijn (12)'
    else: continue
    if out[y,x]!=v: out[y,x]=v; n[k]=n.get(k,0)+1
assert ((out>0)!=(a7>0)).sum()==0
o=Image.fromarray(out,'P'); o.putpalette(im7.getpalette()); o.save('kuiken_r8.png',transparency=0)
print(n,'zwart %',round((out==1).sum()/(out>0).sum()*100,1),'r6 zwart %',round((a6==1).sum()/(a6>0).sum()*100,1))
