# r2: twinkels (zoals r1: plusje op de gemeten modelplek), lijfspikkels (afw. 1, zoals r1) en vuurwerkspikkels om de kop
# (afw. 2) in varianten. Barsten letterlijk van Jordi's vel (ref_burst.json, natief raster 1:1), alleen op lege pixels
# bij B met 1 px afstand tot de sprite (A en C mogen tegen de kop aan: de barst komt uit de kop). Kleuren: donker -> 6, midden -> 7, fel -> 8 (roze/magenta van het model).
#  A: kleine roze barst 'b2' (midden onder) gecentreerd op de kop: compact, komt niet tot de rand
#  B: twee losse barstjes naast de kop in de vrije ruimte: 'b3' (linksboven op het vel) links boven de kop en 'b2' linksonder
#  C: voorstel maker: grote barst 'b1' op de kop, maar alleen binnen straal 13 rond het kopmidden (stralen die uit de kop
#     schieten, zonder de stofrand tot aan de canvasrand)
import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet_r2.json')); a0=np.load('r2_pijl.npy'); H,W=a0.shape
KLEUR={1:6,2:7,3:8}; KOP=(13,16)
B=json.load(open('ref_burst.json'))
def basis():
    a=a0.copy()
    # twinkels: losse restjes rond de 5 modelplekken weg, plusje erop
    T=[(8,6),(5,9),(29,18),(20,26),(16,29)]
    for cx,cy in T:
        for y in range(cy-2,cy+3):
            for x in range(cx-2,cx+3):
                if a[y,x] in (3,4,5) and not any(a[y+dy,x+dx] in (2,7) for dy in (-1,0,1) for dx in (-1,0,1) if 0<=y+dy<H and 0<=x+dx<W):
                    # alleen losse twinkelpixels (geen kop: de kop heeft bruine/roze buren)
                    if sum(1 for dy in (-1,0,1) for dx in (-1,0,1) if a[y+dy,x+dx]>0)<=4: a[y,x]=0
        for dx,dy,v in ((0,0,5),(1,0,3),(-1,0,3),(0,1,3),(0,-1,3)): a[cy+dy,cx+dx]=v
    # lijfspikkels (afw. 1): 2 px straal (lichtroze -> fel creme), van de kop af
    for (i,j,_) in json.load(open('glitter_plekken.json')):
        dx=int(np.sign(i-KOP[0])); dy=int(np.sign(j-KOP[1]))
        for (x,y,v) in ((i,j,5),(i-dx,j-dy,8)):
            if a0[y,x] in (6,7,8,11,12): a[y,x]=v
    return a
def stempel(a,ref,cx,cy,maxr=None,gat=True):
    g=np.array(B[ref]); gh,gw=g.shape; ys,xs=np.where(g>0); my,mx=int(round(ys.mean())),int(round(xs.mean()))
    o=a.copy(); n=0
    for y in range(H):
        for x in range(W):
            if a[y,x]!=0: continue
            if gat and any(0<=y+dy<H and 0<=x+dx<W and a[y+dy,x+dx]>0 for dy in (-1,0,1) for dx in (-1,0,1)): continue
            if maxr and (x-cx)**2+(y-cy)**2>maxr**2: continue
            gy,gx=y-cy+my,x-cx+mx
            if 0<=gy<gh and 0<=gx<gw and g[gy,gx]>0: o[y,x]=KLEUR[g[gy,gx]]; n+=1
    return o,n
a=basis(); np.save('r2_basis.npy',a)
var={'A':[('b2',13,16,None,False)],'B':[('b3',5,4,None,True),('b2',9,40,None,True)],'C':[('b1',13,16,13,False)]}
for k,st in var.items():
    o=a.copy(); tot=0
    for (ref,cx,cy,r,gat) in st: o,n=stempel(o,ref,cx,cy,r,gat); tot+=n
    im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s.png'%k,transparency=0)
    print(k,'spikkelpixels',tot)
