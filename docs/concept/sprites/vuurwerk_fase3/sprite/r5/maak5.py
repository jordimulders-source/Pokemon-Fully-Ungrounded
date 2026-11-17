# r5: samenstellen. kop5_<maat>_<oog>.npy (kop5.py) + losse vlam (vlam5.py) + vuurwerkspikkels variant B opnieuw geplaatst
# (dezelfde barsten b3 en b2 van Jordi's vel, kleuren 6/7/8, alleen op lege pixels met een lege ring van 1 px, net als
# ../r3/spikkels3.py). Staat een barst door de grotere kop te veel in de weg, dan schuift hij naar de plek (binnen 4 px) waar
# de meeste pixels van de barst passen.
import sys, json, numpy as np; from PIL import Image
sys.path.insert(0,'.'); from vlam5 import vlam
PAL=json.load(open('palet.json')); B=json.load(open('../r3/ref_burst.json'))
def stempel(a,ref,cx,cy,kleur):
    H,W=a.shape; g=np.array(B[ref]); gh,gw=g.shape; ys,xs=np.where(g>0); my,mx=int(round(ys.mean())),int(round(xs.mean()))
    o=a.copy()
    for y in range(H):
        for x in range(W):
            if a[y,x]!=0: continue
            if any(0<=y+dy<H and 0<=x+dx<W and a[y+dy,x+dx]>0 for dy in (-1,0,1) for dx in (-1,0,1)): continue
            gy,gx=y-cy+my,x-cx+mx
            if 0<=gy<gh and 0<=gx<gw and g[gy,gx]>0: o[y,x]=kleur[g[gy,gx]]
    return o
K2={1:6,2:7,3:8}
def plaats(a,ref,cx,cy):
    best=None
    for dy in range(-4,5):
        for dx in range(-4,5):
            o=stempel(a,ref,cx+dx,cy+dy,K2); n=int((o!=a).sum())
            sc=(n, -abs(dx)-abs(dy))
            if best is None or sc>best[0]: best=(sc,o,(cx+dx,cy+dy))
    o0=stempel(a,ref,cx,cy,K2); n0=int((o0!=a).sum())
    if n0>=0.9*best[0][0]: return o0,(cx,cy),n0
    return best[1],best[2],best[0][0]
def maak(maat,oog,uit):
    a=np.load('kop5_%d_%d.npy'%(maat,oog)).astype(int); a=vlam(a)
    a,p3,n3=plaats(a,'b3',5,4); a,p2,n2=plaats(a,'b2',9,40)
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(uit,transparency=0)
    return a,{'b3':(p3,n3),'b2':(p2,n2)}
if __name__=='__main__':
    for maat in (115,125):
        for oog in (13,14,7,11):
            a,info=maak(maat,oog,'sprite_%d_%s.png'%(maat,{13:'geel',14:'goud',7:'magenta',11:'rood'}[oog]))
        print(maat,'spikkels',info)
