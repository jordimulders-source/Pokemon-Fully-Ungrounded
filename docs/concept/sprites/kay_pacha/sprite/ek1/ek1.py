# Kay Pacha ek1: eindkeuring (schaduw + belijning + kleurtinten, Dragonfly Cave) op r1 B.
# Run vanuit docs/concept/sprites/kay_pacha:  python3 sprite/ek1/ek1.py [T]
# Alleen uitvoering: silhouet (alpha) blijft exact gelijk, oog (9-11,18)+(11,17) blijft.
import sys, json, numpy as np; from PIL import Image
D='sprite/ek1/'
B=np.load('sprite/r1/B.npy').astype(int); S=B.copy(); H,W=S.shape; FG=S>0
T=float(sys.argv[1]) if len(sys.argv)>1 else 0.35
# ---- palet (index 15 oogpaars -> gedeeld met 13; 15 wordt groene outline base) ----
PAL=[(152,208,160),(28,30,25),
     (60,110,64),(88,148,80),(132,190,102),          # groen schaduw / basis / licht
     (134,92,26),(190,138,40),(224,178,56),(246,214,100),   # goud outline base / schaduw / basis / licht
     (122,106,70),(178,160,116),(212,196,150),(240,234,198), # creme outline base / lijn-schaduw / schaduw / licht
     (150,88,155),(248,243,237),                      # paars (strepen = oogpaars van B, exact) / wit oog
     (36,74,46)]                                      # 15: groene outline base (nieuw)
G0=15
log={}
def zet(x,y,v,why):
    if S[y,x]!=v: log.setdefault(why,[]).append((x,y,int(S[y,x]),int(v))); S[y,x]=v
OOG={(9,18),(10,18),(11,18),(11,17)}
for (x,y) in zip(*np.where(B==15)[::-1]): S[y,x]=13      # oogpaars: zelfde RGB, nu index 13
log['oogpaars index 15->13 (zelfde kleur)']=[(10,18,15,13)]
GRP={2:'g',3:'g',4:'g',13:'g',15:'g',5:'y',6:'y',7:'y',8:'y',9:'c',10:'c',11:'c',12:'c',14:'c'}
BASE={'g':G0,'y':5,'c':9}; SHAD={'g':2,'y':6,'c':10}
def tr(x,y): return not(0<=x<W and 0<=y<H) or not FG[y,x]
def rim(x,y): return FG[y,x] and any(tr(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
def groep(x,y,R=2,orig=B):
    """groep van een pixel; zwart -> meerderheid van niet-zwarte buren (gewogen naar afstand)"""
    v=orig[y,x]
    if v in GRP: return GRP[v]
    sc={}
    for dy in range(-R,R+1):
        for dx in range(-R,R+1):
            xx,yy=x+dx,y+dy
            if (dx or dy) and 0<=xx<W and 0<=yy<H and orig[yy,xx] in GRP:
                g=GRP[orig[yy,xx]]; sc[g]=sc.get(g,0)+1/(dx*dx+dy*dy)
    return max(sc,key=sc.get) if sc else None
# ---- 1. binnenlijnen: zwart binnen het silhouet -> outline base van het voorste onderdeel (masker > mantel > lijf) ----
#      uitzondering: ooglid/wenkbrauwlijn boven het oog (deel van het oog, Gen 3-ogen hebben een zwarte lidlijn)
LID={(8,17),(9,17),(10,17),(9,16),(10,16),(11,16),(12,16),(13,16),(12,17)}
for y in range(H):
    for x in range(W):
        if B[y,x]!=1 or rim(x,y) or (x,y) in LID: continue
        gs=set()
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                xx,yy=x+dx,y+dy
                if 0<=xx<W and 0<=yy<H and B[yy,xx] in GRP: gs.add(GRP[B[yy,xx]])
        g='c' if 'c' in gs else 'y' if 'y' in gs else 'g' if 'g' in gs else groep(x,y,3)
        zet(x,y,BASE[g],'binnenlijn zwart -> outline base voorste onderdeel')
# ---- 2. buitenlijn: richting van de rand; zwart (outline shadow) alleen waar hij naar rechtsonder wijst ----
def normaal(x,y,R=3):
    nx=ny=0.0
    for dy in range(-R,R+1):
        for dx in range(-R,R+1):
            if (dx or dy) and tr(x+dx,y+dy): w=1/(dx*dx+dy*dy); nx+=dx*w; ny+=dy*w
    n=(nx*nx+ny*ny)**.5 or 1; return nx/n,ny/n
RIM=[(x,y) for y in range(H) for x in range(W) if rim(x,y) and (x,y) not in OOG]
cls={}
for (x,y) in RIM:
    if B[y,x]==13 and y<25: continue      # ver oog (paars) aan de koprand: blijft
    nx,ny=normaal(x,y); s=(nx+ny)/2**.5
    cls[(x,y)]=('zwart' if s>T else 'base', s)
# 2a. geen om-en-om: rim-pixel waarvan alle rim-buren (8) de andere klasse hebben -> omdraaien (2x)
for it in range(2):
    new={}
    for (x,y),(c,s) in cls.items():
        nb=[cls[(x+dx,y+dy)][0] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and (x+dx,y+dy) in cls]
        if nb and all(n!=c for n in nb) and len(nb)>=2: new[(x,y)]=('base' if c=='zwart' else 'zwart',s)
    cls.update(new)
for (x,y),(c,s) in cls.items():
    g=groep(x,y)
    if c=='zwart': zet(x,y,1,'buitenlijn: outline shadow zwart (schaduwkant)')
    else:
        v=BASE[g]
        # outline highlight: op de meest belichte stukken (rand wijst naar linksboven) de schaduwtint, binnen de lijn
        if s<-0.88 and g in('c','y','g'):
            inn=[S[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if not tr(x+dx,y+dy) and not rim(x+dx,y+dy)]
            if inn and all(GRP.get(i)==g and i not in (2,5,9,15,10) for i in inn): v=SHAD[g]
        zet(x,y,v,'buitenlijn: outline base/highlight eigen tint (lichtkant)')
np.save(D+'stap1.npy',S)
def save(arr,name):
    im=Image.fromarray(arr.astype('uint8'),'P'); p=[]
    for c in PAL: p+=list(c)
    im.putpalette(p); im.save(D+name,transparency=0)
if __name__=='__main__':
    save(S,'stap1.png')
    assert ((S>0)==FG).all(),'silhouet gewijzigd'
    for (x,y) in [(9,18),(11,18),(11,17)]: assert S[y,x]==14
    assert S[18,10]==13
    for k,v in log.items(): print(f'{k}: {len(v)} px')
    json.dump(log,open(D+'stap1_log.json','w'))
