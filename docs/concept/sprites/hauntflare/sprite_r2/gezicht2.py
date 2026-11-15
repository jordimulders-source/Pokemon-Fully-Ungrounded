# Ronde 2: Haunters gezicht 1-op-1 (schaal 1,0, niets geschrapt). Alleen de gezichtspixels:
# oogwit (f), pupil/zwarte lijn (e,d), donkere lijn (5) en mond (a,9) + tanden (huid in de mond).
# e/5 alleen binnen 1 px van oogwit/pupil/mond/tand (zo valt Haunters kaak- en hoofdomtrek weg).
# Klassen: 1 zwart, 2 donkere lijn, 3 oogwit, 4 mond donker, 5 mond licht, 6 tand. Schrijft gezicht_r2.npy (+12x).
from PIL import Image; import numpy as np
from scipy import ndimage as nd
S='docs/concept/sprites/hauntflare/sprite_r2/'
g=np.array(Image.open('graphics/pokemon/haunter/anim_front.png'))[:64].astype(int)
X0,Y0,X1,Y1=12,27,35,46   # tot en met Haunter-y45 (y46 = kinomtrek)
sub=g[Y0:Y1,X0:X1]
huid=np.isin(sub,[2,3,4])
mond=np.isin(sub,[10,9])
# tanden: huid in de mondzone (Haunter x15-33, y38-45) met >=2 4-buren die mondlijn/mond zijn en mond (a/9) in de 8-buurt
tand=np.zeros_like(huid)
for y in range(38-Y0,46-Y0):
    for x in range(15-X0,34-X0):
        if not huid[y,x]: continue
        n4=[sub[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))]
        if sum(v in (14,5,10,9) for v in n4)>=2 and mond[y-1:y+2,x-1:x+2].any(): tand[y,x]=True
kern=np.isin(sub,[15,13,10,9])|tand
dicht=nd.binary_dilation(kern,np.ones((3,3)))
C=np.zeros_like(sub)
C[(sub==5)&dicht]=2; C[np.isin(sub,[14,13])&dicht]=1; C[sub==15]=3; C[sub==10]=4; C[sub==9]=5; C[tand]=6
np.save(S+'gezicht_r2.npy',C)
ys,xs=np.where(C>0); print('inhoud Haunter x',xs.min()+X0,'-',xs.max()+X0,' y',ys.min()+Y0,'-',ys.max()+Y0,' px',int((C>0).sum()))
pal={0:(200,156,205),1:(16,16,16),2:(82,65,98),3:(255,255,255),4:(180,24,98),5:(222,90,164),6:(172,131,197)}
im=np.array([[pal[v] for v in r] for r in C],'uint8')
Image.fromarray(im).resize((C.shape[1]*12,C.shape[0]*12),Image.NEAREST).save(S+'gezicht_r2_extractie_12x.png')
