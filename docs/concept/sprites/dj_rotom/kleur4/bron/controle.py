"""kleur4: open randen, losse pixels, diff t.o.v. kleur3 binnen/buiten de zones (bliksem x17-31 y0-25, ogen links x18-23 y35-41, rechts x25-31 y34-41)."""
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/dj_rotom/'
a=np.array(Image.open(D+'kleur4/dj_rotom.png')); b=np.array(Image.open(D+'kleur3/dj_rotom.png'))
im=Image.open(D+'kleur4/dj_rotom.png'); print(im.mode,im.size,'transparency',im.info.get('transparency'),'px',int((a>0).sum()))
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
d=a!=b; Z={'bliksem x17-31 y0-25':(slice(0,26),slice(17,32)),'oog links x18-23 y35-41':(slice(35,42),slice(18,24)),'oog rechts x25-31 y34-41':(slice(34,42),slice(25,32))}
used=np.zeros_like(d)
for k,z in Z.items():
    m=np.zeros_like(d); m[z]=True; used|=m; print('%-28s %3d px gewijzigd'%(k,int((d&m).sum())))
print('buiten de zones gewijzigd:',int((d&~used).sum()))
print('alpha-verschil t.o.v. kleur3:',int(((a>0)!=(b>0)).sum()))
