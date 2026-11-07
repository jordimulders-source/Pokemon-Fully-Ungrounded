"""kleur3: open randen, losse pixels (geen 8-buur met dezelfde index), diff t.o.v. kleur2 B per zone."""
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/dj_rotom/'
a=np.array(Image.open(D+'kleur3/dj_rotom.png')); b=np.array(Image.open(D+'kleur2/dj_rotom_B.png'))
im=Image.open(D+'kleur3/dj_rotom.png'); print(im.mode,im.size,'transparency',im.info.get('transparency'),'px',int((a>0).sum()))
op=[];los=[]
for y in range(64):
    for x in range(64):
        v=a[y,x]
        if not v: continue
        n4=[a[yy,xx] if 0<=yy<64 and 0<=xx<64 else 0 for yy,xx in((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
        if 0 in n4 and v!=1: op.append((x,y,int(v)))
        n8=[a[yy,xx] for yy in range(max(0,y-1),min(64,y+2)) for xx in range(max(0,x-1),min(64,x+2)) if (yy,xx)!=(y,x)]
        if v not in n8: los.append((x,y,'.123456789abcdef'[v]))
print('open randen:',op); print('losse pixels (x,y,index):',los)
Z={'1 bliksem x19-30 y14-25':(slice(14,26),slice(19,31)),
   '2 kop x31-32 y32-57':(slice(32,58),slice(31,33)),
   '3 conussen rechts x40-50 y34-55':(slice(34,56),slice(40,51)),
   '3 conussen links x6-12 y41-53':(slice(41,54),slice(6,13)),
   '4 hoek rechtsonder x55-59 y59-60':(slice(59,61),slice(55,60)),
   '5 snoer (17,51)':(slice(51,52),slice(17,18)),
   '5 schaduw kop y55-56 x17-32 + x32 y45-56':None}
d=(a!=b); used=np.zeros_like(d)
for k,z in Z.items():
    m=np.zeros_like(d)
    if z is None: m[55:57,17:33]=True; m[45:57,32]=True
    else: m[z]=True
    m&=~used; used|=m
    print('%-45s %3d px'%(k,int((d&m).sum())))
print('buiten de zones gewijzigd:',int((d&~used).sum()),list(zip(*np.nonzero(d&~used))))
print('totaal gewijzigd t.o.v. B:',int(d.sum()),' alpha-verschil t.o.v. B:',int(((a>0)!=(b>0)).sum()))
