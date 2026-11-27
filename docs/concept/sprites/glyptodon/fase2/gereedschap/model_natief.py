# Jordi 27 nov: r4 als basis, stekel+band van r6 op de plek van de stekel in r3_3, staart van r3_3.
# Alles op het natieve Gemini-raster (100x100), daarna 1:1 terug naar 1024 (blokken van 10,24 px).
import sys
sys.path.insert(0,__file__.rsplit('/',1)[0])
from natief import natief
from kaart import klasse, kaart
import numpy as np
from PIL import Image
D=__file__.rsplit('/',2)[0]+'/gemini/'
r4=natief(D+'r4.png').astype(int); r6=natief(D+'r6.png').astype(int); r33=natief(D+'r3_3_Y_A.png').astype(int)
W=np.array([255,255,255]); K=r4[32,55].copy()  # lijnkleur van r4
out=r4.copy()
cls=np.vectorize(lambda y,x: klasse(out[y,x]))
# 1. oude stekel weg
for y in range(0,33):
    for x in range(44,66):
        if klasse(r4[y,x]) in 'G': out[y,x]=W
        if klasse(r4[y,x])=='K' and y<32: out[y,x]=W
# 2. schildrand (lijn) over de top, en vullen tot de oude voet
rand={**{x:23 for x in range(37,49)},49:24,50:24,51:24,52:25,53:25,54:26,55:26,56:27,57:27,58:28,59:29,60:30,61:31}
for x,yt in rand.items():
    out[:yt,x]=np.where((np.arange(yt)[:,None]>=0),W,W) if x>=44 else out[:yt,x]
    out[yt,x]=K
    for y in range(yt+1,33):
        if klasse(out[y,x]) in '.KG': out[y,x]=r4[33,x] if klasse(r4[33,x])!='K' else r4[34,x]
# 2b. schildstrepen: die van r4 weg, die van r6 erin (Jordi: "dan mag je de schildstrepen van het model gebruiken")
if '--strepen' in sys.argv:
    def schildrand(img,y):
        # eerste aaneengesloten run niet-wit vanaf links = schild (+ kop); geeft (links, rechts)
        row=[klasse(img[y,x]) for x in range(100)]
        xs=[x for x in range(100) if row[x]!='.']
        if not xs: return None
        l=xs[0]; r=l
        while r+1<100 and row[r+1]!='.': r+=1
        return l,r
    def vul(y,x):
        # mediaan van de bruine schildcellen in een 7x7-omgeving (geen streep, geen lijn)
        c=[out[yy,xx] for yy in range(max(0,y-3),y+4) for xx in range(max(0,x-3),min(100,x+4)) if klasse(out[yy,xx])=='B']
        return np.median(np.array(c),0).astype(int) if c else out[y,x]
    # r4-strepen weg: E/Y en losse binnenlijnen in het schild, niet de buitenrand en niet de voorrand
    weg=[]
    for y in range(23,62):
        e=schildrand(out,y)
        if not e: continue
        l,r=e
        while r-1>l and klasse(out[y,r-1])=='K': r-=1   # buitenlijn rechts houden
        for x in range(l+1,r):
            k=klasse(out[y,x])
            if y>=46 and x<40: continue      # voorrand/vizier
            if k in 'EY' or (k=='K' and x>=58): weg.append((y,x))
    for y,x in weg: out[y,x]=W*0+np.array([-1,-1,-1])
    for y,x in weg: out[y,x]=vul(y,x)
    # r6-strepen per rij relatief tussen de schildranden overzetten (rij -1)
    for y in range(26,61):
        e6=schildrand(r6,y); e4=schildrand(out,y-1)
        if e6: e6=(e6[0],min(e6[1],76))  # r6: staart raakt het schild vanaf rij 53
        if not e6 or not e4: continue
        for x in range(e6[0],e6[1]+1):
            if klasse(r6[y,x]) not in 'EY': continue
            if 22<=x<=43 and y<=35: continue
            if y>=49 and x<52: continue
            X = e4[1]-(e6[1]-x) if x>(e6[0]+e6[1])/2 else e4[0]+(x-e6[0])  # afstand tot de dichtstbijzijnde rand
            if klasse(out[y-1,X])=='B': out[y-1,X]=r6[y,x]
# 3. stekel+band van r6 (alles behalve schild en wit), verschoven
DX,DY=int(sys.argv[1]),int(sys.argv[2])
KS=float(sys.argv[6]) if len(sys.argv)>6 else 0
for y in range(5,36):
    for x in range(24,44):
        k=klasse(r6[y,x])
        if k in 'EYK' or (k=='B' and x<=27 and y<=22) or (k=='g'):
            if k=='K' and x>42: continue
            sh=int(round(KS*(23-y))) if y<23 else 0  # schuintrekken: stekel rechtop
            out[y+DY,x+DX+sh]=r6[y,x]
# 4. staart r4 weg, staart r3_3 erachter
for y in range(36,82):
    for x in range(74 if y>=63 else 77,100): out[y,x]=W
TX,TY=int(sys.argv[4]),int(sys.argv[5])
for y in range(38,78):
    for x in range(74,100):
        if klasse(r33[y,x])=='.': continue
        if not (x>=80 or 59<=y<=74): continue
        Y,X=y+TY,x+TX
        if 0<=X<100 and 0<=Y<100 and klasse(out[Y,X])=='.': out[Y,X]=r33[y,x]
np.save(sys.argv[3]+'.npy',out)
Image.fromarray(out.astype('uint8')).resize((1024,1024),Image.NEAREST).save(sys.argv[3]+'.png')
Image.fromarray(out.astype('uint8')).resize((800,800),Image.NEAREST).save(sys.argv[3]+'_8x.png')
kaart(out,56,100,36,82)
