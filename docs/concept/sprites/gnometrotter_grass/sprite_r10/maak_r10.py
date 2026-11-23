# maak_r10.py: Gnometrotter Grass r10 = r9, alleen kleur/schaduw van stok, bladmuts, bladbaard/-snor en haar (blad).
# Vorm/omtrek blijven: lijnpixels (5, 1, buitenrand) blijven staan; alleen vultinten worden opnieuw verdeeld.
# Muts en bladeren: tint uit de modelhelderheid (meet10.py -> hel10.npy), per vlak gekwantiseerd; stok: cilinder (licht links).
# Palet: groene ramp gelijkmatig gemaakt (alleen 12-14). Log: log_r10.txt.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
bim=Image.open('../sprite_r9/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
h=np.load('hel10.npy')
GROEN=[5,12,13,14]; BRUIN=[2,3,4]
yy,xx=np.mgrid[0:64,0:64]
# ---- zones ----
groen=np.isin(B,GROEN)
haarR=ndimage.binary_dilation(ndimage.label(B==14)[0]==ndimage.label(B==14)[0][17,36],np.ones((3,3)))&groen&(yy<=22)
haarL=groen&(xx<=18)&(yy>=13)&(yy<=19)
muts=groen&(yy<=16)&~haarR&~haarL&(xx<=46)
baard=groen&(yy>=17)&(xx<=32)&~haarL&~haarR
stok=np.isin(B,BRUIN)&(xx<=13)&(yy>=36)
ZONES={'stok':stok,'muts':muts,'baard':baard,'haar L':haarL,'haar R':haarR}
# ---- muts en bladeren per vlak: vlakken = samenhangende vulpixels tussen de nerf-/omlijningslijnen (5) uit het model;
#      binnen elk vlak de modelhelderheid (3x3 gemiddeld binnen het vlak, tegen ruis) rangschikken en in banden verdelen ----
def vlakken(m):
    vul=m&np.isin(B,[12,13,14]); Lf,nf=ndimage.label(vul); return Lf,nf
def glad(Lf,i):
    c=Lf==i; ys,xs=np.nonzero(c); hs={}
    for x,y in zip(xs,ys):
        v=[h[y+dy,x+dx] for dx in (-1,0,1) for dy in (-1,0,1) if c[y+dy,x+dx] and h[y+dy,x+dx]>0]
        hs[(x,y)]=np.mean(v) if v else h[y,x]
    return hs
def verdeel(hs,banden):
    """banden: lijst (aandeel, tint) van licht naar donker"""
    ks=sorted(hs,key=lambda p:-hs[p]); n=len(ks); i=0; out={}
    for j,(aand,t) in enumerate(banden):
        k=n if j==len(banden)-1 else int(round(aand*n))
        for p in ks[i:i+k]: out[p]=t
        i+=k
    return out
# muts: één bolling; het lichte linkerblad (was 13, model lum ±100-133) krijgt bogen rond een hooglicht linksboven
# (model: lichtst langs de linkerbovenrand), het rechterblad (was 12, model lum ±70-89) blijft schaduw met een lichte rand
# langs zijn nerf linksboven en een sikkel 5 langs de buitenrand rechts.
for y,x in zip(*np.nonzero(muts&np.isin(B,[12,13,14]))):
    if B[y,x] in (13,14):
        r=np.hypot(x-24.0,(y-4.5)*1.1)
        O[y,x]=14 if r<3.6 else (13 if r<8.8 else 12)
    else:
        nb=[B[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        if B[y,x+1]==1 or B[y-1,x+1]==1 or B[y+1,x+1]==1: O[y,x]=5          # sikkel tegen de zwarte rand rechts
        elif B[y,x-1]==5 or B[y-1,x]==5: O[y,x]=13                         # lichte rand langs de nerf (linksboven)
        else: O[y,x]=12
# bladeren (baard, haar): per blad (vlak tussen de nerven) een lichte helft linksboven en schaduw rechtsonder
for m in (baard,haarL,haarR):
    Lf,nf=vlakken(m)
    for i in range(1,nf+1):
        ys,xs=np.nonzero(Lf==i); n=len(ys)
        orde=np.argsort(0.6*xs+0.8*ys+1e-3*xs)
        banden=[(0.5,14),(0.3,13),(0.2,12)] if n>=8 else [(0.6,14),(0.4,13)]
        j=0
        for k,(aand,t) in enumerate(banden):
            cnt=n-j if k==len(banden)-1 else int(round(aand*n))
            for q in orde[j:j+cnt]: O[ys[q],xs[q]]=t
            j+=cnt
RAND=np.zeros((64,64),bool)
# ---- stok: cilinder zoals Rock af (2 selout | licht | midden | donker | zwart): per rij links 4, midden 3, rechts 2 ----
for y,x in zip(*np.nonzero(stok)):
    if any(B[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): RAND[y,x]=True   # buitenrand (selout) blijft
tak=lambda x,y: 41<=y<=45 and (x<=5 or x>=10)
for y in range(36,60):
    xs=[x for x in range(0,14) if stok[y,x] and not RAND[y,x] and not tak(x,y)]
    if not xs: continue
    for r in np.split(np.array(xs),np.nonzero(np.diff(xs)>1)[0]+1):
        n=len(r); nl=max(1,int(np.ceil(n*0.45)))
        for i,x in enumerate(r): O[y,x]=4 if i<nl else (2 if (n>=4 and i==n-1) else 3)
# zijtakken (rij 41-45): licht van boven: bovenrij 4, onderrij 2, ertussen 3
for y,x in zip(*np.nonzero(stok)):
    if tak(x,y) and not RAND[y,x]:
        O[y,x]=4 if not stok[y-1,x] or RAND[y-1,x] else (2 if (not stok[y+1,x] or RAND[y+1,x]) else 3)
# ---- opschonen: vlakjes < 3 px van een vultint -> meest voorkomende vultint-buur in dezelfde zone ----
VUL={'stok':[2,3,4],'muts':[12,13,14,5],'baard':[12,13,14],'haar L':[12,13,14],'haar R':[12,13,14]}
for _ in range(3):
    for naam,m in ZONES.items():
        vul=VUL[naam]
        ver=(O!=B)&m
        for k in vul:
            Lc,nc=ndimage.label((O==k)&m&~RAND,np.ones((3,3)) if naam in ('stok','muts') else None)
            for i in range(1,nc+1):
                c=Lc==i
                if c.sum()>=3 or not (c&ver).any(): continue
                ys,xs=np.nonzero(c)
                nb=[O[y+dy,x+dx] for x,y in zip(xs,ys) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))
                    if m[y+dy,x+dx] and not RAND[y+dy,x+dx] and O[y+dy,x+dx]!=k and O[y+dy,x+dx] in vul and B[y+dy,x+dx]!=5]
                if nb:
                    v=max(set(nb),key=nb.count)
                    for x,y in zip(xs,ys): O[y,x]=v
# losse enkele pixels (4-samenhang) in de groene zones, geen randje langs een nerf: naar de meest voorkomende buur
for naam in ('muts','baard','haar L','haar R'):
    m=ZONES[naam]
    for k in (12,13,14):
        Lc,nc=ndimage.label((O==k)&m)
        for i in range(1,nc+1):
            ys,xs=np.nonzero(Lc==i)
            if len(ys)!=1: continue
            y,x=ys[0],xs[0]
            if O[y,x]==B[y,x] or (B[y,x]==12 and (B[y,x-1]==5 or B[y-1,x]==5)): continue
            nb=[O[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if m[y+dy,x+dx] and O[y+dy,x+dx] in (12,13,14)]
            if nb: O[y,x]=max(set(nb),key=nb.count)
# ---- palet: groene ramp gelijkmatig (keuring_r5 E): 14/13/12; 5 en alle gedeelde indexen gelijk ----
pal=bim.getpalette()[:48]
NIEUW={14:(150,196,104),13:(110,156,82),12:(72,116,62)}
for i,c in NIEUW.items(): pal[i*3:i*3+3]=list(c)
if __name__=='__main__':
    zone_all=np.zeros((64,64),bool)
    for m in ZONES.values(): zone_all|=m
    ver=O!=B
    assert not (ver&~zone_all).any()
    tel={n:int((ver&m).sum()) for n,m in ZONES.items()}
    print('t.o.v. r9:',tel,'rest 0')
    with open('log_r10.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)):
            z=[n for n,m in ZONES.items() if m[y,x]][0]; f.write('%s x=%d y=%d %d->%d\n'%(z,x,y,B[y,x],O[y,x]))
        f.write('palet: 14 (176,210,120)->(150,196,104); 13 (104,150,80)->(110,156,82); 12 (58,98,56)->(72,116,62)\n')
    out=Image.new('P',(64,64)); out.putpalette(pal); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    H='0123456789abcdef'
    for y in range(0,58): print('%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(0,48)))
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',512); os.chdir(HIER)
    ps=[m,sprite('../sprite_r9/gnometrotter_grass.png').resize((512,512),Image.NEAREST),sprite('gnometrotter_grass.png').resize((512,512),Image.NEAREST)]
    W=Image.new('RGB',(3*520,512),'white')
    for k,p in enumerate(ps): W.paste(p,(k*520,0))
    W.save('vel.png')
