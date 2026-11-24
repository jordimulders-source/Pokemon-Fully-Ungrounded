# kraag_proef.py: Bibarel-rechterwang (anim_front.png frame 1, x30-38 y12-24) pixel voor pixel, met zijn eigen tinten/patroon
# (2->bruin-midden 4, 4->bruin-donker 3, 1->bruinlijn 2, 3->zwart 1; crème van zijn gezichtsplaat niet). Geen opvulling, geen middeling.
# Proef 1: +4/+1, alleen binnen de r1-kraagzone rechts (x35-41, y15-27), rest r1.
# Proef 2: +5/+1, bolletjes mogen 1-2 px over stam/schouder vallen (niet over achtergrond, gezicht of klep): silhouet gelijk.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image
B=np.array(Image.open('../../../../graphics/pokemon/bibarel/anim_front.png'))[:64].astype(int)
MAP={2:4,4:3,1:2,3:1}
basis=laad('sprite_r3/sprite.png')
GEZ=np.zeros((64,64),bool); GEZ[14:28,20:35]=True
def proef(dx,dy,over):
    o=basis.copy(); n=0
    zone=np.zeros((64,64),bool); zone[15:28,35:42]=True
    for y in range(12,25):
        for x in range(30,39):
            v=B[y,x]; X,Y=x+dx,y+dy
            if v not in MAP or not (0<=X<64 and 0<=Y<64) or Y<15 or GEZ[Y,X] or o[Y,X]==0: continue
            if not over and not zone[Y,X]: continue
            if over and X>44: continue
            if o[Y,X]!=MAP[v]: o[Y,X]=MAP[v]; n+=1
    return o,n
p1,n1=proef(4,1,False); p2,n2=proef(5,1,True)
d1=(p1!=basis); d2=(p2!=basis)
print('proef 1:',n1,'px; buiten kraagzone rechts:',int((d1&~np.pad(np.ones((13,7),bool),((15,36),(35,22)))).sum()))
print('proef 2:',n2,'px; waarvan buiten de kraagzone (over stam/schouder):',int((d2&~np.pad(np.ones((13,7),bool),((15,36),(35,22)))).sum()),'| achtergrond geraakt:',int((d2&(basis==0)).sum()))
opslaan(p1,'sprite_r3/kraag_proef.png',12); opslaan(p2,'sprite_r3/kraag_proef2.png',12)
