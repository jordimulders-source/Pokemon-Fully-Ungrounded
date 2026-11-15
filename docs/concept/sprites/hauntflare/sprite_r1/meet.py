# Controles: tintgebruik, tintvlakjes < 3 px, lichte kleur op de buitenrand, zwart/donker om-en-om op de rand,
# en silhouetdiff (alpha) tegen het verkleinde model (model64.png).
import json
from PIL import Image; import numpy as np
from scipy import ndimage as nd
from collections import Counter
S='docs/concept/sprites/hauntflare/sprite_r1/'
o=np.array(Image.open(S+'hauntflare_r1.png')).astype(int)
M=np.asarray(Image.open(S+'model64.png').convert('RGB')).astype(int)
print('kleuren (incl. transparant):',len(np.unique(o)),sorted(Counter(o.flatten().tolist()).items()))
# silhouet
GZ=np.load(S+'gezicht_masker.npy')
ms=~(M.min(2)>=0xf0); ss=o>0
d=ms!=ss
print('silhouetdiff (alpha) tegen model64:',int(d.sum()),[(int(x),int(y)) for y,x in zip(*np.where(d))])
# tintvlakjes
G={'ring':{2,3,4},'bol':{5,6,7,8,9},'vlam/hand':{5,10,11,12,13,15}}
for nm,ts in G.items():
    klein=[]
    for t in ts:
        l,k=nd.label((o==t)&~GZ,np.ones((3,3)))
        for i in range(1,k+1):
            n=(l==i).sum()
            if n<3:
                y,x=np.where(l==i); klein.append((t,int(x[0]),int(y[0]),int(n)))
    print('tintvlakjes <3 px',nm,len(klein),klein)
rand=nd.binary_dilation(o==0,[[0,1,0],[1,1,1],[0,1,0]])&(o!=0)
print('buitenrand:',sorted(Counter(o[rand].tolist()).items()))
licht=[(int(x),int(y),int(o[y,x])) for y,x in zip(*np.where(rand&np.isin(o,[7,8,9,13,14,15,4])))]
print('lichte kleur op de buitenrand:',licht)
# om-en-om: randpixels langs de rand waarvan buren (op de rand) afwisselend 1 en donker (2/5/10) zijn
om=0; lst=[]
for y,x in zip(*np.where(rand&(o==1))):
    for ey,ex in ((0,1),(1,0),(1,1),(1,-1)):
        y1,x1,y2,x2=y+ey,x+ex,y+2*ey,x+2*ex
        if 0<=y2<64 and 0<=x2<64 and rand[y1,x1] and rand[y2,x2] and o[y1,x1] in (2,5,10) and o[y2,x2]==1:
            om+=1; lst.append((int(x1),int(y1)))
print('zwart-donker-zwart op de rand:',om,lst)
