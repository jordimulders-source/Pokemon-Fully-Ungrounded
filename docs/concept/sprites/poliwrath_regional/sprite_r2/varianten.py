# Varianten r2: basis = r1 met spiraal S1 (zelfde basis.py/mat.py uit ../sprite_r1), daarop
#  ogen E1/E2: het HELE Gen 3-Poliwrath-oog incl. ronde oogbult/ooglid, ooglid gekleurd naar het model, E1 geschaald naar verhouding, E2 ongeschaald
#  mond M1/M2/M3: nette 1-px rode lijn op plek/breedte van de modelmond, drie vormen.
import sys, os, numpy as np; from PIL import Image
R1=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../sprite_r1'); sys.path.insert(0,R1)
import importlib.util
_cwd=os.getcwd(); os.chdir(R1)
_sp=importlib.util.spec_from_file_location('r1_varianten',os.path.join(R1,'varianten.py')); V1=importlib.util.module_from_spec(_sp); _sp.loader.exec_module(V1)   # r1: BASIS, buurgeel, MONDZ, cls, lum
os.chdir(_cwd)
H,W,cls,lum,jj,ii=V1.H,V1.W,V1.cls,V1.lum,V1.jj,V1.ii
ROOT=os.path.join(R1,'../../../../../')
pwr=np.array(Image.open(ROOT+'graphics/pokemon/poliwrath/anim_front_gba.png'))[:64]
# ---------- OGEN ----------
# Bronvensters in de Gen 3-Poliwrath (frame 1): oogbult van top (rij 9) tot onderrand oog (rij 19)
SRC={'L':(19,30,9,19),'R':(37,49,9,19)}          # x0,x1,y0,y1  -> 12x11 en 13x11
# Verhouding: kop/lijf Poliwrath op ooghoogte (rij 16) x 19-51 = 33 px; kop hier op ooghoogte (rij 7) x 15-43 = 29 px -> factor 29/33 = 0,879
F=29/33
WIT=(1,2,3); PUP=0xa
def bron(z):
    x0,x1,y0,y1=SRC[z]; return pwr[y0:y1+1,x0:x1+1].copy()
def schrap(sub,nc,nr,z):
    # schrap nc kolommen en nr rijen die het meest op hun buur lijken, niet door de pupil(rij/kolom) en niet de buitenste
    py,px=[int(v[0]) for v in np.where(sub==PUP)]
    def kies(a,n,axis,verb):
        B=a if axis==0 else a.T
        cost=[(np.sum(B[i]!=B[i+1]),i) for i in range(1,len(B)-2)]
        g=[]
        for c,i in sorted(cost):
            if i in verb or i+1 in verb: continue
            if all(abs(i-j)>=3 for j in g): g.append(i)
            if len(g)==n: break
        return sorted(g)
    rows=kies(sub,nr,0,{py}); cols=kies(sub,nc,1,{px})
    return np.delete(np.delete(sub,rows,0),cols,1),rows,cols
MAAT={'E1':{'L':None,'R':None},'E2':{'L':(0,0),'R':(0,0)}}
for z in 'LR':
    h,w=bron(z).shape
    MAAT['E1'][z]=(w-int(round(w*F)),h-int(round(h*F)))   # aantal te schrappen kolommen, rijen
def kopmat(y,x):
    # modelmateriaal op de doelplek; buiten de kop (lucht/ijs): dichtstbijzijnde kopcel (geel of zwart)
    if 0<=y<H and 0<=x<W and cls[y,x] in (1,4): return cls[y,x]
    best=None
    for yy in range(max(0,y-4),min(H,y+5)):
        for xx in range(max(0,x-4),min(W,x+5)):
            if cls[yy,xx] in (1,4) and yy<=19:
                d=(yy-y)**2+(xx-x)**2
                if best is None or d<best[0]: best=(d,cls[yy,xx])
    return best[1] if best else 1
LID={1:{0xb:5,0xc:6,0xd:7},4:{0xb:4,0xc:3,0xd:2}}
MODWIT={'L':17,'R':39}; MODONDER=10      # buitenrand en onderrij van het modeloogwit (r1-meting, gespiegeld model)
INFO={}
def oog(o,e,z):
    sub=bron(z); nc,nr=MAAT[e][z]; rows=cols=[]
    if nc or nr: sub,rows,cols=schrap(sub,nc,nr,z)
    h,w=sub.shape
    wy,wx=np.where(np.isin(sub,WIT))
    ox=wx.min() if z=='L' else wx.max()
    dx=MODWIT[z]-ox; dy=MODONDER-wy.max()
    for j in range(h):
        for i in range(w):
            p=sub[j,i]
            if p==0: continue
            y,x=j+dy,i+dx
            if not(0<=y<H and 0<=x<W): continue
            if p in (0xe,0xa): q=1
            elif p==1: q=8
            elif p in (2,3): q=9
            elif p in (0xb,0xc,0xd): q=LID[kopmat(y,x)][p]
            else: q=1
            o[y,x]=q
    # schaalrand/silhouetrand opschonen: geplakte lidpixels (kop-tinten) die nu aan lucht grenzen -> omlijning zoals in basis.py
    # (geel: 7 aan de lichtkant, 1 aan de schaduwkant; zwart: 1)
    rand=[]
    for j in range(h):
        for i in range(w):
            y,x=j+dy,i+dx
            if sub[j,i] not in (0xb,0xc,0xd) or not(0<=y<H and 0<=x<W): continue
            L_=lambda a,b: not(0<=a<H and 0<=b<W) or o[a,b]==0
            if not any(L_(y+a,x+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1))): continue
            sx=sum(b for a in (-1,0,1) for b in (-1,0,1) if L_(y+a,x+b)); sy=sum(a for a in (-1,0,1) for b in (-1,0,1) if L_(y+a,x+b))
            q=7 if (o[y,x] in (5,6,7) and sx+sy<=0) else 1
            if o[y,x]!=q: rand.append((int(x),int(y),int(o[y,x]),q)); o[y,x]=q
    INFO[(e,z)]=dict(rand=rand,maat=(w,h),geschrapt_rijen=rows,geschrapt_kolommen=cols,plek=(dx,dy,dx+w-1,dy+h-1))
# ---------- MOND ----------
# (x0,x1,rij) segmenten; plek/breedte modelmond x 15-41, midden onder de neusgaten (rij 13) op rij 15
MOND={'M1':[(15,16,17),(17,20,16),(21,35,15),(36,39,16),(40,41,17)],               # boog: 2-4-15-4-2
      'M2':[(15,15,17),(16,16,16),(17,39,15),(40,40,16),(41,41,17)],               # recht midden, mondhoeken 1:1 omlaag geknikt: 1-1-23-1-1
      'M3':[(15,15,17),(16,19,16),(20,25,15),(26,30,16),(31,36,15),(37,40,16),(41,41,17)]}  # golf: 1-4-6-5-6-4-1
def mond(o,m):
    V1.buurgeel(o,V1.MONDZ)          # modelglimlach -> geel uit de kop (zoals r1)
    for x0,x1,y in MOND[m]:
        for x in range(x0,x1+1): o[y,x]=13
def maak(e,m):
    o=V1.BASIS.copy()                 # r1-basis; spiraal S1 = modelspiraal = BASIS zelf
    mond(o,m); oog(o,e,'L'); oog(o,e,'R')
    return o
