# Onderlaag -> sprite: alleen nette randen en palet, geen hertekening.
# 1) kleine tintvlekjes (< 3 px, binnen dezelfde kleurgroep) nemen de meest voorkomende buurtint van die groep aan;
# 2) losse 1-px uitsteeksels/gaten aan de buitenrand weg (alleen pixel met <=1 dekkende 4-buur);
# 3) buitenlijn op de bestaande randpixels: lichtkant (lucht links/boven) = donkerste tint van de eigen groep (selout),
#    schaduwkant (lucht rechts/onder) = zwart; bleek groen (wolken, kleine geest) altijd donkergroen (gekleurde omlijning);
# 4) losse zwarte pixel midden in een vlak (raakt geen andere lijn/rand) -> buurtint, behalve in de oogzone (pupillen).
import numpy as np; from PIL import Image; import sys
IN=sys.argv[1] if len(sys.argv)>1 else 'onderlaag.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'sprite.png'
im=Image.open(IN); P=im.getpalette()[:3*16]; o=np.array(im).astype(int)
GRP={1:'K',2:'F',3:'F',4:'P',5:'P',6:'P',7:'R',8:'R',9:'R',10:'S',11:'S',12:'S'}
SELOUT={'F':6,'P':6,'R':9,'S':12,'K':1}
OOG=(2,26,27,38)   # oogzone in spritecoordinaten x0,x1,y0,y1 (pupillen blijven)
H,W=o.shape
N4=[(0,1),(1,0),(0,-1),(-1,0)]; N8=N4+[(1,1),(1,-1),(-1,1),(-1,-1)]
def nb(y,x,d=N8):
    for dy,dx in d:
        if 0<=y+dy<H and 0<=x+dx<W: yield y+dy,x+dx,o[y+dy,x+dx]
def clusters(mask):
    lab=np.zeros(mask.shape,int); n=0; out=[]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n; cl=[]
        while st:
            cy,cx=st.pop(); cl.append((cy,cx))
            for dy,dx in N8:
                ny,nx=cy+dy,cx+dx
                if 0<=ny<H and 0<=nx<W and mask[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; st.append((ny,nx))
        out.append(cl)
    return out
# 0) wolken en kleine geest egaal: bleekgroene binnenpixels nemen de meest voorkomende bleke tint uit hun 3x3 aan
#    (vlakken worden egaal op hun modelplek; vorm en plek van licht/donker blijven die van het model)
for _ in range(int(sys.argv[3]) if len(sys.argv)>3 else 2):
    n=o.copy()
    for y in range(H):
        for x in range(W):
            if y<=13 or (42<=x<=52 and 42<=y<=54): continue   # kleine geest en vaag achterwiel: lijnen van het model houden
            if o[y,x] in (4,5,6):
                c=[v for _,_,v in nb(y,x) if v in (4,5,6)]+[o[y,x]]
                if len(c)>=7:
                    m=max(set(c),key=c.count)
                    if c.count(m)>c.count(o[y,x]): n[y,x]=m
    o=n
for ronde in range(3):
    # 2) uitsteeksels
    for y in range(H):
        for x in range(W):
            if x>=44 and o[y,x] in (4,5,6): continue   # wolkpunten/slierten rechts: dunne punten van het model houden
            if o[y,x] and sum(1 for _,_,v in nb(y,x,N4) if v)<=1 and sum(1 for _,_,v in nb(y,x) if v)<=2: o[y,x]=0
    # 1) kleine tintvlekjes per tint (niet zwart, niet de lichtste felgroene tint = glans)
    for t in range(2,13):
        if t==2: continue
        for cl in clusters(o==t):
            if len(cl)>=3: continue
            for (y,x) in cl:
                g=GRP[t]; c=[v for _,_,v in nb(y,x) if v and v!=t and GRP.get(v)==g]
                if c: o[y,x]=max(set(c),key=c.count)
    # 4) losse zwarte pixels
    for (cl) in clusters(o==1):
        if len(cl)>1: continue
        y,x=cl[0]
        if OOG[0]<=x<=OOG[1] and OOG[2]<=y<=OOG[3]: continue
        if any(v==0 for _,_,v in nb(y,x,N4)): continue
        c=[v for _,_,v in nb(y,x) if v>1]
        if c: o[y,x]=max(set(c),key=c.count)
# 3) buitenlijn
r=o.copy()
for y in range(H):
    for x in range(W):
        t=o[y,x]
        if not t: continue
        lucht=[(dy,dx) for dy,dx in N4 if not (0<=y+dy<H and 0<=x+dx<W) or o[y+dy,x+dx]==0]
        if not lucht: continue
        g=GRP[t]
        if g=='P': r[y,x]=6; continue
        schaduw=any(d in [(0,1),(1,0)] for d in lucht)
        r[y,x]=1 if schaduw else SELOUT[g]
o=r
for _ in range(2):
    for t in range(3,13):
        if t in (6,9,12): pass
        for cl in clusters(o==t):
            if len(cl)>=3: continue
            for (y,x) in cl:
                if any(not(0<=y+dy<H and 0<=x+dx<W) or o[y+dy,x+dx]==0 for dy,dx in N4): continue
                g=GRP[t]; c=[v for _,_,v in nb(y,x) if v and v!=t and GRP.get(v)==g]
                if c: o[y,x]=max(set(c),key=c.count)
out=Image.fromarray(o.astype('uint8'),'P'); out.putpalette(P+[0]*(768-len(P))); out.save(OUT,transparency=0)
with open('raster.txt','w') as f:
    f.write('# index per pixel (0 = transparant, hex), palet:\n')
    for i in range(13): f.write('# %X %s\n'%(i,tuple(P[3*i:3*i+3])))
    for row in o: f.write(''.join('%X'%v if v else '.' for v in row)+'\n')
print('kleuren',len(np.unique(o)),'(incl. transparant)')
