# r3 punt 4: vuurwerkspikkels op de r3-kop (gezicht V of W). Barsten letterlijk van Jordi's vel (ref_burst.json, natief 1:1),
# alleen op lege pixels met een lege ring van 1 px tot de sprite (geen opaak in de 8 buren).
#  A: b2 (midden onder) op het kopmidden; C: b1 (linksonder) op het kopmidden, straal <= 16  -> kleuren r3: donker 6,
#     midden lichtste roze 8, fel goud 13 (felle eindpixels)
#  B: ongewijzigd t.o.v. r2: b3 (linksboven) links boven de kop + b2 linksonder; kleuren 6/7/8
import json, numpy as np; from PIL import Image
PAL=json.load(open('palet_r2.json')); B=json.load(open('ref_burst.json'))
def stempel(a,ref,cx,cy,kleur,maxr=None):
    H,W=a.shape; g=np.array(B[ref]); gh,gw=g.shape; ys,xs=np.where(g>0); my,mx=int(round(ys.mean())),int(round(xs.mean()))
    o=a.copy()
    for y in range(H):
        for x in range(W):
            if a[y,x]!=0: continue
            if any(0<=y+dy<H and 0<=x+dx<W and a[y+dy,x+dx]>0 for dy in (-1,0,1) for dx in (-1,0,1)): continue
            if maxr and (x-cx)**2+(y-cy)**2>maxr**2: continue
            gy,gx=y-cy+my,x-cx+mx
            if 0<=gy<gh and 0<=gx<gw and g[gy,gx]>0: o[y,x]=kleur[g[gy,gx]]
    return o
K3={1:6,2:8,3:13}; K2={1:6,2:7,3:8}
VAR={'A':[('b2',13,16,K3,None)],'B':[('b3',5,4,K2,None),('b2',9,40,K2,None)],'C':[('b1',13,16,K3,16)]}
for g in 'VW':
    base=np.load('r3_kop_%s.npy'%g)
    for k,st in VAR.items():
        o=base.copy()
        for (ref,cx,cy,kl,r) in st: o=stempel(o,ref,cx,cy,kl,r)
        im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s_%s.png'%(g,k),transparency=0)
        print(g,k,'spikkels',int((o!=base).sum()))
