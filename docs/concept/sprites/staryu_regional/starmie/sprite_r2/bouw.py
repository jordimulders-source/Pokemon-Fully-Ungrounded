# bouw.py r2: voorste ster = r1 (bevroren); achterster = ACHTERSTE ster van de Gen 3 Starmie (set A), verticaal
# gespiegeld (y -> 60-y, kern y30) en DX/DY verschoven, herbelicht (licht linksboven), chips in eigen chocoladetint.
# Gebruik: cd starmie && python3 sprite_r2/bouw.py [DX DY NAAM]
import sys, json; sys.path.insert(0,'gereedschap'); from gemeen import *; from kaal import voorste
DX,DY,NAAM=(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]) if len(sys.argv)>3 else (0,3,'starmie_r2')
# palet r2: geel hagel (15) samengevoegd met koek licht (6); 15 = chocolade
import gemeen
PAL=list(gemeen.PAL); PAL[6]=(250,218,128); PAL[15]=(124,80,56); gemeen.PAL[:]=PAL
CHOC=15
r1=np.asarray(Image.open('sprite_r1/starmie_r1.png')).astype(int).copy()
r1[r1==15]=6                                        # gele hagelslag -> samengevoegde tint
_,fm=voorste(); g,_=laad_g3()
SETA=('top','r','br','bl','l')
from gen3 import TIPS, C
# 1. gespiegelde achterster
B=np.zeros((64,64),int); LAB=np.full((64,64),'',object)
for y,x in zip(*np.where(np.isin(g,[1,2,3,4,14]))):
    n=punt_van(x,y)
    if n not in SETA: continue
    X=x+DX; Y=60-y+DY
    v=g[y,x]
    if v==4:   # donkerste paars: binnenin = donkere facet (5), op de rand van de punt = lijn (4)
        rand=any(g[y+j,x+i] in (0,14) or punt_van(x+i,y+j)!=n or g[y+j,x+i] in (5,6,7,8) for j,i in ((-1,0),(1,0),(0,-1),(0,1)))
        v=4 if rand else 5
    if 0<=X<64 and 0<=Y<64 and not fm[Y,X]: B[Y,X]=v; LAB[Y,X]=n
# 2. herbelichten per punt: facetten = Gen 3-tinten 1-3; de kant van de puntas die naar linksboven kijkt wordt licht
o=np.where(fm,r1,0); log={}
def zet(x,y,k,stap):
    if o[y,x]!=k: o[y,x]=k; log.setdefault(stap,[]).append((int(x),int(y)))
cx,cy=C[0]+DX,60-C[1]+DY
info={}
for n in SETA:
    tx,ty=TIPS[n]; tx,ty=tx+DX,60-ty+DY
    ax=np.array([tx-cx,ty-cy],float); ax/=np.linalg.norm(ax)
    perp=np.array([-ax[1],ax[0]]); licht=1 if perp@np.array([-1,-1])>0 else -1
    pts=[(x,y) for y,x in zip(*np.where(LAB==n))]
    side={}
    for t in (1,2,3,5):
        s=[np.sign((np.array([x-cx,y-cy])@perp)) for x,y in pts if B[y,x]==t]
        if s: side[t]=np.mean(s)*licht   # >0: toon ligt overwegend aan de lichte kant
    lit=[t for t in side if side[t]>0]; sch=[t for t in side if side[t]<=0]
    m={4:2,14:1}
    for t in lit: m[t]=5 if t==min(lit) else 4          # lichte facet: lichtste toon midden, rest oranje
    for t in sch: m[t]=3 if t==max(sch) else 4           # schaduwfacet: donkerste toon schaduw, rest oranje
    info[n]=(side,m)
    for x,y in pts: zet(x,y,m[B[y,x]],'achterster')
# 3. buitenlijn (alleen achterster en voorste-sterpixels die nu aan transparant grenzen): rechts/onder zwart, links/boven donker
fg=o>0
for y,x in zip(*np.where(fg)):
    r=not fg[y,x+1]; b=not fg[y+1,x]; l=not fg[y,x-1]; t=not fg[y-1,x]
    if not (r or b or l or t) or o[y,x]==1: continue
    if fm[y,x]:
        r1fg=r1>0  # in r1 al randpixel? dan bevroren
        if o[y,x] in (1,2): continue
    if r or b: zet(x,y,1,'buitenlijn')
    elif o[y,x]!=2: zet(x,y,2,'buitenlijn')
# 4. binnenlijn: achterpixel die aan de voorste ster grenst (niet zwart) = koek donker
for y,x in zip(*np.where((o>0)&~fm)):
    if o[y,x] in (1,2): continue
    if any(fm[y+dy,x+dx] and o[y+dy,x+dx]!=1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): zet(x,y,2,'binnenlijn achter')
# 5. losse zwarte pixels in de achterster -> donker
for y,x in zip(*np.where((o==1)&~fm)):
    if all(o[y+dy,x+dx]!=1 for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): zet(x,y,2,'losse zwarte pixel')
# 6. chips: 2 per punt, 2 px, op de lichte facet (M) met alleen vulbuurs
FILL=(3,4,5)
for n in SETA:
    kand=[]
    def binnen(x,y): return o[y,x] in FILL and not fm[y,x] and all(o[y+dy,x+dx] in FILL and not fm[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
    for y,x in zip(*np.where(LAB==n)):
        if o[y,x]!=5 or not binnen(x,y): continue
        if o[y,x+1]==5 and binnen(x+1,y): kand.append((x,y,x+1,y))
        elif o[y+1,x]==5 and binnen(x,y+1): kand.append((x,y,x,y+1))
    tx,ty=TIPS[n]; tx,ty=tx+DX,60-ty+DY
    kand.sort(key=lambda c:(c[0]-tx)**2+(c[1]-ty)**2)
    gek=[]
    for c in kand:
        if all(max(abs(c[0]-k[0]),abs(c[1]-k[1]))>=3 for k in gek): gek.append(c)
        if len(gek)==2: break
    for x0,y0,x1,y1 in gek: zet(x0,y0,CHOC,'chips'); zet(x1,y1,CHOC,'chips')
    info[n]=info[n]+(gek,)
opslaan(o,'sprite_r2/%s.png'%NAAM)
diff=(o!=r1); print(NAAM,'DX',DX,'DY',DY)
print('voorste ster diff t.o.v. r1 (na geel->licht):',int((diff&fm).sum()),[(int(x),int(y),CH[r1[y,x]]+'>'+CH[o[y,x]]) for y,x in zip(*np.where(diff&fm))])
fy,fx=np.where(fm)
for n in SETA:
    m=(LAB==n); ys,xs=np.where(m)
    L=max(np.sqrt(((fx-x)**2+(fy-y)**2).min()) for y,x in zip(ys,xs))
    print(n,'px',int(m.sum()),'lengte buiten voorste ster %.1f'%L,'facetten',info[n][0],'chips',info[n][2])
for k,v in log.items(): print(k,len(v))
fg=o>0; yy,xx=np.where(fg); print('figuur x%d-%d y%d-%d %dx%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
