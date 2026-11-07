"""kleur5: open randen, losse pixels (nieuw t.o.v. kleur4?)."""
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/dj_rotom/'
def los(a):
    out=set()
    for y in range(64):
        for x in range(64):
            v=a[y,x]
            if not v: continue
            n8=[a[yy,xx] for yy in range(max(0,y-1),min(64,y+2)) for xx in range(max(0,x-1),min(64,x+2)) if (yy,xx)!=(y,x)]
            if v not in n8: out.add((x,y,'.123456789abcdef'[v]))
    return out
a=np.array(Image.open(D+'kleur5/dj_rotom.png')); k=np.array(Image.open(D+'kleur4/dj_rotom.png'))
im=Image.open(D+'kleur5/dj_rotom.png'); print(im.mode,im.size,'transparency',im.info.get('transparency'),'px',int((a>0).sum()))
op=[(x,y,int(a[y,x])) for y in range(64) for x in range(64) if a[y,x] and a[y,x]!=1 and any(not(0<=yy<64 and 0<=xx<64) or a[yy,xx]==0 for yy,xx in((y-1,x),(y+1,x),(y,x-1),(y,x+1)))]
print('open randen:',op)
L5=los(a); L4=los(k)
print('losse pixels nieuw t.o.v. kleur4:',sorted(L5-L4)); print('losse pixels opgelost:',sorted(L4-L5)); print('losse pixels totaal:',len(L5))
