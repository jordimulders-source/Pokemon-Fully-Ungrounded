# 3 verre vleugel: silhouet uit het model (>=5/9 niet-achtergrond), buitenlijn 1 px (selout 15 boven/links, zwart onder/rechts),
# binnen donkerbruin 4; zwarte modellijn tussen de veren (>=5/9 zwart) -> selout 15 als binnenlijn. Cellen naast kop/snavel blijven.
import numpy as np; from meet import *
HEAD=(2,3,5,6,7,8,9,10,11,12,13,14)
def zone(x,y): return (8<=x<=13 and 0<=y<=12) or (x==14 and 5<=y<=8)
def run(o):
    n=o.copy(); m=np.zeros((64,64),bool)
    for y in range(64):
        for x in range(64): m[y,x]=(nonbg(x,y)>=5) if zone(x,y) else o[y,x]>0
    for y in range(64):
        for x in range(64):
            if not zone(x,y): continue
            nb=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
            if any(o[a,b] in HEAD and not zone(b,a) for a,b in nb): continue
            if not m[y,x]: n[y,x]=0; continue
            up=not m[y-1,x] if y>0 else True; dn=not m[y+1,x]; lf=not m[y,x-1]; rt=not m[y,x+1]
            if dn or rt: n[y,x]=1
            elif up or lf: n[y,x]=15
            else: n[y,x]=15 if (cel(x,y)==1).sum()>=5 else 4
    return n
if __name__=='__main__':
    o=np.load('_tmp/s2.npy'); n=run(o); np.save('_tmp/s3.npy',n); print('verre vleugel px',(n!=o).sum())
