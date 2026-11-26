# Oogvarianten voor de kudu (r3). Pixels 1-op-1 uit de bron, alleen omgekleurd naar het kudupalet; geplaatst met het oogmidden
# op het oogmidden van het model (x283,y368 -> lokaal raster (12,23)).
# a: impala (af, oog B3) box x18-24,y22-26, oogmidden (21,24)
# b: Stantler anim_front_gba.png box x23-29,y23-27, oogmidden (26,26)
# c: reductie van het modeloog met lid (half dicht): lidlijn rij 22 x10-13, daaronder wit|pupil|wit|ooghoek
import numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
DOEL=(12,23)
def box(pad,bx0,by0,bx1,by1,mid,kaart):
    a=np.asarray(Image.open(pad)); dx,dy=DOEL[0]-mid[0],DOEL[1]-mid[1]; out=[]
    for y in range(by0,by1+1):
        for x in range(bx0,bx1+1):
            v=int(a[y,x])
            if v==0: continue
            out.append((x+dx,y+dy,kaart[v],'oog %s: bronpixel (%d,%d) index %d'%(pad.split('/')[-2],x,y,v)))
    return out
IMP={1:'0',2:'K',3:'D',4:'D',5:'M',6:'M',7:'L',8:'W',9:'A',10:'A',11:'3',12:'4'}
STA={1:'W',2:'L',3:'M',4:'D',5:'0',7:'L',8:'L',9:'L',10:'M',12:'4',13:'3',14:'K',15:'0'}
def variant(v):
    if v=='a': return box(R+'docs/concept/sprites/impala_lijn/impala/af/impala.png',18,22,24,26,(21,24),IMP)
    if v=='b': return box(R+'graphics/pokemon/stantler/anim_front_gba.png',23,23,29,27,(26,26),STA)
    return [(x,22,'0','oog c: lidlijn uit het model') for x in range(10,14)]+[(10,23,'W','oog c: oogwit'),(11,23,'0','oog c: pupil'),(12,23,'W','oog c: oogwit'),(13,23,'0','oog c: ooghoek')]
