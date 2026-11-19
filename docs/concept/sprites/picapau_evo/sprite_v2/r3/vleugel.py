# 1 vleugelpunten: silhouet uit het model (cel = vleugel als >=5 van 9 natieve px niet-achtergrond), dan 1 px buitenlijn
# (zwart aan onder/rechts, selout 15 aan boven/links), binnen modeltint; zwarte modellijnen tussen overlappende veren -> donkerbruin 4.
import numpy as np; from meet import *
def zone(x,y): return 2<=y<=29 and (x>=52 or (y>=23 and x>=47))
def run(o):
    new=o.copy(); Z=[(x,y) for y in range(64) for x in range(64) if zone(x,y) and o[y,x] not in (5,6,7)]
    m=np.zeros((64,64),bool)
    for y in range(64):
        for x in range(64):
            m[y,x]= (nonbg(x,y)>=5) if zone(x,y) else o[y,x]>0
    for x,y in Z:
        if not m[y,x]: new[y,x]=0; continue
        up=y>0 and not m[y-1,x]; dn=y<63 and not m[y+1,x]; lf=x>0 and not m[y,x-1]; rt=x==63 or not m[y,x+1]
        if dn or rt: new[y,x]=1
        elif up or lf: new[y,x]=15
        else:
            b=cel(x,y)
            if (b==1).sum()>=3: new[y,x]=4
            else:
                t=toon(x,y,'b'); new[y,x]=o[y,x] if o[y,x] in (2,3,4) else (t or 3)
    return new
if __name__=='__main__':
    o=np.load('r3.npy'); n=run(o); np.save('_tmp/vl.npy',n); print('vleugel px',(n!=o).sum())
